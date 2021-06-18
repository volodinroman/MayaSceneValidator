import os
from MayaSceneValidator.gui.main_gui import ValidatorGUI, create_gui

root_ = os.path.dirname(__file__)


class Validator(object):

    GUI_MODE = 0
    BATCH_MODE = 1

    def __init__(self, mode):

        if mode == Validator.GUI_MODE:
            create_gui()
        elif mode == Validator.BATCH_MODE:
            pass  # batch mode






def main():
    v = Validator(mode=Validator.GUI_MODE)


# if __name__ == '__main__':
#     main()