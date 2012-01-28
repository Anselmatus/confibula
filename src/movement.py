from math import cos
from math import pi
from math import sin
from math import sqrt
from random import randint
from random import uniform

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
	speed = float(frog.energy) / 1000
	if frog.state == 'coupling':
            return self.coupling(id)
        elif frog.state == 'sleeping':
            frog.sleepTime +=1
            return self.sleeping(id,frog.sleepTime)

	elif isinstance(self.getFrog(id), breve.Male):
            if self.getFrog(id).state == 'moveToSing':
                if self.getFrog(id).isCheater == True:
                    return self.cheater(id, location, speed)
                else:
                    return self.moveToSing(id, location, speed)
            elif self.getFrog(id).state == 'singing':
                return self.singer(id)
            elif frog.state == 'hunting':
                return self.hunter(id, speed)
            elif frog.state == 'unLockFromForest' :
                return self.unLockFrog(location, speed)

	elif isinstance(self.getFrog(id), breve.Female):
            if self.getFrog(id).state == 'findPartener':
		return self.findBestMale(id, location, speed)
            elif self.getFrog(id).state == 'hunting':
		return self.hunter(id, speed)

        return self.randomMovement(id, speed)

    def hunter(self, id, speed):
        frog = self.getFrog(id)
        recoveryEnergyLevel = ((frog.maxEnergy / 100.) * 1000)
        env = self.getEnvironment(id)

        # quoi faire si l'energie est retrouvee
        if (frog.energy > recoveryEnergyLevel):
            if isinstance(frog, breve.Female) :
                frog.state = self.controller.config.getValue('standartFemaleState')
            elif isinstance(self.getFrog(id), breve.Male) :
                frog.state = self.controller.config.getValue('standartMaleState')

        # quoi faire quand l'energie n'est toujours pas pleine
        if isinstance(frog, breve.Female):
            frog.energy += 10
            frog.state == 'hunting'

        elif isinstance(frog, breve.Male):
            frog.energy += 10
            frog.state == 'hunting'

        return self.randomMovement(id, speed)


#        elif env == 'Eau':
#            self.getFrog(id).state == 'hunting'
#        elif env == 'Foret':
#            self.getFrog(id).state == 'hunting'
#            if uniform(0, 1) < env.preyProbability:
#                self.getFrog(id).energy += 500

#        return self.randomMovement(id, speed)

#                self.getFrog(id).encounteredPreys += 1
#                self.getFrog(id).totalEnergyBoost += env.preyEnergyBoost
#                return env.preyEnergyBoost


#        if uniform(0, 1) < env.predatorProbability:
#            self.getFrog(id).encounteredPredators += 1
#            return -100
#        if uniform(0, 1) < env.preyProbability:pte
#            self.getFrog(id).encounteredPreys += 1
#            self.getFrog(id).totalEnergyBoost += env.preyEnergyBoost
#            return env.preyEnergyBoost


#	if isinstance(self.getFrog(id), breve.Female) :
#	    self.getFrog(id).state = 'findPartener'
#	return self.randomMovement(id, speed)

    def moveToSing(self, id, location, speed):
        male = self.getFrog(id)
        soundLevel = self.controller.getSoundLevel(location)
        dbMaxToSing = self.controller.config.getValue("dbMaxToSing")
        env = self.getEnvironment(id).getName()

        if( ( ( soundLevel > dbMaxToSing -5 and soundLevel < dbMaxToSing ) or soundLevel == 0 ) and env == 'Eau') :
            male.state = 'singing'
            return breve.vector(0, 0, 0)
        else : # deplacements
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
                    moveField = self.getMoveField(location, speed)
                    min = moveField[0]
                    for point in moveField[1:]:
                        envPoint = self.controller.getEnvironment(self.controller.worldToImage(point)).getName()
                        if(((self.controller.getSoundLevel(point)-dbMaxToSing) ** 2 < (self.controller.getSoundLevel(min)-dbMaxToSing) ** 2) and envPoint == 'Eau'):
                            min = point
                    return min - breve.vector(location.x, location.y, 0)
            else: # if Sound is too high 
                return self.moveToLevelSong(location, speed, dbMaxToSing-2.5)



    def singer(self, id):
        if (self.getFrog(id).energy <= (self.getFrog(id).minEnergy / 100.) * 1000):
            self.getFrog(id).state = 'hunting'
        else :
            self.getFrog(id).energy -= self.controller.config.getValue('singingEnergyCost')
        return breve.vector(0, 0, 0)

    def findBestMale(self, id, location, speed, distanceToStop=0):
        frog = self.getFrog(id)
	viewMale = frog.viewMale()
	
	if self.controller.getSoundLevel(location):
            if viewMale != 0:
                maleChoice = self.partnerChoice(viewMale, id)
                distanceToMale = frog.getDistance(maleChoice)
                if(distanceToStop <= 0):
                    return self.moveTo(location, maleChoice.getLocation(), speed)
                else:
                    if(float(distanceToMale) > float(distanceToStop)):
                        return self.moveTo(location, maleChoice.getLocation(), speed)
                    else:
                        return breve.vector(0, 0, 0)
            else:
                levelSong = 1000
                return self.moveToLevelSong(location, speed, levelSong)

        else:
		frog.state = 'hunting'
		return self.hunter(id, speed)

    def partnerChoice(self,listPartner,id): # choisis un partner en fonction du tableau de male passé en parametre
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
        self.getFrog(id).energy -= ( x ** 2 + y ** 2 ) / 2 # perte d'energie specifique
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
    
    def moveToLevelSong(self, location, speed, levelSong):
        moveField = self.getMoveField(location, speed)
        min = moveField[0]
        for point in moveField[1:]:
            if((self.controller.getSoundLevel(point)-levelSong) ** 2 < (self.controller.getSoundLevel(min)-levelSong) ** 2):
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

    def coupling(self, id):
        if (self.getFrog(id).energy <= (self.getFrog(id).minEnergy / 100.0) * 1000):
            self.getFrog(id).state = 'sleeping'
        else:
            self.getFrog(id).energy -= self.controller.config.getValue("couplingEnergyCost")
        return breve.vector(0, 0, 0)

    def sleeping(self,id,sleepTime):
        if isinstance(self.getFrog(id), breve.Female):
            if sleepTime >= self.controller.config.getValue("timeToSleepFemale"):
                self.getFrog(id).sleepTime = 0
                self.getFrog(id).state = 'hunting'
#            print self.controller.config.getValue("timeToSleepFemale")

        if isinstance(self.getFrog(id), breve.Male):
            if sleepTime >= self.controller.config.getValue("timeToSleepMale"):
                self.getFrog(id).sleepTime = 0
                self.getFrog(id).state = 'hunting'
#            print self.controller.config.getValue("timeToSleepMale")
        
#        print sleepTime
        return breve.vector(0,0,0)
    
    def energyCost(self):
        energy = 3
        return(energy)

breve.Movement = Movement
