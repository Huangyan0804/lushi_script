# Hearthstone Mercenaries Mode Script


## Introduction
This script is to save your time from Mercenaries mode of Hearthstone. 

It is only for study purpose, you will take your own legal responsibility if you commercialize it or earn profit.

For discussion, welcome to our QQ Group: 832946624

For bug reporting, please go to [Issues](https://github.com/zhoubin-me/lushi_script/issues) page to submit

## Installation

Make sure you installed python>=3.6.
To install python, we recommand [Anaconda](https://www.anaconda.com/products/individual#windows).
Make sure you added python path into your ```$PATH``` system environment/variables

Run the following in your commandline/terminal for **Requirements** installation
```bash
pip install opencv-python numpy pyautogui pillow pywin32 pyyaml psutil
```
For Mac OS users:
```bash
pip install opencv-python numpy pyautogui pillow pywin32 pyyaml psutil PyCocoa
```
## Run
If you need a stable version, goto Release to download.
If you wanna test latest version, download the main branch.

In your commandline/terminal, ```cd``` to folder where ```lushi.py``` locates,  run the following
```bash
python lushi.py 
```

## Caution
- Currently only support **Simplified Chinese**, make sure your Hearthstone language is set to this
- Make sure your Hearthstone is set to **windows mode, high graphic quality and 1600x900 resolution**
- For more resolutions, change locations in ```config.yaml```, use ```find_coordinates.py``` to record button locations;
- Please read carefully about **basic section and skill section** in  ```conig.yaml``` before you start your game
- If you wanna blacklist some treasures during selection, put their screenshot into ```treasure_blacklist``` folder
- If you wanna whitelist some heros during stranger reward selection, put their screenshot into ```heros_whitelist``` folder, ***BUT*** DO NOT copy the whole card image, only charactor avatar, otherwise may not recognize
- If you wanna run it in background, consider using a virtual machine
- Please download to **lastest stable** version in release page, if you still have problems, please report on issues page