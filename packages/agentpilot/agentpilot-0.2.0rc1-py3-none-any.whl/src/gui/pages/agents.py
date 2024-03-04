
import json
import sqlite3

from PySide6.QtGui import Qt, QFont
from PySide6.QtWidgets import *

from src.utils.helpers import display_messagebox
from src.utils import sql

from src.gui.components.agent_settings import AgentSettings
from src.gui.components.config import ConfigTree, CVBoxLayout, CHBoxLayout
from src.gui.widgets.base import ContentPage, IconButton


class TopBarMenu(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.parent = parent
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setProperty("class", "sidebar")
        self.setFixedHeight(40)

        self.page_buttons = {
            key: self.Settings_SideBar_Button(parent=self, text=key) for key in self.parent.pages.keys()
        }
        if len(self.page_buttons) == 0:
            return

        first_button = next(iter(self.page_buttons.values()))
        first_button.setChecked(True)

        self.layout = CHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 10, 0)

        self.button_group = QButtonGroup(self)

        i = 0
        for _, btn in self.page_buttons.items():
            self.button_group.addButton(btn, i)
            self.layout.addWidget(btn)
            i += 1

        self.layout.addStretch(1)
        self.button_group.buttonToggled[QAbstractButton, bool].connect(self.onButtonToggled)

    def load(self):
        pass

    def onButtonToggled(self, button, checked):
        if checked:
            index = self.button_group.id(button)
            self.parent.content.setCurrentIndex(index)
            self.parent.content.currentWidget().load()

    class Settings_SideBar_Button(QPushButton):
        def __init__(self, parent, text=''):
            super().__init__()
            self.setProperty("class", "labelmenuitem")
            # self.setContentsMargins(0, 0, 0, 0)
            self.setFixedWidth(100)
            self.setText(self.tr(text))
            self.setCheckable(True)
            self.font = QFont()
            self.font.setPointSize(15)
            self.setFont(self.font)


