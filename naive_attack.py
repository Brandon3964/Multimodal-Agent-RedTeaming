import asyncio
import os
from seeact_package.seeact.agent import SeeActAgent
import sys
import json
import openai

path = os.path.expanduser('~/SeeAct/mmagent_attack')
sys.path.append(path)
from mmagent_attack import injection_utils
from dotenv import load_dotenv

# Setup your API Key here, or pass through environment
load_dotenv()
os.environ["OPENAI_API_KEY"] = ""

with open("./mmagent_attack/attack_config/image_text/4.json", "r") as f:
    attack_config = json.load(f)
injections = injection_utils.get_injections(attack_config)


async def run_agent():
    agent = SeeActAgent(
        default_website=attack_config['task_info']["website_url"], 
        model="gpt-4.1-mini", 
        default_task=attack_config['task_info']["goal"],
        injections=injections)
    await agent.start()
    while not agent.complete_flag:
        prediction_dict = await agent.predict()
        await agent.execute(prediction_dict)
    await agent.stop()

if __name__ == "__main__":
    asyncio.run(run_agent())