import json
import os
import random
from pathlib import Path

from openai import OpenAI

openai_api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=openai_api_key)

random.seed(12102017)
tickers_list = json.load(Path("extracted_tickers.json").open())  # NOQA
random.shuffle(tickers_list)

split_index = int(0.8 * len(tickers_list))
train_data, validation_data = (tickers_list[:split_index], tickers_list[split_index:])


def save_to_jsonl(data: list[dict], output_file_path: str) -> None:
    jsonl_data = [
        {
            "messages": [
                {
                    "role": "system",
                    "content": "Given an asset listed on a stock exchange, return the associated ticker symbol as it appears on Yahoo finance. Keep in mind Yahoo Finance often adds a suffix based on the relevant exchange, such as '.NZ' for New Zealand, '.AX' for Australia, '.T' for Japan, etc.",
                },
                {
                    "role": "user",
                    "content": f'{"United States" if "country" not in item else item["country"]} asset "{item["name"]}"',
                },
                {"role": "assistant", "content": f"{item['ticker']}"},
            ]
        }
        for item in data
    ]

    # Save to JSONL format
    with Path(output_file_path).open("w") as f:
        for item in jsonl_data:
            f.write(json.dumps(item) + "\n")


train_output_file_path = "data/train.jsonl"
validation_output_file_path = "data/valid.jsonl"

save_to_jsonl(train_data, train_output_file_path)
save_to_jsonl(validation_data, validation_output_file_path)

train_file = client.files.create(
    file=Path(train_output_file_path).open("rb"), purpose="fine-tune"
)

valid_file = client.files.create(
    file=Path(validation_output_file_path).open("rb"), purpose="fine-tune"
)

print(f"Training file Info: {train_file}")
print(f"Validation file Info: {valid_file}")

model = client.fine_tuning.jobs.create(
    training_file=train_file.id,
    validation_file=valid_file.id,
    model="gpt-4.1-nano-2025-04-14",
    hyperparameters={"n_epochs": 3, "batch_size": 8, "learning_rate_multiplier": 0.03},
)
job_id = model.id
status = model.status

print(f"Fine-tuning model with jobID: {job_id}.")
print(f"Training Response: {model}")
print(f"Training Status: {status}")
