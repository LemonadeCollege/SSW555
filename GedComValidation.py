#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 20:06:12 2017

@author: josephmiles
"""
from datetime import date
import datetime


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

def listDeadPeople(recordDict):
    """
    list all deceased individuals in a GEDCOM file
    """
    deadpp = []
    indiv = recordDict['ind']
    for info in indiv.values():
        if 'death' in info:
            nm1 = info['name']
            deadpp.append(nm1)
    return deadpp

def listRecentBirth(recordDict):
    """
    list all people who are born in last 30 days
    """
    bth = []
    now = datetime.datetime.now()
    before = now - datetime.timedelta(days = 30)
    ago_day = before.strftime("%Y-%m-%d")
    indival = recordDict["ind"]
    for info2 in indival.values():
        if 'birth' in info2:
            c = str(info2['birth'])
            indid = datetime.datetime.strptime(c,"%Y-%m-%d")
            bf = datetime.datetime.strptime(ago_day,"%Y-%m-%d")
            s = (indid - bf).days
            if s >= 0:
                nm2 = info2['name']
                bth.append(nm2)
    return bth

def maleLastName(recordDict):
    """
    Sprint 2 :show all men's last name
    """
    indiv = recordDict["ind"]
    for i in indiv.values():
        if i["sex"] == "M":
            nm = i["name"]
            full = nm.split(" ")
            last = full[1]
            return ("Last Name:{} (Full Name :{})".format(last,nm))
        
def marriageAfter14(recordDict):
    """
    sprint 2 : show the people who are married after 14 years old
    """
    family = recordDict["fam"]
    indivl = recordDict["ind"]
    now = datetime.datetime.now()

    for info in family.values():
        if "married" in info:
            marry = info["married"]
            wf = info["wife"]
            hd = info["husband"]
            wf_birth = indivl[wf]["birth"]
            hd_birth = indivl[hd]["birth"]                
            h1 = hd_birth.strftime("%Y-%m-%d")
            h2 = datetime.datetime.strptime(h1,"%Y-%m-%d")
            w1 = wf_birth.strftime("%Y-%m-%d")
            w2 = datetime.datetime.strptime(w1,"%Y-%m-%d")
            dif_hd = int((now - h2).days/365.25)
            dif_wf = int((now - w2).days/365.25)  
            
            if dif_hd > 14 :
                if dif_wf > 14:                
                    return ("marrid date:{}, wife:{},husband:{}".format(marry,indivl[wf]["name"],indivl[hd]["name"]))
