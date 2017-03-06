from datetime import date
import datetime
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
dateErrors = []

def dateDiff(d1, d2, method):
    if(method == "Day"):
        return abs((d1 - d2).days)
    elif(method == "Month"):
        return int(abs((d1 - d2).days / 30.4))
    elif(method == "Year"):
        return int(abs((d1 - d2).days / 365.25))
    else:
        print("Incorrect usage of dateDiff: arg3 should be Day, Month, or Year")
        return 0

def parseDateList(dateList, ):
    year = int(dateList[2])
    month = monthDict[dateList[1]]
    day = int(dateList[0])
    thisDate = date(year, month, day)
    if(thisDate > today):
        dateErrors.append(str(thisDate))
        return thisDate
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
o = open('./out.txt', 'w')

for id in sorted(lib["ind"]):
    o.write(id + ' ' + lib["ind"][id]["name"]+'\n')
    o.write('Gender: '+lib["ind"][id]["sex"]+'\n')
    o.write('Birthday: '+str(lib["ind"][id]["birth"])+'\n')
    o.write('Age: '+str(dateDiff(today, lib["ind"][id]["birth"], "Year"))+'\n')
    if("death" in lib["ind"][id]):
        o.write('Death: '+str(lib["ind"][id]["death"])+'\n')
    o.write('\n')

for id in sorted(lib["fam"]):
    o.write(id+'\n')
    wifeId = ""
    husbId = ""
    if "husband" in lib["fam"][id]:
        husbId = lib["fam"][id]["husband"]
        o.write("Husband: " + husbId + ' ' + lib["ind"][husbId]['name']+'\n')
    if "wife" in lib["fam"][id]:
        wifeId = lib["fam"][id]["wife"]
        o.write("Wife: " + wifeId + ' ' + lib["ind"][wifeId]['name']+'\n')  
    if "child" in lib["fam"][id]:
        for child in lib["fam"][id]["child"]:
            childId = child
            o.write("Child: " + childId + ' ' + lib["ind"][childId]['name']+'\n')

o.write("\nValidation:\n")

o.write("\nUS01 Date after current date errors:\n")
for error in dateErrors:
    o.write(error+'\n')

o.write("\nUS03 Birth before Death errors:\n")
for errorString in GedComValidation.checkBirthBeforeDeath(lib):
    o.write(errorString+'\n')

o.write('\nUS31 Living, Unmarried, and Over Thirty:\n')
for IndID in GedComValidation.checkLivingSingle(lib):
    o.write(lib['ind'][IndID]['name']+'\n')


o.write('\nUS34 Large age differences: \n')
for famId in GedComValidation.checklargeAgeDifferences(lib):
    wifeId = lib['fam'][famId]['wife']
    husbandId = lib['fam'][famId]['husband']
    o.write (wifeId + ': ' + lib['ind'][wifeId]['name']+' and ')
    o.write (husbandId + ': ' + lib['ind'][husbandId]['name']+'\n')

    
o.write('\nUS29 All deceased people: \n')
for IndID in GedComValidation.listDeadPeople(lib): 
    o.write("Name:" + IndID +'\n')
    
o.write('\nUS35 List recent births: \n')
for IndID in GedComValidation.listRecentBirth(lib):
    o.write('Name :' + IndID + '\n') 


o.write('\nsprint2: US10 Marriage after 14:\n')
for info in GedComValidation.marriageAfter14(lib):
    o.write(info + '\n')

o.write('\nsprint2: US16 Male last names:\n')
for info in GedComValidation.maleLastName(lib):
    o.write(info + '\n')

