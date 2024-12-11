import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as omani
import maya.cmds as cmds

import maya.mel as mel
import math

import mocaphelperutility


# selectionList = om.MGlobal.getActiveSelectionList()
# iterator = om.MItSelectionList( selectionList, om.MFn.kDagNode )
methodShortFlagName = "-m"
methodLongFlagName = "-method"
iterShortFlagName = "-i"
iterLongFlagName = "-iteration"
intensityShortFlagName = "-in"
intensityLongFlagName = "-intensity"
seltypeShortFlagName = "-sel"
seltypeLongFlagName = "-selecttype"
useTimeShortFlagName = "-u"
useTimeLongFlagName = "-usetime"
timeUnitShortFlagName = "-tu"
timeUnitLongFlagName = "-timeunit"



def syntaxCreator():

    syntax = om.MSyntax()
    
    syntax.addFlag( methodShortFlagName, methodLongFlagName, om.MSyntax.kString )
    syntax.addFlag( iterShortFlagName, iterLongFlagName, om.MSyntax.kLong )
    syntax.addFlag( intensityShortFlagName, intensityLongFlagName, om.MSyntax.kDouble )
    syntax.addFlag( seltypeShortFlagName, seltypeLongFlagName, om.MSyntax.kLong )
    syntax.addFlag( useTimeShortFlagName, useTimeLongFlagName, om.MSyntax.kBoolean )
    syntax.addFlag( timeUnitShortFlagName, timeUnitLongFlagName, om.MSyntax.kDouble )
    

        
    return syntax
    

