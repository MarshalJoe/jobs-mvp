import os
import boto3
import jinja2
from boto3.dynamodb.conditions import Key, Attr

# jobs = [
#     {
#         "title": "Business Systems Engineer",
#         "timestamp": "10 days ago",
#         "company": "ObjectRocket",
#         "location": "Austin, TX",
#         "salary": 0,
#         "link":"https://objectrocket.com/careers?ref=jobs-list",
#         "tags":["datawarehouse", "hubspot", "python"]
#     },
#     {
#         "title": "Elasticsearch Engineer",
#         "timestamp": "14 days ago",
#         "company": "ObjectRocket",
#         "location": "Austin, TX",
#         "salary": 0,
#         "link":"https://objectrocket.com/careers?ref=jobs-list",
#         "tags":["python", "elasticsearch"]
#     },
#     {
#         "title": "Customer Data Engineer",
#         "timestamp": "18 days ago",
#         "company": "ObjectRocket",
#         "location": "Austin, TX",
#         "salary": 0,
#         "link":"https://objectrocket.com/careers?ref=jobs-list",
#         "tags": ["suport", "mongodb"]
#     },
#     {
#         "title": "Cloud Engineer",
#         "timestamp": "30 days ago",
#         "company": "ObjectRocket",
#         "location": "Austin, TX",
#         "salary": 0,
#         "link":"https://objectrocket.com/careers?ref=jobs-list",
#         "tags": ["aws", "docker", "go", "kubernetes"]
#     },

# ]

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

# table = dynamodb.Table('jobs')

# print("Table status:", table.table_status)

# for job in jobs:
#     response = table.put_item(Item=job)
#     print("PutItem succeeded")
#     print(response)

def grab_jobs():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
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
    print("Done.")