import maya.cmds as cmds

class Rule(object):

    def __init__(self):

        self.rule_name = "Object Transforms"
        self.rule_description = "All objects should have all transforms zeroed out"
        self.output = []  # if output is not empty - the Rule has not been passed

    def check(self):
        self.output = []
        # get all transforms in our scene
        allTransforms = cmds.ls(type="transform", l=1)
        cameras = cmds.ls(type="camera", l=1)
        camerasTransforms = cmds.listRelatives(cameras, p=1, f=1)
        for i in allTransforms:
            if i in camerasTransforms:
                continue
            t = cmds.xform(i, q=1, t=1, a=1)
            r = cmds.xform(i, q=1, ro=1, a=1)
            s = cmds.xform(i, q=1, s=1, r=1)
            if t != [0.0, 0.0, 0.0] or r != [0.0, 0.0, 0.0] or s != [1, 1, 1]:
                self.output.append(i)
        return self.output

    def fix(self):
        if self.output:
            for i in self.output:
                cmds.xform(i, t=[0, 0, 0])
                cmds.xform(i, ro=[0, 0, 0])
                cmds.xform(i, s=[1, 1, 1])
        output = self.check()
        return output