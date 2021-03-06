import telepot
import config

token = config.telegram_config["token"]

def send_notification(selected_ambulance,data):
    msg = form_message(selected_ambulance,data)
    receiver_ids = config.telegram_config["reciever_ids"]
    
    for receiver_id in receiver_ids:
        bot = telepot.Bot(token)
        bot.sendMessage(receiver_id,msg)

def form_message(selected_ambulance,data):
    pickup_location_latitude = data["user_session_variables"]["pickup_location"]["latitude"]
    pickup_location_longitude = data["user_session_variables"]["pickup_location"]["longitude"]
    username = data["bybrisk_session_variables"]["username"]
    phone = data["bybrisk_session_variables"]["phone"]
    ambulance_id_and_number = selected_ambulance[0] + " ("+selected_ambulance[1]+")"
    captain_name = selected_ambulance[2]
    captain_phone = selected_ambulance[3]
    
    mapLink = "https://www.google.com/maps/dir/?api=1&destination=" + str(pickup_location_latitude) + "," + str(pickup_location_longitude)

    msg = "ššØšØš¤š¢š§š  ššØš« - "+ambulance_id_and_number+"\n\nššš©š­šš¢š§ š§šš¦š: "+captain_name+"\nššš©š­šš¢š§ š©š”šØš§š: "+captain_phone+"\n\nšš¬šš« š§šš¦š: "+username+"\nšš¬šš« š©š”šØš§š: "+phone+"\n\nšššÆš¢š šš­š -"+mapLink  

    return msg          