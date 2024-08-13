# AWS-Lambda-Selenium-Crawling
AWS Lambda에서 selenium 크롤링을 위해 사용할 Docker 컨테이너 이미지를 위한 Dockerfile과 샘플 크롤링 스크립트입니다.

## Upload Selenium Docker Image on AWS ECR
```bash
export AWS_ACCOUNT_ID={your_aws_id}
export AWS_REGION={your_region}
export IMAGE_NAME=selenium-chrome-driver
export IMAGE_TAG=latest

docker build -t ${IMAGE_NAME} .
docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}:${IMAGE_TAG}
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}:${IMAGE_TAG}
```

## Test for Crawling on Local
두 가지 방법 모두 `./lambda-crawler/` 디렉터리에서 실행합니다.
`./lambda-crawler/event.json` 파일을 수정해서 다양한 상황에 대해 테스트할 수 있습니다.

### Using SAM
```bash
docker build -t selenium-chrome-driver .
sam build
sam local invoke Crawler --event event.json
```

### Using Docker Image
```bash
docker build -t selenium-chrome-driver .
docker run -p 9000:8080 selenium-chrome-driver
# 아래는 새 터미널에서 실행
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d @event.json
```

## References
- https://youtu.be/8XBkm9DD6Ic?si=MT9x_og_yUC2IFrn
- https://towardsdev.com/easily-use-selenium-with-aws-lambda-2cc49ca43b93