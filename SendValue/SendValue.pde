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
       int l = numero_tessera.length();
       for (int i = 0; i < l-2; i++){
       char carattere = numero_tessera.charAt(i);
       num += carattere;
      }
      
    String dati;
    dati = "{codice:" + num + "}";
    int len = dati.length();
    //post http
    //PostRequest post = new PostRequest("http://localhost:8080/api/v0.1/accesso/"+num);
    PostRequest post = new PostRequest("http://progetto-iot2.appspot.com/api/v0.1/accesso/"+num);
    //post.addHeader("Content-Type", "application/json");
    //post.addData("json",dati);

    post.send();
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
