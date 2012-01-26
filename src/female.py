 
# -*- coding: utf-8 -*-

from random import randint
from random import uniform

import breve
import frog

class Female(breve.Frog):
	
    def __init__(self):
        breve.Frog.__init__(self)
        self.encounteredPreys, self.encounteredPredators, self.totalEnergyBoost = 0, 0, 0
        self.state = 'findPartener'
        self.init()

    def init(self):
        self.move(breve.vector(uniform(-8, 8), uniform(-8, 8), 0.01))
        self.setShape(breve.createInstances(breve.Cube, 1).initWith(breve.vector(0.1, 0.1, 0.1)))
        self.setColor(breve.vector(1, 0, 0))

    def iterate(self):
        breve.Frog.iterate(self)
        if self.state == 'coupling' :
            self.setShape(breve.createInstances(breve.Cube, 1).initWith(breve.vector(0.15, 0.15, 0.15)))
            self.setColor(breve.vector(0, 1, 1))
        else :
            self.setShape(breve.createInstances(breve.Cube, 1).initWith(breve.vector(0.1, 0.1, 0.1)))
            self.setColor(breve.vector(1, 0, 0))

    def __str__(self):
        pos = self.controller.worldToImage(self.getLocation())
        env = self.getEnvironment().getName()
        return 'Frog #%d  energy:%d location:%d,%d  env:%s  state:%s' % (self.id, self.energy, pos.x, pos.y, env, self.state)

    

breve.Female = Female
