from .pokeutil import pokes, init
from difflib import get_close_matches

def get_poke(string):
	string = str(string).title()
	if string in pokes:
		return string
	
	matches = get_close_matches(string, pokes)
	if len(matches) > 0:
		return matches[0]
	
	return None


def console(cmd, history):
	parts = cmd.split(" ")
	
	if parts[0] == "init":
		if len(parts) == 5:
			_, left, top, right, bottom = parts
			init(None, int(left), int(top), int(right), int(bottom))
			return f"Initialised with dimensions {[int(i) for i in [left, top, right, bottom]]}"
		else:
			init()
			return "Initialised"
			
	if parts[0] == "singles":
		return "Toggled singles tracking"
		
	if parts[0] == "charm":
		history.setbonus(charm=not history.charm, linkcharm=history.linkcharm, donator=history.donator)
		return "Toggled Shiny Charm"
		
	elif parts[0] == "link":
		history.setbonus(charm=history.charm, linkcharm=not history.linkcharm, donator=history.donator)
		return "Toggled Shiny Charm Link"
		
	elif parts[0] == "donator":
		history.setbonus(charm=history.charm, linkcharm=history.linkcharm, donator=not history.donator)
		return "Toggled Donator"
	
	if parts[0] in ("+", "add"):
		if parts[1].isnumeric():
			if get_poke(parts[2]) in pokes:
				history.add(f"{parts[1]}* {get_poke(parts[2])}")
				return f"Added {parts[1]}* {get_poke(parts[2])}"
			elif parts[2].title() == "Shiny":
				if get_poke(parts[3]) in pokes:
					history.add(f"{parts[1]}* Shiny {get_poke(parts[3])}")
					return f"Added {parts[1]}* Shiny {get_poke(parts[3])}"
				else:
					return f"{parts[3].title()} not found"
			else:
				return f"{parts[2].title()} not found"
		else:
			return f"{parts[1]} is not a number"
			
	if parts[0][0] == "+" and parts[0].replace("+", "").isnumeric():
		if get_poke(parts[1]) in pokes:
			history.add(f"{parts[0][1:]}* {get_poke(parts[1])}")
			return f"Added {parts[0][1:]}* {get_poke(parts[1])}"
		else:
			return f"{parts[1].title()} not found"
			
	if parts[0]  in ("-", "sub"):
		if parts[1].isnumeric():
			if get_poke(parts[2]) in pokes:
				history.sub(f"{parts[1]}* {get_poke(parts[2])}")
				return f"Subtracted {parts[1]}* {get_poke(parts[2])}"
			elif parts[2].title() == "Shiny":
				if get_poke(parts[3]) in pokes:
					history.sub(f"{parts[1]}* Shiny {get_poke(parts[3])}")
					return f"Subtracted {parts[1]}* Shiny {get_poke(parts[3])}"
				else:
					return f"{parts[3].title()} not found"
			else:
				return f"{parts[2].title()} not found"
		else:
			return f"{parts[1]} is not a number"
			
	if parts[0][0] == "-" and parts[0][1:].isnumeric():
		if get_poke(parts[1]) in pokes:
			history.sub(f"{parts[0][1:]}* {get_poke(parts[1])}")
			return f"Subtracted {parts[0][1:]}* {get_poke(parts[1])}"
		else:
			return f"{parts[1].title()} not found"
			
	if parts[0] in ["reset", "r"]:
		if len(parts) > 1:
			if get_poke(parts[1]) in pokes:
				del history.data[get_poke(parts[1])]
				return  "Reset " + get_poke(parts[1])
			else:
				return f"No such pokemon: {parts[1].title()}"
		history.regen_dict()
		return "Reset Progress"
	
	if parts[0] == "total":
		history.toggle_total()
		return "Toggled Total"
		
	if parts[0] in ["track", "t"]:
		if len(parts) == 1:
			history.data["Tracking"] = [p for p in history.data.keys() if p not in ["Last_Addition", "bonus", "Tracking", "showtotal", "pct", "pcttotal"]]
			history.save()
			return "Tracking all encountered"
			
		if get_poke(parts[1]) in pokes or parts[1]=="singles":
			if get_poke(parts[1]) in history.data["Tracking"]:
				return "Already tracking "+ get_poke(parts[1])
			else:
				history.data["Tracking"].append(get_poke(parts[1]))
				history.save()
			return f"Tracking {get_poke(parts[1])}"
		else:
			return f"No such pokemon: {parts[1].title()}"
			
	if parts[0] in ["untrack", "u"]:
		if len(parts) == 1:
			history.data["Tracking"] = []
			history.save()
			return "Untracked all"
			
		if parts[1] == "0":
			history.data["Tracking"] = [poke for poke in history.data["Tracking"] if poke in history.data.keys() ]
			history.save()
			return "Untracked all 0s"
			
		if get_poke(parts[1]) in pokes:
			if get_poke(parts[1]) not in history.data["Tracking"]:
				return "Not tracking "+ get_poke(parts[1])
			else:
				history.data["Tracking"].pop(history.data["Tracking"].index(get_poke(parts[1])))
				history.save()
			return f"Untracking {get_poke(parts[1])}"
		else:
			return f"No such pokemon: {parts[1].title()}"
			
	return f"Unknown Command"
