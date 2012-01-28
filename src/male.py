# -*- coding: utf-8 -*-

import breve
from utils import logger
from utils import config
from random import uniform, randint

class Male(breve.Frog):

    def __init__(self):
        breve.Frog.__init__(self)
        self.voicePower = randint(40, 60)
        self.voiceQuality = randint(1, 10)
        self.throatColor = randint(30, 50)
        self.encounteredPreys, self.encounteredPredators, self.totalEnergyBoost = 0, 0, 0
        self.state = 'moveToSing'
        self.isCheater = False
        self.init()
        self.turnCheater()

    def init(self):
        width = self.controller.config.getValue("mapWidth")/2
        height = self.controller.config.getValue("mapHeight")/2
        self.move(breve.vector(uniform(-width, width), uniform(-height, height), 0.01))
        self.setShape(breve.createInstances(breve.Cube, 1).initWith(breve.vector(0.1, 0.1, 0.1)))
        self.setColor(breve.vector(1, 1, 1))

    def iterate(self):
        breve.Frog.iterate(self)
        
        if self.state == 'singing':
            self.setShape(breve.createInstances(breve.Cube, 1).initWith(breve.vector(0.15, 0.15, 0.15)))
        elif self.state == 'hunting':
            self.setShape(breve.createInstances(breve.Cube, 1).initWith(breve.vector(0.1, 0.1, 0.1)))
            self.setColor(breve.vector(1, 1, 0))
        elif self.state == 'coupling' :
            self.setShape(breve.createInstances(breve.Cube, 1).initWith(breve.vector(0.15, 0.15, 0.15)))
            self.setColor(breve.vector(1, 0, 1))
        else :
            self.setShape(breve.createInstances(breve.Cube, 1).initWith(breve.vector(0.1, 0.1, 0.1)))
            self.setColor(breve.vector(1, 1, 1))
        if self.isCheater:
            self.setColor(breve.vector(0, 0, 0))


    def turnCheater(self):
        power = self.getPower()
        if (power < 85) :
            becomeCheaterProbability = self.controller.config.getValue("becomeCheaterProbability")
            addProbability = becomeCheaterProbability*35/100
            if self.voicePower < 45:
                becomeCheaterProbability += addProbability

            if self.voiceQuality < 3:
                becomeCheaterProbability += addProbability

            if self.throatColor < 36:
                becomeCheaterProbability += addProbability

            if uniform(0, 1) < becomeCheaterProbability:
                self.isCheater = True
                self.setColor(breve.vector(0, 0, 0))

    def getPower(self):
        return self.voicePower + self.voiceQuality + self.throatColor
    
    def __str__(self):
        pos = self.controller.worldToImage(self.getLocation())
        env = self.getEnvironment().getName()
        return 'Frog #%d  energy:%d location:%d,%d  env:%s  state:%s' % (self.id, self.energy, pos.x, pos.y, env, self.state)

breve.Male = Male
