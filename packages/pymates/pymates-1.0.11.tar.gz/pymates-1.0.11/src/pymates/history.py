import os, json
from collections import defaultdict
from copy import deepcopy
from .pokeutil import DEFAULT, pokes

PATH = "/".join(__file__.split("/")[:-1])
#print(os.path.exists(f"{PATH}/history.json"))

class History():
	def __init__(self, fn=f"{PATH}/history.json"):
		self.fn = fn
		if os.path.isfile(fn):
			self.load()
		else:
			self.data = {}
			self.regen_dict()
	
	def regen_dict(self):
		data = defaultdict(int)
		for k, i in DEFAULT.items():
			data[k] = deepcopy(i)
			
		for k, i in self.data.items():
			for m in ["Moltres", "Zapdos", "Articuno", "Entei", "Raiku", "Suicune", "Shiny"]:
				if m in k:
					data[k] = self.data[k]
		self.data = data
		self.save()
	
	@property
	def shinies(self):
		ignore = {
			"showtotal",
		    "pcttotal",
		    "pct",
		    "Tracking",
		    "Last_Addition",
		    "bonus"}
		    
		i = 0
		for key, item in self.data.items():
			if key in ignore:
				continue
			if "Shiny" in key:
				i += item
		return i
		
	@property
	def legends(self):
		ignore = {
			"showtotal",
		    "pcttotal",
		    "pct",
		    "Tracking",
		    "Last_Addition",
		    "bonus"}
		i = 0
		for key, item in self.data.items():
			if key in ignore:
				continue
			if key in {"Zapdos", "Moltres", "Articuno", "Entei", "Raiku", "Suicune"}:
				i += item
		return i
		
	@property
	def showtotal(self):
		return self.data["showtotal"]
		
	def toggle_total(self):
		self.data["showtotal"] = not self.data["showtotal"]
		self.save()
	
	def load(self):
		#print("Loading")
		with open(self.fn) as f:
			s = json.loads(f.read())
			self.data = s
		return s
	
	def save(self):
		#print("Saving")
		with open(self.fn, "w") as f:
			s = json.dumps(self.data, indent=4)
			f.write(s)
	
	def setbonus(self, charm=False, linkcharm=False, donator=False):
		
		
			
		self.data["bonus"] = {	"charm": charm,
												"linkcharm": linkcharm,
												"donator": donator	}
	
	@property
	def charm(self):
		return self.data["bonus"]["charm"]
		
	@property
	def linkcharm(self):
		return self.data["bonus"]["linkcharm"]
		
	@property
	def donator(self):
		return self.data["bonus"]["donator"]
	
	def getbonus(self):
		if self.charm and self.linkcharm:
			linkcharm = False
		else:
			linkcharm = self.linkcharm
		
		if self.charm is True:
			charm = 0.1
		else:
			charm = 0
		
		if linkcharm is True:
			linkcharm = 0.05
		else:
			linkcharm = 0
		
		if self.donator is True:
			donator = 0.1
		else:
			donator = 0
		
		return linkcharm + charm + donator
	
	def track(self, mon):
		if mon not in self.data["Tracking"]:
			self.data["Tracking"].append(mon)
		self.save()
	
	def untrack(self, mon):
		if mon in self.data["Tracking"]:
			self.data["Tracking"].remove(mon)
		self.save()
				
	
	def addsingle(self):
		if "Singles" not in self.data.keys():
			self.data["Singles"] = 1
		else:
			self.data["Singles"] += 1
		self.save()
		
	def sub(self, mons):
			self.data["Last_Addition"] = None
			mons = mons.split(", ")
			if type(mons) is str:
				mons=[mons]
			for mon in mons:
				qty, mon = mon.split("*")
				qty = int(qty)
				mon = mon.replace(" ", "")
				if mon in self.data.keys():
					self.data[mon] -= qty
				
				if self.data[mon] < 1:
						del self.data[mon]

			self.save()
	
	
	def add(self, mons):
			self.data["Last_Addition"] = mons
			mons = mons.split(", ")
			if type(mons) is str:
				mons=[mons]
			for mon in mons:
				qty, mon = mon.split("*")
				qty = int(qty)
				mon = mon.replace(" ", "")
				if mon in self.data.keys():
					self.data[mon] += qty
				else:
					self.data[mon] = qty
					
				
			self.save()
	
	@property
	def total(self):
		out = 0
		for k, i in self.data.items():
			if k in ("Last_Addition", "Tracking", "showtotal", "pcttotal", "pct", "bonus", "Singles"):
				continue
			out += int(i)
		return out
	
	def undo(self):
		if self.data["Last_Addition"] == None:
			return
		self.sub(self.data["Last_Addition"])
	
	def reset(self, mon=""):
		if mon == "":
			self.data = defaultdict(int)
		if mon in self.data.keys():
			self.data["Total"] -= self.data[mon]
			self.data[mon] = 0
		self.save()
		