class Page_Contacts(ContentPage):
    def __init__(self, main):
        super().__init__(main=main)  # , title='Agents')

        self.pages = {
            'Agents': self.Page_Agents(parent=self),
            'Humans': self.Page_Humans(parent=self),
        }
        self.content = QStackedWidget(parent=self)
        for page in self.pages.values():
            self.content.addWidget(page)
        self.top_bar_menu = TopBarMenu(parent=self)

        self.title_layout.addWidget(self.top_bar_menu)
        self.layout.addWidget(self.content)

    def load(self):
        for page in self.pages.values():
            page.load()

    class Page_Agents(QWidget):
        def __init__(self, parent):
            super().__init__(parent=parent)
            self.main = parent.main

            self.layout = CVBoxLayout(self)

            self.btn_explore = IconButton(
                parent=self,
                icon_path=':/resources/icon-globe.png',
                tooltip='Explore',
                size=18,
            )

            self.tree_config = ConfigTree(
                parent=self,
                db_table='agents',
                db_config_field='config',
                query="""
                    SELECT
                        COALESCE(json_extract(config, '$."info.name"'), name) AS name,
                        id,
                        json_extract(config, '$."info.avatar_path"') AS avatar,
                        config,
                        '' AS chat_button,
                        folder_id
                    FROM agents
                    ORDER BY ordr""",
                schema=[
                    {
                        'text': 'Name',
                        'key': 'name',
                        'type': str,
                        'stretch': True,
                        'image_key': 'avatar',
                    },
                    {
                        'text': 'id',
                        'key': 'id',
                        'type': int,
                        'visible': False,
                    },
                    {
                        'key': 'avatar',
                        'text': '',
                        'type': str,
                        'visible': False,
                    },
                    {
                        'text': 'Config',
                        'type': str,
                        'visible': False,
                    },
                    {
                        'text': '',
                        'type': QPushButton,
                        'icon': ':/resources/icon-chat.png',
                        'func': self.on_chat_btn_clicked,
                        'width': 45,
                    },
                ],
                add_item_prompt=('Add Agent', 'Enter a name for the agent:'),
                del_item_prompt=('Delete Agent', 'Are you sure you want to delete this agent?'),
                layout_type=QVBoxLayout,
                config_widget=self.Agent_Config_Widget(parent=self),
                tree_width=600,
                tree_header_hidden=True,
                folder_key='agents',
                filterable=True,
            )
            self.tree_config.tree.setSortingEnabled(False)
            # self.tree_config = TreeConfig(self)
            self.tree_config.build_schema()

            self.tree_config.tree.itemDoubleClicked.connect(self.on_row_double_clicked)

            self.layout.addWidget(self.tree_config)
            self.layout.addStretch(1)

        def load(self):
            self.tree_config.load()

        def explore(self):
            print('explore')
            pass

        class Agent_Config_Widget(AgentSettings):
            def __init__(self, parent):
                super().__init__(parent=parent)
                self.parent = parent

            def save_config(self):
                """Saves the config to database when modified"""
                if self.ref_id is None:
                    return
                json_config_dict = self.get_config()
                json_config = json.dumps(json_config_dict)
                name = json_config_dict.get('info.name', 'Assistant')
                try:
                    sql.execute("UPDATE agents SET config = ?, name = ? WHERE id = ?", (json_config, name, self.ref_id))
                except sqlite3.IntegrityError as e:
                    display_messagebox(
                        icon=QMessageBox.Warning,
                        title='Error',
                        text='Name already exists',
                    )
                    return
                self.load_config(json_config)  # todo needed for configjsontree, but why
                self.settings_sidebar.load()

        def on_row_double_clicked(self):
            agent_id = self.tree_config.get_current_id()
            if not agent_id:
                return

            self.chat_with_agent(agent_id)

        def on_chat_btn_clicked(self, row_data):
            agent_id = self.tree_config.get_current_id()
            if not agent_id:
                return
            self.chat_with_agent(agent_id)

        def chat_with_agent(self, agent_id):
            if self.main.page_chat.workflow.responding:
                return
            self.main.page_chat.new_context(agent_id=agent_id)
            self.main.sidebar.btn_new_context.click()


    class Page_Humans(QWidget):
        def __init__(self, parent):
            super().__init__(parent=parent)
            self.layout = CVBoxLayout(self)

            # self.tree_config = ConfigTree(
            #     parent=self,
            #     db_table='humans',
            #     db_config_field='config',
            #     query="""
            #         SELECT
            #             COALESCE(json_extract(config, '$."info.name"'), name) AS name,
            #             id,
            #             json_extract(config, '$."info.avatar_path"') AS avatar,
            #             config,
            #             '' AS chat_button,
            #             folder_id
            #         FROM agents
            #         ORDER BY ordr""",
            #     schema=[
            #         {
            #             'text': 'Name',
            #             'key': 'name',
            #             'type': str,
            #             'stretch': True,
            #             'image_key': 'avatar',
            #         },
            #         {
            #             'text': 'id',
            #             'key': 'id',
            #             'type': int,
            #             'visible': False,
            #         },
            #         {
            #             'key': 'avatar',
            #             'text': '',
            #             'type': str,
            #             'visible': False,
            #         },
            #         {
            #             'text': 'Config',
            #             'type': str,
            #             'visible': False,
            #         },
            #         {
            #             'text': '',
            #             'type': QPushButton,
            #             'icon': ':/resources/icon-chat.png',
            #             'func': self.on_chat_btn_clicked,
            #             'width': 45,
            #         },
            #     ],
            #     add_item_prompt=('Add Agent', 'Enter a name for the agent:'),
            #     del_item_prompt=('Delete Agent', 'Are you sure you want to delete this agent?'),
            #     layout_type=QVBoxLayout,
            #     config_widget=self.Agent_Config_Widget(parent=self),
            #     tree_width=600,
            #     tree_header_hidden=True,
            #     folder_key='agents'
            # )
            # self.tree_config.tree.setSortingEnabled(False)
            # # self.tree_config = TreeConfig(self)
            # self.tree_config.build_schema()
            #
            # self.tree_config.tree.itemDoubleClicked.connect(self.on_row_double_clicked)
            #
            # self.layout.addWidget(self.tree_config)
            # self.layout.addStretch(1)

        def load(self):
            pass