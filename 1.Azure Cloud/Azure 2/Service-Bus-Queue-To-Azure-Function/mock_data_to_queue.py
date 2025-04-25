import json
import random
import time
from azure.servicebus import ServiceBusClient, ServiceBusMessage

# Azure Service Bus connection details
CONNECTION_STR = "*****"
QUEUE_NAME = "test_queue"

def generate_iot_data():
    return {
        "deviceId": f"device_{random.randint(1, 100)}",
        "temperature": round(random.uniform(20.0, 35.0), 2),
        "humidity": round(random.uniform(30.0, 60.0), 2),
        "batteryLevel": round(random.uniform(10.0, 100.0), 2),
        "timestamp": time.time()
    }

def send_message_to_queue(client, queue_name, message_body):
    """Send a message to the specified Service Bus Queue."""
    sender = client.get_queue_sender(queue_name=queue_name)
    with sender:
        # Create the ServiceBusMessage
        message = ServiceBusMessage(body=json.dumps(message_body))
        sender.send_messages(message)
        print(f"Sent IoT message: {message_body}")

def main():
    # Create a ServiceBusClient using the connection string
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)
    
    try:
        while True:
            # Generate mock IoT telemetry data
            message_body = generate_iot_data()
            
            # Send the message to the Service Bus Queue
            send_message_to_queue(servicebus_client, QUEUE_NAME, message_body)
            
            # Sleep for a short time before sending the next message
            time.sleep(5)

    finally:
        # Close the ServiceBusClient when done
        servicebus_client.close()

if __name__ == "__main__":
    main()
