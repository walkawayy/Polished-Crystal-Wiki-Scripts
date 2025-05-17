import re
import os
import sys

from enum import Enum

class Mode(Enum):
    POLISHED = "Polished"
    FAITHFUL = "Faithful"
    NONE = "None"


def parse_teachable_moves_by_category(filename):
    """Parses TMs, HMs, and move tutor moves with their move category."""
    # TODO If a TM or HM move doubles as a move tutor move, this would need changed.
    try:
        teachable_moves = {}
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                # Stop at end of file.
                if line.startswith("db 0 ; end"):
                    break
                # Check for TM.
                elif line.startswith("db"):
                    # db DYNAMICPUNCH ; TM01 (Chuck)
                    pattern = re.compile(r"db\s+([A-Z_]+)\s*;\s*(TM\d+|HM\d+|MT\d+)", re.IGNORECASE)
                    match = pattern.search(line)

                    move_name = format_move_name(match.group(1))
                    move_category = format_move_category(match.group(2))
                    teachable_moves[move_name] =  move_category

        return teachable_moves
    except FileNotFoundError:
        print(f"""{filename} not found! Quitting.""")
        sys.exit(1)

def ordered_set(sequence):
    """Preserved order set."""
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]

def convert_time_of_day(evolve_happiness_const):
    """Converts the time of day information to more human readable form."""
    mapping = {
        "TR_ANYTIME": "Anytime",
        "TR_MORNDAY": "Morning/Day",
        "TR_EVENITE": "Evening/Night"
    }
    return mapping.get(evolve_happiness_const, "Unknown")

def convert_stat_evolve(evolve_stat_const):
    """Converts the Tyrogue evolution methods to more human readable form."""
    mapping = {
        "ATK_GT_DEF": "Atk greater than Def",
        "ATK_LT_DEF": "Atk less than Def",
        "ATK_EQ_DEF": "Atk equals Def"
    }
    return mapping.get(evolve_stat_const, "Unknown")

def find_asm_file(directory: str, desired_file: str):
    """Recursively traverse polishedcrystal repo folder and find the desired .asm file."""
    for dirpath, _, files in os.walk(directory):
        for file in files:
            if desired_file.lower() in file.lower():
                return os.path.join(dirpath, file)

    print(f"""find_asm_file couldn't find: {desired_file}! Quitting.""")
    sys.exit(1)

def format_move_category(move_category: str):
    """Special name cleanup for Pokemon moves with special characters or names."""
    if "TM" in move_category or "HM" in move_category:
        move_category = move_category[:2] + " " + move_category[2:]
    elif "MT" in move_category:
        move_category = "Move Tutor" # + " " + move_category[2:]
    else:
        move_category = move_category.strip()
    return move_category

def format_move_name(move_name: str):
    """Special name cleanup for Pokemon moves with special characters or names."""
    if "PSYCHIC_M" in move_name:
        move_name = "Psychic"
    elif "X_SCISSOR" in move_name:
        move_name = "X-Scissor"
    elif "DOUBLE_EDGE" in move_name:
        move_name = "Double-Edge"
    elif "U_TURN" in move_name:
        move_name = "U-turn"
    elif "WILL_O_WISP" in move_name:
        move_name = "Will-O-Wisp"
    elif "MUD_SLAP" in move_name:
        move_name = "Mud-Slap"
    else:
        move_name = move_name.strip().replace("_", " ").title()
    return move_name

