import os
import boto3
import jinja2
import datetime as dt
from boto3.dynamodb.conditions import Key, Attr

jobs = [
    {
        "title": "Scrum Master II",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "Rackspace",
        "location": "San Antonio, TX",
        "salary": 0,
        "link":"http://app.jobvite.com/m?3vEZ7kw4",
        "tags":["agile", "leadership", "product",]
    },
    {
        "title": "Manager, Network Defense",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "Rackspace",
        "location": "San Antonio, TX",
        "salary": 0,
        "link":"http://app.jobvite.com/m?3pFZ7kwZ",
        "tags":["security", "leadership", "networking"]
    },
    {
        "title": "Senior DevOps Engineer",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "Rackspace",
        "location": "San Antonio, TX",
        "salary": 0,
        "link":"http://app.jobvite.com/m?3TFZ7kwt",
        "tags":["aws", "python", "automation"]
    },
    {
        "title": "Sr. Linux Implementation Engineer",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "Rackspace",
        "location": "San Antonio, TX",
        "salary": 0,
        "link":"http://app.jobvite.com/m?37GZ7kwI",
        "tags":["linux", "security", "networking"]
    },
    {
        "title": "Software Developer - Managed Public Clouds",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "Rackspace",
        "location": "US Remote",
        "salary": 0,
        "link":"http://app.jobvite.com/m?3yNZ7kwg",
        "tags":["aws", "go", "docker" "node"]
    },
    {
        "title": "Manager, Infrastructure Change Management",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "Rackspace",
        "location": "San Antonio, TX",
        "salary": 0,
        "link":"http://app.jobvite.com/m?3KSZ7kwx",
        "tags":["leadership", "automation"]
    },
    {
        "title": "Linux Systems Engineer",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "Rackspace",
        "location": "Austin, TX",
        "salary": 0,
        "link":"http://app.jobvite.com/m?3yUZ7kwn",
        "tags":["linux", "automation", "networking"]
    },
    {
        "title": "Linux Operations Engineer",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "Rackspace",
        "location": "San Antonio, TX",
        "salary": 0,
        "link":"http://app.jobvite.com/m?3DW07kwv",
        "tags":["linux", "automation", "networking"]
    },
    {
        "title": "Senior Internal Controls Analyst",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "Rackspace",
        "location": "San Antonio, TX",
        "salary": 0,
        "link":"http://app.jobvite.com/m?3lu07kwL",
        "tags":["automation", "fintech"]
    },
    {
        "title": "Data Analyst, Supply Chain",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "Rackspace",
        "location": "San Antonio, TX",
        "salary": 0,
        "link":"http://app.jobvite.com/m?3aY07kw4",
        "tags":["sql", "data", "logistics"]
    },
    {
        "title": "Sr Linux System Engineer",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "Rackspace",
        "location": "Remote",
        "salary": 0,
        "link":"http://app.jobvite.com/m?3o007kwk",
        "tags":["linux", "networking"]
    },
    {
        "title": "Sr Scrum Master",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "Rackspace",
        "location": "San Antonio, TX",
        "salary": 0,
        "link":"http://app.jobvite.com/m?3z007kwv",
        "tags":["agile", "leadership", "product"]
    },
    {
        "title": "Security Analyst II",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "Rackspace",
        "location": "San Antonio, TX",
        "salary": 0,
        "link":"http://app.jobvite.com/m?3i007kwe",
        "tags":["security", "pentesting", "networking"]
    },
    {
        "title": "Senior Technology (IT) Auditor",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "Rackspace",
        "location": "San Antonio, TX",
        "salary": 0,
        "link":"http://app.jobvite.com/m?3M107kwJ",
        "tags":["security", "logistics", "networking"]
    },
    {
        "title": "Sr. Identity & Access Management Engineer",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "Rackspace",
        "location": "US Remote",
        "salary": 0,
        "link":"http://app.jobvite.com/m?38107kw5",
        "tags":["security", "networking", "linux"]
    },
    {
        "title": "iOS Developer",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "Rackspace",
        "location": "Austin, TX",
        "salary": 0,
        "link":"http://app.jobvite.com/m?3B207kwz",
        "tags":["ios", "mobile", "leadership", "ui"]
    },
    {
        "title": "Site Reliability Engineer",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "Rackspace",
        "location": "US Remote",
        "salary": 0,
        "link":"http://app.jobvite.com/m?37207kw5",
        "tags":["networking", "automation", "kubernetes"]
    },
    {
        "title": "OpenStack Architect",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "Rackspace",
        "location": "San Antonio, TX",
        "salary": 0,
        "link":"http://app.jobvite.com/m?3Ev07kw5",
        "tags":["networking", "automation", "architecture"]
    },
    {
        "title": "Network Security Administrator",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "Rackspace",
        "location": "San Antonio, TX",
        "salary": 0,
        "link":"http://app.jobvite.com/m?3N307kwM",
        "tags":["networking", "security", "architecture"]
    },
    {
        "title": "Security Analyst",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "Rackspace",
        "location": "San Antonio, TX",
        "salary": 0,
        "link":"http://app.jobvite.com/m?3T307kwS",
        "tags":["networking", "security", "pentesting"]
    },
    {
        "title": "Linux Administrator",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "Rackspace",
        "location": "San Antonio, TX",
        "salary": 0,
        "link":"http://app.jobvite.com/m?3r407kwr",
        "tags":["linux", "networking"]
    },
    {
        "title": "Windows System Administrator",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "Rackspace",
        "location": "San Antonio, TX",
        "salary": 0,
        "link":"http://app.jobvite.com/m?3J407kwJ",
        "tags":["windows", "networking"]
    },
    {
        "title": "Product Engineer",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "Rackspace",
        "location": "San Antonio, TX",
        "salary": 0,
        "link":"http://app.jobvite.com/m?3V407kwV",
        "tags":["product", "apis", "ui"]
    },
    {
        "title": "Software Developer IV",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "Rackspace",
        "location": "Austin, TX",
        "salary": 0,
        "link":"http://app.jobvite.com/m?3f407kwf",
        "tags":["product", "apis", "ui"]
    },
    {
        "title": "DevOps Engineer IV",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "Rackspace",
        "location": "Austin, TX",
        "salary": 0,
        "link":"http://app.jobvite.com/m?3t507kwu",
        "tags":["automation", "docker", "networking", "apis"]
    },
]

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

