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
   
def checkDate(recordDict):
    errors = []
    today = date.today()
    #Individuals (Birth, Death)
    for uid in recordDict['ind']:
        birthDate = recordDict['ind'][uid]['birth']
        if(birthDate > today):
            errorString = uid + ": Birthday after current date, " + str(birthDate)
            errors.append(errorString)
        if('death' in recordDict['ind'][uid]):
            deathDate = recordDict['ind'][uid]['death']
            if(deathDate > today):
                errorString = uid + ": Death after current date, " + str(deathDate)
                errors.append(errorString)
    #Fams (Marr, Div)
    for fid in recordDict['fam']:
        marDate = recordDict['fam'][fid]['married']
        if(marDate > today):
            errorString = fid + ": Marriage after current date, " + str(marDate)
            errors.append(errorString)
        if('divorced' in recordDict['fam'][fid]):
            divDate = recordDict['fam'][fid]['divorced']
            if(divDate > today):
                errorString = uid + ": Divorce after current date, " + str(divDate)
                errors.append(errorString)
    
    return errors

def checkBirthBeforeDeath(recordDict):
    errors = []
    for uid in recordDict['ind']:
        if('death' in recordDict['ind'][uid]):
            if(recordDict['ind'][uid]['birth'] > recordDict['ind'][uid]['death']):
                errorString = uid + ": " + recordDict['ind'][uid]['name']
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
    lastnm = []
    indiv = recordDict["ind"]
    for i in indiv.values():
        if i["sex"] == "M":
            nm = i["name"]
            full = nm.split(" ")
            last = full[1]
            someone = "Last Name:{} (Full Name :{})".format(last,nm)           
            lastnm.append(someone)
    return lastnm

def marriageAfter14(recordDict):
    """
    sprint 2 : show the people who are married after 14 years old
    """
    family = recordDict["fam"]
    indivl = recordDict["ind"]
    now = datetime.datetime.now()
    marriage = []
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
                    mar_date = marry.strftime("%Y-%m-%d")
                    name1 = indivl[wf]["name"]
                    name2 = indivl[hd]["name"]
                    each_fam = "marrid date:{}, wife:{},husband:{}".format(mar_date,name1,name2)
                    marriage.append(each_fam)
    return marriage

def checkLessThan150(recordDict):
    errors = []
    for uid in recordDict['ind']:
        if(recordDict['ind'][uid]['age'] > 150):
            errorString = uid + ": " + recordDict['ind'][uid]['name']
            errors.append(errorString)
    return errors
    
def checkBirthBeforeMarriage(recordDict):
    errors = []
    for fid in recordDict['fam']:
        husbID = recordDict['fam'][fid]['husband']
        husbBirth = recordDict['ind'][husbID]['birth']
        wifeID = recordDict['fam'][fid]['wife']
        wifeBirth = recordDict['ind'][wifeID]['birth']
        marrDate = recordDict['fam'][fid]['married']
        if(husbBirth > marrDate):
            errorString = fid + ": Husband " + husbID +  " " + recordDict['ind'][husbID]['name'] + " birth after marriage"
            errors.append(errorString)
        if(wifeBirth > marrDate):
            errorString = fid + ": Wife " + wifeID + " " + recordDict['ind'][wifeID]['name'] + " birth after marriage"
            errors.append(errorString)
    return errors

def checkDivorceBeforeMarriage(recordDict):
    marriage = []
    for familyid in recordDict['fam']:
        if 'divorced' in recordDict['fam'][familyid] and recordDict['fam'][familyid]['divorced'] - recordDict['fam'][familyid]['married'] < datetime.timedelta(days = 0):
            marriage.append('Family {} has a divorce date record {} days before its marriage record'.format(familyid, (recordDict['fam'][familyid]['married'] - recordDict['fam'][familyid]['divorced']).days))
            return marriage

def checkMarriedSiblings(recordDict): 
    entries = []
    for familyid in recordDict['fam']: 
        wifeid = recordDict['fam'][familyid]['wife']  
        husbandid = recordDict['fam'][familyid]['husband']
        if 'childof' in recordDict['ind'][wifeid] and 'childof' in recordDict['ind'][husbandid] and recordDict['ind'][wifeid]['childof'] == recordDict['ind'][husbandid]['childof']:
            entries.append('In family {}, {} and {} are married siblings'.format(familyid, recordDict['ind'][wifeid]['name'],recordDict['ind'][husbandid]['name']))
    return entries

def ParentsNotTooOld(ecordDict):
    """
    Sprint 3 : US 13
    """
    fmly = ecordDict["fam"]
    lst = []
    for i in fmly.values():
        title = i.keys()
        if "wife" and "husband" and "child" in title:
           Hu_date = ecordDict["ind"][i["husband"]]["birth"]
           Wf_date = ecordDict["ind"][i["wife"]]["birth"]
           Cd_date = ecordDict["ind"][i["child"]]["birth"]
           if (Cd_date - Hu_date).days <= 80*365:
               if (Cd_date - Wf_date).days <= 60*365:
                   
                   one_fam= "Husband:{},{};Wife:{},{};Child:{},{}".format(i["husband"],Hu_date,i["wife"],Wf_date,i["child"],Cd_date)
                   lst.append(one_fam)
    return lst




