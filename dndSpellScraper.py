# Scrapes spell data from http://dnd5e.wikidot.com/spells

from bs4 import BeautifulSoup as bs
import requests
import urllib
import csv

url = "http://dnd5e.wikidot.com/spells"
response = requests.get(url)

soup = bs(response.text,"html.parser")

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

		spellCastTime = spell.find_all("td")[2].text
		spellRange = spell.find_all("td")[3].text
		spellDuration = spell.find_all("td")[4].text
		spellComponents = spell.find_all("td")[5].text

		# Get the classes that can cast this spell
		spellURL = "http://dnd5e.wikidot.com" + spellLink
		spellResponse = requests.get(spellURL)
		spellSoup = bs(spellResponse.text,"html.parser")

		spellClasses = spellSoup.find_all("p")[-1].text
		spellClasses = spellClasses[len("Spell Lists. "):] # Cut the preceding text

		# Get description of the spell
		totalPCount = len(spellSoup.find_all("p"))
		
		spellAtHigherLevels = ""
		if("At Higher Levels." in spellSoup.find_all("p")[-2].text): # Some spells change depending on user level; record this info
			spellAtHigherLevels = spellSoup.find_all("p")[-2].text
			spellAtHigherLevels = spellAtHigherLevels[len("At Higher Levels. "):]

		spellDescription = ""
		for k in range(3, totalPCount - 1): # The description starts on the third paragraph and goes on for variable length
			spellDescription += ("\n" + spellSoup.find_all("p")[k].text)

		print("=====\n" + spellName, spellSchool, spellCastTime, spellRange, spellDuration, spellComponents)
		print("Classes:", spellClasses)
		print("At Higher Levels:", spellAtHigherLevels)
		print(spellDescription)

		totalSpellCount += 1

print("Total spell count:", totalSpellCount)