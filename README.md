# MotionCapHelper
 maya simple plugin for animator

安装：
将这个文件夹的目录添加到到对应版本的maya.env文件中的MAYA_PLUG_IN_PATH这一行。
例子：
MAYA_PLUG_IN_PATH =C:\Users\（你的用户名）\Documents\maya\2018\plug-ins\MotionCapHelper

启动maya，在maya里打开插件管理器，如果出现了这个插件的名字mocaphelper.py就说明安装
顺利，只要勾选这一个文件的加载就好，不需要勾选其他的比如mocaphelperrecore.py等等文件

勾选后maya会载入插件，之后使用mel或者python的moCapHelper_showUi -lan "CN"指令打开插件的中文界面
或者moCapHelper_showUi打开英文界面（更推荐一点，因为懒得更新汉化）
可以把这个指令新建一个工具架的工具，方面后面调用

Installation:
Add the directory of this folder to the <MAYA_PLUG_IN_PATH> in the corresponding version of the maya.env file.
Example:
MAYA_PLUG_IN_PATH =C:\Users\<username>\Documents\maya\2018\plug-ins\MotionCapHelper

Start Maya, open the plugin manager in Maya, you should see a list of mocaphelper.py/mocaphelperui.py.....
 just check the load state of "mocaphelper.py" file only, no need to check any other files such as mocaphelperrecore.py....

After checking this box, maya will load the plug-in, and then you can use "moCapHelper_showUi" command in mel or python to open the interface of this plug-in.

You can create a new shelf tool with this command.