def get_pokemon_names_for_files(pokemon_name: str):
    """Name cleanup for Pokemon with special characters or forms. Also associates shared evos attacks and egg moves."""
    egg_moves_name = ""
    evo_attacks_name = ""

    if "mime_jr_" in pokemon_name:
        pokemon_name = "Mime Jr."
        egg_moves_name = "MimeJr"
        evo_attacks_name = "MimeJr"
    elif "mr__mime_plain" in pokemon_name:
        pokemon_name = "Mr. Mime"
        egg_moves_name = "MimeJr"
        evo_attacks_name = "MrMimePlain"
    elif "mr__mime_galarian" in pokemon_name:
        pokemon_name = "Mr. Mime Galarian"
        egg_moves_name = "MimeJr"
        # TODO Requires changes in Polished code because uses Rime level up moves.
        evo_attacks_name = "MrMimeGalarian"
    elif "mr__rime" in pokemon_name:
        pokemon_name = "Mr. Rime"
        egg_moves_name = "MimeJr"
        evo_attacks_name = "MrRime"
    elif "diglett_plain" in pokemon_name:
        pokemon_name = "Diglett"
        egg_moves_name = "DiglettAlolan"
        evo_attacks_name = "DiglettPlain"
    elif "rattata_plain" in pokemon_name:
        pokemon_name = "Rattata"
        egg_moves_name = "RattataAlolan"
        evo_attacks_name = "RattataPlain"
    elif "raticate_plain" in pokemon_name:
        pokemon_name = "Raticate"
        egg_moves_name = "RaticatePlain"
        evo_attacks_name = "RaticateAlolan"
    elif "meowth_plain" in pokemon_name:
        pokemon_name = "Meowth"
        egg_moves_name = "MeowthGalarian"
        evo_attacks_name = "MeowthPlain"
    elif "meowth_alolan" in pokemon_name:
        pokemon_name = "Meowth (Alolan)"
        egg_moves_name = "MeowthGalarian"
        evo_attacks_name = "MeowthAlolan"
    elif "growlithe_plain" == pokemon_name:
        pokemon_name = "Growlithe"
        egg_moves_name = "GrowlitheHisuian"
        evo_attacks_name = "GrowlithePlain"
    elif "geodude_plain" in pokemon_name:
        pokemon_name = "Geodude"
        egg_moves_name = "GeodudeAlolan"
        evo_attacks_name = "GeodudePlain"
    elif "slowpoke_plain" in pokemon_name:
        pokemon_name = "Slowpoke"
        egg_moves_name = "SlowpokeGalarian"
        evo_attacks_name = "SlowpokePlain"
    elif "wooper_plain" in pokemon_name:
        pokemon_name = "Wooper"
        egg_moves_name = "WooperPaldean"
        evo_attacks_name = "WooperPlain"
    elif "corsola_plain" in pokemon_name:
        pokemon_name = "Corsola"
        egg_moves_name = "CorsolaGalarian"
        evo_attacks_name = "CorsolaPlain"
    elif "girafarig" == pokemon_name:
        pokemon_name = "Girafarig"
        egg_moves_name = "Girafarig"
        evo_attacks_name = "Farigiraf"
    elif "qwilfish_plain" == pokemon_name:
        pokemon_name = "Qwilfish"
        egg_moves_name = "Qwilfish"
        evo_attacks_name = "QwilfishPlain"
    elif "sneasel_plain" == pokemon_name:
        pokemon_name = "Sneasel"
        egg_moves_name = "Sneasel"
        evo_attacks_name = "SneaselPlain"
    # TODO For FarfetchDGalarianEggMoves to work, requires FarfetchDPlainEggMoves
    #      to be duplicated under its unique egg move db COUNTER.
    elif "farfetch_d_plain" == pokemon_name:
        pokemon_name = "Farfetch'd"
        egg_moves_name = "FarfetchDPlain"
        evo_attacks_name = "FarfetchDPlain"
    elif "farfetch_d_galarian" == pokemon_name:
        pokemon_name = "Farfetch'd (Galarian)"
        egg_moves_name = "FarfetchDGalarian"
        evo_attacks_name = "FarfetchDGalarian"
    elif "sirfetch_d" == pokemon_name:
        pokemon_name = "Sirfetch'd"
        egg_moves_name = "FarfetchDGalarian"
        evo_attacks_name = "SirfetchD"
    elif "mewtwo_plain" == pokemon_name:
        pokemon_name = "Mewtwo"
        egg_moves_name = pokemon_name
        evo_attacks_name = pokemon_name
    elif "mewtwo_armored" == pokemon_name:
        pokemon_name = "Mewtwo (Armored)"
        egg_moves_name = "Mewtwo"
        evo_attacks_name = "Mewtwo"
    elif "ho_oh" == pokemon_name:
        pokemon_name = "Ho-Oh"
        egg_moves_name = "HoOh"
        evo_attacks_name = "HoOh"
    elif "tauros_paldean" == pokemon_name:
        pokemon_name = "Tauros (Combat Breed) (Paldean)"
        egg_moves_name = ""
        evo_attacks_name = "TaurosPaldean"
    elif "tauros_paldean_fire" == pokemon_name:
        pokemon_name = "Tauros (Blaze Breed) (Paldean)"
        egg_moves_name = ""
        evo_attacks_name = "TaurosPaldeanFire"
    elif "tauros_paldean_water" == pokemon_name:
        pokemon_name = "Tauros (Aqua Breed) (Paldean)"
        egg_moves_name = ""
        evo_attacks_name = "TaurosPaldeanWater"
    # More general form fixes.
    elif "plain" in pokemon_name.lower():
        egg_moves_name = pokemon_name.title().replace("_", "")
        evo_attacks_name = egg_moves_name
        pokemon_name = pokemon_name.removesuffix("_plain").title()
    else:
        egg_moves_name = pokemon_name.title().replace("_", "")
        evo_attacks_name = pokemon_name.title().replace("_", "")
        # Format name if has a form.
        parts = pokemon_name.split("_")  # Split at underscore
        if len(parts) > 1:
            pokemon_name = f"{parts[0].title()} ({parts[1].title()})"  # Format form in parentheses
        else:
            pokemon_name = pokemon_name.title()  # If no underscore, just capitalize

    return pokemon_name, egg_moves_name, evo_attacks_name

def extract_base_stat_asm_filenames(filename: str) -> list:
    """Extracts base stat .asm filenames from "base_stats.asm"."""
    asm_files = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            # Skip Red Gyarados and three segment Dudunsparce which are cosmetic forms.
            if "; three segment" in line or "; red" in line:
                continue
            match = re.search(r'([a-zA-Z0-9_]+\.asm)', line)
            if match:
                # Ignore egg dummy base stat data.
                if "egg.asm" not in match.group(1):
                    asm_files.append(match.group(1))
    return asm_files

def parse_johto_dex(filename: str):
    """Parses Pokémon names in Johto dex order."""
    pokemon_names = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            # Extract Pokémon names only if preceded by 'dp'
            match = re.match(r'dp\s+([A-Z][A-Z0-9_]*)', line)
            if match:
                pokemon_names.append(match.group(1))
    return pokemon_names

def order_base_stat_files_by_dex(dex_names: list, asm_files: list):
    """Reorders the Pokemon base stat files by Pokedex order."""
    reordered_base_stat_files = []

    for name in dex_names:
        # Normalize the name for matching.
        normalized_name = name.lower()

        # Find matching .asm files, including alternate forms.
        matches = [file for file in asm_files if file.lower().startswith(normalized_name)]

        if matches:
            reordered_base_stat_files.extend(matches)

        # TODO Remove asm file from list so it's not duplicated.
        for match in matches:
            asm_files.remove(match)

    return reordered_base_stat_files

