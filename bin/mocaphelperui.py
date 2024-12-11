# coding=utf-8
# -*- coding: utf-8 -*-


import os

from mocaphelper import version
import mocaphelperutility
import mocaphelperrecore
import mocaphelperarbcore
from mocaphelpersaccore import updatedsmoothanimcurve


from maya import cmds
from maya import mel
from maya import OpenMayaUI as omui 

try:
    from PySide2.QtCore import * 
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2.QtUiTools import *
    from shiboken2 import wrapInstance 
except ImportError:
    from PySide6.QtCore import * 
    from PySide6.QtGui import *
    from PySide6.QtWidgets import *
    from PySide6.QtUiTools import *
    from shiboken6 import wrapInstance 


mayaMainWindowPtr = omui.MQtUtil.mainWindow() 
pyVersion = mocaphelperutility.getPythonVersion()
if pyVersion < 3:
    mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget) 
else:
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget) 


class MoCapHelperUI(QWidget):
    #sac:
    sac_iteration = 1
    sac_intensity = 1.0
    sac_useTime = True
    sac_method = "3linear"
    sac_selType = "curves"
    sac_timeUnit = 5.0

    #fa:
    fa_refobjs = None

    #re:
    re_exp = ""
    re_name = ""
    re_caseCheck = False
    re_prefix = ""

    #arb:
    arb_fromtime = 10.0
    arb_totime = 11.0
    def __init__(self, *args, **kwargs):

        super(MoCapHelperUI, self).__init__(*args, **kwargs)
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)
        self.setObjectName('mocaphelperui')
        self.setWindowTitle('moCapHelper v'+str(version))
        self.loadUI()
        self.initSac()
        self.initFa()
        self.initre()
        self.intiArb()
        self.re_exp = self.ui.re_expEdit.text()
        # self.arb_syncRange()

    def loadUI(self):
        loader = QUiLoader()
        currentDir = os.path.dirname(__file__)
        file = QFile(currentDir+"/mocaphelperui.ui")
        file.open(QFile.ReadOnly)
        try:
            self.ui = loader.load(file, parentWidget=self) 
        finally:
            file.close()

        layout = QVBoxLayout()
        layout.addWidget(self.ui)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

    #sac:
    def initSac(self):

        self.ui.sac_itEdit.textEdited.connect(self.on_sac_itEditEdited)
        self.ui.sac_inEdit.textEdited.connect(self.on_sac_inEditEdited)
        self.ui.sac_utCheckBox.stateChanged.connect(self.on_sac_utCheckBoxChanged)
        self.ui.sac_tuEdit.textEdited.connect(self.on_sac_tuEditEdited)
        try:
            self.ui.sac_selTypeComboBox.activated[str].connect(self.on_sac_selTypeComboBoxChanged)
            self.ui.sac_smoothMethodComboBox.activated[str].connect(self.on_sac_smoothMethodComboBoxChanged)
        except:
            self.ui.sac_selTypeComboBox.currentTextChanged[str].connect(self.on_sac_selTypeComboBoxChanged)
            self.ui.sac_smoothMethodComboBox.currentTextChanged[str].connect(self.on_sac_smoothMethodComboBoxChanged)
        self.ui.sac_cmdButton.clicked.connect(self.on_sac_cmdButtonClicked)

    def on_sac_itEditEdited(self):
        self.sac_iteration = int(eval(self.ui.sac_itEdit.text()))
    
    def on_sac_inEditEdited(self):
        self.sac_intensity = float(eval(self.ui.sac_inEdit.text()))

    def on_sac_utCheckBoxChanged(self):
        self.sac_useTime = self.ui.sac_utCheckBox.isChecked()

    def on_sac_tuEditEdited(self):
        self.sac_timeUnit = float(eval(self.ui.sac_tuEdit.text()))

    def on_sac_selTypeComboBoxChanged(self, text):
        self.sac_selType = text
    
    def on_sac_smoothMethodComboBoxChanged(self, text):
        self.sac_method = text

    def on_sac_cmdButtonClicked(self):
        seltype = 0

        if self.sac_selType == 'selected keys' :
            seltype = 1


        # cmds.moCapHelper_smoothAniCurve( method = self.sac_method , i = self.sac_iteration , intensity = self.sac_intensity , sel = seltype , u = self.sac_useTime , tu = self.sac_timeUnit )

        updatedsmoothanimcurve(self.sac_method ,self.sac_iteration ,self.sac_intensity , seltype , self.sac_useTime , self.sac_timeUnit )


    #fa:
    def initFa(self):

        self.ui.fa_assignButton.clicked.connect(self.on_fa_assignButtonClicked)
        self.ui.fa_cmdButton.clicked.connect(self.on_fa_cmdButtonClicked)
        self.ui.fa_fastRecordButton.clicked.connect(self.on_fa_fastRecordButtonClicked)


    def on_fa_assignButtonClicked(self):
        curnode = mocaphelperutility.getSelectedNodes()[0]
        self.ui.fa_refEdit.setText(curnode)

    def on_fa_cmdButtonClicked(self):
        if self.ui.fa_refEdit.text() =="":
            raise Exception("no ref obj in ui!")
        else:
            #cmds.moCapHelper_frameAlign(ref = self.fa_refobjs)
            mel.eval("moCapHelper_frameAlign -ref "+self.ui.fa_refEdit.text())

    def on_fa_fastRecordButtonClicked(self):
        obj = mocaphelperutility.getSelectedNodes()[0]
        loc = mocaphelperarbcore.createLoc("mocaphelper_fa_temp_loc")[0]
        cmds.setKeyframe(loc,at = ["tx"])
        self.ui.fa_refEdit.setText(obj)
        mocaphelperutility.selectNodes(loc)
        self.on_fa_cmdButtonClicked()
        self.ui.fa_refEdit.setText(loc)

    #re:
    def initre(self):
        currentDir = os.path.dirname(__file__)
        self.re_presetFilePath = currentDir+"\\re_exp_preset.txt"
        self.re_backupPresetFilePath = currentDir+"\\re_exp_preset_backup.txt"
        if os.path.exists(self.re_presetFilePath) == False:
            mocaphelperrecore.presetfileRebuild(self.re_presetFilePath,self.re_backupPresetFilePath)


        self.ui.re_expPresetComboBox.currentIndexChanged.connect(self.on_re_expPresetComboBoxChanged)
        self.re_reloadPreset()

        self.ui.re_reloadButton.clicked.connect(self.on_re_reloadButtonClicked)
        self.ui.re_openFileButton.clicked.connect(self.on_re_openFileButtonClicked)
        self.ui.re_assignButton.clicked.connect(self.on_re_assignButtonClicked)
        self.ui.re_recordButton.clicked.connect(self.on_re_recordButtonClicked)
        






        self.ui.re_layerNameEdit.setText("layername")
        self.ui.re_prefixEdit.textChanged.connect(self.on_re_layerPrefixEditEdited)
        self.ui.re_prefixEdit.textEdited.connect(self.on_re_layerPrefixEditEdited)
        self.ui.re_layerNameEdit.textChanged.connect(self.on_re_layerNameEditEdited)
        self.ui.re_layerNameEdit.textEdited.connect(self.on_re_layerNameEditEdited)

        self.ui.re_expEdit.textChanged.connect(self.on_re_expEditEdited)
        self.ui.re_expEdit.textEdited.connect(self.on_re_expEditEdited)
        self.ui.re_selectMainCtrlButton.clicked.connect(self.on_re_selectMainCtrlButtonClicked)
        self.ui.re_selectChildButton.clicked.connect(self.on_re_selectChildButtonClicked)
        self.ui.re_selectChildCtrlButton.clicked.connect(self.on_re_selectChildCtrlButtonClicked)
        self.ui.re_selectVisChildCtrlButton.clicked.connect(self.on_re_selectVisChildCtrlButtonClicked)
        self.ui.re_expSelectButton.clicked.connect(self.on_re_expSelectButtonClicked)
        self.ui.re_expCreateLayerButton.clicked.connect(self.on_re_expcreateLayerButtonClicked)
        self.ui.re_selectedCreateLayerButton.clicked.connect(self.on_re_selcreateLayerButtonClicked)
        self.ui.re_caseCheckCheckBox.stateChanged.connect(self.on_re_caseCheckCheckBoxChanged)
        self.ui.re_extractLayerInfoButton.clicked.connect(self.on_re_extractLayerInfoButtonClicked)

    def on_re_layerPrefixEditEdited(self):
        self.re_prefix = self.ui.re_prefixEdit.text()

    def on_re_layerNameEditEdited(self):
        self.re_name = self.ui.re_layerNameEdit.text()

    def on_re_expEditEdited(self):
        self.re_exp = self.ui.re_expEdit.text()

    def on_re_selectChildButtonClicked(self):
        selectednodes = mocaphelperutility.getSelectedNodes()
        children = mocaphelperutility.getChildNodes(selectednodes,nodetype="all")
        mocaphelperutility.selectNodes(children)
        print("objs selected: ",children)

    def on_re_selectChildCtrlButtonClicked(self):
        selectednodes = mocaphelperutility.getSelectedNodes()
        children = mocaphelperutility.getChildNodes(selectednodes,nodetype="nurbsCurve")
        mocaphelperutility.selectNodes(children)
        print("objs selected: ",children)

    def on_re_selectVisChildCtrlButtonClicked(self):
        selectednodes = mocaphelperutility.getSelectedNodes()
        children = mocaphelperutility.getChildNodes(selectednodes,nodetype="nurbsCurve")
        mocaphelperutility.selectNodes(children,visible=True)
        print("objs selected: ",children)

    def on_re_selectMainCtrlButtonClicked(self):
        mocaphelperrecore.selMainCtrl()

    def on_re_expSelectButtonClicked(self):
        actOnType = getReActOnType(self)
        childcheck = self.ui.re_childCheckBox.isChecked()
        seltednodes = mocaphelperutility.getSelectedNodes()
        if childcheck:
            ctrls = mocaphelperutility.getChildNodes(seltednodes,nodetype=actOnType)
        else:
            ctrls = seltednodes
        matchlist = mocaphelperrecore.retestlist(ctrls,self.re_exp,self.re_caseCheck)
        mocaphelperutility.selectNodes(matchlist)
        print("objs selected: ",matchlist)


    def on_re_selcreateLayerButtonClicked(self):
        sel = mocaphelperutility.getSelectedNodes()
        mocaphelperrecore.createDisplayLayer(self.re_prefix+self.re_name,sel)

    def on_re_expcreateLayerButtonClicked(self):
        actOnType = getReActOnType(self)
        childcheck = self.ui.re_childCheckBox.isChecked()
        mocaphelperutility.openUndoChunk()
        try:

            mocaphelperrecore.expCreateDisplayLayer(self.re_exp,self.re_name,self.re_prefix,self.re_caseCheck,childcheck = childcheck ,nodetype = actOnType)
        finally:
            mocaphelperutility.closeUndoChunk()
    def on_re_extractLayerInfoButtonClicked(self):
        mocaphelperrecore.extractLayerInfo(self)

    def on_re_caseCheckCheckBoxChanged(self):
        self.re_caseCheck = self.ui.re_caseCheckCheckBox.isChecked()

    def on_re_expPresetComboBoxChanged(self):
        pass

    def on_re_assignButtonClicked(self):
        index = self.ui.re_expPresetComboBox.currentIndex()
        self.ui.re_layerNameEdit.setText(self.re_itemlist[index][0])
        self.ui.re_expEdit.setText(self.re_itemlist[index][1])


    def on_re_recordButtonClicked(self):
        self.re_rawstr = mocaphelperrecore.strAppend(self.re_rawstr,self.re_name,self.re_exp)
        self.re_itemlist = mocaphelperrecore.rawStrBuild(self.re_rawstr)
        mocaphelperrecore.presetfileRebuild(self.re_presetFilePath,self.re_backupPresetFilePath)
        mocaphelperrecore.presetFileWrite(self.re_presetFilePath,self.re_rawstr)
        self.re_reloadPreset()

    def on_re_openFileButtonClicked(self):
        os.startfile(self.re_presetFilePath)

    def on_re_reloadButtonClicked(self):
        self.re_reloadPreset()

    def re_expPresetComboBoxRebuild(self):
        self.ui.re_expPresetComboBox.clear()
        for item in self.re_itemlist:
            convertedstr = "\""+item[0]+"\"\""+item[1]+"\""
            self.ui.re_expPresetComboBox.addItem( convertedstr )
        self.ui.re_expPresetComboBox.setCurrentIndex(0)

    def re_reloadPreset(self):
        if os.path.exists(self.re_presetFilePath) == False:
            mocaphelperrecore.presetfileRebuild(self.re_presetFilePath,self.re_backupPresetFilePath)
        self.re_rawstr =  mocaphelperrecore.presetFileRead(self.re_presetFilePath)
        self.re_itemlist = mocaphelperrecore.rawStrBuild(self.re_rawstr)
        self.re_expPresetComboBoxRebuild()



    # arb:
    def intiArb(self):
        # timerange
        self.ui.arb_setFromButton.clicked.connect(self.arb_setFrom)
        self.ui.arb_setToButton.clicked.connect(self.arb_setTo)
        self.ui.arb_syncRangeButton.clicked.connect(self.arb_syncRange)
        self.ui.arb_delInRangeButton.clicked.connect(self.on_arb_delInRangeButtonClicked)
        self.ui.arb_delOutRangeButton.clicked.connect(self.on_arb_delOutRangeButtonClicked)
        self.ui.arb_offsetFrameButton.clicked.connect(self.on_arb_offsetFrameButtonClicked)
        self.ui.arb_stickyDelButton.clicked.connect(self.on_arb_stickyDelButtonClicked)

        self.ui.arb_fromEdit.textChanged.connect(self.on_arb_fromEditEdited)
        self.ui.arb_fromEdit.textEdited.connect(self.on_arb_fromEditEdited)

        self.ui.arb_toEdit.textChanged.connect(self.on_arb_toEditEdited)
        self.ui.arb_toEdit.textEdited.connect(self.on_arb_toEditEdited)
        # basic
        self.ui.arb_createLocButton.clicked.connect(self.on_arb_createLocButtonClicked)
        self.ui.arb_rePosButton.clicked.connect(self.on_arb_rePosButtonClicked)
        self.ui.arb_pointConstraintButton.clicked.connect(self.on_arb_pointConstraintButtonClicked)
        self.ui.arb_orientConstraintButton.clicked.connect(self.on_arb_orientConstraintButtonClicked)
        self.ui.arb_parentConstraintButton.clicked.connect(self.on_arb_parentConstraintButtonClicked)
        self.ui.arb_delConstraintButton.clicked.connect(self.on_arb_delConstraintButtonClicked)
        self.ui.arb_bakeButton.clicked.connect(self.on_arb_bakeButtonClicked)
        # simplebake
        self.ui.arb_simpleBakeAAssignButton.clicked.connect(self.on_arb_simpleBakeAAssignButtonClicked)
        self.ui.arb_simpleBakeBAssignButton.clicked.connect(self.on_arb_simpleBakeBAssignButtonClicked)

        self.ui.arb_simpleBakeToLocButton.clicked.connect(self.on_arb_simpleBakeToLocButtonClicked)
        self.ui.arb_simpleBakeAToBButton.clicked.connect(self.on_arb_simpleBakeAToBButtonClicked)
        self.ui.arb_simpleBakeBToAButton.clicked.connect(self.on_arb_simpleBakeBToAButtonClicked)
        # fk2ik

        self.ui.arb_fk2ikEndCtrlAssignButton.clicked.connect(self.on_arb_fk2ikEndCtrlAssignButtonClicked)
        self.ui.arb_fk2ikCtrlRefAssignButton.clicked.connect(self.on_arb_fk2ikCtrlRefAssignButtonClicked)
        self.ui.arb_fk2ikTwistAssignButton.clicked.connect(self.on_arb_fk2ikTwistAssignButtonClicked)
        self.ui.arb_fk2ikTwistRefAssignButton.clicked.connect(self.on_arb_fk2ikTwistRefAssignButtonClicked)
        self.ui.arb_fk2ikConvertButton.clicked.connect(self.on_arb_fk2ikConvertButtonClicked)

        # pinpos
        self.ui.arb_pinPosPinCurButton.clicked.connect(self.on_arb_pinPosPinCurButtonClicked)
        self.ui.arb_pinPosPinParentButton.clicked.connect(self.on_arb_pinPosPinParentButtonClicked)

        self.arb_syncRange()
        
    def on_arb_fromEditEdited(self):
        print("setfrom:",eval(self.ui.arb_fromEdit.text()))
        self.arb_fromtime = float(eval(self.ui.arb_fromEdit.text()))


    def on_arb_toEditEdited(self):
        print("setto:",eval(self.ui.arb_toEdit.text()))
        self.arb_totime = float(eval(self.ui.arb_toEdit.text()))
        # print("setto:",self.ui.arb_toEdit.text(),self.arb_totime)

    def arb_syncRange(self):
        timerange = mocaphelperutility.getTimeRange()
        print("syncrangeresult:",timerange)
        self.ui.arb_fromEdit.setText(str(timerange[0]))
        self.ui.arb_toEdit.setText(str(timerange[1]))


    def arb_setFrom(self):
        time = mocaphelperutility.getCurrentFrame()
        self.ui.arb_fromEdit.setText(str(time))

    def arb_setTo(self):
        time = mocaphelperutility.getCurrentFrame()
        self.ui.arb_toEdit.setText(str(time))

    def on_arb_delInRangeButtonClicked(self):
        objs = mocaphelperutility.getSelectedNodes()
        print("delete inrange",self.arb_fromtime,self.arb_totime)
        mocaphelperarbcore.deleteInrange(objs,self.arb_fromtime,self.arb_totime)

    def on_arb_delOutRangeButtonClicked(self):
        if self.arb_fromtime>self.arb_totime:
            raise Exception("fromtime > totime")
        else:
            objs = mocaphelperutility.getSelectedNodes()
            print("delete outrange",self.arb_fromtime,self.arb_totime)
            mocaphelperarbcore.deleteOutrange(objs,self.arb_fromtime,self.arb_totime)

    def on_arb_offsetFrameButtonClicked(self):
        if self.arb_fromtime==self.arb_totime:
            raise Exception("fromtime == totime")
        else:
            offsettime = self.arb_totime-self.arb_fromtime 
            objs = mocaphelperutility.getSelectedNodes()
            mocaphelperarbcore.offsetFrame(objs,offsettime)

    def on_arb_stickyDelButtonClicked(self):
        mocaphelperarbcore.stickyDelete(self)
    
    def on_arb_createLocButtonClicked(self):
        objs = mocaphelperutility.getSelectedNodes()
        pos = mocaphelperutility.getWorldPos(objs[0])
        rot = mocaphelperutility.getWorldRot(objs[0])
        roo = mocaphelperutility.getRotOrder(objs[0])
        mocaphelperarbcore.createLoc("c_loc_"+objs[0],pos,rot,roo)

    def on_arb_rePosButtonClicked(self):
        objs = mocaphelperutility.getSelectedNodes()
        mocaphelperarbcore.reposition(objs[0],objs[1])

    def on_arb_pointConstraintButtonClicked(self):
        objs = mocaphelperutility.getSelectedNodes()
        ctrlobj = objs[:-1]
        targetobj = objs[-1]
        mocaphelperarbcore.createPointConstraint(ctrlobj,targetobj,maintainoffset=self.ui.arb_maintainOffsetCheckBox.isChecked())

    def on_arb_orientConstraintButtonClicked(self):
        objs = mocaphelperutility.getSelectedNodes()
        ctrlobj = objs[:-1]
        targetobj = objs[-1]
        mocaphelperarbcore.createOrientConstraint(ctrlobj,targetobj,maintainoffset=self.ui.arb_maintainOffsetCheckBox.isChecked())

    def on_arb_parentConstraintButtonClicked(self):
        objs = mocaphelperutility.getSelectedNodes()
        ctrlobj = objs[:-1]
        targetobj = objs[-1]
        mocaphelperarbcore.createParentConstraint(ctrlobj,targetobj,maintainoffset=self.ui.arb_maintainOffsetCheckBox.isChecked())

    def on_arb_delConstraintButtonClicked(self):
        objs = mocaphelperutility.getSelectedNodes()
        mocaphelperarbcore.deleteAllConstraint(objs)
        # for obj in objs:
        #     check = mocaphelperarbcore.checkConstraint(obj)
        #     if check != False:
        #         if check[0] != None:
        #             mocaphelperarbcore.deleteParentConstraint(check[0],obj)
        #         elif check[1] != None :
        #             mocaphelperarbcore.deletePointConstraint(check[1],obj)
        #         elif check[2] != None :
        #             mocaphelperarbcore.deleteOrientConstraint(check[2],obj)
        #         else:
        #             raise Exception("delconstraint error: constraint list out of range!")
        #     else:
        #         point = cmds.listRelatives(obj,children = True,type = "pointConstraint")
        #         orient = cmds.listRelatives(obj,children = True,type = "orientConstraint")


    def on_arb_bakeButtonClicked(self):
        mintime = self.arb_fromtime
        maxtime = self.arb_totime
        objs = mocaphelperutility.getSelectedNodes()
        singleobj = objs[0]
        check = mocaphelperarbcore.checkConstraint(singleobj)
        smartbake = self.ui.arb_smartBakeCheckBox.isChecked()
        if len(objs) == 1 and self.ui.arb_onlyBakeConstraintCheckBox.isChecked() and check != False:
            type = "all"
            if check[0] != None:
                type = "parent"
            elif check[1] != None :
                type = "point"
            elif check[2] != None :
                type = "orient"    
        else:
            type = "parent"
        
        if smartbake:
            mocaphelperarbcore.smartbake(objs,mintime,maxtime,type)
        else:
            mocaphelperarbcore.bake(objs,mintime,maxtime,type)





    def on_arb_simpleBakeAAssignButtonClicked(self):
        obj = mocaphelperutility.getSelectedNodes()[0]
        self.ui.arb_simpleBakeAEdit.setText(obj)

    def on_arb_simpleBakeBAssignButtonClicked(self):
        obj = mocaphelperutility.getSelectedNodes()[0]
        self.ui.arb_simpleBakeBEdit.setText(obj)

    def on_arb_simpleBakeToLocButtonClicked(self):
        mintime = self.arb_fromtime
        maxtime = self.arb_totime
        targetA = self.ui.arb_simpleBakeAEdit.text()
        mocaphelperutility.openUndoChunk()
        try:
            
            # obj = mocaphelperutility.getSelectedNodes()[0]
            locA = mocaphelperarbcore.createLoc(targetA +"_loc")
            mocaphelperarbcore.createParentConstraint(targetA,locA,False)
            mocaphelperarbcore.bake(locA,mintime,maxtime,"all")
            mocaphelperarbcore.deleteAllConstraint(locA)
            self.ui.arb_simpleBakeBEdit.setText(locA[0])

        finally:
            mocaphelperutility.closeUndoChunk()



    def on_arb_simpleBakeAToBButtonClicked(self):
        targetA = self.ui.arb_simpleBakeAEdit.text()
        targetB = self.ui.arb_simpleBakeBEdit.text()
        maintainoffset=self.ui.arb_maintainOffsetCheckBox.isChecked()
        mocaphelperutility.openUndoChunk()
        try:
            check = mocaphelperarbcore.checkConstraint(targetB)
            if check != False:
                raise Exception("obj B has constraint already!")
            else:
                mintime = self.arb_fromtime
                maxtime = self.arb_totime
                type = getArbType(self)
                mocaphelperarbcore.bakeAtoB(targetA,targetB,mintime,maxtime,type,maintainoffset,smart = self.ui.arb_smartBakeCheckBox.isChecked())

        finally:
            mocaphelperutility.closeUndoChunk()

    def on_arb_simpleBakeBToAButtonClicked(self):
        targetA = self.ui.arb_simpleBakeAEdit.text()
        targetB = self.ui.arb_simpleBakeBEdit.text()
        maintainoffset=self.ui.arb_maintainOffsetCheckBox.isChecked()
        mocaphelperutility.openUndoChunk()
        try:
            check = mocaphelperarbcore.checkConstraint(targetA)
            if check != False:
                raise Exception("obj A has constraint already!")
            else:
                mintime = self.arb_fromtime
                maxtime = self.arb_totime
                type = getArbType(self)
                mocaphelperarbcore.bakeAtoB(targetB,targetA,mintime,maxtime,type,maintainoffset,smart = self.ui.arb_smartBakeCheckBox.isChecked())
        finally:
            mocaphelperutility.closeUndoChunk()
        

    def on_arb_fk2ikEndCtrlAssignButtonClicked(self):
        obj = mocaphelperutility.getSelectedNodes()[0]
        self.ui.arb_fk2ikEndCtrlEdit.setText(obj)

    def on_arb_fk2ikCtrlRefAssignButtonClicked(self):
        obj = mocaphelperutility.getSelectedNodes()[0]
        self.ui.arb_fk2ikCtrlRefEdit.setText(obj)

    def on_arb_fk2ikTwistAssignButtonClicked(self):
        obj = mocaphelperutility.getSelectedNodes()[0]
        self.ui.arb_fk2ikTwistEdit.setText(obj)

    def on_arb_fk2ikTwistRefAssignButtonClicked(self):
        obj = mocaphelperutility.getSelectedNodes()[0]
        self.ui.arb_fk2ikTwistRefEdit.setText(obj)

    def on_arb_fk2ikConvertButtonClicked(self):
        mintime = self.arb_fromtime
        maxtime = self.arb_totime
        maintainoffset=self.ui.arb_maintainOffsetCheckBox.isChecked()
        smartbake = self.ui.arb_smartBakeCheckBox.isChecked()
        endctrl = self.ui.arb_fk2ikEndCtrlEdit.text()
        ctrlref = self.ui.arb_fk2ikCtrlRefEdit.text()
        twist = self.ui.arb_fk2ikTwistEdit.text()
        twistref = self.ui.arb_fk2ikTwistRefEdit.text()
        mocaphelperutility.openUndoChunk()
        try:
            if mocaphelperutility.objExist(endctrl) == False:
                endctrl = ""
            if mocaphelperutility.objExist(ctrlref) == False:
                ctrlref = ""
            if mocaphelperutility.objExist(twist) == False:
                twist = ""
            if mocaphelperutility.objExist(twistref) == False:
                twistref = ""

            check = mocaphelperarbcore.checkConstraint(endctrl)
            if check != False:
                raise Exception("endctrl has constraint already!")
            if mocaphelperutility.objExist(twist) == True:
                check = mocaphelperarbcore.checkConstraint(twist)
            if check != False:
                raise Exception("twist has constraint already!")

            if endctrl== "" or ctrlref =="":
                raise Exception("endctrl or ctrlref not set or not exist")
            else:
                if twist == "" or twistref == "":

                    mocaphelperarbcore.bakeAtoB(ctrlref,endctrl,mintime,maxtime,"parent",maintainoffset,smartbake)
                else:
                    mocaphelperarbcore.bakeAtoB(ctrlref,endctrl,mintime,maxtime,"parent",maintainoffset,smartbake)

                    twistpos = mocaphelperutility.getWorldPos(twist)
                    twistrot = mocaphelperutility.getWorldRot(twist)
                    twistroo = mocaphelperutility.getRotOrder(twist)
                    twistloc = mocaphelperarbcore.createLoc("temp_twist_loc",twistpos,twistrot,twistroo)
                    cons1 = mocaphelperarbcore.createParentConstraint(twistref,twistloc,True)
                    cons2 = mocaphelperarbcore.createPointConstraint(twistloc,twist,False)
                    if smartbake:
                        mocaphelperarbcore.smartbake(twist,mintime,maxtime,"point")
                    else:
                        mocaphelperarbcore.bake(twist,mintime,maxtime,"point")
                        
                    mocaphelperutility.deleteObj(cons1)
                    mocaphelperutility.deleteObj(cons2)
                    mocaphelperutility.deleteObj(twistloc)

        finally:
            mocaphelperutility.closeUndoChunk()

    def on_arb_pinPosPinCurButtonClicked(self):
        mintime = self.arb_fromtime
        maxtime = self.arb_totime
        mocaphelperutility.openUndoChunk()
        try:

            objs = mocaphelperutility.getSelectedNodes()
            mocaphelperarbcore.pinCurPos(objs,mintime,maxtime)
        finally:
            mocaphelperutility.closeUndoChunk()

    def on_arb_pinPosPinParentButtonClicked(self):
        mintime = self.arb_fromtime
        maxtime = self.arb_totime
        mocaphelperutility.openUndoChunk()
        try:
            objs = mocaphelperutility.getSelectedNodes()
            mocaphelperarbcore.pinParentPos(objs,mintime,maxtime)
        finally:
            mocaphelperutility.closeUndoChunk()
        


def getArbType(obj):
    index = obj.ui.arb_simpleBakeTypeComboBox.currentIndex()
    # type = mocaphelperutility.unicodeToStr(type)
    # enList = ["all","parent","point","orient","onlyscale"]
    # cnList = ["平移旋转","平移","旋转","所有属性"]
    type = None
    if index == 0:
        type = "all"

    elif index == 1:
        type = "parent"

    elif index == 2:
        type = "point"

    elif index == 3:
        type = "orient"

    else:
        raise Exception("id out of range")
    print("index is now:",index,".type is now:",type)

    return type


def getReActOnType(obj):
    index = obj.ui.re_actTypeComboBox.currentIndex()

    type = None
    if index == 0:
        type = "all"

    elif index == 1:
        type = "nurbsCurve"



    print("index is now:",index,".type is now:",type)
    return type