import json 
from models.conversations import Conversation 
from globals import tracer
from globals import app
from globals import engine
from session import session
from session import mysql_engine

@tracer.capture_method
def get_conversation(conversation_id):
    # Initialize SQLAlchemy engine if it's not already initialized
    global engine
    if engine is None:
        engine = mysql_engine

    # Get a Conversation object from the database
    with session:
        conversation = session.query(Conversation).filter_by(id=conversation_id).first()

        if conversation is None:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': f'Conversation with ID {conversation_id} not found.'})
            }
        return {"statusCode": 200, "body": json.dumps(conversation.to_dict())}
    


@app.get("/get_conversation/{id}")
def handler(event, context):
    conversation_id = int(event['pathParameters']['id'])
    response = get_conversation(conversation_id)
    return response