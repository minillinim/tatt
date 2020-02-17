import yaml
import numpy as np

class ListAttr(list):
    def __init__(self, items):
        list.__init__(self)
        self.__indent__ = "  "
        for item in items:
            self.add_attr(item)

    def add_attr(self, value):
        if isinstance(value, dict):
            self.append(DotAttr(value))
        elif isinstance(value, list):
            self.append(ListAttr(value))
        else:
            self.append(value)

    def _str(self, indent=""):
        augment = ""
        for index in range(len(self)):
            augment += "%s%d:" % (indent, index)
            if isinstance(self[index], DotAttr):
                augment += "\n%s" % self[index]._str(indent+self.__indent__)
            elif isinstance(self[index], ListAttr):
                augment += "\n%s" % (self[index]._str(indent+self.__indent__))
            else:
                augment += " %s" % (self[index])
        return augment

class DotAttr(object):
    def __init__(self, attrs):
        self.__indent__ = "  "
        for key, value in attrs.items():
            self.add_attr(key, value)

    def add_attr(self, key, value):
        if isinstance(value, dict):
            setattr(self, key, DotAttr(value))
        elif isinstance(value, list):
            setattr(self, key, ListAttr(value))
        else:
            setattr(self, key, value)

    def items(self):
        for key in sorted(self.__dict__.keys()):
            if key == "__indent__": continue
            yield (key, self.__dict__[key])

    def _str(self, indent=""):
        augment = ""
        for key, value in self.items():
            augment += "%s%s:" % (indent, key)
            if isinstance(value, DotAttr):
                augment += "\n%s" % value._str(indent+self.__indent__)
            elif isinstance(value, ListAttr):
                augment += "\n%s" % (value._str(indent+self.__indent__))
            else:
                augment += " %s\n" % (str(value))
        return augment

class Config(DotAttr):
    def __init__(self, config_file):
        DotAttr.__init__(self, {})
        with open(config_file) as fh:
            yy = yaml.load(fh)
            for key, value in yy.items():
                self.add_attr(key, value)

    def __str__(self):
        return self._str()
