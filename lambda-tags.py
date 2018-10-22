import os
import boto3
import jinja2
import datetime as dt
from boto3.dynamodb.conditions import Key, Attr

s3 = boto3.resource('s3')
bucket = s3.Bucket('tech-jobs-list')
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

job = {
    "title": "Security Analyst",
    "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
    "company": "Rackspace",
    "location": "San Antonio, TX",
    "salary": 0,
    "link":"http://app.jobvite.com/m?3T307kwS",
    "tags":["networking", "security", "pentesting"]
}

def grab_jobs(tag):
    table = dynamodb.Table('jobs')
    response = table.scan(
        FilterExpression=Attr('tags').contains(tag)
    )
    return response['Items']

def build_list(jobs):
    html = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd())).get_template("templates/job-list.html").render(jobs=jobs)

    with open("index.html", "w") as index_file:
        index_file.write(html)

def upload_list(tag):
    if not folder_exists(tag):
        bucket.put_object(Key=f"tags/{tag.lower()}/")
        
    with open('index.html', 'rb') as data:
        bucket.put_object(Key=f"tags/{tag.lower()}/index.html", Body=data, ContentType='text/html')

def folder_exists(tag):
    key = f"tags/{tag.lower()}/" 
    objs = list(bucket.objects.filter(Prefix=key))
    if len(objs) > 0 and objs[0].key == key:
        return True
    else:
        return False

def generate_joblist(tag):
    jobs = grab_jobs(tag)
    build_list(jobs)
    upload_list(tag)

def process_job(job):
    for tag in job['tags']:
        generate_joblist(tag)

if __name__ == "__main__":
    process_job(job)
    print("Done.")