import pygame as pg
import sys
import os
from random import *

CAPTION = "Minesweeper"
SCREEN_SIZE = (500, 500)

_image_library = {}


def main():
    pg.init()
    pg.display.set_caption(CAPTION)
    screen = pg.display.set_mode(SCREEN_SIZE)
    board = Board()
    pg.display.update()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()

                for i in range(10):
                    for button in board.buttons[i]:
                        if button.button.collidepoint(mouse_pos):
                            button.clicked = True
                            imagePath = str(button.val) + ".png"
                            image = get_image(imagePath)
                            image.convert()
                            screen.blit(image, (button.position.x,button.position.y))
                            pg.display.update()
                            break

    pg.quit()
    sys.exit


def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image is None:
        simplePath = path.replace('/', os.sep).replace('\\', os.sep)
        image = pg.image.load(simplePath)
        _image_library[path] = image
    return image


class Board(object):
    w = 10
    mines = 25
    buttons = []

    def __init__(self):
        self.screen = pg.display.get_surface()
        self.createButtons()
        self.placeMines()
        self.placeNumbers()
        self.draw()

    def placeMines(self):
        """
            place random mines inside the matrix
        """
        count = 0
        while count < self.mines:
            x = randint(0, 9)
            y = randint(0, 9)

            if self.buttons[x][y].val == -1:
                self.buttons[x][y].val = 100
                count += 1

    def placeNumbers(self):
        """
        scan through matrix, count how many mines are near the space, if none, leave as -1, otherwise as the count
        """
        for i in range(self.w):
            for j in range(self.w):
                count = 0
                if self.buttons[i][j].val != 100:
                    if i - 1 >= 0 and self.buttons[i - 1][j].val == 100:
                        count += 1
                    if j - 1 >= 0 and self.buttons[i][j - 1].val == 100:
                        count += 1
                    if i + 1 <= 9 and self.buttons[i + 1][j].val == 100:
                        count += 1
                    if j + 1 <= 9 and self.buttons[i][j + 1].val == 100:
                        count += 1
                    if i - 1 >= 0 and j - 1 >= 0 and self.buttons[i - 1][j - 1].val == 100:
                        count += 1
                    if i - 1 >= 0 and j + 1 <= 9 and self.buttons[i - 1][j + 1].val == 100:
                        count += 1
                    if i + 1 <= 9 and j - 1 >= 0 and self.buttons[i + 1][j - 1].val == 100:
                        count += 1
                    if i + 1 <= 9 and j + 1 <= 9 and self.buttons[i + 1][j + 1].val == 100:
                        count += 1

                if count > 0:
                    self.buttons[i][j].val = count

    def createButtons(self):
        x, y = 1,1
        for i in range(self.w):
            y = 1
            pos = Position(x,y)
            self.buttons.append([])
            for j in range(self.w):
                button = SquareButton(pos, -1)
                self.buttons[i].append(button)
                pg.draw.rect(self.screen,[255,255,255], button.button)
                y += 50
                pos = Position(x,y)
                print(pos.x,pos.y)
            x += 50

    def draw(self):
        for i in range(self.w):
            for j in range(self.w):
                imagepath = str(self.buttons[i][j].val) + '.png'
               # print(imagepath)
                image = get_image(imagepath)
                imagerect = image.get_rect()
              #  print(imagerect)
                imagerect.x = self.buttons[i][j].position.x
                imagerect.y = self.buttons[i][j].position.y
              #  print(imagerect)
                #self.screen.blit(image
                pg.display.update()



class SquareButton(object):
    BUTTON_SIZE = 48

    def __init__(self, pos, value):
        self._val = value
        self._clicked = False
        self._position = pos
        self.button = pg.Rect(self.position.x, self.position.y, self.BUTTON_SIZE, self.BUTTON_SIZE)

    @property
    def clicked(self):
        return self._clicked

    @clicked.setter
    def clicked(self, value):
        self._clicked = value

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, value):
        self._val = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self,pos):
        self._position = pos


class Position(object):

    def __init__(self, newX, newY):
        self._x = newX
        self._y = newY

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self,val):
        self._x = val

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self,val):
        self._y = val




main()
