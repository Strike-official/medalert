import strike

## Create a strike object
strikeObj = strike.Create("SHASHANK","http://www.fb.com")

## Create a question card interface
question_card = strikeObj.Question("key1").\
            QuestionCard().\
            SetHeaderToQuestion(2,strike.HALF_WIDTH).\
            AddGraphicRowToQuestion(strike.PICTURE_ROW,["http://www.pop.com","http://valti.com"],["http://www.pop.com.tbn","http://valti.com.tbn"]).\
            AddGraphicRowToQuestion(strike.VIDEO_ROW,["http://www.pop.com","http://valti.com"],["http://www.pop.com.tbn","http://valti.com.tbn"]).\
            AddTextRowToQuestion(strike.H1,"some testing done here","blue",True)
            
## Create a answer card interface            
answer_card = question_card.Answer(True).\
            AnswerCardArray(strike.HORIZONTAL_ORIENTATION).\
            AnswerCard().\
            SetHeaderToAnswer(1,strike.HORIZONTAL_ORIENTATION).\
            AddGraphicRowToAnswer(strike.VIDEO_ROW,["http://www.pop.com","http://valti.com"],["http://www.pop.com.tbn","http://valti.com.tbn"])

## Create a question text interface
question_text = strikeObj.Question("key2").\
QuestionText().\
SetTextToQuestion("Welocme! to strike dev community")

## Create a text input interface
text_input = question_text.Answer(False).TextInput()

question_text_for_location = strikeObj.Question("key3").\
QuestionText().\
SetTextToQuestion("below we ask for the location")

## Create a location input
location_input = question_text_for_location.Answer(False).LocationInput("Select your location?")

question_text_for_number = strikeObj.Question("key4").\
QuestionText().\
SetTextToQuestion("below we ask for the number")

## Create a location input
number_input = question_text_for_number.Answer(False).NumberInput()

question_text_for_date = strikeObj.Question("key5").\
QuestionText().\
SetTextToQuestion("below we ask for the date")

## Create a date input
date_input = question_text_for_date.Answer(False).DateInput()

print(strikeObj.ToJson())