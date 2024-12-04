import os
import pickle
import re
from datasets import Dataset, DatasetDict

# Directory containing the data
folder = 'reddit_data_unfiltered'
new_folder = 'reddit_data_cleaned'
os.makedirs(new_folder, exist_ok=True)

# Regex to match URLs
url_pattern = re.compile(r'https?://\S+|www\.\S+')

def clean_text(text):
    # Remove URLs
    text = url_pattern.sub("", text)
    # Remove asterisks
    text = text.replace('*', '')
    return text


def clean_and_split_text(text):
    # Split the text into lines
    lines = text.split('\n')
    # Remove any leading/trailing whitespace from each line
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    return cleaned_lines

def clean():
    data = []  # List to store cleaned data
    # Process each file in the directory
    data_array = []
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path) and filename.startswith('reddit_'):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Clean the content
            cleaned_content = clean_text(content)
            
            # Append cleaned data to list
            data.append({'text': cleaned_content})
            data_array.extend(clean_and_split_text(cleaned_content))

    return data, data_array


if __name__ == '__main__':
    cleaned_data, data_array = clean()
    # Convert list of dictionaries to a Hugging Face dataset
    dataset = Dataset.from_dict({'text': [entry['text'] for entry in cleaned_data]})
    # Wrap the dataset in a DatasetDict under the 'train' key
    dataset_dict = DatasetDict({
        'train': dataset
    })
    # Save the dataset to disk
    dataset_dict.save_to_disk('reddit_dataset')
    pickle.dump(data_array, open("data_array.pkl", "wb"))
    pickle.load(open("data_array.pkl", "rb"))
    # Example of how to access the 10th entry of the 'train' split
    # print(dataset_dict['train'][10])
    print("Dataset saved successfully.")
