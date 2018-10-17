import os
import boto3
import jinja2
import datetime as dt
from boto3.dynamodb.conditions import Key, Attr

s3 = boto3.resource('s3')
bucket = s3.Bucket('tech-jobs-list')
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

def grab_jobs(company):
    table = dynamodb.Table('jobs')
    response = table.scan(
        FilterExpression=Attr('company').eq(company)
    )
    return response['Items']

def build_list(jobs):
    html = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd())).get_template("templates/job-list.html").render(jobs=jobs)

    with open("index.html", "w") as index_file:
        index_file.write(html)

def upload_list(company):
    if not folder_exists(company):
        bucket.put_object(Key=f"{company.lower()}/")
        
    with open('index.html', 'rb') as data:
        bucket.put_object(Key=f"{company.lower()}/index.html", Body=data, ContentType='text/html')

def folder_exists(company):
    key = f"{company.lower()}/" 
    objs = list(bucket.objects.filter(Prefix=key))
    if len(objs) > 0 and objs[0].key == key:
        return True
    else:
        return False

def generate_joblist(company):
    jobs = grab_jobs(company)
    build_list(jobs)
    upload_list(company)

if __name__ == "__main__":
    generate_joblist("Rackspace")
    print("Done.")