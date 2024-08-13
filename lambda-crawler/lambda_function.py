import json
import boto3
import io
from datetime import datetime, timedelta

# from crawler.bobaedream_crawler import BobaedreamCrawler
from crawler.dcinside_crawler import DcInsideCrawler
from crawler.naver_cafe_crawler import NaverCafeCralwer


KOREAN_CAR_NAME = {
    'avante':'아반떼',
    'casper':'캐스퍼',
    'genesis':'제네시스',
    'granduer':'그랜저',
    'ioniq':'아이오닉',
    'palisade':'리세이드', # 팰리세이드를 펠리세이드로 적는 사람이 많음
}

def upload_df_to_s3(df, bucket_name, object_name):
    s3 = boto3.client('s3')

    # 데이터프레임을 CSV로 변환하여 메모리에서 처리
    csv_buffer = io.BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    try:
        s3.upload_fileobj(Fileobj=csv_buffer, Bucket=bucket_name, Key=object_name)
        msg = (
            f"총 {len(df)}개의 게시글이 크롤링 되었습니다.\n"
            + f"데이터가 [{bucket_name}:{object_name}]에 성공적으로 저장되었습니다..\n"
        )
        return True, msg
    except Exception as e:
        return False, f"S3 업로드 중 에러 발생: {str(e)}"

def calculate_time_range():
    now_utc0 = datetime.now()
    now_utc9 = now_utc0 + timedelta(hours=9)
    start_datetime = now_utc9.replace(minute=0, second=0, microsecond=0) - timedelta(hours=1)
    end_datetime = start_datetime + timedelta(minutes=59)
    return start_datetime, end_datetime

def get_query_in_korean(query):
    try:
        return KOREAN_CAR_NAME[query]
    except KeyError:
        raise ValueError(f'알 수 없는 자동차 이름({query})입니다.')

def lambda_handler(event, context):
    try:
        start_datetime, end_datetime = calculate_time_range()

        ### 파라미터 확인 ###
        community = event.get('community')
        query = event.get('car_name')
        if not query:
            return {'statusCode': 400, 'body': json.dumps('Error: 검색할 자동차 이름이 지정되지 않았습니다.')}
        
        query_kor = get_query_in_korean(query)

        ### 크롤링 ###
        if community == 'bobaedream':
            pass
        elif community == 'dcinside':
            crawler = DcInsideCrawler(query_kor, start_datetime, end_datetime)
            df = crawler.start_crawling(num_processes=1)
        elif community == 'naver_cafe':            
            crawler = NaverCafeCralwer()
            crawler.set_current_crawl_option("casper")
            df = crawler.start_crawling(end_datetime)
        else:
            return {'statusCode': 400, 'body': json.dumps(f'Error: 알 수 없는 커뮤니티({community})입니다. [bobaedream, dcinside, naver_cafe] 중 하나를 지정하세요.')}

        ### S3 업로드 ###
        object_name = f"monitor/community/{community}/{start_datetime.strftime('%Y%m%d_%H%M')}_{end_datetime.strftime('%H%M')}_{community}_{query}.csv"
        upload_result, msg = upload_df_to_s3(df, "hyundata2-testbucket", object_name)
        if not upload_result:
            return {'statusCode': 500, 'body': json.dumps(f"Error: S3 업로드 실패\n{msg}")}

        return {'statusCode': 200, 'body': json.dumps(msg)}

    except ValueError as ve:
        return {'statusCode': 400, 'body': json.dumps(str(ve))}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(f"Error: 알 수 없는 오류가 발생했습니다. {str(e)}")}