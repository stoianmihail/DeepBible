import sys
import re

associations = {
  "Facerea" : "Facerea",
  "Ieşirea" : "Ieşirea",
  "Leviticul" : "Leviticul",
  "Numerii" : "Numerii",
  "Deuteronomul" : "Deuteronomul",
  "Cartea lui Iosua Navi" : "Iosua Navi",
  "Cartea Judecătorilor" : "Judecători",
  "Cartea Rut" : "Rut",
  "Cartea întâi a Regilor" : "I Regi",
  "Cartea a doua a Regilor" : "II Regi",
  "Cartea a treia a Regilor" : "III Regi",
  "Cartea a patra a Regilor" : "IV Regi",
  "Cartea întâi Paralipomena" : "I Paralipomena",
  "Cartea a doua Paralipomena" : "II Paralipomena",
  "Cartea întâi a lui Ezdra" : "I Ezdra",
  "Cartea lui Neemia" : "Neemia",
  "Estera" : "Esterei",
  "Cartea lui Iov" : "Iov",
  "Psalmii" : "Psalmi",
  "Pildele lui Solomon" : "Pilde",
  "Ecclesiastul" : "Ecclesiastul",
  "Cântarea cântărilor" : "Cântări",
  "Isaia" : "Isaia",
  "Ieremia" : "Ieremia",
  "Plângerile lui Ieremia" : "Plangeri",
  "Iezechiel" : "Iezechiel",
  "Daniel" : "Daniel",
  "Osea" : "Osea",
  "Amos" : "Amos",
  "Miheia" : "Miheia",
  "Ioil" : "Ioil",
  "Avdie" : "Avdie",
  "Iona" : "Iona",
  "Naum" : "Naum",
  "Avacum" : "Avacum",
  "Sofonie" : "Sofonie",
  "Agheu" : "Agheu",
  "Zaharia" : "Zaharia",
  "Maleahi" : "Maleahi",
  "Cartea lui Tobit" : "Tobit",
  "Cartea Iuditei" : "Iudita",
  "Cartea lui Baruh" : "Baruh",
  "Epistola lui Ieremia" : "Epistola lui Ieremia",
  "Cântarea celor trei tineri" : "3 tineri",
  "Cartea a treia a lui Ezdra" : "III Ezdra",
  "Cartea înţelepciunii lui Solomon" : "Solomon",
  "Cartea înţelepciunii lui Isus, fiul lui Sirah" : "Ecclesiasticul",
  "Istoria Susanei" : "Susanei",
  "Istoria omorârii balaurului şi a sfărâmării lui Bel" : "Istoria Balaurului",
  "Cartea întâi a Macabeilor" : "I Macabei",
  "Cartea a doua a Macabeilor" : "II Macabei",
  "Cartea a treia a Macabeilor" : "III Macabei",
  "Rugăciunea regelui Manase" : "Manase",
  "Sfânta Evanghelie după Matei" : "Matei",
  "Sfânta Evanghelie după Marcu" : "Marcu",
  "Sfânta Evanghelie după Luca" : "Luca",
  "Sfânta Evanghelie după Ioan" : "Ioan",
  "Faptele Sfinţilor Apostoli" : "Faptele Apostolilor",
  "Epistola către Romani a Sfântului Apostol Pavel" : "Romani",
  "Epistola întâia către Corinteni a Sfântului Apostol Pavel" : "I Corinteni",
  "Epistola a doua către Corinteni a Sfântului Apostol Pavel" : "II Corinteni",
  "Epistola către Galateni a Sfântului Apostol Pavel" : "Galateni",
  "Epistola către Efeseni a Sfântului Apostol Pavel" : "Efeseni",
  "Epistola către Filipeni a Sfântului Apostol Pavel" : "Filipeni",
  "Epistola către Coloseni a Sfântului Apostol Pavel" : "Coloseni",
  "Epistola întâia către Tesaloniceni a Sfântului Apostol Pavel" : "I Tesaloniceni",
  "Epistola a doua către Tesaloniceni a Sfântului Apostol Pavel" : "II Tesaloniceni",
  "Epistola întâia către Timotei a Sfântului Apostol Pavel" : "I Timotei",
  "Epistola a doua către Timotei a Sfântului Apostol Pavel" : "II Timotei",
  "Epistola către Tit a Sfântului Apostol Pavel" : "Tit",
  "Epistola către Filimon a Sfântului Apostol Pavel" : "Filimon",
  "Epistola către Evrei a Sfântului Apostol Pavel" : "Evrei",
  "Epistola Sobornicească a Sfântului Apostol Iacov" : "Iacov",
  "Întâia epistolă Sobornicească a Sfântului Apostol Petru" : "I Petru",
  "A doua epistolă Sobornicească a Sfântului Apostol Petru" : "II Petru",
  "Întâia Epistolă Sobornicească a Sfântului Apostol Ioan" : "I Ioan",
  "A doua Epistolă Sobornicească a Sfântului Apostol Ioan" : "II Ioan",
  "A treia Epistolă Sobornicească a Sfântului Apostol Ioan" : "III Ioan",
  "Epistola Sobornicească a Sfântului Apostol Iuda" : "Iuda",
  "Apocalipsa Sfântului Ioan Teologul" : "Apocalipsa",
}

