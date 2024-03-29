# -*- coding: utf-8 -*-

from random import randint
from random import uniform

import breve
import frog

class Female(breve.Frog):
	
    def __init__(self):
        breve.Frog.__init__(self)
        self.encounteredPreys, self.encounteredPredators, self.totalEnergyBoost = 0, 0, 0
        self.state = self.controller.config.getValue('standartFemaleState')
        self.seuil = 1.
        self.init()

    def init(self):
        width = self.controller.config.getValue("mapWidth")/2
        height = self.controller.config.getValue("mapHeight")/2
        self.move(breve.vector(uniform(-width, width), uniform(-height, height), 0.01))
        self.setShape(breve.createInstances(breve.Cube, 1).initWith(breve.vector(0.1, 0.1, 0.1)))
        self.setColor(breve.vector(1, 0, 0))

    def iterate(self):
        breve.Frog.iterate(self)
        if self.state == 'coupling' :
            self.setShape(breve.createInstances(breve.Cube, 1).initWith(breve.vector(0.15, 0.15, 0.15)))
            self.setColor(breve.vector(0, 1, 1))
        elif self.state == 'hunting':
            self.setShape(breve.createInstances(breve.Cube, 1).initWith(breve.vector(0.1, 0.1, 0.1)))
            self.setColor(breve.vector(1, 1, 0))
        else :
            self.setShape(breve.createInstances(breve.Cube, 1).initWith(breve.vector(0.1, 0.1, 0.1)))
            self.setColor(breve.vector(1, 0, 0))
        self.logIt()

    def __str__(self):
        pos = self.controller.worldToImage(self.getLocation())
        env = self.getEnvironment().getName()
        return 'Frog #%d  energy:%d location:%d,%d  env:%s  state:%s' % (self.id, self.energy, pos.x, pos.y, env, self.state)
    def logIt(self):
        breve.Frog.logIt(self)
        self.controller.log['frogs']['females']['female:'+ str(self.id)] = self.log
    

breve.Female = Female
