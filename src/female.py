 
# -*- coding: utf-8 -*-

import breve
import frog
from random import uniform, randint

class Female(breve.Frog):
	
    def __init__(self):
        breve.Frog.__init__(self)
        self.encounteredPreys, self.encounteredPredators, self.totalEnergyBoost = 0, 0, 0
        self.state = 'nimp'
	self.init()

    def init(self):
        self.move( breve.vector(uniform(-8, 8), uniform(-8, 8), 0.01) )
        self.setShape( breve.createInstances(breve.Cube, 1).initWith( breve.vector(0.1, 0.1, 0.1)))
        self.setColor( breve.vector( 1, 0, 0 ) )
		
    def iterate(self):
	self.state = self.selectState()
        self.setVelocity( self.controller.selectMovement(self.id) )

    def __str__(self):
        pos = self.controller.worldToImage(self.getLocation())
        env = self.getEnvironment().getName()
        return 'Frog #%d  energy:%d location:%d,%d  env:%s' % (self.id, self.energy, pos.x, pos.y, env)

	def selectState(self):
		#selectioné le choix de stratégie de la femelle
		# si elle est loin des males elle ce dirige vers le chorus et la fonction retourne 'moveToChorus'
		# si elle "voit" au moins un male elle retourne 'findPartner'
		return 'nimp'

breve.Female = Female
