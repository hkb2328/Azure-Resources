import json
import time
import random
from azure.servicebus import ServiceBusClient, ServiceBusMessage

# Azure Service Bus connection details
CONNECTION_STR = "****"
TOPIC_NAME = "test_topic"

def generate_mock_message():
    message_data = {
        "orderId": str(random.randint(1000, 9999)),
        "customerName": random.choice(["John Doe", "Jane Smith", "Alice Brown", "Bob Johnson"]),
        "region": random.choice(["north", "south", "east", "west"]),
        "priority": random.choice(["low", "medium", "high"]),
        "orderAmount": round(random.uniform(100, 1000), 2)
    }
    return message_data

def send_message_to_service_bus(client, topic_name, message_body):
    """Send a message to the specified Service Bus Topic."""
    sender = client.get_topic_sender(topic_name=topic_name)
    with sender:
        # Create the ServiceBusMessage
        message = ServiceBusMessage(
            body=json.dumps(message_body),
            application_properties={
                "region": message_body["region"],
                "priority": message_body["priority"]
            }
        )
        # Send the message
        sender.send_messages(message)
        print(f"Sent message: {message_body}")

def main():
    # Create a ServiceBusClient using the connection string
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)
    
    try:
        while True:
            # Generate a mock message
            message_body = generate_mock_message()
            
            # Send the message to the Service Bus Topic
            send_message_to_service_bus(servicebus_client, TOPIC_NAME, message_body)
            
            # Sleep for a while before sending the next message (optional)
            time.sleep(5)  # Adjust the delay as needed

    finally:
        # Close the ServiceBusClient when done
        servicebus_client.close()

if __name__ == "__main__":
    main()
