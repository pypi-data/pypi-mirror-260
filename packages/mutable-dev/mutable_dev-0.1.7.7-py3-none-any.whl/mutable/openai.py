from typing import Literal, Optional 
import os 
from uuid import uuid4
import openai
import wrapt 
import stripe 
import time 
from mutable.helpers.outcome_simulation import evaluate_sim
import requests 
import pandas as pd 
from datasets import Dataset 
import threading 

def runReady():
    if not os.environ.get('STRIPE_API_KEY'):
        return('STRIPE_API_KEY not found in environment variables')
        quit() 
    else: 
        stripe.api_key = os.environ.get('STRIPE_API_KEY')

runReady()

def checkOAI():
    if not os.environ.get('OPENAI_API_KEY'):
        return('OPENAI_API_KEY not found in environment variables')
        quit() 
    else:
        pass 

checkOAI()

from ragas.metrics import faithfulness, answer_relevancy, context_precision 
#from ragas.metrics.critique import SUPPORTED_ASPECTS, harmfulness 

execution_id = None 





    
class Preferences():
    def __init__(self):
        self.preferences = None

    def configure(self, val):
        self.preferences = val
        if 'api_key' not in val and os.environ.get('MUTABLE_API_KEY') is None:
            print('No API key provided')
            quit()  

    def get_preferences(self):
        return self.preferences 
    

actual_preferences = Preferences()

class MutablePreferences():
    def __init__(self):
        self.preferences = None

    def configure(self, val):
        actual_preferences.configure(val)

class EvaluatePayment():
    def __init__(self):
        self.paymentThresholdMet = None 

    def set_val(self, val):
        self.paymentThresholdMet = val 

    def shouldPay(self):
        return self.paymentThresholdMet


class PersistentContext():
    def __init__(self):
        self.context = [] 
    

    def store_context(self, additionalContext):
        self.context.append(additionalContext)

    def get_context_contents(self):
        k = "".join(self.context)
        return k 
    def get_context(self):
        return self.context 

