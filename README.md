# AddModBlock for Minecraft 1.16 (with Forge)

This simple python script helps with adding source code and json for minecraft blocks. Note! By default this script should never overwrite a file but if it does, so I'm not responsible (although I will be sorry). Make backups!

Before using this script you will have to configure it. Edit the script and modify the first part of the script to suit your needs.

This script supports generating both java and json for: block, tile entity, gui, container, blockstate json, model json, item json, recipe json and loot table json.

To use this run this script from within your mod root folder. If you then want to add a block without tile entity and gui you can do this:

## Usage

| Parameter | Example | Required | Description |
| --------- | ------- | -------- | ----------- |
| `name` | `python AddBlock.py ExampleBlock` | True | |
| `--tile` | `python AddBlock.py ExampleBlock --tile` | False | Generate additional code for a tileentity |
| `--gui` | `python AddBlock.py ExampleBlock --gui` | False | Generate additional code for container and gui (implies tile!) |
| `--nojson` | `python AddBlock.py ExampleBlock --nojson` | False | Prevent generating json |
| `--force` | `python AddBlock.py ExampleBlock --force` | False | Overwrite files even if they exist (be careful!) |

## Notes

The resulting code is by no means finished. It is up to you to make this a nice modded block. Have fun!