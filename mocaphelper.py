# -*- coding: utf-8 -*-
'''
author:crx

this plugin is created for use with autodesk maya 2018+.
(because it import pyside2 module,and i don't know in which version maya would update this.)

-----------------------------
HOW TO USE:
smoothAniCurve is supposed to be used with graph editor in maya,and you must only create an unique one,because plugin uses 
"cmds.animCurveEditor("graphEditor1GraphEd",query = True,areCurvesSelected = True)" to get anim curves.
and you have to select keys or anim curves to use it.
the rest arguments are pretty easy to understand.
and,this core feature is not developed by me,i actually stole it from:https://blog.csdn.net/lulongfei172006/article/details/51493273/
thank you,lulongfei172006.

frameAlign is simple cmd that you set a refence obj to get "frame time list" first,and apply that list to any objs that you selected while pushing that button.
it will set key on  "frame time list"  first,and delete other keys that are not in the list.

mocaphelperui is accessable by cmds.moCapHelper.showUi()
or use it with mel:moCapHelper.showUi;

hope you enjoy it.

'''



import sys

import maya.api.OpenMaya as om
import mocaphelperui
import mocaphelpersaccore
import mocaphelperfacore
import mocaphelperutility

import PySide2.QtWidgets

from PySide2 import QtCore


version = 1.42
ui = None

translator = QtCore.QTranslator()



def maya_useNewAPI():
	"""
	The presence of this function tells Maya that the plugin produces, and
	expects to be passed, objects created using the Maya Python API 2.0.
	"""
	pass

# Initialize the plug-in
def initializePlugin(plugin):
	pluginFn = om.MFnPlugin(plugin)
	try:
		pluginFn.registerCommand(
			mocaphelpersaccore.SmoothAnimCurve.kPluginCmdName, mocaphelpersaccore.SmoothAnimCurve.cmdCreator,mocaphelpersaccore.syntaxCreator
		)

	except:
		sys.stderr.write(
			"Failed to register command: %s\n" % mocaphelpersaccore.SmoothAnimCurve.kPluginCmdName
		)
		raise

	try:
		pluginFn.registerCommand(
			openui.kPluginCmdName, openui.cmdCreator,openuiSyntaxCreator
		)
	except:
		sys.stderr.write(
			"Failed to register command: %s\n" % openui.kPluginCmdName
		)
		raise

	try:
		pluginFn.registerCommand(
			mocaphelperfacore.FrameAlign.kPluginCmdName, mocaphelperfacore.FrameAlign.cmdCreator,mocaphelperfacore.syntaxCreator
		)
	except:
		sys.stderr.write(
			"Failed to register command: %s\n" % mocaphelperfacore.FrameAlign.kPluginCmdName
		)
		raise

	try:
		pluginFn.registerCommand(
			Eval.kPluginCmdName, Eval.cmdCreator,evalSyntaxCreator
		)
	except:
		sys.stderr.write(
			"Failed to register command: %s\n" % Eval.kPluginCmdName
		)
		raise



# Uninitialize the plug-in
def uninitializePlugin(plugin):
	pluginFn = om.MFnPlugin(plugin)
	try:
		pluginFn.deregisterCommand(mocaphelpersaccore.SmoothAnimCurve.kPluginCmdName)
	except:
		sys.stderr.write(
			"Failed to unregister command: %s\n" % mocaphelpersaccore.SmoothAnimCurve.kPluginCmdName
		)
		raise
	try:
		pluginFn.deregisterCommand(openui.kPluginCmdName)
	except:
		sys.stderr.write(
			"Failed to unregister command: %s\n" % openui.kPluginCmdName
		)
		raise


	try:
		pluginFn.deregisterCommand(mocaphelperfacore.FrameAlign.kPluginCmdName)
	except:
		sys.stderr.write(
			"Failed to unregister command: %s\n" % mocaphelperfacore.FrameAlign.kPluginCmdName
		)
		raise

	try:
		pluginFn.deregisterCommand(Eval.kPluginCmdName)
	except:
		sys.stderr.write(
			"Failed to unregister command: %s\n" % Eval.kPluginCmdName
		)
		raise


# command


class openui(om.MPxCommand):

	kPluginCmdName = "moCapHelper_showUi"

	uiLanguageFlagShortName = "lan"
	uiLanguageFlagLongName = "language"
	lang = None
	def __init__(self):
		om.MPxCommand.__init__(self)

	@staticmethod
	def cmdCreator():
		return openui()

	def parseArguments(self,args):
		argdata = om.MArgParser(self.syntax(),args)

		if argdata.isFlagSet( self.uiLanguageFlagShortName ):
			self.lang = argdata.flagArgumentString(self.uiLanguageFlagShortName,0)
		else:
			self.lang = None

		

	def doIt(self, args):
		self.parseArguments(args)
		global ui
		if ui != None:
			print("saved ui ref:",ui)
			print("closing ui:--------",ui.destroy(True,True))

		
		app = PySide2.QtWidgets.QApplication.instance()

		app.installTranslator(translator)
		dir = mocaphelperutility.getDir()
		# translate:
		if self.lang == "CN":
			

			
			translator.load("ui_CN",dir)
			ui = mocaphelperui.MoCapHelperUI()
			ui.setWindowTitle('动补助手 v'+str(version))
			# print(translator.filePath())
			# print(translator.translate())

			# mocaphelperui.translateUi(ui.ui,ui.ui)
		else:
			translator.load("")
			ui = mocaphelperui.MoCapHelperUI()

		ui.show()
		



def openuiSyntaxCreator():

    syntax = om.MSyntax()
    
    syntax.addFlag( openui.uiLanguageFlagShortName, openui.uiLanguageFlagLongName, om.MSyntax.kString )

        
    return syntax



class Eval(om.MPxCommand):

	kPluginCmdName = "moCapHelper_eval"

	strFlagShortName = "s"
	strFlagLongName = "string"
	cmd = ""

	def __init__(self):
		om.MPxCommand.__init__(self)



	def parseArguments(self,args):
		argdata = om.MArgParser(self.syntax(),args)

		if argdata.isFlagSet( self.strFlagShortName ):
			self.cmd = argdata.flagArgumentString(self.strFlagShortName,0)
		else:
			raise Exception("no str input")


	@staticmethod
	def cmdCreator():
		
		return Eval()


	def doIt(self, args):
		self.parseArguments(args)
		print(self.cmd)
		global ui
		if ui != None:
			exec(self.cmd)
		else:
			raise Exception("please create ui first.")
		

def evalSyntaxCreator():

    syntax = om.MSyntax()
    
    syntax.addFlag( Eval.strFlagShortName, Eval.strFlagLongName, om.MSyntax.kString )

        
    return syntax

