# Author: Jason Giroux
# purpose: Parse through manuals to find types of control registers.
# Example: cr0.pe, cr0.XX

import PyPDF2
from os import walk
import re
import json
import yaml

# Location of manuals
manualsFolder = "../manuals/"

# store types of control registers
crX_types = []

# manuals in the manuals folder
files = []

# get names of files in the manuals folder
for(dirpath, dirnames, filenames) in walk(manualsFolder):
    for i in filenames:
        files.append(manualsFolder + i)
    break

iternations = {}

for i in files:
    pdfFileObj = open(i, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pageNum = 0
    while True:
        try:
            pageObj = pdfReader.getPage(pageNum)
        except:
            break
        page = pageObj.extractText()
        reg = "(CR[0-9][.][A-z]{2})"
        match = re.search(reg, page)
        try:
            foundIteration = match.group(1)
        except:
            foundIteration = None

        pageNum = pageNum + 1

        if not foundIteration:
            continue

        elif len(iternations) == 0:
            print(foundIteration)
            temp = {
                "name": foundIteration,
                "page": pageNum,
                "manual": i
            }
            iternations[temp["name"]] = temp

        else:
            print(foundIteration)
            for a in iternations:
                if foundIteration not in a:
                    temp = {
                        "name": foundIteration,
                        "page": pageNum,
                        "manual": i
                    }
                    iternations[temp["name"]] = temp
                    break

# write to json file
with open("control_reg.json", "w") as output_file:
    json.dump(iternations, output_file, indent=4)

with open("control_reg.yml", "w") as output_file:
    yaml.dump(iternations, output_file, indent=4)

print(json.dumps(iternations, indent = 4))
