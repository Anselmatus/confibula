# -*- coding: utf-8 -*-

__author__="antoine"
__date__ ="$1 déc. 2011 17:03:48$"

import breve

knownColors = {"black" : breve.vector(0, 0, 0),
                    "white" : breve.vector(1, 1, 1),
                    "blue" : breve.vector(0, 0, 1),
                    "green" : breve.vector(0, 1, 0),
                    "red" : breve.vector(1, 0, 0)
                    }

def getRgbColor(color):
    """Accepts both textual colors and hexadecimal colors.
    Input example :
        - White
        - blue
        - {"blue" : 234, "green" : 23, "red"}
    """
    
    if color.lower() in knownColors:
        return knownColors[color.lower()]
    color = color[1:]
    r = float(int(color[0:2], 16)) / 255
    g = float(int(color[2:4], 16)) / 255
    b = float(int(color[4:6], 16)) / 255
    return breve.vector(r, g, b)