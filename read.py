import re
import sys
import util
import json
from unidecode import unidecode

def parseTitles(inputFile):
  next(inputFile)
  bible = dict()
  books = dict()
  
  testament = " Testament"
  currTestament = "Vechiul" + testament
  bible[currTestament] = dict()
  
  for row in inputFile:
    row = row.strip()
    if row == "NOUL" + testament.upper():
      break
    bible[currTestament][row] = dict()
    books[unidecode(row.upper())] = (currTestament, row)
  
  currTestament = "Noul" + testament
  bible[currTestament] = dict()
  for row in inputFile:
    row = row.strip()
    if row.find("Apocalipsa") != -1:
      bible[currTestament][row] = dict()
      books[unidecode(row.upper())] = (currTestament, row)
      break
    bible[currTestament][row] = dict()
    books[unidecode(row.upper())] = (currTestament, row)
  return bible, books

def handleError(book, chapter = "", verse = ""):
  if not chapter:
    print("Book \"" + book + "\" might be empty!")
    sys.exit(1)
  else:
    print("Error while parsing book \"" + book + "\", " + str(chapter) + ", " + str(verse))
    sys.exit(1)

def parseBooks(bible, books, inputFile, specialBook = "Estera"):
  testament = ""
  lastBook = ""
  currBook = ""
  chapter = 0
  verse = 0
  
  verseRegex = re.compile(util.computeVerseRegex())
  chapterRegex = re.compile(util.computeChapterRegex())
  crossRefRegex = re.compile(util.computeCrossReferencesRegex())
  
  while True:
    try:
      row = next(inputFile).strip()
    except:
      break
    
    # Does a new book start?
    if unidecode(row.upper()) in books:
      testament = books[unidecode(row.upper())][0]
      currBook = books[unidecode(row.upper())][1]
    
    # If yes, then check if it has any subtitle
    if currBook != lastBook:
      print("Start parsing book \"" + currBook + "\"")
      lastBook = currBook
      try:
        row = next(inputFile).strip()
      except:
        handleError(currBook)
      
      # Is there a subtitle?
      if not re.search(r'\d', row):
        try:
          row = next(inputFile).strip()
        except:
          handleError(currBook)
      chapter = 0

    # Does a new chapter begin?
    if chapterRegex.search(row):
      try:
        row = next(inputFile).strip()
      except:
        handleError(currBook)
      
      bible[testament][currBook][chapter + 1] = dict()
      chapter += 1
      verse = 0
      
      # Check for the special book
      # First skip over the subtitle
      row = next(inputFile).strip()
      collected = ""
      while not verseRegex.search(row):
        collected += " " + row
        try:
          row = next(inputFile).strip()
        except:
          handleError(currBook)
      if currBook == specialBook:
        bible[testament][currBook][chapter]["addendum"] = collected.strip()
        
    # Is this the beginning of a regular verse?
    if verseRegex.search(row):
      row = verseRegex.sub("", row)
      bible[testament][currBook][chapter][verse + 1] = dict()
      bible[testament][currBook][chapter][verse + 1]["text"] = row
      verse += 1
    elif not crossRefRegex.search(row):
      if verse in bible[testament][currBook][chapter]:
        bible[testament][currBook][chapter][verse]["text"] += " " + row
      else:
        handleError(currBook, chapter, verse)
    else:
      bible[testament][currBook][chapter][verse]["cross-references"] = row
  return bible
      
def parseBibleVersion(bibleFile):
  inputFile = open(bibleFile, "r")
  bible, books = parseTitles(inputFile)
  parseBooks(bible, books, inputFile)

  if False:
    print(bible["Noul Testament"]["Sfânta Evanghelie după Matei"][22][17])
    print(bible["Vechiul Testament"]["Psalmii"][135])
    print(bible["Noul Testament"]["Apocalipsa Sfântului Ioan Teologul"][22][21])
    print(bible["Vechiul Testament"]["Estera"][1]["addendum"])
    print(bible["Noul Testament"]["A treia Epistolă Sobornicească a Sfântului Apostol Ioan"][1][7])
  
    for (testament, book) in books.values():
      if not bible[testament][book]:
        print("Book \"" + book + "\" is empty!")
        sys.exit(1)
  version = dict()
  version["books"] = books
  version["bible"] = bible
  return version

def main(bibleFile):
  # python3 read.py biblia.txt
  if True:
    with open('biblia.json', 'w') as output:
      bibleVersion = parseBibleVersion(bibleFile)
      json.dump(bibleVersion, output)
  else:
    crossRefRegex = re.compile(util.computeCrossReferencesRegex())
    bibleVersion = json.loads(open('biblia.json', 'r').read())
    cr1 = bibleVersion["bible"]["Vechiul Testament"]["Ieremia"]["32"]["3"]["cross-references"]
    cr2 = bibleVersion["bible"]["Vechiul Testament"]["Ieremia"]["32"]["5"]["cross-references"]
    cr3 = bibleVersion["bible"]["Noul Testament"]["Sfânta Evanghelie după Matei"]["27"]["49"]["cross-references"]
    cr4 = bibleVersion["bible"]["Noul Testament"]["Sfânta Evanghelie după Luca"]["14"]["27"]["cross-references"]
    
if __name__ == '__main__':
  main(sys.argv[1])
