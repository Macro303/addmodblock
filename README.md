# AddModBlock for Minecraft 1.16 (with Forge)

This simple python script helps with adding source code and json for minecraft blocks.

This script supports generating Json for:
 - Blockstate
 - Model
 - Block Item
 - Recipe
 - Loot Table

This script also supports generating Java for:
 - Block
 - Tile Entity
 - Gui
 - Container

## Requirements
 - Requires Python 3+

## Steps
 1. Edit the `config.ini` to suit your needs.
 2. Copy the `AddBlock` folder and `config.ini` file to your mod root folder
 3. Run the following *(look at the arguments section for more details)*:
   ```bash
   $ python -m AddBlock {name}
   ```

## Arguments

| Argument | Example | Required | Description |
| --------- | ------- | -------- | ----------- |
| `name` | `python -m AddBlock ExampleBlock` | True | |
| `--tile` | `python -m AddBlock ExampleBlock --tile` | False | Generate additional code for a tileentity |
| `--gui` | `python -m AddBlock ExampleBlock --gui` | False | Generate additional code for container and gui (implies tile!) |
| `--nojson` | `python -m AddBlock ExampleBlock --nojson` | False | Prevent generating json files |
| `--force` | `python -m AddBlock ExampleBlock --force` | False | Overwrite files even if they exist (be careful!) |

## Notes
By default this script should never overwrite a file but if it does, so I'm not responsible (although I will be sorry). Make backups!

The resulting code is by no means finished. It is up to you to make this a nice modded block. Have fun!