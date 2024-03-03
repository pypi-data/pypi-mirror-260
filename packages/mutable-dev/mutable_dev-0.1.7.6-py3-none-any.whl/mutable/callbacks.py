import logging
import os 
import time 
import re 
from typing import Any, Dict, List, Optional, Sequence, Union
from uuid import UUID, uuid4 
from langchain.callbacks.base import BaseCallbackHandler 
from langchain_core.documents.base import Document 
from langfuse import Langfuse 
import asyncio
import stripe 
import requests 
import pandas as pd 
from datasets import Dataset 

from ragas.metrics import faithfulness, answer_relevancy, context_precision 
from ragas.metrics.critique import SUPPORTED_ASPECTS, harmfulness 



execution_id = None 
langfuse = Langfuse()

class MutableHandler(BaseCallbackHandler):
    def __init__(self, *args, langfuseHandler, stripe_subscription_id, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance_id = uuid4()
        self.langfuseHandler = langfuseHandler
        self.langfuse_trace_id = None
        self.langfuse_trace = None 
        self.answer = None 
        self.question = None
        self.documents = []
        self.scores = {}
        self.api_key = None 
        self.execution_id = None 
        ''' 
        self.preferences = preferences
        self.metrics = preferences['metrics']
        '''
        self.stripe_subscription_id = stripe_subscription_id
        self.userInput = None 
        self.user_score = None 
        self.thumbs_up = None 
        self.paymentThresholdMet = None

        self.runReady() 
        self.checkOAI()
        self.getAPIKey() 

    def runReady(self):
        if not os.environ.get('STRIPE_API_KEY'):
            return('STRIPE_API_KEY not found in environment variables')
            quit() 
        else: 

            stripe.api_key = os.environ.get('STRIPE_API_KEY')

    def checkOAI(self):
        if not os.environ.get('OPENAI_API_KEY'):
            return('OPENAI_API_KEY not found in environment variables')
            quit() 
        else:
  
            pass 
    def getAPIKey(self): 
        if self.api_key is not None: 
            pass 
        else:
            if os.environ.get('MUTABLE_API_KEY'):
                self.api_key = os.environ.get('MUTABLE_API_KEY')
                self.setPreferences() 
            else:
                print('Please set MUTABLE_API_KEY in your environment variables')
                quit() 

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
        for m in self.metrics:
            print("Scoring: %s"%(m))
            qa_dict = {"question": self.question, "contexts": self.documents, "answer": self.answer} 
            qa_new = pd.DataFrame([qa_dict])
            qa_eval = Dataset.from_pandas(qa_new)
            j = k[m].score(
               qa_eval
            )
            self.scores[m] = j[0][m]
            print("Scored it: %s is %s"%(m, self.scores[m]))
        return self.scores
    def on_retriever_end(self, documents, **kwargs): 
        for doc in documents:
            self.documents.append(doc.page_content)
        

    def on_chain_end(self, outputs:Dict[str,Any], *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs:Any) -> Any: 
        try: 
            self.langfuse_trace_id = self.langfuseHandler.trace.id 
            #self.get_and_score_trace()
            '''
            
            trace_id = self.langfuse_trace_id 
            self.langfuse_trace = langfuse.get_trace(id=trace_id)
            trace = self.langfuse_trace 
            self.answer = self.langfuse_trace.output
            self.question = self.langfuse_trace.input
            scores = self.score_with_ragas()
            self.scores = scores 
            self.logScore(trace, scores)
            '''
            
        except Exception as e:
            print(f'Exception occured: {e}')

    def get_and_score_trace(self, userInput = {}):
        trace_id = self.langfuse_trace_id 
        print("Got trace ID")
        self.langfuse_trace = langfuse.get_trace(id=trace_id)
        print("Got trace")
        input_keys = self.langfuse_trace.input.keys() 
        query_key = list(input_keys)[0]
        self.question = self.langfuse_trace.input[query_key]
        print("Got query")
        found_output = False 
        for obs in self.langfuse_trace.observations: 
            if obs.output is not None and not (isinstance(obs.output, list)):
                found_output = True 
                if isinstance(obs.output, dict):
                    self.answer = obs.output[list(obs.output.keys())[0]]
                else:
                    self.answer = obs.output 
        print("Got answer")   
        if not userInput:
            self.scoring_flow()
            return self.evaluate_response()
        if userInput:
            self.scoring_flow()
            print ('Got user input%s'%(userInput))
            self.userInput = userInput 
            user_score = userInput['user_score'] if userInput['user_score'] else None 
            thumbs_up = userInput['thumbs_up'] if userInput['thumbs_up'] is not None else None 
            self.user_score = user_score 
            self.thumbs_up = thumbs_up 
            print('User inputs added as model attributes: %s, %s'%(self.user_score, self.thumbs_up))
            return self.evaluate_response()

    def scoring_flow(self):
        scores = self.score_with_ragas()
        print("Scored!")
        self.logScore()
        
    def log_execution(self):
        payload = {"query": self.question, "context": ",".join(self.documents), "result": self.answer, "scores": self.scores}
        r = requests.post('https://mutable-api-production.up.railway.app/api/log-execution', headers={'x-api-key': self.api_key}, json=payload)
        execution_id = r.json()['id'] 
        self.execution_id = execution_id  
        if not r.status_code == 200:
            print("Error trying to log execution")
        else:
            pass 

    
    def log_trans(self, payload):
        r = requests.post('https://mutable-api-production.up.railway.app/api/log-payment', headers={'x-api-key': self.api_key}, json=payload)
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
    def unwrapSubscription(self): 
        """
        Take subscription ID and return primitives, including:
        Subscription items, unit price (if applicable), usage quantity, 
        """
        try: 
            stripe_subscription = stripe.Subscription.retrieve(id=self.stripe_subscription_id)
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
        
    
    def logScore(self):
        for k in self.scores: 
            print("Logging score: (%s, %s)"%(k, self.scores[k]))
            langfuse.score(trace_id=self.langfuse_trace_id, name=k, value=self.scores[k])
            print("Logged %s"%(k))
    def return_documents(self):
        return self.documents 

    def return_trace_id(self):
        return self.langfuse_trace_id
    
    def get_trace_score(self):
        trace_id = self.langfuse_trace_id 
        langfuseTrace = langfuse.get_trace(id=trace_id)
        scores = langfuseTrace.scores 
        return scores 
    
    def get_stored_scores(self):
        return self.scores
    def get_qa(self):
        return (self.question, self.answer)
    

    def meet_threshold(self, scores): 
        thresholds = {} 
        print("Created thresholds dictionary")
        for score_key in scores: 
            thresholds[score_key] = self.threshold_score
        print("Thresholds added for: (%s)"%(str(thresholds.keys())))
        metThreshold = []
        for score in scores:
            print("Evaluating %s"%(score))
            if scores[score] >= float(thresholds[score]):
                print("%s threshold met: %s >= %s"%(score, scores[score], thresholds[score])) 
                metThreshold.append(True)
            else:
                print('%s threshold not met: %s < %s'%(score, scores[score], thresholds[score]))
                metThreshold.append(False)
        if False in metThreshold:
            return False 
        else:
            return True
        


    def scoresIn(self):
        trace = langfuse.get_trace(id=self.langfuse_trace_id)
        print('Scores: %s'%(trace.scores))
        if not trace.scores:
            self.scoresIn() 
        else:
            if not len(trace.scores) == len(self.metrics):
                self.scoresIn()
            else:
                return trace.scores 

    def evaluation_flow(self):
        print("Evaluating with trace ID: %s..."%(self.langfuse_trace_id))
        trace = langfuse.get_trace(id=self.langfuse_trace_id)
        '''
        score_dict = {}
        print("Score dictionary instantiated")
        
        print('Now, we run a recursive function that continiously checks for scores')
        scores_rec = self.scoresIn()
        '''
        scores_rec = self.scores
        print('Scores received%s'%(scores_rec))
        self.log_execution()
        '''
        for score in scores_rec: 
            print("Adding %s to the dictionary"%(score.name))
            score_dict[score.name] = score.value 
            print("Added")
        '''
        print("Checking threshold met")
        threshold_met = self.meet_threshold(scores_rec)
         
        
        return threshold_met 
        
    def evaluate_response(self):
        if not self.userInput: 
            threshold_met = self.evaluation_flow()
            if threshold_met: 
                self.paymentThresholdMet = True 
                print("Performance threshold met. Triggering payment!")
                self.mainPayment()
            else:
                self.paymentThresholdMet = False 
                print('Performance threshold not met. No payment triggered.')
        else:
            print('Executing chain with user input')
            threshold_met = self.evaluation_flow()
            qualThreshold = False 
            if self.user_score: 
                print('There\'s a user score')
                user_score = self.user_score 
                print('%s vs. %s'%(user_score, self.threshold_score))
                qualThreshold = True if user_score >= self.threshold_score else False 
                print(qualThreshold)
            if self.thumbs_up is not None: 
                print('There\'s also a thumbs up response')
                thumbs_up = self.thumbs_up 
                qualThreshold = True if thumbs_up else False 
                print(qualThreshold)
            if qualThreshold and threshold_met:
                self.paymentThresholdMet = True 
                print("Performance threshold met. Triggering payment!") 
                self.mainPayment() 
            else:
                self.paymentThresholdMet = False 
                print('Performance threshold not met. No payment triggered.')


    def shouldPay(self):
        return self.paymentThresholdMet
             





    def mainPayment(self):
        try: 
            if not self.stripe_subscription_id:
                print('No subscription ID passed into the preferences handler. Be sure to pass in a \'stripe_subscription-id\' key-value pair to the MutablePreferences.configure() method')
                quit() 
            else: 
                stripe_subscription_id = self.stripe_subscription_id
                details, plan, corr_price, tiers, usage_amt = self.unwrapSubscription(stripe_subscription_id)
                
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
                    ex_id = self.execution_id 
                    relevant_tier = tiers[self.getTier(tiers, usage_amt)]
                    if relevant_tier.get('unit_amount') > 0:
                        amt = relevant_tier.get('unit_amount')/(10**int(relevant_tier.get('unit_amount_decimal')))
                        payload = {'ex_id': ex_id, 'amount': amt, 'subscription_id': stripe_subscription_id}
                    else: 
                        payload = {'ex_id': ex_id, 'amount': "No incremental price", 'subscription_id': stripe_subscription_id}

                    self.log_trans(payload)

                    print('Monthly invoice incremented by satisfactory response unit price')

                except Exception as e:
                    print('Exception encountered %s'%(e))
        except Exception as e:
            print('Exception encountered %s'%(e))




        
