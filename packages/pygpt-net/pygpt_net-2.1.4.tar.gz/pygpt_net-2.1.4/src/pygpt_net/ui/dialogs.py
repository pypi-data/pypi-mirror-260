#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.02.27 19:00:00                  #
# ================================================== #

from pygpt_net.ui.dialog.about import About
from pygpt_net.ui.dialog.applog import AppLog
from pygpt_net.ui.dialog.assistant import Assistant
from pygpt_net.ui.dialog.changelog import Changelog
from pygpt_net.ui.dialog.create import Create
from pygpt_net.ui.dialog.debug import Debug
from pygpt_net.ui.dialog.dictionary import Dictionary
from pygpt_net.ui.dialog.editor import Editor
from pygpt_net.ui.dialog.image import Image
from pygpt_net.ui.dialog.license import License
from pygpt_net.ui.dialog.logger import Logger
from pygpt_net.ui.dialog.models import Models
from pygpt_net.ui.dialog.plugins import Plugins
from pygpt_net.ui.dialog.preset import Preset
from pygpt_net.ui.dialog.rename import Rename
from pygpt_net.ui.dialog.settings import Settings
from pygpt_net.ui.dialog.snap import Snap
from pygpt_net.ui.dialog.start import Start
from pygpt_net.ui.dialog.update import Update
from pygpt_net.ui.widget.dialog.alert import AlertDialog
from pygpt_net.ui.widget.dialog.confirm import ConfirmDialog


class Dialogs:
    def __init__(self, window=None):
        """
        Dialogs setup

        :param window: Window instance
        """
        self.window = window
        self.about = About(self.window)
        self.assistant = Assistant(self.window)
        self.app_log = AppLog(self.window)
        self.changelog = Changelog(self.window)
        self.create = Create(self.window)
        self.debug = Debug(self.window)
        self.dictionary = Dictionary(self.window)
        self.editor = Editor(self.window)
        self.image = Image(self.window)
        self.license = License(self.window)
        self.logger = Logger(self.window)
        self.preset = Preset(self.window)
        self.rename = Rename(self.window)
        self.snap = Snap(self.window)
        self.start = Start(self.window)
        self.update = Update(self.window)

    def setup(self):
        """Setup dialogs"""
        for id in self.window.controller.dialogs.debug.ids:
            self.debug.setup(id)

        self.about.setup()
        self.app_log.setup()
        self.changelog.setup()
        self.create.setup()
        self.preset.setup()
        self.assistant.setup()
        self.editor.setup()
        self.rename.setup()
        self.snap.setup()
        self.start.setup()
        self.update.setup()
        self.image.setup()
        self.license.setup()
        self.logger.setup()

        self.window.settings = Settings(self.window)
        self.window.plugin_settings = Plugins(self.window)
        self.window.model_settings = Models(self.window)
        self.window.ui.dialog['alert'] = AlertDialog(self.window)
        self.window.ui.dialog['confirm'] = ConfirmDialog(self.window)

    def post_setup(self):
        """Post setup dialogs (after plugins and rest of data is registered)"""
        self.dictionary.setup()

    def confirm(
            self,
            type: str,
            id: any,
            msg: str,
            parent_object=None
    ):
        """
        Show confirm dialog

        :param type: confirm type
        :param id: confirm object id
        :param msg: message to show
        :param parent_object: parent object
        """
        self.window.ui.dialog['confirm'].type = type
        self.window.ui.dialog['confirm'].id = id
        self.window.ui.dialog['confirm'].message.setText(msg)
        self.window.ui.dialog['confirm'].parent_object = parent_object
        self.window.ui.dialog['confirm'].show()

    def alert(self, msg):
        """
        Show alert dialog

        :param msg: message to show
        """
        self.window.ui.dialog['alert'].message.setPlainText(msg)
        self.window.ui.dialog['alert'].show()

    def open_editor(self, id: str, data_id: str, width: int = 400, height: int = 400):
        """
        Open editor dialog

        :param id: editor dialog id
        :param data_id: data id
        :param width: dialog width
        :param height: dialog height
        """
        if id not in self.window.ui.dialog:
            return
        self.window.ui.dialog[id].resize(width, height)
        self.window.ui.dialog[id].data_id = data_id
        self.window.ui.dialog[id].show()

    def open_dictionary_editor(
            self,
            id: str,
            option: dict,
            data: dict,
            idx: int,
            width: int = 400,
            height: int = 400
    ):
        """
        Open dictionary editor dialog

        :param id: dictionary editor id (parent id . option key)
        :param option: dictionary option keys
        :param data: data
        :param idx: index on list (needed to save update)
        :param width: dialog width
        :param height: dialog height
        """
        dialog_id = "editor.dictionary." + id
        if dialog_id not in self.window.ui.dialog:
            print("Dialog not found: " + dialog_id)
            return
        self.window.controller.config.dictionary.append_editor(id, option, data)
        self.window.ui.dialog[dialog_id].resize(width, height)
        self.window.ui.dialog[dialog_id].data = data  # store editing data
        self.window.ui.dialog[dialog_id].idx = idx  # store editing record idx
        self.window.ui.dialog[dialog_id].show()

    def register_dictionary(
            self,
            key: str,
            parent: str,
            option: dict
    ):
        """
        Register dictionary data to dictionary editor

        :param key: option key (main dictionary key)
        :param parent: parent id
        :param option: dictionary option keys
        """
        dict_id = parent + "." + key
        self.dictionary.register(dict_id, key, parent, option)

    def open(
            self,
            id: str,
            width: int = 400,
            height: int = 400
    ):
        """
        Open dialog

        :param id: dialog id
        :param width: dialog width
        :param height: dialog height
        """
        if id not in self.window.ui.dialog:
            return
        self.window.ui.dialog[id].resize(width, height)
        qr = self.window.ui.dialog[id].frameGeometry()
        cp = self.window.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.window.ui.dialog[id].move(qr.topLeft())
        self.window.ui.dialog[id].show()

    def close(self, id: str):
        """
        Close dialog

        :param id: dialog id
        """
        if id not in self.window.ui.dialog:
            return
        self.window.ui.dialog[id].close()