abbvs = {
  "Facerea" : "Fac.",
  "Ieşirea" : "Ieş.",
  "Leviticul" : "Lev.",
  "Numerii" : "Num.",
  "Deuteronomul" : "Deut.",
  "Cartea lui Iosua Navi" : "Iosua",
  "Cartea Judecătorilor" : "Jud.",
  "Cartea Rut" : "Rut",
  "Cartea întâi a Regilor" : "1 Reg.",
  "Cartea a doua a Regilor" : "2 Reg.",
  "Cartea a treia a Regilor" : "3 Reg.",
  "Cartea a patra a Regilor"  : "4 Reg.",
  "Cartea întâi Paralipomena" : "1 Paral.",
  "Cartea a doua Paralipomena" : "2 Paral.",
  "Cartea întâi a lui Ezdra" : "1 Ezd.",
  "Cartea lui Neemia" : "Neem.",
  "Estera" : "Est.",
  "Cartea lui Iov" : "Iov",
  "Psalmii" : "Ps.", 
  "Pildele lui Solomon" : "Pild.",
  "Ecclesiastul" : "Eccl.",
  "Cântarea cântărilor" : "Cânt.",
  "Isaia" : "Is.",
  "Ieremia" : "Ier.",
  "Plângerile lui Ieremia" : "Plâng.",
  "Iezechiel" : "Iez.",
  "Daniel" : "Dan.",
  "Osea" : "Os.",
  "Amos" : "Am.",
  "Miheia" : "Mih.",
  "Ioil" : "Ioil",
  "Avdie" : "Avd.",
  "Iona" : "Iona",
  "Naum" : "Naum",
  "Avacum" : "Avac.",
  "Sofonie" : "Sof.",
  "Agheu" : "Ag.",
  "Zaharia" : "Zah.",
  "Maleahi" : "Mal.",
  "Cartea lui Tobit" : "Tob.",
  "Cartea Iuditei" : "Idt.",
  "Cartea lui Baruh" : "Bar.",
  "Epistola lui Ieremia" : "Ier.",
  "Cântarea celor trei tineri" : "",
  "Cartea a treia a lui Ezdra" : "3 Ezd.",
  "Cartea înţelepciunii lui Solomon" : "Înţel.",
  "Cartea înţelepciunii lui Isus, fiul lui Sirah" : "Sir.",
  "Istoria Susanei" : "Sus.",
  "Istoria omorârii balaurului şi a sfărâmării lui Bel" : "",
  "Cartea întâi a Macabeilor" : "1 Mac.",
  "Cartea a doua a Macabeilor" : "2 Mac.",
  "Cartea a treia a Macabeilor" : "3 Mac.",
  "Rugăciunea regelui Manase" : "",
  "Sfânta Evanghelie după Matei" : "Mat.",
  "Sfânta Evanghelie după Marcu" : "Marc.",
  "Sfânta Evanghelie după Luca" : "Luc.",
  "Sfânta Evanghelie după Ioan" : "Ioan",
  "Faptele Sfinţilor Apostoli" : "Fapt.",
  "Epistola către Romani a Sfântului Apostol Pavel" : "Rom.",
  "Epistola întâia către Corinteni a Sfântului Apostol Pavel" : "1 Cor.",
  "Epistola a doua către Corinteni a Sfântului Apostol Pavel" : "2 Cor.",
  "Epistola către Galateni a Sfântului Apostol Pavel" : "Gal.",
  "Epistola către Efeseni a Sfântului Apostol Pavel" : "Ef.",
  "Epistola către Filipeni a Sfântului Apostol Pavel" : "Filip.",
  "Epistola către Coloseni a Sfântului Apostol Pavel" : "Col.",
  "Epistola întâia către Tesaloniceni a Sfântului Apostol Pavel" : "1 Tes.",
  "Epistola a doua către Tesaloniceni a Sfântului Apostol Pavel" : "2 Tes.",
  "Epistola întâia către Timotei a Sfântului Apostol Pavel" : "1 Tim.",
  "Epistola a doua către Timotei a Sfântului Apostol Pavel" : "2 Tim.",
  "Epistola către Tit a Sfântului Apostol Pavel" : "Tit",
  "Epistola către Filimon a Sfântului Apostol Pavel" : "Filim.",
  "Epistola către Evrei a Sfântului Apostol Pavel" : "Evr.",
  "Epistola Sobornicească a Sfântului Apostol Iacov" : "Iac.",
  "Întâia epistolă Sobornicească a Sfântului Apostol Petru" : "1 Petr.",
  "A doua epistolă Sobornicească a Sfântului Apostol Petru" : "2 Petr.",
  "Întâia Epistolă Sobornicească a Sfântului Apostol Ioan" : "1 Ioan",
  "A doua Epistolă Sobornicească a Sfântului Apostol Ioan" : "2 Ioan",
  "A treia Epistolă Sobornicească a Sfântului Apostol Ioan" : "3 Ioan",
  "Epistola Sobornicească a Sfântului Apostol Iuda" : "Iuda",
  "Apocalipsa Sfântului Ioan Teologul" : "Apoc."
}

def prepareAbbvs():
  values = filter(lambda x: x, abbvs.values())
  final = []
  for val in values:
    if val[len(val) - 1] == '.':
      length = len(val)
      val = val[:length - 1] + '\\.'
    final.append(val)
  return final

def computeAbbvsRegex():
  return r'(' + '|'.join(prepareAbbvs()) + ')'

def computeCrossReferencesRegex():
  possibilites = r'(' + '|'.join(prepareAbbvs()) + ')'
  return possibilites + '((?:([:;])?\s[1-9]\d*((?:\,\s[1-9]\d*(-[1-9]\d*)?))+)+)(\.)?'

def computeInsideRegex():
  return r'([:;])?(\s[1-9]\d*)(\,\s[1-9]\d*(-[1-9]\d*)?)+'

def computeVerseRegex():
  return r'^[0-9]+\.'

def computeChapterRegex():
  return r'^CAP\.\s[0-9]+|^PSALMUL\s[0-9]+'

def parseAbbvs(row, regex):
  return re.findall(regex, row)
  
def parseCrossReferences(row, regex):
  return re.findall(regex, row)

def parseInsideCrossReferences(refs, regex):
  return re.findall(regex, refs)
