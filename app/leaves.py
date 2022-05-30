from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from dirtree import read_tree
from store import Store
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList, TwoLineListItem
from kivymd.uix.textfield import MDTextField
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import AsyncImage, Image
from kivy.loader import Loader
from kivy.properties import StringProperty

from zebralist import ZebraList2
from leaf_screen_generic import GenericLeaf
from leaf_screen_generic import create_cerpc_crud_form
from edit_image_form import cerpc_img_edit



class LeafFormsBuilder:
    def __init__(self):
        self.builders_dict = {}

    def register(self, name, builder):
        self.builders_dict[name] = builder

    def build(self, name):
        print(name)
        return self.builders_dict.get(name)


def create_cerpc_form(app):
    obj_table = 'cieco'
    form = BoxLayout(orientation='vertical')
    scroll = ScrollView()
    list_view = MDList()
    rackmaterials = app.store.get_rackmaterials(tipo="pannello", subtipo="cieco")
    for rm in rackmaterials:
        item = ZebraList2(
            obj_table=obj_table,
            obj_key=rm['id'],
            text=f"{rm['units']} units",
            secondary_text=f"qty: {rm['quantity']}    pos: {rm['position']}    comm: {rm['comm']}",
            on_press=lambda evt: app.show_form('cerpc_crud', 'cerpc', evt)
        )
        list_view.add_widget(item)
    scroll.add_widget(list_view)
    form.add_widget(scroll)
    return form


def register_leaf_forms(builder):
    builder.register('cerpc', create_cerpc_form)
    builder.register('cerpc_crud', create_cerpc_crud_form)
    builder.register('cerpc_img_edit', cerpc_img_edit)
    
