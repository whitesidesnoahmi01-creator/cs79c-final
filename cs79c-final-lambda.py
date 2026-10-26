import json
import boto3
from urllib.parse import unquote_plus

s3 = boto3.client('s3')
table = boto3.resource('dynamodb').Table('cs79c-file-results')
sns = boto3.client('sns')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    filename = event['Records'][0]['s3']['object']['key']
    filename = unquote_plus(filename)

    file = s3.get_object(Bucket=bucket, Key=filename)
    text = file['Body'].read().decode('utf-8')

    words = len(text.split())
    lines = len(text.splitlines())

    table.put_item(Item={
        'fileName': filename,
        'wordCount': words,
        'lineCount': lines,
        'processedBy': 'Noah Whitesides'
    })

    sns.publish(
        TopicArn='arn:aws:sns:us-west-2:659817809860:cs79c-file-alerts',
        Subject='File processed',
        Message=f'{filename}: {words} words, {lines} lines'
    )

    print('File processed:', filename)
    print('Words:', words)
    print('Lines:', lines)