def parse_egg_moves(filename):
    """Parses egg moves."""
    try:
        egg_moves = {}
        with open(filename, 'r') as file:
            current_pokemon = None
            for line in file:
                line = line.strip()
                # Stop at end of file.
                if line.startswith("NoEggMoves:"):
                    break
                # Get name of the Pokemon.
                elif line.endswith("EggMoves:"):
                    current_pokemon = line.replace("EggMoves:", "").strip()
                    egg_moves[current_pokemon] = []
                # Get the egg moves for the current Pokemon.
                elif line.startswith("db") and current_pokemon:
                    if "$ff" in line:
                        current_pokemon = None
                        continue

                    # Remove anything after a semicolon.
                    line = re.sub(r";.*", "", line).strip()
                     # Get the move and format the name.
                    move = line.split(" ")[1]
                    move = format_move_name(move)
                    egg_moves[current_pokemon].append(move)
        return egg_moves
    except FileNotFoundError:
        print(f"""{filename} not found! Quitting.""")
        sys.exit(1)

def parse_evos_attacks(filename):
    """Parses level up moves and evolution data."""
    try:
        evos_attacks = {}
        with open(filename, 'r') as file:
            mode = Mode.NONE
            current_pokemon = None
            for line in file:
                line = line.strip()
                if line.startswith("if !DEF(FAITHFUL)"):
                    mode = Mode.POLISHED
                elif line.startswith("if DEF(FAITHFUL)"):
                    mode = Mode.FAITHFUL
                elif line.startswith("else"):
                    mode = Mode.POLISHED
                elif line.startswith("endc"):
                    mode = Mode.NONE
                # Stop at end of file.
                if line.startswith("EggEvosAttacks:"):
                    break
                # Get current Pokemon.
                elif line.endswith("EvosAttacks:"):
                    current_pokemon = line.replace("EvosAttacks:", "").strip()
                    evos_attacks[current_pokemon] = {"evo_data_faithful": [], "evo_data_polished": [], "moves": []}
                # Get evolution information.
                elif line.startswith("evo_data") and current_pokemon:
                    # Check if faithful or polished evolution.
                    evo_mode = Mode.FAITHFUL.value.lower()
                    # Tag Faithful only or Polished only move.
                    if mode is not Mode.NONE:
                        evo_mode = mode.value.lower()

                    # Find the evolution data which is up to 5 fields.
                    match = re.match(r"evo_data (\w+), (\w+)(?:, (\w+))?(?:, (\w+))?(?:, (\w+))?", line)
                    evo_info = {}

                    first_field = match.group(1) # Evolution type
                    second_field =  match.group(2) # Method or time of day
                    third_field = match.group(3) # Evolution or time of day or stat spread
                    fourth_field = match.group(4) if match.group(4) else None # Form or evolution
                    fifth_field = match.group(5) if match.group(5) else None # Form

                    if first_field == "EVOLVE_ITEM":
                        evo_info["type"] = first_field.strip().replace("_", " ").title()
                        evo_info["method"] = second_field.strip().replace("_", " ").title()
                        evo_info["evolution"] = third_field.strip().replace("_", " ").title()
                        if fourth_field:
                            evo_info["form"] = fourth_field.strip().replace("_", " ").title()
                    elif first_field == "EVOLVE_HOLDING":
                        evo_info["type"] = first_field.strip().replace("_", " ").title()
                        evo_info["method"] = second_field.strip().replace("_", " ").title()
                        evo_info["evolution"] = fourth_field.strip().replace("_", " ").title()
                        if fifth_field:
                            evo_info["form"] = fifth_field.strip().replace("_", " ").title()
                        evo_info["time_of_day"] = convert_time_of_day(third_field)
                    elif first_field == "EVOLVE_HAPPINESS":
                        evo_info["type"] = first_field.strip().replace("_", " ").title()
                        evo_info["method"] = convert_time_of_day(second_field)
                        evo_info["evolution"] = third_field.strip().replace("_", " ").title()
                        if fourth_field:
                            evo_info["form"] = fourth_field.strip().replace("_", " ").title()
                    elif first_field == "EVOLVE_STAT": # only for Tyrogue (no need for "EVOLVE_TYROGUE")
                        evo_info["type"] = first_field.strip().replace("_", " ").title()
                        evo_info["method"] = second_field.strip().replace("_", " ").title()
                        evo_info["evolution"] = fourth_field.strip().replace("_", " ").title()
                        evo_info["evolve_stat"] = convert_stat_evolve(third_field)
                    elif first_field == "EVOLVE_LOCATION":
                        evo_info["type"] = first_field.strip().replace("_", " ").title()
                        evo_info["method"] = second_field.strip().replace("_", " ").title()
                        evo_info["evolution"] = third_field.strip().replace("_", " ").title()
                        if fourth_field:
                            evo_info["form"] = fourth_field.strip().replace("_", " ").title()
                    elif first_field == "EVOLVE_MOVE":
                        evo_info["type"] = first_field.strip().replace("_", " ").title()
                        evo_info["method"] = second_field.strip().replace("_", " ").title()
                        evo_info["evolution"] = third_field.strip().replace("_", " ").title()
                        if fourth_field:
                            evo_info["form"] = fourth_field.strip().replace("_", " ").title()
                    elif first_field == "EVOLVE_CRIT": # only for Galarian Farfetch'd
                        evo_info["type"] = first_field.strip().replace("_", " ").title()
                        evo_info["method"] = convert_time_of_day(second_field)
                        evo_info["evolution"] = third_field.strip().replace("_", " ").title()
                        # Ignore PLAIN_FORM fourth_field.
                    elif first_field == "EVOLVE_PARTY": # only for Mantyke
                        evo_info["type"] = first_field.strip().replace("_", " ").title()
                        evo_info["method"] = second_field.strip().replace("_", " ").title()
                        evo_info["evolution"] = third_field.strip().replace("_", " ").title()
                    else:
                        # Try to assume "EVOLVE_LEVEL" for everything else.
                        evo_info["type"] = first_field.strip().replace("_", " ").title()
                        evo_info["method"] = second_field.strip().replace("_", " ").title()
                        evo_info["evolution"] = third_field.strip().replace("_", " ").title()
                        if fourth_field and not "NO_FORM" in fourth_field and not "PLAIN_FORM" in fourth_field:
                            evo_info["form"] = fourth_field.strip().replace("_", " ").title()

                    evos_attacks[current_pokemon][f"evo_data_{evo_mode}"].append(evo_info)

                # Get level up move information.
                elif re.match(r"db \d+, [A-Z_]+", line):
                    # Remove anything after a semicolon.
                    line = re.sub(r";.*", "", line).strip()
                    parts = line.split(", ")
                    level = parts[0].split(" ")[1]
                    # Get the move and format the name.
                    move = parts[1]
                    move = format_move_name(move)
                    # Tag Faithful only or Polished only move.
                    if mode is not Mode.NONE:
                        move = f"{move} ({mode.value})"
                    evos_attacks[current_pokemon]["moves"].append((level, move))
        return evos_attacks
    except FileNotFoundError:
        print(f"""{filename} not found! Quitting.""")
        sys.exit(1)

