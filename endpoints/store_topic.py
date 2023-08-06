import json 
from aws_lambda_powertools.utilities.validation import validate

from models.topics import Topic

from globals import tracer
from globals import app
from globals import engine
from session import session
from session import mysql_engine
# from schemas.conversation import conversation as conversation_schema


@tracer.capture_method
def store_topic(body):
    # Initialize SQLAlchemy engine if it's not already initialized
    global engine
    if engine is None:
        engine = mysql_engine


    topic = Topic(
                topicName=body.get('topicName'),
                details=body.get('details'),
                createdDate=body.get('createdDate')
            )
            

    # Store the Conversation object in the database
    with session:
        session.add(topic)
        session.commit()

# @validate(inbound_schema=conversation_schema)
@app.post("/store_topic")
def handler(event, context):
    body = json.loads(event.get('body', '{}'))
    store_topic(body)
    return {"statusCode": 200, "body": "Data stored successfully!"}