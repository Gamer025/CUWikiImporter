import json
import pywikibot
from pywikibot import textlib
from enum import Enum
from collections import OrderedDict


# Created with pwb generate_family_file.py
site = pywikibot.Site("en", "testgg")
#site = pywikibot.Site("en", "scavwiki")

data_types = Enum('data_types', [('Item', 0), ('Recipe', 1), ('Liquid', 2), ('Tile', 3)])

infobox_names = ["Scav Item Infobox", "Scav Recipe???", "Scav Liquid Infobox", "Scav Tile Infobox"]
#infobox_names = ["Item Infobox", "Recipe???", "Liquid Infobox", "Tile Infobox"]

namespaces = ["ScavWiki/Items/", "ScavWiki/Recipes/", "ScavWiki/Liquids/", "ScavWiki/Tiles/"]
#namespaces = ["User:Gamer025/sandbox/Items/", "User:Gamer025/sandbox/Recipes/", "User:Gamer025/sandbox/Liquids/", "User:Gamer025/sandbox/Tiles/"]

def main():
    global wiki_json_data
    
    # Login needs to be setup with pwb generate_user_files.py
    site.login()
    with open("data.json", "r", encoding="utf-8") as f:
        wiki_json_data = json.load(f)

    # Create pages if they don't exist otherwise update templates if needed
    for liquids in wiki_json_data["liquids"]:
        page = pywikibot.Page(site, generate_page_path(liquids["localeName"], data_types.Liquid))

        if not page.exists():
            create_page(liquids["localeName"], data_types.Liquid)
        else:
            update_template(liquids["localeName"], data_types.Liquid)

    for item in wiki_json_data["items"]:
        page = pywikibot.Page(site, generate_page_path(item["fullName"], data_types.Item))
        if not page.exists():
            create_page(item["fullName"], data_types.Item)
        else:
            update_template(item["fullName"], data_types.Item)

# https://stackoverflow.com/questions/51359783/how-to-flatten-multilevel-nested-json
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


def merge_params(existing, new):
    merged = existing.copy()
    for key, value in new.items():
        merged[key] = value
    return merged

# Convert the different value types to correct mediawiki strings (e.g. null to empty string)
def convert_value_to_mediawiki_string(value):
    if value is None:
        return ""
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, list):
        # Convert list of dicts to JSON-like representation
        if all(isinstance(x, dict) for x in value):
            return "[" + ", ".join(json.dumps(x) for x in value) + "]"
        # Convert list of primitives
        return "[" + ", ".join(map(str, value)) + "]"
    return str(value)

_lang_cache = {}

# Get display name for an object in main    
def object_name_to_lang(object_name: str, type: data_types, lang: str = "EN"):
    if lang not in _lang_cache:
        try:
            with open(f"{lang}.json", "r", encoding="utf-8") as f:
                _lang_cache[lang] = json.load(f)
        except FileNotFoundError:
            print(f"Couldn't find '{lang}.json', returning raw object name.")
            return object_name

    lang_data = _lang_cache[lang]

    if (type == type.Item):
        json_path = "main"
    else:
        json_path = "other"

    try:
        return lang_data[json_path][object_name]
    except Exception:
        print(f"[ERROR] Could not find key '{object_name}' in '{lang}.json'.")
        return object_name
    
# Get description for an object in main    
def object_name_to_desc(object_name: str, type: data_types, lang: str = "EN"):
    if lang not in _lang_cache:
        try:
            with open(f"{lang}.json", "r", encoding="utf-8") as f:
                _lang_cache[lang] = json.load(f)
        except FileNotFoundError:
            print(f"Couldn't find '{lang}.json', returning raw object name.")
            return object_name

    lang_data = _lang_cache[lang]

    if (type == type.Item):
        json_path = "main"
    else:
        json_path = "other"

    try:
        return lang_data[json_path][f"{object_name}dsc"]
    except Exception:
        print(f"[ERROR] Could not find key '{object_name}dsc' in '{lang}.json'.")
    return lang_data.get()