def parse_evolution_moves(filename):
    """Parses evolution moves from the file and formats the Pokemon name and form."""
    evolution_moves = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            
            # Ignore lines that do not start with 'db' or contain 'NO_MOVE'
            if not line.startswith("db") or "NO_MOVE" in line:
                continue
            
            # Extract move name and Pokémon name from the comment
            match = re.match(r'db\s+(\w+).*;\s*(.+)', line)
            if match:
                # Get the move and format the name.
                move = match.group(1)
                move = format_move_name(move)

                # Get Pokémon name and format it contains '_FORM'.
                pokemon_name = match.group(2).strip()
                parts = pokemon_name.split(", ")  # Split at comma and space
                if len(parts) == 2 and "_FORM" in parts[1]:
                    pokemon_name = parts[0].title() + parts[1].title().replace("_Form", "")
                else:
                    pokemon_name = pokemon_name.title()

                evolution_moves[pokemon_name] = move

    return evolution_moves

def parse_unique_wild_moves(filename):
    """Parses unique wild moves from the file and formats the Pokemon name and form."""
    unique_wild_moves = {}

    # Read the file
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Loop through each line
    for line in lines:
        # Check if the line starts with 'unique_moves'.
        if line.strip().startswith('unique_moves'):
            # Remove inline comments for consistent parsing.
            line = line.split(';')[0]

            # Clean up line and split by commas.
            parts = [part.strip() for part in line.split(',')]

            # Check the number of parts to determine the structure.
            if len(parts) == 3:
                # Format: unique_moves LOCATION, POKEMON, MOVE
                location = parts[0].split()[1]
                pokemon_name = parts[1]
                move = parts[2]
                form = None
            elif len(parts) == 4:
                # Format: unique_moves LOCATION, POKEMON, FORM, MOVE
                location = parts[0].split()[1]
                pokemon_name = parts[1]
                form = parts[2]
                move = parts[3]
            else:
                # Skip malformed lines
                continue

            # Format Pokemon name and account if it contains FORM.
            pokemon_name, _, _ = get_pokemon_names_for_files(pokemon_name)

            # TODO Fragile. Deleted Pikachu form info in "unique_wild_moves.asm" since it's the only form. Replaced with:
            #	   unique_moves YELLOW_FOREST,    PIKACHU,    FLY  ; Yellow special move, assumed only Pikachu can learn Fly
	        #      unique_moves YELLOW_FOREST,    PIKACHU,    SURF ; Yellow special move, assumed only Pikachu can learn Surf
            #      so the moves show up as unique wild moves on normal Pikachu's learnset since the rest of the learnset
            #      for the forms are the same.
            if form:
                pokemon_name = pokemon_name.title() + form.title().replace("_Form", "")
            else:
                pokemon_name = pokemon_name.title()

            # Add to dictionary.
            if pokemon_name not in unique_wild_moves:
                unique_wild_moves[pokemon_name] = []

            unique_wild_moves[pokemon_name].append({
                "move": format_move_name(move),
                "location": location.strip().replace("_", " ").title()
            })

    return unique_wild_moves

