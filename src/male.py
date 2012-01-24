# -*- coding: utf-8 -*-

import breve
from utils import logger
from utils import config
from random import uniform, randint

class Male(breve.Frog):

    def __init__(self):
        breve.Frog.__init__(self)
        self.voicePower = randint(50, 100)
        self.voiceQuality = randint(1, 10)
        self.throatColor = randint(30, 50)
        self.encounteredPreys, self.encounteredPredators, self.totalEnergyBoost = 0, 0, 0
        self.state = 'moveToSing'
        self.isCheater = False
        self.init()
        self.turnCheater()

    def init(self):
        self.move(breve.vector(uniform(-8, 8), uniform(-8, 8), 0.01))
        self.setShape(breve.createInstances(breve.Cube, 1).initWith(breve.vector(0.1, 0.1, 0.1)))
        self.setColor(breve.vector(1, 1, 1))
		
    def iterate(self):
        self.setVelocity(self.controller.selectMovement(self.id))

    def turnCheater(self):
        if (self.voicePower < 75 or self.voiceQuality < 5 or self.throatColor < 40) :
            becomeCheaterProbability = self.controller.config.getValue("becomeCheaterProbability")
            addProbability = becomeCheaterProbability*35/100
            if self.voicePower < 60:
                becomeCheaterProbability += addProbability

            if self.voiceQuality < 3:
                becomeCheaterProbability += addProbability

            if self.throatColor < 36:
                becomeCheaterProbability += addProbability

            if uniform(0, 1) < becomeCheaterProbability:
                self.isCheater
    
    def __str__(self):
        pos = self.controller.worldToImage(self.getLocation())
        env = self.getEnvironment().getName()
        return 'Frog #%d  energy:%d location:%d,%d  env:%s  state:%s' % (self.id, self.energy, pos.x, pos.y, env, self.state)

breve.Male = Male
