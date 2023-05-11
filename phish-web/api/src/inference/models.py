import boto3

def predict(url: str):

    return url

def predict_and_save(url: str):
    prediction = predict(url)

    s3 = boto3.resource('s3')
    bucket_name = 'name'
    key = 'predictions/prediction.txt' # filename

    s3.Object(bucket_name, key).put(Body=str(prediction))

    return prediction