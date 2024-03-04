import os
#os.system("sudo -E play-audio /storage/emulated/0/Documents/MATES/src/mates/gg.mp3")
#os.system(f"sudo -E screencap -p /storage/emulated/0/Documents/base3.jpg")


from .pokeutil import *
import cv2

def test():
	expected = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: True, 8: True, 9: True, 10:True}
	expected_mons = {7:["Rapidash" for _ in range(5)], 8:["Rapidash" for _ in range(5)], 9:["Meowth"], 10:["Pidgey"]}
		
	#init_out_of_combat()
	failed = 0
	
	i = 0
	for i in range(1, 11):
		basearray = cv2.imread(f"{PATH}/tests/{i}.png")
		base = Image.fromarray(basearray)
		cropped = np.array(base.crop((0,0,3040,400)))
		
		in_combat = count_mons(cropped) > 0
		if  in_combat != expected[i]:
			print("Case", i, "Failed")
			failed += 1
		
		if i in expected_mons.keys():
			if get_mons(basearray) != expected_mons[i]:
				print("Case", i, "Failed\nExpected: ", expected_mons[i], "\nGot: ", get_mons(basearray))
				failed += 1
				Image.fromarray(basearray).save(f"{PATH}/tests/failed{i}.png")
				
		
		
	
	if failed > 0:
		print("Failed", failed, "cases")
		return False
	else:
		print("Passed all cases")
		return True
import subprocess

def tests():
	print("Running tests")
	if test():
		subprocess.run(["play-audio /storage/emulated/0/Documents/MATES/src/mates/gg.mp3"], shell=True)
		
if __name__ == "__main__":
	tests()