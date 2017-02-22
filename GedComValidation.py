#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 20:06:12 2017

@author: josephmiles
"""
from datetime import date


def checkLivingSingle(recordDict):
    return [i for i in recordDict['ind'] if 'death' not in recordDict['ind'][i] and 'spouseof' not in recordDict['ind'][i] and date.today().year - recordDict['ind'][i]['birth'].year > 30]
   
def checkBirthBeforeDeath(recordDict):
    errors = []
    for uid in recordDict['ind']:
        if('death' in recordDict['ind'][uid]):
            if(recordDict['ind'][uid]['birth'] > recordDict['ind'][uid]['death']):
                errorString = "User " + uid + " birth before death"
                errors.append(errorString)
    return errors

def checklargeAgeDifferences(recordDict):
    familyIds = []
    for familyId in recordDict['fam']:
        husbandId = recordDict['fam'][familyId]['husband']
        wifeId = recordDict['fam'][familyId]['wife']
        today = date.today().year
        husbandAge = today - recordDict['ind'][husbandId]['birth'].year
        wifeAge = today - recordDict['ind'][wifeId]['birth'].year
        if  husbandAge > 2 * wifeAge or husbandAge * 2 < wifeAge:
            familyIds.append(familyId)
    return familyIds