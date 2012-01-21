 
# -*- coding: utf-8 -*-

import breve
from random import uniform, randint

class Female(breve.Mobile):
    numFrog = 0
	
    def __init__(self):
        breve.Female.__init__(self)
        self.encounteredPreys, self.encounteredPredators, self.totalEnergyBoost = 0, 0, 0
        self.init()

    def init(self):
        self.move( breve.vector(uniform(-8, 8), uniform(-8, 8), 0.01) )
        self.setShape( breve.createInstances(breve.Cube, 1).initWith( breve.vector(0.1, 0.1, 0.1)))
        self.setColor( breve.vector( 1, 0, 0 ) )
		
    def iterate(self):
        self.setVelocity( self.controller.selectMovement(self.getId()) ) 

    def __str__(self):
        pos = self.controller.worldToImage(self.getLocation())
        env = self.getEnvironment().getName()
        return 'Frog #%d  energy:%d location:%d,%d  env:%s' % (self.id, self.energy, pos.x, pos.y, env)

breve.Female = Female
