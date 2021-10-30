# 小白常见问题Q&A
### Q:我完全没学过代码能用这个脚本吗？
### A:完全没问题，英语不要太差，善用百度能解决大部分问题。
***
## 1.运行pip intall指令时的常见问题
### Q:在cmd中运行pip install指令时跳出黄字警告怎么办？
### A:这个是正常现象不需要管。
### Q:在cmd中运行pip install指令时出现一长串的红色字符怎么办？
### A：说明下载失败了，尝试多运行几次pip install指令，直到全部显示Requirement already satisfied既可。
### Q：这些东西下载来有什么用？
### A：这些是脚本运行时的依赖库，不可或缺。
### Q: 在cmd中运行pip install指令时显示 'pip' 不是内部或外部命令，也不是可运行的程序或批处理文件是为什么？
### A：说明你没安装Python，可以直接百度python官网或者去微软商店里面下载。
### Q: psutil依赖包下载完成后显示安装失败了,重试了好几次还是一样是为什么？
### A: 说明你安装的Python版本过高，可以下载[Micsoft Visaul C++](https://download.visualstudio.microsoft.com/download/pr/d3cbdace-2bb8-4dc5-a326-2c1c0f1ad5ae/9B9DD72C27AB1DB081DE56BB7B73BEE9A00F60D14ED8E6FDE45DAB3E619B5F04/VC_redist.x64.exe)后再次运行指令即可,也可以直接重新安装旧版的Python 3.7 或者Python 3.8
***
## 2.安装相关软件的注意事项
### Q: 安装Python时有什么要注意的？
### A: 如果没有特殊需求强烈建议安装Python 3.7或者Python 3.8版本，建议使用微软商店或者去Python官网下载安装。
### Q: 安装[Anaconda3](https://www.anaconda.com/products/individual#windows)时有什么需要注意的？
### A: 安装时请仔细看清每一步，确保在Advanced Options界面时勾选Add Anaconda3 to the system PATH environment variable选项（该选项默认是不勾选的）以确保脚本的正常运行。
***
## 3.如何运行脚本的相关问题
### Q: 上面的这些步骤我已经全部完成了，脚本压缩包也下载并解压好了，为什么我双击lushi.py没有任何反应？
### A： lushi.py没有办法直接运行，需要通过cmd启动，在cmd中通过python lushi.py指令启动启动脚本前，需要先将cmd CD到lushi.py所在路径，具体的操作方法为在cmd中输入CD加空格加lushi.py所在路径，详细可参照[命令提示符——CMD目录操作——cd命令](https://jingyan.baidu.com/article/73c3ce28480637e50343d992.html)。
### Q: 成功启动脚本后该如何设置脚本？
### A: 脚本的设置文件是config_chs.yaml和config_eng.yaml这两个文件，根据你炉石客户端的语言设置对应的配置文件即可。
