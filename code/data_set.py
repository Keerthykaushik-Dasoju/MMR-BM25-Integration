import requests

#Method for fetching json data from api and saving it to a local file
def fetch_json_from_api_and_save(api_url, output_file, chunk_size=1024):
    try:
        response = requests.get(api_url, stream=True)
        response.raise_for_status()  # Check for any request errors

        # Raise an exception if the content is too large
        max_content_size = 500 * 1024 * 1024  # 400 MB
        content_size = 0

        with open(output_file, 'wb') as file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                content_size += len(chunk)
                if content_size > max_content_size:
                    raise ValueError("API response content is too large.")

                file.write(chunk)

        print(f"API response saved to {output_file}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except ValueError as e:
        print(f"Error processing data: {e}")

# URL of the API Personalization citation user
# api_url = "https://ciir.cs.umass.edu/downloads/LaMP/LaMP_1/dev/dev_questions.json"

# URL of the API Personalization citation time
# api_url = "https://ciir.cs.umass.edu/downloads/LaMP/time/LaMP_1/dev/dev_questions.json"

# URL of the API Personalized news categorization user
# api_url = "https://ciir.cs.umass.edu/downloads/LaMP/LaMP_2/dev/dev_questions.json"

# URL of the API Personalized news categorization time
# api_url = "https://ciir.cs.umass.edu/downloads/LaMP/time/LaMP_2/dev/dev_questions.json"

# URL of the API Personalized title generation user
# api_url = "https://ciir.cs.umass.edu/downloads/LaMP/LaMP_5/dev/dev_questions.json"

# URL of the API Personalized title generation time
api_url = "https://ciir.cs.umass.edu/downloads/LaMP/time/LaMP_5/dev/dev_questions.json"

# Specify the output file
output_file = "api_response.json"

# Fetch JSON data from the API and save to a file
fetch_json_from_api_and_save(api_url, output_file)
