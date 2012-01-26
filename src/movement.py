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
	print 'movement ok'

    def selectMovement(self, id):
	if self.getFrog(id).state == 'coupling':
            return self.coupling(id)
        elif self.getFrog(id).state == 'sleeping':
            self.getFrog(id).sleepTime +=1
            return self.sleeping(id,self.getFrog(id).sleepTime)

	elif isinstance(self.getFrog(id), breve.Male):

            if self.getFrog(id).state == 'moveToSing':
                return self.moveToSing(id)
            elif self.getFrog(id).state == 'singing':
                return self.singer(id)
            elif self.getFrog(id).state == 'hunting':
                return self.hunter(id)

	elif isinstance(self.getFrog(id), breve.Female):

            if self.getFrog(id).state == 'findPartener':
		return self.findPartner(id)
            elif self.getFrog(id).state == 'hunting':
		return self.hunter(id)
	else:
		return self.randomMovement(id)

    def hunter(self, id):
        env = self.getEnvironment(id)
        
        if (self.getFrog(id).energy > (self.getFrog(id).maxEnergy / 100.) * 1000):
            if isinstance(self.getFrog(id), breve.Female):
                self.getFrog(id).state = 'findPartener'
            elif isinstance(self.getFrog(id), breve.Male):
                self.getFrog(id).state = 'moveToSing'


        elif isinstance(self.getFrog(id), breve.Female):
            self.getFrog(id).energy += 10
            self.getFrog(id).state == 'hunting'

        elif isinstance(self.getFrog(id), breve.Male):
            self.getFrog(id).energy += 1
            self.getFrog(id).state == 'hunting'

        return self.randomMovement(id)


#        elif env == 'Eau':
#            self.getFrog(id).state == 'hunting'
#        elif env == 'Foret':
#            self.getFrog(id).state == 'hunting'
#            if uniform(0, 1) < env.preyProbability:
#                self.getFrog(id).energy += 500

#        return self.randomMovement(id)

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
#	return self.randomMovement(id)

    def moveToSing(self, id):
        speed = float(self.getFrog(id).energy) / 1000
        location = self.getFrog(id).getLocation()
        soundLevel = self.controller.getSoundLevel(location)
        dbMaxToSing = self.controller.config.getValue("dbMaxToSing")
        env = self.getEnvironment(id).getName()
        if(((soundLevel > dbMaxToSing -5 and soundLevel < dbMaxToSing) or soundLevel == 0) and env == 'Eau'):

            self.getFrog(id).state = 'singing'
            return breve.vector(0, 0, 0)

        else: # deplacements
            self.getFrog(id).energy -= speed / 2
            if (env != 'Eau' or soundLevel >= dbMaxToSing):
                moveField = self.getMoveField(location, speed)

            if(env != 'Eau'):
                return breve.vector(0, 0, 0)
            elif(soundLevel < dbMaxToSing):
                return self.moveTo(location, self.controller.getSoundSource(), speed)
            else: # to close to sing
                min = moveField[0]
                middle = dbMaxToSing-2.5
                for point in moveField[1:]:
                    if((self.controller.getSoundLevel(point)-middle) ** 2 < (self.controller.getSoundLevel(min)-middle) ** 2):
                        min = point
                return min - breve.vector(location.x, location.y, 0)

    def singer(self, id):
        if (self.getFrog(id).energy <= (self.getFrog(id).minEnergy / 100.) * 1000):
            self.getFrog(id).state = 'hunting'
        else:
            self.getFrog(id).energy -= 1
        return breve.vector(0, 0, 0)

    def findPartner(self, id):
	female = self.getFrog(id)
	location = female.getLocation()
	speed = float(female.energy) / 1000
	viewMale = female.viewMale()
	
	if self.controller.getSoundLevel(location):
		if viewMale != 0:
			return self.partnerChoice(viewMale, id, speed)
		else:
			moveField = self.getMoveField(location, speed)
			maxDB = self.controller.getSoundLevel(moveField[0])
#			print maxDB
			dotChoice = moveField[0]
#			print dotChoice
		for dot in moveField[1:]:
#			print self.controller.getSoundLevel(dot)
			if maxDB <= self.controller.getSoundLevel(dot):
				maxDB = self.controller.getSoundLevel(dot)
				dotChoice = dot
#				print 'up',maxDB
#		print 'location :',self.getFrog(id).getLocation()
#		print dotChoice, '    ', maxDB
		return dotChoice - breve.vector(location.x,location.y,0)
        else:
		female.state = 'hunting'
		return self.hunter(id)

    def partnerChoice(self, listPartner, id, speed):#choisis un partner en fonction du tableau de male passé en parametre
	malePower = listPartner[0].voicePower + listPartner[0].voiceQuality + listPartner[0].throatColor
	maleChoice = listPartner[0]
	
	for male in listPartner[1:]:
		if malePower > (male.voicePower + male.voiceQuality + male.throatColor):
			malePower = male.voicePower + male.voiceQuality + male.throatColor
			maleChoice = male
        femeleX = int(self.getFrog(id).getLocation().x * 10)
        femeleY = int(self.getFrog(id).getLocation().y * 10)
        maleX = int(maleChoice.getLocation().x * 10)
        maleY = int(maleChoice.getLocation().y * 10)
        if(femeleX == maleX and femeleY == maleY):
            maleChoice.state = "coupling"
            self.getFrog(id).state = "coupling"
	return self.moveTo(self.getFrog(id).getLocation(), maleChoice.getLocation(), speed)

    def randomMovement(self, id):
        speed = float(self.getFrog(id).energy) / 2000
        x, y = uniform(-speed, speed), uniform(-speed, speed)
        self.getFrog(id).energy -= (x ** 2 + y ** 2) / 2
	return breve.vector(x, y, 0)


    def cheater(self):
	return breve.vector(0, 0, 0)

    def moveTo(self, location, destination, speed):
        direction = destination - location
	direction.x = direction.x
	direction.y = direction.y
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
