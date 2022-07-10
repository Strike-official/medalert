import json


HALF_WIDTH="HALF"
FULL_WIDTH="FULL"
PICTURE_ROW="pic_row"
VIDEO_ROW="video_row"
HORIZONTAL_ORIENTATION="HORIZONTAL"
VERTICAL_ORIENTATION="VERTICAL"
H1 = "h1"
H2 = "h2"
H3 = "h3"
H4 = "h4"
H5 = "h5"
H6 = "h6"

class Create:

    def __init__(self,actionHandler,nextActionHandler):
        self.meta_response_object = {
            "status":200,
            "body":{
                "actionHandler" : actionHandler,
                "nextActionHandlerURL" : nextActionHandler,
                "questionArray": []
            }
        }

        #import the different modules
        # from .stub import Question,Answer

## Stub
    def Question(self,qContext):
        self.meta_response_object["body"]["questionArray"].append(
            {
                "question":{
                    "qContext":qContext
                }
            })  
        return self 

    def Answer(self,multiple_select):
        self.meta_response_object["body"]["questionArray"][len(self.meta_response_object["body"]["questionArray"])-1].update(
                answer={
                    "multipleSelect":multiple_select
                }
        )

        return self    

## Question Card interface
    def QuestionCard(self):  
        self.meta_response_object["body"]["questionArray"][len(self.meta_response_object["body"]["questionArray"])-1]["question"].update(
            questionType="Card"
        )  
        return self

    def SetHeaderToQuestion(self,context_index,width):
        self.meta_response_object["body"]["questionArray"][len(self.meta_response_object["body"]["questionArray"])-1]["question"].update(
            qCard=[
                {
                    "type":"header",
                    "descriptor":{
                        "context-object":context_index,
                        "card-type":width
                    }
                }
            ]
        ) 

        return self

    def AddGraphicRowToQuestion(self,graphic_type,url,thumbnail_url):
        self.meta_response_object["body"]["questionArray"][len(self.meta_response_object["body"]["questionArray"])-1]["question"]["qCard"].append(
            {"type":graphic_type,
             "descriptor":{
                "value":url,
                "thumbnail":thumbnail_url
            }
            }
        )            
        return self

    def AddTextRowToQuestion(self,row_type,value,color,bold):
        self.meta_response_object["body"]["questionArray"][len(self.meta_response_object["body"]["questionArray"])-1]["question"]["qCard"].append(
            {"type":row_type,
             "descriptor":{
                "value":[value],
                "color":color,
                "bold":bold
            }
            }
        )
        return self


    
## Answer Card interface    
    def AnswerCardArray(self,card_orientation):
        multipleSelectVal = self.meta_response_object["body"]["questionArray"][len(self.meta_response_object["body"]["questionArray"])-1]["answer"]["multipleSelect"]
        
        self.meta_response_object["body"]["questionArray"][len(self.meta_response_object["body"]["questionArray"])-1].update(
            answer={
                    "multipleSelect":multipleSelectVal,
                    "card-orientation":card_orientation,
                    "responseType":"Card",
                    "qCard":[]
                }
        )

        return self       
    
    def AnswerCard(self):

        self.meta_response_object["body"]["questionArray"][len(self.meta_response_object["body"]["questionArray"])-1]["answer"]["qCard"].append(
            []
        )

        return self 

    def SetHeaderToAnswer(self,card_context,width):

        q_card_array = self.meta_response_object["body"]["questionArray"][len(self.meta_response_object["body"]["questionArray"])-1]["answer"]["qCard"]
        self.meta_response_object["body"]["questionArray"][len(self.meta_response_object["body"]["questionArray"])-1]["answer"]["qCard"][len(q_card_array)-1].append(
            {   
                "type":"header",
                "descriptor":{
                    "context-object":card_context,
                    "card-type":width
                }
            }
        )

        return self

    def AddGraphicRowToAnswer(self,graphic_type,url,thumbnail_url):

        q_card_array = self.meta_response_object["body"]["questionArray"][len(self.meta_response_object["body"]["questionArray"])-1]["answer"]["qCard"]
        self.meta_response_object["body"]["questionArray"][len(self.meta_response_object["body"]["questionArray"])-1]["answer"]["qCard"][len(q_card_array)-1].append(
            {   
                "type":graphic_type,
                "descriptor":{
                    "value":url,
                    "thumbnail":thumbnail_url
                }
            }
        )

        return self 

    def AddTextRowToAnswer(self,row_type,value,color,bold):
        q_card_array = self.meta_response_object["body"]["questionArray"][len(self.meta_response_object["body"]["questionArray"])-1]["answer"]["qCard"]

        self.meta_response_object["body"]["questionArray"][len(self.meta_response_object["body"]["questionArray"])-1]["answer"]["qCard"][len(q_card_array)-1].append(
            {"type":row_type,
             "descriptor":{
                "value":[value],
                "color":color,
                "bold":bold
            }
            }
        )
        return self

## Text Interface
    def QuestionText(self):  
        self.meta_response_object["body"]["questionArray"][len(self.meta_response_object["body"]["questionArray"])-1]["question"].update(
            questionType="Text"
        )  
        return self   

    def SetTextToQuestion(self,question_text):
        self.meta_response_object["body"]["questionArray"][len(self.meta_response_object["body"]["questionArray"])-1]["question"].update(
            qText=question_text
        )
        return self

## Text Input interface
    def TextInput(self):    
        self.meta_response_object["body"]["questionArray"][len(self.meta_response_object["body"]["questionArray"])-1].update(
            answer={
                    "responseType":"Text-Input"
                }
        )

        return self

## Location Input interface        
    def LocationInput(self,location_input_text):  
        self.meta_response_object["body"]["questionArray"][len(self.meta_response_object["body"]["questionArray"])-1].update(
            answer={
                    "responseType":"Location-Input",
                    "qLocation-Input": [location_input_text] 
                }
        )

        return self

## Number Input interface        
    def NumberInput(self):  
        self.meta_response_object["body"]["questionArray"][len(self.meta_response_object["body"]["questionArray"])-1].update(
            answer={
                    "responseType":"Number-Input"
                }
        )

        return self

## Date Input interface        
    def DateInput(self):  
        self.meta_response_object["body"]["questionArray"][len(self.meta_response_object["body"]["questionArray"])-1].update(
            answer={
                    "responseType":"Date-Input"
                }
        )

        return self

    def Data(self):
        data = vars(self)["meta_response_object"]
        return data

    def ToJson(self):
        json_data = json.dumps(vars(self)["meta_response_object"])
        return json_data

     