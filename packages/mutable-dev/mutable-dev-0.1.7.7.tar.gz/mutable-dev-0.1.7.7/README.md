# Mutable
A Python SDK for adding success-based pricing to LLM-based applications
Don't hesitate to reach out to [chase@mutability.ai](mailto:chase@mutability.ai) with any questions, concerns, or if you need guidance (or if you just want to say hi!). If you're looking to integrate this with a production-grade application and want a more high touch integration, we'd love to meet you. Book some time with us [here](https://calendly.com/chase-baseflow/1-1-with-chase).

[![Website Badge](https://img.shields.io/badge/visit-website-blue)](https://bemutable.io) [![Twitter URL](https://img.shields.io/twitter/url/https/twitter.com/bukotsunikki.svg?style=social&label=Follow%20%40bemutable)](https://twitter.com/bemutable)


Mutable is a Python toolkit with packages designed to make adding success-based pricing to your LLM-based application ridiculously simple and intutuive. Success-based pricing is the inevitable next step in pricing for software that's speculative and produces work (rather than facilitates it). Intercom Fin and Sierra AI are leading the pack. You should join them.

- Determine a consensus definition of success to better understand and serve user needs
- Capture and measure success, provide users with insight into model performance
- Programmatically tether consumption and usage fees to success threshold
- Drive adoption to your application by aligning your incentives with your users'

## Features

- Instrumentation of OpenAI and Langchain to cover most implementations of LLMs
- Integrates directly with Stripe and preexisting subscriptions
- Robust evaluation of RAG functionality and outcome/scenario simulation
- Integrate user scoring and qualitative feedback into success determination
- Dashboard for monitoring and billing visibility


## Quickstart
First, install the Mutable Python SDK via pip
```
pip install mutable-dev
```

Then, set relevant API keys (e.g., Stripe, OpenAI)
```
export OPENAI_API_KEY=YOUR_API_KEY_HERE
export STRIPE_API_KEY=YOUR_API_KEY_HERE
export MUTABLE_API_KEY=YOUR_API_KEY_HERE
```
Generate your Mutable API key from the API console and configure your preferences (e.g., numerical thresholds, evaluative metrics)
### OpenAI example
Make the relevant imports, add runtime preferences (e.g., relevant Stripe subscription ID, phrase used to demarcate question from context in single-prompt applications), and then call `evaluate_success_and_payment()` wherever and whenever applicable.
```python
from mutable.openai import openai, evaluate_success_and_payment, MutablePreferences 
import os 

''' Need your own business logic to extract the Stripe subscription ID corresponding to the user in the session
'''
MutablePreferences().configure({'stripe_subscription_id': 'sub_1OnWlNDTU9hgRfhMx4ozr8wm', 'question_demarcator': 'Question'})


'''
Example GPT-3.5 wrapper application
'''

ended = False 
while not ended:
    newQuery = input("Provide your query or type \"end\" to end the chat: ")
    if newQuery == "end":
        ended = True 
    else:
        prompt = f"Context: Lemonde stands in Palo Alto are few and far between. Question: {newQuery}"
        completion = openai.chat.completions.create(
        model="gpt-3.5-turbo", messages=[
               
                {"role": "user", "content": prompt}
            ]
        )

        print("Response: %s"%(completion.choices[0].message))
        '''
        Execute this function whenever relevant (e.g., after each Q&A volley or generation) to judge the outputs of your model and log a transaction
        '''
        evaluate_success_and_payment() 
        
        

```
### Langchain quickstart
```python
from langchain import hub 
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI 
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma 
from langchain.chains import RetrievalQA
from langchain.prompts import  PromptTemplate
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from mutable.callbacks import MutableHandler
from langfuse.callback import CallbackHandler 




# Example subscription ID, to be retrieved through own business logic
subscription_id = 'sub_1OnWlNDTU9hgRfhMx4ozr8wm'


# Setting up Langfuse for logging and more sophisicated observability
lfHandler = CallbackHandler()
# Initialize Mutable callback handler
mHandler = MutableHandler(langfuseHandler=lfHandler, stripe_subscription_id=subscription_id)



# Example chain
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
def createChain():
    currentDirectory = os.getcwd()
    print("Beginning document loader...")
    loader = DirectoryLoader(f'{currentDirectory}/exampleDocs/')
    docs = loader.load() 
    print("Loading documents...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    print("Chunking...")
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    print("Vector store created...")

    retriever = vectorstore.as_retriever(callbacks=[mutabilityHandler]) 
    print("Retriever created...")
    example_prompt_string = """
    Respond to the question using only the provided context.
    {context}
    {question}"""
    EXAMPLE_PROMPT = PromptTemplate(input_variables=['context', 'question'], template=example_prompt_string)
    llm = ChatOpenAI(model_name='gpt-3.5-turbo-1106', temperature=0)
    chain_type_kwargs = {"prompt": EXAMPLE_PROMPT}
    print("Chain being instantiated...")
    rag_chain = RetrievalQA.from_chain_type(
        retriever=retriever,
        chain_type_kwargs=chain_type_kwargs,
        llm=llm,
        chain_type="stuff",
        verbose=True
    )
    return rag_chain

if __name__ == '__main__':
    ragChain = createChain() 
    result = ragChain("What are the obligations of All-American Homecare to supervisors as a fiscal intermediary? Please list them out and provide exposition for each duty.", callbacks=[lfHandler, mHandler])
    print(result)
    print(mHandler.get_and_score_trace())

    
    #print(mHandler.get_stored_scores())
```
## Roadmap 
- 🚧  More robust event and transaction tracking with performance breakdowns and prompt guidance
- 🚧  Instrumentation for other LLM frameworks (e.g., LiteLLM)
- 🚧  Integration with other payment platforms 
- 🚧  Modularity in evaluation (e.g., substitute with your own evaluation framework)
- 🚧  Pricing page creator
