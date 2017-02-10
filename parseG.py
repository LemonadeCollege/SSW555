validTags = [ 'INDI','NAME','SEX','BIRT',\
                'DEAT','FAMC','FAMS','FAM',\
                'MARR','HUSB','WIFE','CHIL',\
                'DIV','DATE','HEAD','TRLR',\
                'NOTE','GIVN','SURN','_MAR']

def parse_and_print(line):
    lineL = line.split()
    level = lineL[0]
    if level == "0":
        tag = lineL[-1]
    else:
        tag = lineL[1]
    if tag not in validTags:
        tag = "Invalid Tag"
    print("Line: %sLevel: %s \nTag: %s \n\n" % (line, level, tag))
    
#main
f = open('Project-Test.ged', "r")
line = f.readline()

while line:
    parse_and_print(line)
    line = f.readline()
f.close()
