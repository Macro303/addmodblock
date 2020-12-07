# AddModBlock for Minecraft 1.16 (with Forge)

This simple python script helps with adding source code and json for minecraft blocks. Note! By default this script should never overwrite a file but if it does, so I'm not responsible (although I will be sorry). Make backups!

This script supports generating Java for:
 - Block
 - Tile Entity
 - Gui
 - Container

This script also supports generating Json for:
 - Blockstate
 - Model
 - Block Item
 - Recipe
 - Loot Table

## Requirements
 - Requires Python 3+ _(Run `python --version` to show your python version)_
 - Edit the `config.ini` to suit your needs.
 - Run this from within your mod root folder

## Usage

| Parameter | Example | Required | Description |
| --------- | ------- | -------- | ----------- |
| `name` | `python -m AddBlock ExampleBlock` | True | |
| `--tile` | `python -m AddBlock ExampleBlock --tile` | False | Generate additional code for a tileentity |
| `--gui` | `python -m AddBlock ExampleBlock --gui` | False | Generate additional code for container and gui (implies tile!) |
| `--nojson` | `python -m AddBlock ExampleBlock --nojson` | False | Prevent generating json |
| `--force` | `python -m AddBlock ExampleBlock --force` | False | Overwrite files even if they exist (be careful!) |

## Notes

The resulting code is by no means finished. It is up to you to make this a nice modded block. Have fun!