# -*- coding: utf-8 -*-


__author__="Confibula team"

__date__ ="$23 nov. 2011 15:12:55$"


#breve import
import breve

#python imports
from math import sqrt, log10

#modules imports
from tokenize import tabsize
from utils import config
from utils import logger
from utils import color

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
        self.frogsMale = []
	self.frogsFemale = []
        self.frogs = []
	self.malesSingAll = 0
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
	self.offsetCamera( breve.vector( 0, 0, 22) ) # (0, 0, z) depends on the picture's size
        # End of environment

        # Loading frogs
        self.loadMaleFrogs()
	self.loadFemaleFrogs()
	self.movement = breve.createInstances(breve.Movement, 1)
#        self.setUpMenus()

    def iterate(self):
        breve.Control.iterate(self)
	if self.malesSingAll == -1 :
            if self.malesPlaced() :
                self.loadFemaleFrogs()

        print self.frogs[5].state

    
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
        envNames = self.config.getValue("envNames") #envNames is a tuple
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

    def loadMaleFrogs(self):
        frogsMaleNumber = self.config.getValue("frogsMaleNumber")
        del(self.frogsMale[:])
        self.frogsMale = breve.createInstances(breve.Male, frogsMaleNumber)
        self.frogs.extend(self.frogsMale)

    def loadFemaleFrogs(self):
	frogsFemaleNumber = self.config.getValue("frogsFemaleNumber")
	del(self.frogsFemale[:])
	self.frogsFemale = breve.createInstances(breve.Female, frogsFemaleNumber)
	self.frogs.extend(self.frogsFemale)

    def selectMovement(self, id):
        return self.movement.selectMovement(id)

    def getNearestForest(self, location):
        Forest = self.config.getValue("forestCenter")
        nearest = (Forest[0],Forest[1])
        for i in range(2, len(Forest), 2):
            if( sqrt((Forest[i]-location.x)**2 + (Forest[i+1]-location.y)**2) < sqrt((nearest[0]-location.x)**2 + (nearest[1]-location.y)**2)) :
                nearest = (Forest[i],Forest[i+1])
        return breve.vector(nearest[0], nearest[1], 0)

    def getNearestWater(self, location):
        water = self.config.getValue("waterCenter")
        nearest = (water[0],water[1])
        for i in range(2, len(water), 2):
            if( sqrt(water[i]**2 + water[i+1]**2) < sqrt(nearest[0]**2 + nearest[1]**2)) :
                nearest = (water[i],water[i+1])
        return breve.vector(nearest[0], nearest[1], 0)

# je propose de fusionner les diff�rents getNearest en fonction du fichier de config ?

    def getEnvironment(self, location):
        pixelColor = self.image.getRgbPixel(location.x, location.y)
        for env in self.environment:
            if (env.getColor() == pixelColor):
                return env
        return Environment("No environnement", "black")

    def getSoundLevel(self, location):
        '''
        location : position in the simulation (location.x & location.y)
        '''
        SPL = 0
        for frog in self.frogs:
            
            if frog.state == 'singing' :
                #pos = self.worldToImage(frog.getLocation())
                pos = frog.getLocation()
                dist = (location.x - pos.x)**2 + (location.y - pos.y)**2
                if dist <= 0:
                    sndLvl = frog.voicePower
                else:
                    sndLvl = frog.voicePower - 10*log10(dist)
                SPL += 10**(sndLvl/10) # SPL = 10^(SPL1/10) + 10^(SPL2/10) + ...
        if SPL == 0 :
            return 0
        level = 10 * log10(SPL)  # I = 10 * log( SPL) dB
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
            if frog.state == 'singing' :
                pos = frog.getLocation()
                weight = frog.voicePower
                xG += weight*pos.x # calculating the numerators, for the x coordinate
                yG += weight*pos.y # for the y one
                weightSum += weight # denominator (same for every coord)
        xG /= weightSum
        yG /= weightSum
        return breve.vector(xG, yG, 0.01) # simulation coordinates
    
    def getNbFrogsSinging(self):
        i = 0
        for frog in self.frogsMale:
            if frog.state == 'singing' :
                i+=1
        return i


    def malesPlaced(self):
            self.malesSingAll = 1
            for frog in self.frogsMale:
                if frog.state != 'singing' :
                    self.malesSingAll = 0
                    break
            return self.malesSingAll
        
    def onBorder(self, location):
        tooMuch = [] #array( left, right, top, bottom)
        if (location.x >= 8):
            tooMuch.append(False)
            tooMuch.append(True)
        elif location.x <= -8:
            tooMuch.append(True)
            tooMuch.append(False)
        else:
            tooMuch.append(False)
            tooMuch.append(False)

        if (location.y >= 8):
            tooMuch.append(True)
            tooMuch.append(False)
        elif location.y <= -8:
            tooMuch.append(False)
            tooMuch.append(True)
        else:
            tooMuch.append(False)
            tooMuch.append(False)
        return tooMuch

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

#    def debugSound(self):
#        test = breve.createInstances(breve.Mobile, 1)
#        test.setShape(breve.createInstances(breve.Cube, 1).initWith(breve.vector(0.1, 0.1, 0.1)))
#        tab = self.movement.getMoveField(test.getLocation(), 0.3)
#        maxDB = 0
#	for i in range(len(tab)) :
#		gog = breve.createInstances(breve.Mobile, 1)
#                gog.move(tab[i])
#                gog.setShape(breve.createInstances(breve.Cube, 1).initWith(breve.vector(0.1, 0.1, 0.1)))
#                if maxDB <= self.controller.getSoundLevel(gog.getLocation()):
#                    maxDB = self.controller.getSoundLevel(gog.getLocation())
#                    dotChoice = gog
#                    iChoice = i
#        dotChoice.setColor(breve.vector(1, 0, 0))
#        print iChoice

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