class SmoothAnimCurve(om.MPxCommand):
    kPluginCmdName = "moCapHelper_smoothAniCurve"
    method = 0
    iteration = 1
    intensity = 1.0
    seltype = 0
    useTime = True
    timeUnit = 5.0

    animcruvechanage = None

    def __init__(self):
        om.MPxCommand.__init__(self)


    def parseArguments(self,args):

        argdata = om.MArgParser(self.syntax(),args)

        if argdata.isFlagSet( methodShortFlagName ):
            if argdata.flagArgumentString(methodShortFlagName,0) == "3linear":
                self.method = 0
            elif argdata.flagArgumentString(methodShortFlagName,0) == "3bell":
                self.method = 1
            elif argdata.flagArgumentString(methodShortFlagName,0) == "3ham":
                self.method = 2
            elif argdata.flagArgumentString(methodShortFlagName,0) == "5quad":
                self.method = 10
            elif argdata.flagArgumentString(methodShortFlagName,0) == "5bell":
                self.method = 11
            elif argdata.flagArgumentString(methodShortFlagName,0) == "5ham":
                self.method = 12
            else:
                raise Exception("input method argument is not vaild!"+str(argdata.flagArgumentString(methodShortFlagName,0)))
        else:
            raise Exception("no input method argument")
        
        if argdata.isFlagSet( iterShortFlagName ):
            if argdata.flagArgumentInt(iterShortFlagName,0) <= 100:
                self.iteration = argdata.flagArgumentInt(iterShortFlagName,0)
            else:
                raise Exception("iteration is bigger than 100,little bit too high,right?")
        
        if argdata.isFlagSet( intensityShortFlagName ):
            self.intensity = argdata.flagArgumentFloat(intensityShortFlagName,0)

        if argdata.isFlagSet( seltypeShortFlagName ):
            self.seltype = argdata.flagArgumentInt(seltypeShortFlagName,0)

        if argdata.isFlagSet( useTimeShortFlagName ):
            self.useTime = argdata.flagArgumentBool(useTimeShortFlagName,0)

        if argdata.isFlagSet( timeUnitShortFlagName ):
            self.timeUnit = argdata.flagArgumentFloat(timeUnitShortFlagName,0)

    @staticmethod
    def cmdCreator():
        return SmoothAnimCurve()
    
    def doIt(self, args):

        self.animcruvechanage = omani.MAnimCurveChange()
        self.parseArguments(args)




        animcurves = self.getanimcurves()

        for iter in range(self.iteration):

            for cv in animcurves:
                keylist = self.getkeylist(cv)
                templist = self.smoothkeylistvalue(cv,keylist)
                print(templist)
                mslist = om.MGlobal.getSelectionListByName(repr(cv)[2:-1])
                mit = om.MItSelectionList(mslist)
                mobj = mit.getDependNode()
                manimcurve = omani.MFnAnimCurve(mobj)
                curveisangular = False
                if manimcurve.animCurveType == manimcurve.kAnimCurveTA or manimcurve.animCurveType == manimcurve.kAnimCurveUA :
                    curveisangular = True
                for i in templist:
                    if curveisangular:
                        value = math.radians(i[1])
                    else:
                        value = i[1]
                    manimcurve.setValue(i[0],value,self.animcruvechanage)
                    pass


        print("using smoothanimcurve cmd with argument:\nselect type:",self.seltype,"\niteration:",self.iteration,"\nintensity:",self.intensity,"\nusetime:",self.useTime,"\ntimeunit:",self.timeUnit,"\nmethod:",self.method)


    def undoIt(self):
        if self.animcruvechanage != None :
            self.animcruvechanage.undoIt()
            print("undo success") 
        else:
            print("undo failed:self.animcruvechanage == None") 

    def redoIt(self):
        if self.animcruvechanage != None :
            self.animcruvechanage.redoIt()
            print("redo success") 
        else:
            print("redo failed:self.animcruvechanage == None") 

    def isUndoable(self):
        return True

    def getanimcurves(self):
        selectflag = cmds.animCurveEditor("graphEditor1GraphEd",query = True,areCurvesSelected = True)
        showncurves = cmds.animCurveEditor("graphEditor1GraphEd",query = True,curvesShown  = True)
        selectedcurves = cmds.keyframe(q = True,s = True,name = True)
        isoflag = 0
        if showncurves == None:
            raise Exception("plugin can't find any curve in graph editor,no curve shown or selected.")
        else:
            isoflag = len(showncurves) != len(selectedcurves)

        if selectflag:
            return selectedcurves
        if isoflag:
            self.seltype == 0
            return showncurves
        else:
            raise Exception("plugin can't find any curve in graph editor,no curve shown or selected.")
        
        # if selectflag:
        #     return selectedcurves
        # else:
        #     return showncurves
        # print(showncurves)
        # print("----------------")
        # print(selectedcurves)

    def getkeylist(self,animcurve):
        numkeys = cmds.keyframe(animcurve,q = True,keyframeCount = True)
        keylist = []
        #seltype == 0 :all keys on curves
        if self.seltype == 0:
            for i in range(numkeys):
                keylist.append([i,0.0])
        #seltype == 1 :selected keys only
        elif self.seltype == 1:
            numselkeyindexlist = cmds.keyframe(animcurve,sl = True,q=True,indexValue = True)
            for index in numselkeyindexlist:
                keylist.append([int(index),0.0])
        return keylist


        
    def smoothkeylistvalue(self,curve,keylist):
        flag5pt = False
        compareint = 0
        if self.method>=9:
            compareint = 1
            flag5pt = True
        numkeys = cmds.keyframe(curve,q = True,keyframeCount = True)
        for key in keylist:
            time = getkeytime(curve,key[0])
            value = getkeyvalue(curve,time)


            if key[0] <=compareint or numkeys-key[0]<=compareint+1:
                
                key[1] = value
            
            else:
                pretime2 = 0
                prevalue2 = 0
                nexttime2 = 0 
                nextvalue2 = 0

                pretime = getkeytime(curve,key[0]-1)
                nexttime = getkeytime(curve,key[0]+1)

                if self.useTime:
                    pretime = time - self.timeUnit
                    nexttime = time + self.timeUnit
                else:
                    pass

                prevalue = getkeyvalue(curve,pretime)
                nextvalue = getkeyvalue(curve,nexttime)


                

                if flag5pt:
                    pretime2 = getkeytime(curve,key[0]-2)
                    nexttime2 = getkeytime(curve,key[0]+2)

                    if self.useTime:
                        pretime2 = time - self.timeUnit*2
                        nexttime2 = time + self.timeUnit*2
                    else:
                        pass


                    prevalue2 = getkeyvalue(curve,pretime2)
                    nextvalue2 = getkeyvalue(curve,nexttime2)

                if self.method == 0:
                    tempvalue = value+prevalue+nextvalue
                    key[1] = lerp(value,tempvalue/3,self.intensity)
                elif self.method == 1:
                    tempvalue = 0.576*value+0.212*prevalue+0.212*nextvalue
                    key[1] = lerp(value,tempvalue,self.intensity)
                elif self.method == 2:
                    tempvalue = 0.86*value+0.07*prevalue+0.07*nextvalue
                    key[1] = lerp(value,tempvalue,self.intensity)
                elif self.method == 10:
                    tempvalue = 12*prevalue+nextvalue-3*prevalue2+nextvalue2+17*value
                    key[1] = lerp(value,tempvalue/35,self.intensity)
                elif self.method == 11:
                    tempvalue = 0.11*(prevalue2+nextvalue2)+0.24*(prevalue+nextvalue)+0.3*(value)
                    key[1] = lerp(value,tempvalue,self.intensity)
                elif self.method == 12:
                    tempvalue = 0.04*(prevalue2+nextvalue2)+0.24*(prevalue+nextvalue)+0.44*(value)
                    key[1] = lerp(value,tempvalue,self.intensity)
                else:
                    raise Exception("method error while using smoothkeylistvalue()")

        return keylist

def getkeytime(curve,id):
    time = cmds.keyframe(curve,index=(id,id),q=True)[0]
    return time
def getkeyvalue(curve,time):
    value = cmds.keyframe(curve,t = (time,time),ev = True , q = True )[0]
    return value
def lerp(originvalue,newvalue,intensity):
    temp = newvalue-originvalue
    return originvalue+temp*intensity




# define new smooth function

