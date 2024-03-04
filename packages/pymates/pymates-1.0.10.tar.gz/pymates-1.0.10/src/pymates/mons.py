
import cv2
import numpy as np
import pytesseract
from PIL import Image
from .pokeutil import PATH, log





def get_grayscale(image):
	#converts image to black and white
	return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)


def thresholding(image):
	#applies thresholding to the image
	return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
	
def get_text(image):
	#post process the image for OCR
	gray = get_grayscale(image)
	thresh = thresholding(gray)
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
	opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations = 1)
	
	#if pytesseract installed extract text from image
	return pytesseract.image_to_string(opening, lang = 'eng', config = '--psm 6')
	
pokes = {'Bulbasaur', 'Caterpie', 'Voltorb', 'Electrode', 'Exeggcute', 'Exeggutor', 'Cubone', 'Marowak', 'Hitmonlee', 'Hitmonchan', 'Lickitung', 'Koffing', 'Metapod', 'Weezing', 'Rhyhorn', 'Rhydon', 'Chansey', 'Tangela', 'Kangaskhan', 'Horsea', 'Seadra', 'Goldeen', 'Seaking', 'Butterfree', 'Staryu', 'Starmie', 'Mr. Mime', 'Scyther', 'Jynx', 'Electabuzz', 'Magmar', 'Pinsir', 'Tauros', 'Magikarp', 'Weedle', 'Gyarados', 'Lapras', 'Ditto', 'Eevee', 'Vaporeon', 'Jolteon', 'Flareon', 'Porygon', 'Omanyte', 'Omastar', 'Kakuna', 'Kabuto', 'Kabutops', 'Aerodactyl', 'Snorlax', 'Dratini', 'Dragonair', 'Dragonite', 'Beedrill', 'Chikorita', 'Bayleef', 'Meganium', 'Cyndaquil', 'Quilava', 'Typhlosion', 'Totodile', 'Croconaw', 'Pidgey', 'Feraligatr', 'Sentret', 'Furret', 'Hoothoot', 'Noctowl', 'Ledyba', 'Ledian', 'Spinarak', 'Ariados', 'Crobat', 'Pidgeotto', 'Chinchou', 'Lanturn', 'Pichu', 'Cleffa', 'Igglybuff', 'Togepi', 'Togetic', 'Natu', 'Xatu', 'Mareep', 'Flaaffy', 'Ampharos', 'Bellossom', 'Marill', 'Azumarill', 'Sudowoodo', 'Politoed', 'Hoppip', 'Skiploom', 'Jumpluff', 'Rattata', 'Aipom', 'Sunkern', 'Sunflora', 'Yanma', 'Wooper', 'Quagsire', 'Espeon', 'Umbreon', 'Murkrow', 'Slowking', 'Ivysaur', 'Raticate', 'Misdreavus', 'Unown', 'Wobbuffet', 'Girafarig', 'Pineco', 'Forretress', 'Dunsparce', 'Gligar', 'Steelix', 'Snubbull', 'Spearow', 'Granbull', 'Qwilfish', 'Scizor', 'Shuckle', 'Heracross', 'Sneasel', 'Teddiursa', 'Ursaring', 'Slugma', 'Magcargo', 'Fearow', 'Swinub', 'Piloswine', 'Corsola', 'Remoraid', 'Octillery', 'Delibird', 'Mantine', 'Skarmory', 'Houndour', 'Houndoom', 'Ekans', 'Kingdra', 'Phanpy', 'Donphan', 'Porygon2', 'Stantler', 'Smeargle', 'Tyrogue', 'Hitmontop', 'Smoochum', 'Elekid', 'Arbok', 'Magby', 'Miltank', 'Blissey', 'Raikou', 'Entei', 'Suicune', 'Larvitar', 'Pupitar', 'Tyranitar', 'Lugia', 'Pikachu', 'Treecko', 'Grovyle', 'Sceptile', 'Torchic', 'Combusken', 'Blaziken', 'Mudkip', 'Marshtomp', 'Raichu', 'Swampert', 'Poochyena', 'Mightyena', 'Zigzagoon', 'Linoone', 'Wurmple', 'Silcoon', 'Beautifly', 'Cascoon', 'Dustox', 'Sandshrew', 'Lotad', 'Lombre', 'Ludicolo', 'Seedot', 'Nuzleaf', 'Shiftry', 'Taillow', 'Swellow', 'Wingull', 'Pelipper', 'Sandslash', 'Ralts', 'Kirlia', 'Gardevoir', 'Surskit', 'Masquerain', 'Shroomish', 'Breloom', 'Slakoth', 'Vigoroth', 'Slaking', 'Nidoran♀', 'Nincada', 'Ninjask', 'Shedinja', 'Whismur', 'Loudred', 'Exploud', 'Makuhita', 'Hariyama', 'Azurill', 'Nosepass', 'Venusaur', 'Nidorina', 'Skitty', 'Delcatty', 'Sableye', 'Mawile', 'Aron', 'Lairon', 'Aggron', 'Meditite', 'Medicham', 'Electrike', 'Nidoqueen', 'Manectric', 'Plusle', 'Minun', 'Volbeat', 'Illumise', 'Roselia', 'Gulpin', 'Swalot', 'Carvanha', 'Sharpedo', 'Nidoran♂', 'Wailmer', 'Wailord', 'Numel', 'Camerupt', 'Torkoal', 'Spoink', 'Grumpig', 'Spinda', 'Trapinch', 'Vibrava', 'Nidorino', 'Flygon', 'Cacnea', 'Cacturne', 'Swablu', 'Altaria', 'Zangoose', 'Seviper', 'Lunatone', 'Solrock', 'Barboach', 'Nidoking', 'Whiscash', 'Corphish', 'Crawdaunt', 'Baltoy', 'Claydol', 'Lileep', 'Cradily', 'Anorith', 'Armaldo', 'Feebas', 'Clefairy', 'Milotic', 'Castform', 'Kecleon', 'Shuppet', 'Banette', 'Duskull', 'Dusclops', 'Tropius', 'Chimecho', 'Absol', 'Clefable', 'Wynaut', 'Snorunt', 'Glalie', 'Spheal', 'Sealeo', 'Walrein', 'Clamperl', 'Huntail', 'Gorebyss', 'Relicanth', 'Vulpix', 'Luvdisc', 'Bagon', 'Shelgon', 'Salamence', 'Beldum', 'Metang', 'Metagross',  'Ninetales',  'Turtwig', 'Grotle', 'Torterra', 'Jigglypuff', 'Chimchar', 'Monferno', 'Infernape', 'Piplup', 'Prinplup', 'Empoleon', 'Starly', 'Staravia', 'Staraptor', 'Bidoof', 'Charmander', 'Wigglytuff', 'Bibarel', 'Kricketot', 'Kricketune', 'Shinx', 'Luxio', 'Luxray', 'Budew', 'Roserade', 'Cranidos', 'Rampardos', 'Zubat', 'Shieldon', 'Bastiodon', 'Burmy', 'Wormadam', 'Mothim', 'Combee', 'Vespiquen', 'Pachirisu', 'Buizel', 'Floatzel', 'Golbat', 'Cherubi', 'Cherrim', 'Shellos', 'Gastrodon', 'Ambipom', 'Drifloon', 'Drifblim', 'Buneary', 'Lopunny', 'Mismagius', 'Oddish', 'Honchkrow', 'Glameow', 'Purugly', 'Chingling', 'Stunky', 'Skuntank', 'Bronzor', 'Bronzong', 'Bonsly', 'Mime Jr.', 'Gloom', 'Happiny', 'Chatot', 'Spiritomb', 'Gible', 'Gabite', 'Garchomp', 'Munchlax', 'Riolu', 'Lucario', 'Hippopotas', 'Vileplume', 'Hippowdon', 'Skorupi', 'Drapion', 'Croagunk', 'Toxicroak', 'Carnivine', 'Finneon', 'Lumineon', 'Mantyke', 'Snover', 'Paras', 'Abomasnow', 'Weavile', 'Magnezone', 'Lickilicky', 'Rhyperior', 'Tangrowth', 'Electivire', 'Magmortar', 'Togekiss', 'Yanmega', 'Parasect', 'Leafeon', 'Glaceon', 'Gliscor', 'Mamoswine', 'Porygon-Z', 'Gallade', 'Probopass', 'Dusknoir', 'Froslass', 'Rotom', 'Venonat','Venomoth', 'Snivy', 'Servine', 'Serperior', 'Tepig', 'Pignite', 'Charmeleon', 'Diglett', 'Emboar', 'Oshawott', 'Dewott', 'Samurott', 'Patrat', 'Watchog', 'Lillipup', 'Herdier', 'Stoutland', 'Purrloin', 'Dugtrio', 'Liepard', 'Pansage', 'Simisage', 'Pansear', 'Simisear', 'Panpour', 'Simipour', 'Munna', 'Musharna', 'Pidove', 'Meowth', 'Tranquill', 'Unfezant', 'Blitzle', 'Zebstrika', 'Roggenrola', 'Boldore', 'Gigalith', 'Woobat', 'Swoobat', 'Drilbur', 'Persian', 'Excadrill', 'Audino', 'Timburr', 'Gurdurr', 'Conkeldurr', 'Tympole', 'Palpitoad', 'Seismitoad', 'Throh', 'Sawk', 'Psyduck', 'Sewaddle', 'Swadloon', 'Leavanny', 'Venipede', 'Whirlipede', 'Scolipede', 'Cottonee', 'Whimsicott', 'Petilil', 'Lilligant', 'Golduck', 'Basculin', 'Sandile', 'Krokorok', 'Krookodile', 'Darumaka', 'Darmanitan', 'Maractus', 'Dwebble', 'Crustle', 'Scraggy', 'Mankey', 'Scrafty', 'Sigilyph', 'Yamask', 'Cofagrigus', 'Tirtouga', 'Carracosta', 'Archen', 'Archeops', 'Trubbish', 'Garbodor', 'Primeape', 'Zorua', 'Zoroark', 'Minccino', 'Cinccino', 'Gothita', 'Gothorita', 'Gothitelle', 'Solosis', 'Duosion', 'Reuniclus', 'Growlithe', 'Ducklett', 'Swanna', 'Vanillite', 'Vanillish', 'Vanilluxe', 'Deerling', 'Sawsbuck', 'Emolga', 'Karrablast', 'Escavalier', 'Arcanine', 'Foongus', 'Amoonguss', 'Frillish', 'Jellicent', 'Alomomola', 'Joltik', 'Galvantula', 'Ferroseed', 'Ferrothorn', 'Klink', 'Charizard', 'Poliwag', 'Klang', 'Klinklang', 'Tynamo', 'Eelektrik', 'Eelektross', 'Elgyem', 'Beheeyem', 'Litwick', 'Lampent', 'Chandelure', 'Poliwhirl', 'Axew', 'Fraxure', 'Haxorus', 'Cubchoo', 'Beartic', 'Cryogonal', 'Shelmet', 'Accelgor', 'Stunfisk', 'Mienfoo', 'Poliwrath', 'Mienshao', 'Druddigon', 'Golett', 'Golurk', 'Pawniard', 'Bisharp', 'Bouffalant', 'Rufflet', 'Braviary', 'Vullaby', 'Abra', 'Mandibuzz', 'Heatmor', 'Durant', 'Deino', 'Zweilous', 'Hydreigon', 'Larvesta', 'Volcarona',  'Kadabra',  'Meloetta', 'Genesect', 'Alakazam', 'Deoxys', 'Wormadam', 'Wormadam', 'Shaymin', 'Rotom', 'Rotom', 'Rotom', 'Machop', 'Rotom', 'Rotom', 'Castform', 'Basculin', 'Machoke', 'Machamp', 'Bellsprout', 'Squirtle', 'Weepinbell', 'Victreebel', 'Tentacool', 'Tentacruel', 'Geodude', 'Graveler', 'Golem', 'Ponyta', 'Rapidash', 'Slowpoke', 'Wartortle', 'Slowbro', 'Magnemite', 'Magneton', "Farfetch'd", 'Doduo', 'Dodrio', 'Seel', 'Dewgong', 'Grimer', 'Muk', 'Blastoise', 'Shellder', 'Cloyster', 'Gastly', 'Haunter', 'Gengar', 'Onix', 'Drowzee', 'Hypno', 'Krabby', 'Kingler', "Singles", "Zapdos", "Moltres", "Articuno", "Entei", "Raiku", "Suicune"}
legends = ["Zapdos", "Moltres", "Articuno", "Entei", "Raiku", "Suicune"]
try:
	from nltk import edit_distance as distance
	NLTK = False
