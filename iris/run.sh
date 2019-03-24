
docker run --rm -v "$PWD/task":/var/task -v "$PWD/opt":/opt lambci/lambda:python3.7 lambda_function.lambda_handler
