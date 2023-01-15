import random
import time

import arcade
from math import pi, sin, cos, acos
from time import sleep


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_COLOR = arcade.color.AIR_FORCE_BLUE
SCREEN_TITLE = "DUCK_HUNT"
COOL_DOWN = 5
LVL = "1"
LVL_UP_COUNT = 10
SOUND = arcade.load_sound("img/backsound2.wav")
SOUNDGUN = arcade.load_sound("img/shoot.mp3")
BACKGROUND = arcade.load_texture("img/fons2.jpg")
ysl = 0
UPDOWN = 0

def get_distance(obj1, obj2):
    return ((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2) ** 0.5

class Cross_hare:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.cool_down = 0
        self.texturecrosshair = arcade.load_texture("img/crosshair.png")

    def draw(self):
       #arcade.draw_point(self.x, self.y, [0, 200, 200], 10)
        self.texturecrosshair.draw(self.x, self.y, 30, 30)
        if self.cool_down > 0:
            arcade.draw_point(self.x+1, self.y+1,[0, 0, 0], 5)


        # arcade.draw_text(str(self.get_degree()), self.x + 5, self.y + 5,[200, 0, 0], 14)

    def update(self):
        if self.cool_down > 0:
            self.cool_down -= 1

    def shoot(self):
        self.cool_down = COOL_DOWN
        arcade.play_sound(SOUNDGUN)

      # arcade.stop_sound(SOUNDGUN)



    def move_to(self, x, y):
        self.x = x
        self.y = y



    def get_degree(self):
        dx = self.x - SCREEN_WIDTH / 2
        dy = self.y - 0
        r = (dx ** 2 + dy ** 2) ** 0.5
        return acos(dx / r) * 180 / pi

class Dog:
    def __init__(self):
        self.x = 70
        self.y = 133
        self.dog = arcade.load_texture("img/dog.gif")

    def draw(self):
        self.dog.draw(self.x, self.y, 210, 210)

    def move(self):
            self.x += 5

class Duck:
    def __init__(self):
        self.x = random.randint(70, SCREEN_WIDTH-70)
        self.y = 50
        self.degrees = random.randint(45, 135)
        self.speed = 2
        self.dx = cos(self.degrees * pi / 180)
        self.dy = sin(self.degrees * pi / 180)
        self.cross = Cross_hare()
        self.texture = arcade.load_texture("img/duck.png")
        self.texture2 = arcade.load_texture("img/duck2.png")
        self.texture3 = arcade.load_texture("img/duck3.png")
        self.texture4 = arcade.load_texture("img/duck4.png")
        self.duckdown = arcade.load_texture("img/Duckdown.png")

    def move(self):

        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def move2(self):

        self.y -= 5


    def draw(self):
        if self.degrees >= 90 :

            self.texture.draw(self.x, self.y, 70, 70, self.degrees - 180)




        else:

            self.texture2.draw(self.x, self.y, 70, 70, self.degrees)

    def draw2(self):
        self.duckdown.draw(self.x, self.y, 70, 70)


    def is_out(self):
        return self.x < -10 or self.x > SCREEN_WIDTH + 10 or self.y > SCREEN_HEIGHT + 10

    def check_strike(self, cross):
        if cross.cool_down > 0:
            return get_distance(self, cross) < 30
        else:
            return False

        # arcade.draw_point(self.x, self.y, [200, 0, 0], 50)

class Anime:
    def __init__(self):
        self.starts1 = arcade.load_texture("img/Welcome1.png")
        self.starts2 = arcade.load_texture("img/Welcome2.png")

    def draw(self):
        if random.randint(1,2) == 1:
            self.starts1.draw(400,300,800,600)
        else:
            self.starts2.draw(400,300,800,600)

class End:
    def __init__(self):
        self.go1 = arcade.load_texture("img/GO 1.png")
        self.go2 = arcade.load_texture("img/GO 2.png")

    def draw(self):
        if random.randint(1,2) == 1:
            self.go1.draw(400,300,800,600)
        else:
            self.go2.draw(400,300,800,600)

class MyGame(arcade.Window):
    """ Главный класс приложения. """

    def __init__(self, width, height):
        super().__init__(width, height, SCREEN_TITLE)
        arcade.play_sound(SOUND)
        arcade.set_background_color(SCREEN_COLOR)
        self.file = open('score.txt', 'a')
        self.choose = arcade.load_texture("img/choose1.png")
        self.backbround = arcade.load_texture("img/fons2.jpg")
        self.start1 = arcade.load_texture("img/Welcome1.png")
        self.start2 = arcade.load_texture("img/Welcome2.png")
        self.step = 0
        self.statys = 0
        self.lvl = 1
        self.LVL_UP_COUNT = 0
        self.score = 0
        self.ggg = 10
        self.g = 0
        self.cross = Cross_hare()
        self.ducks = Duck()
        self.exit = 0
        self.i = 0
        self.x = 0
        self.kol = 2
        self.sum = 0
        self.y = 0
        self.rand = 0
        self.down = 0
        self.gameov = False
        self.set_mouse_visible(False)
        self.textureGrass = arcade.load_texture("img/grass.png")
        self.texturegun = arcade.load_texture("img/gun.png")
        self.texturegun2 = arcade.load_texture("img/gun2.png")
        self.score_texture = arcade.load_texture("img/Score2.png")
        self.duck_list = []
        self.duck_fall = []
        self.fail_list = []
        self.fon_list = []
        self.fails = 5

        self.nextlvl = arcade.load_texture("img/nextlvl2.jpg")

    def setup(self):
        # Настроить игру здесь
        self.duck = Duck()
        self.dog = Dog()
        #self.anim = Anime()
        self.cross_hare = Cross_hare()
        # 'run', 'game over', 'pause', 'next level'
        self.pause_time = 180
        self.state = 'start'

    def get_info(self):
        st = "Счет: {}\n".format(self.score)
        return st

    def on_draw(self):
        """ Отрендерить этот экран. """
        arcade.start_render()

        #if self.state == 'start':
           # while self.exit == 1:
        #   for i in range (100):
         #       self.start = arcade.load_texture("img/Welcome1.png")
          #      self.start.draw(0,0,800,600)
           #     time.sleep(1)
            #    self.start = arcade.load_texture("img/Welcome2.png")
             #   self.start.draw(0, 0, 800, 600)
              #  self.state = 'vibor'

            #    if keyboard.wait("enter") == True:
             #       self.exit = 1


        if self.state == 'start' :

            for fon in self.fon_list:
                fon.draw()


        if self.state == 'vibor':
            self.choose.draw(400, 300, 800, 600)

       # if self.statys == 1:
        #    self.backbround = arcade.load_texture("img/fons.png")
         #   self.backbround.draw(400, 300, 800, 600)


      #  if self.statys == 2:
       #     self.backbround = arcade.load_texture("img/fons2.jpg")
        #    self.backbround.draw(400, 300, 800, 600)





        if self.state in ['run']:

            self.backbround.draw(400, 300, 800, 600)


            for duck in self.duck_list:
                duck.draw()
                #self.x = duck.x
                #self.y = duck.y

            self.dog.draw()



            # arcade.draw_text(MAIN_STR, 300, 400, arcade.color.WHITE, 12, 500)
            # print(self.score)





            self.textureGrass.draw(400, 100, 900, 200)

            self.score_texture.draw(45, 352, 90, 45)

            arcade.draw_text("Жизней: " + str(int(self.fails)), 7, 345, arcade.color.WHITE, font_size=12)

            self.score_texture.draw(45, 452, 90, 45)

            #arcade.draw_text("X: " + str(int(self.x)), 7, 245, arcade.color.WHITE, font_size=22)

            arcade.draw_text("Уровень: " + str(int(self.lvl)), 7, 445, arcade.color.WHITE, font_size= 12)

            self.score_texture.draw(45, 522, 90, 45)

            arcade.draw_text(self.get_info(), 7, 500, arcade.color.WHITE, font_size= 12, font_name= 'Kenney Rocket')



            if self.cross_hare.get_degree() >= 90:
                self.texturegun.draw(400, -40, 500, 450, self.cross_hare.get_degree() + 232,)
            else:
                self.texturegun2.draw(400, -40, 500, 450, self.cross_hare.get_degree() - 45 )
            self.cross_hare.draw()



        elif self.state == 'game over':

            for fl in self.fail_list:
                fl.draw()
        elif self.state == 'next level':
            self.nextlvl.draw(400, 300, 800, 600)
            if self.statys == 0:
                self.choose.draw(400, 300, 800, 600)

            arcade.draw_text('Вы перешли на уровень ' + str(int(self.lvl))+' !', 220, 300, arcade.color.WHITE, 25)
            #self.textureGrass.draw(400, 100, 900, 200)




        # Здесь код рисунка

    def update(self, delta_time):
        """ Здесь вся игровая логика и логика перемещения."""
        self.ent = 0

        if self.state == 'start':
            for i in range(100):
                self.fon_list.append(Anime())


            if self.statys == 3:
                self.state = 'vibor'

        if self.state == 'vibor':
            if self.statys == 1:
                self.backbround = arcade.load_texture("img/fons.png")

                self.state = 'run'
            if self.statys == 2:
                self.backbround = arcade.load_texture("img/fons2.jpg")
               # self.backbround.draw(400, 300, 800, 600)
                self.state = 'run'


        self.step += 1



        if self.state == 'run':



            self.cross_hare.update()
            if (self.kol > self.sum):
                self.sum += 1
                if self.sum < 0:
                    self.sum = 1
                self.duck_list.append(Duck())
                #self.ent += 1

            self.dog.move()

            #if self.fails == 5:
             #   self.state = 'game over'

            for duck in self.duck_list:
                duck.move()
                if duck.check_strike(self.cross_hare):

                    self.duck_fall.append(Duck())
                    self.duck_list.remove(duck)
                    self.sum -= 1
                    
                    duck.move2()
                    self.score += 1



                    if (self.score >= self.ggg):


                        self.state = 'next level'
                        self.pause_time = 80

                        self.LVL_UP_COUNT += 10
                        self.lvl += 1
                        self.ggg = self.ggg + self.LVL_UP_COUNT
                        self.g = self.ggg
                        self.rand = random.randint (0,self.lvl+10)
                        self.fails += self.rand
                        self.kol += 1
                        self.sum = 0

                        for duck in self.duck_list:
                            self.duck_list.remove(duck)

                if duck.is_out():
                    self.duck_list.remove(duck)
                    self.score -= 1
                    self.ent += 1
                    self.fails -= 1
                    self.sum -= 1
                if self.fails < 0 and self.state != 'next level':
                    pass
                    self.state = 'game over'

        elif self.state == 'game over':
            for i in range(100):
                self.fail_list.append(End())
            if self.statys == 3:
                self.gameov = True
            if self.gameov:
                self.file.write(str(self.score) + "\n")
                self.score = 0

                self.setup()
                self.update(1)
                self.gameov = False
                self.choose = arcade.load_texture("img/choose1.png")
                self.backbround = arcade.load_texture("img/fons2.jpg")
                self.start1 = arcade.load_texture("img/Welcome1.png")
                self.start2 = arcade.load_texture("img/Welcome2.png")
                self.step = 0
                self.statys = 0
                self.lvl = 1
                self.LVL_UP_COUNT = 0
                self.score = 0
                self.ggg = 10
                self.g = 0
                self.cross = Cross_hare()
                self.ducks = Duck()
                self.exit = 0
                self.i = 0
                self.x = 0
                self.kol = 2
                self.sum = 0
                self.y = 0
                self.rand = 0
                self.down = 0
                self.gameov = False
                self.set_mouse_visible(False)
                self.textureGrass = arcade.load_texture("img/grass.png")
                self.texturegun = arcade.load_texture("img/gun.png")
                self.texturegun2 = arcade.load_texture("img/gun2.png")
                self.score_texture = arcade.load_texture("img/Score2.png")
                self.duck_list = []
                self.duck_fall = []
                self.fail_list = []
                self.fon_list = []
                self.fails = 5
                self.state = 'start'
        elif self.state == 'next level':
            self.pause_time -= 1
            if self.pause_time <= 0:
                self.state = 'run'



    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.cross_hare.move_to(x, y)


    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.cross_hare.shoot()

     #   if self.cross_hare.cool_down > 0:
    #        if get_distance(self, self.cross) > 30:
     #           self.fails += 1











    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()
        if symbol == arcade.key.KEY_1:
            self.statys = 1
        if symbol == arcade.key.KEY_2:
            self.statys = 2
        if symbol == arcade.key.ENTER:
            self.statys = 3




    #def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):

def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()