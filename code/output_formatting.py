import json

def get_json_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            # Load JSON content from the file
            json_content = json.load(file)

        # Check if the content is a list
        if isinstance(json_content, dict):
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


def personalization_citation_output_formatting():
    # Specify the path to your JSON file
    file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/lambda_0.6_k_4/CalculatedOutputs/user/mmr/personalization_citation.json'
    
    # Get Json from the file
    json_content = get_json_from_file(file_path)

    new_json_content = {}

    new_json_content['task'] = json_content['task']

    golds = json_content['golds']

    new_golds = []

    for gold in golds:

        each_gold_id = gold['id']

        each_gold_output = gold['output']

        each_new_gold = {}

        each_new_gold['id'] = each_gold_id

        each_new_gold['output'] = each_gold_output[:3]

        new_golds.append(each_new_gold)
    
    new_json_content['golds'] = new_golds

    new_file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/code/formatted_output.json'

    # Save the selected data to a new JSON file
    with open(new_file_path, 'w') as new_file:
        json.dump(new_json_content, new_file, indent=2)

    print("New JSON file created with selected data.")

personalization_citation_output_formatting()
