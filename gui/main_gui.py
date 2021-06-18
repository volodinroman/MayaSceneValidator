from PySide2 import QtWidgets, QtCore, QtGui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import os
import maya.cmds as cmds

from MayaSceneValidator.core.resources import Resources
from MayaSceneValidator.core.common import log
from MayaSceneValidator.gui.ruleWidget.ruleWidget import RuleWidget


class ValidatorGUI(MayaQWidgetDockableMixin, QtWidgets.QDockWidget):
    def __init__(self):
        super(ValidatorGUI, self).__init__()
        self.resources = Resources.get_instance()

        self.setup_ui()

    def setup_ui(self):
        self.setMinimumWidth(420)
        self.setMinimumHeight(500)
        self.setWindowTitle("Validator")
        self.setObjectName("mayaSceneValidatorID")
        self.setDockableParameters(width=420)  # MayaQWidgetDockableMixin

        # main layout
        self.main_widget = QtWidgets.QWidget()
        self.setWidget(self.main_widget)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignTop)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_widget.setLayout(self.main_layout)

        # top panel
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.setSpacing(5)
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(self.buttons_layout)

        # pre-scroll creation
        self.scroll_layout = QtWidgets.QVBoxLayout()

        # button run
        self.button_run = QtWidgets.QPushButton("Start Validator")
        self.button_run.setFixedHeight(32)
        self.button_run.clicked.connect(self.run_validator)
        self.buttons_layout.addWidget(self.button_run)

        # button fix
        self.button_fix = QtWidgets.QPushButton("Fix Failed Checks")
        self.button_fix.setFixedHeight(32)
        self.button_fix.clicked.connect(self.fix_validator)
        self.buttons_layout.addWidget(self.button_fix)

        # presets
        self.combo_presets = QtWidgets.QComboBox()
        self.combo_presets.setFixedHeight(32)
        self.combo_presets.setMinimumWidth(250)
        self.buttons_layout.addWidget(self.combo_presets)

        for i in self.resources.get_presets():
            preset_name = os.path.split(i)[1]
            preset_name_no_extension = os.path.splitext(preset_name)[0]
            self.combo_presets.addItem(preset_name_no_extension)
            self.combo_presets.setCurrentText(self.resources.preset_current)

        self.combo_presets.currentTextChanged.connect(self.save_config_preset)

        # scroll area
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumWidth(300)
        self.scroll_area.setFocusPolicy(QtCore.Qt.NoFocus)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll_area_widget = QtWidgets.QWidget()
        self.scroll_area.setWidget(self.scroll_area_widget)

        self.scroll_layout.setAlignment(QtCore.Qt.AlignTop)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(5)  # layout
        self.scroll_area_widget.setLayout(self.scroll_layout)
        self.main_layout.addWidget(self.scroll_area)

        # some initial data in scrollArea
        self.help_label = QtWidgets.QLabel("Press 'Run' to validate the scene")
        self.scroll_layout.addWidget(self.help_label)


    def save_config_preset(self, text):
        self.resources.save_current_preset(text)
        log(message="config.ini saved. New preset is {}".format(text))

    def clean_scroll(self, rule_name=None):
        if self.scroll_layout:
            if self.scroll_layout.count() > 0:
                for i in range(0, self.scroll_layout.count()):
                    item = self.scroll_layout.itemAt(i)
                    widget = item.widget()

                    if rule_name:
                        if rule_name==widget.get_rule_name():
                            widget.deleteLater()
                    else:
                        widget.deleteLater()

    def run_validator(self):
        log(message="Run...")

        rules = self.resources.get_current_preset_rules()

        self.clean_scroll()

        for i in rules:
            log(message="{} run".format(i), category="Rule")

            cmd = "from MayaSceneValidator.rules.{}.rule import Rule".format(i)
            exec(cmd)

            rule = Rule()
            rule_name = rule.rule_name
            rule_description = rule.rule_description
            rule_output = rule.check()

            if rule_output:
                rule_widget = RuleWidget(rule_instance=rule)
                rule_widget.set_rule_name(rule_name)
                rule_widget.set_rule_description(rule_description)
                rule_widget.signal_validator_run.connect(self.run_rule)
                rule_widget.signal_validator_fix.connect(self.fix_validator)

                for j in rule_output:
                    rule_widget.add_invalid_object(j)

                self.scroll_layout.addWidget(rule_widget)


    def fix_validator(self, rule_name):
        if self.scroll_layout:
            if self.scroll_layout.count() > 0:
                for i in range(0, self.scroll_layout.count()):
                    item = self.scroll_layout.itemAt(i)
                    widget = item.widget()
                    name = widget.get_rule_name()

                    if rule_name:
                        if rule_name==name:
                            result = widget.rule_run_fix()
                            log(message="{} fix".format(name), category="Fix")
                            if not result:
                                self.clean_scroll(rule_name=name)
                    else:
                        result = widget.rule_run_fix()
                        log(message="{} fix".format(name), category="Fix")
                        if not result:
                            self.clean_scroll(rule_name=name)

    def run_rule(self, rule_name):
        print "test"
        if self.scroll_layout:
            if self.scroll_layout.count() > 0:
                for i in range(0, self.scroll_layout.count()):
                    item = self.scroll_layout.itemAt(i)
                    widget = item.widget()
                    name = widget.get_rule_name()

                    if rule_name == name:
                        result = widget.rule_run_check()

                        if not result:
                            self.clean_scroll(rule_name=name)
                        else:
                            widget.recreate_list(new_list=result)


def create_gui():
    # https://matiascodesal.com/blog/how-to-setup-pycharm-for-maya-scripting-with-autocomplete-and-external-documentation/

    if cmds.workspaceControl("mayaSceneValidatorIDWorkspaceControl", exists=True):
        cmds.deleteUI("mayaSceneValidatorIDWorkspaceControl", control=True)
        cmds.workspaceControlState("mayaSceneValidatorIDWorkspaceControl", remove=1)

    dialog = ValidatorGUI()
    dialog.show(dockable=True, area="right", allowedArea="right", floating=True)

    cmds.workspaceControl("mayaSceneValidatorIDWorkspaceControl", e=1,
                          tabToControl=["AttributeEditor", -1],
                          wp="preffered",
                          iw=420,
                          mw=420,
                          minimumWidth=True)
