from root.general_tools.tools import get_google_formatted_address_using_address, get_unique_addresses
import re

to_be_deleted_from_address = ["/"]
number_founder_pattern = "[^\d]?(\d+)[^\d]?"

def find_thai_addresses(text, patterns, is_contact_page=False):
    found_addresses = []
    for pattern in patterns:
        items = re.findall(pattern, text)
        if(items):
            for item in items:
                # cleaning addresses
                add = re.sub("\n", " ", item[0])
                add = add.strip()
                add = re.sub("\s{2,}", " ", add)
                found_addresses.append(add)
    return list(set(found_addresses))

def get_thai_address_parts(address, language="th"):
    return {"address":address, "components":[], "source":"company-website"}

def recheck_thai_addresses(address):
    digits = re.sub("\D", "", address)
    if(len(digits) > len(address)/2):
        return None

    if(not "ที่ตั้ง" in address and not "address" in address and not "Office" in address and not "สำนักงานใหญ่" in address):
        if(":" in address):
            return None

    if(re.search("(\d{1,4}/\d{1,4}/\d{1,4})", address)):
        return None

    address = re.sub('\"|\(|\)', " ", address)
    
    m = re.search("ที่ตั้ง[^\w]+", address, flags=re.IGNORECASE)
    if(m):
        address = address.replace(m.group(0), "")
    
    m = re.search("address[^\w]+", address, flags=re.IGNORECASE)
    if(m):
        address = address.replace(m.group(0), "")
    
    m = re.search("Office[^\w]+", address, flags=re.IGNORECASE)
    if(m):
        address = address.replace(m.group(0), "")

    m = re.search("สำนักงานใหญ่[^\w]+", address, flags=re.IGNORECASE)
    if(m):
        address = address.replace(m.group(0), "")
        
    address = address.replace("\\n", ", ")
    address = re.sub(",\W*,", ", ", address)
    address = re.sub(" ,", ",", address)
    address = re.sub("\s{2,}", " ", address)
    return address

def purify_thai_addresses(address_list):
    '''
    get a list of thai addresses and return a list of unique
    and splitted addresses extracted from input addresses 
    '''
    rechecked_addresses = []
    for add in address_list:
        rechecked_address = recheck_thai_addresses(add)
        if(rechecked_address):
            rechecked_addresses.append(rechecked_address)

    unique_addresses = get_unique_addresses(rechecked_addresses, to_be_deleted_from_address)

    splitted_addresses = []
    for add in unique_addresses:
        splitted_addresses.append(get_thai_address_parts(add))
    return splitted_addresses


def find_thai_phones(text, patterns):
    phones = []
    for pattern in patterns:
        items = re.findall(pattern, text)
        for item in items:
            phones.append(item)
    return list(set(phones))
