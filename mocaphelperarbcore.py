# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel

import mocaphelperutility
import math

def createLoc(strname,cd = (0,0,0),rot = (0,0,0),roo = "xyz"):
    locname = cmds.spaceLocator(name = strname)
    mocaphelperutility.setWorldPos(locname,cd)
    mocaphelperutility.setWorldRot(locname,rot,roo)
    return locname

def reposition(objA,objB):
    tempp = mocaphelperutility.getWorldPos(objB)
    tempr = mocaphelperutility.getWorldRot(objB)
    temproo = mocaphelperutility.getRotOrder(objB)
    mocaphelperutility.setWorldPos(objA,tempp)
    mocaphelperutility.setWorldRot(objA,tempr,temproo)


def checkConstraint(obj):
    parent = cmds.parentConstraint(obj, targetList = True ,q = True ) 
    point = cmds.pointConstraint(obj, targetList = True ,q = True ) 
    orient = cmds.orientConstraint(obj, targetList = True ,q = True ) 
    if parent == None and point == None and orient == None:
        return False
    else:
        conslist = [parent,point,orient]
        return conslist
    
def deleteAllConstraint(obj):
    cmds.delete(obj,cn=True)

def createPointConstraint(ctrlobj,targetobj,maintainoffset = False):
    name = cmds.pointConstraint(ctrlobj,targetobj,mo = maintainoffset)
    return name

def createOrientConstraint(ctrlobj,targetobj,maintainoffset = False):
    name = cmds.orientConstraint(ctrlobj,targetobj,mo = maintainoffset)
    return name

def createParentConstraint(ctrlobj,targetobj,maintainoffset = False):
    name = cmds.parentConstraint(ctrlobj,targetobj,mo = maintainoffset)
    return name
'''
def deletePointConstraint(ctrlobj,targetobj):
    cmds.pointConstraint(ctrlobj,targetobj,remove = True)

def deleteParentConstraint(ctrlobj,targetobj):
    cmds.parentConstraint(ctrlobj,targetobj,remove = True)

def deleteOrientConstraint(ctrlobj,targetobj):
    cmds.orientConstraint(ctrlobj,targetobj,remove = True)
'''
def bake(objs,mintime,maxtime,type = "all"):
    # if smartbake == True:
    if type == "all":
        cmds.bakeResults(objs,t =(mintime,maxtime),simulation = True)
    else:
        if type == "parent":
            atb = ["tx","ty","tz","sx","sy","sz","rx","ry","rz"]

        elif type == "point":
            atb = ["tx","ty","tz"]

        elif type == "orient":
            atb = ["rx","ry","rz"]

        elif type == "onlyscale":
            atb = ["sx","sy","sz"]

        else:
            raise Exception("bake error:type unidentified:",type)
        cmds.bakeResults(objs,t =(mintime,maxtime),at = atb)

def smartbake(objs,mintime,maxtime,type = "all"):
    if type == "all":
        cmds.bakeResults(objs,t =(mintime,maxtime),smart = True,simulation = True)
    else:
        if type == "parent":
            atb = ["tx","ty","tz","sx","sy","sz","rx","ry","rz"]

        elif type == "point":
            atb = ["tx","ty","tz"]

        elif type == "orient":
            atb = ["rx","ry","rz"]

        elif type == "onlyscale":
            atb = ["sx","sy","sz"]

        else:
            raise Exception("bake error:type unidentified")
        cmds.bakeResults(objs,t =(mintime,maxtime),smart = True,at = atb)


def deleteInrange(objs,start,end):
    if cmds.keyframe(objs,q = True) == None :
        raise Exception("ref has no keys!")
    else:
        mocaphelperutility.cutKey(objs,start+0.01,end-0.01)
        # mocaphelperutility.autoKetTangent(objs,start,start)
        # mocaphelperutility.autoKetTangent(objs,end,end)

