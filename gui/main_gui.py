from PySide2 import QtWidgets, QtCore, QtGui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import os
import maya.cmds as cmds

from MayaSceneValidator.core.resources import Resources
from MayaSceneValidator.core.common import log


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

        # button run
        self.button_run = QtWidgets.QPushButton("Start Validator")
        self.button_run.setFixedHeight(32)
        self.button_run.clicked.connect(self.run_validator())
        self.buttons_layout.addWidget(self.button_run)

        # button fix
        self.button_fix = QtWidgets.QPushButton("Fix Failed Checks")
        self.button_fix.setFixedHeight(32)
        self.button_fix.clicked.connect(self.fix_validator())
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
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_layout.setAlignment(QtCore.Qt.AlignTop)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(5)  # layout
        self.scroll_area_widget.setLayout(self.scroll_layout)
        self.main_layout.addWidget(self.scroll_area)

        # test
        for i in range(20):
            b = QtWidgets.QPushButton("test {}".format(i))
            self.scroll_layout.addWidget(b)

    def save_config_preset(self, text):
        self.resources.save_current_preset(text)
        log(message="config.ini saved. New preset is {}".format(text))


    def run_validator(self):
        pass

    def fix_validator(self):
        pass


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
