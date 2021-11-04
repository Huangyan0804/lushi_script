# -*- coding: utf-8 -*-
import base64
import json
import os
import sys

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import *

if sys.executable.endswith("pythonw.exe"):
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.path.join(os.getenv("TEMP"), "stderr-" + os.path.basename(sys.argv[0])), "w")


class DropLineEdit(QLineEdit):  # support drag
    def __init__(self, parent=None):
        super(DropLineEdit, self).__init__(parent)
        # self.setAcceptDrops(True)
        self.setDragEnabled(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        if e.mimeData().hasText():
            file_path = e.mimeData().text()
            file_path = file_path.split('\n')
            # print(filePath[0])  # only read the first file
            file_path = file_path[0].split('///')  # remove file:///
            self.setText(file_path[1])  # save file path into QLineEdit
        else:
            e.ignore()


class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main.ui', self)

        self.save = self.findChild(QPushButton, 'Save')  # Find the button
        self.save.clicked.connect(self.saveButtonPressed)  # Click event

        self.run = self.findChild(QPushButton, 'Run')
        self.run.clicked.connect(self.runButtonPressed)
        self.help = self.findChild(QPushButton, 'Help')
        self.help.clicked.connect(self.helpButtonPressed)

        with open('main.ui', 'r') as f:
            ui_xml = f.read().replace('\n', "")

        self.log = self.findChild(QLineEdit, 'hs_log')
        self.bn = self.findChild(QLineEdit, 'bn_path')
        self.language = self.findChild(QSpinBox, 'language')
        self.team_id = self.findChild(QSpinBox, 'team_id')
        self.boss_id = self.findChild(QSpinBox, "boss_id")
        self.hero_count = self.findChild(QSpinBox, "hero_count")
        self.reward_count = self.findChild(QSpinBox, "reward_count")
        self.delay = self.findChild(QDoubleSpinBox, "delay")
        self.confidence = self.findChild(QDoubleSpinBox, "confidence")
        self.longest_waiting = self.findChild(QSpinBox, "longest_waiting")
        self.early_stop = self.findChild(QCheckBox, "early_stop")
        self.auto_restart = self.findChild(QCheckBox, "auto_restart")

        self.load_config()

        self.show()

    def helpButtonPressed(self):
        help_text_eng = '''Run with the GUI, the config will covers the basic part of config.yaml,
                            and the other config still read config.yaml
                            language: Hearthstone Language. 0 means English, the others are Chinese simplified

                            team_id: number of your team ID for battle, start counting from 0
                            boss_id: number of the boss ID for battle, start counting from 0
                            hero_count: Number of mercenaries in the team, at least 3
                            reward_count: total number of rewards after finishing the map
                            early_stop: whether early stop battle once collected surprise option on map
                            delay: delay between consecutive operations, if you always missing clicking some button, 
                            you may need to change the delay to > 1.0.
                            confidence: confidence threshold for image template matching on screen
                            longest_waiting: longest_waiting time to restart Hearthstone
                            bn_path: Battle.net.exe path. Support drag.
                            hs_log: Path of Power.log. Support drag.
                            auto_restart: enable auto restart Hearthstone
                            '''.strip().replace('  ', '')
        help_text_chs = '''通过GUI运行，配置覆盖config.yaml的basic部分，其余配置仍读取config.yaml
                            language: 0是英文模式，其他选项均为中文。

                            team_id: 出战队伍的编号, 从0开始计数
                            boss_id: 目标悬赏的编号, 从0开始计数
                            hero_count: 队伍中佣兵的数量，至少3人
                            reward_count: 完成悬赏后的奖励数目
                            early_stop: 在拿到神秘选项后是否提前结束战斗
                            delay: 连续操作之间的延迟, 如果脚本经常少点某些按钮, 你可能需要增加延迟使delay > 1.0
                            confidence: 屏幕上图像模板匹配的置信阈值
                            longest_waiting: 如果界面卡住，最多等多少秒重启炉石
                            
                            bn_path: 战网路径。支持拖拽Battle.net.exe获取路径
                            hs_log: 炉石日志路径(在炉石游戏的安装目录里找Logs/Power.log)支持拖拽Power.log获取路径
                            
                            auto_restart: 遇到，掉线等是否自动重启
                            '''.strip().replace('  ', '')
        QMessageBox.information(self, 'Help', help_text_eng, QMessageBox.Ok, QMessageBox.Ok)
        QMessageBox.information(self, '帮助', help_text_chs, QMessageBox.Ok, QMessageBox.Ok)

    def load_config(self):
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config = f.read()
            config = json.loads(config)
            print(config)
            self.log.setText(config['hs_log'])
            self.bn.setText(config['bn_path'])
            self.team_id.setValue(config['team_id'])
            self.boss_id.setValue(config['boss_id'])
            self.hero_count.setValue(config['hero_count'])
            self.reward_count.setValue(config['reward_count'])
            self.delay.setValue(config['delay'])
            self.confidence.setValue(config['confidence'])
            self.longest_waiting.setValue(config['longest_waiting'])
            self.language.setValue(config['language'])
            self.auto_restart.setChecked(config['auto_restart'])
            self.early_stop.setChecked(config['early_stop'])
        except:
            pass

    def update_config(self):
        basic_config = {
            'hs_log': self.log.text(),
            'bn_path': self.bn.text(),
            'early_stop': int(self.early_stop.isChecked()),
            'auto_restart': int(self.auto_restart.isChecked()),

            'pvp_delay': 0.5,
            'fast_surrender': 0,
            'mode': 'pve',

            'team_id': self.team_id.value(),
            'boss_id': self.boss_id.value(),
            'hero_count': self.hero_count.value(),
            'reward_count': self.reward_count.value(),
            'delay': self.delay.value(),
            'confidence': self.confidence.value(),
            'longest_waiting': self.longest_waiting.value()
        }
        return basic_config

    def saveButtonPressed(self):
        # This is executed when the button is pressed
        res = self.update_config()
        res['language'] = self.language.value()
        print(self.update_config())
        with open('config.json', 'w', encoding='utf-8') as f:
            f.writelines(json.dumps(res, sort_keys=True, indent=4, separators=(',', ':')) + '\n')

    def runButtonPressed(self):
        basic_config = self.update_config()
        lang = 'chs' if self.language.value() else 'eng'

        basic_arg = base64.b64encode(json.dumps(basic_config).encode('utf-8')).decode('utf-8')
        sys.exit(os.system(f'start cmd /K python lushi.py --lang {lang} --basic {basic_arg}'))


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())
