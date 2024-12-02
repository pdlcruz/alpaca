# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainer, Seq2SeqTrainingArguments, DataCollatorForSeq2Seq
# from datasets import load_dataset
# from evaluate import load

# # Load tokenizer and model
# model_checkpoint = "meta-llama/Llama-3.1-8B-Instruct"
# tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
# model = AutoModelForSeq2SeqLM.from_pretrained(model_checkpoint)

# # Load your custom dataset (Reddit/Twitter posts)
# train_dataset = load_dataset("json", data_files="path_to_your_data.json", split="train")
# val_dataset = load_dataset("json", data_files="path_to_your_data.json", split="validation")

# # Preprocessing function
# def preprocess_function(examples):
#     inputs = [ex["input"] for ex in examples]
#     targets = [ex["output"] for ex in examples]
#     model_inputs = tokenizer(inputs, max_length=1024, truncation=True, padding="max_length")
#     labels = tokenizer(targets, max_length=128, truncation=True, padding="max_length")
#     model_inputs["labels"] = labels["input_ids"]
#     return model_inputs

# # Apply preprocessing to the datasets
# train_dataset = train_dataset.map(preprocess_function, batched=True)
# val_dataset = val_dataset.map(preprocess_function, batched=True)

# # Data collator to handle padding
# data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

# # Training arguments
# training_args = Seq2SeqTrainingArguments(
#     output_dir="./model",             # Output directory
#     evaluation_strategy="epoch",      # Evaluate after each epoch
#     learning_rate=2e-5,               # Learning rate
#     per_device_train_batch_size=16,   # Training batch size
#     per_device_eval_batch_size=16,    # Evaluation batch size
#     weight_decay=0.01,                # Weight decay
#     num_train_epochs=3,               # Number of epochs
#     predict_with_generate=True,       # Use generate for prediction
#     fp16=True,                        # Use mixed precision
# )

# # Trainer initialization
# trainer = Seq2SeqTrainer(
#     model=model,
#     args=training_args,
#     train_dataset=train_dataset,
#     eval_dataset=val_dataset,
#     data_collator=data_collator,
#     tokenizer=tokenizer
# )

# # Fine-tune the model
# trainer.train()

# # Save the fine-tuned model
# trainer.save_model("./model/final_model")

#######################
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainer, Seq2SeqTrainingArguments, DataCollatorForSeq2Seq
# from datasets import load_dataset
# from evaluate import load

# # Load tokenizer and model (Llama-3 as an example)
# print("Loading model and tokenizer...")
# model_checkpoint = "google-t5/t5-small"
# tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
# model = AutoModelForSeq2SeqLM.from_pretrained(model_checkpoint)
# print("Model and tokenizer loaded.")

# # 1. Load the Legal English Dataset (train split)
# print("Loading Legal English dataset...")
# legal_dataset = load_dataset("json", data_files={"train": "legal_english_train.json", "validation": "legal_english_validation.json"})

# # Access the train and validation splits
# train_legal_dataset = legal_dataset["train"]
# val_legal_dataset = legal_dataset["validation"]

# print("Legal English dataset loaded.")
# print(f"Train Legal Dataset: {train_legal_dataset}")
# print(f"Validation Legal Dataset: {val_legal_dataset}")

# # 2. Load the Spanish Vernacular Dataset (e.g., Reddit in Spanish)
# print("Loading Spanish Vernacular dataset...")
# spanish_dataset = load_dataset("json", data_files={"train": "reddit_spanish_train.json", "validation": "reddit_spanish_validation.json"})

# # Access the train and validation splits
# train_spanish_dataset = spanish_dataset["train"]
# val_spanish_dataset = spanish_dataset["validation"]

# print("Spanish Vernacular dataset loaded.")
# print(f"Train Spanish Dataset: {train_spanish_dataset}")
# print(f"Validation Spanish Dataset: {val_spanish_dataset}")

