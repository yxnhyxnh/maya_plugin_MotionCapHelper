import datetime
import getpass
import glob
import os
import shutil
import subprocess

import maya.cmds as cmds
import maya.mel as mel


PREV_DIR_ENV = "Mocaphelper_Playblast_Path"





def get_prev_path():
    if cmds.optionVar(exists=PREV_DIR_ENV):
        return cmds.optionVar(q=PREV_DIR_ENV)
    else:
        return None

def set_prev_path(dir_path):
    cmds.optionVar(sv=(PREV_DIR_ENV, dir_path))


def getMagicMaskNode():
    magic_mask_nodes = cmds.ls(type='magicMask')
    if magic_mask_nodes == None:
        return None
    else:
        return magic_mask_nodes[0]
    

def resetHUD():
    mel.eval('source "initHUD";')


def removeHUD():
    default_hud_list = cmds.headsUpDisplay(lh=True)
    if default_hud_list:
        for default_hud in default_hud_list:
            cmds.headsUpDisplay(default_hud, rem=True)



    # cmds.setAttr('%s.displayFilmGate' % main_cam, 0)
    # cmds.setAttr('%s.displayResolution' % main_cam, 0)


def moCapHelper_Playblast(cam,filepath,offscreen):
    pass