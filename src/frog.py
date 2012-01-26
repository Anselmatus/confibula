# -*- coding: utf-8 -*-

import breve
from random import randint
from random import uniform

class Frog(breve.Mobile):
    numFrog = 0
	
    def __init__(self):
        breve.Mobile.__init__(self)
        Frog.numFrog += 1 
	self.id = Frog.numFrog
        self.energy = self.controller.config.getValue('energy')
        self.minEnergy = randint(5, 20)
        self.maxEnergy = randint(80, 95)
        self.state = None
        self.encounteredPreys, self.encounteredPredators, self.totalEnergyBoost = 0, 0, 0
        self.sleepTime = 0
        self.init()

    def init(self):
        width = self.controller.config.getValue("mapWidth")/2
        height = self.controller.config.getValue("mapHeight")/2
        self.move(breve.vector(uniform(-width, width), uniform(-height, height), 0.01))
        self.setShape(breve.createInstances(breve.Cube, 1).initWith(breve.vector(0.1, 0.1, 0.1)))
        self.setColor(breve.vector(1, 1, 1))
		
    def iterate(self):
        move = self.controller.selectMovement(self.id)
        #exemple utilisation methode onBorder()
        speed = float(self.energy) / 1000
        onBorder = self.onBorder()
        borderRight = self.controller.config.getValue("mapWidth")/2
        borderTop = self.controller.config.getValue("mapHeight")/2
        if onBorder[0]:
            self.move(breve.vector(borderRight, self.getLocation().y, 0.01))
        if onBorder[1]:
            self.move(breve.vector(-borderRight, self.getLocation().y, 0.01))
        if onBorder[2]:
            self.move(breve.vector(self.getLocation().x, -borderTop, 0.01))
        if onBorder[3]:
            self.move(breve.vector(self.getLocation().x, borderTop, 0.01))
        # fin exemple
        if (onBorder[0]==False and onBorder[1]==False and onBorder[2]==False and onBorder[3]==False):
            self.setVelocity(move)



        
    def getId(self):
        return self.id

    def getEnvironment(self):
        return self.controller.getEnvironment(self.controller.worldToImage(self.getLocation()))

    def onBorder(self):
        location = self.getLocation();
        return self.controller.onBorder(location)

    def getEnergy(self):
        return self.energy

    def getSoundLevel(self):
        return self.controller.getSoundLevel(self.controller.worldToImage(self.getLocation()))
    
    def getBestMale(self, listMale=[]):
        if len(listMale) == 0:
            listMale = self.viewMale()
        malePower = listMale[0].voicePower + listMale[0].voiceQuality + listMale[0].throatColor
	maleChoice = listMale[0]

	for male in listMale[1:]:
            if malePower > (male.voicePower + male.voiceQuality + male.throatColor):
                malePower = male.voicePower + male.voiceQuality + male.throatColor
                maleChoice = male
        return maleChoice
    
    def viewMale(self):
	visionDistance = self.controller.config.getValue("visionDistance")
	viewMale = []
	#parcour la liste des males présent et les met dans un tableau pour recencer les male "vu" par la femelle
	for male in self.controller.frogsMale:
            if self.getDistance(male) < visionDistance and male.state == 'singing':
                viewMale.append(male)
	#si il y a des males "vu"
	if len(viewMale) != 0:
            return viewMale
	else:
            return 0;

    def viewFemale(self):
	visionDistance = self.controller.config.getValue("visionDistanceMale")
	viewFemale = []
	#parcour la liste des males présent et les met dans un tableau pour recencer les male "vu" par la femelle
	for female in self.controller.frogsFemale:
            if self.getDistance(female) < visionDistance:
                viewFemale.append(female)
	#si il y a des males "vu"
	if len(viewFemale) != 0:
            return viewFemale
	else:
            return 0;

    def getBestFemale(self, listFemale=[]):
        if len(listFemale) == 0:
            listFemale = self.viewFemale()
	femaleChoice = listFemale[0]
        femaleId = listFemale[0].getId()
	for female in listFemale[1:]:
		if femaleId > female.getId() and (female.state == 'hunting' or female.state == 'findPartener'):
			femaleId = female.getId()
			femaleChoice = female
        return femaleChoice

    def __str__(self):
        pos = self.controller.worldToImage(self.getLocation())
        env = self.getEnvironment().getName()
        return 'Frog #%d  energy:%d location:%d,%d  env:%s  state:%s' % (self.id, self.energy, pos.x, pos.y, env, self.state)

breve.Frog = Frog
