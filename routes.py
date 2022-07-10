import python_sdk.strike as strike #For timebeing, strike is a private library. Has to be downloaded into the local from https://github.com/Strike-official/python-sdk 
import config
import flask
import requests
from flask import jsonify
from flask import request
import sql
import constants

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# The public API link of the hosted server has to be added here.
# Use ngrok to easily make your api public
baseAPI=config.baseAPI
# hospital_data=sql.get_hospital_data()

@app.route('/medalertBot/book/get/location', methods=['POST'])
def book_get_location():
    ## Create a strike object
    strikeObj = strike.Create("getting_started",baseAPI+"/medalertBot/book/get/hospitals")


    # First Question: Whats your name?
    quesObj1 = strikeObj.Question("start_location").\
                QuestionText().\
                SetTextToQuestion("What's your location?")
    quesObj1.Answer(False).LocationInput("Select location here")

    return jsonify(strikeObj.Data())

@app.route('/medalertBot/book/get/hospitals', methods=['POST'])
def book_get_hospital():

    data = request.get_json()
    latitude=data["bybrisk_session_variables"]["location"]["latitude"]
    longitude=data["bybrisk_session_variables"]["location"]["longitude"]
    print(latitude)
    print(longitude)

    print(hospital_data)
    ## Create a strike object
    strikeObj = strike.Create("getting_started",baseAPI+"/respondBack")


    # Get data of all the hospitals found in 5km radius of the user
    quesObj1 = strikeObj.Question("hospital_id").QuestionText().SetTextToQuestion("Select a hospital")
    
    answer_card = quesObj1.Answer(True).AnswerCardArray(strike.VERTICAL_ORIENTATION)
    for i in hospital_data:
        answer_card = answer_card.AnswerCard().\
            SetHeaderToAnswer(1,strike.FULL_WIDTH).\
            AddTextRowToAnswer(strike.H4,i[1],"Black",True).\
            AddTextRowToAnswer(strike.H5,i[5],"#757574",False).\
            AddTextRowToAnswer(strike.H5,"📍 "+i[2],"black",False).\
            AddTextRowToAnswer(strike.H5,i[7],"black",False).\
            AddTextRowToAnswer(strike.H4,"22 min","#d93025",True).\
            AddTextRowToAnswer(strike.H4,"3.7 km","#70757a",True)

    return jsonify(strikeObj.Data())


@app.route('/respondBack', methods=['POST'])
def respondBack():
    data = request.get_json()
    name=data["user_session_variables"]["name"]
    dob=data["user_session_variables"]["dob"][0]
    
    strikeObj = strike.Create("getting_started", baseAPI)

    question_card = strikeObj.Question("").\
                QuestionText().\
                SetTextToQuestion("Hi! "+name+" You are the choosen few. You are lucky to be born on "+dob+".")

    return jsonify(strikeObj.Data())

#########################################
######## Admin bot action handler #######
#########################################

## get_ambulance_data fetches the ambulace data and its stauts
@app.route('/medalertBotAdmin/ambulance/get/all', methods=['POST'])
def get_ambulance_data():

    vahicle_number = "NA"

    strikeObj = strike.Create("manage_ambulance", baseAPI+"/medalertBotAdmin/ambulance/set/status")
    quesObj1 = strikeObj.Question("ambulance_id_and_number").QuestionText().SetTextToQuestion("Which ambulance to manage?")
    
    ambulances_data = sql.get_ambulance_data()

    ambulance_status_color = constants.unavailable_color

    answer_card = quesObj1.Answer(True).AnswerCardArray(strike.VERTICAL_ORIENTATION)
    for ambulance_data in ambulances_data:

        ## Skip if ambulace state is dead
        if ambulance_data[4] == constants.dead_state:
            continue

        ## Set available sign based on status
        if ambulance_data[4] == constants.available_state:
            ambulance_status_color = constants.available_color
        else:
            ambulance_status_color = constants.unavailable_color

        answer_card = answer_card.AnswerCard().\
                SetHeaderToAnswer(1,strike.HALF_WIDTH).\
                AddTextRowToAnswer(strike.H3,ambulance_data[0]+constants.id_number_delimiter+ambulance_data[1],"Black",True).\
                AddTextRowToAnswer(strike.H4,ambulance_data[4],ambulance_status_color,True).\
                AddTextRowToAnswer(strike.H4,"Driver: "+ambulance_data[2],constants.plain_text_color,False)
    
    return jsonify(strikeObj.Data())

## set_ambulance_status sets the status of the ambulance to active
@app.route('/medalertBotAdmin/ambulance/set/status', methods=['POST'])
def set_ambulance_status():
    data = request.get_json()
    ambulance_id_and_number = data["user_session_variables"]["ambulance_id_and_number"][0]
    ambulance_id_and_number_array = ambulance_id_and_number.split(constants.id_number_delimiter)
    ambulance_id = ambulance_id_and_number_array[0]
    vehicle_number = ambulance_id_and_number_array[1]

    strikeObj = strike.Create("manage_ambulance", baseAPI+"/medalertBotAdmin/ambulance/response?ambulance_id="+ambulance_id+"&vehicle_number="+vehicle_number)

    quesObj1 = strikeObj.Question("ambulance_status").QuestionText().SetTextToQuestion("What's the satus of "+ambulance_id)
    
    answer_card = quesObj1.Answer(False).AnswerCardArray(strike.VERTICAL_ORIENTATION)
    answer_card = answer_card.AnswerCard().\
            SetHeaderToAnswer(1,strike.HALF_WIDTH).\
            AddTextRowToAnswer(strike.H4,constants.available_status,"Black",True)

    answer_card.AnswerCard().\
            SetHeaderToAnswer(1,strike.HALF_WIDTH).\
            AddTextRowToAnswer(strike.H4,constants.unavailable_status,"Black",True)
    
    return jsonify(strikeObj.Data())


## response_ambulace_status_update responds to the ambulance status update handler 
@app.route('/medalertBotAdmin/ambulance/response', methods=['POST'])
def response_ambulace_status_update():
    ambulance_id = request.args.get('ambulance_id')
    vehicle_number = request.args.get('vehicle_number')
    data = request.get_json()

    ambulance_status = data["user_session_variables"]["ambulance_status"][0]
    if ambulance_status == constants.unavailable_status:
       ambulance_state = constants.unavailable_state
    if ambulance_status == constants.available_status:
       ambulance_state = constants.available_state

    ## Update status of ambulance
    sql.update_ambulance_data(ambulance_state,vehicle_number)

    strikeObj = strike.Create("getting_started", baseAPI+"/medalertBotAdmin/ambulance/get/all")
    quesObj1 = strikeObj.Question("response").QuestionText().SetTextToQuestion("Status of " + ambulance_id + "(" + vehicle_number + ") updated to " + ambulance_state)

    answer_card = quesObj1.Answer(False).AnswerCardArray(strike.VERTICAL_ORIENTATION)
    answer_card = answer_card.AnswerCard().\
            SetHeaderToAnswer(1,strike.HALF_WIDTH).\
            AddTextRowToAnswer(strike.H4,constants.back_handler,"Black",True)
    
    return jsonify(strikeObj.Data())

app.run(host='0.0.0.0', port=5001)