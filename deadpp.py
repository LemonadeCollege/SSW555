#!/usr/bin/env python    
# -*- coding: utf-8 -*-    
# Filename: deadpp.py

"""
"this is for test"

def deadpp(nm):
    pass
    
"""
def deadpp():
    """
    this function is to find out all deceased people in the file.
    """
    validTags = [ 'INDI','NAME','DEAT','DATE']
    lib = {}
    uid = "0"
    datefg = "0"
    lst = []
    try:
        f = open('Project-Test.ged', "r") 
    except FileNotFoundError:
        print("'Project-Test.ged' is not existed ")
    else:
        for line in f:
            info = line.strip().split(' ')
            #Check if INDI or FAM
            if(info[1][0] == "@"):
                if info[2] in validTags:
                    if(info[2] == "INDI"): 
                        uid = info[1]

            else:
                if(uid != "0" ):
                    if(uid not in lib): #if UID not in lib
                        lib[uid] = {} #add it
                    if info[1] in validTags:
                        if(uid != "0" and info[1] == "NAME"):
                            lib[uid]["name"] = info[2] + " " + info[3][1:-1]
                        elif(uid != "0" and info[1] == "DEAT"):
                            datefg = "1" #flag for the DEAT tag
                        elif(uid != "0" and info[1] == "DATE"):
                            Ddate = info[2:]
                            Str_date = ' '.join(Ddate)
                        if(datefg == "1"):
                            lib[uid]["death"] = Str_date

    for i in lib.values():
        if "death" in i:            
            #print("{} is dead in {}".format(i['name'],i['death']))  
            str_name = i["name"]
            lst.append(str_name) 
            
    return lst

