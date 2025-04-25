import azure.functions as func
import logging
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import os

app = func.FunctionApp()

@app.blob_trigger(arg_name="myblob", path="landing-zn/{name}",
                               connection="blobstoragetestgds_STORAGE") 
def gdsBlobTriggerDev(myblob: func.InputStream):

    blobName = myblob.name
    service_bus_connection_str = os.getenv('SERVICE_BUS_CONNECTION_STRING')
    topic_name = os.getenv('SERVICE_BUS_TOPIC_NAME')

    logging.info(f"Service Bus Connection Str {service_bus_connection_str}")
    logging.info(f"Service Bus Topic Name {topic_name}")
    
    if blobName.endswith(".csv"):
        logging.info(f"Blob trigger function processed blob \n"
                        f"Name: {blobName}\n")
    # Add your processing logic here
    else:
        logging.info(f"Ignored blob: {blobName} as it is not a CSV file.")
    
    custom_message = f"{blobName} blob arrived in storage account container !!"
    custom_subject = f"Azure Function to Service Bus Message"
    
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=service_bus_connection_str, logging_enable=True)
    with servicebus_client:
        sender = servicebus_client.get_topic_sender(topic_name=topic_name)
        with sender:
            message = ServiceBusMessage(
                body=custom_message,
                subject=custom_subject
            )
            sender.send_messages(message)

    logging.info(f'Message sent to Service Bus Topic {topic_name} !!')
