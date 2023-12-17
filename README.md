# MotionCapHelper
 maya simple plugin for animator

Installation:
Add the directory of this folder to the <MAYA_PLUG_IN_PATH> in the corresponding version of the maya.env file.
Example:
MAYA_PLUG_IN_PATH =C:\Users\<username>\Documents\maya\2018\plug-ins\MotionCapHelper

Start Maya, open the plugin manager in Maya, you should see a list of mocaphelper.py/mocaphelperui.py.....
 just check the load state of "mocaphelper.py" file only, no need to check any other files such as mocaphelperrecore.py....

After checking this box, maya will load the plug-in, and then you can use "moCapHelper_showUi" command in mel or python to open the interface of this plug-in.

You can create a new shelf tool with this command.