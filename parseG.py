validTags = [ 'INDI','NAME','SEX','BIRT',\
                'DEAT','FAMC','FAMS','FAM',\
                'MARR','HUSB','WIFE','CHIL',\
                'DIV','DATE','HEAD','TRLR',\
                'NOTE','GIVN','SURN','_MARNM']

skipTags = [ 'GIVN','SURN','_MARNM']

lib = {
    "ind": {},
    "fam": {}
}

uid = "0"
famUID = "0"

dateflag = "0"

f = open('Project-Test.ged', "r")

for line in f:
    parsed = line.strip().split(' ')
    
    #Check if INDI or FAM
    if(parsed[1][0] == "@"):
        if parsed[2] in validTags:
            if(parsed[2] != "FAM"): #must be INDI
                uid = parsed[1]
            else:
                famUID = parsed[1]

    #Check standard format
    else:

        #Individual
        if(uid != "0" and famUID == "0"):
            if(not(lib["ind"].has_key(uid))): #if UID not in lib
                lib["ind"][uid] = {} #add it
            if parsed[1] in validTags:
                if(uid != "0" and parsed[1] == "NAME"):
                    lib["ind"][uid]["name"] = parsed[2] + " " + parsed[3][1:-1]
                if(uid != "0" and parsed[1] in skipTags):
                    continue
                elif(uid != "0" and parsed[1] == "SEX"):
                    lib["ind"][uid]["sex"] = parsed[2]
                elif(uid != "0" and parsed[1] == "BIRT"):
                    dateflag = "1" #flag for the BIRT tag
                elif(uid != "0" and parsed[1] == "DEAT"):
                    dateflag = "2" #flag for the DEAT tag
                #now add the date as an array into the structure
                elif(uid != "0" and parsed[1] == "DATE"):
                    if(dateflag == "1"):
                        lib["ind"][uid]["birth"] = parsed[2:]
                        dateflag = "0" #clear the flags
                    elif(dateflag == "2"):
                        lib["ind"][uid]["death"] = parsed[2:]
                        dateflag = "0"
                elif(uid != "0" and parsed[1] == "FAMC"):
                    lib["ind"][uid]["childof"] = parsed[2]
                elif(uid != "0" and parsed[1] == "FAMS"):
                    lib["ind"][uid]["spouseof"] = parsed[2]
            else:
                uid = "0" #clear flag

        #FAM
        elif(uid == "0" and famUID != "0"):
            if(not(lib["fam"].has_key(famUID))): #if no entry for the family
                lib["fam"][famUID] = {} #add it
            if parsed[1] in validTags:
                if(famUID != "0" and parsed[1] == "MARR"):
                    dateflag = "3" #dateflag for MARR tag
                elif(famUID != "0" and parsed[1] == "DATE" and dateflag == "3"):
                    lib["fam"][famUID]["married"] = parsed[2:]
                    dateflag = "0"
                elif(famUID != "0" and parsed[1] == "DIV"):
                    dateflag = "4" #dateflag for DIV tag
                elif(famUID != "0" and parsed[1] == "DATE" and dateflag == "4"):
                    lib["fam"][famUID]["divorced"] = parsed[2:]
                    dateflag = "0"
                elif(famUID != "0" and parsed[1] == "WIFE"):
                    lib["fam"][famUID]["wife"] = parsed[2] #make WIFE key & add UID
                elif(famUID != "0" and parsed[1] == "HUSB"):
                    lib["fam"][famUID]["husband"] = parsed[2] #make HUSB key & add UID
                elif(famUID != "0" and parsed[1] == "CHIL"):
                    if(not(lib["fam"][famUID].has_key("child"))):
                        lib["fam"][famUID]["child"] = [parsed[2]]
                    else:
                        lib["fam"][famUID]["child"].append(parsed[2]) #make CHIL key & add UID
            else:
                famUID = "0"


f.close()

for id in sorted(lib["ind"]):
    print lib["ind"][id]
