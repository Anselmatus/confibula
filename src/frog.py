# -*- coding: utf-8 -*-

import breve
from random import uniform, randint

class Frog(breve.Mobile):
    numFrog = 0
    sexType = ('Female','Male') 
	
    def __init__(self):
        breve.Mobile.__init__(self)
        Frog.numFrog += 1 
	self.id = Frog.numFrog
        self.energy = 1000
        self.voicePower = randint(86,89)
	self.sex = Frog.sexType[randint(0,1)]
        self.encounteredPreys, self.encounteredPredators, self.totalEnergyBoost = 0, 0, 0
        self.init()

    def init(self):
        self.move( breve.vector(uniform(-8, 8), uniform(-8, 8), 0.01) )
        self.setShape( breve.createInstances(breve.Cube, 1).initWith( breve.vector(0.1, 0.1, 0.1)))
        self.setColor( breve.randomExpression( breve.vector( 1, 1, 1 ) ) )
		
    def iterate(self):
        self.setVelocity( self.controller.selectMovement(self.getId()) ) 

    def getId(self):
        return self.id

    def getEnvironment(self):
        return self.controller.getEnvironment(self.controller.worldToImage(self.getLocation()))

    def getSoundLevel(self):
        return self.controller.getSoundLevel(self.controller.worldToImage(self.getLocation()))

    def __str__(self):
        pos = self.controller.worldToImage(self.getLocation())
        env = self.getEnvironment().getName()
        return 'Frog #%d  energy:%d  voicePower:%d  location:%d,%d  env:%s' % (self.id, self.energy, self.voicePower, pos.x, pos.y, env)

breve.Frog = Frog
