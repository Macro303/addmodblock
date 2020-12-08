import json
from argparse import ArgumentParser
from configparser import ConfigParser
from pathlib import Path
from typing import Dict, Any, Optional

from AddBlock.templates import *

#################################################################################
# Config
#################################################################################
config = ConfigParser()
config.read('config.ini')

MODID_REF = config['ModID']['ModID Ref']
MODID = config['ModID']['ModID']

ROOT_PACKAGE = config['Packages']['Root Package']
SOURCE_ROOT = Path('src/main/java')
for folder in ROOT_PACKAGE.split('.'):
    SOURCE_ROOT = SOURCE_ROOT.joinpath(folder)
ASSET_RESOURCE_ROOT = Path('src/main/resources/assets').joinpath(MODID)
DATA_RESOURCE_ROOT = Path('src/main/resources/data').joinpath(MODID)

PACKAGE_BLOCKS = config['Packages']['Blocks']
PACKAGE_TILES = config['Packages']['Tiles']
PACKAGE_CONTAINERS = config['Packages']['Containers']
PACKAGE_SCREENS = config['Packages']['Screens']
#################################################################################


def generate(template: str, inputs: Dict[str, str], conditionals: Optional[Dict[str, Any]] = None) -> str:
    for cond_name, conditional in (conditionals or {}).items():
        lines = template.splitlines()
        gen = True
        newlines = []
        for line in lines:
            if line.strip() == '?{' + cond_name:
                gen = conditional
            elif line.strip() == '?}' + cond_name:
                gen = True
            elif gen:
                newlines.append(line)

        template = '\n'.join(newlines)

    for inp, val in inputs.items():
        template = template.replace(f"$[{inp}]", val)
        template = template.replace(f"$U[{inp}]", val.upper())
        template = template.replace(f"$L[{inp}]", val.lower())
    return template.strip()


def add_templated_java(package: str, name: str, suffix: str, force: bool, template: str, conditionals: Optional[Dict[str, Any]] = None):
    path = SOURCE_ROOT
    for folder in package.split('.'):
        path = path.joinpath(folder)
    path.mkdir(parents=True, exist_ok=True)
    java_path = path.joinpath(f"{name}{suffix}.java")

    if (not force) and java_path.exists():
        print(f"File `{java_path}` already exists. Not generated")
    else:
        print(f"Generated `{java_path}`")
        with open(java_path, 'w') as outfile:
            outfile.write(generate(template=template, inputs={
                'package': f"{ROOT_PACKAGE}.{package}",
                'modid_ref': MODID_REF,
                'modid': MODID,
                'name': name
            }, conditionals=conditionals))


def add_templated_json(path: Path, package: str, name: str, force: bool, template: str):
    for folder in package.split('.'):
        path = path.joinpath(folder)
    path.mkdir(parents=True, exist_ok=True)
    json_path = path.joinpath(f"{name.lower()}.json")

    if (not force) and json_path.exists():
        print(f"File `{json_path}` already exists. Not generated")
    else:
        print(f"Generated `{json_path}`")
        with open(json_path, 'w') as outfile:
            json.dump(json.loads(generate(template=template, inputs={
                "modid": MODID,
                "name": name
            })), outfile, indent=2, sort_keys=True)


def add_block(name: str, force: bool, gui: bool, tile: bool, no_json: bool, no_java: bool):
    if not no_java:
        conditionals = {
            'gui': gui,
            'tile': tile
        }
        add_templated_java(package=PACKAGE_BLOCKS, name=name, suffix='Block', force=force, template=TEMPLATE_BLOCK, conditionals=conditionals)
        if gui:
            add_templated_java(package=PACKAGE_CONTAINERS, name=name, suffix='Container', force=force, template=TEMPLATE_CONTAINER, conditionals=conditionals)
            add_templated_java(package=PACKAGE_SCREENS, name=name, suffix='Screen', force=force, template=TEMPLATE_SCREEN, conditionals=conditionals)
        if tile:
            add_templated_java(package=PACKAGE_TILES, name=name, suffix='Tile', force=force, template=TEMPLATE_TILE, conditionals=conditionals)
    if not no_json:
        add_templated_json(path=ASSET_RESOURCE_ROOT, package='blockstates', name=name, force=force, template=TEMPLATE_BLOCKSTATE)
        add_templated_json(path=ASSET_RESOURCE_ROOT, package='models.block', name=name, force=force, template=TEMPLATE_BLOCK_MODEL)
        add_templated_json(path=ASSET_RESOURCE_ROOT, package='models.item', name=name, force=force, template=TEMPLATE_ITEM_MODEL)
        add_templated_json(path=DATA_RESOURCE_ROOT, package='loot_tables.blocks', name=name, force=force, template=TEMPLATE_LOOTTABLE)
        add_templated_json(path=DATA_RESOURCE_ROOT, package='recipes', name=name, force=force, template=TEMPLATE_RECIPE)


if __name__ == '__main__':
    parser = ArgumentParser(description='Make a Block')
    parser.add_argument('name', help='CamelCase name of the block to add')
    parser.add_argument('--force', help='Overwrite files even if they exist (be careful!)', action='store_true')
    parser.add_argument('--tile', help='Generate additional code for a tileentity', action='store_true')
    parser.add_argument('--gui', help='Generate additional code for container and gui (implies tile!)', action='store_true')
    parser.add_argument('--nojson', help='Prevent generating Json files', action='store_true')
    parser.add_argument('--nojava', help='Prevent generating Java files', action='store_true')
    args = parser.parse_args()

    print(f'Adding block {args.name}')
    add_block(name=args.name, force=args.force, gui=args.gui, tile=args.gui or args.tile, no_json=args.nojson, no_java=args.nojava)
