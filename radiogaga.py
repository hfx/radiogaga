#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import curses, sys, subprocess

class Radiogaga:
	keylist = [] 
	channel = {}
	debuglist = []

	def __init__(self):
		# start curses
		stdscr = curses.initscr()
		# Keine Anzeige gedrückter Tasten
		curses.noecho()
		# Kein line-buffer
		curses.cbreak()
		# Escape-Sequenzen aktivieren
		stdscr.keypad(1)
		self.channelDict()
		self.playRadio(stdscr)
	
	def channelDict(self):
		"""
		fobj = open("channels.txt", "r")
		for line in fobj:
			print line
			#l = line.split[' ']
			#self.channel[ l[0] ] = l[1]
		fobj.close()
		
		"""	
		self.channel = {
				"1" : "http://www.radioswissclassic.ch/live/mp3.m3u",
				"2" : "http://www.inforadio.de/live.m3u",
				"3" : "http://www.dradio.de/streaming/dlf.m3u",
				"4" : "http://edge.live.mp3.mdn.newmedia.nacamar.net/klassikradio128/livestream.mp3",
				"5" : "",
				"6" : "http://www.ndr.de/resources/metadaten/audio/m3u/ndrinfo.m3u",
				"7" : "http://www.dradio.de/streaming/dkultur.m3u", 
				"8" : "http://85.239.108.41/90elf_basis_hq",
				"9" : "http://www.wdr.de/wdrlive/media/fhe.m3u", # funkhaus europa
				"10" : "http://www.multicult.fm/fileadmin/stream/multicult.FM.m3u", # multicult2.0 #kaputt
				"11" : "http://mp3stream7.apasf.apa.at:8000", # ö3
				"12" : "http://srvhost24.serverhosting.apa.net:8000/rsdstream128.m3u", # stephansdom
				"13" : "http://www.latinastereo.com/html/listen.pls", # salsa
				"14" : "http://radio.memonet.ru:8000/echo.mp3",
				"15" : "http://www.dradio.de/streaming/dradiowissen.m3u",
				"16" : "http://stream.berliner-rundfunk.de/brf/mp3-128/internetradio/",
				"17" : "http://listen.radionomy.com/Radio-Cubana",
				"18" : "http://stream.hoerradar.de/antennemv-mp3.m3u",
				"19" : "http://85.239.108.41/90elf_rp01",
				"20" : "http://85.239.108.41/90elf_rp02",
			}
		
	def exitCurses(self, stdscr):
		# Ende
		curses.nocbreak()
		stdscr.keypad(0)
		curses.echo()
		curses.endwin()

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
			channel = "http://www.radioswissclassic.ch/live/mp3.m3u"
			radio1 = subprocess.Popen(['mpg123', '-@', channel])	
			while True:			
				# Warten auf Tastendruck
				c = stdscr.getch()
				self.debuglist.append(c)
				channel = self.getNumKey(c)
				self.keylist.append( channel )
				if channel != '':
					if channel == 'Enter':
						radio1.kill()
						#subprocess.Popen(['shutdown', '-h', 'now'])	
						#break
					elif channel == 'DEL':
						try:
							radio1.kill()
						except:
							pass
						#break
						subprocess.Popen(['shutdown', '-h', 'now'])
				
			
					else:
						try:
							radio1.kill()
						except:
							pass
						radio1 = subprocess.Popen(['mpg123', '-@', channel])
					
				#break

			
					

			#	if c == "[H":
			#		break
			#		radio1 = subprocess.Popen(['mpg123', '-@', 'http://www.radioswissclassic.ch/live/mp3.m3u'])
			#	elif c == 2:
			#		print c
			#		radio1.kill()	



		finally: 
			self.exitCurses(stdscr)
			print self.keylist
			print self.channel
			print self.debuglist

def main():
	radio = Radiogaga()

if __name__ == "__main__":
	sys.exit(main())
