import maya.api.OpenMaya as om
import maya.cmds as cmds
import maya.mel as mel

import os


def selectNodes(nodelist,visible = False):
    cmds.select(cl=True)
    if visible == True:
        cmds.select(nodelist,vis = True)
    else:
        cmds.select(nodelist)

def addSelectNodes(nodelist):
    for node in nodelist:
        cmds.select(node,add = True)

def orderSelectNodes(nodelist):
    cmds.select(cl=True)
    for node in nodelist:
        cmds.select(node,add = True)

def getSelectedNodes(nodetype = "all",longname = True):
    selectednodes = cmds.ls(selection = True,type = "dagNode",long = longname)
    if nodetype != "all":
        selectednodes = filterCertainTypeInList(selectednodes,nodetype)
    return selectednodes

def getChildNodes(parents,nodetype = "all",combine = True):
    list = []

    for parent in parents:
        childlist = cmds.listRelatives(parent, ad=True, type = "transform",fullPath = True)

        if childlist == None:
            continue
        else:
            if nodetype == "all":
                list += childlist

            else:
                list += filterCertainTypeInList(childlist,nodetype)
        
    if list != None:
        if combine == True:
            return list+parents
        else:
            return list
    else:
        raise Exception("error when getting child")

def filterCertainTypeInList(list,type = "nurbsCurve"):
    matchlist = []
    for node in list:
        if getShapeType(node) == type:
            matchlist.append(node)
        
    return matchlist

def getShapeType( node = "" ):
    shape = cmds.listRelatives(node,shapes = True,fullPath = True)
    if shape != None:
        shape = shape[0]
        return cmds.nodeType(shape)
    else:
        return None


def objExist(obj):
    if len(cmds.ls(obj)) == 0:
        return False
    else:
        return True
    
def getCurrentFrame():
    return cmds.currentTime(q = True)

def getTimeRange(local = False):
    #local means time slider range in maya time line
    if local == True:
        return cmds.playbackOptions(q = True,min = True),cmds.playbackOptions(q = True,max = True)
    else:
        return cmds.playbackOptions(q = True,ast = True),cmds.playbackOptions(q = True,aet = True)
    

def getWorldPos(obj):
    return cmds.xform(obj,q = True,ws = True,t = True)

def getWorldRot(obj):
    return cmds.xform(obj,q = True,ws = True,ro = True)

def getRotOrder(obj):
    return cmds.xform(obj,q = True,roo = True)

def setWorldPos(obj,cd = (0.0,0.0,0.0)):
    cmds.xform(obj,ws = True,t = cd)

def setWorldRot(obj,rot = (0.0,0.0,0.0),targetRotOrder = "xyz"):
    originOrder = cmds.xform(obj,q = True,roo = True)
    if originOrder == targetRotOrder:
        cmds.xform(obj,ws = True,ro = rot)
    else:
        if targetRotOrder in ['xyz', 'yzx','zxy','xzy','yxz','zyx']:
            cmds.xform(obj,ws = True,ro = rot,roo = targetRotOrder)
            cmds.xform(obj,ws = True,roo = originOrder)
        else:
            raise Exception("rot order does not exist.")

def cutKey(objlist,mintime,maxtime,insertside = False):
    if insertside:
        cmds.cutKey(objlist,t =(mintime,maxtime),cl = True,option = "curve")
    else:
        cmds.cutKey(objlist,t =(mintime,maxtime),cl = True)

def autoKetTangent(objs,mintime,maxtime):
    cmds.keyTangent(objs,e = True,itt="auto", ott="auto", t=(mintime,maxtime))


def deleteObj(obj):
    cmds.delete(obj)

def unicodeToStr(str):
    return repr(str)[2:-1]

def getDir():
    dir = os.path.dirname(__file__)
    return dir