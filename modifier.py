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
    text = url_pattern.sub("", text)
    text = text.replace('*', '')
    return text


def clean_and_split_text(text):
    lines = text.split('\n')
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    return cleaned_lines

def clean():
    data = [] 
    data_array = []
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path) and filename.startswith('reddit_'):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            cleaned_content = clean_text(content)
            
            data.append({'text': cleaned_content})
            data_array.extend(clean_and_split_text(cleaned_content))

    return data, data_array


if __name__ == '__main__':
    cleaned_data, data_array = clean()

    dataset = Dataset.from_dict({'text': [entry['text'] for entry in cleaned_data]})

    dataset_dict = DatasetDict({
        'train': dataset
    })

    dataset_dict.save_to_disk('reddit_dataset')
    pickle.dump(data_array, open("data_array.pkl", "wb"))
    pickle.load(open("data_array.pkl", "rb"))
    print("Dataset saved successfully.")
