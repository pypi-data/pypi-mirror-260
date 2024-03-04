import time 
from uuid import uuid4 
import stripe 
import requests 

stripe.api_key = 'sk_test_51OHcovDTU9hgRfhMraaWCNcAWRwv0m1qMyb8SQWFryDPUthpdHHeAtC67BbDiIaYQoVNSsaPsrbB7q8qEipURSeu00HJr4fq5U'


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
    
details, plan, price, tiers, amt = unwrapSubscription('sub_1OXdQbDTU9hgRfhMdJZJS6KX')
print(tiers)
relevant_tier = getTier(tiers, amt)
print(tiers[relevant_tier])
    

"""" 
def triggerPayment(mutable, actual_preferences):
    try: 
        if not 'stripe_subscription_id' in actual_preferences.get_preferences():
            print('No subscription ID passed into the preferences handler. Be sure to pass in a \'stripe_subscription-id\' key-value pair to the MutablePreferences.configure() method')
            quit() 
        else: 
            stripe_subscription_id = actual_preferences.get_preferences()['stripe_subscription_id']
            sub = stripe.Subscription.retrieve(id=stripe_subscription_id)
            subscription_items = sub.get('items')
            if not subscription_items: 
                print('No subscription items associated with this subscription. Make sure this is a metered-type subscription')
                quit() 
            if subscription_items.get('data') and len(subscription_items.get('data')) > 0:
                subscription_item_id = subscription_items.get('data')[0]['id']
            else:
                print('Please make sure subscription type is metered')


            usage_quantity=1 
            timestamp = int(time.time())
            idempotency_key = str(uuid4())

            try: 
                stripe.SubscriptionItem.create_usage_record(
                    subscription_item_id,
                    quantity=usage_quantity,
                    timestamp=timestamp,
                    action='set',
                    idempotency_key=idempotency_key

                )
                ex_id = mutable.execution_id
                price = stripe.Price.retrieve(id=subscription_items['data'][0]['price']['id'], expand=['tiers'])
                unit_price = price['tiers'][0]['unit_amount']
                dec = int(price['tiers'][0]['unit_amount_decimal'])
                amt = unit_price/(10**dec)
                payload = {'ex_id': ex_id, 'amount': amt, 'subscription_id': stripe_subscription_id}
                log_trans(payload)

                print('Monthly invoice incremented by satisfactory response unit price')

            except Exception as e:
                print('Exception encountered %s'%(e))
    except Exception as e:
        print('Exception encountered %s'%(e))

"""