# # Preprocessing function
# # def preprocess_function(examples):
# #     print("Preprocessing data...")
# #     inputs = [ex["input"] for ex in examples]
# #     targets = [ex["output"] for ex in examples]
# #     model_inputs = tokenizer(inputs, max_length=1024, truncation=True, padding="max_length")
# #     labels = tokenizer(targets, max_length=128, truncation=True, padding="max_length")
# #     model_inputs["labels"] = labels["input_ids"]
# #     print("Preprocessing completed.")
# #     return model_inputs

# def preprocess_function(examples):
#     # For Legal English dataset
#     if "term" in examples and "definition" in examples:
#         inputs = examples["term"]
#         targets = examples["definition"]
    
#     # For Spanish Vernacular dataset
#     elif "text" in examples and "label" in examples:
#         inputs = examples["text"]
#         targets = examples["label"]
    
#     # Return the processed inputs and targets as needed
#     return {"inputs": inputs, "labels": targets}

# # Apply preprocessing to both datasets
# print("Applying preprocessing to datasets...")
# train_legal_dataset = train_legal_dataset.map(preprocess_function, batched=True)
# val_legal_dataset = val_legal_dataset.map(preprocess_function, batched=True)

# train_spanish_dataset = train_spanish_dataset.map(preprocess_function, batched=True)
# val_spanish_dataset = val_spanish_dataset.map(preprocess_function, batched=True)
# print("Preprocessing applied to all datasets.")

# # Data collator to handle padding
# print("Initializing data collator...")
# data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)
# print("Data collator initialized.")

# # Training arguments
# training_args = Seq2SeqTrainingArguments(
#     output_dir="./model",             # Output directory
#     evaluation_strategy="epoch",      # Evaluate after each epoch
#     learning_rate=2e-5,               # Learning rate
#     per_device_train_batch_size=16,   # Training batch size
#     per_device_eval_batch_size=16,    # Evaluation batch size
#     weight_decay=0.01,                # Weight decay
#     num_train_epochs=3,               # Number of epochs
#     predict_with_generate=True,       # Use generate for prediction
#     fp16=False,                        # Use mixed precision
# )

# # Stage 1: Fine-tune on Legal English Dataset
# print("Starting fine-tuning on Legal English dataset...")
# trainer = Seq2SeqTrainer(
#     model=model,
#     args=training_args,
#     train_dataset=train_legal_dataset,
#     eval_dataset=val_legal_dataset,
#     data_collator=data_collator,
#     tokenizer=tokenizer
# )

# # Train on legal dataset
# trainer.train()
# print("Fine-tuning on Legal English dataset completed.")

# # Save the model after legal fine-tuning
# trainer.save_model("./model/legal_finetuned_model")
# print("Model after legal fine-tuning saved.")

# # Stage 2: Fine-tune on Spanish Vernacular Dataset
# print("Starting fine-tuning on Spanish Vernacular dataset...")
# trainer = Seq2SeqTrainer(
#     model=model,
#     args=training_args,
#     train_dataset=train_spanish_dataset,
#     eval_dataset=val_spanish_dataset,
#     data_collator=data_collator,
#     tokenizer=tokenizer
# )

# # Train on Spanish vernacular dataset
# trainer.train()
# print("Fine-tuning on Spanish Vernacular dataset completed.")

# # Save the final model after all fine-tuning
# trainer.save_model("./model/final_model")
# print("Final model saved.")


from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainer, Seq2SeqTrainingArguments, DataCollatorForSeq2Seq
from datasets import load_dataset
from evaluate import load

# Load tokenizer and model (T5 model as an example)
print("Loading model and tokenizer...")
model_checkpoint = "google-t5/t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
model = AutoModelForSeq2SeqLM.from_pretrained(model_checkpoint)
print("Model and tokenizer loaded.")

