from kivymd.uix.list import MDList, TwoLineListItem
from kivy.properties import NumericProperty, StringProperty, ObjectProperty


class ZebraList2(TwoLineListItem):
    obj_table = StringProperty()
    obj_key = NumericProperty()
