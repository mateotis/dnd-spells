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

	levelTable = soup.find_all("table",class_="wiki-content-table")[i]

	for j in range(1, 100):
		try:
			spell = levelTable.find_all("tr")[j]
		except:
			break

		spellName = spell.find_all("td")[0].text
		if("(UA)" in spellName or "(HB)" in spellName): # Filter out Unearthed Arcana and homebrew spells
			continue
		spellSchool = spell.find_all("td")[1].text
		if(" " in spellSchool): # Cut off dunamancy marker from school name
			spaceLoc = spellSchool.find(" ")
			spellSchool = spellSchool[0:spaceLoc]
		spellCastTime = spell.find_all("td")[2].text
		spellRange = spell.find_all("td")[3].text
		spellDuration = spell.find_all("td")[4].text
		spellComponents = spell.find_all("td")[5].text

		print("=====\n" + spellName, spellSchool, spellCastTime, spellRange, spellDuration, spellComponents)

		totalSpellCount += 1

print("Total spell count:", totalSpellCount)