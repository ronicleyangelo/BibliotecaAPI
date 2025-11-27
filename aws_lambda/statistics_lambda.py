import json

def lambda_handler(event, context):
    print("Lambda de estatísticas executada")
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Estatísticas processadas'})
    }