# -*- coding: utf-8 -*-
from json import JSONDecoder
from confibula.utils.config import Config
from random import randint
from fractions import Fraction

#coef Gini
cumulative = lambda x: map(lambda y: sum(x[:y+1]), range(len(x)))
giniCoeff = lambda l: sum(map(lambda x: x[0] - x[1], zip(map(lambda x: Fraction(x, len(l)), range(1, len(l))), map(lambda x: Fraction(x, sum(l)), cumulative(sorted(l))[:-1])))) * Fraction(2, len(l) - 1)

class Individu():
	
	def __init__(self):
		self.config = Config("confibulaInit.cfg")
		self.config.load()
		self.male = [0 for i in range(self.config.getValue("frogsMaleNumber"))]
		self.coefComp = 0.0
		self.log = None
		
	def setLog(self, log):
		""" json.JSONDecoder().decode(open("logs/5.log").read())"""
		self.log = log
	
	def setCoefComp(self):
		jsMale = self.log["frogs"]["males"]
		i=0
		for male in jsMale:
			jsFemale = jsMale[male]["WithCoupling"]
			for female in jsFemale:
				self.male[i] += 1 
			i += 1
			
		femaleNumber = self.config.getValue("frogsMaleNumber")
		tab=[femaleNumber]
		tab.extend(self.male)
		self.coefComp = float(giniCoeff(tab))
	
		
	    
	def changeParam(self):
		val = 0;
		#niv energie; patience ; vitesse;
		val = self.config.getValue("lowLimitMinEnergy")
		val += randint(-5,5)
		self.config.setValue("lowLimitMinEnergy",val)

		val = self.config.getValue("highLimitMinEnergy")
		val += randint(-5,5)
		if self.config.getValue("lowLimitMinEnergy") >= val:
			val += self.config.getValue("lowLimitMinEnergy") - val + 1
		self.config.setValue("highLimitMinEnergy",val)

		val = self.config.getValue("lowLimitMaxEnergy")
		val += randint(-5,5)
		self.config.setValue("lowLimitMaxEnergy",val)

		val = self.config.getValue("highLimiteMaxEnergy")
		val += randint(-5,5)
		if self.config.getValue("lowLimitMaxEnergy") >= val:
			val += self.config.getValue("lowLimitMaxEnergy") - val + 1
		self.config.setValue("highLimiteMaxEnergy",val)

		val = self.config.getValue("dbMaxToSing")
		val += randint(-5,5)
		self.config.setValue("dbMaxToSing",val)

		val = self.config.getValue("visionDistanceMale")
		val += randint(-5,5)
		self.config.setValue("visionDistanceMale",val)

		val = self.config.getValue("patienceTimeToCoupling")
		val += randint(-5,5)
		self.config.setValue("patienceTimeToCoupling",val)

		val = self.config.getValue("lowVoicePower")
		val += randint(-5,5)
		self.config.setValue("lowVoicePower",val)

		val = self.config.getValue("highVoicePower")
		val += randint(-5,5)
		if self.config.getValue("lowVoicePower") >= val:
			val += self.config.getValue("lowVoicePower") - val + 1
		self.config.setValue("highVoicePower",val)

		val = self.config.getValue("lowVoiceQuality")
		val += randint(-5,5)
		self.config.setValue("lowVoiceQuality",val)

		val = self.config.getValue("highVoiceQuality")
		val += randint(-5,5)
		if self.config.getValue("lowVoiceQuality") >= val:
			val += self.config.getValue("lowVoiceQuality") - val + 1
		self.config.setValue("highVoiceQuality",val)

		val = self.config.getValue("lowThroatColor")
		val += randint(-5,5)
		self.config.setValue("lowThroatColor",val)
		
		val = self.config.getValue("highThroatColor")
		val += randint(-5,5)
		if self.config.getValue("lowThroatColor") >= val:
			val += self.config.getValue("lowThroatColor") - val + 1
		self.config.setValue("highThroatColor",val)

		val = self.config.getValue("visionDistance")
		val += randint(-5,5)
		self.config.setValue("visionDistance",val)

		val = self.config.getValue("minChorusSize")
		val += randint(-5,5)
		if val < 0:
			val = 0
		self.config.setValue("minChorusSize",val)
		
	def __cmp__(self,other):
		return cmp(self.coefComp, other.coefComp)
