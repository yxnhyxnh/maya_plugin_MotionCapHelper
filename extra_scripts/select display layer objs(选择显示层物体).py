import maya.cmds as cmds
import maya.mel as mel

curlayer = cmds.editDisplayLayerGlobals( query=True, cdl=True )
if curlayer =="defaultLayer" :
    raise Exception("using default layer!")
else:
    slist = cmds.editDisplayLayerMembers(curlayer,query=True )
    print(slist)
    cmds.select( clear=True )
    cmds.select(slist, visible=True )

    mel.eval("syncChannelBoxFcurveEd;")
    mel.eval("syncChannelBoxFcurveEd;")
    mel.eval("syncChannelBoxFcurveEd;")
