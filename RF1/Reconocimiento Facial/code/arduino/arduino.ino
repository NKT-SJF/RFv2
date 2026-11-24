#include <SPI.h>
#include <Ethernet.h>

// Configura los parámetros de la red
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED }; // Dirección MAC del Shield
IPAddress ip(192, 168, 1, 178); // Dirección IP fija (Cambiar)
EthernetServer server(80); // Servidor en el puerto 80

const int relayPin = 7; // Pin conectado al relay

void setup() {
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW); // El relay empieza apagado
  
  Ethernet.begin(mac, ip);
  server.begin();
  
  Serial.begin(9600);
  Serial.println("Servidor listo...");
}

void loop() {
  EthernetClient client = server.available(); // Escucha conexiones entrantes
  
  if (client) {
    String request = ""; // Para almacenar el mensaje recibido
    
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        request += c;
        
        // Fin de la petición
        if (c == '\n') {
          Serial.println(request);
          
          // Activa el relay si recibe la señal esperada
          if (request.indexOf("open") != -1) {
            digitalWrite(relayPin, HIGH); // Activa el relay
            delay(3000); // Mantiene la puerta abierta por 3 segundos
            digitalWrite(relayPin, LOW); // Desactiva el relay
            client.println("HTTP/1.1 200 OK");
            client.println("Content-Type: text/plain");
            client.println("Connection: close");
            client.println();
            client.println("Puerta abierta.");
            break;
          }
        }
      }
    }
    client.stop(); // Finaliza la conexión
  }
}
