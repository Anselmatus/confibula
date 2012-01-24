# -*- coding: utf-8 -*-

__author__= "antoine"

from utils import color

class Environment:
    def __init__(self, name, c):
        self.name = name
        self.color = color.getRgbColor(c)
        self.ease = 0

    def __str__(self):
        return "Env %s, color %s, ease %s" % (self.name, self.color, self.ease)

    def setName(self, name):
        self.name = name

    def setColor(self, c):
        self.color = color.getRgbColor(c)

    def getName(self):
        return self.name

    def getColor(self):
        return self.color

if __name__ == "__main__":
    e = Environment('Eau', 'blue')
    print e.getName()
    print e.getColor()
