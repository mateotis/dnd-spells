# Scrapes spell data from http://dnd5e.wikidot.com/spells

from bs4 import BeautifulSoup as bs
import requests
import urllib
import csv
import time

url = "http://dnd5e.wikidot.com/spells"
response = requests.get(url)

soup = bs(response.text,"html.parser")

spellList = []
missingSpellList = []
totalSpellCount = 0

for i in range(10):

	if i == 0:
		print("\n========\nCANTRIPS\n========\n")
	else:
		print("\n========\nLEVEL", i, "SPELLS\n========\n")

	levelTable = soup.find_all("table",class_="wiki-content-table")[i] # One table per spell level

	for j in range(1, 100):
		try: # Dynamic boundary check
			spell = levelTable.find_all("tr")[j]
		except:
			break

		spellNameRaw = spell.find_all("td")[0]
		spellLink = spell.find("a", href=True)["href"] # Get link for each individual spell

		spellName = spell.find_all("td")[0].text
		if("(UA)" in spellName or "(HB)" in spellName): # Filter out Unearthed Arcana and homebrew spells
			continue
		spellSchool = spell.find_all("td")[1].text
		if(" " in spellSchool): # Cut off dunamancy marker from school name
			spellSchool = spellSchool[0:spellSchool.find(" ")]

		spellLevel = str(i) # Level 0 = cantrip, the rest are normal
		spellCastTime = spell.find_all("td")[2].text
		spellRange = spell.find_all("td")[3].text
		spellDuration = spell.find_all("td")[4].text
		spellComponents = spell.find_all("td")[5].text

		# Open the individual spell page
		spellURL = "http://dnd5e.wikidot.com" + spellLink
		spellResponse = requests.get(spellURL)
		spellSoup = bs(spellResponse.text,"html.parser")

		try: # Failsafe, should not be needed, but never bad to have
			spellClasses = spellSoup.find_all("p")[-1].text
			spellClasses = spellClasses[len("Spell Lists. "):] # Cut the preceding text
		except:
			pass

		# Get description of the spell
		totalPCount = len(spellSoup.find_all("p"))
		if(totalPCount == 0): # Should never be the case, save for requests loading errors
			missingSpellList.append(spellName) # But if it IS the case, then let's record what we're missing
			continue
		
		spellAtHigherLevels = ""
		if("At Higher Levels." in spellSoup.find_all("p")[-2].text): # Some spells change depending on user level; record this info
			spellAtHigherLevels = spellSoup.find_all("p")[-2].text
			spellAtHigherLevels = spellAtHigherLevels[len("At Higher Levels. "):]

		spellDescription = ""
		if(spellAtHigherLevels != ""): # Cut off already-recorded data from the general description
			for k in range(3, totalPCount - 2): # The description starts on the third paragraph and goes on for variable length
				spellDescription += (spellSoup.find_all("p")[k].text + "\n")
		else:
			for k in range(3, totalPCount - 1):
				spellDescription += (spellSoup.find_all("p")[k].text + "\n")

		print("=====\n" + spellName, spellLevel, spellSchool, spellCastTime, spellRange, spellDuration, spellComponents)
		print("Classes:", spellClasses)
		print("At Higher Levels:", spellAtHigherLevels)
		print(spellDescription)

		spellData = [spellName, spellLevel, spellSchool, spellCastTime, spellRange, spellDuration, spellComponents, spellClasses, spellAtHigherLevels, spellDescription]
		spellList.append(spellData)

		totalSpellCount += 1

print("Total spell count:", totalSpellCount)

print("Writing to CSV...")

with open("dnd-spells.csv", mode="w", encoding = "UTF-8") as spellcsv:
	fieldnames = ["Spell Name", "Level", "School", "Casting Time", "Range", "Duration", "Components", "Classes", "At Higher Levels", "Description"]
	writer = csv.DictWriter(spellcsv, fieldnames=fieldnames)
	writer.writeheader()
	for i in spellList:
		writer.writerow({"Spell Name": i[0], "Level": i[1], "School": i[2], "Casting Time": i[3], "Range": i[4], "Duration": i[5], "Components": i[6], "Classes": i[7], "At Higher Levels": i[8], "Description": i[9]})

print("Done!")
if(len(missingSpellList) == 0):
	print("All spells covered!")
else:
	print("Missing spells:")
	for i in missingSpellList:
		print(i)