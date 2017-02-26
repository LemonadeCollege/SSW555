from datetime import date
import datetime


validTags = [ 'INDI','NAME','BIRT','DATE']

monthDict = {   "JAN":1 , "FEB":2 , "MAR":3 , "APR":4, \
                "MAY":5 , "JUN":6 , "JUL":7 , "AUG":8 ,\
                "SEP":9 , "OCT":10 , "NOV":11 , "DEC":12 \
            }

def parseDateList(dateList):
    year = int(dateList[2])
    month = monthDict[dateList[1]]
    day = int(dateList[0])
    return date(year, month, day)

#Main loop
def bfBirth():
    lib = {}
    uid = "0"
    dateflag = "0"
    lst = []
    f = open('Project-Test.ged', "r")    
    for line in f:
        parsed = line.strip().split(' ')
    
    #Check if INDI or FAM
        if(parsed[1][0] == "@"):
            if parsed[2] in validTags:
                if(parsed[2] == "INDI"): #must be INDI
                    uid = parsed[1]
                    #Check standard format
        else:

        #Individual
            if(uid != "0"):
                if(uid not in lib): #if UID not in lib
                    lib[uid] = {} #add it
                if parsed[1] in validTags:
                    if(uid != "0" and parsed[1] == "NAME"):
                        lib[uid]["name"] = parsed[2] + " " + parsed[3][1:-1]
                    elif(uid != "0" and parsed[1] == "BIRT"):
                        dateflag = "1" #flag for the BIRT tag
                    elif(uid != "0" and parsed[1] == "DATE"):
                        thisDate = parseDateList(parsed[2:]) #Parse date string into date object
                        if(dateflag == "1"):
                            lib[uid]["birth"] = thisDate
                            dateflag = "0" #clear the flags
                            
    now = datetime.datetime.now()
    before = now - datetime.timedelta(days = 30)
    ago_day = before.strftime("%Y-%m-%d")
    indival = lib
    for info in indival.values():
        if 'birth' in info:
            c = str(info['birth'])
            indiv = datetime.datetime.strptime(c,"%Y-%m-%d")
            bf = datetime.datetime.strptime(ago_day,"%Y-%m-%d")
            s = (indiv - bf).days
            if s >= 0:
                #print("the date of 30 days ago is {}".format(ago_day))
                #print("{} is born in {}".format(info['name'],info['birth']))
                lst.append(info['name'])
    return lst
