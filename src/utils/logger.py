# -*- coding: utf-8 -*-


from time import ctime
from os.path import exists
from os import mkdir


console = True
logFile = True
date = str(ctime())
fileName = 'logs/' + date + '.log'
fileName = fileName.replace(' ', '-')
lines = []

def init():
    if logFile:
        if not exists('logs'):
            mkdir('logs')

def log(text):
    """
    Affiche une info de log dans la console et/ou le fichier de log.
    """
    if console:
        print "    ", text
    if logFile:
        lines.append('\t%s\n' % text)

def warn(text):
    """
    Affiche un warning dans la console et/ou le fichier de log.
    """
    if console:
        print text
    if logFile:
        lines.append('/!\ %s /!\ \n' % text)

def title(text):
    """
    Affiche l'entrée ou la sortie d'un partie du code, ex : chargement des paramtres dans la console et/ou le fichier de log.
    """
    if console:
        print text
    if logFile:
        lines.append('$ %s\n' % text)

def error(text):
    """
    Affiche une erreur dans la console et/ou le fichier de log.
    """
    if console:
        print text
    if logFile:
        lines.append('\n##### %s #####\n' % text)

def write():
    if len(lines) > 0:
        file = open(fileName, 'a')
        for line in lines:
            file.write(line)
        del(lines[:])
