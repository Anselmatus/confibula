# -*- coding: utf-8 -*-

from subprocess import call
from subprocess import Popen
import os
from confibula.utils.config import Config
import json
from Individu import Individu
from math import sqrt
from os.path import exists
NBCONF = 10
NBIT = 40
class Opti:
	
	def __init__(self):
		self.pop = [];
    		self.fileConfibula = "./Confibula";
    		self.Confibula = "confibula.py";
    		
    	def init(self):
	    for i in range(NBCONF):
	    	self.pop.append(Individu())
		self.pop[i].config.load()
		self.pop[i].changeParam()
	       
	def routine(self):
		try : os.unlink("./result") 
		except :pass
		
		for i in range(NBIT):
			self.run()			
			self.adequation()
			
			mini = self.pop[0].coefComp 
			maxi = self.pop[0].coefComp 
			moy = 0
			for j in range(NBCONF):
				moy += self.pop[j].coefComp 
				if self.pop[j].coefComp < mini : mini = self.pop[j].coefComp
				if self.pop[j].coefComp > maxi : maxi = self.pop[j].coefComp
			moy /= float(NBCONF)
			fichier = open("./result","a+", 777)
			fichier.write("iteration " + str(i) + " coef minimum :" + str(mini) +"\n")
			fichier.write("iteration " + str(i) + " coef maximum :" + str(maxi) +"\n")
			fichier.write("iteration " + str(i) + " moyenne coef :" + str(moy) +"\n\n")			
			
			self.mutation()
		self.pop[0].config.save("meilleureConfig.cfg")
		
	def adequation(self):
		for indiv in self.pop:
			indiv.setCoefComp()
		self.pop.sort()
		self.pop.reverse()
	
	def run(self):
		simulation = []
		for i in range(NBCONF):
			try:
				os.mkdir("./config")
			except:
				print "pass !1"
				pass
				
			try:
				os.mkdir("./config/"+str(i))
			except:
				print "pass !2"
				pass
			call("ls")
			os.chdir("./config/"+str(i))
			try:
				os.unlink("./logs/1.log")
			except:
				print "pass 3 !"
				pass
			self.pop[i].config.changeFile("confibula.cfg")
			self.pop[i].config.save()
			while not exists("./logs/1.log"): 
				simulation.append(call("breve -x -u -t 30 ../../confibula/confibula.py", shell=True))
			fichierLog = open("./logs/1.log","r+").read()
			#simulation.append(Popen("breve -x -u -t 3 ../../confibula/confibula.py", shell=True))		
			self.pop[i].setLog(json.JSONDecoder().decode(fichierLog))
			call("ls")
			os.chdir("../../")
			
		#for simul in simulation:
		#	simul.wait()
		
		#for i in range(NBCONF):
		#	os.chdir("./config/"+str(i)+"/logs/")
		#	call("ls")
		#	fichierLog = open("./1.log","r+").read()
		#	self.pop[i].setLog(json.JSONDecoder().decode(fichierLog))
		#	os.chdir("../../../")

        def mutation(self):
		i = 0
	        j = 0
	        k = NBCONF/2
	        
	        tailleSousChaine = int(round(sqrt(NBCONF*(0.4*2)))+1)
	        exces = int(((tailleSousChaine*(tailleSousChaine-1))/2) - (NBCONF*0.4))
	
	        while i<tailleSousChaine and (((tailleSousChaine-i)*(tailleSousChaine-i-1))/2)-exces > 0:
	                restant = (((tailleSousChaine-i)*(tailleSousChaine-i-1))/2)-exces
	                j = i+1
	                while j<tailleSousChaine :
	                        if restant <= tailleSousChaine-i and j > i+restant : break
	                        
	                        
	                        nouveauConf = self.pop[k].config
	                        conf1 = self.pop[i].config
	                        conf2 = self.pop[j].config

	                        nouveauConf.setValue("lowLimitMinEnergy", (conf1.getValue("lowLimitMinEnergy")+conf2.getValue("lowLimitMinEnergy"))/2)
	                        highLimitMinEnergy = (conf1.getValue("highLimitMinEnergy")+conf2.getValue("highLimitMinEnergy"))/2
	                        if nouveauConf.getValue("lowLimitMinEnergy") == highLimitMinEnergy : highLimitMinEnergy += 1
	                        nouveauConf.setValue("highLimitMinEnergy", highLimitMinEnergy )
	                        
	                        
	                        nouveauConf.setValue("lowLimitMaxEnergy", (conf1.getValue("lowLimitMaxEnergy")+conf2.getValue("lowLimitMaxEnergy"))/2 )
	                        highLimiteMaxEnergy = (conf1.getValue("highLimiteMaxEnergy")+conf2.getValue("highLimiteMaxEnergy"))/2
	                        if nouveauConf.getValue("lowLimitMaxEnergy") == highLimiteMaxEnergy : highLimiteMaxEnergy += 1
	                        nouveauConf.setValue("highLimiteMaxEnergy", highLimiteMaxEnergy )
	                        
	                        
	                        nouveauConf.setValue("lowVoicePower", (conf1.getValue("lowVoicePower")+conf2.getValue("lowVoicePower"))/2 )
	                        highVoicePower = (conf1.getValue("highVoicePower")+conf2.getValue("highVoicePower"))/2
	                        if nouveauConf.getValue("lowVoicePower") == highVoicePower : highVoicePower += 1
	                        nouveauConf.setValue("highVoicePower", highVoicePower )
	                        
	                        nouveauConf.setValue("lowVoiceQuality", (conf1.getValue("lowVoiceQuality")+conf2.getValue("lowVoiceQuality"))/2 )
	                        highVoiceQuality =  (conf1.getValue("highVoiceQuality")+conf2.getValue("highVoiceQuality"))/2
	                        if nouveauConf.getValue("lowVoiceQuality") == highVoiceQuality : highVoiceQuality += 1
	                        nouveauConf.setValue("highVoiceQuality", highVoiceQuality)
	                        
	                        nouveauConf.setValue("lowThroatColor", (conf1.getValue("lowThroatColor")+conf2.getValue("lowThroatColor"))/2 )
	                        highThroatColor = (conf1.getValue("highThroatColor")+conf2.getValue("highThroatColor"))/2
	                        if nouveauConf.getValue("lowThroatColor") == highThroatColor : highThroatColor += 1
	                        nouveauConf.setValue("highThroatColor", highThroatColor )
	                        
	                        
	                        nouveauConf.setValue("visionDistanceMale", (conf1.getValue("visionDistanceMale")+conf2.getValue("visionDistanceMale"))/2 )
	                        nouveauConf.setValue("patienceTimeToCoupling", (conf1.getValue("patienceTimeToCoupling")+conf2.getValue("patienceTimeToCoupling"))/2 )
	                        nouveauConf.setValue("dbMaxToSing", (conf1.getValue("dbMaxToSing")+conf2.getValue("dbMaxToSing"))/2 )
	                        nouveauConf.setValue("visionDistance", (conf1.getValue("visionDistance")+conf2.getValue("visionDistance"))/2 )
	                        nouveauConf.setValue("minChorusSize", (conf1.getValue("minChorusSize")+conf2.getValue("minChorusSize"))/2 )
	                        

	                        k += 1
	                        j += 1
	                        
	                i += 1
	        i = int((NBCONF*0.9)-1)
	        for i in range(NBCONF) :
				self.pop[i].changeParam()
	              

