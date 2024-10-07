from rank_bm25 import BM25Okapi
import re
import json

def bm25(documents, query, parameters_combined):

    # Tokenize the query
    tokenized_query = query.lower().split()

    tokenized_documents = [doc.split() for doc in parameters_combined]

    # Initialize BM25 model
    bm25 = BM25Okapi(tokenized_documents)

    # Get BM25 scores for each document
    scores = bm25.get_scores(tokenized_query)

    # Combine scores with document IDs
    document_scores = list(zip(range(len(documents)), scores))

    # Sort documents by BM25 score in descending order
    sorted_documents = sorted(document_scores, key=lambda x: x[1], reverse=True)

    return sorted_documents

def bm25_for_two_documents(doc1, doc2):
    tokenized_doc1 = doc1.lower().split()
    tokenized_doc2 = doc2.lower().split()

    # Combine documents into a list
    corpus = [tokenized_doc1, tokenized_doc2]

    # Initialize BM25 model
    bm25 = BM25Okapi(corpus)

    # Get BM25 score between document 1 and document 2
    bm25_score = bm25.get_scores(tokenized_doc1)[1]

    # Print BM25 score
    # print(f"BM25 score between Document 1 and Document 2: {bm25_score}")

    return bm25_score

def mmr(documents, parameters_combined, sorted_documents, lambda_param):
    
    # Initialize the set of selected documents
    selected_documents = [sorted_documents[0][0]]

    # Update the selected documents using MMR
    for _ in range(1, min(10, len(documents))):
        max_mmr = float('-inf')
        selected_doc = None

        for doc_id, score in sorted_documents[:20]:
            if doc_id not in selected_documents:
                # Calculate MMR score
                mmr_score = lambda_param * score - (1 - lambda_param) * max([bm25_for_two_documents(parameters_combined[doc_id], parameters_combined[selected_doc_id]) for selected_doc_id in selected_documents])

                # Update selected document if MMR score is greater
                if mmr_score > max_mmr:
                    max_mmr = mmr_score
                    selected_doc = doc_id

        # Add the selected document to the set
        selected_documents.append(selected_doc)

    return selected_documents

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
    
def update_queries(file_path, task, lambda_param):
    # Get Json from the file
    json_array = get_json_from_file(file_path)

    number_of_data_points = len(json_array)

    bm25_queries = []
    mmr_queries = []

    for i in range(number_of_data_points):
        # Assuming query is the paper title you provided
        input = json_array[i]['input']
        id = json_array[i]['id']
        your_profile_documents = json_array[i]['profile']

        if (task == "LaMP_1"):

            parameters_combined = [(doc['title'] + ' ' + doc['abstract']).lower() for doc in your_profile_documents]

            match = re.search(r'"([^"]*)"', input)

            # Print the first extracted title
            if not match:
                print(f"did not get a match, so skipping this input : {input}")
            query = match.group(1)

        elif (task == "LaMP_2"):

            parameters_combined = [(doc['text'] + ' ' + doc['category']).lower() for doc in your_profile_documents]

            input_split = input.split("article:")

            query = input_split[1]

        elif (task == "LaMP_5"):

            parameters_combined = [(doc['title'] + ' ' + doc['abstract']).lower() for doc in your_profile_documents]

            query = input.replace("Generate a title for the following abstract of a paper: ", "")

        bm25_docs = bm25(your_profile_documents, query, parameters_combined)

        # Use MMR to get the top 10 diverse and relevant results
        mmr_documents = mmr(your_profile_documents, parameters_combined, bm25_docs, lambda_param)

        # Get the top n results
        n = 3

        top_n_bm25_results = [your_profile_documents[doc_id] for doc_id, _ in bm25_docs[:n+1]]

        top_n_mmr_results = [your_profile_documents[doc_id] for doc_id in mmr_documents[:n+1]]
        
        bm25_query = query + " "

        mmr_query = query + " "


        for j in range(n):
            if task == "LaMP_1":
                bm25_query += top_n_bm25_results[j+1]['title']
                mmr_query += top_n_mmr_results[j+1]['title']
            elif task == "LaMP_2":
                bm25_query += top_n_bm25_results[j]['text']
                mmr_query += top_n_mmr_results[j]['text']
            elif task == "LaMP_5":
                bm25_query += top_n_bm25_results[j]['abstract']
                mmr_query += top_n_mmr_results[j]['abstract']
            if j != n-1:
                bm25_query += " "
                mmr_query += " "

        bm25_input = input.replace(query, bm25_query)
        mmr_input = input.replace(query, mmr_query)

        current_query_bm25 = {}
        current_query_bm25['id'] = id
        current_query_bm25['input'] = bm25_input
        bm25_queries.append(current_query_bm25)

        current_query_mmr = {}
        current_query_mmr['id'] = id
        current_query_mmr['input'] = mmr_input
        mmr_queries.append(current_query_mmr)

    return bm25_queries, mmr_queries

