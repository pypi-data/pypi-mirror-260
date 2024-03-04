from langchain import hub 
from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI 
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.prompts import  PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field 
import os 

if not os.environ.get('OPENAI_API_KEY'): 
    print('Set your OpenAI API key in your environment variables')
    quit() 
else: 
    pass 

class Evaluation(BaseModel):
    qualitative_feedback: str = Field(description='Exhaustive qualitative feedback based on how the identity constructed as a party interacting with the generated contents would behave/react to the content and how well their reaction aligns with what is the inferred purpose of the generation given the task/query')
    numerical_feedback: int = Field(description="1-100 numerical complement to the qualitative feedback on the generated contents given the provided scenario and constraints")


class Behaviors(BaseModel):
    behaviors: dict = Field(description="Behavioral choices and their corresponding definitions that should map perfectly to a realistic set of actions/reactions that our constructed identity could take")


'''
params: 
identity -> construct a contextually relevant identity of someone whose actions/reactions will determine the realized value of the generated text
task -> prompt/query 
result -> generation 
'''

evaluation_parser = JsonOutputParser(pydantic_object=Evaluation)
behavior_parser = JsonOutputParser(pydantic_object=Behaviors)


def evaluate_sim(scenario, task, result):
    model = ChatOpenAI(temperature=0)
    scenario = scenario 

    behavior_prompt_text = """
    In this exercise, you will be provided with a setting and a corresponding task. Your role is to identify the downstream persona who directly interacts with and is impacted by the output generated from these inputs. Consider how this persona would encounter the generated material in a real-world scenario, its relevance to their lifestyle, and how it aligns with their behaviors and actions.

    For example, if the setting is creating a name for a lemonade stand in Palo Alto, CA, that appeals to hikers and climbers, your focus should be on the hikers and climbers themselves. They are the end-users who will engage with and be influenced by the name of the lemonade stand in their real-world activities.

    Your task is to choose this downstream persona and then list 8-9 specific behaviors or actions characteristic of this persona. These actions should be those that directly relate to their potential interaction with the lemonade stand, reflecting how they might value and engage with it.

    Here is the setting:
    {scenario}

    Here is the task:
    {task}

    Format your response according to the following instructions.
    {format_instructions}

"""


    behavior_prompt = PromptTemplate(
        input_variables=['scenario', 'task'],
        template=behavior_prompt_text,
        partial_variables={'format_instructions': behavior_parser.get_format_instructions()}
    )
    print('Generating set of behaviors for simulated persona...')
    behavior_chain = behavior_prompt | model | behavior_parser 
    behavioral_functions = behavior_chain.invoke({'scenario': scenario, 'task': task})
    print(behavioral_functions)

    prompt = PromptTemplate(input_variables=['scenario', 'task', 'result', 'behaviors'], template = """
    In this evaluation, you will analyze the value of generated content by simulating how a constructed identity, based on a given scenario and task, interacts with this content. You will be provided with a JSON dictionary of that represent various ambient behaviors of the persona. These behaviors might or might not engage directly with the generated content.

    Your role is to assume the identity crafted from the scenario and use these functions to simulate realistic interactions with the generated content. Play out this simulated scenario step-by-step.
                            
    For instance, if the scenario involves an AI copilot creating content to enhance SEO, embody the role of an internet user who browses content casually. The functions you will receive might include actions like searching, scanning search results, and clicking on links. 
    You should then use the identity you've embodied to realistically walk through their search journey, from the queries they write, the links that are returned, the ones they ultimately click, how long they stay on each, etc. Please talk yourself through every discrete step 
    of the simulation. Make a record of which behaviors are ultimately taken, the context of their enaction, and the intensity of their realization. Let this be a record of your behavioral reaction to everything, including the content.
    Then, come out of the identity, and objectively evaluate the generated content against the task that prompted its generation and how a simulated persona, namely the one you were, would receive it based on that same behavioral record you generated.


    Your evaluation should be carefully informed. Consider the following:
    1. Which behaviors did the identity you simulated choose to engage with, and why?
    2. What was the intensity and frequency of these interactions?
    3. Based on this simulated engagement, how effective is the generated content in fulfilling the task's intended outcome?
                            
    A very verbose example would be:
    You receive the following scenario: AI copilot that's designed to generate product metadata for Etsy listings and drive conversion to the product.
    Task: Generate product title, description, and tasks for a artisanal red mug with North Carolinian cultural references 
    You should assume the identity of a North Carolinian with artsy affectations who would conceivably shop on Etsy. Truly think of their personal qualities and embody them.
    You are given behaviors, like browseEtsy, clickOnItem, engageWithItem, buyItem, removeItemFromCart, shareItem, that represent the types of actions this identity would ambiently perform. 
    Let's say the generated content is okay, but not stimulating. You may trigger the browseEtsy behavior with search queries that really align with the generated title because when you search for red mugs with North Carolinian cultural references,
    you're not verbose with your search but the title generated is verbose and highly descriptive. As such, you never trigger the clickOnItem behavior because you never encountered it. Alternatively, it generated a very attractive product title
    that chaught your eye and got to the engageWithItem behavior but you never triggered the buyItem behavior because you weren't persuaded by the description as it didn't resonate with what would resonate with the identity you've assumed. 
    After this, you come out of the identity and evaluate it based on these simulated findings.

    Your assessment should provide insights into the content's likely real-world impact and effectiveness. Strictly ahdere to the following format for your evaluation:
    {format_instructions}

    Scenario for Identity Construction:
    {scenario}

    Task Informing Content Generation:
    {task}

    Generated Content for Evaluation:
    {result}

    JSON Dictionary of Possible Behaviors:
    {behaviors}
""", partial_variables={'format_instructions': evaluation_parser.get_format_instructions()})
        
    
    print('Doing evaluation...')
    chain = prompt | model | evaluation_parser 
    return chain.invoke({'scenario': scenario, 'task': task, 'result': result, 'behaviors': behavioral_functions})


