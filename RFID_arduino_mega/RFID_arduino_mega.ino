/* FILE:    RFID_arduino
   DATE:    23/05/2019
   VERSION: 0.1
    
Autore Toppi Andrea

PINOUT:
RC522 MODULE    Uno/Nano /Mega   
SDA             D10     D9
SCK             D13     D52
MOSI            D11     D51
MISO            D12     D50
IRQ             N/A     =
GND             GND     =
RST             D9      8
3.3V            3.3V    =


 collegamenti display
 * LCD RS pin to digital pin 23
 * LCD Enable to digital pin 25
 * LCD D4 pin to digital pin 27
 * LCD D5 pin to digital pin 29
 * LCD D6 pin to digital pin 31
 * LCD D7 pin to digital pin 33
 * LCD R/W pin to ground

 */
 
#include <SPI.h>
#include <MFRC522.h>
#include <EEPROM.h>
#include <LiquidCrystal.h>
/* Vengono definiti PIN del RFID reader*/
#define SDA_DIO 9
#define RESET_DIO 8
#define delayRead 1000 // Time of delay
#define delayLed 500
/* Definizione led di messaggio*/
#define ledRosso 36
#define ledVerde 38
/* Definizione dei PIN dell'LCD*/
#define RS 23
#define Enable 25
#define D4 27
#define D5 29
#define D6 31
#define D7 33
 
/* Viene creata una istanza della RFID libreria */
MFRC522 RC522(SDA_DIO, RESET_DIO); 
LiquidCrystal lcd(RS, Enable, D4, D5, D6, D7);

/* Variabile di stato*/
int stato = 0;
 
void setup()
{ 
  Serial.begin(9600);
  /* Abilita SPI*/
  SPI.begin(); 
  /* Viene inizilizzato RFID reader */
  RC522.PCD_Init();
  
  pinMode(ledVerde,OUTPUT);
  pinMode(ledRosso,OUTPUT);

  lcd.begin(20, 4);
  lcd.setCursor(2, 0);lcd.print("Controllo accessi");
  lcd.setCursor(4, 1);lcd.print("Sviluppato da");
  lcd.setCursor(2, 2);lcd.print("Andrea e Antonio");
  lcd.setCursor(4, 3);lcd.print("Versione 0.1");
}
 
void loop()
{
  byte i;  
  char ser;
  String messaggio, nome, cognome;
  
  switch(stato){
    default:
          // Se viene letta una tessera
          if (RC522.PICC_IsNewCardPresent())
          {
            // Viene letto il suo codice 
            if (!RC522.PICC_ReadCardSerial())
              return;
            String codiceLetto ="";
     
            // Viene caricato il codice della tessera, all'interno di una Stringa
            for(i = 0; i < RC522.uid.size; i++)
             {
              codiceLetto += RC522.uid.uidByte[i] < 0x10 ? "0" : ""; // operatore ternario: se la condizione è verificata inserisci 0
              codiceLetto += String (RC522.uid.uidByte[i],HEX);
            }

            Serial.println(codiceLetto);

            stato++;
          }
    break;
    case 1:
          if (Serial.available()){
            messaggio = "";
            nome = "";
            cognome = "";
            
            lcd.clear();
            lcd.setCursor(2, 0);
            lcd.print("Controllo accessi");

            nome = leggiDati();
            lcd.setCursor(1, 1);
            nome.toUpperCase();
            lcd.print(nome);
            
            cognome = leggiDati();
            lcd.setCursor(1, 2);
            cognome.toUpperCase();
            lcd.print(cognome);
            
            messaggio = leggiDati();
            lcd.setCursor(1, 3);
            lcd.print(messaggio);

            if (verificaCodice(messaggio,"ACCESSO CONSENTITO\n"))
              accendiLed(ledVerde);
            else
              accendiLed(ledRosso);
              
            delay(2000);
            stato--;
            lcd_init();
            }
    break;  
    }  
}

/*  Funzione che gestisce l'output del display*/
void lcd_init(){
  lcd.clear();
  lcd.setCursor(2, 0);lcd.print("Controllo accessi");
  lcd.setCursor(4, 1);lcd.print("Sviluppato da");
  lcd.setCursor(2, 2);lcd.print("Andrea e Antonio");
  lcd.setCursor(4, 3);lcd.print("Versione 0.1");
  }

/* Questa funzione delle i dati che arrivano sulla seriale*/
String leggiDati(){
  char c;
  String s;
  do{
    if (Serial.available()){  // Deve continuare a leggere solo se nel buffer c'è qualcosa
      c=Serial.read();
      s += c;
    }
  }while(c != '\n');
  return s;
}

// Questa funzione verifica se il codice Letto è autorizzato
boolean verificaCodice(String messaggio, String codiceAutorizzato){
  if(messaggio.equals(codiceAutorizzato)){
    return true;
  }else{
    return false;
  }  
}    

// Questa funzione permette di accendere un LED per un determinato periodo
void accendiLed(int ledPin){
  digitalWrite(ledPin,HIGH);
  delay(delayLed);
  digitalWrite(ledPin,LOW);
  delay(delayLed);
  digitalWrite(ledPin,HIGH);
  delay(delayLed);
  digitalWrite(ledPin,LOW);
}
