import random
from time import sleep
import pygame
from pygame import mixer
from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, x, y, width, image):
        self._x = x
        self._y = y
        self._width = width
        self._image = image

    @abstractmethod
    def draw(self, game_display):
        pass

    @abstractmethod
    def get_rect(self):
        pass


class Car(Vehicle):
    def __init__(self, x, y, width, image):
        super().__init__(x, y, width, image)
        self.lives = 3

    def draw(self, game_display):
        game_display.blit(self._image, (self._x, self._y))

    def get_rect(self):
        return pygame.Rect(self._x, self._y, self._width, self._image.get_height())

    def lose_life(self):
        self.lives -= 1
        
    def is_alive(self):
        return self.lives > 0


class EnemyCar(Vehicle):
    def __init__(self, x, y, width, height, image, speed):
        super().__init__(x, y, width, image)
        self.height = height
        self.speed = speed

    def move_down(self):
        self._y += self.speed
        if self._y > 600:
            self._y = 0 - self.height
            self._x = random.randrange(70, 900)

    def draw(self, game_display):
        game_display.blit(self._image, (self._x, self._y))

    def get_rect(self):
        return pygame.Rect(self._x, self._y, self._width, self.height)

class Background:
    def __init__(self, display_width):
        self.backgroundImg = pygame.image.load(".\\img\\back2.jpg")
        self.bg_x1 = (display_width / 2) - (1000 / 2)
        self.bg_x2 = (display_width / 2) - (1000 / 2)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 3
        self.count = 0

class Item:
    def __init__(self, image):
        self.x = random.randrange(70, 900)
        self.y = -400
        self.img_item = image
    
    def move_down(self, game_display):
        self.y += 3
        game_display.blit(self.img_item, (self.x, self.y))

    def get_Rect(self):
        return pygame.Rect(self.x, self.y, self.img_item.get_width(), self.img_item.get_height())

    def remove(self):
        self.y = -600

