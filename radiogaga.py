#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import curses, sys, subprocess, os

class Radiogaga:
	keylist = [] 
	channel = {}
	debuglist = []

	def __init__(self):
		# start curses
		stdscr = curses.initscr()
		curses.def_shell_mode()
		# Keine Anzeige gedrückter Tasten
		curses.noecho()
		# Kein line-buffer
		curses.cbreak()
		# Escape-Sequenzen aktivieren
		stdscr.keypad(1)
		self.channelDict()
		self.playRadio(stdscr)
	
	def channelDict(self):
		# fetch the list of channels
		filename = "/var/www/channels.txt"
		FILE = open(filename,"r+")
		for line in FILE:
                	ziffer, sender, info  = line.split(";")
			self.channel[ziffer] = sender

	def exitCurses(self, stdscr):
		# Ende
		curses.nocbreak()
		stdscr.keypad(0)
		curses.echo()
		curses.endwin()
		# cannot restore normal mode after curses-exit, wtf?
		curses.reset_shell_mode()
		print "ending radio session"

	def getNumKey(self, c):
		if c == 27: # Escape
			return 'ESC'
		elif c == curses.KEY_DOWN: # keycode: 258			
			return self.channel['2']
		elif c == curses.KEY_UP: # keycode: 259 
			return self.channel['8']
		elif c == curses.KEY_LEFT: # keycode: 260 
			return self.channel['4']
		elif c == curses.KEY_RIGHT: # keycode: 261 
			return self.channel['6']
		elif c == 262: # NUM 7
			return self.channel['7']
		elif c == 339: # NUM 9
			return self.channel['9']
		elif c == 338: # NUM 3
			return self.channel['3']	
		elif c == 360: # NUM 1
			return self.channel['1']
		elif c == 84:
			return self.channel['5']
		elif c == 43: # NUM +
			return '+'
		elif c == 45: # NUM -
			return '-'
		elif c == 331: # NUM 0
			return self.channel['10']
		elif c == 330 or c == ',': # NUM ,
			return ','
		elif c == 44:
			return 'DEL'
		elif c == 47: # NUM /
			return '/'
		elif c == 42: # NUM x
			return 'x'
		elif c == 10: # NUM Enter
			return 'Enter'	
		elif c == 49: # 1
			return self.channel['11']
		elif c == 50: #2:
			return self.channel['12']
		elif c == 51: #3:
			return self.channel['13']
		elif c == 52: #4
			return self.channel['14']
		elif c == 53: #5
			return self.channel['15']
		elif c == 54: #6:
			return self.channel['16']
		elif c == 55: #7:
			return self.channel['17']
		elif c == 56: #8:
			return self.channel['18']
		elif c == 57: #9:
			return self.channel['19']
		elif c == 48: #0
			return self.channel['20']
		else:
			return ""
		

	def playRadio(self, stdscr):
		try:
			#default channel on startup
			actualChannel = "http://www.radioswissclassic.ch/live/mp3.m3u"
			radio1 = subprocess.Popen(['mpg123', '-@', actualChannel])	
			while True:			
				# Warten auf Tastendruck
				c = stdscr.getch()
				self.debuglist.append(c)
				actualChannel = self.getNumKey(c)
				self.keylist.append( actualChannel )
				if actualChannel != '':
					# Enter mutes the radio and reads in a new channel list
					if actualChannel == 'Enter':
						try:
							radio1.kill()
							self.channelDict()
						except:
							pass
					# ESC kills the radio
					elif actualChannel == 'ESC':
						try:
							radio1.kill()
							break
						except:
							pass
					# other keys: an other channel chosen
					else:
						try:
							radio1.kill()
						except:
							pass
						radio1 = subprocess.Popen(['mpg123', '-@', actualChannel])
					
		finally: 
			self.exitCurses(stdscr)
			print self.keylist
			print self.channel
			print self.debuglist

def main():
	radio = Radiogaga()

if __name__ == "__main__":
	sys.exit(main())