def deleteOutrange(objs,start,end):
    if cmds.keyframe(objs,q = True) == None :
        raise Exception("ref has no keys!")
    
    framelist = set(cmds.keyframe(objs,q = True))
    minframe = min(framelist)
    maxframe = max(framelist)
    if minframe < start:
        mocaphelperutility.cutKey(objs,minframe,start-0.01)
        # mocaphelperutility.autoKetTangent(objs,start,start)
    if maxframe > end:
        mocaphelperutility.cutKey(objs,end+0.01,maxframe)
        # mocaphelperutility.autoKetTangent(objs,end,end)


def offsetFrame(objs,offset):
    cmds.keyframe(objs,e = True,tc = float(offset),o = "over",relative = True)

def stickyDelete(ui):
    objs = mocaphelperutility.getSelectedNodes()
    fromframe = eval(ui.ui.arb_fromEdit.text())
    curframe = mocaphelperutility.getCurrentFrame()
    if fromframe != curframe:
        mocaphelperutility.cutKey(objs,fromframe,curframe,True)
        mocaphelperutility.autoKetTangent(objs,fromframe,curframe)
        ui.ui.arb_fromEdit.setText(str(curframe))
        ui.ui.arb_toEdit.setText(str(curframe))
    else:
        raise Exception("from == curframe")
    

def bakeAtoB(A,B,start,end,type,maintainoffset = False,smart = False):
    print("type == ",type)
    if type == "parent" or type == "all":
        createParentConstraint(A,B,maintainoffset)
    elif type == "point":
        createPointConstraint(A,B,maintainoffset)
    elif type == "orient":
        createOrientConstraint(A,B,maintainoffset)
    elif type == "onlyscale":
        createParentConstraint(A,B,maintainoffset)

    if smart:
        smartbake(B,start,end,type)
    else:
        bake(B,start,end,type)
        
    deleteAllConstraint(B)


def pinCurPos(objs,mintime,maxtime):
    min = mintime
    max = maxtime
    if min > max:
            min = maxtime
            max = mintime
    if min == max:
        raise Exception("min == max.")
    
    
    cmds.undoInfo(openChunk=True)
    try:
        cdlist = []
        # cmds.currentTime(min)
        for obj in objs:

            pos = mocaphelperutility.getWorldPos(obj)
            rot = mocaphelperutility.getWorldRot(obj)
            cdlist.append([pos,rot])
        for i in range(int(math.floor(min)),int(math.ceil(max)+1)):

            cmds.currentTime(float(i))
            cmds.setKeyframe(objs,at = ["tx","ty","tz","rx","ry","rz"])
            for i in range(len(objs)):
                pos = cdlist[i][0]
                rot = cdlist[i][1]
                cmds.xform(objs[i],ws = True,translation = pos,rotation = rot)
    finally:
        cmds.undoInfo(closeChunk=True)

def pinParentPos(objs,mintime,maxtime):

    leng = len(objs)
    if leng <= 1:
        raise Exception("not enough obj selected,at least 2.")
    min = mintime
    max = maxtime
    if min > max:
            min = maxtime
            max = mintime
    if min == max:
        raise Exception("min == max.")
    
    cmds.undoInfo(openChunk=True)

    try:
        cmds.currentTime(min)
        consobj = objs[:-1]
        beconsobj = objs[-1]

        pos = mocaphelperutility.getWorldPos(beconsobj)
        rot = mocaphelperutility.getWorldRot(beconsobj)
        roo = mocaphelperutility.getRotOrder(beconsobj)
        loc = createLoc("mocaphelper_arb_pinparent_temp_loc",pos,rot,roo)[0]
        createParentConstraint(consobj,loc,True)
        bake(loc,min,max,type="parent")



        for i in range(int(math.floor(min)),int(math.ceil(max)+1)):

            cmds.currentTime(float(i))
            cmds.setKeyframe(beconsobj,at = ["tx","ty","tz","rx","ry","rz"])
            reposition(beconsobj,loc)

        mocaphelperutility.deleteObj(loc)
        mocaphelperutility.selectNodes(beconsobj)
    finally:
        cmds.undoInfo(closeChunk=True)