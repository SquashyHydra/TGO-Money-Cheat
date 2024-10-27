import lzstring, os, sys, glob, json
from pathlib import Path

current_directory = Path.home() / 'AppData' / 'Local' / 'User Data'
save_data_json = str(current_directory / "save_data.json")

try:
    rpgsave_files = glob.glob("DefaultTGOfile*.rpgsave", root_dir=str(current_directory))
except Exception as e:
    print("no save files")
    os._exit(1)

sys.tracebacklimit = 0

def read_save_file(save_file):
    try:
        with open(save_file, "r") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"please in put a number from 1-{len(rpgsave_files)}")

def get_temp_data():
    with open(save_data_json, 'r') as json_file:
        data = json.load(json_file)
    return data

def decode_rpgsave(save_file):
    lz = lzstring.LZString()
    save = read_save_file(save_file)
    decoded = lz.decompressFromBase64(save)
    parsed = json.loads(decoded)
    return parsed

def encode_rpgsave():
    lz = lzstring.LZString()
    parsed = get_temp_data()
    minified = json.dumps(parsed, separators=(',', ':'))
    encoded = lz.compressToBase64(minified)
    return encoded

def save_temp_data(save_data):
    with open(save_data_json, 'w') as json_file:
        json.dump(save_data, json_file, indent=4, sort_keys=True)
    create_new_game_save()

def create_new_game_save():
    i = 1
    for file in rpgsave_files:
        print(f"{file.replace(".rpgsave", "").replace("DefaultTGOfile", "")}: Save {file.replace(".rpgsave", "").replace("DefaultTGOfile", "")} -- {file}")
        if i <= len(rpgsave_files):
            i += 1
    try:
        choice = int(input("select a save file to overwrite: "))
        if choice < 1 or selected_file > len(rpgsave_files):
            if choice == selected_file:
                print("you are not supposed to select the save you are trying to edit, incase something goes wrong")
                os._exit(1)
    except ValueError:
        print("you are not supposed to select the save you are trying to edit, incase something goes wrong")
        os._exit(1)
    new_save_file = str(current_directory / f"DefaultTGOfile{choice}.rpgsave")
    game_data = encode_rpgsave()
    with open(new_save_file, 'w') as file:
        file.write(game_data)
    cleanup()

def cleanup():
    try:
        os.remove(save_data_json)
    except FileNotFoundError:
        pass

def money_cheat(save_data):
    variables = save_data['variables']
    game_variables = variables['_data']['@a']
    value_search = input("Enter the amount of money you have: ")
    i = 0
    value_replace = input("Enter the amount of money you want: ")
    for game_var in game_variables:
        if isinstance(game_var, int):
            if game_var == int(value_search):
                game_variables[i] = int(value_replace)
        i += 1
    return save_data

def user_select_save():
    i = 1

    for file in rpgsave_files:
        print(f"{file.replace(".rpgsave", "").replace("DefaultTGOfile", "")}: Save {file.replace(".rpgsave", "").replace("DefaultTGOfile", "")} -- {file}")
        if i <= len(rpgsave_files):
            i += 1

    try:
        selected_file = int(input(f"select the save file you want to edit(1-{len(rpgsave_files)}): "))
        if selected_file < 1 or selected_file > len(rpgsave_files):
            raise ValueError(f"Value must be a integer from 1-{len(rpgsave_files)}")
        return selected_file
    except ValueError:
        print(f"please select the save you want to edit 1-{len(rpgsave_files)}")
        os._exit(1)

def main():
    save_file = str(current_directory / f"DefaultTGOfile{selected_file}.rpgsave")

    save_data = decode_rpgsave(save_file)

    save_data = money_cheat(save_data)

    save_temp_data(save_data)

if __name__ == "__main__":
    try:
        selected_file = user_select_save()
        main()
    except Exception as e:
        print(e)
    finally:
        cleanup()