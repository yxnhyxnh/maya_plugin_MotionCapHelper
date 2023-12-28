import maya.cmds as cmds
objs = cmds.ls(selection = True,type = "dagNode",long = True)

selectobjflag = True
selectmultiobjflag = False
if len(objs) == 0:
    selectobjflag = False
else:
    if len(objs) != 1:
        selectmultiobjflag = True
    


if objs == None:
    selectobjflag = False

curves = cmds.keyframe(query = True , selected = True , name  = True)
print(type(curves))
selectkeyflag = True
if curves == None:
    selectkeyflag = False

if selectobjflag:
    if selectkeyflag:
        nodes = set()
        for cv in curves:
            node = cmds.listConnections(cv)[0]
            nodes.add(node)
        cmds.select(clear = True)
        cmds.select(nodes)
        print("TRACE BACK OBJS FROM KEY: " + str(nodes))
    else:
        obj = cmds.ls(objs[0])[0]
        
        layer = cmds.ls(cmds.listConnections(obj,t = "displayLayer"))
        if len(layer) == 0:
            print("this obj has no layer,or you have selected multiple objs.")
        elif cmds.editDisplayLayerGlobals(cdl = True,q = True) == "defaultLayer":
            print("no display layer selected,trace back won\'t work.")
        else:
            cmds.editDisplayLayerGlobals(cdl = layer[0])
            
            if selectmultiobjflag:
                print("TRACE BACK LAYER FROM OBJ: " + layer[0] + "BUT WITH MULTIPLE OBJS SELECTED,SO RESULE IS UNEXPECTED.")
            else:
                print("TRACE BACK LAYER FROM OBJ: " + layer[0] )
else :
    print("no objs selected!")
