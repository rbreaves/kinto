#!/usr/bin/env python3

# Copyright (C) 2017 Gopikrishnan R

"""
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import subprocess,time,os,gi.repository
gi.require_version('Budgie','1.0')
gi.require_version('Gtk','3.0')
from gi.repository import Budgie, GObject, Gtk

class Kinto(GObject.GObject, Budgie.Plugin):

	__gtype_name__ = "Kinto"

	def __init__(self):

		GObject.Object.__init__(self)

	def do_get_panel_widget(self, uuid):

		return KintoApplet(uuid)




class KintoApplet(Budgie.Applet):

	homedir = os.path.expanduser("~")
	kconfig = homedir+"/.config/kinto/kinto.py"

	box = Gtk.EventBox()
	revealer=Gtk.Revealer()                      # Contains individual restart actions
	button=Gtk.Button()                          # Restart Button, Restarts both panel & WM
	button.set_relief(Gtk.ReliefStyle.NONE)
	button_arrow=Gtk.Button()                    # Down arrow
	button_arrow.set_relief(Gtk.ReliefStyle.NONE)
	img = Gtk.Image.new_from_icon_name("kinto-invert", Gtk.IconSize.BUTTON)
	img_arrow=Gtk.Image.new_from_icon_name('pan-down-symbolic',Gtk.IconSize.BUTTON)
	revealed=False                               # Whether Gtk.Revealer is open or not.
	checkbox_autostart = Gtk.CheckButton()
	button_suspend = Gtk.Button()
	button_winmac = Gtk.Button()
	button_setscale = Gtk.Button()
	button_suspend.set_relief(Gtk.ReliefStyle.NONE)
	button_winmac.set_relief(Gtk.ReliefStyle.NONE)
	button_setscale.set_relief(Gtk.ReliefStyle.NONE)
	suspend_id=0
	winmac_id=0
	chkautostart_id=0
	autostart_bool = False

	# subprocess.Popen(['sh',homedir+'/.config/kinto/logoff.sh'])

	with open(kconfig) as configfile:
		autostart_line = configfile.read().split('\n')[1]

	if "autostart = true" in autostart_line.casefold():
		autostart_bool = True

	def __init__(self,uuid):
		Budgie.Applet.__init__(self)
		self.initUI()

	def initUI(self):
		self.popover = Budgie.Popover.new(self.box)
		seperator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
		self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)         # To store the Reset(Both) button and arrow
		self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)           # Main VBox
		self.vbox_buttons = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)   # Vbox inside revealer

		self.box.set_tooltip_text("Kinto")

		self.checkbox_autostart.set_label("Autostart")
		# self.checkbox_autostart.modify_fg(Gtk.STATE_NORMAL, Gtk.Gdk.color_parse('#366B7E'));
		if self.autostart_bool:
			# subprocess.Popen(['sudo', 'systemctl','restart','xkeysnail'])
			self.checkbox_autostart.set_active(True)
			self.chkautostart_id = self.checkbox_autostart.connect("clicked",self.setAutostart,False)
		else:
			# subprocess.Popen(['sudo', 'systemctl','stop','xkeysnail'])
			self.checkbox_autostart.set_active(False)
			self.chkautostart_id = self.checkbox_autostart.connect("clicked",self.setAutostart,True)
		# self.chkautostart_id = self.checkbox_autostart.connect("clicked",self.setAutostart,True)
		self.hbox.pack_start(self.checkbox_autostart,True,False,5)
		# self.hbox.pack_start(self.button_autostart,True,False,5)
		self.hbox.pack_end(seperator,True,False,0)
		self.vbox.pack_start(self.hbox,True,False,5)
		# self.vbox.pack_start(seperator,True,False,0)

		time.sleep(5)
		res = subprocess.Popen(['sudo', 'systemctl','is-active','--quiet','xkeysnail'])
		res.wait()
		
		if res.returncode == 0:
			# self.button_suspend = Gtk.Button("Suspend Kinto")
			self.button_suspend.set_label("Suspend Kinto")
			self.img.set_from_icon_name("kinto-invert", Gtk.IconSize.BUTTON)
			self.suspend_id = self.button_suspend.connect("clicked",self.suspend,True)
		else:
			# self.button_suspend = Gtk.Button("Enable Kinto")
			self.button_suspend.set_label("Enable Kinto")
			# self.img.set_from_icon_name("kinto", Gtk.IconSize.BUTTON)
			self.img.set_from_icon_name("kinto-color", Gtk.IconSize.BUTTON)
			self.suspend_id = self.button_suspend.connect("clicked",self.suspend,False)
		self.vbox.pack_start(self.button_suspend,True,False,5)
		# self.vbox.pack_start(seperator,True,False,0)

		self.box.add(self.img)
		self.box.connect("button-press-event", self.on_press)
		self.add(self.box)

		command = "perl -ne 'print if /(#.*)(# Mac)\n/' ~/.config/kinto/kinto.py | wc -l"
		res = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
		res.wait()
		res = res.communicate()[0]

		if True:
			self.button_winmac.set_label("Set Win/Mac KB Type")
			self.winmac_id = self.button_winmac.connect("clicked",self.setKB,"winmac")
		else:
			self.button_winmac.set_label("Set Mac Only KB Type")
			self.winmac_id = self.button_winmac.connect("clicked",self.setKB,"mac")
		self.vbox.pack_start(self.button_winmac,True,False,5)
		# self.vbox.pack_start(seperator,True,False,0)
		# self.hbox.pack_end(self.button_arrow,False,False,5)

		# if res.returncode == 0:
		# 	self.button_setscale.set_label("Set 1x DPI Scale")
		# 	self.button_setscale.connect("clicked",self.setScale,1)
		# else:
		# 	self.button_setscale.set_label("Set 2x DPI Scale")
		# 	self.button_setscale.connect("clicked",self.setScale,2)
		# self.vbox.pack_start(self.button_setscale,True,False,5)
		# self.vbox.pack_start(seperator,True,False,0)

		self.vbox.pack_start(self.hbox,False,False,5)
		self.vbox.pack_start(self.revealer,False,False,0)

		self.popover.add(self.vbox)

		self.popover.get_child().show_all()

		self.box.show_all()

		self.show_all()



	def	on_press(self, box, e):

		if e.button != 1:
			return Gdk.EVENT_PROPAGATE

		if self.popover.get_visible():
			self.revealer.set_visible(False)

		else:
			self.revealer.set_reveal_child(False)                                       # Close Revealer (if open) before showing popover
			self.img_arrow.set_from_icon_name('pan-down-symbolic',Gtk.IconSize.BUTTON)  # Reset to pan-down icon
			self.manager.show_popover(self.box)

	def do_update_popovers(self, manager):

		self.manager = manager
		self.manager.register_popover(self.box, self.popover)

	def change_icon(self):
		""" Change arrow to down/up """

		if not self.revealed:
			self.img_arrow.set_from_icon_name('pan-up-symbolic',Gtk.IconSize.BUTTON)
			self.revealed=True

		else:
			self.img_arrow.set_from_icon_name('pan-down-symbolic',Gtk.IconSize.BUTTON)
			self.revealed=False

	def revealer_show(self,button):
		""" Open/Close the revealer """

		if self.revealer.get_reveal_child():
			self.change_icon()
			self.revealer.set_reveal_child(False)

		else:
			self.change_icon()
			self.revealer.set_reveal_child(True)

	def suspend(self,button,suspendKinto):
		try:
			if suspendKinto:
				subprocess.Popen(['sudo', 'systemctl','stop','xkeysnail'])
				self.button_suspend.set_label("Enable Kinto")
				self.img.set_from_icon_name("kinto-color", Gtk.IconSize.BUTTON)
				self.button_suspend.disconnect(self.suspend_id)
				self.suspend_id = self.button_suspend.connect("clicked",self.suspend,False)
				self.box.add(self.img)

			else:
				subprocess.Popen(['sudo', 'systemctl','restart','xkeysnail'])
				self.button_suspend.set_label("Suspend Kinto")
				self.img.set_from_icon_name("kinto-invert", Gtk.IconSize.BUTTON)
				self.button_suspend.disconnect(self.suspend_id)
				self.suspend_id = self.button_suspend.connect("clicked",self.suspend,True)
				self.box.add(self.img)

		except subprocess.CalledProcessError:                                  # Notify user about error on running restart commands.
			subprocess.Popen(['notify-send','Kinto: Error Suspending!','-i','budgie-desktop-symbolic'])

	def setKB(self,button,kbtype):
		try:
			if kbtype == "winmac":
				label = "Set Mac KB Type"
				connect = "mac"

				setwinmac = ['s/^(\s{3})(\s{1}#)(.*# WinMac\n|.*# WinMac -)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(Mac\n|Mac -)/   $3$7$6$7$8/g']

			else:
				label = "Set Win/Mac KB Type"
				connect = "winmac"

				setwinmac = ['s/^(\s{3})(\s{1}#)(.*# Mac\n|.*# Mac -)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(WinMac)/   $3$7$6$7$8/g']

			restart = ['sudo', 'systemctl','restart','xkeysnail']
			# restart = "sudo systemctl restart xkeysnail"
			# stop = "sudo systemctl stop xkeysnail"
			# start = "sudo systemctl start xkeysnail"
			cmds = ['perl','-pi','-e']+setwinmac+[self.kconfig]

			subprocess.Popen(cmds)

			cmdsTerm = subprocess.Popen(cmds)
			cmdsTerm.wait()

			subprocess.Popen(restart)
			# cmdsTerm.kill()
			# stopTerm = subprocess.Popen(stop,shell=True)
			# stopTerm.wait()
			# stopTerm.kill()
			# time.sleep(2)
			# startTerm = subprocess.Popen(start,shell=True)
			# startTerm.wait()
			# startTerm.kill()

			self.button_winmac.set_label(label)
			self.button_winmac.disconnect(self.winmac_id)
			self.winmac_id = self.button_winmac.connect("clicked",self.setKB,connect)

		except subprocess.CalledProcessError:                                  # Notify user about error on running restart commands.
			subprocess.Popen(['notify-send','Kinto: Error Reseting KB Type!','-i','budgie-desktop-symbolic'])

	def setAutostart(self,button,kbtype):
		print('test')
	
	def setScale(self,button,scale):
		print("scale")

#END
