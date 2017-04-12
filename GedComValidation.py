#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 20:06:12 2017

@author: josephmiles
"""
from datetime import date
import datetime
import collections


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

                           
def ParentsNotTooOld(recordDict):
    """
    Sprint 3 : Parents not too old
    """
    fmly = recordDict["fam"]
    lst = []
    for i in fmly.values():   
        title = i.keys()
        if "wife" and "husband" and "child" in title:
            Hu_date = recordDict["ind"][i["husband"]]["birth"]
            Wf_date = recordDict["ind"][i["wife"]]["birth"]
            for j in i["child"]:                           
                Cd_date = recordDict["ind"][j]["birth"]
                if (Cd_date - Hu_date).days <= 80*365:
                    if (Cd_date - Wf_date).days <= 60*365:

                        each_fam = "Husband({}:{});Wife({}:{});Child({}:{})".format(i["husband"],Hu_date,i["wife"],Wf_date,j,Cd_date)
                        lst.append(each_fam)
    return lst

def auntsAndUncles(recordDict):
    entries = []
    for familyid in recordDict['fam']: 
        wifeid = recordDict['fam'][familyid]['wife']  
        husbandid = recordDict['fam'][familyid]['husband']
        if 'childof' not in recordDict['ind'][wifeid] or 'childof' not in recordDict['ind'][husbandid]:
            continue
        fam1ID = recordDict['ind'][wifeid]['childof'] 
        #print(fam1ID)
        
        fam2ID = recordDict['ind'][husbandid]['childof'] 
        #print(fam2ID)
        wifeParentNiece = recordDict['fam'][fam1ID]['wife']
        husbandParentNiece = recordDict['fam'][fam1ID]['husband']
        wifeParentNephew = recordDict['fam'][fam2ID]['wife']
        husbandParentNephew = recordDict['fam'][fam2ID]['husband']
        #print(wifeParentNiece)
        #print(husbandParentNiece)
        
        #print(wifeParentNephew)
        #print(husbandParentNephew)
        if 'childof' in recordDict['ind'][wifeParentNiece] or 'childof' in recordDict['ind'][husbandParentNiece]:
            if recordDict['ind'][wifeParentNiece]['childof'] == fam2ID or recordDict['ind'][husbandParentNiece]['childof'] == fam2ID:
                entries.append('In family {}, {} and {} are married uncle and niece.'.format(familyid, recordDict['ind'][husbandid]['name'], recordDict['ind'][wifeid]['name']))
        if 'childof' in recordDict['ind'][wifeParentNephew] or 'childof' in recordDict['ind'][husbandParentNephew]:   
            if recordDict['ind'][wifeParentNephew]['childof'] == fam1ID or recordDict['ind'][husbandParentNephew]['childof'] == fam1ID:
                entries.append('In family {}, {} and {} are married aunt and nephew.'.format(famid, recordDict['ind'][wifeid]['name'], recordDict['ind'][husbandid]['name']))
    return entries   

def AllMultipleBirths(recordDict):
    """
    sprint3 :All Multiple Births
    """
    fam = recordDict["fam"]
    births = []
    l1 = []
    
    for i in fam.values():
        if "child" in i.keys():
            if len(i["child"]) > 1 :
                
                for a in i["child"]:
                    for b in i["child"]:
                        if a != b:
                            a_date = recordDict["ind"][a]["birth"]
                            b_date = recordDict["ind"][b]["birth"]
                            if a_date == b_date:
                                births.append(a)
                                births.append(b)                              
                                for j in births:
                                    dt = recordDict["ind"][j]["birth"]
                                    nm = recordDict["ind"][j]["name"]
                                    cd = "{}: Name {}, Birthday {}".format(j,nm,dt)
                                    l1.append(cd)
    l2 = set(l1)
    return l2
                    
def BirthBfDeathOfParents(recordDict):
    """
    Sprint4 : US09 Birth before death of parents
    """
    a = recordDict['fam']
    lst_record = []
    for i in a.values():
        if 'child' in i.keys():
            fa = i['husband']
            ma = i['wife']
            cds = i['child']      
            for cd in cds:
                if 'death' in recordDict['ind'][fa].keys():
                    fa_dd = recordDict['ind'][fa]['death'] - datetime.timedelta(days = 270)
                    if 'death' in recordDict['ind'][ma].keys():
                         ma_dd = recordDict['ind'][ma]['death']
                         cd_bt = recordDict['ind'][cd]['birth']
                         if cd_bt > ma_dd or cd_bt > fa_dd:
                             record ="checking results:{}'s birthday {} is after mather {}'s deathday {} or 9 months before father {}'s deathday {}".format(cd,cd_bt,ma,ma_dd,fa,fa_dd)                             
                             lst_record.append(record)
    return lst_record

  
def UniqueFirstNameInFamily(recordDict):
    """
    sprint4: US25 Unique first names in families
    """
    mult = []
    fam = recordDict['fam']
    for i in fam.values():
        info1 = []
        if 'child' in i.keys():
            cd = i['child']
            if len(cd) > 1:
                for j in cd:
                    fname = recordDict['ind'][j]['given']
                    fbirth = recordDict['ind'][j]['birth']
                    comb = "{}:{}".format(fname,fbirth)
                    info1.append(comb)
        info2 = set(info1)
        for a in info2:
            info1.remove(a)
        mult.extend(info1)
    if len(mult) == 0:
        return ["there are not two children with same first name and birthday"]
    else:
        return mult

def ListRecentDeath(recordDict):
    dth = []
    today = datetime.datetime.now()
    before = today - datetime.timedelta(days = 30)
    ago_day = before.strftime("%Y-%m-%d")
    indival = recordDict["ind"]
    for info2 in indival.values():
        if 'death' in info2:
            c = str(info2['death'])
            indid = datetime.datetime.strptime(c,"%Y-%m-%d")
            df = datetime.datetime.strptime(ago_day,"%Y-%m-%d")
            s = (indid - df).days
            if s >= 0 and info2['death'] < date.today():
                nm2 = info2['name'] + " Death: " + str(info2['death'])
                dth.append(nm2)
    return dth