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
                return self.singing(id)
            elif self.getFrog(id).state == 'hunting':
                return self.hunter(id)
	if isinstance(self.getFrog(id), breve.Female) :
            if self.getFrog(id).state == 'findPartener' :
                return self.findPartner(id)
	    elif self.getFrog(id).state == 'hunting' :
                return self.hunter(id)
            else :
		return self.randomMovement(id)
	else :
	    return self.randomMovement(id)

    def randomMovement(self, id):
        speed = float(self.getFrog(id).energy)/2000
        x, y = uniform(-speed, speed), uniform(-speed, speed)
        self.getFrog(id).energy -= x ** 2 + y ** 2
	return breve.vector(x, y, 0)


    def cheater(self):
	return 0

    def singing(self, id):
        if (self.getFrog(id).energy <= (self.getFrog(id).minEnergy/100.)*1000 ) :
            self.getFrog(id).state = 'hunter'
        else :
            self.getFrog(id).energy -= 3
        return breve.vector(0, 0, 0)

    def moveToSing(self, id):
        speed = float(self.getFrog(id).energy)/2000
        location = self.getFrog(id).getLocation()
        soundLevel = self.controller.getSoundLevel(location)
        dbMaxToSing = self.controller.config.getValue("dbMaxToSing")
        
        if( ( soundLevel > dbMaxToSing -5 and soundLevel < dbMaxToSing ) or soundLevel == 0) :
            
            self.getFrog(id).state = 'singing'
            return breve.vector(0, 0, 0)

        else :
            self.getFrog(id).energy -= speed**2
            if(soundLevel < dbMaxToSing) :
                return self.moveToChorus(location, speed)

            elif(soundLevel > dbMaxToSing-5) :

                moveField = []
                moveField.append( breve.vector(location.x + speed, location.y, 0) )
                moveField.append( breve.vector(location.x - speed, location.y, 0) )
                moveField.append( breve.vector(location.x, location.y + speed, 0) )
                moveField.append( breve.vector(location.x, location.y - speed, 0) )
                moveField.append( breve.vector(location.x + cos(pi/4)*speed, location.y + sin(pi/4)*speed, 0) )
                moveField.append( breve.vector(location.x + cos(pi/4)*speed, location.y - sin(pi/4)*speed, 0) )
                moveField.append( breve.vector(location.x - cos(pi/4)*speed, location.y + sin(pi/4)*speed, 0) )
                moveField.append( breve.vector(location.x - cos(pi/4)*speed, location.y - sin(pi/4)*speed, 0) )

                min = moveField[0]
                middle = dbMaxToSing-2.5
                for point in moveField[1:] :
                    if( (self.controller.getSoundLevel(point)-middle)**2 < (self.controller.getSoundLevel(min)-middle)**2 ) :
                        min = point
                return min - breve.vector(location.x, location.y, 0)

    def hunter(self, id):
        return self.randomMovement(id)
        env = self.getEnvironment()
        if uniform(0, 1) < env.predatorProbability:
            self.getFrog(id).encounteredPredators += 1
            return -100
        if uniform(0, 1) < env.preyProbability:
            self.getFrog(id).encounteredPreys += 1
            self.getFrog(id).totalEnergyBoost += env.preyEnergyBoost
            return env.preyEnergyBoost
	if isinstance(self.getFrog(id), breve.Female) :
	    self.getFrog(id).sate = 'findPartener'
	return breve.vector(0, 0, 0)

    def moveToChorus(self, location, speed):
	soundSource = self.controller.getSoundSource()
        direction = soundSource - location
        distance = sqrt( direction.x**2 +  direction.y**2  )
        return (direction/distance)*speed

    def findPartner(self, id):
		female = self.getFrog(id)
		location = female.getLocation()
		speed = float(female.energy)/2000
		viewMale =female.viewMale()
		if self.controller.getNbFrogsSinging():
			if viewMale != 0 :
				return self.partnerChoice(viewMale,id)
			else:
				return self.moveToChorus(location, speed)
		else:
			female.state = 'none'
			return self.hunter(id)

    def getEnvironment(self, id):
        return self.controller.getEnvironment(self.controller.worldToImage(self.getFrog(id).getLocation()))

    def getFrog(self, id):
	return self.controller.frogs[id-1]
		
    def partnerChoice(self,listPartener,id):#choisis un partener en fonction du tableau de male passé en parametre
	return breve.vector(0, 0, 0)
breve.Movement = Movement