def parse_pokemon_data(filename: str, pokemon_data: dict):
    """Parses each pokemon's base stat asm file."""
    try:
        with open(filename, 'r') as file:
            mode = Mode.NONE
            for line in file:
                line = line.strip()
                if line.startswith("if DEF(FAITHFUL)"):
                    mode = Mode.FAITHFUL
                elif line.startswith("else"):
                    mode = Mode.POLISHED
                elif line.startswith("endc"):
                    mode = Mode.NONE
                # Parse base stats.
                elif re.search(r"; \d{1,3} BST", line):
                    # Remove leading "db".
                    line = re.sub(r"^db\s+", "", line)

                    # Remove anything after a semicolon.
                    line = re.sub(r";.*", "", line).strip()

                    # Split into list based on comma and remove blank spaces.
                    stats = [item.strip() for item in line.split(",")]

                    # Fill in stats.
                    stats_keys = ["HP", "Atk", "Def", "Speed", "SAt", "SDf"]
                    if mode is Mode.NONE:
                        pokemon_data[f"stats_{Mode.FAITHFUL.value.lower()}"] = dict(zip(stats_keys, map(int, stats)))
                    else:
                        pokemon_data[f"stats_{mode.value.lower()}"] = dict(zip(stats_keys, map(int, stats)))
                # Parse types.
                elif "; type" in line:
                    # Remove leading "db".
                    line = re.sub(r"^db\s+", "", line)

                    # Remove anything after a semicolon.
                    line = re.sub(r";.*", "", line).strip()

                    # Split into list based on comma, remove blank spaces, capitalize first letter, and remove duplicate types.
                    types = ordered_set([item.strip().title() for item in line.split(",")])

                    # Fill in type.
                    if mode is Mode.NONE:
                        pokemon_data[f"type_{Mode.FAITHFUL.value.lower()}"] = types
                    else:
                        pokemon_data[f"type_{mode.value.lower()}"] = types
                # Parse held items.
                elif "; held items" in line:
                    # Remove leading "db".
                    line = re.sub(r"^db\s+", "", line)

                    # Remove anything after a semicolon.
                    line = re.sub(r";.*", "", line).strip()

                    # Split into list based on comma, remove blank spaces, capitalize first letter, and remove duplicate types.
                    held_items = [item.strip().replace("_", " ").title() for item in line.split(",")]

                    # Fill in held items.
                    pokemon_data["held_items"] = held_items
                # Parse abilities.
                elif "abilities_for" in line:
                    # Split into list based on comma, remove blank spaces, and capitalize first letter.
                    line = [item.strip().title() for item in line.split(",")]

                    # Remove leading "abilities_for POKEMON" and remove duplicate types.
                    abilities = line[1:]

                    # Fill in abilities.
                    if mode is Mode.NONE:
                        pokemon_data[f"abilities_{Mode.FAITHFUL.value.lower()}"] = abilities
                    else:
                        pokemon_data[f"abilities_{mode.value.lower()}"] = abilities
                # Parse egg groups.
                elif "; egg groups" in line:
                    # Remove leading "dn".
                    line = re.sub(r"^dn\s+", "", line)

                    # Remove anything after a semicolon.
                    line = re.sub(r";.*", "", line).strip()

                    # Split into list based on comma, remove blank spaces, capitalize first letter, remove leading "EGG_", and remove duplicate groups.
                    egg_groups = ordered_set([item.strip().title()[4:] for item in line.split(",")])

                     # Fill in egg group.
                    pokemon_data[f"egg_groups"] = egg_groups
                # Parse TM and HM learnsets.
                elif "tmhm" in line:
                    # Remove leading "tmhm".
                    # line = re.sub(r"^tmhm\s+", "", line)
                    line = re.sub(r"^tmhm\s*", "", line)

                    # Split into list based on comma, remove blank spaces, replace "_", and capitalize first letter.
                    # TODO X-Scissor, Double-Edge, U-turn, Will-O-Wisp, and Mud-Slap have "-". Check names.asm.
                    tm_hm_moves = [format_move_name(item) for item in line.split(",") if line]

                     # Fill in TM and HM learnsets.
                    pokemon_data[f"tm_hm_moves"] = tm_hm_moves

            return pokemon_data

    except FileNotFoundError:
        print(f"""{filename} not found! Quitting.""")
        sys.exit(1)

