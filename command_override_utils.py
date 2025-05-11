# command_override_utils.py
import json
import os
import config  # Import your config file

def get_current_state() -> dict:
    file_path = config.COMMAND_OVERRIDE_FILE_PATH
    # Renamed the key here
    default_state = {"command_override": config.DEFAULT_HEATING_COMMAND, "controller_on": False}

    if not os.path.exists(file_path):
        print(f"Warning: State file not found at '{file_path}', returning default state.")
        return default_state

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            # Ensure both keys exist, provide defaults if not
            command_override = data.get("command_override", default_state["command_override"])
            # Look for the new key name
            controller_on = data.get("controller_on", default_state["controller_on"])
            # Ensure controller_on is boolean
            if not isinstance(controller_on, bool):
                print(f"Warning: 'controller_on' value in file is not boolean ({controller_on}), returning default.")
                controller_on = default_state["controller_on"]

            # Return dictionary with the new key name
            return {"command_override": command_override, "controller_on": controller_on}

    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Error reading state file '{file_path}': {e}, returning default state.")
        return default_state
    except Exception as e:
        print(f"Error reading state file: {e}, returning default state.")
        return default_state

# Function to update specific keys in the state file atomically (No change needed internally)
def update_command_state_file(controller_on: bool = None, command_override: int = None) -> bool:
    file_path = config.COMMAND_OVERRIDE_FILE_PATH
    temp_file_path = file_path + ".tmp"

    to_update_state = get_current_state()
    if controller_on is not None:
        to_update_state["controller_on"] = controller_on
    if command_override:
        to_update_state["command_override"] = command_override

    try:
        os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)

        with open(temp_file_path, 'w') as f:
            json.dump(to_update_state, f, indent=4)

        os.replace(temp_file_path, file_path)

        print(f"State file '{file_path}' updated with: {to_update_state}")
        return True
    except (IOError, OSError) as e:
        print(f"Error: Failed to write state file '{file_path}': {e}")
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        return False
    except Exception as e:
        print(f"Error: Unexpected error when updating state file: {e}")
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        return False