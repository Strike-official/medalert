import random

def is_ambulance_available(ambulance_detail_array):
    if len(ambulance_detail_array) > 0:
        return True
    return False    

def get_ambulace(ambulance_detail_array):
    index = random.randint(0,len(ambulance_detail_array)-1)
    return ambulance_detail_array[index]
