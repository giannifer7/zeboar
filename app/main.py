from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import MDList
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDToolbar
#from kivymd.uix.toolbar import MDTopAppBar
from kivy.utils import platform

from kivy.logger import Logger
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen
from kivymd.uix.screen import MDScreen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivymd.toast import toast

from navigation_drawer import navigation_helper
from dirtree import read_tree, DirNode
from store import Store
from leaves import LeafFormsBuilder, register_leaf_forms
from leaf_screen_generic import GenericLeaf


if platform not in ('android', 'ios'):
    Window.size = (300, 500)


class DirectoryPress:
    def __init__(self, tl):
        self.tl = tl

    def __call__(self, instance):
        theApp = MDApp.get_running_app()
        theApp.add_screen(self.tl)
        theApp.sm.transition.direction = 'left'
        theApp.sm.current = self.tl.path_string()


class BackPress:
    def __init__(self, tl):
        self.tl = tl

    def __call__(self, instance):
        theApp = MDApp.get_running_app()
        theApp.remove_node(self.tl)



class ZebraApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.directory_fn = 'directory.txt'
        self.data_url = 'http://127.0.0.1:8000'
        #self.data_url = 'https://425d-2-40-118-34.eu.ngrok.io'
        self.sm = None
        self.previous_screen = None
        self.tree_root, self.tree_as_path_dict = read_tree(self.directory_fn)
        self.leaf_forms_builder = LeafFormsBuilder()
        self.user = ('admin', 'admin')
        self.store = Store(self, self.data_url, self.user)

    class ContentNavigationDrawer(BoxLayout):
        pass

    class DrawerList(ThemableBehavior, MDList):
        pass

    def on_start(self):
        #on_press = DirectoryPress(child)
        pass

    def build_config(self, config):
        config.setdefaults('section1', {
            'key1': 'value1',
            'key2': '42'
        })
        # config.get('section1', 'key1'),
        # config.getint('section1', 'key2')))

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        screen = Builder.load_string(navigation_helper)
        self.sm = screen.ids.screen_manager
        self.sm.transition: NoTransition()
        self.add_screen(self.tree_root)
        register_leaf_forms(self.leaf_forms_builder)
        self.sm.current = 'h'
        return screen

    def navigation_draw(self):
        print("Navigation")

    def scan_action_db_connect(self, url):
        self.data_url = url

    def scan_db(self):
        print("scan_db")
        self.get_qr_with_action(ZebraApp.scan_action_db_connect)

    def profile(self):
        print("profile")
        self.root.ids.nav_drawer.set_state("close")
        if self.previous_screen is None:
            self.previous_screen = self.sm.current
        self.sm.current = "scr 2"

    def dir_screen(self):
        print("dir_screen")
        self.root.ids.nav_drawer.set_state("close")
        if self.previous_screen is not None:
            self.sm.current = self.previous_screen
        self.previous_screen = None

    def get_qr_with_action(self, action):
        # https://github.com/tshirtman/android_jnius_custom_java/fork
        if platform != 'android':
            return
        from jnius import autoclass
        from jnius import cast
        from android import activity
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        IntentIntegrator = autoclass("com.google.zxing.integration.android.IntentIntegrator")
        integrator = IntentIntegrator(currentActivity)
        def on_qr_result(requestCode, resultCode, intent):
            jScanResult = IntentIntegrator.parseActivityResult(requestCode, resultCode, intent)
            scanResult = cast('com.google.zxing.integration.android.IntentResult', jScanResult)
            contents = scanResult.getContents()
            Logger.info(contents)
            action(self, contents)
        activity.bind(on_activity_result=on_qr_result)
        integrator.initiateScan()

    def populate_leaf(self, vbox, node):
        path = node.long_path_string()
        lbl = MDLabel(text=path, halign="center", size_hint=(1, .08))
        vbox.add_widget(lbl)
        form = self.leaf_forms_builder.build(node.path_string())
        return form
    
    def show_form(self, form_name, prev_form_name, widget):
        new_screen = GenericLeaf(
            name=form_name, 
            prev_form_name=prev_form_name,
            list_event=widget,
            #api_endpoint=api_endpoint,
            #api_id=api_id
        )
        self.sm.add_widget(new_screen)
        self.sm.transition.direction = 'left'
        self.sm.current = form_name

    def remove_node(self, node):
        self.sm.transition.direction = 'right'
        self.sm.remove_widget(self.sm.get_screen(node.path_string()))
        self.sm.current = node.parent.path_string()

    def add_screen(self, node):
        new_screen = Screen(name=node.path_string())
        self.sm.add_widget(new_screen)
        y_hint = .87 if platform not in ('android', 'ios') else .915
        hbox = BoxLayout(size_hint=(1, y_hint))
        if node.parent is not None:
            back = Button(text='<', size_hint=(.1, 1))
            back.bind(on_press=BackPress(node))
            hbox.add_widget(back)
        vbox = BoxLayout(orientation='vertical')
        form = self.populate_leaf(vbox, node)
        if form is not None:
            vbox.add_widget(form(self))
        else:
            inner_vbox = BoxLayout(orientation='vertical', size_hint=(1, .9))
            for child in node:
                item = Button(text=child.long_tag)
                item.bind(on_press=DirectoryPress(child))
                inner_vbox.add_widget(item)
            vbox.add_widget(inner_vbox)
        hbox.add_widget(vbox)
        new_screen.add_widget(hbox)

if __name__ == "__main__":
    theApp = ZebraApp()
    theApp.run()
