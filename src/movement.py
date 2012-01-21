from math import sin, cos, pi, sqrt
import breve
from random import uniform, randint

class Movement(breve.Abstract):

    def __init__(self):
        breve.Abstract.__init__(self)
        self.init()

    def init(self):
        print 'movement ok'

    def selectMovement(self, id):
        if isinstance(self.getFrog(id), breve.Male) :
            if self.getFrog(id).state == 'moveToSing' :
                return self.moveToSing(id)
            elif self.getFrog(id).state == 'singing' :
                return self.singing(id)
            elif self.getFrog(id).state == 'hunting' :
                return self.hunter(id)
        elif isinstance(self.getFrog(id), breve.Female) :
            return self.randomMovement(id)
        else:
                return self.randomMovement(id)

    def randomMovement(self, id):
        speed = 3 * (float(self.getFrog(id).energy)/1000)
        x, y = uniform(-speed, speed), uniform(-speed, speed)
        self.getFrog(id).energy -= x**2 + y**2
        return breve.vector(x, y, 0)


    def cheater(self):
        return 0

    def singing(self, id):
        self.getFrog(id).energy -= 3
        return breve.vector(0, 0, 0)

    def moveToSing(self, id):
        speed = 2 * (float(self.getFrog(id).energy)/1000)
        location = self.getFrog(id).getLocation()
        if( (self.controller.getSoundLevel(location) > self.controller.config.getValue("dbMaxToSing")-5 and self.controller.getSoundLevel(location) < self.controller.config.getValue("dbMaxToSing") ) or self.controller.getSoundLevel(location) == 0) :

            self.getFrog(id).state = 'singing'
            return breve.vector(0, 0, 0)

        elif(self.controller.getSoundLevel(location) < self.controller.config.getValue("dbMaxToSing") ) :

            distanceX = (self.controller.getSoundSource().x - location.x)
            distanceY = (self.controller.getSoundSource().y - location.y)
            distance = sqrt( distanceX**2 +  distanceY**2  )
            x = (distance/distanceX)*speed
            y = (distance/distanceY)*speed
            return breve.vector(x, y, 0)

        elif(self.controller.getSoundLevel(location) > self.controller.config.getValue("dbMaxToSing")-5) :
            tab = []
            tab.append( breve.vector(location.x + speed, location.y, 0) )
            tab.append( breve.vector(location.x - speed, location.y, 0) )
            tab.append( breve.vector(location.x, location.y + speed, 0) )
            tab.append( breve.vector(location.x, location.y - speed, 0) )
            tab.append( breve.vector(location.x + cos(pi/4)*speed, location.y + sin(pi/4)*speed, 0) )
            tab.append( breve.vector(location.x + cos(pi/4)*speed, location.y - sin(pi/4)*speed, 0) )
            tab.append( breve.vector(location.x - cos(pi/4)*speed, location.y + sin(pi/4)*speed, 0) )
            tab.append( breve.vector(location.x - cos(pi/4)*speed, location.y - sin(pi/4)*speed, 0) )

            min = tab[0]
            middle = self.controller.config.getValue("dbMaxToSing")-2.5
            for point in tab[1:] :
                if( (self.controller.getSoundLevel(point)-middle)**2 < (self.controller.getSoundLevel(min)-middle)**2 ) :
                    min = point
            return min

    def hunter(self):
        env = self.getEnvironment()
        if uniform(0, 1) < env.predatorProbability :
            self.getFrog(id).encounteredPredators += 1
            return -100
        if uniform(0, 1) < env.preyProbability :
            self.getFrog(id).encounteredPreys += 1
            self.getFrog(id).totalEnergyBoost += env.preyEnergyBoost
            return env.preyEnergyBoost
        return 0

    def findPartner(self):
        return 0

    def getEnvironment(self, id):
        return self.controller.getEnvironment(self.controller.worldToImage(self.getFrog(id).getLocation()))

    def getFrog(self, id):
        return self.controller.frogs[id-1]

breve.Movement = Movement
