import maya.api.OpenMaya as om
import maya.cmds as cmds
import maya.mel as mel

import re

import mocaphelperutility


def retestlist(strlist,exp,casecheck = False):
    matchlist = []
    pyVersion = mocaphelperutility.getPythonVersion()
    if pyVersion < 3:

        if (type(exp)== unicode ):
            raw_exp = repr(exp)[2:-1]
        elif (type(exp)== str ):
            raw_exp = exp
        else:
            raise Exception("unidentified string format input!")
        
    else:
        raw_exp = exp

    print("convert---"+exp+"---to---"+raw_exp)
    for longname in strlist:
        shortname = longname2shortname(longname)[0]
        print("checking:---exp---"+raw_exp+"---objname---"+shortname)
        if casecheck == False:
            if re.search(raw_exp,shortname,re.I) != None:
                matchlist.append(longname)
                print("succeed")
            else:
                print("failed")
                continue
        else:
            if re.search(raw_exp,shortname) != None:
                matchlist.append(longname)
                print("succeed")
            else:
                print("failed")
                continue
    
    if len(matchlist) == 0:
        print("no obj match expression!")
        return None
    else:
        return matchlist



def expCreateDisplayLayer(exp,name,prefix = "",casecheck = False,childcheck = True,nodetype = "all"):
    selected = mocaphelperutility.getSelectedNodes()
    if childcheck:

        untestlist = mocaphelperutility.getChildNodes(selected,nodetype=nodetype)
    else:
        untestlist = selected
    combinelist = []
    #check for multiple exp exist
    if exp.find(";") != -1 or name.find(";") != -1:
        splitedexplist = exp.split(";")
        splitednamelist = name.split(";")
        if len(splitedexplist) != len(splitednamelist):
            raise Exception("name and exp count not match!")
        else:
            for i in range(len(splitedexplist)):
                combinelist.append([splitedexplist[i],splitednamelist[i]])
    else:
        combinelist =[[exp,name]]

    for combine in combinelist:

        matchlist = retestlist(untestlist,combine[0],casecheck)
        print("matchlist:",matchlist)

        createDisplayLayer(prefix+combine[1],matchlist)
    
    
def createDisplayLayer(name,objlist):
    cmds.createDisplayLayer(n= name,nr = True,empty = True)
    cmds.editDisplayLayerMembers(name,objlist,nr = True)
    


def extractLayerInfo(ui):
    name = cmds.editDisplayLayerGlobals( query=True, cdl=True )
    members =cmds.editDisplayLayerMembers( name, query=True )
    exp = ""
    for member in members:
        noPrefixMember = deleteRigPrefix(member)
        if noPrefixMember[1] == True:
            exp = exp+"."+ noPrefixMember[0] +"|"
        else:
            exp = exp+ noPrefixMember[0] +"|"
    # remove last "|",cause it will match all name str.
    exp = exp[0:-1]
    ui.ui.re_layerNameEdit.setText(name)
    ui.ui.re_expEdit.setText(exp)
    return 

def selMainCtrl():
# main name:
# ".MainExtra2" ".wenchangtai" ".Main_all"
    curves = cmds.ls(type = "dagNode")
    curves = mocaphelperutility.filterCertainTypeInList(curves,type = "nurbsCurve")
    matchlist = []
    a = retestlist(curves,".MainExtra2$|.wenchangtai$|.Main_all$")
    if a != None:
        matchlist += a
    cmds.select(cl = True)
    cmds.select(matchlist)


def longname2shortname(name):
    id = name.rfind("|")
    if id == -1:
        return name,False
    else:
        return name[id+1:],True
    
def deleteRigPrefix(name):
    id = name.rfind(":")
    if id == -1:
        return name,False
    else:
        return name[id:],True
    


def presetfileRebuild(filepath,backupfilepath):
    backupstr = presetFileRead(backupfilepath)
    presetFileWrite(filepath,backupstr)

    

def rawStrBuild(rawstr):
    split = rawstr.split("\n")
    newlist = []
    for i in range(int(len(split)/2)):
        name = split[2*i]
        exp = split[2*i+1]
        newlist.append([name,exp])
    if len(newlist) == 0:
        raise Exception("split list is empty!")
    else:
        return newlist
    
def strAppend(oristr,line1,line2):
    newstr = oristr+"\n"+str(line1)+"\n"+str(line2)
    return newstr


def presetFileRead(filepath):
    file = open(filepath,mode ="r+")
    file.seek(0,0)
    raw = file.read()
    file.close()
    return raw


def presetFileWrite(filepath,str):
    print("writing file:\n"+str)
    file = open(filepath,mode ="w+")
    file.seek(0,0)
    file.write(str)
    file.close()

