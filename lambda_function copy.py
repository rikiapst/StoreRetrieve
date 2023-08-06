from aws_lambda_powertools.utilities.typing import LambdaContext

from session import mysql_engine
from globals import tracer, logger, metrics
from globals import engine

from endpoints.get_conversation import handler as retrieve_handler
from endpoints.store_conversations import handler as store_conversation
from endpoints.store_topic import handler as store_topic
from endpoints.store_user import handler as store_user


# Map route keys to handler functions
routes = {
    "POST /store_conversation": store_conversation,
    "POST /store_topic": store_topic,
    "POST /store_user": store_user,
    "GET /retrieve/{id}": retrieve_handler
}



@metrics.log_metrics
@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext):
    print("event")
    global engine

    # Initialize SQLAlchemy engine if it's not already initialized
    if engine is None:
        engine = mysql_engine

    print("--=-=-=-",event)

    http_method = event.get('httpMethod')
    resource = event.get('resource')

    if http_method and resource:
        route_key = http_method + ' ' + resource
        handler = routes.get(route_key)

        if handler:
            return handler(event, context)
        else:
            return {"statusCode": 404, "body": "Not Found"}


