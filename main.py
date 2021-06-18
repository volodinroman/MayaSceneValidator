import os
from MayaSceneValidator.gui.main_gui import ValidatorGUI, create_gui
from MayaSceneValidator.core.batch_mode import BatchValidator
root_ = os.path.dirname(__file__)


class Validator(object):

    GUI_MODE = 0
    BATCH_MODE = 1

    def __init__(self, mode, preset, auto_fix=False):

        if mode == Validator.GUI_MODE:
            create_gui()
        elif mode == Validator.BATCH_MODE:
            batch = BatchValidator()
            batch.start(preset=preset, auto_fix=auto_fix)

def main(preset="modeling", autofix=False, mode=Validator.GUI_MODE):
    v = Validator(mode=mode, preset=preset, auto_fix=autofix)

