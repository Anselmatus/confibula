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
        self.minEnergy = randint(self.controller.config.getValue('lowLimitMinEnergy'), self.controller.config.getValue('highLimitMinEnergy'))
        self.maxEnergy = randint(self.controller.config.getValue('lowLimitMaxEnergy'), self.controller.config.getValue('lowLimitMaxEnergy'))
        self.energy = self.controller.config.getValue('energy')*self.maxEnergy/100
        self.state = None # initialization
        self.encounteredPreys, self.encounteredPredators, self.totalEnergyBoost = 0, 0, 0
        self.sleepTime = 0
        self.timeLastCoupling = 0
        self.speedMax = randint(800, 1300);
        self.init()

    def init(self):
        width = self.controller.config.getValue("mapWidth")/2
        height = self.controller.config.getValue("mapHeight")/2
        self.move(breve.vector(uniform(-width, width), uniform(-height, height), 0.01))
        self.setShape(breve.createInstances(breve.Cube, 1).initWith(breve.vector(0.1, 0.1, 0.1)))
        self.setColor(breve.vector(1, 1, 1))
		
    def iterate(self):
        move = self.controller.selectMovement(self.id)
        onBorder = self.onBorder()
        self.move(onBorder)
        if(move != breve.vector(0,0,0)) :
            self.setVelocity(breve.vector(uniform(move.x-0.5,move.x+0.5), uniform(move.y-0.5,move.y+0.5), 0))
        else :
            self.setVelocity(move)

    def getId(self):
        return self.id

    def getEnvironment(self):
        print self.controller.worldToImage(self.getLocation())
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
        malePower = listMale[0].getPower()
	maleChoice = listMale[0]

	for male in listMale[1:]:
            if malePower > male.getPower():
                malePower = male.getPower()
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
            if self.getDistance(female) < visionDistance and (female.state == 'hunting' or female.state == 'findPartener'):
                viewFemale.append(female)
	#si il y a des males "vu"
	if len(viewFemale) != 0:
            return viewFemale
	else:
            return 0;
    def speed(self):
        return float(self.energy) / self.speedMax

    def getBestFemale(self, listFemale=[]):
        if len(listFemale) == 0:
            listFemale = self.viewFemale()
	femaleChoice = listFemale[0]
        femaleId = listFemale[0].getId()
	for female in listFemale[1:]:
		if femaleId > female.getId():
			femaleId = female.getId()
			femaleChoice = female
        return femaleChoice

    def __str__(self):
        pos = self.controller.worldToImage(self.getLocation())
        env = self.getEnvironment().getName()
        return 'Frog #%d  energy:%d location:%d,%d  env:%s  state:%s' % (self.id, self.energy, pos.x, pos.y, env, self.state)

breve.Frog = Frog
