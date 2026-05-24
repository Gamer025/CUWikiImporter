import json
import pywikibot
from pywikibot import textlib
from enum import Enum


site = pywikibot.Site("en", "scavwiki")
data_types = Enum('data_types', [('Item', 0), ('Recipe', 1), ('Liquid', 2), ('Tile', 3)])
infobox_names = ["Item Infobox", "Recipe???", "Liquid Infobox", "Tile Infobox"]
namespaces = ["User:Gamer025/sandbox/Items/", "User:Gamer025/sandbox/Recipes/", "User:Gamer025/sandbox/Liquids/", "User:Gamer025/sandbox/Tiles/"]

def main():
    global json_data
    
    # Login needs to be setup with pwb generate_user_files.py
    site.login()
    with open("data.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

    create_page("bigpack", data_types.Item)
    update_template("bigpack", data_types.Item)

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


# Convert the different value types to correct mediawiki strings (e.g. null to empty string)
def convert_value(value):
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

# Generate a mediawiki itembox template string
def build_template(data, template_name):
    flat = flatten_json(data)
    # {{Item Infobox
    lines = [f"{{{{{template_name}"]

    # | key = value
    for key, value in flat.items():
        lines.append(f"| {key} = {convert_value(value)}")

    # }}
    lines.append("}}")
    return "\n".join(lines)

def create_template(object_name: str, type: data_types) -> str:
    if (type is data_types.Item ):
        item_data = next(
            (x for x in json_data.get("items", []) if x.get("fullName") == object_name),
            None
        )
        return build_template(item_data, infobox_names[type.value])
    # TODO: Figure out on what to match recipes (probably result -> id ?)
    if (type is data_types.Recipe ):
        item_data = next(
            (x for x in json_data.get("recipes", []) if x.get("fullName") == object_name),
            None
        )
        return build_template(item_data, infobox_names[type.value])
    if (type is data_types.Liquid ):
        item_data = next(
            (x for x in json_data.get("liquids", []) if x.get("localename") == object_name),
            None
        )
        return build_template(item_data, infobox_names[type.value])
    if (type is data_types.Tile ):
        item_data = next(
            (x for x in json_data.get("tiles", []) if x.get("name") == object_name),
            None
        )
        return build_template(item_data, infobox_names[type.value])
         
        

def create_page(item_name: str, type: data_types):
    page = pywikibot.Page(site, f"{namespaces[type.value]}{item_name}")
    if page.exists():
        print(f"Tried creating already existing page {page}, page creation cancelled!")
        return;

    
    page.text = create_template(item_name, type)
    page.save()


def update_template(object_name: str, type: data_types):
    global json_data

    page = pywikibot.Page(site, f"{namespaces[type.value]}{object_name}")

    if not page.exists():
        print("Tried updating template data non existing page!")
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
            infobox_params = params
            break

    # Otherwise put it on the top of the page
    if not found:
        page.text = create_template(object_name, type) + "\n" + text
        page.save(summary="Added Infobox to page because it was missing")
        

    # TODO: Code for updating existing info boxes

if __name__=="__main__":
    main()