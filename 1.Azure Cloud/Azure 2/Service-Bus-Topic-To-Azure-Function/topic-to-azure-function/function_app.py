import azure.functions as func
import logging

app = func.FunctionApp()

@app.service_bus_topic_trigger(arg_name="azservicebus", subscription_name="filter_based_sub", topic_name="test_topic",
                               connection="servicebusgdsdev_SERVICEBUS") 
def servicebusTopicTrigger(azservicebus: func.ServiceBusMessage):
    logging.info('Python ServiceBus Topic trigger processed a message: %s',
                azservicebus.get_body().decode('utf-8'))
