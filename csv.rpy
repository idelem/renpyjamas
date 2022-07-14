# renpy csv importer

init -1000 python:

    # https://codereview.stackexchange.com/questions/171107/python-class-initialize-with-dict

    class Data():
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    def load_file(fn):
        if not renpy.loadable("data/" + fn):
            return
        return renpy.file("data/" + fn)

    def make_obj(line, keys, Obj):
        row = line.strip().split(",")
        d = {}
        for i in range(len(row)):
            k = keys[i]
            v = row[i]
            d[k] = v
        obj = Obj(**d)

    def _import_data(fn, Obj):
        f = load_file(fn + ".csv")
        first = f.readline()
        keys = first.strip().split(",")
        for line in f:
            if line.strip()[0] == "#": # ignores comment
                continue
            make_obj(line, keys, Obj)
        
        f.close()

# sample usage
# you need to define class attributes in __slots__

init python:
    class Foo(Data):
        __slots__ = [
            "field1", 
            "field2", 
        ]
        def __init__(self, **kwargs):
            super(Foo, self).__init__(**kwargs)
            # do other things here

label import_data():
    python:
        _import_data("foo", Foo) # pass in file name and class
    return
