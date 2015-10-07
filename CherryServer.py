import cherrypy, os, os.path, string, time, json, threading
from SimpleMail import Mail
from datetime import datetime
import RPi.GPIO as GPIO


class PiServer(object):
    def __init__(self,door, **kwargs):
        '''Server applicaiton holds door object'''

        self.door = door
        cherrypy.engine.subscribe(channel = 'stop', callback= self.__stop)

    def __stop(self):
        self.door.monitor = False


    @cherrypy.expose
    def index(self):
        return open('index.html')

    #This GET method is polled to check the status of the door, if opened or closed
    @cherrypy.expose
    def doorStatus(self):
        return str(self.door.state)
    #Action to open or close the door
    @cherrypy.expose
    def doorAction(self, state):
        if state == "True":
            self.door.open()
        if state == "False":
            self.door.close()

        return str(self.door.state)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def doorLog(self):
        '''Returns the in memory copy of times the door was opened'''

        log = [self.door.time_open, self.door.time_closed]
        return log



class Door(object):
    def __init__(self,config, **kwargs):

        self.mailer = Mail(config)
        #True the door is open, False it's closed
        self.state = False
        #List of times the door was opened and closed
        self.time_open = []
        self.time_closed = []

        #Input pins for door
        self.DOOR_PIN = config['doorPin']
        self.RELAY_PIN = config['relayPin']



        #Start the new thread up
        self.monitor = True
        self.monitor_thread = threading.Thread(target=self.__monitor_door)
        #self.monitor_thread.setDaemon(True)
        self.monitor_thread.start()






    def __monitor_door(self):
        '''Monitors the state of the door every second'''

        GPIO.cleanup()
          #Set GPIO board up to use basic numbering
        GPIO.setmode(GPIO.BOARD)
        #Set as input PIN with pull up resistor sense this is just a switch
        GPIO.setup(self.DOOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #Setup for relay
        GPIO.setup(self.RELAY_PIN,GPIO.OUT)

        print("I'm another thread")
        while self.monitor:
           if GPIO.input(self.DOOR_PIN):
              #Door is open
              if not self.state:
                  self.state = True
                  self.time_open.append(datetime.now())
                 # self.mailer.send("Door is open", "Door monitor")
                  print("Door open")
           else:
               #The door is closed
               if self.state:
                   self.state = False
                   self.time_closed.append(datetime.now())
                   print("Door shut")

           time.sleep(1)


    #Open door - my relay is active low so no voltage to input pin cause relay to come on
    def open(self):
        GPIO.output(self.RELAY_PIN, False)
    #Close the door
    def close(self):
        GPIO.output(self.RELAY_PIN,True)





      
       

 # load config
def load():
    with open('config.json') as f:
        return json.load(f)


config = load()
garage_door = Door(config)



 #Start the server
 #This is a blocking call
cherrypy.config.update({'server.socket_host':'157.89.76.117'})
cherrypy.quickstart(PiServer(garage_door))