except:
	NLTK = False
	
	
from difflib import get_close_matches

def get_closest(s, poss, nltk=False):
	if not NLTK:
		out = get_close_matches(s, poss)
		if len(out) > 0:
			return out[0]
		return ""
		
	out = {}
	low = 999
	best = ""
	for p in poss:
		out[p] = distance(s, p, True)
		if out[p] < low:
			low = out[p]
			best = p
	return best
	
female_template = cv2.imread(f"{PATH}/fem.png", 0)

def fem(image, template):
	image = Image.fromarray(image)
	left, top, right, bottom = 0, 0, image.width, image.height//3.3
	
	h, w = image.size
		
	gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
	
	matches = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
	threshold = 0.5
	loc = np.where(matches >= threshold)
		
	i = 0
	for pt in zip(*loc[::-1]):
		i += 1
	
	return "Female" if i > 0 else "Male"

def name_mons(image, template):
	mons, shiny, legend = [], False, False
	image = Image.fromarray(image)
	left, top, right, bottom = 0, 0, image.width, image.height//3.3
	image = image.crop((left, top, right, bottom))
	
	h, w = image.size
		
	gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
	abc = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ \n"
		
		#counts the number of hp icons in the upper half of the screen
	matches = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
	threshold = 0.9
	loc = np.where(matches >= threshold)
		
	i = 0
	for pt in zip(*loc[::-1]):
		i += 1
		#cv2.rectangle(np.array(image), pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
	#image.save("Output.png")
	
	
	
	if i == 5:
		shinycount = 0
		text = "".join([t for t in get_text(image) if t in abc]).replace("\n", " L").replace("Shiny ", "Shiny-").replace("Shimy ", "Shiny-")
		if "Shiny-" in text:
			shiny = True
			shinycount = text.count("Shiny")
		
		text = text.split(" L")
		success = False
		for t in text:
			t = "".join([bit for bit in t.split(" ") if len(bit) > 3])
			if t.title() in pokes:
				mon = t.title().replace("Shiny-", "Shiny ")
				success = True
				break
		
		for t in text:
			if success:
				break
			t = "".join([bit for bit in t.split(" ") if len(bit) > 3])
			if len(get_closest(t.title(), pokes)) > 0:
				mon = get_closest(t.title().replace("Shiny-", ""), pokes)
				success = True
				break
		
		mons = [mon for _ in range(5)]
		for i, mon in enumerate(text):
			if "Nidoran" in mon:
				if fem(np.array(image), female_template) == "Female":
					text[i] = text[i].replace("♂", "♀")
				else:
					text[i] = text[i].replace("♀", "♂")
					
		if shiny:
			for i in range(0, shinycount):
				text[i] = "Shiny "+text[0]
			
	else:
		if i < 3:
			left, top, right, bottom = 0, 0, image.width//3, image.height
			image = image.crop((left, top, right, bottom))
		text = "".join([t for t in get_text(image) if t in abc]).replace("Shiny ", "Shiny-").replace("Shimy ", "Shiny-")
		if "Shiny-" in text:
			shiny = True
			
		text=text.split("\n")
		#print(text)
		#
		
		for t in text:
			if " L" in t:
				t = t.replace("Shiny-", "").split(" L")
				if len(t)>0:
					match = get_closest(t[0], pokes)
					if len(matches) > 0:
						mons.append(match)
		
		
		for i, mon in enumerate(mons):
			if "Nidoran" in mon:
				if fem(np.array(image), female_template) == "Female":
					mons[i] = mon.replace("♂", "♀")
				else:
					mons[i] = mon.replace("♀", "♂")
	
	if shiny and len(mons) == 1:
		mons[0] = "Shiny "+mons[0] 
		

	for mon in mons:
		log(mon, error=True)
		if str(mon).replace("Shiny ", "") in legends:
			legend = True
	return mons, shiny, legend




