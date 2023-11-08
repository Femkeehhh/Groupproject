import time
from fhict_cb_01.custom_telemetrix import CustomTelemetrix
import requests

board = CustomTelemetrix()
latestData = None
BUZZER = 3
x = 0
y = 0
clock = [0 , 0 , 1, 6]
bluePin = 6
greenPin = 5
yellowPin = 7
buttonPin = 9
button2Pin = 8  
display = ""
counter = 0
timeList = ["0030"]
emptyList = []
loopRun = 0
orderReady = False
check = None

def buzzerON():
     global orderReady
     orderReady = True
     global BUZZER
     board.analog_write(BUZZER,225)
     
def buzzerOFF():
     global orderReady
     orderReady = False
     global BUZZER
     board.analog_write(BUZZER,0)
def timeFunc(clock):

    if(clock[1] == 0 and clock[2] == 0 and clock[3] == 0):
         clock[0] -= 1
         clock[1] = 10
         
         
    if(clock[2] == 0 and clock[3] == 0):
         clock[1] -= 1
         clock[2] = 6
         
    if(clock[3] == 0):
         clock[2] -= 1
         clock[3] = 10

    clock[3] -= 1
    display = "".join(map(str, clock))
    time.sleep(0.9)
    return display

def time_system(pizzaList):
     global emptyList
     counter = 0 
     for pizza in pizzaList:
          clock = [int(integer)for integer in pizza]
          if(clock[1] == 0 and clock[2] == 0 and clock[3] == 0):
               clock[0] -= 1
               clock[1] = 10
         
         
          if(clock[2] == 0 and clock[3] == 0):
               clock[1] -= 1
               clock[2] = 6
         
          if(clock[3] == 0):
               clock[2] -= 1
               clock[3] = 10

          clock[3] -= 1
          display = "".join(map(str, clock))
          if(counter > len(emptyList)):
               emptyList.append(display)
          else:
               if(counter == len(emptyList)):
                    emptyList.append(display)
                    counter += 1
               else:
                    emptyList[counter] = display
                    counter += 1    


 
def setup():
       board.set_pin_mode_digital_input_pullup(buttonPin)
       board.set_pin_mode_digital_input_pullup(button2Pin)
       board.set_pin_mode_digital_output(greenPin)
       board.set_pin_mode_digital_output(yellowPin)
       board.set_pin_mode_digital_output(bluePin)
       board.set_pin_mode_analog_output(BUZZER)
       time.sleep(0.01)
       print("setup")


def loop(data):
     global clock
     global counter
     global display
     global timeList
     global emptyList
     global loopRun
     global latestData
     global check

     global orderReady 
     #orderReady = False
     latestData = {"Order status" : orderReady}

     time.sleep(0.1)
     buttonState = board.digital_read(buttonPin)
     if(buttonState[0]== 0):
          counter += 1
     if(counter > 0):
          time_system(data)
          board.displayShow(emptyList[0])

          #display = timeFunc(data)
          #board.displayShow(display)
          board.digital_write(bluePin,0)
          board.digital_write(yellowPin,1)
          time.sleep(0.9)
          counter2 = 0
          for i in timeList:
               timeList[counter2] = emptyList[counter2]
               counter2 += 1
               counter2 = int(counter2)
     if emptyList != []:
          if(emptyList[0]== "0000"):
               board.digital_write(yellowPin,0)
               board.digital_write(greenPin,1)
               #buzzerON()
               orderReady = True
               latestData = orderReady
               #latestData = {"Order status" : orderReady}
               check = True
               time.sleep(1.5)
               buzzerOFF()
               board.digital_write(greenPin,0)
               emptyList.remove(emptyList[0])
               timeList.remove(timeList[0])
               

               if emptyList == []:
                    loopRun = None
   
setup()
while True:
    try:
          if(check != None):
                if latestData != None:
                    data = {"orderReady": latestData}
                    request = requests.post("http://127.0.0.1:5000/order_ready", json = data)
                    print(latestData)
                    orderReady = False
                    latestData = orderReady
                    #latestData = {"Order status" : orderReady}
                    check = None

          buttonState = board.digital_read(button2Pin)
          buttonState2 = board.digital_read(buttonPin)
          if buttonState != None:
               if(buttonState[0]== 0):
                    x += 1
          if buttonState2 != None:
               if(buttonState2[0]== 0):
                    y += 1
          if(y > 0):
               board.displayOff()
               board.shutdown()
          if(x > 0):
               timeList.append("0030")
               if latestData != None:
                    print(latestData)
                    orderReady = False
                    request = requests.post("http://127.0.0.1:5000/order_preparing", json = latestData)
               board.digital_write(bluePin,1)
               x = 0
               loopRun = 0
          if(loopRun != None):
               loop(timeList)
          #if latestData != None:
               #request = requests.post("http://127.0.0.1:5000/post_data", json = latestData)
         
    except KeyboardInterrupt:
        board.shutdown()
