import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from time import sleep
from twilio.rest import Client
import Text
import myemail2
from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

camera = PiCamera()

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11,GPIO.IN)
GPIO.setup(3,GPIO.OUT)

control_pins = [31,33,35,37]

for pin in control_pins:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, 0)
	
while True:
    i=GPIO.input(11)
    if i==0:
        print "Nope",i
        time.sleep(1)
    elif i==1:
        print "Yes",i
        GPIO.output(3,1)

        halfstep_seq = [
                [1,0,0,0],
                [1,1,0,0],
                [0,1,0,0],
                [0,1,1,0],
                [0,0,1,0],
                [0,0,1,1],
                [0,0,0,1],
                [1,0,0,1]
        ]        

        for i in range(512):
                for halfstep in range(8):
                        for pin in range(4):
                                GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
                        time.sleep(0.001)
	
	for pin in control_pins:
               GPIO.setup(pin, GPIO.OUT)
               GPIO.output(pin, 0)

        camera.start_preview()
        camera.start_recording('/home/pi/Desktop/Treat/video.h264')
        sleep(10)
        camera.stop_recording()
        camera.stop_preview()
                
	account_sid = 'ACb9dab907e5aca735ea665f370251adb8'
	auth_token = 'a1b4a34038512fe2569f0504710bf947'
	client = Client(account_sid, auth_token)
        message = client.messages \
                .create(
                     body="Your pet just got a treat!",
                     from_='+15023736897',
                     to='+15024925427'
                 )

	print(message.sid)
	
	email_user = 'TreatDispenser305@gmail.com'
	email_password = 'Treats305'
	email_send = 'tlr.nichols@gmail.com'

	subject = 'Treat Time!'

	msg = MIMEMultipart()
	msg['From'] = email_user
	msg['To'] = email_send
	msg['Subject'] = subject

	body = 'Hi there, your pet just got a treat!'
	msg.attach(MIMEText(body,'plain'))                
	
	filename='/home/pi/Desktop/Treat/video.h264'
	attachment  =open(filename,'rb')

	part = MIMEBase('application','octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition',"attachment; filename= "+filename)
	
	msg.attach(part)
	text = msg.as_string()
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.starttls()
	server.login(email_user,email_password)
	
	server.sendmail(email_user,email_send,text)
        server.quit()
        
	GPIO.output(3,0)
        
        time.sleep(10)
                