class StreetCarRacing:
    def __init__(self):
        
        pygame.init()
        pygame.mixer.init()
        self.crash_sound = pygame.mixer.Sound('.\\sound\\explosion.wav')
        self.crash_sound.set_volume(0.5)
        self.display_width = 1000
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.tambah_enemy_cars = []
        mixer.music.load('.\\sound\\background.wav')
        mixer.music.set_volume(1)
        mixer.music.play(-1)
        self.ledakan = []
        self.FPS = 60
        self.heart = pygame.image.load('.\\img\\heart.png')
        self.score = 0
        self.enemy_car_spacing = 150  # Jarak antara setiap EnemyCar
        self.game_display = None
        self.program_icon = pygame.image.load('.\\img\\car_Icon.png')
        pygame.display.set_icon(self.program_icon)

        self.inisialisasi()

    def inisialisasi(self):
        self.crashed = False

        self.car = Car(self.display_width * 0.35, self.display_height * 0.8, 49, pygame.image.load('.\\img\\car.png'))

        # enemy_car
        # self.enemy_car = EnemyCar(random.randrange(80, 900), -600, 49, 100, pygame.image.load('.\\img\\enemy_car_1.png'), 5)
        self.item = Item(pygame.image.load(".\\img\\bom.png"))

        # ledakan
        for i in range(7):
            img = pygame.image.load(f'.\\img\\ledakan{i}.png')
            self.ledakan.append(pygame.transform.scale(img, (100, 100)))

        # Background
        self.bgImg = Background(self.display_width)

    def racing_window(self):
        self.game_display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Street Car Racing')
        self.run_car()

    def heart_img(self):
        heart_width = self.heart.get_width()
        heart_height = self.heart.get_height()

        for i in range(self.car.lives):
            x = 850 + i * (heart_width)
            y = 10
            self.game_display.blit(self.heart, (x, y))
    
    def show_ledakan(self, x, y):
        for img in self.ledakan:
            self.game_display.blit(img, (x, y))
            pygame.display.update()
            pygame.time.wait(50)

    def run_car(self):

        while not self.crashed:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True
                # print(event)

                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_LEFT or event.key == pygame.K_a):
                        self.car._x -= 50
                    if (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                        self.car._x += 50 
                                        

            self.game_display.fill(self.black)
            self.Background_raod()

            while len(self.tambah_enemy_cars) < 3:
                for i in range(3):
                    x = random.randrange(60, 900)
                    y = -600 - self.enemy_car_spacing
                    if len(self.tambah_enemy_cars) % 2:
                        self.enemy_car = EnemyCar(x, y, 49, 100, pygame.image.load('.\\img\\enemy_car_1.png'), 2)
                        self.tambah_enemy_cars.append(self.enemy_car)
                    else:
                        self.enemy_car = EnemyCar(x, y, 49, 100, pygame.image.load('.\\img\\enemy_car_2.png'), 3)
                        self.tambah_enemy_cars.append(self.enemy_car)

            for self.enemy_car in self.tambah_enemy_cars:
                self.enemy_car.draw(self.game_display)
                self.enemy_car.move_down()

                if self.car.get_rect().colliderect(self.enemy_car.get_rect()):
                    self.car.lose_life()
                    self.tambah_enemy_cars.remove(self.enemy_car)
                    self.crash_sound.play()
                    self.show_ledakan(self.car._x, self.car._y)

                    if not self.car.is_alive():
                        self.crashed = True
                        self.display_message("Game Over !!!")
                        break

            for self.enemy_car in self.tambah_enemy_cars:
                self.enemy_car.move_down()
                if self.enemy_car._y > self.display_height:
                    self.enemy_car.move_down()

            self.heart_img()
            self.car.draw(self.game_display)
            self.score += 1
            self.show_score(self.score)
            self.bgImg.count += 1
            if (self.bgImg.count % 100 == 0):
                self.enemy_car.speed += 0.1
                self.bgImg.bg_speed += 1

            # item bom yang akan muncul ketika darah mobil tersisa satu
            if (self.car.lives == 1):
                self.item.move_down(self.game_display)
                if self.item.y > 600:
                    self.item.remove()

                if self.item.get_Rect().colliderect(self.car.get_rect()):
                    self.item.remove()   
                    for self.enemy_car in self.tambah_enemy_cars:
                        self.enemy_car._y = -600

            if self.car._x < 50 or self.car._x > 920: 
                self.show_ledakan(self.car._x, self.car._y)
                self.crash_sound.play()
                if self.car._x < 50 :
                    self.car._x += 50
                else :
                    self.car._x -= 50
                self.car.lose_life()

                if not self.car.is_alive():
                    self.crashed = True
                    self.display_message("Game Over !!!")
                    break

            pygame.display.update()
            self.clock.tick(self.FPS)

    def display_message(self, msg):
        font = pygame.font.SysFont("comicsansms", 72, True)
        text = font.render(msg, True, (255, 255, 255))
        self.game_display.blit(text, (500 - text.get_width() // 2, 300 - text.get_height() // 2))
       
        pygame.display.update()
        self.clock.tick(self.FPS)
        sleep(1)
        car_racing.inisialisasi()
        car_racing.racing_window()

    def Background_raod(self):
        self.game_display.blit(self.bgImg.backgroundImg, (self.bgImg.bg_x1, self.bgImg.bg_y1))
        self.game_display.blit(self.bgImg.backgroundImg, (self.bgImg.bg_x2, self.bgImg.bg_y2))

        self.bgImg.bg_y1 += self.bgImg.bg_speed
        self.bgImg.bg_y2 += self.bgImg.bg_speed

        if self.bgImg.bg_y1 >= self.display_height:
            self.bgImg.bg_y1 = -600

        if self.bgImg.bg_y2 >= self.display_height:
            self.bgImg.bg_y2 = -600

    # score bertambah berdasarkan iterasi loop while pada metode run_car()
    def show_score(self, count):
        font = pygame.font.SysFont("lucidaconsole", 20)
        text = font.render("Score : " + str(count), True, self.white)
        self.game_display.blit(text, (60, 0))

if __name__ == '__main__':
    car_racing = StreetCarRacing()
    car_racing.racing_window()
