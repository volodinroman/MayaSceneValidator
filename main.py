import os
from MayaSceneValidator.core.resources import Resources
root_ = os.path.dirname(__file__)

class Validator(object):
    def __init__(self):
        self.resources = Resources()




def main():
    v = Validator()


if __name__ == '__main__':
    main()