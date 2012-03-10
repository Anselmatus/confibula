# -*- coding: utf-8 -*-

import breve
from utils import logger
from utils import config
from random import uniform, randint

class Male(breve.Frog):

    def __init__(self):
        breve.Frog.__init__(self)
        self.voicePower = randint(self.controller.config.getValue('lowVoicePower'), self.controller.config.getValue('highVoicePower'))
        self.voiceQuality = randint(self.controller.config.getValue('lowVoiceQuality'), self.controller.config.getValue('highVoiceQuality'))
        self.throatColor = randint(self.controller.config.getValue('lowThroatColor'), self.controller.config.getValue('highThroatColor'))
        self.patience = randint(80, 100)
        timeFemaleLoad = self.controller.config.getValue("femaleLoadTimeDefault")*3
        patienceTimeToCoupling = int(self.controller.config.getValue("patienceTimeToCoupling"))
        self.patienceTimeMax = randint(int(timeFemaleLoad), patienceTimeToCoupling)
        self.encounteredPreys, self.encounteredPredators, self.totalEnergyBoost = 0, 0, 0
        self.state = self.controller.config.getValue('standartMaleState')
        self.isCheater = False
        self.init()

    def init(self):
        width = self.controller.config.getValue("mapWidth")/2
        height = self.controller.config.getValue("mapHeight")/2
        self.move(breve.vector(uniform(-width, width), uniform(-height, height), 0.01))
        self.setShape(breve.createInstances(breve.Cube, 1).initWith(breve.vector(0.1, 0.1, 0.1)))
        self.setColor(breve.vector(1, 1, 1))

    def iterate(self):
        breve.Frog.iterate(self)
        self.losePatience()
        if self.isCheater == True:
                self.setShape(breve.createInstances(breve.Cube, 1).initWith(breve.vector(0.1, 0.1, 0.1)))
                self.setColor(breve.vector(0, 0, 0))
        elif self.state == 'singing':
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

    def turnCheater(self, power=0):
        if power == 0:
            power = self.getPower()
        if (power < self.powerAverage()) :
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
                return True
        return False


    def losePatience(self):
        timeNoCoupling = int(self.controller.getTime() - self.timeLastCoupling)
        timeNoCouplingPercent = int(timeNoCoupling*100/self.patienceTimeMax)
        if timeNoCouplingPercent > self.patience and self.isCheater == False:
            power = self.getPower()*(100-timeNoCouplingPercent)/100
            if self.turnCheater(power) == True:
                self.state = "moveToSing"

    def getPower(self):
        return self.voicePower + self.voiceQuality + self.throatColor
    def powerAverage(self):
        listMale = self.viewMale()
        average = 0;
        i = 0;
        if listMale == 0:
            return 0
        for male in listMale[1:]:
            i=i+1
            average = male.getPower()
        if i==0:
            return 0
        average = average/i
        return average

    def __str__(self):
        pos = self.controller.worldToImage(self.getLocation())
        env = self.getEnvironment().getName()
        return 'Frog #%d  energy:%d location:%d,%d  env:%s  state:%s' % (self.id, self.energy, pos.x, pos.y, env, self.state)

breve.Male = Male