# Create a new template from scratch or update existing data when existing_data is passed
def create_template(object_name: str, type: data_types, existing_data: OrderedDict = None) -> str:
    
    # Get data from JSON dump depending on what we are dealing with (Item, Fluid, ...)
    if (type is data_types.Item ):
        item_data = next(
            (x for x in wiki_json_data.get("items", []) if x.get("fullName") == object_name),
            None
        )
    # TODO: Figure out on what to match recipes on (probably result -> id ?)
    if (type is data_types.Recipe ):
        item_data = next(
            (x for x in wiki_json_data.get("recipes", []) if x.get("fullName") == object_name),
            None
        )
    if (type is data_types.Liquid ):
        item_data = next(
            (x for x in wiki_json_data.get("liquids", []) if x.get("localeName") == object_name),
            None
        )
        # Convert individual rgba values to single hex string
        item_data["color"] = "#{:02X}{:02X}{:02X}{:02X}".format(*[item_data["color"][k] for k in ("r", "g", "b", "a")]
)
    if (type is data_types.Tile ):
        item_data = next(
            (x for x in wiki_json_data.get("tiles", []) if x.get("name") == object_name),
            None
        )

    # Update existing template
    if (existing_data is not None):
        # Overwrite all params that with data that exists in the JSON dump
        prepared_data = merge_params(existing_data, flatten_json(item_data))
    else :
        prepared_data = flatten_json(item_data)
       

    # Language data
    prepared_data["displayName"] = object_name_to_lang(object_name, type)
    prepared_data["description"] = object_name_to_desc(object_name, type)

    for key in prepared_data:
        prepared_data[key] = convert_value_to_mediawiki_string(prepared_data[key])

    # Sort the dictionary by key names so its easier to find stuff in the generated itemboxes
    sorted_data = dict(sorted(prepared_data.items()))
    return textlib.glue_template_and_params((infobox_names[type.value], sorted_data))


# Generate full path to this object e.g. /Item/Backpack
def generate_page_path(object_name: str, type: data_types) -> str:
    return f"{namespaces[type.value]}{object_name_to_lang(object_name, type)}"

def create_page(object_name: str, type: data_types):
    page = pywikibot.Page(site, generate_page_path(object_name, type))
    if page.exists():
        print(f"Tried creating already existing page {page}, page creation cancelled!")
        return;

    
    page.text = create_template(object_name, type)
    page.save()


def update_template(object_name: str, type: data_types):
    global wiki_json_data

    page = pywikibot.Page(site, generate_page_path(object_name, type))

    if not page.exists():
        print("Tried updating template data on non existing page!")
        return

    text = page.text

   
    # Get all templates on page
    templates = textlib.extract_templates_and_params(text)

    # Check if template already exists, should normally be the case
    infobox_name = infobox_names[type.value]
    found = False

    for template, params in templates:
        if template.strip().lower() == infobox_name.lower():
            found = True
            # Need to remove all the trailing \n in every param value because otherwise glue_template_and_params will double them up ...
            stripped_params = {k: v.rstrip("\n") for k, v in params.items()}
            infobox_template = (template, stripped_params)
            break
        
    # Otherwise put it on the top of the page
    if not found:
        page.text = create_template(object_name, type) + "\n" + text
        print(f"Adding infobox to {page} because its missing")
        page.save(summary="Added Infobox to page because it was missing")
        return
    
    # If we find the existing template replace it with and updated version if needed
    old_template_text = textlib.glue_template_and_params(infobox_template)
    new_template_text = create_template(object_name, type, infobox_template[1])
    if (old_template_text != new_template_text):
        if (old_template_text in page.text):
            page.text = page.text.replace(old_template_text, new_template_text, 1)
            print(f"Updating infobox on {page}")
            page.save(summary="Updated existing infobox because didn't match with computed infobox.")
        else:
            print(f"Error updating infobox on page {page}. Old itembox could not be found with the following string: \n {old_template_text}")
    else:
        print(f"Updating infobox on {page}")

        
if __name__=="__main__":
    main()