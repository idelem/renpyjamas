# sorry, this is for list view
default headline = Line("")

init python:
    
    class Line:
        def __init__(self, text, prev=None, next=None):
            self.text = text
            self.prev = prev
            self.next = next
            self.iv = FieldInputValue(self, "text")
        
        def append(self, line):
            line.prev = self
            line.next = self.next
            self.next = line

        def prepend(self, line):
            line.next = self
            line.prev = self.prev
            self.prev = line

        def remove(self):
            if self.prev:
                self.prev.next = self.next
            if self.next:
                self.next.prev = self.prev

        def flatten(self):
            # 不包括自己
            lst = []
            line = self.next
            while line:
                lst.append(line.text)
                line = line.next
            return lst

        def rollout(self):
            lst = []
            line = self.next
            while line:
                lst.append(line)
                line = line.next
            return lst

        def set_tail(self, lines):
            if lines:
                self.next = lines[0]
                lines[0].prev = self
        
        def cut_tail(self):
            self.next = None

screen dict_input(keys, obj):
    # 目前只能编辑字符串字段！
    frame:
        background Solid("#fff")
        has vbox
        $ order = 0 # 用来给列表排版
        for i in range(len(keys)):
            $ k = keys[i]
            hbox:
                ysize 32
                $ attr = getattr(obj, k)
                # str
                if isinstance(attr, str):
                    $ iv = FieldInputValue(obj, k)
                    textbutton k xsize 128
                    button action Show("single_input", iv=iv, order=order) xfill True:
                        text attr
                    $ order += 1
                # list
                elif hasattr(attr, "append"):
                    # $ print "dict_input: {}".format(id(attr))
                    textbutton k xsize 128
                    button action [Function(headline.set_tail, make_lines(attr)), Show("list_input", lst=(obj,k), order=order)] xfill True:
                        text "点击编辑列表"
                    $ order += 1 # len(attr)
                
        textbutton "填完了" action [
            Function(headline.cut_tail),
            Hide("single_input"), 
            Hide("list_input"),
            Hide("dict_input"), 
            Return()
            ]

init python:
    def make_lines(lst):
        lines = []
        for i in range(len(lst)):
            line = Line(lst[i])
            lines.append(line)
            line.iv = FieldInputValue(line, "text")
        for i in range(len(lines)):
            if i-1 >= 0:
                lines[i].prev = lines[i-1]
            if i+1 < len(lines):
                lines[i].next = lines[i+1]
        return lines

    def make_headline(lines):
        if lines:
            return Line("", next=lines[0])
        return Line("")

    def make_list(hl):
        return hl.flatten()

    def set_list(ref, hl):
        obj, attr = ref
        setattr(obj, attr, hl.flatten())
        # print "set_lst: {}".format(id(lst))


screen list_input(lst, order=0):
    # $ print "list_input: {}".format(id(lst))
    $ yp = order * 36

    $ lines = headline.rollout()

    frame:
        background Solid("#f7f7f7")
        xpos 128
        ypos yp
        vbox:
            textbutton "+" action [Function(headline.append, Line(""))]
            for i in range(len(lines)):
                $ line = lines[i]
                hbox:
                    hbox:
                        xsize 128
                        # 添加
                        textbutton "+" action [Function(line.append, Line(""))]
                        # 删除
                        textbutton "x" action [Function(line.remove)]
                        textbutton "[i]"
                    button action Show("single_input", iv=line.iv, order=i+order, xp=128, yp=12, ls=43) xfill True:
                        textbutton line.text
            # 最后把链表转回 list
            hbox:
                textbutton "填完了" action [
                    Function(set_list, lst, headline), 
                    Hide("single_input"), 
                    Hide("list_input"),
                    ]

screen single_input(iv, order=0, xp=0, yp=0, ls=36):
    zorder 999
    $ yp = order * ls + yp
    frame:
        background Solid("#fff")
        xpos xp+128
        ypos yp
        ysize ls
        hbox:
            input value iv
            textbutton "√" action Hide("single_input")
