from datetime import date
from collections import defaultdict
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

siblingDict = defaultdict(list) #Key will be age, value will be list of ID's

uid = "0"
famUID = "0"
dateflag = "0"
today = date.today()

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
    return thisDate

#Main loop
try:
    f = open('Project-Test.ged', "r")
except FileNotFoundError:
    print("'Project-Test.ged' is not existed")
else:    
    nonUniqueIds = []
    for line in f:
        parsed = line.strip().split(' ')
    #Check if INDI or FAM
        if(parsed[1][0] == "@"):
            if parsed[2] in validTags:
                if(parsed[2] != "FAM"): #must be INDI
                    famUID = '0'
                    uid = parsed[1]
                    if(uid in lib["ind"]):
                        nonUniqueIds.append(uid)
                else:
                    uid = '0'
                    famUID = parsed[1]
                    if(famUID in lib["fam"]):
                        nonUniqueIds.append(famUID)

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
                            lib["ind"][uid]["age"] = dateDiff(today, thisDate, "Year")
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
    o.write('Sprint3, US27\n Age: '+str(lib["ind"][id]["age"])+'\n')
    if("death" in lib["ind"][id]):
        o.write('Death: '+str(lib["ind"][id]["death"])+'\n')
    o.write('\n')

for id in sorted(lib["fam"]):
    siblingDict = defaultdict(list)
    o.write(id+'\n')
    wifeId = ""
    husbId = ""
    o.write("Married: " + str(lib['fam'][id]['married'])+'\n')
    if("divorced" in lib['fam'][id]):
        o.write("Divorced: " + str(lib['fam'][id]['divorced'])+'\n')
    if "husband" in lib["fam"][id]:
        husbId = lib["fam"][id]["husband"]
        o.write("Husband: " + husbId + ' ' + lib["ind"][husbId]['name']+'\n')
    if "wife" in lib["fam"][id]:
        wifeId = lib["fam"][id]["wife"]
        o.write("Wife: " + wifeId + ' ' + lib["ind"][wifeId]['name']+'\n')  
    if "child" in lib["fam"][id]:
        o.write("Sprint 3: US28 Order siblings by age\n")
        for child in lib["fam"][id]["child"]:
            childID = child
            childAge = lib["ind"][childID]["age"]
            siblingDict[childAge].append(childID)
        for age in sorted(siblingDict):
            for childID in siblingDict[age]:
                o.write("Child: " + childID + ' ' + lib["ind"][childID]['name']+', age '+str(age)+'\n')
    o.write('\n')

o.write("\nValidation:\n")

o.write("\nUS01 Date after current date errors:\n")
for errorString in GedComValidation.checkDate(lib):
    o.write(errorString+'\n')

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

o.write('\nSprint2: US07 Users Older Than 150 Years Old:\n')
for errorString in GedComValidation.checkLessThan150(lib):
    o.write(errorString+'\n')

o.write('\nSprint2: US02 Birth After Marriage errors:\n')
for errorString in GedComValidation.checkBirthBeforeMarriage(lib):
    o.write(errorString+'\n')


o.write('\nSprint2: US04 Marriage before Divorce families:\n')
for entry in GedComValidation.checkDivorceBeforeMarriage(lib):
    o.write(entry+'\n')

o.write('\nSprint2: US18 Married Siblings:\n')
for entry in GedComValidation.checkMarriedSiblings(lib):
    o.write(entry+'\n')
    
o.write('\nSprint3: US12 Parents not too old:\n')
for age in GedComValidation.ParentsNotTooOld(lib):
  o.write(age+'\n')

o.write('\nSprint3:')
o.write('Non-Unique Ids: ')
o.write(str(nonUniqueIds))

o.write('\n\nSprint3: US20 Aunts and Uncles:\n')
for entry in GedComValidation.auntsAndUncles(lib):
    o.write(entry + '\n')
    
o.write('\nSprint3: US32 All Multiple Births:\n')
for births in GedComValidation.AllMultipleBirths(lib):
    o.write(births + '\n')

