# Gets spell damage types for each spell from two separate sources (spell description and a csv file taken from an external source) and adds them to the database

import csv

damageTypes = ["acid", "bludgeoning", "cold", "fire", "force", "lightning", "necrotic", "piercing", "poison", "psychic", "radiant", "slashing", "thunder"]

dmgTypeDict = {}
spellList = []

with open("dnd-spells-scraped.csv", newline='') as spellcsv: # Read spell csv contents into main memory
	reader = csv.reader(spellcsv, delimiter=",")
	rowCnt = 0
	for row in reader:
		if(rowCnt == 0): # Skip header row
			rowCnt += 1
			continue
		spellList.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])

with open("listfist-damage-types.csv", newline='') as typecsv: # Also read in external damage type specification
	reader = csv.reader(typecsv, delimiter=";") # Special delimiter!
	rowCnt = 0
	for row in reader:
		if(rowCnt == 0): # Skip header row
			rowCnt += 1
			continue
		dmgTypeDict[row[1]] = row[4]

dmgTypeFound = False
dmgTypeFoundCnt = 0
for spell in spellList:
	dmgTypeFound = False

	for dmgType in damageTypes:
		if((dmgType + " damage") in spell[9]): # Search spell description for damage type
			spell.insert(6, dmgType.capitalize()) # Insert damage type between Duration and Components
			dmgTypeFoundCnt += 1
			dmgTypeFound = True
			break # For now, only record one damage type for a spell, if applicable

	for extspell in dmgTypeDict: # Now iterate through the external csv for extra precision
		if(extspell == spell[0]):
			if(dmgTypeFound == True): # If the previous search has already found a damage type, just overwrite it
				spell[6] = dmgTypeDict[extspell]
				break
			else:
				spell.insert(6, dmgTypeDict[extspell]) # If not, newly insert it at the proper place
				dmgTypeFoundCnt += 1
				dmgTypeFound = True
				break
			
	if(dmgTypeFound == False):
		spell.insert(6, "") # Make sure every row has the new column, even if there's nothing in it

print("Found damage type for", dmgTypeFoundCnt, "spells. Writing updated CSV...")

with open("dnd-spells-updated.csv", mode="w", encoding = "UTF-8") as spellcsv:
	fieldnames = ["Spell Name", "Level", "School", "Casting Time", "Range", "Duration", "Damage Type", "Components", "Classes", "At Higher Levels", "Description"]
	writer = csv.DictWriter(spellcsv, fieldnames=fieldnames)
	writer.writeheader()
	for i in spellList:
		writer.writerow({"Spell Name": i[0], "Level": i[1], "School": i[2], "Casting Time": i[3], "Range": i[4], "Duration": i[5], "Damage Type": i[6], "Components": i[7], "Classes": i[8], "At Higher Levels": i[9], "Description": i[10]})
