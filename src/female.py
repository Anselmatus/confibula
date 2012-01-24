 
# -*- coding: utf-8 -*-

from random import randint
from random import uniform

import breve
import frog

class Female(breve.Frog):
	
    def __init__(self):
        breve.Frog.__init__(self)
        self.encounteredPreys, self.encounteredPredators, self.totalEnergyBoost = 0, 0, 0
        self.state = self.selectState()
        self.init()

    def init(self):
        self.move(breve.vector(uniform(-8, 8), uniform(-8, 8), 0.01))
        self.setShape(breve.createInstances(breve.Cube, 1).initWith(breve.vector(0.1, 0.1, 0.1)))
        self.setColor(breve.vector(1, 0, 0))
		
    def iterate(self):
        self.state = self.selectState()
        self.setVelocity(self.controller.selectMovement(self.id))

    def __str__(self):
        pos = self.controller.worldToImage(self.getLocation())
        env = self.getEnvironment().getName()
        return 'Frog #%d  energy:%d location:%d,%d  env:%s  state:%s' % (self.id, self.energy, pos.x, pos.y, env, self.state)

    def viewMale(self):
	visionDistance = self.controller.config.getValue("visionDistance")
	viewMale = []
	#parcour la liste des males présent et les met dans un tableau pour recencer les male "vu" par la femelle
	for male in self.controller.frogsMale:
            if self.getDistance(male) < visionDistance:
                viewMale.append(male)
	#si il y a des males "vu"
	if len(viewMale) != 0:
            return viewMale
	else:
            return 0;

breve.Female = Female
