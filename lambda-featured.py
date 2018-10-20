import os
import boto3
import jinja2
import datetime as dt
from boto3.dynamodb.conditions import Key, Attr

job = {
	"title": "Security Analyst",
	"timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
	"company": "Rackspace",
	"location": "San Antonio, TX",
	"salary": 0,
	"link":"http://app.jobvite.com/m?3T307kwS",
	"tags":["networking", "security", "pentesting"]
}

s3 = boto3.resource('s3')
bucket = s3.Bucket('tech-jobs-list')

def build_featured(job):
    html = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd())).get_template("templates/featured.html").render(job=job)

    with open("index.html", "w") as index_file:
        index_file.write(html)

def upload_featured():
    with open('index.html', 'rb') as data:
        bucket.put_object(Key="featured/index.html", Body=data, ContentType='text/html')

if __name__ == "__main__":
    build_featured(job)
    upload_featured()
    print("Done.")