import json
import joblib
import boto3

loaded_model = None

def load_model():
    global loaded_model
    
    # load model from s3 bucket
    s3 = boto3.client("s3")

    bucket_name = 'phishing-project'
    model_folder = "model/latest/"

    try:
       response = s3.list_objects(Bucket=bucket_name, Prefix=model_folder)
    except Exception as e:
       print('handle exception error')
       
    objects = response['Contents']
    model = objects[0]['Key']

    response = s3.get_object(Bucket=bucket_name, Key=model)
    pkl_file_content = response['Body'].read()
    loaded_model = joblib.loads(pkl_file_content)
    return loaded_model


def lambda_handler(event, context):
    
    # check if model is loaded
    if not loaded_model:
        load_model()
    
    msg_body = json.loads(event['Records'][0]['body'])
    url = msg_body['url']
    # make inference using model
    prediction = phish_inference(loaded_model)
    # store url and inference result
        
    
    return json.dumps({
        'statusCode': 200,
        'url': url,
        'prediction': prediction
    })
