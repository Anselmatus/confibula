from math import cos, pi, sin, sqrt
from random import randint, uniform


import breve

class Movement(breve.Abstract):

    def __init__(self):
	breve.Abstract.__init__(self)
	self.init()

    def init(self):
        # env = self.getEnvironment(id)
	print 'movement ok'

    def selectMovement(self, id):
        frog = self.getFrog(id)
	location = frog.getLocation()
	speed = frog.speed()

        # Coupling & Sleeping state
	if frog.state == 'coupling':
            return self.coupler(id)
        elif frog.state == 'sleeping':
            frog.sleepTime +=1
            return self.sleeper(id,frog.sleepTime)

        # Classic Male Movement
	elif isinstance(frog, breve.Male):
            if frog.state == 'moveToSing':
                if frog.isCheater == True:
                    return self.cheater(id, location, speed)
                else:
                    return self.moveToSing(id, location, speed)
            elif frog.state == 'singing':
                return self.singer(id)
            elif frog.state == 'hunting':
                return self.hunter(id, speed, location)
            elif frog.state == 'unLockFromForest' :
                return self.unLockFrog(location, speed)

        # Classic Female Movement
	elif isinstance(frog, breve.Female):
            if frog.state == 'findPartener':
                desire = uniform(0,100)
                if(desire < frog.seuil):
                    return self.findBestMale(id, location, speed)
                else:
                    frog.seuil += uniform(0,1)
                    frog.state = 'hunting'
                    return self.hunter(id, speed, location)
            elif frog.state == 'hunting':
		return self.hunter(id, speed, location)

        # Error Movement
        return self.randomMovement(id, speed)

    def hunter(self, id, speed, location):
        frog = self.getFrog(id)
        recoveryEnergyLevel = ((frog.maxEnergy / 100.) * 1000)
        env = self.getEnvironment(id)
        envName = env.getName()

        if envName == "No environnement":
            return self.moveTo(location, breve.vector(0,0,0), speed)

        # what happen when energy is recovery
        if (frog.energy > recoveryEnergyLevel):
            if isinstance(frog, breve.Female):
                frog.state = self.controller.config.getValue('standartFemaleState')
            elif isinstance(self.getFrog(id), breve.Male) :
                frog.state = self.controller.config.getValue('standartMaleState')

        if uniform(0, 1) < env.preyProbability:
            frog.encounteredPreys += 1
            frog.totalEnergyBoost += env.preyEnergyBoost
            frog.energy += env.preyEnergyBoost

        if uniform(0, 1) < env.predatorProbability:
            frog.encounteredPredators += 1
            frog.energy -= env.predatorEnergyLost

        if isinstance(frog, breve.Male):
            if uniform(0, 1) < env.preyProbability:
                frog.throatColor += env.preyProteinBoost
            if uniform(0, 1) < env.predatorProbability:
                frog.throatColor -= env.predatorProteinLost

        frog.state == 'hunting'
        return self.randomMovement(id, speed)
    