# print(client.list_tables())

# table = dynamodb.create_table(
#     TableName='jobs',
#     KeySchema=[
#         {
#             'AttributeName': 'title',
#             'KeyType': 'HASH'  #Partition key
#         },
#         {
#             'AttributeName': 'company',
#             'KeyType': 'RANGE'  #Sort key
#         }
#     ],
#     AttributeDefinitions=[
#         {
#             'AttributeName': 'title',
#             'AttributeType': 'S'
#         },
#         {
#             'AttributeName': 'company',
#             'AttributeType': 'S'
#         }  
#     ],
#     ProvisionedThroughput={
#         'ReadCapacityUnits': 10,
#         'WriteCapacityUnits': 10
#     }
# )


def add_jobs(jobs):
    table = dynamodb.Table('jobs')
    for job in jobs:
        response = table.put_item(Item=job)
        print("PutItem succeeded")


def grab_jobs():
    table = dynamodb.Table('jobs')
    response = table.scan(
        FilterExpression=Attr('company').eq("ObjectRocket")
    )
    return response['Items']


def build(jobs):
    html = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd())).get_template("templates/job-list.html").render(jobs=jobs)

    with open("index.html", "w") as index_file:
        index_file.write(html)


def upload():
    s3 = boto3.resource('s3')

    with open('index.html', 'rb') as data:
        s3.Bucket('tech-jobs-list').put_object(Key='index.html', Body=data, ContentType='text/html')

if __name__ == "__main__":
    # jobs = grab_jobs()
    # build(jobs)
    # upload()
    add_jobs(jobs)
    print("Done.")