def generate_pokemon_learnset_page(pokemon_data: dict, pokemon_file, learnset_file: str, prev_pokemon_data: dict, next_pokemon_data: dict, teachable_moves_category: dict):
    """Generates a Pokemon's learnset page with base stats, abilities, evolution data, egg groups, and learnset."""
    with open(pokemon_file, 'w') as md_file:
        md_file.write(f"""&#8593;&nbsp;[Back to Pokemon Learnsets](Pokemon-Learnsets)\n\n""")

        if prev_pokemon_data:
            prev_link = f"""[{prev_pokemon_data["name"]}]({prev_pokemon_data["name"].replace("(", "").replace(')', '').replace("'", "").replace(" ", "")})"""
            md_file.write(f"""&#8592;&nbsp;{prev_link}&nbsp;&nbsp;""")
        if next_pokemon_data: 
            next_link = f"""[{next_pokemon_data["name"]}]({next_pokemon_data["name"].replace("(", "").replace(')', '').replace("'", "").replace(" ", "")})"""
            md_file.write(f"""{next_link}&nbsp;&#8594;""")
        
        md_file.write("\n")

        md_file.write(f"""## {pokemon_data.get("name")}\n\n""")

        # Type and stats info.
        md_file.write(f"### Base Stats\n\n")
        type_f = ", ".join(pokemon_data["type_faithful"])
        type_p = "-"
        stats_version_f = "-"
        stats_version_p = "-"
        bsts_f = pokemon_data["stats_faithful"]
        bsts_p = {}
        # Check if Pokemon has a different Polished type.
        if pokemon_data["type_polished"]:
            stats_version_f = Mode.FAITHFUL.value
            stats_version_p = Mode.POLISHED.value
            type_p = ", ".join(pokemon_data["type_polished"])
        # Check if Pokemon has different Polished stats.
        if pokemon_data["stats_polished"]:
            stats_version_f = Mode.FAITHFUL.value
            stats_version_p = Mode.POLISHED.value
            bsts_p = pokemon_data["stats_polished"]

        md_file.write(f"| Version           | Type     | HP                    | Atk                    | Def                    | SAt                    | SDf                    | Speed                    |\n")
        md_file.write(f"|:------------------|:---------|:----------------------|:-----------------------|:-----------------------|:-----------------------|:-----------------------|:-------------------------|\n")
        md_file.write(f"| {stats_version_f} | {type_f} | {bsts_f.get('HP', 0)} | {bsts_f.get('Atk', 0)} | {bsts_f.get('Def', 0)} | {bsts_f.get('SAt', 0)} | {bsts_f.get('SDf', 0)} | {bsts_f.get('Speed', 0)} |\n")
        if pokemon_data["type_polished"] or pokemon_data["stats_polished"]:
            md_file.write(f"| {stats_version_p} | {type_p} | {bsts_p.get('HP', '-')} | {bsts_p.get('Atk', '-')} | {bsts_p.get('Def', '-')} | {bsts_p.get('SAt', '-')} | {bsts_p.get('SDf', '-')} | {bsts_p.get('Speed', '-')} |\n")
        md_file.write("\n")

        # Ability info.
        md_file.write(f"### Abilities\n\n")
        ability_version_f = "-"
        ability_version_p = "-"
        abilities_f = ", ".join(pokemon_data["abilities_faithful"]).replace("_", " ").title()
        abilities_p = []
        # Check if Pokemon has different Polished abilities.
        if pokemon_data["abilities_polished"]:
            ability_version_f = Mode.FAITHFUL.value
            ability_version_p = Mode.POLISHED.value
            abilities_p = ", ".join(pokemon_data["abilities_polished"]).replace("_", " ").title()

        md_file.write(f"| Version             | Abilities                  |\n")
        md_file.write(f"|:--------------------|:---------------------------|\n")
        md_file.write(f"| {ability_version_f} | {abilities_f} |\n")
        if pokemon_data["abilities_polished"] != []:
            md_file.write(f"| {ability_version_p} | {abilities_p} |\n")
        md_file.write("\n")

        # Evolution info.
        evo_version_f = "-"
        evo_version_p = "-"
        # Check if Pokemon has different Polished evolution info.
        if pokemon_data["evo_data_polished"]:
            evo_version_f = Mode.FAITHFUL.value
            evo_version_p = Mode.POLISHED.value

        if pokemon_data["evo_data_faithful"]:
            md_file.write(f"### Evolution Data\n\n")
            column_titles = []
            for evolution_method in pokemon_data["evo_data_faithful"]:
                check_column_titles = [title.replace("_", " ").title() for title in evolution_method.keys()]
                # Account for varying number of columns for different evolution methods.
                if len(check_column_titles) > len(column_titles):
                    column_titles = check_column_titles
            md_file.write(f"| Version | {' | '.join(key for key in column_titles)} |\n")
            md_file.write(f"|:--------|:- {' |:- '.join('' for key in column_titles)} |\n")

        for evo in pokemon_data["evo_data_faithful"]:
            column_values = [value for value in evo.values()]
            # Account for varying number of columns for different evolution methods.
            while len(column_values) < len(column_titles):
                column_values.append("-")
            md_file.write(f"| {evo_version_f} | {' | '.join(value for value in column_values)} |\n")

        for evo in pokemon_data["evo_data_polished"]:
            column_values = [value for value in evo.values()]
            # Account for varying number of columns for different evolution methods.
            while len(column_values) < len(column_titles):
                column_values.append("-")
            md_file.write(f"| {evo_version_p} | {' | '.join(value for value in column_values)} |\n")

        md_file.write("\n")

        # Egg groups.
        if pokemon_data["egg_groups"] != []:
            egg_groups = ", ".join(pokemon_data["egg_groups"])
            md_file.write(f"### Egg Groups\n\n")
            md_file.write(f"""{egg_groups}\n""")
            md_file.write("\n")

        # Learnset.
        md_file.write("### Learnset\n\n")
        md_file.write("| Level | Move |\n")
        md_file.write("|--------|-------|\n")

        if pokemon_data["unique_wild_moves"]:
            for unique_wild_move in pokemon_data["unique_wild_moves"]:
                md_file.write(f"""| {unique_wild_move["location"]} | {unique_wild_move["move"]} |\n""")
            md_file.write(f"""| - | - |\n""")

        if pokemon_data["evolution_move"]:
            md_file.write(f"""| Evolve | {pokemon_data["evolution_move"]} |\n""")
            pokemon_data["evolution_move"]
            md_file.write(f"""| - | - |\n""")

        if pokemon_data["level_up_moves"]:
            for level, move in pokemon_data["level_up_moves"]:
                md_file.write(f"""| {level} | {move} |\n""")

        if pokemon_data["tm_hm_moves"]:
            move_tutor_move = False

            md_file.write(f"""| - | - |\n""")
            for move in pokemon_data["tm_hm_moves"]:
                current_category = teachable_moves_category[move]

                # Write a separator between TMs / HMs and move tutor moves
                if not move_tutor_move and "Move Tutor" in current_category:
                    md_file.write(f"""| - | - |\n""")
                    move_tutor_move = True

                md_file.write(f"""| {current_category} | {move} |\n""")

        if pokemon_data["egg_moves"]:
            md_file.write(f"""| - | - |\n""")
            for move in pokemon_data["egg_moves"]:
                md_file.write(f"""| Egg Move | {move} |\n""")
            md_file.write("\n")

        # Write links to main learnset page.
        link_text = f"""[{pokemon_data.get("name")}]({pokemon_data.get("name").replace("(", "").replace(')', '').replace("'", "").replace(" ", "")})"""
        learnset_file.write(f"""{link_text}""")
        learnset_file.write("\n\n")

def generate_held_item_page(pokemon_data_list: list, held_item_file: str):
    """Generates a page showing Pokemon that can carry a held item and what item(s) they hold."""
    held_item_file.write(f"| Pokemon | Item 1 | Item 2 |\n")
    held_item_file.write(f"|:--------|:-------|:-------|\n")

    for pokemon_data in pokemon_data_list:
        held_item_one = pokemon_data.get("held_items", "No Item")[0]
        held_item_two = pokemon_data.get("held_items", "No Item")[1]
        if "No Item" not in held_item_one or "No Item" not in held_item_two:
            held_item_file.write(f"""| {pokemon_data.get("name")} | {held_item_one} | {held_item_two} |\n""")

    held_item_file.write("\n")

