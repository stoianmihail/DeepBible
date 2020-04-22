import numpy as np
import json
import util
import sys

order = dict()
mapOrder = dict()
abbvsRegex = util.computeAbbvsRegex()
crossReferencesRegex = util.computeCrossReferencesRegex()
insideRegex = util.computeInsideRegex()
fastSearchAbbvs = set(util.abbvs.values())

def analyzeCrossReferences(row, currentChapterIndex, order, matrix):
  crs = util.parseCrossReferences(row, crossReferencesRegex)
  if len(crs) != len(util.parseAbbvs(row, abbvsRegex)):
    print("Problem: " + row)
    sys.exit(1)
  
  for cr in crs:
    book = cr[0]
    refs = cr[1]
    try:
      parsed = util.parseInsideCrossReferences(refs, insideRegex)
      for elem in parsed:
        chapter = elem[1].strip()
        try:
          # This is the correct way for the hyperlink: [...][currentChapterIndex]
          matrix[order[(book, int(chapter))]][currentChapterIndex] += 1
        except:
          print("Problem: " + row + " chapter: " + chapter)
          sys.exit(1)
    except:
      print(row + " book: " + book)
      sys.exit(1)

def analyzeChapter(book, biblePart, chapterIndex, order, matrix):
  chapterSize = len(biblePart) - 1

  for index in range(1, chapterSize + 1):
    if 'cross-references' in biblePart[str(index)]:
      analyzeCrossReferences(biblePart[str(index)]["cross-references"], chapterIndex, order, matrix)

def analyzeBook(book, biblePart, abbv, matrix):
  bookSize = len(biblePart)
  for chapter in range(1, bookSize + 1):
    analyzeChapter(book, biblePart[str(chapter)], order[(abbv, chapter)], order, matrix)

def analyzeBible(bibleVersion):
  n = 0
  for (testament, book) in bibleVersion["books"].values():
    bookSize = len(bibleVersion["bible"][testament][book])
    for index in range(1, bookSize + 1):
      order[(util.abbvs[book], index)] = n
      mapOrder[n] = (book, index)
      n += 1
  
  matrix = np.empty(shape=(n, n))
  matrix.fill(0)
  
  for (testament, book) in bibleVersion["books"].values():
    print("Analyze book \"" + book + "\"")
    analyzeBook(book, bibleVersion["bible"][testament][book], util.abbvs[book], matrix)
  return matrix
  
def computePowerMatrix(bibleVersion, matrix, rho = 0.85, numIterations = 10000):
  n = len(matrix)
  rev = (1 - rho) * (1.0 / n)
  sums = np.zeros(shape=n)
  
  # TODO: analyze also regex of verses (7-9), add the number of references within it and divide by the length of the chapter
  for rowIndex in range(n):
    for colIndex in range(n):
      sums[colIndex] += matrix[rowIndex][colIndex]
  for rowIndex in range(n):
    for colIndex in range(n):
      elem = 0
      if sums[colIndex]:
        elem = matrix[rowIndex][colIndex] / sums[colIndex]
      matrix[rowIndex][colIndex] = rho * elem + rev
  powerMatrix = np.eye(n)
  while numIterations:
    if numIterations % 2 == 1:
      powerMatrix = powerMatrix.dot(matrix)
    matrix = matrix.dot(matrix)
    numIterations >>= 1
  return powerMatrix
  
def rankChapters(powerMatrix):
  n = len(powerMatrix)
  ranking = np.empty(shape=n)
  ranking.fill(1.0 / n)
  return powerMatrix.dot(ranking)
  
def main(bibleVersionFile):
  # python3 analyzer.py biblia.json
  bibleVersion = json.loads(open(bibleVersionFile, 'r').read())
  matrix = analyzeBible(bibleVersion)
  ranking = rankChapters(computePowerMatrix(bibleVersion, matrix))
  total = np.array(ranking).sum()
  
  perm = np.argsort(-ranking)
  partialSum = 0
  rank = 0
  for index in perm:
    rank += 1
    print(str(rank) + ": \"" + str(mapOrder[index][0]) + "\", Chapter=" + str(mapOrder[index][1]))
    partialSum += ranking[index]
    if partialSum > 0.10 * total:
      break
  
if __name__ == '__main__':
  main(sys.argv[1])
