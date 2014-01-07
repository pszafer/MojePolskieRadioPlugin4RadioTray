#!/bin/sh
echo "Script to install MojePolskieRadioPlugin on Ubuntu"
echo "It will prompt for password because it needs simplejson module for python to install"
echo "sudo apt-get install python-simplejson"
sudo apt-get install python-simplejson
killall radiotray
cp mojepolskieradio.glade ~/.local/share/radiotray/plugins/mojepolskieradio.glade
cp mojepolskieradio.plugin ~/.local/share/radiotray/plugins/mojepolskieradio.plugin
cp MojePolskieRadioPlugin.py ~/.local/share/radiotray/plugins/MojePolskieRadioPlugin.py

echo "Everything ready! You can run RadioTray now"
