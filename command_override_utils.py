# command_override_utils.py
import json
import os
import config  # Import your config file


def get_command_override(default_value: int = config.DEFAULT_HEATING_COMMAND) -> int:
    """
    Retrieves the command override value from the file specified in config.py.
    Returns the default_value if the file doesn't exist, is empty, or malformed.
    """
    try:
        with open(config.COMMAND_OVERRIDE_FILE_PATH, 'r') as f:
            data = json.load(f)

        override_value = data.get("command_override")  # Expects {"command_override": XX} in the JSON

        if override_value is None:
            # Key "command_override" not found in JSON
            # print(f"Debug: Key 'command_override' not found in {config.COMMAND_OVERRIDE_FILE_PATH}. Using default: {default_value}")
            return default_value

        # Attempt to cast to int, handle potential errors
        return int(override_value)

    except FileNotFoundError:
        # File doesn't exist, so no override is set
        # print(f"Debug: Override file {config.COMMAND_OVERRIDE_FILE_PATH} not found. Using default: {default_value}")
        return default_value
    except Exception as e:  # Catch any other unexpected errors
        print(f"Warning: Unexpected error when getting command override: {e}. Using default: {default_value}")
        return default_value


def set_command_override(new_command_value: int) -> bool:
    """
    Updates the command override value in the file specified in config.py.
    Writes the value as JSON: {"command_override": new_command_value}
    Returns True on success, False on failure.
    """
    try:
        # Ensure the target directory exists (Docker should have mounted it, but good practice)
        os.makedirs(config.COMMAND_OVERRIDE_DIR, exist_ok=True)

        temp_file_path = config.COMMAND_OVERRIDE_FILE_PATH + ".tmp"

        with open(temp_file_path, 'w') as f:
            json.dump({"command_override": new_command_value}, f)

        # Atomically move the temporary file to the actual file path
        os.rename(temp_file_path, config.COMMAND_OVERRIDE_FILE_PATH)

        print(f"Command override updated to {new_command_value} in '{config.COMMAND_OVERRIDE_FILE_PATH}'")
        return True
    except (IOError, OSError) as e:
        print(f"Error: Failed to write command override file '{config.COMMAND_OVERRIDE_FILE_PATH}': {e}")
        return False
    except Exception as e:  # Catch any other unexpected errors
        print(f"Error: Unexpected error when setting command override: {e}")
        return False