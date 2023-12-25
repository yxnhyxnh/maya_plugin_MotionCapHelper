import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as omani
import maya.cmds as cmds

import maya.mel as mel

import mocaphelperutility

refobjsShortFlagName = "-ref"
refobjsLongFlagName = "-refobjs"



def syntaxCreator():

    syntax = om.MSyntax()
    
    syntax.addFlag( refobjsShortFlagName, refobjsLongFlagName, om.MSyntax.kString )

        
    return syntax
    
class FrameAlign(om.MPxCommand):
    kPluginCmdName = "moCapHelper_frameAlign"

    ref = ""
    animcruvechanage = None

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return FrameAlign()
    
    
    def parseArguments(self,args):

        argdata = om.MArgParser(self.syntax(),args)

        if argdata.isFlagSet( refobjsShortFlagName ):
            self.ref = argdata.flagArgumentString(refobjsShortFlagName,0)
        else:
            raise Exception("No refence argument!")
    
    def isUndoable(self):
        return True


    def doIt(self,args):
        self.animcruvechanage = omani.MAnimCurveChange()
        self.parseArguments(args)
        # start = cmds.playbackOptions( q=True,min=True )
        # end  = cmds.playbackOptions( q=True,max=True )
        if mocaphelperutility.objExist(self.ref) == False:
            raise Exception("ref obj does not exist!")
        selectedobjs = mocaphelperutility.getSelectedNodes()
        print(self.ref)
        if cmds.keyframe(self.ref,q = True) == None :
            raise Exception("ref has no keys!")
        else:
            framelist = set(cmds.keyframe(self.ref,q = True))
        for frame in framelist:
            cmds.setKeyframe(selectedobjs,t = (frame,frame),rk= True,hierarchy = "none",i = True,itt = "auto")
        
        for obj in selectedobjs:
            objframelist = set(cmds.keyframe(obj,q = True))
            for objframe in objframelist:
                if objframe in framelist:
                    continue
                else:
                    mocaphelperutility.cutKey(obj,objframe,objframe)


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




# def cutlist(sourcelist,splitlist):
#     backindex = 0
#     forwardindex = 0
#     for i in len(sourcelist):
#         if sourcelist[i] in splitlist:

# def fastRecord(obj):
#     pos = mocaphelperutility.getWorldPos(obj)
#     loc = mocaphelperarbcore.createLoc("mocaphelper_fa_temp_loc")