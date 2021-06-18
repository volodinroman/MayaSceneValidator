from PySide2 import QtWidgets, QtGui, QtCore
import os
import maya.cmds as cmds

root_ = os.path.dirname(__file__)

class RuleListPanel(QtWidgets.QWidget):
    def __init__(self, description="test"):
        super(RuleListPanel, self).__init__()

        self.rule_description = description

        self.setup_ui()

    def setup_ui(self):
        # Widget properties
        self.setMinimumWidth(290)
        self.setFixedHeight(300)
        self.setVisible(0)

        #  set background color
        self.bg = 30
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtGui.QColor(self.bg, self.bg, self.bg))
        self.setPalette(palette)

        # main layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignTop)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(5, 10, 5, 10)
        self.setLayout(self.main_layout)

        # add label description
        self.description = QtWidgets.QLabel("Description")
        self.main_layout.addWidget(self.description)

        # add description content
        self.description_content = QtWidgets.QLabel(self.rule_description)
        self.main_layout.addWidget(self.description_content)

        # add List Widget
        self.list = QtWidgets.QListWidget()
        self.list.itemClicked.connect(self.select_item)
        self.main_layout.addWidget(self.list)


    def select_item(self, item):
        cmds.select(item.text())

    def get_description(self):
        return self.rule_description

    def set_description(self, desc):
        self.rule_description = desc
        self.description_content.setText(desc)

    def add_item(self, item="Unknown"):
        self.list.addItem(item)

    def clear_list(self):
        self.list.clear()

    def toggle_visibility(self):
        self.setVisible(not self.isVisible())

