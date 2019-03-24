
rm -f LambdaFunction.zip \
&& rm -rf LambdaFunction \
&& mkdir LambdaFunction \
&& cp -r ./src/* ./LambdaFunction \
&& pip install -r ./requirements.txt -t ./LambdaFunction --no-cache-dir \
&& find ./LambdaFunction -name "*.pyc" -type f -delete \
&& cd ./LambdaFunction \
&& zip -r ../LambdaFunction.zip * \
&& cd ..