def getanimcurves():
    selectflag = cmds.animCurveEditor("graphEditor1GraphEd",query = True,areCurvesSelected = True)
    showncurves = cmds.animCurveEditor("graphEditor1GraphEd",query = True,curvesShown  = True)
    selectedcurves = cmds.keyframe(q = True,s = True,name = True)
    isoflag = 0
    if showncurves == None:
        raise Exception("plugin can't find any curve in graph editor,no curve shown or selected.")
    else:
        isoflag = len(showncurves) != len(selectedcurves)

    if selectflag:
        return selectedcurves
    if isoflag:
        return showncurves
    else:
        raise Exception("plugin can't find any curve in graph editor,no curve shown or selected.")

def getkeylist(animcurve,selType):
    numkeys = cmds.keyframe(animcurve,q = True,keyframeCount = True)
    keylist = []
    #seltype == 0 :all keys on curves
    if selType == 0:
        for i in range(numkeys):
            keylist.append([i,0.0])
    #seltype == 1 :selected keys only
    elif selType == 1:
        numselkeyindexlist = cmds.keyframe(animcurve,sl = True,q=True,indexValue = True)
        for index in numselkeyindexlist:
            keylist.append([int(index),0.0])
    return keylist

def smoothkeylist(intensity,method,useTime,timeUnit,curve,keylist):
    flag5pt = False
    compareint = 0
    if method>=9:
        compareint = 1
        flag5pt = True
    numkeys = cmds.keyframe(curve,q = True,keyframeCount = True)
    for key in keylist:
        time = getkeytime(curve,key[0])
        value = getkeyvalue(curve,time)


        if key[0] <=compareint or numkeys-key[0]<=compareint+1:
            
            key[1] = value
        
        else:
            pretime2 = 0
            prevalue2 = 0
            nexttime2 = 0 
            nextvalue2 = 0

            pretime = getkeytime(curve,key[0]-1)
            nexttime = getkeytime(curve,key[0]+1)

            if useTime:
                pretime = time - timeUnit
                nexttime = time + timeUnit
            else:
                pass

            prevalue = getkeyvalue(curve,pretime)
            nextvalue = getkeyvalue(curve,nexttime)


            

            if flag5pt:
                pretime2 = getkeytime(curve,key[0]-2)
                nexttime2 = getkeytime(curve,key[0]+2)

                if useTime:
                    pretime2 = time - timeUnit*2
                    nexttime2 = time + timeUnit*2
                else:
                    pass


                prevalue2 = getkeyvalue(curve,pretime2)
                nextvalue2 = getkeyvalue(curve,nexttime2)

            if method == 0:
                tempvalue = value+prevalue+nextvalue
                key[1] = lerp(value,tempvalue/3,intensity)
            elif method == 1:
                tempvalue = 0.576*value+0.212*prevalue+0.212*nextvalue
                key[1] = lerp(value,tempvalue,intensity)
            elif method == 2:
                tempvalue = 0.86*value+0.07*prevalue+0.07*nextvalue
                key[1] = lerp(value,tempvalue,intensity)
            elif method == 10:
                tempvalue = 12*(prevalue+nextvalue)-3*(prevalue2+nextvalue2)+17*value
                key[1] = lerp(value,tempvalue/35,intensity)
            elif method == 11:
                tempvalue = 0.11*(prevalue2+nextvalue2)+0.24*(prevalue+nextvalue)+0.3*(value)
                key[1] = lerp(value,tempvalue,intensity)
            elif method == 12:
                tempvalue = 0.04*(prevalue2+nextvalue2)+0.24*(prevalue+nextvalue)+0.44*(value)
                key[1] = lerp(value,tempvalue,intensity)
            else:
                raise Exception("method error while using smoothkeylist()")

    return keylist

def updatedsmoothanimcurve(method , iteration , intensity , selType , useTime , timeUnit):
    if method == "3linear":
        methodint = 0
    elif method == "3bell":
        methodint = 1
    elif method == "3ham":
        methodint = 2
    elif method == "5quad":
        methodint = 10
    elif method == "5bell":
        methodint = 11
    elif method == "5ham":
        methodint = 12
    else:
        raise Exception("input method argument is not vaild!"+method)
    
    print("smooth method:"+method+str(methodint))
    mocaphelperutility.openUndoChunk()
    animcurves = getanimcurves()

    for i in range(iteration):
        for curve in animcurves:
            keylist = getkeylist(curve,selType)
            templist = smoothkeylist(intensity,methodint,useTime,timeUnit,curve,keylist)

            curveisangular = False
            curvetype = cmds.nodeType(curve)
            if curvetype == "animCurveTA" or curvetype == "animCurveUA" :
                curveisangular = True
            for keypair in templist:
                # if curveisangular:
                #     value = math.radians(keypair[1])
                # else:
                #     value = keypair[1]
                value = keypair[1]
                cmds.keyframe(curve,edit = True,index = (keypair[0],keypair[0]),valueChange = value)

    mocaphelperutility.closeUndoChunk()