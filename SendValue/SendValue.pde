import processing.serial.*;
import javax.xml.bind.DatatypeConverter;
import processing.net.*;
import http.requests.*;

JSONObject response;
String name;
String surname;
String message;

Client myClient; 
Serial serial;

void setup(){
  String port_name = "/dev/ttyACM0";
  serial = new Serial(this, port_name, 9600);  
}

void draw(){
  String num = "";
  String numero_tessera = "";
  if (serial.available()>0){
       numero_tessera = serial.readStringUntil('\n'); 
    if (numero_tessera != null){
       for (int i = 0; i < 8; i++){
       char carattere = numero_tessera.charAt(i);
       num += carattere;
      }
      
    String dati;
    dati = "{\"codice\":" + num + "}";
    int len = dati.length();
    //post http
    PostRequest post = new PostRequest("http://localhost:8080/api/v0.1/accesso/"+num);
    //PostRequest post = new PostRequest("http://progetto-iot2.appspot.com/api/v0.1/accesso/"+num);
    //post.addHeader("Content-Type", "application/json");
    //post.addData("codice", dati);
    //System.out.println("Reponse Content: " + post.getContent());

    post.send();
    //postValue("localhost",8080,"/api/v0.1/accesso/",num);
    System.out.println("Reponse Content: " + post.getContent());
    
    
    response = parseJSONObject(post.getContent()); 
    name = response.getString("nome"); 
    surname = response.getString("cognome");
    message = response.getString("message");
    
    if (name!=null){
      serial.write(name+'\n');
      serial.write(surname+'\n');
      serial.write(message+'\n');
    }else if(name==null){
        serial.write('\n');
        serial.write('\n');
        serial.write(message+'\n');}
    
}}}

void postValue(String host, int port, String path, String valore) {
   
  String httpBuffer; 
   
  println("Connessione in corso...");
  myClient = new Client(this, host, port); 
   
  if (myClient.active())
  {
    println("Connessione avvenuta!");
     
    // invio request line
    httpBuffer = "POST " + path + " HTTP/1.1 \n";
    
    // invio la richiesta
    println(httpBuffer);
    myClient.write(httpBuffer);
    
    // calcolo il campo dati in formato json
    String dati;
    dati = "{\"codice\":" + valore + "}";
    int len = dati.length();
        
         
    // invio header "Host"
    httpBuffer = "Host: " + host + ":" + str(port) + "\n";
    
    println(httpBuffer);
    myClient.write(httpBuffer);
     
    // invio header "Connection"
    httpBuffer = "Connection: close \n";
    println(httpBuffer);
    myClient.write(httpBuffer);
     
    // invio header "Content-Type",
    httpBuffer = "Content-Type: application/json; charset=utf-8 \n";
    println(httpBuffer);
    myClient.write(httpBuffer);
     
    // invio "Content-Length" (dimensione dati + 2 sommando i
    // doppi apici per il formato JSON delle ASP.NET Web API)
    httpBuffer = "Content-Length: " + str(len) + " \n";
    println(httpBuffer);
    myClient.write(httpBuffer);
    
    // autenticazione
    //String auth = username + ":" + password;
    //String encodedAuth =DatatypeConverter.printBase64Binary(auth.getBytes());
    
    //httpBuffer = "Authorization: Basic " + encodedAuth + " \n";
    //println(httpBuffer);
    //myClient.write(httpBuffer);
   
    // linea vuota tra headers HTTP e Body
    myClient.write("\n");
    
    // invio Body
    println(dati);
    myClient.write(dati);
    
     //attendo la risposta
    delay(1000);
     
    // ci sono byte disponibili
    while (myClient.available()>0)
    {
      // leggo il prossimo e lo trasmetto sulla seriale
      char c = myClient.readChar();
      print(c);
    }
   
   println ("fine connessione");
   myClient.stop();
   
  }}
