import boto3
import json
from jinja2 import Template

s3_client = boto3.client('s3')
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

def lambda_handler(event, context):
    input_bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    output_bucket = "faq-output-bucket"
    
    try:
        file_content = ""
        
        response = s3_client.get_object(Bucket=input_bucket, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        
        faq_data = json.loads(file_content)
        print(f"Successfully read file {key} from bucket {input_bucket}.")
        print(f"FAQ Data: {faq_data}")
        
        faq_responses = generate_faq_responses(faq_data)
        output_file_name = key.replace('.json', '-results.json')
        
        s3_client.put_object(
            Bucket=output_bucket,
            Key=output_file_name,
            Body=json.dumps(faq_responses),
            ContentType='application/json'
        )
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error occurred: {e}")
        }

    return {
        'statusCode': 200,
        'body': json.dumps(f"Successfully generated FAQ responses for {key} from bucket {input_bucket}.")
    }

def generate_faq_responses(faq_data):
    with open('prompt_template.txt', "r") as file:
        template_string = file.read()

    template = Template(template_string)
    
    faq_responses = []
    
    for faq in faq_data['faqs']:
        question = faq['question']
        context = faq.get('context', "")
        data = {
            'question': question,
            'context': context
        }
        
        prompt = template.render(data)
        print(f"Generated Prompt: {prompt}")
        
        response_text = invoke_bedrock_model(prompt)
        faq_responses.append({
            'question': question,
            'response': response_text
        })
        
    return faq_responses

def invoke_bedrock_model(prompt):
    kwargs = {
        "modelId": "amazon.titan-text-express-v1",
        "contentType": "application/json",
        "accept": "*/*",
        "body": json.dumps(
            {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 2048,
                    "stopSequences": [],
                    "temperature": 0.7,
                    "topP": 0.9
                }
            }
        )
    }
    
    response = bedrock_runtime.invoke_model(**kwargs)
    response_body = json.loads(response.get('body').read())
    response_text = response_body.get('results')[0].get('outputText')
    
    return response_text
