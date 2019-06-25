import serial
from requests import post
from time import sleep


while(1):
    x = ''
    ser = serial.Serial("/dev/ttyACM0")

    x = ser.readline().strip().decode("utf-8")
    print ('Tentativo da: ', x)

    # p = post('http://localhost:8080/api/v0.1/accesso', json={'codice':x})
    p = post('http://progetto-iot2.appspot.com/api/v0.1/accesso', json={'codice':x})
    # sleep(1) # Time in seconds

    j = p.json()
    print(j)

    if len(j)>1:
        nome = bytes(j['nome']+'\n', 'utf-8')
        cognome = bytes(j['cognome']+'\n', 'utf-8')
        message = bytes(j['message']+'\n', 'utf-8')
        
        ser.write(nome)
        ser.write(cognome)
        ser.write(message)

    else:
        message = bytes(j['message']+'\n', 'utf-8')

        ser.write(message)
    
    sleep(1) # Time in seconds

    ser.close()