def find_names(image, threshold=0.9, already_tried=False):
	
	hp = cv2.imread(f"{PATH}/hp.png", 0)
	
	if type(image) == np.array:
		image = Image.fromarray(image)
	left, top, right, bottom = 0, 0, image.width, image.height//3.3
	
	h, w = image.size
		
	gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
	
	matches = cv2.matchTemplate(gray, hp, cv2.TM_CCOEFF_NORMED)
	loc = np.where(matches >= threshold)
		
	
	out = []
	for pt in zip(*loc[::-1]):
		x, y = pt
		out.append((x, y))
		
		continue
		
		if len(out) == 0:
			out.append((x, y))
		for z in out:
			d = (x - z[0]) + (y - z[1])
			#print(d)
			if abs(d) > 100:
				out.append((x, y))
				
	
	return out

class Nameplate():
	def __init__(self, image):
		self.image = image
		self.text = self.get_text()
		self.pokemon = self.get_pokemon()
	
	
	def get_text(self):
		gray = get_grayscale(self.image)
		thresh = thresholding(gray)
		kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
		opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations = 1)
		
		return pytesseract.image_to_string(opening, lang = 'eng', config = '--psm 6')
		
	
	def get_pokemon(self):
		out = self.text.split(" ")[0]
		if out == "Shiny":
			out = "Shiny " + get_close_matches(self.text.split(" ")[1], mons)[0]
		else:
			if "Nidoran"in self.text or "♂" in out or True in ["Nidoran" in m for m in get_close_matches(out, pokes)]:
				out = self.nidoran()
			else:
				out = get_close_matches(out, pokes)
				if len(out) > 0:
					out = out[0]
		
		return out
		
	def __str__(self):
		return str(self.pokemon)
		
	def __repr__(self):
		return str(self)
	
	def save(self, fn):
		self.image.save(fn)
		

	def nidoran(self):
		female_template = cv2.imread(f"{PATH}/fem.png", 0)
		gray = cv2.cvtColor(np.array(self.image), cv2.COLOR_BGR2GRAY)
		
		matches = cv2.matchTemplate(gray, female_template, cv2.TM_CCOEFF_NORMED)
		threshold = 0.5
		loc = np.where(matches >= threshold)
			
		i = 0
		for pt in zip(*loc[::-1]):
			i += 1
		
		#print("Female", i)
		
		return "Nidoran♀" if i > 0 else "Nidoran♂"

def extract_nameplates(img, plates):
	if len(plates) == 0:
		return []
	
	out = []
	if type(img) == np.array:
		im = Image.fromarray(img)
	else:
		im = img
		
	w, h = im.size
	for x, y in plates:
		
		left = x - (w//150)
		top = y - (h//24)
		right = left + (w//8)
		bottom = top + (h//24)
		
		dimensions = (left, top, right, bottom)
		out.append(Nameplate(im.crop(dimensions)))
		
		
	return out

def get_names(cap, as_str=True):
	names = find_names(cap)
	nameplates = extract_nameplates(cap, names)
	return [str(n) for n in nameplates] if as_str else nameplates
	


if __name__ == "__main__":
	template = cv2.imread(f"/storage/emulated/0/Documents/yo/hp.png", 0)
	
	for j in range(1,6):
		image = cv2.imread(f"/storage/emulated/0/Documents/yo/wtf{j}.png")
		mons, shiny, legend = name_mons(image, template)
		if legend:
			print("Legendary")
		if shiny:
			print("Shiny")
		print(mons)
		