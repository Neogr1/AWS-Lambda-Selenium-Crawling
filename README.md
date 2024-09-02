# Selenium-Crawling-on-AWS-Lambda
Dockerfile and sample crawling script for a Docker container image for selenium crawling on AWS Lambda.

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
You can modify the `event.json` file to test for different situations.

### Using SAM
```bash
docker build -t ${IMAGE_NAME} .
sam build
sam local invoke Crawler --event event.json
```

### Using Docker Image
```bash
docker build -t ${IMAGE_NAME} .
docker run -p 9000:8080 selenium-chrome-driver
# run the command below in new terminal
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d @event.json
```

## References
- https://youtu.be/8XBkm9DD6Ic?si=MT9x_og_yUC2IFrn
- https://towardsdev.com/easily-use-selenium-with-aws-lambda-2cc49ca43b93