def generate_polished_changes_page(pokemon_data_list: list, changes_file: str):
    """Generates a page showing the differences in the Faithful vs Polished roms."""
    # Table of Contents.
    changes_file.write(f"""## Contents\n\n""")
    changes_file.write(f"""- [Polished Type Changes](#polished-type-changes)\n""")
    changes_file.write(f"""- [Polished Evolution Changes](#polished-evolution-changes)\n""")
    changes_file.write(f"""- [Polished Ability Changes](#polished-ability-changes)\n""")
    changes_file.write(f"""- [Polished Base Stat Changes](#polished-base-stat-changes)\n""")
    changes_file.write("\n")

    # Type changes.
    changes_file.write(f"""## Polished Type Changes\n\n""")
    changes_file.write(f"""| Pokemon                | {Mode.FAITHFUL.value} | {Mode.POLISHED.value} |\n""")
    changes_file.write(f"""|:-----------------------|:----------------------|:----------------------|\n""")
    for pokemon_data in pokemon_data_list:
        if pokemon_data["type_polished"]:
            type_f = ", ".join(pokemon_data["type_faithful"])
            type_p = ", ".join(pokemon_data["type_polished"])
            changes_file.write(f"""| {pokemon_data["name"]} | {type_f}              | {type_p}              |\n""")
    changes_file.write("\n")

    # Evolution changes.
    changes_file.write(f"## Polished Evolution Changes\n\n")
    for pokemon_data in pokemon_data_list:
        if pokemon_data["evo_data_polished"]:
            column_titles = [title.replace("_", " ").title() for title in pokemon_data["evo_data_faithful"][0].keys()]
            changes_file.write(f"| Version | {' | '.join(key for key in column_titles)} |\n")
            changes_file.write(f"|:--------|:- {' |:- '.join('' for key in column_titles)} |\n")

            for evo in pokemon_data["evo_data_faithful"]:
                column_values = [value for value in evo.values()]
                changes_file.write(f"| {Mode.FAITHFUL.value} | {' | '.join(value for value in column_values)} |\n")

            for evo in pokemon_data["evo_data_polished"]:
                column_values = [value for value in evo.values()]
                changes_file.write(f"| {Mode.POLISHED.value} | {' | '.join(value for value in column_values)} |\n")
    changes_file.write("\n")

    # Ability info.
    changes_file.write(f"## Polished Ability Changes\n\n")
    for pokemon_data in pokemon_data_list:
        if pokemon_data["abilities_polished"]:
            changes_file.write(f"""#### {pokemon_data.get("name")}\n\n""")
            changes_file.write(f"| Version | Abilities       |\n")
            changes_file.write(f"|:--------|:----------------|\n")
            abilities_f = ", ".join(pokemon_data["abilities_faithful"]).replace("_", " ").title()
            abilities_p = ", ".join(pokemon_data["abilities_polished"]).replace("_", " ").title()
            changes_file.write(f"| {Mode.FAITHFUL.value} | {abilities_f} |\n")
            changes_file.write(f"| {Mode.POLISHED.value} | {abilities_p} |\n")
            changes_file.write("\n")

    changes_file.write("\n")

    # Base stat changes.
    changes_file.write(f"""## Polished Base Stat Changes\n\n""")
    for pokemon_data in pokemon_data_list:
        if pokemon_data["stats_polished"]:
            changes_file.write(f"""#### {pokemon_data.get("name")}\n\n""")
            changes_file.write(f"| Version           | HP                    | Atk                    | Def                    | SAt                    | SDf                    | Speed                    |\n")
            changes_file.write(f"|:------------------|:----------------------|:-----------------------|:-----------------------|:-----------------------|:-----------------------|:-------------------------|\n")

            bsts_f = pokemon_data["stats_faithful"]
            bsts_p = pokemon_data["stats_polished"]
            bsts_p = {key: "-" if bsts_f[key] == bsts_p[key] else bsts_p[key] for key in bsts_f}

            changes_file.write(f"| {Mode.FAITHFUL.value} | {bsts_f.get('HP', 0)} | {bsts_f.get('Atk', 0)} | {bsts_f.get('Def', 0)} | {bsts_f.get('SAt', 0)} | {bsts_f.get('SDf', 0)} | {bsts_f.get('Speed', 0)} |\n")
            changes_file.write(f"| {Mode.POLISHED.value} | {bsts_p.get('HP', '-')} | {bsts_p.get('Atk', '-')} | {bsts_p.get('Def', '-')} | {bsts_p.get('SAt', '-')} | {bsts_p.get('SDf', '-')} | {bsts_p.get('Speed', '-')} |\n")
            changes_file.write("\n")

    changes_file.write("\n")


