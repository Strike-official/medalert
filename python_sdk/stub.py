
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