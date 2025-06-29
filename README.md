# 6/8/2025 updates
Run ```scripts/run_attack.sh``` to run an automatic attack that extract injection point, generate attack image, then perform attack.



# SETUP

1. Follow the SeeAct setup to install dependency
2. Install SeeAct from source in ```seeact_package``` by doing ```pip3 install -e .```
3. Install and setup a VNC server to visualize the agent.
4. Put your OpenAI api in ```naive_attack.py```. Then run the script for a demo. To try other attacks and examples, replace the config with other configs in ```mmagent_attack/attack_config```
5. To customize attack, modify the attack functions in ```injection_utils.py```




[//]: # (# SeeAct <br> GPT-4V&#40;ision&#41; is a Generalist Web Agent, if Grounded)

<h1 align="center">SeeAct <br> GPT-4V(ision) is a Generalist Web Agent, if Grounded</h1>

<p align="center">
<a href="https://osu-nlp-group.github.io/Mind2Web/"><img src="https://img.shields.io/badge/Mind2Web-Homeage-red.svg" alt="Mind2Web Benchmark"></a>
<a href="https://www.licenses.ai/ai-licenses"><img src="https://img.shields.io/badge/OPEN RAIL-License-green.svg" alt="Open RAIL License"></a>
<a href="https://huggingface.co/datasets/osunlp/Mind2Web"><img src="https://img.shields.io/badge/Mind2Web-Dataset-yellow.svg" alt="Mind2Web Benchmark"></a>
<a href="https://huggingface.co/datasets/osunlp/Multimodal-Mind2Web"><img src="https://img.shields.io/badge/Multimodal Mind2Web-Dataset-blue.svg" alt="Mind2Web Benchmark"></a>
<a href="https://pypi.org/project/seeact/"><img src="https://img.shields.io/badge/seeact-PyPI-red.svg" alt="Python 3.10"></a>
</p>

<p align="center">
<a href="https://www.python.org/downloads/release/python-3109/"><img src="https://img.shields.io/badge/python-3.10-blue.svg" alt="Python 3.10"></a>
<a href="https://playwright.dev/python/docs/intro"><img src="https://img.shields.io/badge/Playwright-1.44-green.svg" alt="Playwright"></a>
<a href="https://github.com/OSU-NLP-Group/SeeAct"><img src="https://img.shields.io/github/stars/OSU-NLP-Group/SeeAct?style=social" alt="GitHub Stars"></a>
<a href="https://github.com/OSU-NLP-Group/SeeAct/issues"><img src="https://img.shields.io/github/issues-raw/OSU-NLP-Group/SeeAct" alt="Open Issues"></a>
<a href="https://twitter.com/osunlp"><img src="https://img.shields.io/twitter/follow/OSU_NLP_Group" alt="Twitter Follow"></a>
</p>

SeeAct is a system for <a href="https://osu-nlp-group.github.io/Mind2Web/">generalist web agents</a> that autonomously carry out tasks on any given website, 
with a focus on large multimodal models (LMMs) such as GPT-4V(ision). 
It consists of two main components: 
(1) A robust codebase that supports running web agents on live websites, and
(2) an innovative framework that utilizes LMMs as generalist web agents.

![Demo Video GIF](https://raw.githubusercontent.com/OSU-NLP-Group/SeeAct/gh-pages/static/videos/readme_demo.gif)

<p align="center">
<a href="https://osu-nlp-group.github.io/SeeAct/">Website</a> •
<a href="https://arxiv.org/abs/2401.01614">Paper</a> •
<a href="https://huggingface.co/datasets/osunlp/Multimodal-Mind2Web">Dataset</a> •
<a href="https://twitter.com/ysu_nlp/status/1742398541660639637">Twitter</a>
</p>

<h3>Updates</h3>

- 2024/11/10: We have open-sourced SeeAct Chrome Extension source code! Try and have fun at [SeeActChromeExtension](https://github.com/OSU-NLP-Group/SeeActChromeExtension)!

- 2024/9/30: [WebOlympus: An Open Platform for Web Agents on Live Websites](https://aclanthology.org/2024.emnlp-demo.20/) has been accepted to EMNLP'24 Demo Track! 

- 2024/8/17: Crawler mode added!

- 2024/7/9: Support SoM (Set-of-Mark) grounding strategy!

- 2024/5/18: Support for Gemini and LLaVA!

- 2024/5/1: SeeAct has been accepted to ICML'24!

- 2024/4/28: Released [SeeAct Python Package](https://pypi.org/project/seeact/#history), with many updates and many features on the way. Have a try with `pip install seeact`

- 2024/3/18: [Multimodal-Mind2Web](https://huggingface.co/datasets/osunlp/Multimodal-Mind2Web) dataset released. We have paired each HTML document with the corresponding webpage screenshot image and saved the trouble of downloading [Mind2Web Raw Dump](https://github.com/OSU-NLP-Group/Mind2Web?tab=readme-ov-file#raw-dump-with-full-traces-and-snapshots).

# SeeAct Tool

The SeeAct tool enables running web agents on live websites through [PlayWright](https://playwright.dev/), 
serving as an interface between an agent and a web browser. 
It efficiently tunnels inputs from the browser to the agent, and translates predicted actions of the agent into browser events for execution. 
This tool can be used for running web agent demos and evaluating their performance on live websites.


## Setup

1. Create a conda environment and install dependency:
```bash
conda create -n seeact python=3.11
conda activate seeact
pip install seeact
```

2. Set up PlayWright and install the browser kernels.
```bash
playwright install
```

## Usage


```python
import asyncio
import os
from seeact.agent import SeeActAgent

# Setup your API Key here, or pass through environment
os.environ["OPENAI_API_KEY"] = "Your API KEY Here"

async def run_agent():
    agent = SeeActAgent(model="gpt-4-turbo")
    await agent.start()
    while not agent.complete_flag:
        prediction_dict = await agent.predict()
        await agent.execute(prediction_dict)
    await agent.stop()

if __name__ == "__main__":
    asyncio.run(run_agent())
```
### SeeActAgent Main Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| model | Prefered LLM model to run the task | str | gpt-4o | no |
| default_task | Default task to run  | str | Find the pdf of the paper "GPT-4V(ision) is a Generalist Web Agent, if Grounded" | no |
| default_website | Default starting website  | str | https://www.google.com/ | no |
| grounding_strategy | Grounding strategy <ul><li>`text_choice`: use text choices</li><li>`text_choice_som`: use text choices with set of marks</li></ul> | str | text_choice_som | no |
| config_path | Configuration file path | str | None | no |
| save_file_dir | Folder to save output files  | str | seeact_agent_files | no |
| temperature | Termperature passed to LLM | num | 0.9 | no |
| crawler_mode | Flag to enable crawler mode | bool | False | no |
| crawler_max_steps | Max step to allow crawler to travel | int | 10 | no |


## Supported Models
SeeAct starts with using OpenAI GPT4-V, and now it supports some other models.
Below is the list of currently supported models, to use any one of the model below, simpliy use `SeeActAgent(model="gpt-4-turbo")`, and specify the API key if needed.
| Provider | Model | Compatibility | API KEY | Note
|----------|-------|---------------|---------|:-----------:|
| OpenAI | gpt-4-vision-preview | High | OPENAI_API_KEY in env |  |
| OpenAI | gpt-4-turbo | High | OPENAI_API_KEY in env |  |
| OpenAI | gpt-4o | High | OPENAI_API_KEY in env |  |
| Google | gemini-1.5-pro-latest | High | GEMINI_API_KEY in env | Rate limitting at 2 RPM by Google, need to add wait time in the code to work |
| Ollama | llava | Low | N/A | Install Ollama, start Ollama, pull llava |

## API Keys
If you plan to use OpenAI family models, pass in the API Key in python or by environment variable
```python
os.environ["OPENAI_API_KEY"] = "Your API KEY Here"
```
Your OpenAI API key is available at [OpenAI account page](https://platform.openai.com/account/api-keys). 

To use Gemini, pass in the API Key in python or by environment variable
```python
os.environ["GEMINI_API_KEY"] = "Your API KEY Here"
```
Your Google API key is available at [Google AI Studio](https://aistudio.google.com/app/apikey).

## Configuration File
An alternative to provide SeeActAgent input parameters is to use a config file, once the config file is provided, it will override all other input paramters.
```python
agent = SeeActAgent(config_path="demo_mode.toml")
```
Sample configuration files are available at `src/config/`.

### Crawler Mode
In the new introduced crawler mode, SeeAct could randomly click any links on the given starting web page, and travel steps defined by `crawler_max_steps`.

### Demo Mode

In the demo mode, SeeAct takes `task` and `website` from user terminal input. Run SeeAct in demo mode with the following command:

```bash
cd src
python seeact.py
```
Demo mode will use the default configuration file at `src/config/demo_mode.toml`.

#### Configuration
SeeAct is configurable through TOML files in `src/config/`. 
These files enable you to customize various aspects of the system's behavior 
via the following parameters:
- `is_demo`: Set `true` to allow task and website from user terminal input, set `false` to run tasks and websites from a JSON file (useful for batch evaluation).
- `default_task` and `default_website`: Default task and website used in the demo mode.
- `max_op`: Maximum number of actions the agent can take for a task.
- `save_file_dir`: Directory path to save output results, including terminal logs and screenshot images.

#### Terminal User Input
After starting SeeAct, you'll be required to enter a `task description` 
or you can press `Enter` to use the default task of finding our paper on arXiv.

Next, you need to input the `website URL` (please ensure it includes all necessary prefixes (https, www))
or you can press `Enter` to use the default Google homepage (https://www.google.com/). 

### Auto Mode

You can also automatically run SeeAct on a list of tasks and websites in a JSON file. 
Run SeeAct with the following command:

```bash
cd src
python seeact.py -c config/auto_mode.toml
```
In the configuration file, `task_file_path` defines the path of the JSON file.
It is default to `../data/online_tasks/sample_tasks.json`, which contains a variety of task examples.

### Customized Usage
For custom scenarios, modify the configuration files to adapt the tool
to your specific requirements. 
This includes setting up custom tasks, adjusting experiment parameters, 
and configuring Playwright options for more precise control over the web browsing experience.


## Safety and Monitoring

The current version is research/experimental in nature and by no means perfect. Please always be very cautious of safety risks and closely monitor the agent. 
In the default setting (`monitor = true`), the agent will prompt for confirmation before executing every operation.
This setting pauses the agent before each operation, allowing for close examination, action rejection, and other human intervention like manually doing some operation when needed.

**You should always monitor the agent's predictions before execution to prevent harmful outcomes. Please reject any action that may cause any potential harm.**

You can monitor and intervene actions through terminal input before each execution:
- `Y` or `Enter`: Accept this action.
- `n`: Reject this action and record it in the action history.
- `i`: Reject this action and pause for human intervention. 
  - During the pause, you can do anything, such as opening or closing tabs, opening another link, and so on, except for directly closing the browser. If the current active tab is closed, the active tab will default to the last tab in the browser. If all tabs are closed, the browser will reopen a Google page.
  - You can leave a message after manual operations, which will be injected into the prompt of the agent, for better human-agent cooperation.
- `e`: Terminate the session and save results.

We do not support direct login actions to safeguard your personal information 
and prevent exposure to potential safety and legal risks. 
**To prevent unintended consequential errors, we advise against using SeeAct for tasks that require account login.**


# Multimodal-Mind2Web Dataset
[Multimodal-Mind2Web](https://huggingface.co/datasets/osunlp/Multimodal-Mind2Web) is the multimodal version of Mind2Web dataset hosted on Huggingface under OpenRAIL License. 
In this dataset, we align each HTML document in the dataset with its corresponding webpage screenshot image from the [Mind2Web Raw Dump](https://github.com/OSU-NLP-Group/Mind2Web?tab=readme-ov-file#raw-dump-with-full-traces-and-snapshots).
This multimodal version addresses the inconvenience of loading images from the ~300GB Mind2Web Raw Dump. 

### Data Splits
- train: 7775 actions from 1009 tasks.
- test_task: 1339 actions from 177 tasks. Tasks from the same website are seen during training.
- test_website: 1019 actions from 142 tasks. Websites are not seen during training.
- test_domain: 4060 actions from 694 tasks. Entire domains are not seen during training.

The **_train_** set may include some screenshot images not properly rendered caused by rendering issues during Mind2Web annotation. The three **_test splits (test_task, test_website, test_domain)_** have undergone human verification to confirm element visibility and correct rendering for action prediction.


### Data Fields
Each line in the dataset is an action consisting of screenshot image, HTML text and other fields required for action prediction, for the convenience of inference.
- "annotation_id" (str): unique id for each task
- "website" (str): website name
- "domain" (str): website domain
- "subdomain" (str): website subdomain
- "confirmed_task" (str): task description
- **"screenshot" (str): path to the webpage screenshot image corresponding to the HTML.**
- "action_uid" (str): unique id for each action (step)
- "raw_html" (str): raw html of the page before the action is performed
- "cleaned_html" (str): cleaned html of the page before the action is performed
- "operation" (dict): operation to perform
  - "op" (str): operation type, one of CLICK, TYPE, SELECT
  - "original_op" (str): original operation type, contain additional HOVER and ENTER that are mapped to CLICK, not used
  - "value" (str): optional value for the operation, e.g., text to type, option to select
- "pos_candidates" (list[dict]): ground truth elements. Here we only include positive elements that exist in "cleaned_html" after our preprocessing, so "pos_candidates" might be empty. The original labeled element can always be found in the "raw_html".
  - "tag" (str): tag of the element
  - "is_original_target" (bool): whether the element is the original target labeled by the annotator
  - "is_top_level_target" (bool): whether the element is a top level target find by our algorithm. please see the paper for more details.
  - "backend_node_id" (str): unique id for the element
  - "attributes" (str): serialized attributes of the element, use `json.loads` to convert back to dict
- "neg_candidates" (list[dict]): other candidate elements in the page after preprocessing, has similar structure as "pos_candidates"
- "action_reprs" (list[str]): human readable string representation of the action sequence
- "target_action_index" (str): the index of the target action in the action sequence
- "target_action_reprs" (str): human readable string representation of the target action

# Experiments

### Screenshot Generation
You can also generate screenshot image and query text data from the Mind2Web raw dump. 
Run the following commands to generate screenshot images and overlay image annotation for each grounding method:

```
cd src/offline_experiments/screenshot_generation

# Textual Choices
python textual_choices.py

# Element Attributes
python element_attributes.py

# Image Annotation
python image_annotation.py
```
Please download the Mind2Web raw dump from [this link](https://github.com/OSU-NLP-Group/Mind2Web?tab=readme-ov-file#raw-dump-with-full-traces-and-snapshots) and the query source data from [here](https://buckeyemailosu-my.sharepoint.com/:f:/g/personal/zheng_2372_buckeyemail_osu_edu/Ei95kzWnWlVAn4DR5I3zDDEBUZtC-9vIf0VBuFMOzZNn2w?e=OcH9Om). After downloading, please place both files in the `../data/` directory.


## Online Evaluation of Mind2Web Tasks
To reproduce the online evaluation experiments in the paper, run the following command to run SeeAct in auto mode:
```
python src/seeact.py -c config/online_exp.toml
```
Note: Some tasks may require manual updates to the task descriptions due to time sensitivity.

We followed the 2-stage strategy of [MindAct](https://github.com/OSU-NLP-Group/Mind2Web) for a fair comparison. You can find the trained ranker model [DeBERTa-v3-base](https://huggingface.co/osunlp/MindAct_CandidateGeneration_deberta-v3-base) in the Huggingface Model Hub.


## Licensing Information
The code under this repo is licensed under an [OPEN RAIL-S License](https://www.licenses.ai/ai-pubs-open-rails-vz1).

The data under this repo is licensed under an [OPEN RAIL-D License](https://huggingface.co/blog/open_rail).

The model weight and parameters under this repo are licensed under an [OPEN RAIL-M License](https://www.licenses.ai/ai-pubs-open-railm-vz1).

## Disclaimer

The code was released solely for research purposes, with the goal of making the web more accessible via language technologies. 
The authors are strongly against any potentially harmful use of the data or technology by any party. 

## Acknowledgment
We extend our heartfelt thanks to Xiang Deng for his original contributions to the SeeAct system. 
Additionally, we are grateful to our colleagues from the OSU NLP group for 
testing the SeeAct system and offering valuable feedback.


## Contact

Questions or issues? File an issue or contact 
[Boyuan Zheng](mailto:zheng.2372@osu.edu),
[Boyu Gou](mailto:gou.43@osu.edu),
[Huan Sun](mailto:sun.397@osu.edu),
[Yu Su](mailto:su.809@osu.edu),
The Ohio State University

## Citation Information

If you find this work useful, please consider starring our repos and citing our papers: 

<a href="https://github.com/OSU-NLP-Group/SeeAct"><img src="https://img.shields.io/github/stars/OSU-NLP-Group/SeeAct?style=social&label=SeeAct" alt="GitHub Stars"></a>
<a href="https://github.com/OSU-NLP-Group/Mind2Web"><img src="https://img.shields.io/github/stars/OSU-NLP-Group/Mind2Web?style=social&label=Mind2Web" alt="GitHub Stars"></a>

```
@inproceedings{zheng-etal-2024-webolympus,
    title = "{W}eb{O}lympus: An Open Platform for Web Agents on Live Websites",
    author = "Zheng, Boyuan  and Gou, Boyu  and Salisbury, Scott  and Du, Zheng  and Sun, Huan  and Su, Yu",
    editor = "Hernandez Farias, Delia Irazu  and Hope, Tom  and Li, Manling",
    booktitle = "Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing: System Demonstrations",
    month = nov,
    year = "2024",
    address = "Miami, Florida, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.emnlp-demo.20",
    pages = "187--197",
}

@inproceedings{zheng2024seeact,
  title={GPT-4V(ision) is a Generalist Web Agent, if Grounded},
  author={Boyuan Zheng and Boyu Gou and Jihyung Kil and Huan Sun and Yu Su},
  booktitle={Forty-first International Conference on Machine Learning},
  year={2024},
  url={https://openreview.net/forum?id=piecKJ2DlB},
}

@inproceedings{deng2023mindweb,
  title={Mind2Web: Towards a Generalist Agent for the Web},
  author={Xiang Deng and Yu Gu and Boyuan Zheng and Shijie Chen and Samuel Stevens and Boshi Wang and Huan Sun and Yu Su},
  booktitle={Thirty-seventh Conference on Neural Information Processing Systems},
  year={2023},
  url={https://openreview.net/forum?id=kiYqbO3wqw}
}
```
