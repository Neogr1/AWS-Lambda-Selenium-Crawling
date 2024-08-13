import json
import boto3

cars = ['그랜저', '아반떼', '팰리세이드', '캐스퍼', '제네시스', '아이오닉']
communities = ['dcinside', 'bobaedream', 'navercafe']

def lambda_handler(event, context):
    lambda_client = boto3.client('lambda')

    for car in cars:
        for community in communities:
            payload = {
                'car_name': car,
                'community_name': community
            }

            try:
                # 비동기 호출
                lambda_client.invoke(
                    FunctionName='monitor-community',  # 실제 크롤링 Lambda 함수 이름으로 변경
                    InvocationType='Event',  # 비동기 호출
                    Payload=json.dumps(payload)
                )

                print(f"Invoked {car} in {community} successfully.")
                
            except Exception as e:
                print(f"Error invoking Lambda for {car} in {community}: {str(e)}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Lambda functions triggered for all car and community combinations.')
    }
