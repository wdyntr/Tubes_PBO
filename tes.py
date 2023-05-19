import random
from time import sleep #memberi jeda program dalam jangka waktu tertentu
import pygame
from pygame import mixer #memberikan suara
from abc import ABC, abstractmethod
from button import Button

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
        self.heart = 3

    def draw(self, game_display):
        game_display.blit(self._image, (self._x, self._y))

    def get_rect(self):
        return pygame.Rect(self._x, self._y, self._width, self._image.get_height())

    def lose_life(self):
        self.heart -= 1

    def life_increases(self):
        self.heart += 1
        
    def is_alive(self):
        return self.heart > 0


class EnemyCar(Vehicle):
    def __init__(self, x, y, width, height, image, speed):
        super().__init__(x, y, width, image)
        self.height = height
        self.speed = speed

    def move_down(self):
        self._y += self.speed
        if self._y > 600:
            self._y = 0 - self.height #?
            self._x = random.randrange(70, 900)

    def draw(self, game_display):
        game_display.blit(self._image, (self._x, self._y))

    def get_rect(self):
        return pygame.Rect(self._x, self._y, self._width, self.height)

class Background:
    def __init__(self, display_width):
        self.backgroundImg = pygame.image.load(".\\img\\back2.jpg")
        self.bg_x1 = (display_width / 2) - (1000 / 2) #?
        self.bg_x2 = (display_width / 2) - (1000 / 2) #?
        self.bg_y1 = 0 #?
        self.bg_y2 = -600 #?
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
        self.y = -1200
        self.x = random.randrange(70, 900)

