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

# set pins to that of the board
GPIO.setmode(GPIO.BOARD)

# set pin 11 as input for motion sensor
GPIO.setup(11,GPIO.IN)
# set pin 3 as output for LED
GPIO.setup(3,GPIO.OUT)

# set the control pins for the stepper motor
control_pins = [31,33,35,37]
for pin in control_pins:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, 0)

# This block will read the motion sensor and print "Nope" to the terminal if no
# motion is detected and "Yes" if there is motion while also turning on an LED
while True:
    i=GPIO.input(11)
    if i==0:
        print "Nope",i
        time.sleep(1)
    elif i==1:
        print "Yes",i
        GPIO.output(3,1)

# If motion is detected the following mototr sequence will begin to dispense a
# treat
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

# all motor pins are turned off once a treat is dispensed
	for pin in control_pins:
               GPIO.setup(pin, GPIO.OUT)
               GPIO.output(pin, 0)

# The camera will then turn on and record a 10 second video with a preview
        camera.start_preview()
        camera.start_recording('/home/pi/Desktop/Treat/video.h264')
        sleep(10)
        camera.stop_recording()
        camera.stop_preview()

# The Pi will then notify the phone number entered in the "to" section with the
# body message
	account_sid = 'ACb9dab907e5aca735ea665f370251adb8'
	auth_token = 'a1b4a34038512fe2569f0504710bf947'
	client = Client(account_sid, auth_token)
        message = client.messages \
                .create(
                     body="Your pet just got a treat!",
                     from_='+15023736897',
                     to='+15024925427'
                 )

# The message ID is then printed to the terminal
	print(message.sid)

# The sequence to send an email of the video begins below is the set accounts
	email_user = 'TreatDispenser305@gmail.com'
	email_password = 'Treats305'
	email_send = 'tlr.nichols@gmail.com'

	subject = 'Treat Time!'

	msg = MIMEMultipart()
	msg['From'] = email_user
	msg['To'] = email_send
	msg['Subject'] = subject

# Sets body of email and video attachments
	body = 'Hi there, your pet just got a treat!'
	msg.attach(MIMEText(body,'plain'))

	filename='/home/pi/Desktop/Treat/video.h264'
	attachment  =open(filename,'rb')

# The following 2 blocks builds the email
	part = MIMEBase('application','octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition',"attachment; filename= "+filename)

	msg.attach(part)
	text = msg.as_string()
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.starttls()
	server.login(email_user,email_password)

# This block sends the email
	server.sendmail(email_user,email_send,text)
        server.quit()

# Turns LED off
	GPIO.output(3,0)

# Dispenser waits 10 seconds before dispensing again
        time.sleep(10)
