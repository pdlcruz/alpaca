from transformers import AutoTokenizer, AutoModelForCausalLM, Seq2SeqTrainer, Seq2SeqTrainingArguments, DataCollatorForSeq2Seq
from datasets import load_dataset
import os

# Load tokenizer and model
print("Loading model and tokenizer...")
model_checkpoint = "meta-llama/Llama-3.1-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
model = AutoModelForCausalLM.from_pretrained(model_checkpoint)
print("Model and tokenizer loaded.")


text_file = "reddit_data_cleaned/reddit_PERU.txt"
print(f"Loading dataset from {text_file}...")
dataset = load_dataset("text", data_files={"train": text_file})
train_dataset = dataset["train"]

def preprocess_function(examples):
    inputs = examples["text"]
    targets = inputs

    model_inputs = tokenizer(inputs, max_length=512, truncation=True, padding="max_length")
    labels = tokenizer(targets, max_length=128, truncation=True, padding="max_length")

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

print(f"Applying preprocessing to {text_file}...")
train_dataset = train_dataset.map(preprocess_function, batched=True)
print(f"Preprocessing completed for {text_file}.")

# Data collator for dynamic padding
print("Initializing data collator...")
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)
print("Data collator initialized.")

training_args = Seq2SeqTrainingArguments(
    output_dir="./alpaca_single_file",  # Output directory specific to the file
    evaluation_strategy="no",          # No evaluation for independent files
    learning_rate=2e-5,                 # Learning rate
    per_device_train_batch_size=16,     # Training batch size
    weight_decay=0.01,                  # Weight decay
    num_train_epochs=3,                 # Number of epochs
    predict_with_generate=True,         # Use generate for prediction
    fp16=False,                         # Use mixed precision
    save_total_limit=1,                 # Limit total saved checkpoints
)

print(f"Initializing trainer for {text_file}...")
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    data_collator=data_collator,
    tokenizer=tokenizer
)
print(f"Trainer initialized for {text_file}.")

# Fine-tune the model
print(f"Starting fine-tuning for {text_file}...")
trainer.train()
print(f"Fine-tuning completed for {text_file}.")

trainer.save_model("./alpaca")
print(f"Model saved for {text_file}.")
