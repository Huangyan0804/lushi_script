# -*- coding: utf-8 -*-
import os
import re
import sys

import PyQt5
import pinyin
import yaml
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtCore import QStringListModel, QThread, pyqtSignal
from PyQt5.QtWidgets import *

from utils.util import HEROS

if sys.executable.endswith("pythonw.exe"):
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.path.join(os.getenv("TEMP"), "stderr-" + os.path.basename(sys.argv[0])), "w")

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Thread_2(QThread):  
    _signal =pyqtSignal()
    def __init__(self,config):
        super().__init__()
        self.config = config
    def run(self):
        from lushi import run_from_gui
        run_from_gui(self.config)
        self._signal.emit()
        
class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ui/main_chs.ui', self)

        self.trans = QtCore.QTranslator()
        if __import__('locale').getdefaultlocale()[0] == 'zh_CN':
            self.ui_lang = 'chs'
        else:
            self.ui_lang = 'eng'

        self.boss_id = self.findChild(QSpinBox, 'boss_level')
        self.team_id = self.findChild(QSpinBox, 'team_id')
        self.reward_count = self.findChild(QSpinBox, 'boss_reward')
        self.bn_path = self.findChild(QLineEdit, 'bn_path')
        self.hs_path = self.findChild(QLineEdit, 'hs_path')
        self.bn_path_find = self.findChild(QToolButton, 'load_path')
        self.bn_path_find.clicked.connect(self.on_load_path_click_bn)
        self.hs_path_find = self.findChild(QToolButton, 'load_path2')
        self.hs_path_find.clicked.connect(self.on_load_path_click_hs)
        self.lang_dropdown = self.findChild(QComboBox, 'lang')
        self.lang_dropdown.addItem('EN-1024x768')
        self.lang_dropdown.addItem('ZH-1600x900')
        self.current_order = self.findChild(QLabel, 'current_order')

        self.save = self.findChild(QPushButton, 'save')  # Find the button
        self.save.clicked.connect(self.saveButtonPressed)  # Click event
        self.run = self.findChild(QPushButton, 'run')  # Find the button
        self.run.clicked.connect(self.runButtonPressed)  # Click event
        self.load = self.findChild(QPushButton, 'load')  # Find the button
        self.load.clicked.connect(self.loadButtonPressed)  # Click event

        self.hero_dropdown = self.findChild(QComboBox, 'hero_list')
        if self.ui_lang == 'chs':
            heros_sorted = {k: v[0] for k, v in sorted(
                HEROS.items(), key=lambda item: pinyin.get(item[1][0], format="strip", delimiter=""))}
            for k, v in heros_sorted.items():
                self.hero_dropdown.addItem(v)
        elif self.ui_lang == 'eng':
            heros_sorted = {k: v[1] for k, v in sorted(HEROS.items(), key=lambda item: item[1][1])}
            for k, v in heros_sorted.items():
                self.hero_dropdown.addItem(v)

        self.hero_list = self.findChild(QListView, 'heros')
        self.slm = QStringListModel([])
        self.hero_list.setModel(self.slm)
        self.hero_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.hero_list.clicked.connect(self.on_hero_clicked)
        self.hero_index = -1

        self.add = self.findChild(QPushButton, 'add')
        self.add.clicked.connect(self.addButtonPressed)  # Click event
        self.delete = self.findChild(QPushButton, 'del_1')
        self.delete.clicked.connect(self.delButtonPressed)  # Click event
        self.go_up = self.findChild(QPushButton, 'goup')
        self.go_up.clicked.connect(self.upButtonPressed)  # Click event
        self.delete = self.findChild(QPushButton, 'godown')
        self.delete.clicked.connect(self.downButtonPressed)  # Click event
        self.modify = self.findChild(QPushButton, 'modify')
        self.modify.clicked.connect(self.modifyButtonPressed)  # Click event

        self.radio_buttons = []
        for radio_text in ['321', '312', '213', '231', '123', '132']:
            radio = self.findChild(QRadioButton, f'r{radio_text}')
            radio.toggled.connect(self.on_radio_click)
            self.radio_buttons.append(radio)

        self.auto_restart = self.findChild(QCheckBox, 'auto_restart')
        self.early_stop = self.findChild(QCheckBox, 'early_stop')

        self.action_eng = self.findChild(QAction, 'actionEnglish')
        self.action_eng.triggered.connect(self.tiggerEnglish)
        self.action_chs = self.findChild(QAction, 'actionChinese')
        self.action_chs.triggered.connect(self.triggerChinese)

        self.spell_order = "1, 2, 3"
        self.bn_path_str = ""
        self.hs_path_str = ""
        self.hero_info = {}
        self.config = {}
        self.load_config('config/default.yaml')
        self.show()

        if self.ui_lang == 'eng':
            self.tiggerEnglish()

    def tiggerEnglish(self):
        # load qm file
        self.trans.load("ui/main_eng")
        # get app instance and load trans
        QApplication.instance().installTranslator(self.trans)
        # translate
        self.retranslateUi()
        self.show()
        self.ui_lang = 'eng'
        hero_ordered = {k_: v_ for k_, v_ in sorted(self.hero_info.items(), key=lambda item: item[1][-1])}
        str_list = []
        for k, v in hero_ordered.items():
            if len(re.findall(r'[\u4e00-\u9fff]+', v[0])) > 0:
                self.hero_info[k] = [v[1], v[0], v[2], v[3]]
                str_list.append(v[1])
        if len(str_list) > 0:
            self.slm.setStringList(str_list)

        self.hero_dropdown.clear()
        heros_sorted = {k: v[1] for k, v in sorted(HEROS.items(), key=lambda item: item[1][1])}
        for k, v in heros_sorted.items():
            self.hero_dropdown.addItem(v)

    def triggerChinese(self):
        self.trans.load("ui/main_chs")
        # get app instance and load trans
        QApplication.instance().installTranslator(self.trans)
        # translate
        self.retranslateUi()
        self.show()
        self.ui_lang = 'chs'
        hero_ordered = {k_: v_ for k_, v_ in sorted(self.hero_info.items(), key=lambda item: item[1][1])}
        str_list = []
        for k, v in hero_ordered.items():
            if len(re.findall(r'[\u4e00-\u9fff]+', v[0])) == 0:
                self.hero_info[k] = [v[1], v[0], v[2], v[3]]
                str_list.append(v[1])
        if len(str_list) > 0:
            self.slm.setStringList(str_list)

        self.hero_dropdown.clear()
        heros_sorted = {k: v[0] for k, v in sorted(
            HEROS.items(), key=lambda item: pinyin.get(item[1][0], format="strip", delimiter=""))}

        for k, v in heros_sorted.items():
            self.hero_dropdown.addItem(v)

    def loadButtonPressed(self):
        load_path = QtWidgets.QFileDialog.getOpenFileName(self, "Load Config", "", "YAML Config(*.yaml)")[0]
        if load_path == '':
            load_path = 'config/default.yaml'
        self.load_config(load_path)

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_hero_clicked(self, index):
        self.hero_index = index.row()
        str_list = self.slm.stringList()
        if 0 <= self.hero_index < len(str_list):
            name = str_list[self.hero_index]
            for k, v in self.hero_info.items():
                if v[0] == name:
                    self.current_order.setText(self.hero_info[k][2])
                    break

    def on_load_path_click_hs(self):
        self.hs_path_str = QtWidgets.QFileDialog.getOpenFileName(self, 'Find Path of Hearthstone.exe')[0]
        if len(self.hs_path_str) > 0:
            self.hs_path.setText(self.hs_path_str)

    def on_load_path_click_bn(self):
        self.bn_path_str = QtWidgets.QFileDialog.getOpenFileName(self, 'Find Path of Battle.net.exe')[0]
        if len(self.bn_path_str) > 0:
            self.bn_path.setText(self.bn_path_str)

    def on_radio_click(self):
        bt = self.sender()
        if bt.isChecked():
            self.spell_order = bt.text()

    def upButtonPressed(self):
        str_list = self.slm.stringList()
        if 1 <= self.hero_index < len(str_list):
            str_list[self.hero_index], str_list[self.hero_index - 1] = str_list[self.hero_index - 1], str_list[
                self.hero_index]
            self.slm.setStringList(str_list)

    def downButtonPressed(self):
        str_list = self.slm.stringList()
        if 0 <= self.hero_index < len(str_list) - 1:
            str_list[self.hero_index], str_list[self.hero_index + 1] = str_list[self.hero_index + 1], str_list[
                self.hero_index]
            self.slm.setStringList(str_list)

    def delButtonPressed(self):
        str_list = self.slm.stringList()
        if 0 <= self.hero_index < len(str_list):
            name = str_list.pop(self.hero_index)
            self.slm.setStringList(str_list)
            for k, v in self.hero_info.items():
                if v[0] == name:
                    del self.hero_info[k]
                    break

    def modifyButtonPressed(self):
        str_list = self.slm.stringList()
        if 0 <= self.hero_index < len(str_list):
            name = str_list[self.hero_index]
            for k, v in self.hero_info.items():
                if v[0] == name:
                    self.hero_info[k][2] = self.spell_order
                    self.current_order.setText(self.spell_order)
                    break

    def addButtonPressed(self):
        str_list = self.slm.stringList()
        if self.hero_dropdown.currentText() not in str_list and len(str_list) < 6:
            str_list.append(self.hero_dropdown.currentText())
            if self.ui_lang == 'eng':
                kv = [(k, v[0], v[1]) for k, v in HEROS.items() if v[1] == self.hero_dropdown.currentText()]
            else:
                kv = [(k, v[0], v[1]) for k, v in HEROS.items() if v[0] == self.hero_dropdown.currentText()]
            idx, name_chs, name_eng = kv[0]
            index = len(str_list) - 1
            if self.ui_lang == 'chs':
                self.hero_info[idx] = [name_chs, name_eng, self.spell_order, index]
            elif self.ui_lang == 'eng':
                self.hero_info[idx] = [name_eng, name_chs, self.spell_order, index]
            self.slm.setStringList(str_list)

    def load_config(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        except:
            return QMessageBox.critical(self, 'Error!', "Load Path Fail", QMessageBox.Ok, QMessageBox.Ok)

        for k, v in self.config.items():
            if k == 'boss_id':
                self.boss_id.setValue(v + 1)
            if k == 'team_id':
                self.team_id.setValue(v + 1)
            if k == 'reward_count':
                self.reward_count.setValue(v)
            if k == 'bn_path':
                self.bn_path.setText(v)
            if k == 'hs_path':
                self.hs_path.setText(v)
            if k == 'auto_restart':
                self.auto_restart.setChecked(v)
            if k == 'early_stop':
                self.early_stop.setChecked(v)
            if k == 'lang':
                self.lang.setCurrentText(v)
            if k == 'ui_lang':
                self.ui_lang = v
                if v == 'chs':
                    self.triggerChinese()
                elif v == 'eng':
                    self.tiggerEnglish()
            if k == 'hero':
                hero_ordered = {k_: v_ for k_, v_ in sorted(v.items(), key=lambda item: item[1][-1])}
                self.hero_info = {}
                for k, v in hero_ordered.items():
                    self.hero_info[k] = [v[0], v[1], v[2], v[3]]
                str_list = [v[0] for k, v in hero_ordered.items()]
                self.slm.setStringList(str_list)

    def save_config(self):
        self.config['boss_id'] = self.boss_id.value() - 1
        self.config['team_id'] = self.team_id.value() - 1
        self.config['reward_count'] = self.reward_count.value()
        self.config['bn_path'] = self.bn_path.text()
        self.config['hs_path'] = self.hs_path.text()
        self.config['auto_restart'] = self.auto_restart.isChecked()
        self.config['early_stop'] = self.early_stop.isChecked()
        self.config['lang'] = self.lang.currentText()
        self.config['delay'] = 0.5
        self.config['confidence'] = 0.8
        self.config['longest_waiting'] = 80
        self.config['ui_lang'] = self.ui_lang
        new_hero_info = {}
        hero_order_list = self.slm.stringList()
        for k, v in self.hero_info.items():
            hero_index = hero_order_list.index(v[0])
            new_hero_info[k] = [v[0], v[1], v[2], hero_index]
        self.config['hero'] = new_hero_info

    def saveButtonPressed(self):
        self.save_config()
        save_path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save To', "", "YAML Config (*.yaml)")[0]
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f)
            print(self.config)
        except:
            return QMessageBox.critical(self, 'Error!', "Save Path Fail", QMessageBox.Ok, QMessageBox.Ok)

    def runButtonPressed(self):
        hero_text = ""
        for k, v in self.hero_info.items():
            hero_text += f"\t{v[0]}:\t{v[2]}\n"

        cfm_text = f'''
            Current Setting:\n
            Boss ID: {self.config['boss_id'] + 1}\n
            Team ID: {self.config['team_id'] + 1}\n
            Boss Reward: {self.config['reward_count']}\n
            BattleNet Path: {self.config['bn_path']}\n
            HearthStone Path: {self.config['hs_path']}\n
            Auto Restart: {self.config['auto_restart']}\n
            Early Stop: {self.config['early_stop']}\n
            Language & Resolution: {self.config['lang']}\n
            Heroes:\n
            {hero_text}
        '''.strip().replace('    ', '')

        reply = QMessageBox.question(self, 'CONFIRM', cfm_text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            
            self.save_config()
            self.thread_2 =Thread_2(self.config)
            self.thread_2.start()
        else:
            pass

    def retranslateUi(self):  # generate from python -m PyQt5.uic.pyuic main_chs.ui -o main_chs_ui.py
        _translate = QtCore.QCoreApplication.translate
        # MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "关卡选择序号"))
        self.label_4.setText(_translate("MainWindow", "战网路径"))
        self.load_path.setText(_translate("MainWindow", "..."))
        self.label_2.setText(_translate("MainWindow", "队伍选择序号"))
        self.label_5.setText(_translate("MainWindow", "炉石路径"))
        self.load_path2.setText(_translate("MainWindow", "..."))
        self.label_3.setText(_translate("MainWindow", "关卡奖励数量"))
        self.label_8.setText(_translate("MainWindow", "语言与分辨率"))
        self.early_stop.setText(_translate("MainWindow", "拿完惊喜提前结束"))
        self.auto_restart.setText(_translate("MainWindow", "脚本宕机自动重启"))
        self.label_7.setText(_translate("MainWindow", "下拉选择添加英雄"))
        self.skill_order.setTitle(_translate("MainWindow", "技能释放顺序"))  # cannot translate
        self.r321.setText(_translate("MainWindow", "3, 2, 1"))
        self.r312.setText(_translate("MainWindow", "3, 1, 2"))
        self.r213.setText(_translate("MainWindow", "2, 1, 3"))
        self.r231.setText(_translate("MainWindow", "2, 3, 1"))
        self.r123.setText(_translate("MainWindow", "1, 2, 3"))
        self.r132.setText(_translate("MainWindow", "1, 3, 2"))
        self.add.setText(_translate("MainWindow", "添加"))
        self.empty.setText(_translate("MainWindow", "..."))
        self.goup.setText(_translate("MainWindow", "上移"))
        self.godown.setText(_translate("MainWindow", "下移"))
        self.del_1.setText(_translate("MainWindow", "删除"))
        self.modify.setText(_translate("MainWindow", "修改"))
        self.label_9.setText(_translate("MainWindow", "当前英雄技能顺序:"))
        self.label_6.setText(_translate("MainWindow", "英雄出场顺序"))
        self.load.setText(_translate("MainWindow", "加载配置"))
        self.save.setText(_translate("MainWindow", "保存配置"))
        self.run.setText(_translate("MainWindow", "运行脚本"))
        # self.menuLanguage.setTitle(_translate("MainWindow", "Language"))
        self.actionEnglish.setText(_translate("MainWindow", "English"))
        self.actionChinese.setText(_translate("MainWindow", "Chinese"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui()
    app.exec_()
