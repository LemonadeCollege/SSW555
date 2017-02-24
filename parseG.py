from datetime import date

import GedComValidation

validTags = [ 'INDI','NAME','SEX','BIRT',\
                'DEAT','FAMC','FAMS','FAM',\
                'MARR','HUSB','WIFE','CHIL',\
                'DIV','DATE','HEAD','TRLR',\
                'NOTE','GIVN']

monthDict = {   "JAN":1 , "FEB":2 , "MAR":3 , "APR":4, \
                "MAY":5 , "JUN":6 , "JUL":7 , "AUG":8 ,\
                "SEP":9 , "OCT":10 , "NOV":11 , "DEC":12 \
        }

lib = {
    "ind": {},
    "fam": {}
}

uid = "0"
famUID = "0"
dateflag = "0"
today = date.today()

def parseDateList(dateList):
    year = int(dateList[2])
    month = monthDict[dateList[1]]
    day = int(dateList[0])
    thisDate = date(year, month, day)
    if(thisDate > today):
        print("ERROR: date after current date, reverted to current date")
        return today
    else:
        return thisDate

#Main loop
try:
    f = open('Project-Test.ged', "r")
except FileNotFoundError:
    print("'Project-Test.ged' is not existed")
else:    
    for line in f:
        parsed = line.strip().split(' ')
    
    #Check if INDI or FAM
        if(parsed[1][0] == "@"):
            if parsed[2] in validTags:
                if(parsed[2] != "FAM"): #must be INDI
                    famUID = '0'
                    uid = parsed[1]
                else:
                    uid = '0'
                    famUID = parsed[1]

                    #Check standard format
        else:

        #Individual
            if(uid != "0" and famUID == "0"):
                if(uid not in lib["ind"]): #if UID not in lib
                    lib["ind"][uid] = {} #add it
                if parsed[1] in validTags:
                    if(uid != "0" and parsed[1] == "NAME"):
                        lib["ind"][uid]["name"] = parsed[2] + " " + parsed[3][1:-1]
                    if(uid != "0" and parsed[1] == "GIVN"):
                        lib["ind"][uid]["given"] = parsed[2]
                    elif(uid != "0" and parsed[1] == "SEX"):
                        lib["ind"][uid]["sex"] = parsed[2]
                    elif(uid != "0" and parsed[1] == "BIRT"):
                        dateflag = "1" #flag for the BIRT tag
                    elif(uid != "0" and parsed[1] == "DEAT"):
                        dateflag = "2" #flag for the DEAT tag
                        #now add the date into the structure
                    elif(uid != "0" and parsed[1] == "DATE"):
                        thisDate = parseDateList(parsed[2:]) #Parse date string into date object
                        if(dateflag == "1"):
                            lib["ind"][uid]["birth"] = thisDate
                            dateflag = "0" #clear the flags
                        elif(dateflag == "2"):
                            lib["ind"][uid]["death"] = thisDate
                            dateflag = "0"
                    elif(uid != "0" and parsed[1] == "FAMC"):
                        lib["ind"][uid]["childof"] = parsed[2]
                    elif(uid != "0" and parsed[1] == "FAMS"):
                        lib["ind"][uid]["spouseof"] = parsed[2]
                            #else:
                                # uid = "0" #clear flag

                                #FAM
            elif(uid == "0" and famUID != "0"):
                if(famUID not in lib["fam"]): #if no entry for the family
                    lib["fam"][famUID] = {} #add it
                if parsed[1] in validTags:
                    if(famUID != "0" and parsed[1] == "MARR"):
                        dateflag = "3" #dateflag for MARR tag
                    elif(famUID != "0" and parsed[1] == "DATE" and dateflag == "3"):
                        thisDate = parseDateList(parsed[2:]) #Parse date string into date object
                        lib["fam"][famUID]["married"] = thisDate
                        dateflag = "0"
                    elif(famUID != "0" and parsed[1] == "DIV"):
                        dateflag = "4" #dateflag for DIV tag
                    elif(famUID != "0" and parsed[1] == "DATE" and dateflag == "4"):
                        thisDate = parseDateList(parsed[2:]) #Parse date string into date object
                        lib["fam"][famUID]["divorced"] = thisDate
                        dateflag = "0"
                    elif(famUID != "0" and parsed[1] == "WIFE"):
                        lib["fam"][famUID]["wife"] = parsed[2] #make WIFE key & add UID
                    elif(famUID != "0" and parsed[1] == "HUSB"):
                        lib["fam"][famUID]["husband"] = parsed[2] #make HUSB key & add UID
                    elif(famUID != "0" and parsed[1] == "CHIL"):
                        if "child" not in lib["fam"][famUID]:
                            lib["fam"][famUID]["child"] = [parsed[2]]
                        else:
                            lib["fam"][famUID]["child"].append(parsed[2]) #make CHIL key & add UID
                    #else:
                    # famUID = "0"


f.close()

for id in sorted(lib["ind"]):
    print (lib["ind"][id]["birth"])

for id in sorted(lib["ind"]):
    print (id, lib["ind"][id]["name"])

for id in sorted(lib["fam"]):
    print(id)
    wifeId = ""
    husbId = ""
    if "husband" in lib["fam"][id]:
        husbId = lib["fam"][id]["husband"]
        print ("Husband: ", husbId, lib["ind"][husbId]['name'])
    if "wife" in lib["fam"][id]:
        wifeId = lib["fam"][id]["wife"]
        print ("Wife: ", wifeId, lib["ind"][wifeId]['name'])
    if "child" in lib["fam"][id]:
        for child in lib["fam"][id]["child"]:
            childId = child
            print ("Child: ", childId, lib["ind"][childId]['name'])

print("Errors:")
print(GedComValidation.checkBirthBeforeDeath(lib))


print('Living, Unmarried, and Over Thirty:')
for IndID in GedComValidation.checkLivingSingle(lib):
    print(lib['ind'][IndID]['name'])


print('large age differences: ')
for famId in GedComValidation.checklargeAgeDifferences(lib):
    wifeId = lib['fam'][famId]['wife']
    husbandId = lib['fam'][famId]['husband']
    print (wifeId + ': ' + lib['ind'][wifeId]['name'])
    print (husbandId + ': ' + lib['ind'][husbandId]['name'])








