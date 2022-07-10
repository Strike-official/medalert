import requests
import config

def call_notification():
    url = config.calling_service["url"]
    url = url+'?From='+ config.calling_service["to_number"] +'&CallerId='+config.calling_service["caller_id"]+'&Url='+config.calling_service["flow_url"]

    x = requests.post(url,timeout=30)

    print(x.text)