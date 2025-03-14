# Polished Crystal Wiki Scripts

## Overview
Parses various data files from [Polished Crystal](https://github.com/Rangi42/polishedcrystal) and generates markdown pages for the [wiki](https://github.com/Rangi42/polishedcrystal/wiki).

## Features
- Parses abilities, evolution data, level-up moves, egg moves, TM/HM learnsets, move tutor moves, unique wild moves, and more.
- Extracts data from Polished Crystal's `.asm` files.
- Generates markdown files for each Pokemon's learnset in Johto Pokedex order.
- Creates markdown pages for held items and Polished changes.

## Dependencies
- This script relies on Python 3 (unsure on minimum version but it definitely works on 3.10.12).
- Ensure that you have the necessary data files from the Polished Crystal repository before running the script.

## Usage
### Running the Script
```sh
python generate_wiki_pages.py
```
This will parse the required `.asm` files and generate the markdown pages in place.

### Input Files
The script reads data from the following directories:
- `../polishedcrystal/data/moves/`
- `../polishedcrystal/data/pokemon/`

Currently, `generate_wiki_pages.py` generates all files in place, so it's best used by copying the script
into the Polished Crystal Wiki git folder. The script also expects the Polished Crystal codebase to be
in the same folder named `polishedcrystal`. These should probably be passed as command line arguments
in the future.

### Output Files
- `Pokemon-Learnsets.md`: A main index of Pokemon learnsets.
- Individual markdown files for each Pokemon's learnset.
- `Wild-Held-Items.md`: Lists Pokemon and their held items.
- `Pokemon-Type,-Evolution,-Ability,-and-Stat-Changes.md`: Summarizes differences in the Faithful vs Polished ROMs.

### Notes
The Polished Crystal Wiki can be updated by anyone via Github on the web, but only Polised Crystal contributors
have permission to push to the wiki git repo. If there are massive changes to the learnsets that change many
files, it's best to zip the wiki repo and send it to a Polished Crystal dev to push to avoid individually
editing many pages.