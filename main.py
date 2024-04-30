# VBT - Valheim Backup Tool
# --------------------------
# Author: Seshnik
# Version: 0.1

# Description:
# This script is designed to create backups of Valheim worlds and player data.
# It will also allow you to restore the backups if needed.
#
# The script will also allow you to delete old backups to save space.
# This may extend to creating backups of the Game Files for switching to the PTB.


# Imports
import os
import shutil
from datetime import datetime
from collections import defaultdict


def get_backup_path():
    appdata_path = os.getenv('APPDATA')
    return os.path.join(appdata_path, '..', 'LocalLow', 'IronGate', 'Valheim', 'VBT_BACKUPS')


def create_backup_folders():
    backup_root = get_backup_path()
    subfolders = ['worlds', 'characters', 'worlds_local', 'characters_local']
    for folder in subfolders:
        os.makedirs(os.path.join(backup_root, folder), exist_ok=True)


def get_save_path(saves):
    appdata_path = os.getenv('APPDATA')
    if saves == 'char':
        return os.path.join(appdata_path, '..', 'LocalLow', 'IronGate', 'Valheim', 'characters')

    elif saves == 'localchar':
        return os.path.join(appdata_path, '..', 'LocalLow', 'IronGate', 'Valheim', 'characters_local')

    elif saves == 'world':
        return os.path.join(appdata_path, '..', 'LocalLow', 'IronGate', 'Valheim', 'worlds')

    elif saves == 'localworld':
        return os.path.join(appdata_path, '..', 'LocalLow', 'IronGate', 'Valheim', 'worlds_local')


def list_saves(directory):
    save_files = defaultdict(list)
    valid_extensions = {'.fwl', '.db', '.fwl.old', '.db.old', '.fch'}  # Set of valid save file extensions
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and '_backup' not in f.lower()]
        for file in files:
            ext = os.path.splitext(file)[1]  # Get the file extension
            if ext in valid_extensions:
                base_name = file.split('.')[0]
                save_files[base_name].append(file)
    except Exception as e:
        print(f"Error accessing {directory}: {e}")
    return dict(save_files)


def display_world_saves():
    world_path = get_save_path('world')
    local_world_path = get_save_path('localworld')

    world_saves = list_saves(world_path)
    local_world_saves = list_saves(local_world_path)

    saves_list = []
    saves_map = {}

    # Add world saves
    for save in world_saves:
        saves_list.append(save)
        saves_map[save] = (world_path, world_saves[save])

    # Add local world saves with prefix
    for save in local_world_saves:
        display_name = "[Local Save] " + save
        saves_list.append(display_name)
        saves_map[display_name] = (local_world_path, local_world_saves[save])

    if not saves_list:
        print("No saves found.")
        return

    print("Available saves:")
    print("-" * 50)
    for i, save in enumerate(saves_list, 1):
        print(f"{i}. {save}")

    print("-" * 50)
    print(f"{len(saves_list) + 1}. Backup all")
    print(f"{len(saves_list) + 2}. Cancel")
    print(" ")
    choice = input("Select a save to backup OR choose to backup all saves: ")

    try:
        choice = int(choice)
        if choice == len(saves_list) + 2:
            print("Cancelling Backup...")
            clear_screen()
            return
        elif choice == len(saves_list) + 1:
            cleanScreen()
            print("Backing up all saves...")
            for name, (path, files) in saves_map.items():
                print(f"Backing up {name} from {path}...")
                backup_files('world' if 'Local Save' not in name else 'localworld', name.replace('[Local Save] ', ''), files)
                print(" ")
                print("-- BACKUP COMPLETE --")
                display_options()
        elif 1 <= choice <= len(saves_list):
            cleanScreen()
            selected_save = saves_list[choice - 1]
            save_path, files = saves_map[selected_save]
            print(f"Backing up {selected_save} from {save_path}...")
            backup_files('world' if '[Local Save]' not in selected_save else 'localworld', selected_save.replace('[Local Save] ', ''), files)
            print(" ")
            print("-- BACKUP COMPLETE --")
            display_options()
        else:
            print("Invalid choice.")
    except ValueError:
        print("Please enter a number.")


