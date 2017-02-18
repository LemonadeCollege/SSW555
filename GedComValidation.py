#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 20:06:12 2017

@author: josephmiles
"""



def checkLivingSingle(recordDict):
    return [i for i in recordDict['ind'] if 'death' not in recordDict['ind'][i] and 'spouseof' not in recordDict['ind'][i] and 2017 - recordDict['ind'][i]['birth'].year > 30]
   
            
