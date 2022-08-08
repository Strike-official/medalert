import python_sdk.strike as strike #For timebeing, strike is a private library. Has to be downloaded into the local from https://github.com/Strike-official/python-sdk 
import config
import flask
import requests
from flask import jsonify
from flask import request
import sql
import constants
import helper
import telegram
import call

app = flask.Flask(__name__)
app.config["DEBUG"] = True


baseAPI=config.baseAPI

#########################################
######## Ambulance booking bot action handler #######
#########################################

@app.route('/medalertBot/ambulance/get/location', methods=['POST'])
def get_location_for_booking():
    strikeObj = strike.Create("book_ambulance",baseAPI+"/medalertBot/ambulance/book")
    quesObj1 = strikeObj.Question("pickup_address").\
                QuestionText().\
                SetTextToQuestion("Please enter your address?")
    quesObj1.Answer(False).TextInput()

    quesObj2 = strikeObj.Question("pickup_location").\
                QuestionText().\
                SetTextToQuestion("What's your location?")
    quesObj2.Answer(False).LocationInput("Select location here")

    return jsonify(strikeObj.Data())

@app.route('/medalertBot/ambulance/book', methods=['POST'])
def send_response():

    data = request.get_json()

    ## Check for available ambulances
    available_ambulances = sql.get_available_ambulance()
    print(available_ambulances)

    strikeObj = strike.Create("getting_started", baseAPI+"/medalertBot/ambulance/get/location")

    if helper.is_ambulance_available(available_ambulances):
        selected_ambulance = helper.get_ambulace(available_ambulances)

        ## Update status of ambulance to unavailable
        sql.update_ambulance_state(constants.unavailable_state,selected_ambulance[1])

        ## Push to telegram
        telegram.send_notification(selected_ambulance,data)
    
        ## Send a call notification
        call.call_notification(selected_ambulance[3], data["bybrisk_session_variables"]["phone"])

        ## Send response to user
        question_card = strikeObj.Question("last_leg").\
            QuestionCard().\
            SetHeaderToQuestion(2,strike.HALF_WIDTH).\
            AddTextRowToQuestion(strike.H4,"Your ambulance is on it's way",constants.available_color,True).\
            AddTextRowToQuestion(strike.H4,"Ambulance no. - "+selected_ambulance[1]+" ",constants.plain_text_color,False).\
            AddTextRowToQuestion(strike.H4,"Contact no. - "+config.calling_service['to_number'],constants.plain_text_color,False)

        answer_card = question_card.Answer(False).AnswerCardArray(strike.VERTICAL_ORIENTATION)
        answer_card = answer_card.AnswerCard().\
            SetHeaderToAnswer(1,strike.HALF_WIDTH).\
            AddTextRowToAnswer(strike.H4,constants.back_handler,"Black",True)   

    else:
        question_card = strikeObj.Question("last_leg").\
            QuestionCard().\
            SetHeaderToQuestion(2,strike.HALF_WIDTH).\
            AddTextRowToQuestion(strike.H4,"Sorry! all of our ambulances are busy at this moment.",constants.sorry_color,True)

        answer_card = question_card.Answer(False).AnswerCardArray(strike.VERTICAL_ORIENTATION)
        answer_card = answer_card.AnswerCard().\
            SetHeaderToAnswer(1,strike.HALF_WIDTH).\
            AddTextRowToAnswer(strike.H4,constants.back_handler,"Black",True)

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

@app.route('/medalertBot/history', methods=['POST'])
def show_history():
    data = request.get_json()
    name=data["bybrisk_session_variables"]["username"]
    user_id=data["bybrisk_session_variables"]["userId"]

    ## Get user booking history
    ambulance_details = sql.get_booking_history(user_id,name)
    
    strikeObj = strike.Create("getting_started", baseAPI)

    question_card = strikeObj.Question("").\
                QuestionText().\
                SetTextToQuestion("Hi! " + name + " below is your ambulance booking history")

    answer_card = question_card.Answer(False).AnswerCardArray(strike.VERTICAL_ORIENTATION)

    for ambulance_detail in ambulance_details:
        answer_card = answer_card.AnswerCard().\
            SetHeaderToAnswer(10,strike.HALF_WIDTH).\
            AddTextRowToAnswer(strike.H4,"Driver Name: "+ambulance_detail[2],"Black",True).\
            AddTextRowToAnswer(strike.H4,ambulance_detail[3],"#4839bd",False).\
            AddTextRowToAnswer(strike.H4,"Vehicle No. "+ambulance_detail[1],"Black",False).\
            AddTextRowToAnswer(strike.H5,"Booked on. "+str(ambulance_detail[13]),"#687987",False)

    return jsonify(strikeObj.Data())

#########################################
######## Admin bot action handler #######
#########################################

## get_ambulance_data fetches the ambulace data and its stauts
@app.route('/medalertBotAdmin/ambulance/get/all', methods=['POST'])
def get_ambulance_data():
    data = request.get_json()
    user_phone_number = data["bybrisk_session_variables"]["phone"]


    vahicle_number = "NA"

    strikeObj = strike.Create("manage_ambulance", baseAPI+"/medalertBotAdmin/ambulance/set/status")
    quesObj1 = strikeObj.Question("ambulance_id_and_number").QuestionText().SetTextToQuestion("Which ambulance to manage?")
    
    ambulances_data = sql.get_ambulance_data()

    ambulance_status_color = constants.unavailable_color

    answer_card = quesObj1.Answer(True).AnswerCardArray(strike.VERTICAL_ORIENTATION)
    authorised = False
    for ambulance_data in ambulances_data:

        ## Skip if ambulace state is dead
        if ambulance_data[4] == constants.dead_state:
            continue

        ## Skip if the user is not a superUser or the Driver himself.
        if (user_phone_number not in config.admin_phone_number) and (ambulance_data[3] != user_phone_number):
            print("Unathorised - driverNumber="+ambulance_data[3]+" -UserPhoneNumber="+user_phone_number)
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
        authorised = True
    if not authorised:
        answer_card = answer_card.AnswerCard().\
                SetHeaderToAnswer(1,strike.HALF_WIDTH).\
                AddTextRowToAnswer(strike.H3,"You are not authorised to perform this operation.","#ff3333",True)
        # If unauthorised, Reset nextHandlerURL such that this is the last message.
        strikeObj.meta_response_object["body"]["nextActionHandlerURL"]=""
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
    sql.update_ambulance_state(ambulance_state,vehicle_number)

    strikeObj = strike.Create("getting_started", baseAPI+"/medalertBotAdmin/ambulance/get/all")
    quesObj1 = strikeObj.Question("response").QuestionText().SetTextToQuestion("Status of " + ambulance_id + "(" + vehicle_number + ") updated to " + ambulance_state)

    answer_card = quesObj1.Answer(False).AnswerCardArray(strike.VERTICAL_ORIENTATION)
    answer_card = answer_card.AnswerCard().\
            SetHeaderToAnswer(1,strike.HALF_WIDTH).\
            AddTextRowToAnswer(strike.H4,constants.back_handler,"Black",True)
    
    return jsonify(strikeObj.Data())

app.run(host='0.0.0.0', port=config.port)