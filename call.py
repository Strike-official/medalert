import requests
import config

def call_notification(driver_number, patient_number):
    url = config.calling_service["url"]
    url = url+'?From='+ driver_number +'&CallerId='+config.calling_service["caller_id"]+'&To='+patient_number

    x = requests.post(url,timeout=30)

    print(x.text)