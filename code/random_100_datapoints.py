import json
import random

# Specify the path to your JSON file
input_file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/DataSets/time/personalization_title_generation.json'

output_file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/LabelOutputs/time/personalization_title_generation.json'

# Specify the path for the new JSON file
trimmed_input_file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/code/trimmed_input.json'

trimmed_output_file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/code/trimmed_output.json'


# Method to get json content from a file
def get_json_from_file(file_path, fileType):
    try:
        with open(file_path, 'r') as file:
            # Load JSON content from the file
            json_content = json.load(file)

        # Check if the content is a list
        if isinstance(json_content, fileType):
            return json_content
        else:
            raise ValueError("JSON content is not a list.")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    except ValueError as e:
        print(f"Error: {e}")
        return None

# Get Json from the file
input_data = get_json_from_file(input_file_path, list)

output_data = get_json_from_file(output_file_path, dict)

golds = output_data['golds']

print(len(input_data))

# Set the range and the number of random integers
lower_limit = 0
upper_limit = len(input_data)-1
number_of_integers = 100

# Generate a list of random integers
random_integers = [random.randint(lower_limit, upper_limit) for _ in range(number_of_integers)]

# Create a new list using the random integers as indices
trimmed_input_data = [input_data[index] for index in random_integers]

trimmed_golds = [golds[index] for index in random_integers]

trimmed_output_data = {}

trimmed_output_data['task'] = output_data['task']

trimmed_output_data['golds'] = trimmed_golds

# Save the selected data to a new JSON file
with open(trimmed_input_file_path, 'w') as new_input_file:
    json.dump(trimmed_input_data, new_input_file, indent=2)

with open(trimmed_output_file_path, 'w') as new_output_file:
    json.dump(trimmed_output_data, new_output_file, indent=2)

print("New JSON file created with selected data.")