class MutableOpenAI():
    def __init__(self, contextHandler, paymentsEvaluator, preferences):
        self.prompt = None 
        self.query = None 
        self.result = None 
        self.oaiKwargs = None 
        self.contextHandler = contextHandler
        self.metrics = []
        self.documents = [] 
        self.scores = {}
        self.scores_with_outcome = {}
        self.paymentThresholdMet = None 
        self.paymentsEvaluator = paymentsEvaluator
        self.preferences = preferences 
        self.api_key = None 
        self.execution_id = None 
        #self.check_for_api_key()


    
        


    def setPreferences(self):
        r = requests.get('https://mutable-api-production.up.railway.app/api/get-preferences', headers={'x-api-key': self.api_key})

        if not r.status_code == 200:
            message = r.json()['message']
            print(message)
            quit()
        else: 
            
            r_preferences = r.json().get('preferences')
            self.metrics = r_preferences['evaluation_metrics'].split(',')
            self.threshold_score = r_preferences['performance_threshold']
            self.scenario = r_preferences['product_description']
            if (self.metrics and self.threshold_score and self.scenario) is not None: 
                pass 
            else: 
                print('Preferences not fully set')
                quit() 
           
   

    def score_with_ragas(self): 
        k = {'faithfulness': faithfulness, 'answer_relevancy': answer_relevancy, 'context_precision': context_precision}
        self.scores = {}
        for m in self.metrics:
            print("Scoring: %s"%(m))
            qa_dict = {"question": self.query, "contexts": self.documents, "answer": self.result}
            k_new = pd.DataFrame([qa_dict])
            qa_row = Dataset.from_pandas(k_new)

            j = k[m].score(
                qa_row
            )
            self.scores[m] = j[0][m]
            print("Scored it: %s is %s"%(m, self.scores[m]))
        return self.scores

    def log_oai_kwargs(self, oaiKwargs):
        self.oaiKwargs = oaiKwargs 
        self.log_qa() 

    def checkMessages(self): 
        passed_oai_kwargs = self.oaiKwargs
        foundMessages = False
        messageKwarg = None 
        for item in passed_oai_kwargs: 
            if isinstance(passed_oai_kwargs[item], list):
                if 'role' in passed_oai_kwargs[item][0]:
                    foundMessages = True 
                    messageKwarg = str(item) 
                    return foundMessages, messageKwarg 
                else: 
                    foundMessages = False 
            else:
                foundMessages = False 

        return foundMessages, messageKwarg 
    def split_context_question(self, text, question_demarcate=None): 
        if question_demarcate is None: 
            return text, None
        else: 
            question_start_index = text.find(question_demarcate)
            question_end_index = question_start_index+(len(question_demarcate)+1) 
            if question_end_index <= len(text):
                manip_question = text[question_end_index:].strip()
            else: 
                print('Couldn\'t find end of question sequence')
                quit()  
            print("Query: %s"%(manip_question))
            manip_context = text[:question_start_index]
            print("Context: %s"%(manip_context))
            return manip_question, manip_context

    
    def log_qa(self):

        systemPrompts = []
        userPrompts = []
        
        messages_contained, messages_name = self.checkMessages()
        if not messages_contained:
            print('No messages passed into chat completion call')
            quit() 

        received_messages = self.oaiKwargs[messages_name]

        for k in received_messages: 
            if k['role'] == 'system':
                print('Adding system prompt: %s'%(k['content']))
                systemPrompts.append(k['content'])
            if k['role'] == 'user':
                print('Adding human prompt: %s'%(k['content']))
                userPrompts.append(k['content'])
      
        # store most recent prompts 
        print('System prompts received: %s'%(systemPrompts))
        print('User prompts received: %s'%(userPrompts))
        
        # split context/prompt and question if not done via kwargs
        if not systemPrompts:
            query, context = self.split_context_question(userPrompts[-1], question_demarcate=actual_preferences.get_preferences().get('question_demarcator'))

            self.query = query 
            self.prompt = context 
            self.contextHandler.store_context(self.prompt) if self.prompt else None 
            print('Context handler contents....')
            print(self.contextHandler.get_context())
            self.contextHandler.store_context(self.query)
            print('Context handler contents....')
            print(self.contextHandler.get_context())
        else: 

            self.prompt = systemPrompts[-1] if systemPrompts else None 
            self.query = userPrompts[-1] if userPrompts else None 

            # add to persistent context handler for context scoring 
            for sysPrompt in systemPrompts:
                self.contextHandler.store_context(sysPrompt)
            for userPrompt in userPrompts:
                self.contextHandler.store_context(userPrompt)

    def log_result(self, result): 
        self.result = result.choices[0].message.content 
        self.contextHandler.store_context(self.result)
        

    def describe_intercept(self):
        print(f'Intercepted function with prompt: {self.prompt}, query: {self.query}, and result: {self.result}')
    
    def meet_threshold(self, scores): 
        thresholds = {} 
        print("Created thresholds dictionary")
        for score_key in scores: 
            thresholds[score_key] = float(self.threshold_score) 
        print("Thresholds added for: (%s)"%(str(thresholds.keys())))
        metThreshold = []
        for score in scores:
            print("Evaluating %s"%(score))
            if scores[score] >= thresholds[score]:
                print("%s threshold met: %s >= %s"%(score, scores[score], thresholds[score])) 
                metThreshold.append(True)
            else:
                print('%s threshold not met: %s < %s'%(score, scores[score], thresholds[score]))
                metThreshold.append(False)
        if False in metThreshold:
            return False 
        else:
            return True
        
    def thematic_evaluation(self):
        if self.prompt:
            task = self.prompt+". " + "You've been asked to do the following: "+self.query
        else: 
            task = "You've been asked to do the following: "+self.query
        thematic_evaluation_result = evaluate_sim(self.scenario, task, self.result)
        if isinstance(thematic_evaluation_result, dict):
            print(thematic_evaluation_result['numerical_feedback'])
            thematic_dict = {'qualitative_feedback': thematic_evaluation_result['qualitative_feedback'], 'numerical_feedback': thematic_evaluation_result['numerical_feedback']}
            self.scores_with_outcome = {}
            self.scores_with_outcome = self.scores
            self.scores_with_outcome['outcome_simulation'] = thematic_dict 
            return thematic_evaluation_result['numerical_feedback'] > float(self.threshold_score)
        else: 
            print('Thematic evaluation output in incorrect format')
            return False 

    def log_execution(self, query, context, result, scores):
        payload = {"query": query, "context": context, "result": result, "scores": scores}
        r = requests.post('https://mutable-api-production.up.railway.app/api/log-execution', headers={'x-api-key': self.api_key}, json=payload)
        execution_id = r.json()['id'] 
        self.execution_id = execution_id  
        if not r.status_code == 200:
            print("Error trying to log execution")
        else:
            pass 
    
    def begin_evaluation(self):
        self.evaluate_response()
        self.paymentsEvaluator.set_val(self.paymentThresholdMet) 


    def evaluate_response(self): 
        self.documents = self.contextHandler.get_context() 
        print(f"Current contents of document handler: {self.documents}")
        scores = self.score_with_ragas() 
        threshold_met = self.meet_threshold(scores) 
        simulated_outcome_threshold_met = self.thematic_evaluation()
        
        self.log_execution(self.query, ",".join(self.documents), self.result, self.scores_with_outcome)


        if threshold_met and simulated_outcome_threshold_met:
            self.paymentThresholdMet = True 
        else:
            self.paymentThresholdMet = False

    def shouldPay(self):
        return self.paymentThresholdMet 
    

    def set_params(self):
        self.preferences = actual_preferences 
        if os.environ.get('MUTABLE_API_KEY'):
            self.api_key = os.environ.get('MUTABLE_API_KEY')
            global_api_key = self.api_key 
            self.setPreferences() 
        else: 
            if self.preferences.get_preferences() is not None and 'api_key' in self.preferences.get_preferences():
                self.api_key = self.preferences.get_preferences()['api_key']
                global_api_key = self.api_key 
                self.setPreferences()
            else:
                print('No API key found')
                quit() 

    

    def chat_completion_wrapper(self, wrapped, instance, args, kwargs):

        self.set_params() 
        self.log_oai_kwargs(kwargs)
        result = wrapped(*args, **kwargs)
        self.log_result(result)



        return result 




