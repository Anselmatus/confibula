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
	if isinstance(self.getFrog(id), breve.Male):

            if self.getFrog(id).state == 'moveToSing':
                return self.moveToSing(id)
            elif self.getFrog(id).state == 'singing':
                return self.singer(id)
            elif self.getFrog(id).state == 'hunting':
                return self.hunter(id)

	if isinstance(self.getFrog(id), breve.Female) :

            if self.getFrog(id).state == 'findPartener' :
                return self.findPartner(id)
	    elif self.getFrog(id).state == 'hunting' :
                return self.hunter(id)
            else :
		return self.randomMovement(id)



    def hunter(self, id):
#        env = self.getEnvironment()
#        if uniform(0, 1) < env.predatorProbability:
#            self.getFrog(id).encounteredPredators += 1
#            return -100
#        if uniform(0, 1) < env.preyProbability:pte
#            self.getFrog(id).encounteredPreys += 1
#            self.getFrog(id).totalEnergyBoost += env.preyEnergyBoost
#            return env.preyEnergyBoost
	if isinstance(self.getFrog(id), breve.Female) :
	    self.getFrog(id).sate = 'findPartener'
	return self.randomMovement(id)

    def moveToSing(self, id):
        speed = float(self.getFrog(id).energy)/1000
        location = self.getFrog(id).getLocation()
        soundLevel = self.controller.getSoundLevel(location)
        dbMaxToSing = self.controller.config.getValue("dbMaxToSing")
        env = self.getEnvironment(id).getName()

        if( ( ( soundLevel > dbMaxToSing -5 and soundLevel < dbMaxToSing ) or soundLevel == 0 ) and env == 'Eau') :

            self.getFrog(id).state = 'singing'
            return breve.vector(0, 0, 0)

        else : # deplacements
            self.getFrog(id).energy -= speed/2
            if (env != 'Eau' or soundLevel >= dbMaxToSing) :
                moveField = self.getMoveField(location, speed)

            if(env != 'Eau') :
                print env
                return breve.vector(0, 0, 0)
            elif(soundLevel < dbMaxToSing) :
                return self.moveTo(location, self.controller.getSoundSource(), speed)
            else : # to close to sing
                min = moveField[0]
                middle = dbMaxToSing-2.5
                for point in moveField[1:] :
                    if( (self.controller.getSoundLevel(point)-middle)**2 < (self.controller.getSoundLevel(min)-middle)**2 ) :
                        min = point
                return min - breve.vector(location.x, location.y, 0)

    def singer(self, id):
        if (self.getFrog(id).energy <= (self.getFrog(id).minEnergy/100.)*1000 ) :
            self.getFrog(id).state = 'hunting'
        else :
            self.getFrog(id).energy -= 1
        return breve.vector(0, 0, 0)

    def findPartner(self, id):
	female = self.getFrog(id)
	location = female.getLocation()
	speed = float(female.energy)/2000
	viewMale =female.viewMale()
	if self.controller.getSoundLevel(location):
            if viewMale != 0 :
		return self.partnerChoice(viewMale,id)
            else:
		return self.moveTo(location, self.controller.getSoundSource(), speed)
        else:
		female.state = 'hunter'
		return self.hunter(id)

    def partnerChoice(self,listPartner,id):#choisis un partner en fonction du tableau de male passé en parametre
	malePower = listPartner[0].voicePower + listPartner[0].voiceQuality + listPartner[0].throatColor
	maleChoice = listPartner[0]
	for male in listPartner[1:]:
            if malePower > (male.voicePower + male.voiceQuality + male.throatColor):
                malePower = male.voicePower + male.voiceQuality + male.throatColor
		maleChoice = male
	return maleChoice.getLocation() - self.getFrog(id).getLocation()

    def randomMovement(self, id):
        speed = float(self.getFrog(id).energy)/2000
        x, y = uniform(-speed, speed), uniform(-speed, speed)
        self.getFrog(id).energy -= ( x ** 2 + y ** 2 ) / 2
	return breve.vector(x, y, 0)


    def cheater(self):
	return 0

    def moveTo(self, location, destination, speed):
        direction = destination - location
        distance = sqrt( direction.x**2 +  direction.y**2  )
        return (direction/distance)*speed

    def getEnvironment(self, id):
        return self.controller.getEnvironment(self.controller.worldToImage(self.getFrog(id).getLocation()))

    def getFrog(self, id):
	return self.controller.frogs[id-1]

    def getMoveField(self, location, speed):
        moveField = [] # array of point around the frog
        moveField.append( breve.vector(location.x + speed, location.y, 0) )
        moveField.append( breve.vector(location.x - speed, location.y, 0) )
        moveField.append( breve.vector(location.x, location.y + speed, 0) )
        moveField.append( breve.vector(location.x, location.y - speed, 0) )
        moveField.append( breve.vector(location.x + cos(pi/4)*speed, location.y + sin(pi/4)*speed, 0) )
        moveField.append( breve.vector(location.x + cos(pi/4)*speed, location.y - sin(pi/4)*speed, 0) )
        moveField.append( breve.vector(location.x - cos(pi/4)*speed, location.y + sin(pi/4)*speed, 0) )
        moveField.append( breve.vector(location.x - cos(pi/4)*speed, location.y - sin(pi/4)*speed, 0) )
        return moveField


breve.Movement = Movement
