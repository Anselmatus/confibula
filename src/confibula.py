# -*- coding: utf-8 -*-


__author__="Antoine et Chou"

__date__ ="$23 nov. 2011 15:12:55$"


#breve import
import breve

#python imports
from math import sqrt, log10

#modules imports
from utils import config
from utils import logger

import environment
import frog
import male
import female
import movement


Environment = environment.Environment

class Confibula(breve.Control):
    def __init__(self):
        breve.Control.__init__(self)
        self.config = None
        self.movememt = None
        self.map = None
        self.environment = []
        self.frogs = []

        self.init()
	

    def init(self):
        print "Loading config from confibula.cfg"
        self.config = config.Config('confibula.cfg')
        self.config.load()
        print "Config loaded."
        print "Starting simulation."

        logger.init()
        logger.console = self.config.getValue("consoleOutput")
        logger.logFile = self.config.getValue("logfileOutput")
        if logger.logFile:
            self.scheduleRepeating('writeLogFile', 1)

        # /!\ ------------ RESERVED to Chou & Antoine ------------ /!\
        # Initialisation of the environment
        self.loadEnvironment()
	self.offsetCamera( breve.vector( 0, 0, 22) )
        # End of environment

        # Loading frogs
        self.loadFrogs()
	self.movement = breve.createInstances(breve.Movement, 1)
        self.setUpMenus()


    def iterate(self):
        print self.getSoundLevel( self.frogs[3].getLocation() )
        breve.Control.iterate(self)
    
    def setUpMenus(self):
        self.addMenu('''Redistribuer les grenouilles''', 'loadFrogs') # not working
        self.addMenu('''Afficher les environements''', 'printEnvironments') # debug purpose
        self.addMenu('''Afficher le niveau sonore''', 'printSoundLevel') # debug purpose
        self.addMenu('''Afficher les grenouilles''', 'printFrogs') # debug purpose
        self.addMenu('''Afficher barycentre du son''', 'printSoundSource') # debug purpose
        self.addMenu('''Afficher les proies''', 'printEncounteredPreys') # debug purpose

    def loadEnvironment(self):
        self.loadMap()
        
        myEnv = None
        envNames = self.config.getValue("envNames")
        envColors = self.config.getValue("envColors")
        envEase = self.config.getValue("envEase")
        preyProbability = self.config.getValue("preyEncounterProbability")
        preyEnergyBoost = self.config.getValue("preyEnergyBoost")
        predatorProbability = self.config.getValue("predatorEncounterProbability")
        logger.title("Loading %d environments." % len(envNames))
        for i in range(0, len(envNames)):
            myEnv = Environment(envNames[i], envColors[i])
            myEnv.ease = envEase[i]
            myEnv.preyProbability = preyProbability[i]
            myEnv.preyEnergyBoost = preyEnergyBoost[i]
            myEnv.predatorProbability = predatorProbability[i]
            self.environment.append(myEnv)
            logger.log(myEnv)
        logger.title("Environment loading complete.")

    def loadMap(self):
        imageFile = self.config.getValue("mapFile")
        self.image = breve.createInstances(breve.Image,1).load(imageFile)
        self.image.width = self.image.getWidth()
        self.image.height = self.image.getHeight()
	self.map = Map(self.image)

    def loadFrogs(self):
        frogsNumber = self.config.getValue("frogsNumber")
        del(self.frogs[:])
        self.frogs = breve.createInstances(breve.Male, frogsNumber)

    def selectMovement(self, id):
        return self.movement.selectMovement(id)      

    def getEnvironment(self, location):
        pixelColor = self.image.getRgbPixel(location.x, location.y)
        for env in self.environment:
            if (env.getColor() == pixelColor):
                return env

    def getSoundLevel(self, location):
        '''
        location : position in he simulation (location.x & location.y)   
        '''
        SPL = 0
        for frog in self.frogs:
            if isinstance(frog , breve.Male) and frog.state == 'singing' :
                #pos = self.worldToImage(frog.getLocation())
                pos = frog.getLocation()
                dist = (location.x - pos.x)**2 + (location.y - pos.y)**2
                if (dist != 0) :
                    sndLvl = frog.voicePower - 10*log10(dist)
                else :
                    sndLvl = frog.voicePower
                SPL += 10**(sndLvl/10) # SPL = 10 * log( 10^(SPL1/10) + 10^(SPL2/10) + ...)
        if SPL != 0 :
            level = 10 * log10(SPL)  # I = 10 * log( SPL) dB
        else :
            level = 0
        return level

    def getSoundSource(self):
        '''
        A, B, C trois points du systeme pondéré { (A,a), (B,b), (C,c) }.
        Pour tout point M du plan défini par A, B, C : aMA + bMB + cMC = (a+b+c)MG
        Avec G le barycentre des points A, B, C.

        On obtient ses coordonnées :

             axA + bxB + cxC
        xG = ---------------
              a  +  b  +  c

             ayA + byB + cyC
        yG = ---------------
              a  +  b  +  c

             azA + bzB + czC
        zG = ---------------
              a  +  b  +  c

        Bon, ici la coordonnée en z ne nous sert pas puisqu'on travaille dans le plan.

        On peut généraliser ce calcul pour n points.
        '''
        xG, yG, weightSum = 0.0, 0.0, 0.0 # weightSum = a+b+c = sum of the weight of each point
        for frog in self.frogs:
            if isinstance(frog , breve.Male) and frog.state == 'singing' :
                pos = frog.getLocation()
                weight = frog.voicePower
                xG += weight*pos.x # calculating the numerators, for the x coordinate
                yG += weight*pos.y # for the y one
                weightSum += weight # denominator (same for every coord)
        xG /= weightSum
        yG /= weightSum
        return breve.vector(xG, yG, 0) # simulation coordinates

    def worldToImage(self, location):
        '''
        Changes the coordinates of a breve.vector from simulation's world to image coordinates.
        '''
        location.x = int((location.x + 8) * (self.image.width/16))
        location.y = int((location.y + 8) * (self.image.height/16))
        return location

    def writeLogFile(self):
        logger.write()


    def printEnvironments(self):
        logger.title('Listing all frogs\' environments')
        for frog in self.frogs:
            logger.log(frog.getEnvironment())

    def printSoundLevel(self):
        logger.title('Sound level from following coordinates :')
        x, y = int(raw_input('x : ')), int(raw_input('y : '))
        logger.log('x=%d, y=%d' % (x, y))
        lvl = self.getSoundLevel(breve.vector(x, y, 0))
        logger.log('Sound intensity level : %dB' % lvl)

    def printSoundSource(self):
        logger.title('Printing sound source\'s position')
        location = self.getSoundSource()
        logger.log('x = %f' % location.x)
        logger.log('y = %f' % location.y)

    def printFrogs(self):
        logger.title('Listing all frogs :')
        for frog in self.frogs:
            logger.log(frog)

    def printEncounteredPreys(self):
        logger.title('Encountered preys :')
        for frog in self.frogs:
            logger.log('Frog #%d, preys : %d, energy : %d, predators : %d' % (frog.id, frog.encounteredPreys, frog.totalEnergyBoost, frog.encounteredPredators))

breve.Confibula = Confibula


class Map(breve.Stationary):
    def __init__(self, image):
	breve.Stationary.__init__( self )
	self.setTextureImage(image)
	mapShape = breve.createInstances( breve.Cube, 1 ).initWith( breve.vector( 16, 16, 0.0001 )) # constante magique
	self.setShape( mapShape )
	self.setTextureImage(image)
	self.move( breve.vector( 0, 0, 0 ) )
        self.setRotation( breve.vector(0,0,1),1.5708)



breve.Map = Map


Confibula()



