#!/usr/bin/python3
#!/usr/bin/python3

import time
import os
from pyfingerprint.pyfingerprint import PyFingerprint
import RPi.GPIO as GPIO

# Configurer les broches pour les LEDs
LED_GREEN = 16
LED_RED = 18
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_GREEN, GPIO.OUT)
GPIO.setup(LED_RED, GPIO.OUT)

# Chemin d'enregistrement de l'image de l'empreinte digitale
OUTPUT_IMG_PATH = "/home/pi/my_images/fingerprint_{}.bmp".format(time.strftime("%Y%m%d-%H%M%S"))

# Initialiser le capteur d'empreintes digitales
try:
    sensor = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)
    if sensor.verifyPassword() == False:
        raise ValueError('Le capteur d\'empreintes digitales est protégé par un mot de passe!')
except Exception as e:
    print('Le capteur d\'empreintes digitales n\'a pas pu être initialisé!')
    print('Message d\'erreur: {}'.format(e))
    exit(1)

# Afficher le nombre d'empreintes digitales actuellement stockées dans le capteur
print('Empreintes digitales stockées: {}/{}'.format(sensor.getTemplateCount(), sensor.getStorageCapacity()))

# Boucle infinie de capture d'empreinte digitale
while True:
    try:
        print('En attente d\'une empreinte digitale...')

        # Attendre que le capteur lise l'empreinte digitale comme une image
        while sensor.readImage() == False:
            print('Aucune empreinte digitale détectée. En attente...')
            time.sleep(2)

        print('Empreinte digitale détectée. Téléchargement de l\'image...')

        # Télécharger l'image de l'empreinte digitale sur le système de fichiers
        sensor.downloadImage(OUTPUT_IMG_PATH)

        # Allumer la LED verte pour indiquer que la capture a réussi
        GPIO.output(LED_GREEN, GPIO.HIGH)
        GPIO.output(LED_RED, GPIO.LOW)

        print('L\'image a été enregistrée sous "{}".'.format(OUTPUT_IMG_PATH))

    except Exception as e:
        # Allumer la LED rouge pour indiquer que la capture a échoué
        GPIO.output(LED_GREEN, GPIO.LOW)
        GPIO.output(LED_RED, GPIO.HIGH)

        print('La capture a échoué!')
        print('Message d\'erreur: {}'.format(e))

        # Attendre avant de recommencer la capture
        time.sleep(2)

    # Attendre avant de recommencer la capture
    time.sleep(2)

# Nettoyer les broches de la LED et libérer le capteur d'empreintes digitales
GPIO.cleanup()
sensor = None


"""
    This script allow for capturing and saving on computer the raw image of a fingerprint.

import time
import sys, os
from pyfingerprint.pyfingerprint import PyFingerprint





if len(sys.argv) < 2 :
    help()
OUTPUT_IMG_PATH = "/home/pi/my_images/fingerprint_{}.bmp".format(time.strftime("%Y%m%d-%H%M%S"))
#OUTPUT_IMG_PATH = sys.argv[1]

## Tries to initialize the sensor
try:
    sensor = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)

    if sensor.verifyPassword() == False :
        raise ValueError('The fingerprint sensor is protected by password!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: {}'.format(e))
    exit(1)

## Gets info about how many fingerprint are currently stored
print('Currently stored fingers: {}/{}'.format(sensor.getTemplateCount(), sensor.getStorageCapacity()))

while True :
## Tries to search the finger and calculate hash
    try:
        print('Waiting for finger...')
    
    ## Wait for finger to be read as an image
        while sensor.readImage() == False :
            # Set the LED color to green when recognition is in progress
            sensor.setLED(0x00FF00, 1)

    # Do fingerprint recognition here

    # Set the LED color back to red when waiting for a finger again
            sensor.setLED(0xFF0000, 1)
            print('No finger detected. Waiting...')
            time.sleep(10)
        print('Finger detected. Downloading image...')

        print('Downloading image (this may take a while)...')
      
        sensor.downloadImage(OUTPUT_IMG_PATH)

        print('The image have been saved to "{}".'.format(OUTPUT_IMG_PATH))
       

    except Exception as e:
         print('Operation failed!')
         print('Exception message: {}'.format(str(e)))
         exit(1)
"""