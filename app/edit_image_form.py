from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import platform
from kivy.config import Config
from dirtree import read_tree
from store import Store
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList, TwoLineListItem
from kivymd.uix.textfield import MDTextField
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import AsyncImage, Image
from kivy.loader import Loader
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from zebralist import ZebraList2


bu_leaf_screen_generic_kv = '''
<BuGenericLeaf>:
    BoxLayout:
        id: external_vbox
        orientation: 'vertical'
        spacing: dp(5)

        MDLabel:
            id: form_title
            #text: ''
            halign: "center"
            size_hint: (1, .08)

        BoxLayout:
            id: generic_leaf_inner
            orientation: 'vertical'

        BoxLayout:
            id: buttons_hbox
            size_hint: (1, .12)

            Button:
                id: cancel_button
                text: 'Cancel'
                on_press: root.cancel()

            Button:
                id: new_button
                text: 'New'

            Button:
                id: clone_button
                text: 'BuClone'

            Button:
                id: del_button
                text: 'Del'

            Button:
                id: take_button
                text: 'Take'

            Button:
                id: ok_button
                text: 'OK'
'''


Builder.load_string(bu_leaf_screen_generic_kv)

class BuGenericLeaf(Screen):
    prev_form_name = StringProperty('')
    list_event = ObjectProperty()
    #api_endpoint = StringProperty('')
    #api_id = StringProperty('')

    def on_enter(self):
        y_hint = .87 if platform not in ('android', 'ios') else .915
        self.ids.external_vbox.size_hint = (1, y_hint)
        self.ids.generic_leaf_inner.clear_widgets()
        #title, widget = create_cerpc_crud_form(self.list_event)
        widgetBuilder = MDApp.get_running_app().leaf_forms_builder.build(self.name)
        title, widget = widgetBuilder(self.list_event)
        self.ids.form_title.text = title
        self.ids.generic_leaf_inner.add_widget(widget)

    def cancel(self):
        sm = MDApp.get_running_app().sm
        sm.transition.direction = 'right'
        sm.remove_widget(self)
        sm.current = self.prev_form_name


bu_cerpc_crud_form_kv = '''
BuRootWidget:
    # position of Anchor Layout 
    anchor_x: 'center'
    anchor_y: 'center'
    
    BoxLayout:
        orientation: 'vertical'
        size_hint: (0.9, 1)
        
        AsyncImage:
            id: pos_pic
            source: root.image_path
'''


class BuRootWidget(AnchorLayout):
    image_path = StringProperty('')
    pos_pic_idx = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def change_image(self, path):
        self.image_path = path
        
    def next_pic(self, increment):
        print(increment)
        self.pos_pic_idx += increment
        try:
            self.image_path = MDApp.get_running_app().store.image_url(self.rec['pos_pics'], self.pos_pic_idx)
        except IndexError:
            pass


    def edit_pic(self):
        MDApp.get_running_app().show_form('cerpc_img_edit', 'cerpc_crud', self)




    def load(self, list_event):
        big_image_path = list_event.big_image_path
        print(big_image_path)
        #store = MDApp.get_running_app().store
        self.image_path = big_image_path


def cerpc_img_edit(list_event):
    form = Builder.load_string(bu_cerpc_crud_form_kv)
    form.load(list_event)
    # image_file = "IMG_20220401_140434_4.jpg"
    return 'pannello cieco', form
