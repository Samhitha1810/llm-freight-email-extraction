import json

def load_ports():
    with open("port_codes_reference.json", encoding="utf-8") as f:
        ports = json.load(f)

    name_to_code = {}
    code_to_name = {}

    for p in ports:
        name = p["name"].lower().strip()
        code = p["code"].strip()

        # Store normal name
        name_to_code[name] = code
        
        # Store no-space variant
        name_to_code[name.replace(" ", "")] = code

        # Store code → canonical name
        code_to_name[code] = p["name"]

    # Common abbreviations
    name_to_code["hk"] = "HKHKG"
    name_to_code["hongkong"] = "HKHKG"

    return name_to_code, code_to_name


def normalize_port(port_text, name_to_code, code_to_name):
    if not port_text:
        return None, None

    text = port_text.lower().strip()

    # Take first if multiple ports listed
    for sep in ["/", ",", " and "]:
        if sep in text:
            text = text.split(sep)[0].strip()
            break

    # Handle common short port codes seen in emails
    shorthand = {
        "maa": "chennai",
        "maa icd": "chennai icd",
        "sha": "shanghai",
        "ham": "hamburg",
        "blr": "bangalore icd",
        "hyd": "hyderabad icd",
        "jed": "jeddah",
        "dam": "dammam",
        "ruh": "riyadh",
        "yok": "yokohama",
        "hou": "houston",
        "lax": "los angeles",
        "lgb": "long beach",
        "kel": "keelung",
        "hcm": "ho chi minh",
        "cpt": "cape town",
        "pus": "busan",
        "sin": "singapore",
        "sub": "surabaya",
        "bkk": "bangkok",
        "sha icd": "shanghai",
    }

    if text in shorthand:
        text = shorthand[text]

    # Direct match
    code = name_to_code.get(text)

    # Try no-space variant
    if not code:
        code = name_to_code.get(text.replace(" ", ""))

    if not code:
        return None, None

    return code, code_to_name[code]