persistentContextHandler = PersistentContext() 
paymentsEvaluator = EvaluatePayment()
mutable = MutableOpenAI(persistentContextHandler, paymentsEvaluator, actual_preferences)

wrapt.wrap_function_wrapper(openai, 'chat.completions.create', mutable.chat_completion_wrapper)



def beginEvaluation():
    mutable.begin_evaluation() 



def shouldPay():
    return paymentsEvaluator.shouldPay()

def log_trans(payload):
    r = requests.post('https://mutable-api-production.up.railway.app/api/log-payment', headers={'x-api-key': mutable.api_key}, json=payload)
    if not r.status_code == 200:
        print(r.json())
    else:
        pass 

def getTier(tiers, amt):
    tier_thresholds = [] 
    for i in tiers: 
        if i.get('up_to') is None: 
            tier_thresholds.append(float('inf'))
        else:
            tier_thresholds.append(i.get('up_to'))
    
    k = 0 
    while k < len(tier_thresholds):
        if amt>tier_thresholds[k]:
            k+=1 
        else: 
            return k 
        

def unwrapSubscription(subscription_id): 
    """
    Take subscription ID and return primitives, including:
    Subscription items, unit price (if applicable), usage quantity, 
    """
    try: 
        stripe_subscription = stripe.Subscription.retrieve(id=subscription_id)
        subscription_items = stripe_subscription.get('items') if 'items' in stripe_subscription else None 
        if not subscription_items:
            return ("No items found within subscription. Make sure your subscriptions are configured properly")
        else: 
            subscription_item_data = subscription_items.get('data') if 'data' in subscription_items else None 
            if not subscription_item_data:
                return('No data associated with item. Make sure your subscriptions are configured properly') 
            else: 
                if len(subscription_item_data) > 0:
                    subscription_item_details = subscription_item_data[0]
                    subscription_item_id = subscription_item_details.get('id')
                    plan = subscription_item_details.get('plan')
                    price = subscription_item_details.get('price')
                    corresponding_price = stripe.Price.retrieve(id=price.get('id'), expand=['tiers'])
                    pricing_tiers = corresponding_price.get('tiers')
                    usage_record = stripe.SubscriptionItem.list_usage_record_summaries(subscription_item_id).get('data')
                    usage_amt = 0
                    for usage in usage_record:
                        usage_amt+=usage.get('total_usage')


                    return subscription_item_details, plan, corresponding_price, pricing_tiers, usage_amt 
                    
                else: 
                    return('No data associated with item. Make sure your subscriptions are configured properly') 
    except Exception as e:
        return str(e)

def triggerPayment():
    try: 
        if not 'stripe_subscription_id' in actual_preferences.get_preferences():
            print('No subscription ID passed into the preferences handler. Be sure to pass in a \'stripe_subscription-id\' key-value pair to the MutablePreferences.configure() method')
            quit() 
        else: 
            stripe_subscription_id = actual_preferences.get_preferences()['stripe_subscription_id']
            details, plan, corr_price, tiers, usage_amt = unwrapSubscription(stripe_subscription_id)
            
            timestamp = int(time.time())
            idempotency_key = str(uuid4())
            try: 
                stripe.SubscriptionItem.create_usage_record(
                    details.get('id'),
                    quantity=1,
                    timestamp=timestamp,
                    action='increment',
                    idempotency_key=idempotency_key

                )
                ex_id = mutable.execution_id
                relevant_tier = tiers[getTier(tiers, usage_amt)]
                if relevant_tier.get('unit_amount') > 0:
                    amt = relevant_tier.get('unit_amount')/(10**int(relevant_tier.get('unit_amount_decimal')))
                    payload = {'ex_id': ex_id, 'amount': amt, 'subscription_id': stripe_subscription_id}
                else: 
                    payload = {'ex_id': ex_id, 'amount': "No incremental price", 'subscription_id': stripe_subscription_id}

                log_trans(payload)

                print('Monthly invoice incremented by satisfactory response unit price')

            except Exception as e:
                print('Exception encountered %s'%(e))
    except Exception as e:
        print('Exception encountered %s'%(e))


def evaluate_success_and_payment():
    def run_in_background(): 
        beginEvaluation()
        evaluatePayment = shouldPay()
            # Trigger payment 
        if evaluatePayment:
            triggerPayment() 
        else:
            pass 

    thread = threading.Thread(target=run_in_background)
    thread.start() 