# Specify the path to your JSON file
file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/TrimmedDataSets/time/personalization_title_generation.json' #chage the file_type as well
file_type = "LaMP_5" #change the file_path as well 

lambda_params = [0.4, 0.5, 0.6]

def update(file_path, file_type, lambda_param, new_file_path):

    if file_type == "LaMP_1" and "personalization_citation" not in file_path:
        print("incorrect file path or file type, make sure both should point to same data set")
    elif file_type == "LaMP_2" and "personalization_news_categorization" not in file_path:
        print("incorrect file path or file type, make sure both should point to same data set")
    elif file_type == "LaMP_5" and "personalization_title_generation" not in file_path:
        print("incorrect file path or file type, make sure both should point to same data set")
    else:
        bm25_queries, mmr_queries = update_queries(file_path, file_type, lambda_param)

        # Specify the path for the new JSON file
        bm25_new_file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/code/bm25_queries_k_3'+new_file_path+'.json'
        with open(bm25_new_file_path, 'w') as bm25_new_file:
            json.dump(bm25_queries, bm25_new_file, indent=2)

        # Specify the path for the new JSON file
        mmr_new_file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/code/mmr_queries_k_3'+new_file_path+'.json'
        with open(mmr_new_file_path, 'w') as mmr_new_file:
            json.dump(mmr_queries, mmr_new_file, indent=2)

for lambda_param in lambda_params:
    # Specify the path to your JSON file
    file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/TrimmedDataSets/user/personalization_citation.json' #chage the file_type as well
    file_type = "LaMP_1" #change the file_path as well 
    update(file_path, file_type, lambda_param, str(lambda_param)+"user_1")

    # Specify the path to your JSON file
    file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/TrimmedDataSets/time/personalization_citation.json' #chage the file_type as well
    file_type = "LaMP_1" #change the file_path as well 
    update(file_path, file_type, lambda_param, str(lambda_param)+"time_1")

    # Specify the path to your JSON file
    file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/TrimmedDataSets/user/personalization_news_categorization.json' #chage the file_type as well
    file_type = "LaMP_2" #change the file_path as well 
    update(file_path, file_type, lambda_param, str(lambda_param)+"user_2")

    # Specify the path to your JSON file
    file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/TrimmedDataSets/time/personalization_news_categorization.json' #chage the file_type as well
    file_type = "LaMP_2" #change the file_path as well 
    update(file_path, file_type, lambda_param, str(lambda_param)+"time_2")

    # Specify the path to your JSON file
    file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/TrimmedDataSets/user/personalization_title_generation.json' #chage the file_type as well
    file_type = "LaMP_5" #change the file_path as well 
    update(file_path, file_type, lambda_param, str(lambda_param)+"user_5")

    # Specify the path to your JSON file
    file_path = '/home/keerthykaushik/UMass/F23/646-IR/Project/TrimmedDataSets/time/personalization_title_generation.json' #chage the file_type as well
    file_type = "LaMP_5" #change the file_path as well 
    update(file_path, file_type, lambda_param, str(lambda_param)+"time_5")