import yaml

class ListAttr(list):
    def __init__(self):
        list.__init__(self)
        self.__indent__ = "  "

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
    def __init__(self):
        self.__indent__ = "  "

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

    def items(self):
        for key in sorted(self.__dict__.keys()):
            if key == "__indent__": continue
            yield (key, self.__dict__[key])

class Config(DotAttr):
    def __init__(self, config_file):
        DotAttr.__init__(self)
        with open(config_file) as fh:
            yy = yaml.load(fh)
            for key, value in yy.items():
                self._add_dot_value(self, key, value)

    def _add_list_value(self, value):
        if isinstance(value, dict):
            dot_attr = DotAttr()
            for key2, value2 in value.items():
                self._add_dot_value(dot_attr, key2, value2)
            return dot_attr
        elif isinstance(value, list):
            list_attr = ListAttr()
            for item in value:
                list_attr.append(self._add_list_value(item))
            return list_attr
        else:
            return value

    def _add_dot_value(self, store, key, value):
        if isinstance(value, dict):
            dot_attr = DotAttr()
            for key2, value2 in value.items():
                self._add_dot_value(dot_attr, key2, value2)
            setattr(store, key, dot_attr)
        elif isinstance(value, list):
            list_attr = ListAttr()
            for item in value:
                list_attr.append(self._add_list_value(item))
            setattr(store, key, list_attr)
        else:
            setattr(store, key, value)

    def __str__(self):
        return self._str()
