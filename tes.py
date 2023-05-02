import random
from time import sleep
import pygame

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

    def draw(self, game_display):
        game_display.blit(self._image, (self._x, self._y))

    def get_rect(self):
        return pygame.Rect(self._x, self._y, self._width, self._image.get_height())


class EnemyCar(Vehicle):
    def __init__(self, x, y, width, height, image, speed):
        super().__init__(x, y, width, image)
        self.height = height
        self.speed = speed

    def move_down(self):
        self._y += self.speed
        if self._y > 600:
            self._y = 0 - self.height
            self._x = random.randrange(310, 450)

    def draw(self, game_display):
        game_display.blit(self._image, (self._x, self._y))

    def get_rect(self):
        return pygame.Rect(self._x, self._y, self._width, self.height)

class Background:
    def __init__(self, display_width):
        self.backgroundImg = pygame.image.load(".\\img\\back_ground.jpg")
        self.bg_x1 = (display_width / 2) - (360 / 2)
        self.bg_x2 = (display_width / 2) - (360 / 2)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 3
        self.count = 0

class CarRacing:
    def __init__(self):

        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.game_display = None
        self.program_icon = pygame.image.load('.\\img\\car_Icon.png')
        pygame.display.set_icon(self.program_icon)

        self.initialize()

    def initialize(self):
        self.crashed = False

        self.car = Car(self.display_width * 0.45, self.display_height * 0.8, 49, pygame.image.load('.\\img\\car.png'))

        # enemy_car
        self.enemy_car = EnemyCar(random.randrange(310, 450), -600, 49, 100, pygame.image.load('.\\img\\enemy_car_1.png'), 5)

        # Background
        self.bgImg = Background(self.display_width)

    def racing_window(self):
        self.game_display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Car Race')
        self.run_car()

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
            self.back_ground_raod()

            self.enemy_car.draw(self.game_display)
            self.enemy_car.move_down()

            if self.car.get_rect().colliderect(self.enemy_car.get_rect()):
                self.crashed = True
                self.display_message("Game Over !!!")

            if self.enemy_car._y > self.display_height:
                self.enemy_car.move_down()
                self.count += 1

            self.car.draw(self.game_display)
            self.highscore(self.bgImg.count)
            self.bgImg.count += 1
            if (self.bgImg.count % 100 == 0):
                self.enemy_car.speed += 1
                self.bgImg.bg_speed += 1

            if self.car._y < self.enemy_car._y + self.enemy_car.height:
                if self.car._x > self.enemy_car._x and self.car._x < self.enemy_car._x + self.enemy_car._width or self.car._x + self.car._width > self.enemy_car._x and self.car._x + self.car._width < self.enemy_car._x + self.enemy_car._width:
                    self.crashed = True
                    self.display_message("Game Over !!!")

            if self.car._x < 310 or self.car._x > 460:
                self.crashed = True
                self.display_message("Game Over !!!")

            pygame.display.update()
            self.clock.tick(60)

    def display_message(self, msg):
        font = pygame.font.SysFont("comicsansms", 72, True)
        text = font.render(msg, True, (255, 255, 255))
        self.game_display.blit(text, (400 - text.get_width() // 2, 240 - text.get_height() // 2))
       
        pygame.display.update()
        self.clock.tick(60)
        sleep(1)
        car_racing.initialize()
        car_racing.racing_window()

    def back_ground_raod(self):
        self.game_display.blit(self.bgImg.backgroundImg, (self.bgImg.bg_x1, self.bgImg.bg_y1))
        self.game_display.blit(self.bgImg.backgroundImg, (self.bgImg.bg_x2, self.bgImg.bg_y2))

        self.bgImg.bg_y1 += self.bgImg.bg_speed
        self.bgImg.bg_y2 += self.bgImg.bg_speed

        if self.bgImg.bg_y1 >= self.display_height:
            self.bgImg.bg_y1 = -600

        if self.bgImg.bg_y2 >= self.display_height:
            self.bgImg.bg_y2 = -600

    def run_enemy_car(self, thingx, thingy):
        self.game_display.blit(self.enemy_car, (thingx, thingy))

    def highscore(self, count):
        font = pygame.font.SysFont("lucidaconsole", 20)
        text = font.render("Score : " + str(count), True, self.white)
        self.game_display.blit(text, (0, 0))

if __name__ == '__main__':
    car_racing = CarRacing()
    car_racing.racing_window()
