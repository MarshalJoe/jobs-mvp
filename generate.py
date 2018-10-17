import os
import boto3
import jinja2
import datetime as dt
from boto3.dynamodb.conditions import Key, Attr

jobs = [
    {
        "title": "Software Engineer",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "company": "ObjectRocket",
        "location": "Austin, TX",
        "salary": 0,
        "link":"http://app.jobvite.com/m?3qrH7kwu",
        "tags":["apis", "docker", "aws",]
    }
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



# print("Table status:", table.table_status)


def add_jobs(jobs):
    table = dynamodb.Table('jobs')
    for job in jobs:
        response = table.put_item(Item=job)
        print("PutItem succeeded")
        print(response)


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
    jobs = grab_jobs()
    build(jobs)
    upload()
    # add_jobs(jobs)
    print("Done.")