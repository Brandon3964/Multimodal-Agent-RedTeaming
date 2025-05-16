from huggingface_hub import login
from datasets import load_dataset

# Your huggingface Token
login("")

# Now load the gated dataset
dataset = load_dataset("osunlp/Online-Mind2Web")

for item in dataset['test']:
    task_inst, website, reference_len, level = item['confirmed_task'], item['website'], item['reference_length'], item['level']
    assert False
