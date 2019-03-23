import pytest
import lambda_function as lf

def test_lambda_function_1():
	assert 'https://s3.eu-west-2.amazonaws.com/bucket/key' == lf.get_url("bucket","key")


event = {
	"Type" : "Notification",
	"MessageId" : "c4f0fd78-8cf9-5996-bcc0-a872a4145db2",
	"TopicArn" : "arn:aws:sns:eu-west-2:021908831235:aws-earth-mo-atmospheric-ukv-prd",
	"Message" : { "model": "mo-atmospheric-ukv-prd", "object_size": 213811.0, "forecast_reference_time": "2019-03-17T22:00:00Z", "forecast_period": "23400", "forecast_period_units": "seconds", "ttl": 1553555754, "time": "2019-03-18T04:30:00Z", "bucket": "aws-earth-mo-atmospheric-ukv-prd", "key": "caae6365251b4924578e3f2072bab4c79f049eb8.nc", "created_time": "2019-03-17T23:11:13Z", "name": "lwe_snowfall_rate"},
	"Timestamp" : "2019-03-18T23:15:57.668Z",
	"SignatureVersion" : "1",
	"Signature" : "hycHiTbRRruhXFgbN8111P/aCox5+hXMx5pMjHIqI0IZaZtHK8gCcE9UEQ/Z58IBvB17xHkZAq93JFjxXDbWXS0ZQa+jTEpUtHo99eaDV9C4p2zIex+ZQMcLXW9FFloygpqH0OZvv2/cOuoz9eCHb9hc5pEAGhHWgEP8HJiNQjzn1uNwzD8XXR7a4G8j0sJPUH1FVeKch7UTENM0j8CAxQ2D2RJOBOEDlCu6fZGCDtDtGDIek94tyjV6wbcZL7Gi03FHMglY2XTWLcj2TfAi7zGXQwpBFwUUkwN/RkLnwcVqF5fykhBAotf66FuXn3lwPhN0Z09LeNsPEfEC80WOLQ==",
	"SigningCertURL" : "https://sns.eu-west-2.amazonaws.com/SimpleNotificationService-6aad65c2f9911b05cd53efda11f913f9.pem",
	"UnsubscribeURL" : "https://sns.eu-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-2:021908831235:aws-earth-mo-atmospheric-ukv-prd:a79594c3-7fc8-406a-97e7-e443415ce6e6",
	"MessageAttributes" : {
		"forecast_reference_time" : {"Type":"String","Value":"2019-03-17T22:00:00Z"},
		"name" : {"Type":"String","Value":"lwe_snowfall_rate"},
		"model" : {"Type":"String","Value":"mo-atmospheric-ukv-prd"}
	}
}

def test_target_bucket():
	assert 'conformed.takehome.power.io' == lf.target_bucket()

def test_partition():
	assert None != lf.partition()
	partition = lf.partition()
	print ( partition )
	assert '2019' in partition 
	assert '/3/' in partition 

def test_event_parse():
	bucket, key = lf.parse_event(event)
	assert "aws-earth-mo-atmospheric-ukv-prd" == bucket
	assert "caae6365251b4924578e3f2072bab4c79f049eb8.nc" == key

def test_url():
	bucket = "bucket"
	key = "key"
	url = lf.get_url(bucket, key)
	assert None != url

def test_download():
	bucket, key = lf.parse_event(event)
	url = lf.get_url(bucket, key)
	lf.download(url, key)
	import os.path
	os.path.isfile(key)

def test_parse():
	bucket, key = lf.parse_event(event)
	url = lf.get_url(bucket, key)
	lf.download(url, key)
	[obj] = lf.parse(key)
	print( obj )

def test_write():
	bucket, key = lf.parse_event(event)
	bucket = 'conformed.takehome.power.io'
	encoded_string = "Hello world".encode('utf-8')
	r = lf.write(encoded_string, bucket, key +'.txt')
	assert None != r
	print ( r.metadata )

def test_lambda_function():
	r = lf.lambda_handler(event, None)
	assert None != r
