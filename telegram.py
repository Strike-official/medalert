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
    pickup_address = data["user_session_variables"]["pickup_address"]
    pickup_location_latitude = data["user_session_variables"]["pickup_location"]["latitude"]
    pickup_location_longitude = data["user_session_variables"]["pickup_location"]["longitude"]
    username = data["bybrisk_session_variables"]["username"]
    phone = data["bybrisk_session_variables"]["phone"]
    ambulance_id_and_number = selected_ambulance[0] + " ("+selected_ambulance[1]+")"
    captain_name = selected_ambulance[2]
    captain_phone = selected_ambulance[3]
    
    mapLink = "https://www.google.com/maps/dir/?api=1&destination=" + str(pickup_location_latitude) + "," + str(pickup_location_longitude)

    msg = "𝐁𝐨𝐨𝐤𝐢𝐧𝐠 𝐟𝐨𝐫 - "+ambulance_id_and_number+"\n\n𝐂𝐚𝐩𝐭𝐚𝐢𝐧 𝐧𝐚𝐦𝐞: "+captain_name+"\n𝐂𝐚𝐩𝐭𝐚𝐢𝐧 𝐩𝐡𝐨𝐧𝐞: "+captain_phone+"\n\n𝐏𝐚𝐭𝐢𝐞𝐧𝐭 𝐧𝐚𝐦𝐞: "+username+"\n𝐏𝐚𝐭𝐢𝐞𝐧𝐭 𝐩𝐡𝐨𝐧𝐞: "+phone+"\n𝐏𝐚𝐭𝐢𝐞𝐧𝐭 𝐀𝐝𝐝𝐫𝐞𝐬𝐬: " + pickup_address + "\n\n𝐍𝐞𝐯𝐢𝐠𝐚𝐭𝐞 -"+mapLink

    return msg          