import os
import boto3
import jinja2

jobs = [
    {
        "title": "Business Systems Engineer",
        "timestamp": "10 days ago",
        "company": "ObjectRocket",
        "location": "Austin, TX",
        "link":"https://objectrocket.com/careers?ref=jobs-list",
        "tags":["datawarehouse", "hubspot", "python"]
    },
    {
        "title": "Elasticsearch Engineer",
        "timestamp": "14 days ago",
        "company": "ObjectRocket",
        "location": "Austin, TX",
        "link":"https://objectrocket.com/careers?ref=jobs-list",
        "tags":["python", "elasticsearch"]
    },
    {
        "title": "Customer Data Engineer",
        "timestamp": "18 days ago",
        "company": "ObjectRocket",
        "location": "Austin, TX",
        "link":"https://objectrocket.com/careers?ref=jobs-list",
        "tags": ["suport", "mongodb"]
    },
    {
        "title": "Cloud Engineer",
        "timestamp": "30 days ago",
        "company": "ObjectRocket",
        "location": "Austin, TX",
        "link":"https://objectrocket.com/careers?ref=jobs-list",
        "tags": ["aws", "docker", "go", "kubernetes"]
    },

]

def build(jobs):
    html = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd())).get_template("templates/job-list.html").render(jobs=jobs)

    with open("index.html", "w") as index_file:
        index_file.write(html)


def upload():
    s3 = boto3.resource('s3')

    with open('index.html', 'rb') as data:
        s3.Bucket('tech-jobs-list').put_object(Key='index.html', Body=data, ContentType='text/html')

if __name__ == "__main__":
    build(jobs)
    upload()
    print("Done.")