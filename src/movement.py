
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
	    return self.randomMovement(id)
	else :
	    return self.randomMovement(id)
	
    def randomMovement(self, id):
	speed = 3 * (float(self.getFrog(id).energy)/1000)
        x, y = uniform(-speed, speed), uniform(-speed, speed)
        self.getFrog(id).energy -= x**2 + y**2
	return breve.vector(x, y, 0)
	 
	
    def cheater(self):
	return 0
	
    def singer(self):
	return 0
	
    def hunter(self):
	env = self.getEnvironment()
        if uniform(0, 1) < env.predatorProbability :
            self.encounteredPredators += 1
            return -100
        if uniform(0, 1) < env.preyProbability :
            self.encounteredPreys += 1
            self.totalEnergyBoost += env.preyEnergyBoost
            return env.preyEnergyBoost
	return 0
	
    def findPartner(self):
	return 0
	
    def getEnvironment(self, id):
        return self.controller.getEnvironment(self.controller.worldToImage(self.getFrog(id).getLocation()))
        
    def getFrog(self, id):
        return self.controller.frogs[id-1]
	
breve.Movement = Movement