# 1. Load the Legal English Dataset (train split)
print("Loading Legal English dataset...")
legal_dataset = load_dataset("json", data_files={"train": "legal_english_train.json", "validation": "legal_english_validation.json"})

# Access the train and validation splits
train_legal_dataset = legal_dataset["train"]
val_legal_dataset = legal_dataset["validation"]

print("Legal English dataset loaded.")
print(f"Train Legal Dataset: {train_legal_dataset}")
print(f"Validation Legal Dataset: {val_legal_dataset}")

# 2. Load the Spanish Vernacular Dataset (e.g., Reddit in Spanish)
print("Loading Spanish Vernacular dataset...")
spanish_dataset = load_dataset("json", data_files={"train": "reddit_spanish_train.json", "validation": "reddit_spanish_validation.json"})

# Access the train and validation splits
train_spanish_dataset = spanish_dataset["train"]
val_spanish_dataset = spanish_dataset["validation"]

print("Spanish Vernacular dataset loaded.")
print(f"Train Spanish Dataset: {train_spanish_dataset}")
print(f"Validation Spanish Dataset: {val_spanish_dataset}")

# Preprocessing function
def preprocess_function(examples):
    # For Legal English dataset
    if "term" in examples and "definition" in examples:
        inputs = examples["term"]
        targets = examples["definition"]
    
    # For Spanish Vernacular dataset
    elif "text" in examples and "label" in examples:
        inputs = examples["text"]
        targets = examples["label"]
    
    # Tokenize inputs and labels
    model_inputs = tokenizer(inputs, max_length=1024, truncation=True, padding="max_length")
    labels = tokenizer(targets, max_length=128, truncation=True, padding="max_length")
    
    # Ensure labels are formatted correctly
    model_inputs["labels"] = labels["input_ids"]
    
    return model_inputs

# Apply preprocessing to both datasets
print("Applying preprocessing to datasets...")
train_legal_dataset = train_legal_dataset.map(preprocess_function, batched=True)
val_legal_dataset = val_legal_dataset.map(preprocess_function, batched=True)

train_spanish_dataset = train_spanish_dataset.map(preprocess_function, batched=True)
val_spanish_dataset = val_spanish_dataset.map(preprocess_function, batched=True)
print("Preprocessing applied to all datasets.")

# Data collator to handle padding
print("Initializing data collator...")
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)
print("Data collator initialized.")

# Training arguments
training_args = Seq2SeqTrainingArguments(
    output_dir="./model",             # Output directory
    evaluation_strategy="epoch",      # Evaluate after each epoch
    learning_rate=2e-5,               # Learning rate
    per_device_train_batch_size=16,   # Training batch size
    per_device_eval_batch_size=16,    # Evaluation batch size
    weight_decay=0.01,                # Weight decay
    num_train_epochs=3,               # Number of epochs
    predict_with_generate=True,       # Use generate for prediction
    fp16=False,                       # Use mixed precision
)

# Stage 1: Fine-tune on Legal English Dataset
print("Starting fine-tuning on Legal English dataset...")
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_legal_dataset,
    eval_dataset=val_legal_dataset,
    data_collator=data_collator,
    tokenizer=tokenizer
)

# Train on legal dataset
trainer.train()
print("Fine-tuning on Legal English dataset completed.")

# Save the model after legal fine-tuning
trainer.save_model("./model/legal_finetuned_model")
print("Model after legal fine-tuning saved.")

# Stage 2: Fine-tune on Spanish Vernacular Dataset
print("Starting fine-tuning on Spanish Vernacular dataset...")
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_spanish_dataset,
    eval_dataset=val_spanish_dataset,
    data_collator=data_collator,
    tokenizer=tokenizer
)

# Train on Spanish vernacular dataset
trainer.train()
print("Fine-tuning on Spanish Vernacular dataset completed.")

# Save the final model after all fine-tuning
trainer.save_model("./model/final_model")
print("Final model saved.")


