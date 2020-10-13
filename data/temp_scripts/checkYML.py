import yaml
from os import listdir
from os.path import isfile, join
import re

cpu_id_dir = "../amd/register/cpuid/"
cpu_id_files = [f for f in listdir(cpu_id_dir) if isfile(join(cpu_id_dir, f))]
Namereg = "(E[A-D]X)"
purposeReg = "(CPUID_Fn[0-9]*[A-z|0-9]_E[A|B|C|D]X)"

def check_access_mech(contents, fileName):
    name = contents[0]["name"]
    function = contents[0]["access_mechanisms"][0]["function"]
    output = contents[0]["access_mechanisms"][0]["output"]
    if(function != output):
        print("[ERROR] function is not the same as output", fileName)
    else:
        match = re.search(Namereg, name)
        group = match.group(0)

        if(group != function.upper()):
            print("[ERROR] Name does not match function", fileName)
        if(group != output.upper()):
            print("[ERROR] Name does not match output: ", fileName)

def check_purpose(contents, fileName):
    name = contents[0]["name"]
    purpose = contents[0]["purpose"]

    match = re.search(purposeReg, purpose)
    group = match.group(0)

    nameMatch = re.search(purposeReg, name)
    nameGroup = nameMatch.group(0)

    if(group != nameGroup):
        print("[ERROR] Name does not match Purpose: ", fileName)


for i in cpu_id_files:
    try:
        with open(cpu_id_dir+i) as file:
            contents = yaml.load(file, Loader=yaml.FullLoader)
            check_access_mech(contents, i)
            check_purpose(contents, i)
    except:
        print("[ERROR] Cannot parse YAML File: ", i)
