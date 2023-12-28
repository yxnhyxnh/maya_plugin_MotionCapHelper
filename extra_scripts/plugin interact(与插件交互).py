'''
this is an example of how you set hotkey or use scripts to drive this plugin's cmds.
if you know python and pyside2,go see codes and .ui file to find what you need.
the most simple usage is to drive a qt pushbutton.(which is exactly what you did when you hit a button in plugin ui.)
and you might need QLineEdit.setText() to set str in those text field.
anyway,go check qt wiki :https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QWidget.html#qwidget
have fun scripting.
'''

import maya.cmds as cmds

cmds.moCapHelper_eval(s ="ui.arb_stickyDelButton.click()" )