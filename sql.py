import mysql.connector
import uuid
import config

mydb = mysql.connector.connect(
  host=config.mysql_config["host"],
  user=config.mysql_config["user"],
  password=config.mysql_config["password"],
  database=config.mysql_config["db"]
)

def get_ambulance_data():
  mydb.reconnect()
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM med_alert_ambulance_details;")
  myresult = mycursor.fetchall()
  mydb.commit()
  print("[DB TOUCH] fetched ambulance details")
  return myresult

def get_booking_history(user_id, user_name):
  mydb.reconnect()
  mycursor = mydb.cursor()
  mycursor.execute("SELECT med_alert_ambulance_details.*,med_alert_booking_detail.* FROM med_alert_ambulance_details INNER JOIN med_alert_booking_detail ON med_alert_ambulance_details.id=med_alert_booking_detail.ambulance_id where med_alert_booking_detail.user_id='"+user_id+"' order by med_alert_booking_detail.date_created desc;")
  myresult = mycursor.fetchall()
  mydb.commit()
  print("[DB TOUCH] fetched booking details for user_id: "+user_id+", user_name: "+user_name)
  return myresult  

def update_ambulance_state(state,vehicle_number):
  mydb.reconnect()
  mycursor = mydb.cursor()
  sql = "UPDATE med_alert_ambulance_details SET state = '"+state+"' WHERE vehicle_number = '"+vehicle_number+"'"
  mycursor.execute(sql)
  mydb.commit()
  print("[DB TOUCH] updated status of "+vehicle_number+" to "+state)

def get_available_ambulance(category):
  mydb.reconnect()
  mycursor = mydb.cursor()
  mycursor.execute("select * from med_alert_ambulance_details where state='available' AND ambulance_type_tag='"+category+"';")
  myresult = mycursor.fetchall()
  mydb.commit()
  print("[DB TOUCH] fetched available ambulances")
  return myresult

def get_ambulance_by_id(ambulance_id):
  mydb.reconnect()
  mycursor = mydb.cursor()
  mycursor.execute("select * from med_alert_ambulance_details where id='"+ambulance_id+"';")
  myresult = mycursor.fetchall()
  mydb.commit()
  print("[DB TOUCH] fetched ambulances with id: "+ambulance_id)
  return myresult

def get_available_ambulance_category():
  mydb.reconnect()
  mycursor = mydb.cursor()
  mycursor.execute("select DISTINCT(ambulance_type_tag) from med_alert_ambulance_details where state='available';")
  myresult = mycursor.fetchall()
  mydb.commit()
  print("[DB TOUCH] fetched get_available_ambulance_category")
  return myresult

def store_ambulance_booking(userId,ambulanceID,lat,long,pickupAddr):
  mydb.reconnect()
  mycursor = mydb.cursor()
  sql = "INSERT INTO med_alert_booking_detail (user_id,ambulance_id,latitude,longitude,address) values ('"+userId+"','"+ambulanceID+"','"+str(lat)+"','"+str(long)+"','"+pickupAddr+"');"
  mycursor.execute(sql)
  mydb.commit()
  print("[DB TOUCH] Added store_ambulance_booking of "+ambulanceID+" for "+userId+" @ "+pickupAddr)
