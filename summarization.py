#summarization.py
import transformers
import torch
import argparse
from transformers import AutoTokenizer, AutoModelForCausalLM


MODEL_ID = "meta-llama/Llama-3.1-8B-Instruct"

print("Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.bfloat16, 
    device_map="auto",         
)

# Function to summarize text
def summarize_text(input_text, max_new_tokens=150):
    """
    Summarize the input text using the Meta-Llama model.

    Args:
        input_text (str): The input document to summarize.
        max_new_tokens (int): Maximum tokens in the summary.

    Returns:
        str: The generated summary.
    """
    prompt = f"Summarize the following text in Spanish:\n\n{input_text}\n\nSummary:"
    print("Generating summary...")
    outputs = model.generate(
        **tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024).to("cuda"),
        max_new_tokens=max_new_tokens,
        num_beams=4,  
        early_stopping=True,
    )
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return summary


def summarize_batch(input_texts, max_new_tokens=150):
    """
    Summarize multiple input texts.

    Args:
        input_texts (list of str): List of documents to summarize.
        max_new_tokens (int): Maximum tokens in each summary.

    Returns:
        list of str: List of generated summaries.
    """
    summaries = []
    for text in input_texts:
        summaries.append(summarize_text(text, max_new_tokens))
    return summaries


# Command-line interface
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize text using Meta-Llama-3.1-8B-Instruct")
    parser.add_argument("--text", type=str, help="Input text to summarize", required=False)
    parser.add_argument("--file", type=str, help="Path to a text file to summarize", required=False)
    parser.add_argument("--batch_file", type=str, help="Path to a text file with multiple lines for batch summarization", required=False)
    parser.add_argument("--max_tokens", type=int, default=150, help="Maximum tokens for the summary")

    args = parser.parse_args()

    if args.text:
        print("Summarizing single input...")
        summary = summarize_text(args.text, args.max_tokens)
        print("\nGenerated Summary:\n", summary)

    elif args.file:
        print(f"Reading file: {args.file}")
        with open(args.file, "r", encoding="utf-8") as f:
            input_text = f.read()
        summary = summarize_text(input_text, args.max_tokens)
        print("\nGenerated Summary:\n", summary)

    elif args.batch_file:
        print(f"Reading batch file: {args.batch_file}")
        with open(args.batch_file, "r", encoding="utf-8") as f:
            input_texts = f.readlines()
        summaries = summarize_batch(input_texts, args.max_tokens)
        print("\nGenerated Summaries:\n")
        for i, summary in enumerate(summaries, 1):
            print(f"Summary {i}:\n{summary}\n")
    else:
        print("Please provide --text, --file, or --batch_file as input.")