if __name__ == "__main__":
    # Read TMs, HMs, and move tutor.
    tmhm_file = find_asm_file("../polishedcrystal/data/moves/", "tmhm_moves.asm")
    teachable_moves_category = parse_teachable_moves_by_category(tmhm_file)

    # Read Johto Pokedex.
    johto_dex_file = find_asm_file("../polishedcrystal/data/pokemon/", "dex_order_new.asm")
    johto_dex = parse_johto_dex(johto_dex_file)

    # Find Pokemon base stat files.
    pokemon_asms = extract_base_stat_asm_filenames("../polishedcrystal/data/pokemon/base_stats.asm")

    # Create list of Pokemon data dicts.
    default_pokemon_data = {
        "name" : "",
        "egg_moves_name" : "",
        "evo_attacks_name" : "",
        "type_faithful": [],
        "type_polished": [],
        "abilities_faithful": [],
        "abilities_polished": [],
        "stats_faithful": {},
        "stats_polished": {},
        "held_items": [],
        "egg_groups": [],
        "evo_data_faithful": {},
        "evo_data_polished": {},
        "unique_wild_moves": [],
        "evolution_move": "",
        "level_up_moves": [],
        "egg_moves": [],
        "tm_hm_moves": [],
    }
    pokemon_data_list = [default_pokemon_data.copy() for asm in pokemon_asms]

    # Associates Dex list with base stat file.
    dex_order_base_stat_files = order_base_stat_files_by_dex(johto_dex, pokemon_asms)

    # Read level up moves and evolution methods.
    evos_attacks_file = find_asm_file("../polishedcrystal/data/pokemon/", "evos_attacks.asm")
    evos_attacks = parse_evos_attacks(evos_attacks_file)

    # Read egg moves.
    egg_moves_file = find_asm_file("../polishedcrystal/data/pokemon/", "egg_moves.asm")
    egg_moves = parse_egg_moves(egg_moves_file)

    # Read evolution moves.
    evolution_moves_file = find_asm_file("../polishedcrystal/data/pokemon/", "evolution_moves.asm")
    evolution_moves = parse_evolution_moves(evolution_moves_file)

    # Read unique wild moves.
    uniqe_wild_moves_file = find_asm_file("../polishedcrystal/data/pokemon/", "unique_wild_moves.asm")
    unique_wild_moves = parse_unique_wild_moves(uniqe_wild_moves_file)

    # Collate all relevant Pokemon data for the learnset pages.
    evolutions_egg_moves = []
    for base_stat_file, pokemon_data in zip(dex_order_base_stat_files, pokemon_data_list):
        # Remove ".asm" extension.
        pokemon_file = find_asm_file("../polishedcrystal/data/pokemon/base_stats", f"{base_stat_file}")
        name_without_ext = os.path.splitext(base_stat_file)[0]

        # Get display name, egg move name, and evo attack name.
        pokemon_data["name"], pokemon_data["egg_moves_name"], pokemon_data["evo_attacks_name"] = get_pokemon_names_for_files(name_without_ext)
        print(f"""pokemon names: { pokemon_data["name"]} {pokemon_data["egg_moves_name"]} {pokemon_data["evo_attacks_name"]}""")

        # Collect Pokemon data from base stat .asm file.
        pokemon_data = parse_pokemon_data(pokemon_file, pokemon_data)

        if pokemon_data["evo_attacks_name"] in evos_attacks:
            pokemon_data["evo_data_faithful"] = evos_attacks[pokemon_data["evo_attacks_name"]]["evo_data_faithful"]
            pokemon_data["evo_data_polished"] = evos_attacks[pokemon_data["evo_attacks_name"]]["evo_data_polished"]
            pokemon_data["level_up_moves"] = evos_attacks[pokemon_data["evo_attacks_name"]]["moves"]

        if pokemon_data["evo_attacks_name"] in evolution_moves:
            pokemon_data["evolution_move"] = evolution_moves[pokemon_data["evo_attacks_name"]]

        if pokemon_data["evo_attacks_name"] in unique_wild_moves:
            pokemon_data["unique_wild_moves"] = unique_wild_moves[pokemon_data["evo_attacks_name"]]

        if pokemon_data["egg_moves_name"] in egg_moves:
            pokemon_data["egg_moves"] = egg_moves[pokemon_data["egg_moves_name"]]
            # Check if this has an evolution that needs egg moves carried over.
            for evolution_data in pokemon_data["evo_data_faithful"]:
                save_egg_moves = (f"""{evolution_data["evolution"]}{evolution_data.get("form", "").split(" ")[0]}""", egg_moves[pokemon_data["egg_moves_name"]])
                # Don't double save if a Pokemon has multiple evolution methods for the same evolution. Ex - Eeevee.
                if save_egg_moves not in evolutions_egg_moves:
                    evolutions_egg_moves.append(save_egg_moves)

        # Check if this is an evolution that needs egg moves from the previous evolution carried over.
        for load_egg_moves in evolutions_egg_moves:
            if load_egg_moves[0] in pokemon_data["evo_attacks_name"]:
                pokemon_data["egg_moves"] = load_egg_moves[1]
                # Check if Pokemon has an evolution and carry over egg moves.
                for evolution_data in pokemon_data["evo_data_faithful"]:
                    save_egg_moves = (f"""{evolution_data["evolution"]}{evolution_data.get("form", "").split(" ")[0]}""", load_egg_moves[1])
                    # Don't double save if a Pokemon has multiple evolution methods for the same evolution. Ex - Eeevee.
                    if save_egg_moves not in evolutions_egg_moves:
                        evolutions_egg_moves.append(save_egg_moves)

    # Generate Pokemon learnset pages in Johto Pokedex order.
    with open("Pokemon-Learnsets.md", 'w') as learnset_file:
        for idx, pokemon_data in enumerate(pokemon_data_list):
            prev_pokemon_data = pokemon_data_list[idx - 1] if idx > 0 else {}
            next_pokemon_data = pokemon_data_list[idx + 1] if idx < len(pokemon_data_list) - 1 else {}

            md_file_name = f"""{pokemon_data.get("name").replace("(", "").replace(')', '').replace("'", "").replace(" ", "")}.md"""
            generate_pokemon_learnset_page(pokemon_data, md_file_name, learnset_file, prev_pokemon_data, next_pokemon_data, teachable_moves_category)

    # Write held items file.
    # TODO The online wiki added text to the top of this file. Every time this script runs it will overwrite the file with
    #      only the parsed information, so make sure to double check changes.
    with open("Wild-Held-Items.md", 'w') as held_items_file:
        generate_held_item_page(pokemon_data_list, held_items_file)

    # Write Polished differences file.
    with open("Pokemon-Type,-Evolution,-Ability,-and-Stat-Changes.md", 'w') as changes_file:
        generate_polished_changes_page(pokemon_data_list, changes_file)
