##########################################################################
# Copyright 2013 Carlos Ribeiro
#
# This file is part of Radio Tray
#
# Radio Tray is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 1 of the License, or
# (at your option) any later version.
#
# Radio Tray is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Radio Tray.  If not, see <http://www.gnu.org/licenses/>.
#   Author of this plugin: Pawel Szafer, pszafer@gmail.com
#
##########################################################################
from Plugin import Plugin
import gtk
import gobject
import urllib2
from lib import utils
import os
from lib.common import SYSTEM_PLUGIN_PATH, USER_PLUGIN_PATH
import base64, socket
import simplejson as myjson

class MojePolskieRadioPlugin(Plugin):
    def __init__(self):
        super(MojePolskieRadioPlugin, self).__init__()
        
    def activate(self):
        if os.path.exists(os.path.join(USER_PLUGIN_PATH, "mojepolskieradio.glade")):
            self.gladefile = utils.load_ui_file(os.path.join(USER_PLUGIN_PATH, "mojepolskieradio.glade"))
        elif os.path.exists(os.path.join(SYSTEM_PLUGIN_PATH, "mojepolskieradio.glade")):
            self.gladefile = utils.load_ui_file(os.path.join(SYSTEM_PLUGIN_PATH, "mojepolskieradio.glade"))
        else:
            self.log.error('Error initializing MojePolskieRadio plugin: mojepolskieradio.glade not found')
        self.window = self.gladefile.get_object('dialog1')
        if (self.window):
            self.gladefile.connect_signals(self)
        
        
    def getName(self):
        return self.name    
        
    def on_menu(self, data):
        self.window.show()
        
    def on_run_clicked(self, widget):
        self.putIntoBookmarksMojePolskieRadioStations()
        return
        
    def on_close_clicked(self, widget):
        self.window.hide()
        return True
    def putIntoBookmarksMojePolskieRadioStations(self):
        groupName = "Moje Polskie Radio"
        CHANNELS_URL    = 'http://moje.polskieradio.pl/api/?key=%s&output=json'
        A_I_K           = 'MjJhZmMzNzg2NzQxLWRlZDktMjU4NC02NmViLWZkZjkzNDAy'    
        parent_group = "root"
        self.provider.addGroup(parent_group, groupName)
        groupIndex = self.provider.listGroupNames().index(groupName)
        aik = base64.b64decode(A_I_K)
        u = urllib2.urlopen(CHANNELS_URL % aik[::-1])
        jsonString = myjson.loads(u.read())
        u.close()
        channels = jsonString['channel']
        for channel in channels:
            name = channel['title']
            streams = channel["AlternateStationsStreams"]
            for stream in streams:
                if stream['name'] == "mp3":
                    url = stream['link']
                    break
            if len(name) > 0 and len(url) > 0:
                if self.provider._radioExists(name):
                    self.provider.updateRadio(name, name, url)
                else:
                    self.provider.addRadio(name, url, groupName)
        self.eventManagerWrapper.notify('Moje Polskie Radio', 'All stations downloaded. Reload bookmarks now!')
    def hasMenuItem(self):
        return True