class StreetCarRacing:
    def __init__(self):
        
        pygame.init() #Double?
        pygame.mixer.init()
        self.SCREEN = pygame.display.set_mode((1000, 600))
        self.BG = pygame.image.load(".\\img\\Background.png") #
        self.crash_sound = pygame.mixer.Sound('.\\sound\\explosion.wav')
        self.crash_sound.set_volume(0.5)
        self.display_width = 1000
        self.display_height = 600
        self.clock = pygame.time.Clock()
        self.tambah_enemy_cars = []
        mixer.music.load('.\\sound\\background.wav')
        mixer.music.play(-1)
        self.ledakan = []
        self.heart = pygame.image.load('.\\img\\heart.png')
        self.bom_sound = pygame.mixer.Sound('.\\sound\\bom.mp3')
        self.bom_sound.set_volume(0.5)
        self.score = 0
        self.FPS = 60
        self.game_display = None
        self.program_icon = pygame.image.load('.\\img\\car_Icon.png')
        pygame.display.set_caption('Street Car Racing')
        pygame.display.set_icon(self.program_icon)

        self.inisialisasi()

    def inisialisasi(self):
        self.crashed = False

        self.car = Car(self.display_width * 0.35, self.display_height * 0.8, 49, pygame.image.load('.\\img\\car.png'))

        # item bom yang dapat menghilangkan musuh. item ini akan muncul ketika darah user tersisa satu
        self.item = Item(pygame.image.load(".\\img\\bom.png"))

        # item heart yang akan muncuk ketika nyawa player kurang dari 3
        self.item_heart = Item(pygame.image.load(".\\img\\heart.png"))

        # ledakan
        for i in range(8):
            img = pygame.image.load(f'.\\img\\ledakan{i}.png')
            self.ledakan.append(pygame.transform.scale(img, (100, 100)))

        # Background
        self.bgImg = Background(self.display_width)

    # def racing_window(self):
    #     self.game_display = pygame.display.set_mode((self.display_width, self.display_height))
    #     self.run_car()

    def heart_img(self):
        self.heart_width = self.heart.get_width()
        self.heart_height = self.heart.get_height()

        for i in range(self.car.heart):
            x = 850 + i * (self.heart_width)
            y = 0
            self.game_display.blit(self.heart, (x, y))
    
    def show_ledakan(self, x, y):
        for img in self.ledakan:
            self.game_display.blit(img, (x, y))
            pygame.display.update()
            pygame.time.wait(50)

    def get_font(self, size): # Returns Press-Start-2P in the desired size
        return pygame.font.Font(".\\font\\ethnocentric rg.otf", size)

    def main_menu(self):
        while True:
            self.SCREEN.blit(self.BG, (0, 0))
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()
            self.MENU_TEXT = self.get_font(70).render("MAIN MENU", True, "#b68f40")
            self.MENU_RECT = self.MENU_TEXT.get_rect(center = (500, 50))
            
            #top score
            # if self.score != 0:
            #     self.SCORE_TEXT = self.get_font(50).render("SCORE: " + str(self.score), True, "#b68f40")
            #     self.SCORE_RECT = self.SCORE_TEXT.get_rect(center = (500, 250))

            self.PLAY_BUTTON = Button(image=pygame.image.load(".\\img\\Menu Rect.png"), pos = (500, 300), 
                                text_input="PLAY", font = self.get_font(50), base_color="#d7fcd4", hovering_color="white")
            self.QUIT_BUTTON = Button(image=pygame.image.load(".\\img\\Menu Rect.png"), pos = (500, 450), 
                                text_input="QUIT", font = self.get_font(50), base_color="#d7fcd4", hovering_color="white")

            self.SCREEN.blit(self.MENU_TEXT, self.MENU_RECT)

            for button in [self.PLAY_BUTTON, self.QUIT_BUTTON]:
                button.changeColor(self.MENU_MOUSE_POS)
                button.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.PLAY_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                        self.run_car()
                        pygame.quit() #agar tidak ada double window
                    if self.QUIT_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                        pygame.quit()

            pygame.display.update()

    def run_car(self):
        self.game_display = pygame.display.set_mode((self.display_width, self.display_height))
        self.car.heart = 3
        self.score = 0

        while not self.crashed:
            self.game_display.fill("black")
            self.Background_road()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True
                # print(event)
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_LEFT or event.key == pygame.K_a):
                        self.car._x -= 50
                    if (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                        self.car._x += 50 

            while len(self.tambah_enemy_cars) < 2:
                for i in range(4):
                    x = random.randrange(60, 900)
                    y = random.randrange(-600, 0)
                    if i % 2:
                        self.enemy_car = EnemyCar(x, y, 49, 100, pygame.image.load('.\\img\\enemy_car_1.png'), 1)
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

            self.heart_img()
            self.car.draw(self.game_display)
            self.score += 1
            self.Show_score(self.score)
            self.bgImg.count += 1
            if (self.bgImg.count % 100 == 0):
                self.enemy_car.speed += 0.1
                self.bgImg.bg_speed += 1

            # jika nyawa player kurang dari 3 maka item heart akan muncul untuk menambah nyawa player
            if self.car.heart < 3:
                self.item_heart.move_down(self.game_display)
                if self.item_heart.y > 600:
                    self.item_heart.remove()

                if self.item_heart.get_Rect().colliderect(self.car.get_rect()):
                    self.item_heart.remove()
                    self.car.life_increases()

            # item bom yang akan muncul ketika darah mobil tersisa satu
            if (self.car.heart == 1):
                self.item.move_down(self.game_display)
                if self.item.y > 600:
                    self.item.remove()

                if self.item.get_Rect().colliderect(self.car.get_rect()):
                    self.item.remove()
                    self.bom_sound.play()
                    for self.enemy_car in self.tambah_enemy_cars:
                        self.enemy_car._y = -600
                        self.enemy_car._x = random.randrange(70, 900)

            if self.car._x < 50 or self.car._x > 920: 
                self.crash_sound.play()
                self.show_ledakan(self.car._x, self.car._y)
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

        #pengkondisian agar kembali ke menu
        if self.crashed:
            self.crashed = False
            sleep(1)
            self.main_menu()

        #Mengulang kembali permainan
        # self.inisialisasi()
        # self.racing_window()

    def Background_road(self):
        self.game_display.blit(self.bgImg.backgroundImg, (self.bgImg.bg_x1, self.bgImg.bg_y1))
        self.game_display.blit(self.bgImg.backgroundImg, (self.bgImg.bg_x2, self.bgImg.bg_y2))

        self.bgImg.bg_y1 += self.bgImg.bg_speed
        self.bgImg.bg_y2 += self.bgImg.bg_speed

        if self.bgImg.bg_y1 >= self.display_height:
            self.bgImg.bg_y1 = -600

        if self.bgImg.bg_y2 >= self.display_height:
            self.bgImg.bg_y2 = -600

    def Show_score(self, count):
        font = pygame.font.SysFont("lucidaconsole", 20)
        text = font.render("Score : " + str(count), True, "white")
        self.game_display.blit(text, (60, 0))

if __name__ == '__main__':
    car_racing = StreetCarRacing()
    car_racing.main_menu()
