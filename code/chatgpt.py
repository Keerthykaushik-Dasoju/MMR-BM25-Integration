import openai

import os

import pandas as pd

import time, json

openai.api_key = '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'

def get_completion(prompt, model="gpt-3.5-turbo"):

    messages = [{"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(

    model=model,

    messages=messages,

    temperature=0,

    )

    return response.choices[0].message["content"]

def generate_answers(queries, task, data_type, method):
    # Initialize the output dictionary
    output = {}
    # Set the task in the output dictionary
    output['task'] = task
    # Initialize the list to store individual query outputs
    output_list = []
    print("started generating answers")
     # Counter for tracking progress
    counter = 0
    for query in queries:
        # Extract input and ID from the query
        input = query['input']
        id = query['id']
        # Get completion/response for the input
        response = get_completion(input)
        # Create a dictionary for the current query's output
        current_output = {}
        current_output['id'] = id
        current_output['output'] = response
        # Append the current output to the list
        output_list.append(current_output)
        # Increment the counter and print progress
        counter += 1
        print(counter)
    # Add the list of query outputs to the output dictionary
    output['golds'] = output_list
    # Specify the path for the new JSON file
    path = task+'_'+data_type+'_'+method+'_output'
    new_file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/code/results/'+path+'.json'
    with open(new_file_path, 'w') as new_file:
        json.dump(output, new_file, indent=2)


def get_json_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            # Load JSON content from the file
            json_content = json.load(file)

        # Check if the content is a list
        if isinstance(json_content, list):
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

# Specify the path to your JSON file
file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/UpdatedQueries/time/mmr/personalization_title_generation.json'
file_type = "LaMP_5"

def generate_answer_files(file_path,file_type,data_type,method):
    # Error conditions
    if file_type == "LaMP_1" and "personalization_citation" not in file_path:
        print("incorrect file path or file type, make sure both should point to same data set")
    elif file_type == "LaMP_2" and "personalization_news_categorization" not in file_path:
        print("incorrect file path or file type, make sure both should point to same data set")
    elif file_type == "LaMP_5" and "personalization_title_generation" not in file_path:
        print("incorrect file path or file type, make sure both should point to same data set")
    else:
        # Get Json from the file
        json_array = get_json_from_file(file_path)
        generate_answers(json_array, file_type, data_type, method)

# Specify the path to your JSON file
# file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/UpdatedQueries/user/bm25/personalization_citation.json'
# file_type = "LaMP_1"
# data_type = "user"
# method = "bm25"
# generate_answer_files(file_path, file_type, data_type, method)

# file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/UpdatedQueries/user/mmr/personalization_citation.json'
# file_type = "LaMP_1"
# data_type = "user"
# method = "mmr"
# generate_answer_files(file_path, file_type, data_type, method)

# file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/UpdatedQueries/time/bm25/personalization_citation.json'
# file_type = "LaMP_1"
# data_type = "time"
# method = "bm25"
# generate_answer_files(file_path, file_type, data_type, method)

# file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/UpdatedQueries/time/mmr/personalization_citation.json'
# file_type = "LaMP_1"
# data_type = "time"
# method = "mmr"
# generate_answer_files(file_path, file_type, data_type, method)

# file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/UpdatedQueries/user/bm25/personalization_news_categorization.json'
# file_type = "LaMP_2"
# data_type = "user"
# method = "bm25"
# generate_answer_files(file_path, file_type, data_type, method)

# file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/UpdatedQueries/user/mmr/personalization_news_categorization.json'
# file_type = "LaMP_2"
# data_type = "user"
# method = "mmr"
# generate_answer_files(file_path, file_type, data_type, method)

# file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/UpdatedQueries/time/bm25/personalization_news_categorization.json'
# file_type = "LaMP_2"
# data_type = "time"
# method = "bm25"
# generate_answer_files(file_path, file_type, data_type, method)

# file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/UpdatedQueries/time/mmr/personalization_news_categorization.json'
# file_type = "LaMP_2"
# data_type = "time"
# method = "mmr"
# generate_answer_files(file_path, file_type, data_type, method)


# file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/UpdatedQueries/user/bm25/personalization_title_generation.json'
# file_type = "LaMP_5"
# data_type = "user"
# method = "bm25"
# generate_answer_files(file_path, file_type, data_type, method)

# file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/UpdatedQueries/user/mmr/personalization_title_generation.json'
# file_type = "LaMP_5"
# data_type = "user"
# method = "mmr"
# generate_answer_files(file_path, file_type, data_type, method)

# file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/UpdatedQueries/time/bm25/personalization_title_generation.json'
# file_type = "LaMP_5"
# data_type = "time"
# method = "bm25"
# generate_answer_files(file_path, file_type, data_type, method)

file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/UpdatedQueries/time/mmr/personalization_title_generation.json'
file_type = "LaMP_5"
data_type = "time"
method = "mmr"
generate_answer_files(file_path, file_type, data_type, method)