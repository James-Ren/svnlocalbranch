# svnlocalbranch
Auto export and import SVN modified files and reverted

现在主流的代码版本控制工具都用git，而我们公司因为历史原因依然使用SVN管理代码，而SVN的分支管理能力很弱，我们一般都不用，有时候会遇到在做任务时候需要修改一个bug，或者，需要对代码进行一些备份。
正好学习python，就用他写了一个小工具，用来导出导入代码的未修改部分。可以用于保存任务，也可以作为临时性还原工具。
主要原理：
导出：
1. 列出svn项目中所有修改未提交的文件，写入svnchange.txt,以供筛选。
2. 在svnchange.txt中选出需要的文件，删除不需要打包的文件
3. 继续下一步，打包出对应文件复制到pybranch目录中，还原选中文件，并将各个文件的版本号记录在svn.json后用。
还原分支到项目：
1. 选择要还原的分支目录
2. 比较文件的版本和现在系统的版本，没有更新就自动覆盖
3. 如果更新了文件，则先将文件还原到原版本，覆盖，然后重新update，如果有冲突，自己修改解决冲突。
使用前需要配置config.json 输入导出目录的信息。包括本地的SVN工程目录，svn用户名和密码。

我还打包了exe方便组员使用。就在dist目录下。
这个需要svn命令行工具支持，如果没有可以到如下地址下载安装：
[https://www.visualsvn.com/files/Apache-Subversion-1.9.7.zip](https://www.visualsvn.com/files/Apache-Subversion-1.9.7.zip)