def display_character_saves():
    char_path = get_save_path('char')
    local_char_path = get_save_path('localchar')

    char_saves = list_saves(char_path)
    local_char_saves = list_saves(local_char_path)

    saves_list = []
    saves_map = {}

    # Add character saves
    for save in char_saves:
        saves_list.append(save)
        saves_map[save] = (char_path, char_saves[save])

    # Add local character saves with prefix
    for save in local_char_saves:
        display_name = "[Local Save] " + save
        saves_list.append(display_name)
        saves_map[display_name] = (local_char_path, local_char_saves[save])

    if not saves_list:
        print("No saves found.")
        return

    print("Available character saves:")
    print("-" * 50)
    for i, save in enumerate(saves_list, 1):
        print(f"{i}. {save}")

    print("-" * 50)
    print(f"{len(saves_list) + 1}. Backup all")
    print(f"{len(saves_list) + 2}. Cancel")
    print(" ")
    choice = input("Select a save to backup OR choose to backup all saves: ")

    try:
        choice = int(choice)
        if choice == len(saves_list) + 2:
            print("Cancelling Backup...")
            clear_screen()
            return
        elif choice == len(saves_list) + 1:
            cleanScreen()
            print("Backing up all saves...")
            for name, (path, files) in saves_map.items():
                print(f"Backing up {name} from {path}...")
                backup_files('char' if 'Local Save' not in name else 'localchar', name.replace('[Local Save] ', ''), files)
                print(" ")
                print("-- BACKUP COMPLETE --")
                display_options()
        elif 1 <= choice <= len(saves_list):
            selected_save = saves_list[choice - 1]
            save_path, files = saves_map[selected_save]
            cleanScreen()
            print(f"Backing up {selected_save} from {save_path}...")
            backup_files('char' if '[Local Save]' not in selected_save else 'localchar', selected_save.replace('[Local Save] ', ''), files)
            print(" ")
            print("-- BACKUP COMPLETE --")
            display_options()
        else:
            cleanScreen()
            print("Invalid choice.")
            display_options()
    except ValueError:
        print("Please enter a number.")


def backup_files(save_type, save_name, files):
    backup_root = get_backup_path()
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
    save_path_map = {
        'char': 'characters',
        'localchar': 'characters_local',
        'world': 'worlds',
        'localworld': 'worlds_local'
    }
    target_folder = save_path_map.get(save_type)
    if not target_folder:
        print(f"Unknown save type: {save_type}")
        return

    # Create a new subfolder for the backup
    backup_subfolder = f"{save_name}-{timestamp}"
    target_path = os.path.join(backup_root, target_folder, backup_subfolder)
    os.makedirs(target_path, exist_ok=True)

    for file in files:
        source = os.path.join(get_save_path(save_type), file)
        destination = os.path.join(target_path, file)
        try:
            shutil.copy2(source, destination)
            print(f"Backed up {file} to {destination}")
        except Exception as e:
            print(f"Failed to back up {file}: {e}")


def display_and_restore_backups():
    categories = {
        1: ['worlds', 'worlds_local'],
        2: ['characters', 'characters_local']
    }
    print("Select a category to restore from:")
    for index, category in categories.items():
        print(f"{index}. {category[0].capitalize()}")

    category_index = int(input("Enter the number corresponding to your choice: "))
    selected_category = categories.get(category_index)

    if selected_category:
        subcategory = select_subcategory(selected_category)
        if subcategory:
            backups = list_backups_in_category(subcategory)

            if backups:
                print("Available backups:")
                for i, backup in enumerate(backups, 1):
                    print(f"  {i}. {backup}")
                print("")

                backup_index = int(input(f"Choose the backup to restore from {subcategory}: ")) - 1
                if 0 <= backup_index < len(backups):
                    backup_to_restore = backups[backup_index]
                    confirm = input(f"Are you sure you want to restore {backup_to_restore}? (Y/N): ").lower()
                    if confirm.lower() == 'yes' or confirm.lower() == 'y':
                        restore_backup(subcategory, backup_to_restore)
                    else:
                        cleanScreen()
                        print(" --- Restoration cancelled. ---")
                        display_options()

                else:
                    cleanScreen()
                    display_options()
                    print("Invalid backup number provided, returning to main menu.")
            else:
                cleanScreen()
                display_options()
                print(f"No backups available for {subcategory}, returning to main menu.")
        else:
            cleanScreen()
            display_options()
            print("Invalid subcategory number provided, returning to main menu.")

    else:
        cleanScreen()
        display_options()
        print("Invalid category number provided, returning to main menu.")


def select_subcategory(categories):
    print("Select a subcategory:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category.capitalize()}")
    subcategory_index = int(input("Enter the number corresponding to your choice: ")) - 1
    if 0 <= subcategory_index < len(categories):
        return categories[subcategory_index]
    else:
        return None


def list_backups_in_category(category):
    backup_root = get_backup_path()
    category_path = os.path.join(backup_root, category)
    try:
        return [d for d in os.listdir(category_path) if os.path.isdir(os.path.join(category_path, d))]
    except FileNotFoundError:
        print(f"No backups found in {category_path}")
        return []