#        frog = self.getFrog(id)
#        recoveryEnergyLevel = ((frog.maxEnergy / 100.) * 1000)
#        env = self.getEnvironment(id)
#        envName = env.getName()
#
#        if envName == "No environnement":
#            return self.moveTo(location, breve.vector(0,0,0), speed)
#
#        # what happen when energy is recovery
#        if (frog.energy > recoveryEnergyLevel):
#            if isinstance(frog, breve.Female):
#                frog.state = self.controller.config.getValue('standartFemaleState')
#            elif isinstance(self.getFrog(id), breve.Male) :
#                frog.state = self.controller.config.getValue('standartMaleState')
#
#        if uniform(0, 1) < env.preyProbability:
#            frog.encounteredPreys += 1
#            frog.totalEnergyBoost += env.preyEnergyBoost
#            frog.energy += env.preyEnergyBoost
#
#        if uniform(0, 1) < env.predatorProbability:
#            frog.encounteredPredators += 1
#            frog.energy -= env.predatorEnergyLost
#
#        if isinstance(frog, breve.Male):
#            if uniform(0, 1) < env.preyProbability:
#                frog.throatColor += env.preyProteinBoost
#            if uniform(0, 1) < env.predatorProbability:
#                frog.throatColor -= env.predatorProteinLost
#
#        if envName == "Eau":
#            forestCenter = self.controller.getNearestForest(location)
#            return self.moveTo(location, forestCenter, speed)
#
#        frog.state == 'hunting'
#        return self.randomMovement(id, speed)

    def moveToSing(self, id, location, speed):
        male = self.getFrog(id)
        soundLevel = self.controller.getSoundLevel(location)
        dbMaxToSing = self.controller.config.getValue("dbMaxToSing")
        env = self.getEnvironment(id).getName()

        if( ( ( soundLevel > dbMaxToSing -1 and soundLevel < dbMaxToSing ) or soundLevel == 0 ) and env == 'Eau') :
            male.state = 'singing'
            return breve.vector(0, 0, 0)
        else : # movement
            male.energy -= speed/2
            
            if(env != 'Eau'):
                if( soundLevel == 0 ) :
                    return self.moveTo(location, self.controller.getNearestWater(location), speed)
                elif soundLevel >= dbMaxToSing:
                    self.state = 'unLockFromForest'
                    return self.unLockFrog(location,speed)
                else :
                    return self.moveTo(location, self.controller.getSoundSource(), speed)
            elif(soundLevel < dbMaxToSing):
                
                direction = self.moveTo(location, self.controller.getSoundSource(), speed)
                if( self.controller.getEnvironment(self.controller.worldToImage(direction + location)).getName() == 'Eau' ) :
                    return direction
                else :
                    return self.moveToLevelSong(location, speed, 0, 1)
            else: # if Sound is too high 
                return self.moveToLevelSong(location, speed, 0, 1)



    def singer(self, id):
        if (self.getFrog(id).energy <= (self.getFrog(id).minEnergy / 100.) * 1000):
            self.getFrog(id).state = 'hunting'
        else :
            self.getFrog(id).energy -= self.controller.config.getValue('singingEnergyCost')
        return breve.vector(0, 0, 0)

    def findBestMale(self, id, location, speed, distanceToStop=0):
        frog = self.getFrog(id)
	viewMale = frog.viewMale()
	
	if self.controller.getSoundLevel(location) and self.controller.getNbFrogsSinging() >= self.controller.config.getValue("minChorusSize"):
            if viewMale != 0:
                maleChoice = self.partnerChoice(viewMale, id)
                distanceToMale = frog.getDistance(maleChoice)
                if(distanceToStop <= 0):
                    direction =  maleChoice.getLocation()
    #                    rand = uniform(-0.4,0.4)
    #                    direction.x -= rand
    #                    direction.y += rand
                    return self.moveTo(location, direction, speed)
                else:
                    if(float(distanceToMale) > float(distanceToStop)):
                        direction =  maleChoice.getLocation()
    #                        rand = uniform(-0.4,0.4)
    #                        direction.x += rand
    #                        direction.y -= rand
                        return self.moveTo(location, direction, speed)
                    else:
                        return breve.vector(0, 0, 0)
            else:
                levelSong = 1000
                return self.moveToLevelSong(location, speed, levelSong)
        else:
            frog.state = 'hunting'
            return self.hunter(id, speed, location)

    def partnerChoice(self,listPartner,id): # choose a frogpartner considering a frogtable in parameter
	maleChoice = self.getFrog(id).getBestMale(listPartner)
        femeleX = int(self.getFrog(id).getLocation().x * 10)
        femeleY = int(self.getFrog(id).getLocation().y * 10)
        maleX = int(maleChoice.getLocation().x * 10)
        maleY = int(maleChoice.getLocation().y * 10)
        if(femeleX == maleX and femeleY == maleY):
            maleChoice.state = "coupling"
            self.getFrog(id).state = "coupling"
	return maleChoice

    def randomMovement(self, id, speed):
        x, y = uniform(-speed, speed), uniform(-speed, speed)
        self.getFrog(id).energy -= ( x ** 2 + y ** 2 ) / 2 # specific energy lost
	return breve.vector(x, y, 0)

    def cheater(self, id, location, speed):
        cheater = self.getFrog(id) 
        viewFemale = cheater.viewFemale()
        if viewFemale != 0:
            femaleChoice = cheater.getBestFemale(viewFemale)
            cheaterX = int(location.x * 10)
            cheaterY = int(location.y * 10)
            femaleX = int(femaleChoice.getLocation().x * 10)
            femaleY = int(femaleChoice.getLocation().y * 10)
            if(cheaterX == femaleX and cheaterY == femaleY):
                femaleChoice.state = "coupling"
                cheater.state = "coupling"
            return self.moveTo(location, femaleChoice.getLocation(), speed)
        else:
            return self.findBestMale(id, location, speed, 0.5)
    
    def moveToLevelSong(self, location, speed, levelSong, water=0):
        moveField = self.getMoveField(location, speed)
        min = moveField[0]
        for point in moveField[1:]:
            if (water != 0) : # param to say if we avoid water or not
                envPoint = self.controller.getEnvironment(self.controller.worldToImage(point)).getName()
            else :
                envPoint = 'Eau'
            if((((self.controller.getSoundLevel(point)-levelSong ) ** 2) < ((self.controller.getSoundLevel(min)-levelSong) ** 2) ) and envPoint == 'Eau'):
                min = point
        return min - breve.vector(location.x, location.y, 0)

    def unLockFrog(self, location, speed):
        levelSong = 0
        unlockVector = self.moveToLevelSong(location, speed, levelSong)
        if ( self.controller.getEnvironment(self.controller.worldToImage(unlockVector-location)).getName() == 'Eau') :
            self.state = 'moveToSing'
        return unlockVector


 #   def rotation(self, angle, direction):
 #       cosAngle = cos(angle)
 #       sinAngle = sin(angle)
 #       newX = direction.x * cosAngle-direction.y * sinAngle
 #       newY = direction.y * cosAngle + direction.x * sinAngle
 #       direction.x = newX
 #       direction.y = newY
 #       return direction
        
    def moveTo(self, location, destination, speed):    
        direction = destination - location
        distance = sqrt(direction.x ** 2 + direction.y ** 2)
        return (direction / distance) * speed

    def getEnvironment(self, id):
        return self.controller.getEnvironment(self.controller.worldToImage(self.getFrog(id).getLocation()))

    def getFrog(self, id):
	return self.controller.frogs[id-1]

    def getMoveField(self, location, speed):
        moveField = [] # array of point around the frog
        moveField.append(breve.vector(location.x + speed, location.y, 0))
        moveField.append(breve.vector(location.x - speed, location.y, 0))
        moveField.append(breve.vector(location.x, location.y + speed, 0))
        moveField.append(breve.vector(location.x, location.y - speed, 0))
        moveField.append(breve.vector(location.x + cos(pi / 4) * speed, location.y + sin(pi / 4) * speed, 0))
        moveField.append(breve.vector(location.x + cos(pi / 4) * speed, location.y - sin(pi / 4) * speed, 0))
        moveField.append(breve.vector(location.x - cos(pi / 4) * speed, location.y + sin(pi / 4) * speed, 0))
        moveField.append(breve.vector(location.x - cos(pi / 4) * speed, location.y - sin(pi / 4) * speed, 0))
        return moveField

    def coupler(self, id):
        if (self.getFrog(id).energy <= (self.getFrog(id).minEnergy / 100.0) * 1000):
            self.getFrog(id).state = 'sleeping'
            self.getFrog(id).nbCoupling=self.getFrog(id).nbCoupling+1
            self.getFrog(id).timeLastCoupling = self.controller.getTime()
            if isinstance(self.getFrog(id), breve.Male) and self.getFrog(id).isCheater == True:
                self.getFrog(id).isCheater = False
        else:
            self.getFrog(id).energy -= self.controller.config.getValue("couplingEnergyCost")
        return breve.vector(0, 0, 0)

    def sleeper(self,id,sleepTime):
        frog = self.getFrog(id)
        if isinstance(frog, breve.Female):
            if sleepTime >= self.controller.config.getValue("timeToSleepFemale"):
                frog.sleepTime = 0
                frog.seuil = 0
                frog.state = 'hunting'
#            print self.controller.config.getValue("timeToSleepFemale")

        if isinstance(frog, breve.Male):
            if sleepTime >= self.controller.config.getValue("timeToSleepMale"):
                frog.sleepTime = 0
                frog.state = 'hunting'
#            print self.controller.config.getValue("timeToSleepMale")
        
#        print sleepTime
        return breve.vector(0,0,0)

breve.Movement = Movement
