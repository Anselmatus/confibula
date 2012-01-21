# -*- coding: utf-8 -*-

import breve
from utils import logger
from random import uniform, randint

class Male(breve.Frog):


    def __init__(self):
        breve.Frog.__init__(self)
        self.voicePower = randint(50,100)
        self.voiceQuality = randint(1,10)
        self.throatColor = randint(30,50)
        self.encounteredPreys, self.encounteredPredators, self.totalEnergyBoost = 0, 0, 0
        self.init()

    def init(self):
        self.move( breve.vector(uniform(-8, 8), uniform(-8, 8), 0.01) )
        self.setShape( breve.createInstances(breve.Cube, 1).initWith( breve.vector(0.1, 0.1, 0.1)))
        self.setColor( breve.vector( 0, 0, 0.4 ) )
        self.state = "moveToSing"
		
    def iterate(self):
        self.setVelocity( self.controller.selectMovement(self.getId()) )

    
    def __str__(self):
        pos = self.controller.worldToImage(self.getLocation())
        env = self.getEnvironment().getName()
        return 'Frog #%d  energy:%d  voicePower:%d  location:%d,%d  env:%s' % (self.id, self.energy, self.voicePower, pos.x, pos.y, env)

breve.Male = Male
 
