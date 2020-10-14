import yaml
from os import listdir
from os.path import isfile, join
import re

cpu_id_dir = "../amd/register/cpuid/"
cpu_id_files = [f for f in listdir(cpu_id_dir) if isfile(join(cpu_id_dir, f))]

vmcb_dir = "../amd/register/vmcb/"
vmcb_files = [f for f in listdir(vmcb_dir) if isfile(join(vmcb_dir, f))]

Namereg = "(E[A-D]X)"
purposeReg = "(CPUID_Fn[0-9]*[A-z|0-9]_E[A|B|C|D]X)"
errors = 0

def check_CPUID_access_mech(contents, fileName):
    global errors
    name = contents[0]["name"]
    function = contents[0]["access_mechanisms"][0]["function"]
    output = contents[0]["access_mechanisms"][0]["output"]
    if(function != output):
        print("[ERROR] function is not the same as output", fileName)
        errors = errors + 1
    else:
        match = re.search(Namereg, name)
        group = match.group(0)

        if(group != function.upper()):
            print("[ERROR] Name does not match function", fileName)

def check_CPUID_purpose(contents, fileName):
    global errors
    name = contents[0]["name"]
    purpose = contents[0]["purpose"]

    match = re.search(purposeReg, purpose)
    group = match.group(0)

    nameMatch = re.search(purposeReg, name)
    nameGroup = nameMatch.group(0)

    if(group != nameGroup):
        print("[ERROR] Name does not match Purpose: ", fileName)
        errors = errors + 1

def check_vmcb_purpose(contents, fileName):
    global errors
    name = contents[0]["name"]
    purpose = contents[0]["purpose"]

    if not name in purpose:
        print("[ERROR] Name and purpose does not match: ", fileName)
        errors = errors + 1

def check_vmcb_access_mech(contents, fileName):
    global errors
    name = contents[0]["name"]
    access_read = contents[0]["access_mechanisms"][0]["offset"]
    access_write = contents[0]["access_mechanisms"][1]["offset"]
    if access_write != access_read:
        print("[ERROR] Access Read does not match Access Write: ", fileName)

    name = "0x" + name.replace("h","")
    name = int(name, 16)

    if name != access_read:
        print("[ERROR] Name does not match Access Read: ", fileName)
    if name != access_write:
        print("[ERROR] Name does not match Access Write: ", fileName)

# Check CUPID Validity
for i in cpu_id_files:
    try:
        with open(cpu_id_dir+i) as file:
            contents = yaml.load(file)
            check_CPUID_access_mech(contents, i)
            check_CPUID_purpose(contents, i)
    except Exception as error:
        print("[ERROR] Cannot parse YAML File: ", i, "\nError: ", error)
        errors=errors+1

# CHeck VMCB
for i in vmcb_files:
    try:
        with open(vmcb_dir+i) as file:
            contents = yaml.load(file)
            check_vmcb_purpose(contents, i)
            check_vmcb_access_mech(contents, i)
    except Exception as error:
        print("[ERROR] Cannot parse YAML File: ", i, "\nError: ", error)
        errors = errors+1


print("Total errors: ", errors)