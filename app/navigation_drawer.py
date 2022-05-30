navigation_helper = """
<ContentNavigationDrawer>
    orientation: 'vertical'
    padding: "8dp"
    spacing: "8dp"

    ScrollView:

        DrawerList:
            id: md_list

            MDList:
                OneLineIconListItem:
                    text: "Profile"
                    on_press: app.profile()
                    IconLeftWidget:
                        icon: "face-profile"

                OneLineIconListItem:
                    id: "scan_db"
                    text: "scan db connection"
                    on_release: app.scan_db()
                    IconLeftWidget:
                        icon: "qrcode-scan"

                OneLineIconListItem:
                    text: "connection"
                    # on_release: app.gen_connection_qr()

                    IconLeftWidget:
                        icon: "connection"


                OneLineIconListItem:
                    text: "dir"
                    on_release: app.dir_screen()
                    IconLeftWidget:
                        icon: "file-tree"


MDScreen:

    MDToolbar:
        id: toolbar
        pos_hint: {"top": 1}
        elevation: 3
        title: "  Decima1948 - Zebra4"
        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

    MDNavigationLayout:
        x: toolbar.height

        ScreenManager:
            id: screen_manager

            MDScreen:
                name: "scr 2"

                MDLabel:
                    text: "Screen 2"
                    halign: "center"

        MDNavigationDrawer:
            id: nav_drawer

            ContentNavigationDrawer:
                screen_manager: screen_manager
                nav_drawer: nav_drawer
"""
