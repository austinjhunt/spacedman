""" Utility functions for dealing with AWS usage plans and API Keys """
import boto3,random,string 
from django.conf import settings 
from django.contrib.auth.models import User
from httpsrv.models import Profile

def generate_random_string(strlen): 
    """ Method to generate a random string of characters of a specified length
    args:
    strlen (int) number of characters in random string 
    """
    nums = [random.choice(string.digits) for i in range(30)] 
    lower = [random.choice(string.ascii_lowercase) for i in range(30)] 
    upper = [random.choice(string.ascii_uppercase) for i in range(30)] 
    combo = nums + lower + upper 
    return ''.join(random.choice(combo) for i in range(strlen))
    
def delete_api_keys_for_user(username=None):
    """ function to remove all API keys for a user given their username
    Args:
    - username (string) username of user whose API keys are to be deleted
    """
    delete_response = []
    try: 
        u = User.objects.get(username=username)
        client = boto3.client(
            'apigateway',
            region_name='us-east-1',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        ) 
        keys = client.get_api_keys()['items']
        for k in keys: 
            # all API key names are formatted as <username>_<operation>
            if k['name'].startswith(f"spaced_{username}_"):
                # delete this api key using its ID
                response = client.delete_api_key(
                    apiKey=k['id']
                ) 
                delete_response.append(response)
    except Exception as e:
        print(e)
    return delete_response 
    

def create_and_add_api_key_to_usage_plan(user=None,key_value=None,
        operation=None):
        """ Use boto3.create_usage_plan_key to add an existing API key to 
        a usage plan since there is no way to add a key to a usage plan 
        when the key is being created 
        Args:
        - user (User object) user to whom key belongs 
        - key_value (string) value of key, should correspond to operation  
        by creating new API key or by running get_api_keys()
        - operation (string) options: [read, cud] where cud entails create,update,delete
        """ 
        response = None 
        if user and key_value and operation:  
            # Create these API keys on AWS
            # create client
            client = boto3.client(
                'apigateway',
                region_name='us-east-1',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                )

            # Save api key identifiers as username_<operation> e.g. huntaj_read
            response = client.create_api_key(
                name=f'spaced_{user.username}_{operation}'.lower(),
                description=f'SpacEd {operation} API key for {user.username}',
                enabled=True, # whether API key can be used by callers
                value=key_value,  
            )
            # Get the ID of that API key, need it to add key to usage plan 
            key_id = response['id']
            # Get the id of the usage plan for this project 
            try: 
                usage_plans = client.get_usage_plans()['items']
                for up in usage_plans: 
                    if up['name'] == "SpacedApiUsagePlan":
                        usage_plan_id = up['id'] 
                        break 
                # Map the API key that was created to the Usage Plan using a 
                # Usage Plan Key
                response = client.create_usage_plan_key( 
                    usagePlanId=usage_plan_id, 
                    keyId=key_id, 
                    keyType="API_KEY" 
                )
            except Exception as e:
                print(e)  
        return response 


def create_api_keys_for_all_users():
    for u in User.objects.all():
        p = Profile.objects.get(user=u)
        # if they don't have local api keys, create those first
        if not p.read_api_key:
            p.read_api_key = generate_random_string(128)
        if not p.cud_api_key: 
            p.cud_api_key = generate_random_string(128)
        p.save()

        for operation, api_key in {
            'read': p.read_api_key,
            'cud':p.cud_api_key
            }.items():
            response = create_and_add_api_key_to_usage_plan(user=u,key_value=api_key,operation=operation)
            print(response)
            