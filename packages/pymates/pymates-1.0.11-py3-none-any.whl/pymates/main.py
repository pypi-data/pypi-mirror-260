from .history import History
from .pokeutil import *
from .windows import *
import numpy as np
from .console import console
import datetime
import curses
from copy import deepcopy
from .mons import get_names


__ver__="1.0.11"



def handle_mons(cap, reported, singles=False, w=3040, h=1440, history = None):
	com = False
	
	#Count health bars
	cropped = np.array(deepcopy(cap).crop((0,0,w,h//3.6)))
	
	n_mons = count_mons(cropped)
	
	
	#get mons names
	
	out = ""
	
		
	if n_mons > 0:
		com = True
		mons = get_names(cap)
		
			
		tries = 1
		
		while tries < 3 and len(mons) < n_mons:
			cap = capture()
			mons = get_names(cap)
			tries += 1
			
			if len(mons) < n_mons or mons == "[]":
				time.sleep(0.3)
			else:
				break
		
		if mons in ["[]", []]:
			mons = "Unrecognised"
				
		if reported:
			return com, reported, out
		
		if len(mons) < 1:
			return com, reported, out
			
		#reports the mon
		reported = True
		if True in [True if "Shiny" in m else False for m in mons]:
			shiny = True
		else:
			shiny = False
		
		for m in mons:
			if m in ["Zapdos", "Moltres", "Articuno", "Entei", "Raiku", "Suicune"]:
				legend = True
		else:
			legend = False
		
		ti = str(datetime.datetime.now()).split(".")[0]
		log(f"[{ti}]:", list_to_words(mons))
		#adds it to the history
		
		if singles:
			history.addsingle()
		history.add(list_to_words(mons))
			
		if shiny or legend:
			os.system(f"screencap -p {PATH}/screenshots/GG{mons[0]}.png")
			
			out = "GG!! " + list_to_words(mons)
		else:
			out = "+"+list_to_words(mons)
			
			
	else:
		reported = False
			
	return com, reported, out
		

"""		
proportions = get_device_proportions()
device_y, device_x = min(proportions), max(proportions)
	"""	

def main(scr):
	
	history = History()
	hp = cv2.imread(f"{PATH}/hp.png", 0)
	
	#Initialising ths colours
	curses.start_color()
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
	curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
	curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
	
	
	#hides cursor
	curses. curs_set(0)
	
	#height and width of the terminal
	h, w = scr.getmaxyx()
	
	splash_screen(scr, "MATES", w, h//2, subtitle="Encounter Tracker", author="Th3M4ttman", ver=__ver__, speed=7, delay=5) 
	
	
	#Auto capture off by default
	capturing = False
	
	#stops waiting on input
	scr.nodelay(True)
	
	#initialising the windows
	capwin = Capture(1, w, 0, 1, history)
	total_window = Counter("Total", 1,w, 1, 0, history)
	
	#time until next clear of the output field
	clear_timer = None
	
	text =">: " #cmd input
	out = "" #cmd output
	
	mons = history.data["Tracking"] #which mons to track
	
	def regen(scr, mons, w):
		#regenerates a tracking window for each mon in mons
		windows = []
		
		for i, mon in enumerate(mons):
			windows.append(Counter(mon, i+2, w, i+2, 0, history))
			
		return windows, len(windows)+2, len(windows)+3
	
	#generating windows
	windows, input_line, output_line = regen(scr, mons, w)
	
	#whether the pokemon on screen has been reported yet
	reported = True 
	
	#timer to next auto capture
	cap_timer = datetime.datetime.now()
	c = combat(1, w, 0, h-1, max_w=w)
	in_combat=False
	
	#timer to next auto capture
	cap_timer = datetime.datetime.now()
	
	singles = "Singles" in history.data["Tracking"]
	#main program loop
	while True:
		
		_h, _w = h, w
		h, w = scr.getmaxyx()
		if (h, w) != (_h, _w):
			
			
			"""
			c.clear()
			c.window.move(0, h-1)
			c.window.resize(1, w)
			c.refresh()"""
			scr.clear()
			del c
			c = combat(1, w, 0, h-1, max_w=w)
			
			"""
			capwin.clear()
			capwin.window.resize(1, w)
			capwin.window.move(0, 1)
			capwin.refresh()"""
			
			del capwin
			capwin = Capture(1, w, 0, 1, history)
	
			mons = history.data["Tracking"]
			regen(scr, mons, w)
			
		mons = []
		
		c.refresh(in_combat, reported, singles, history.shinies, history.legends)
		
		#clears output every 4 seconds
		if clear_timer:
			if datetime.datetime.now() > clear_timer:
				out = ""
				clear_timer = None
				scr.clear()
			
				try:
					scr.addstr(input_line,0, text)
					scr.addstr(output_line, 0, " "*(w-1))
					regen(scr, mons, w)
					c.window.clear()
				except Exception as e:
					if "addwstr" not in str(e):
						raise e
				
		
		
		#Auto capture
		if capturing and datetime.datetime.now() > cap_timer:
			cap = capture() 
			if cap:
				cropped = np.array(deepcopy(cap).crop((0,0,w,h//3.6)))
				
				in_combat, reported, _out = handle_mons(cap, reported, singles=singles, history=history)
				
				if _out != "":
					out = _out
					clear_timer = datetime.datetime.now() + datetime.timedelta(seconds=8)
				
		
		
		#sets the visibility of the total encounters
		total_window.visible = history.showtotal
		
		#updates the total encounters
		total_window.set(history.total)
		
		#update each of the counters
		for window in windows:
			if window.title in history.data.keys():
				n = history.data[window.title]
			else:
				n = 0
			
			if window.value != n:
				window.set(n)
			else:
				window.refresh()
		
		#updates the capture indicator
		capwin.set(capturing)
		
		#getting keyboard input
		try:
			key = scr.getkey()
		except:
			key = ""
		
		if key == "\n": #run command
			if text.replace(">: ", "") in ("quit", "exit", "qq"):
				return #exit the program
			try:
				if text.replace(">: ", "") == "": #press enter to toggle capture
					capturing = not capturing
				else: #execute command
					out = console(text.replace(">: ", ""), history)
					history.save()
					
				if out == "Toggled singles tracking":
					singles = not singles
					if singles:
						history.track("Singles")
					else:
						history.untrack("Singles")
					windows, input_line, output_line = regen(scr, history.data["Tracking"], w)
				
				#regenerate the tracking windows
				if "Tracking" in out or "Untracking" in out or "Untracked" in out:
					windows, input_line, output_line = regen(scr, history.data["Tracking"], w)
				
				#reset the terminal area
				text =">: "
				scr.clear()
				clear_timer = datetime.datetime.now() + datetime.timedelta(seconds=3)
					
					
			except Exception as e:
				out = ""
				text =">: "
				if "addwstr" not in str(e):
					raise e
				
		elif key in abc: #add letter to the input
			text += key
			
		elif key == "\x7f": #backspace
			if len(text) > 3:
				text = text[:-1]
			scr.clear() 
		
		try: #command output
			try:
				scr.addstr(input_line,0, text, curses.color_pair(5))
				
				if "toggled" in out.lower() or "Initialised" in out:
					colour = curses.color_pair(4)
					scr.addstr(output_line,0, out, colour)
					hp = cv2.imread(f"{PATH}/hp.png", 0)
				
				elif "track" in out.lower():
					colour = curses.color_pair(4)
					scr.addstr(output_line,0, out, colour)
					
				elif "add" in out.lower() or "+" in out.lower():
					colour = curses.color_pair(1)
					
					if "+" in out.lower():
						if "," in out.lower():
							mons = [m.split("* ") for m in out.replace("+", "").split(", ")]
						else:
							mons = [out.replace("+", "").split("* ")]
							
						i = 0
						for qty, mon in mons:
							if "Shiny" in mon:
								colour = curses.color_pair(4)
								
							elif mon in {"Moltres", "Zapdos", "Articuno", "Entei", "Raiku", "Suicune"}:
								colour = curses.color_pair(5)
							else:
								colour = curses.color_pair(1)
								
							string = qty + "x " + mon + (", "  if i > 0 else "")
							scr.addstr(output_line,i, string, colour)
							i += len(string) + 1
							
							
						
					elif "add" in out.lower():
						qty, mon = out.split("* ")
						qty = qty.split(" ")[-1]
						
						scr.addstr(output_line,0, qty+"x ", colour)
						
						if "Shiny" in mon:
							colour = curses.color_pair(4)
						elif mon in {"Moltres", "Zapdos", "Articuno", "Entei", "Raiku", "Suicune"}:
							colour = curses.color_pair(5)
						else:
							colour = curses.color_pair(1)
							
						scr.addstr(output_line, len(qty)+2, mon, colour)
						
						
				elif "sub" in out.lower() or "-" in out.lower():
					colour = curses.color_pair(2)
					
					if "-" in out.lower():
						if "," in out.lower():
							mons = [m.split("* ") for m in out.replace("-", "").split(", ")]
						else:
							mons = [out.replace("-", "").split("* ")]
							
						i = 0
						for qty, mon in mons:
							if "Shiny" in mon:
								colour = curses.color_pair(4)
								
							elif mon in {"Moltres", "Zapdos", "Articuno", "Entei", "Raiku", "Suicune"}:
								colour = curses.color_pair(5)
							else:
								colour = curses.color_pair(2)
								
							string = qty + "x " + mon + (", "  if i > 0 else "")
							scr.addstr(output_line,i, string, colour)
							i += len(string) + 1
							
							
						
					elif "sub" in out.lower():
						qty, mon = out.split("* ")
						qty = qty.split(" ")[-1]
						
						scr.addstr(output_line,0, qty+"x ", colour)
						
						if "Shiny" in mon:
							colour = curses.color_pair(4)
						elif mon in {"Moltres", "Zapdos", "Articuno", "Entei", "Raiku", "Suicune"}:
							colour = curses.color_pair(5)
						else:
							colour = curses.color_pair(2)
							
						scr.addstr(output_line, len(qty)+2, mon, colour)
					
				else:
					colour= curses.color_pair(5)
					scr.addstr(output_line, 0, out, colour)
				
				
			except Exception as e:
				if "addwstr" not in str(e):
					raise e
					
				scr.addstr(output_line,0, "Error "+str(e))
				clear_timer = datetime.datetime.now() + datetime.timedelta(seconds=10)
					
		except Exception as e:
			if "addwstr" not in str(e):
				raise e
			scr.addstr(output_line,0, "Error "+str(e))
			clear_timer = datetime.datetime.now() + datetime.timedelta(seconds=10)
			out = ""
		
	
		scr.refresh()
		
		time.sleep(.2)
	return 

#run program
def run():
	curses.wrapper(main)

if __name__ == "__main__":
	run()