def restore_backup(category, backup_name):
    backup_root = get_backup_path()
    backup_path = os.path.join(backup_root, category, backup_name)
    if category.lower() == 'worlds_local':
        original_path = get_save_path("localworld")

    elif category.lower() == 'worlds':
        original_path = get_save_path("world")

    elif category.lower() == 'characters_local':
        original_path = get_save_path("localchar")

    elif category.lower() == 'characters':
        original_path = get_save_path("char")
    else:
        print(f"Unknown category: {category}")
        return
    print(f"Restoring from {backup_path} to {original_path}")
    if not os.path.exists(backup_path):
        print(f"Error: Backup path does not exist: {backup_path}")
        return
    if not os.path.exists(original_path):
        print(f"Error: Original path does not exist: {original_path}")
        return
    try:
        files = os.listdir(backup_path)
        for file in files:
            src = os.path.join(backup_path, file)
            dest = os.path.join(original_path, file)
            shutil.copy2(src, dest)
        print(f"Successfully restored {backup_name} to {original_path}")
        cleanScreen()
        display_options()
    except Exception as e:
        print(f"Error restoring backup: {e}")


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
        display_menu()
    else:
        os.system('clear')
        display_menu()


def cleanScreen():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # for linux, maybe Mac too.
        os.system('clear')


def display_menu():
    print(r"""
 ██▒   █▓ ▄▄▄▄   ▄▄▄█████▓
▓██░   █▒▓█████▄ ▓  ██▒ ▓▒
 ▓██  █▒░▒██▒ ▄██▒ ▓██░ ▒░
  ▒██ █░░▒██░█▀  ░ ▓██▓ ░ 
   ▒▀█░  ░▓█  ▀█▓  ▒██▒ ░ 
   ░ ▐░  ░▒▓███▀▒  ▒ ░░   
   ░ ░░  ▒░▒   ░     ░    
     ░░   ░    ░   ░                                                                                                                                                                                   
                """)
    print("Version: 0.1")
    print("Author: Nik (github.com/Seshnik)")
    print()
    display_options()


def display_options():
    print("┌───────────────────────┐")
    print("│  Valheim Backup Tool  │")
    print("├───────────────────────┤")
    print("│ 1. Backup Worlds      │")
    print("│ 2. Backup Characters  │")
    print("│ 3. Restore A Backup   │")
    print("│ 4. Delete Old Backups │")
    print("│ 5. Help               │")
    print("│ 6. Exit               │")
    print("└───────────────────────┘")


def display_help_menu():
    cleanScreen()
    print("\nHelp Menu")
    print("┌───────────────────────────────────────────────────────┐")
    print("│ 1. Backup Worlds                                      │")
    print("│    - Backs up all your world files to a secure        │")
    print("│      location. Each backup is timestamped for easy    │")
    print("│      identification.                                  │")
    print("│                                                       │")
    print("│ 2. Backup Characters                                  │")
    print("│    - Saves a copy of your character files. This       │")
    print("│      ensures you have a recoverable copy in case of   │")
    print("│      file corruption or loss.                         │")
    print("│                                                       │")
    print("│ 3. Restore a Backup                                   │")
    print("│    - Allows you to restore any of your previously     │")
    print("│      backed-up worlds or characters.                  │")
    print("│                                                       │")
    print("│ 4. Delete Old Backups                                 │")
    print("│    - This function does not yet exist in this version │")
    print("│      (It will allow you to remove old Backups)        │")
    print("│                                                       │")
    print("│ 5. Help                                               │")
    print("│    - Displays this help menu with information about   │")
    print("│      all available commands and their functions.      │")
    print("│                                                       │")
    print("│ 6. Exit                                               │")
    print("│    - Exits the backup tool.                           │")
    print("└───────────────────────────────────────────────────────┘")
    print("Thank you for using Valheim Backup Tool!\n")
    continiue = input("Press Enter to continue...")
    cleanScreen()
    display_menu()
    #display_options()


if __name__ == '__main__':
    create_backup_folders()
    display_menu()
    while True:
        #clear_screen()
        choice = input("Select an option: ")

        if choice == "1":
            display_world_saves()
        elif choice == "2":
            display_character_saves()
        elif choice == "3":
            display_and_restore_backups()
        elif choice == "4":
            print("Sorry, this has not been implemented yet!\n"
                  "You can delete the folders manually, located: AppData/LocalLow/IronGate/Valheim/VBT_BACKUPS")
        elif choice == "5":
            display_help_menu()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")
