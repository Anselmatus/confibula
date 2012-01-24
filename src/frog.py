# -*- coding: utf-8 -*-

from random import randint
from random import uniform

import breve

class Frog(breve.Mobile):
    numFrog = 0
	
    def __init__(self):
        breve.Mobile.__init__(self)
        Frog.numFrog += 1 
	self.id = Frog.numFrog
        self.energy = 1000
        self.minEnergy = randint(5, 20)
        self.state = None
        self.encounteredPreys, self.encounteredPredators, self.totalEnergyBoost = 0, 0, 0
        self.init()

    def init(self):
        self.move(breve.vector(uniform(-8, 8), uniform(-8, 8), 0.01))
        self.setShape(breve.createInstances(breve.Cube, 1).initWith(breve.vector(0.1, 0.1, 0.1)))
        self.setColor(breve.vector(1, 1, 1))
		
    def iterate(self):
        move = self.controller.selectMovement(self.id)
        location = self.getLocation();
        if (location.x >= 8):
            move.x = 0
        elif location.x <= -8:
            move.x = 0

        if (location.y >= 8):
            move.y = 0
        elif location.y <= -8:
            move.y = 0
        self.setVelocity(move)
        
    def getId(self):
        return self.id

    def getEnvironment(self):
        return self.controller.getEnvironment(self.controller.worldToImage(self.getLocation()))

    def getSoundLevel(self):
        return self.controller.getSoundLevel(self.controller.worldToImage(self.getLocation()))
	
    def __str__(self):
        pos = self.controller.worldToImage(self.getLocation())
        env = self.getEnvironment().getName()
        return 'Frog #%d  energy:%d location:%d,%d  env:%s  state:%s' % (self.id, self.energy, pos.x, pos.y, env, self.state)

breve.Frog = Frog
