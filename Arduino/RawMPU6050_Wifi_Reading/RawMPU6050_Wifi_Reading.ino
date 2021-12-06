// Basic demo for accelerometer readings from Adafruit MPU6050
// Added in MQTT communucation to access the IMU data from ROS

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <PubSubClient.h>       // Connect and publish to the MQTT broker
#include <ESP8266WiFi.h>        // Include the Wi-Fi library
#include <WiFiClient.h>


// MQTT - Usable with multiple device by configuration device name.
const char DEVICE_NAME[] = "mpu6050_1";

const char* mpu_datagroup = "main/mpu/datas";

// IP address of your MQTT server - change server username and password as it fits your system
const char* mqtt_server = "######";
const char* mqtt_username = "######"; // MQTT username
const char* mqtt_password = "######"; // MQTT password
const char* clientID = "mpuclient"; // MQTT client ID


// WiFi  - change ssid and password as it fits your system
const char* ssid     = "######";         // The SSID (name) of the Wi-Fi network you want to connect to
const char* password = "######";     // The password of the Wi-Fi network

// Data String
String datagroup;

Adafruit_MPU6050 mpu;
int readings= 0;
int total_readings_rate= 0;
int timer= 0;

// Initialise the WiFi and MQTT Client objects
WiFiClient wifiClient;
// 1883 is the listener port for the Broker
PubSubClient client(mqtt_server, 1883, wifiClient); 

// Custom function to connet to the MQTT broker via WiFi
void connect_MQTT(){
  Serial.print("Connecting to ");
  Serial.println(ssid);

  // Connect to the WiFi
  WiFi.begin(ssid, password);

  // Wait until the connection has been confirmed before continuing
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  // Debugging - Output the IP Address of the ESP8266
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Connect to MQTT Broker
  // client.connect returns a boolean value to let us know if the connection was successful.
  // If the connection is failing, make sure you are using the correct MQTT Username and Password (Setup Earlier in the Instructable)
  if (client.connect(clientID, mqtt_username, mqtt_password)) {
    Serial.println("Connected to MQTT Broker!");
  }
  else {
    Serial.println("Connection to MQTT Broker failed...");
  }
}

void setup(void) {
  Serial.begin(115200);
  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens

  Serial.println("Adafruit MPU6050 test!");

  // Try to initialize!
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");

  mpu.setAccelerometerRange(MPU6050_RANGE_4_G);

  mpu.setGyroRange(MPU6050_RANGE_500_DEG);

  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);


  Serial.println("");
  delay(100);
  
  connect_MQTT();
  Serial.setTimeout(2000);
  
  
  //timer=millis();

  
}

void loop() {

  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  
  //readings=readings+1;
  //total_readings_rate=1000*readings/(millis()-timer);
        
  //Serial.print(total_readings_rate);Serial.print(" millis \t");

  /* Print out the values */
  Serial.print("Acceleration X: ");
  Serial.print(a.acceleration.x);
  Serial.print(", Y: ");
  Serial.print(a.acceleration.y);
  Serial.print(", Z: ");
  Serial.print(a.acceleration.z);
  Serial.println(" m/s^2");

  Serial.print("Rotation X: ");
  Serial.print(g.gyro.x);
  Serial.print(", Y: ");
  Serial.print(g.gyro.y);
  Serial.print(", Z: ");
  Serial.print(g.gyro.z);
  Serial.println(" rad/s");

  Serial.print("Temperature: ");
  Serial.print(temp.temperature);
  Serial.println(" degC");

  Serial.println("");

  datagroup = String();
  datagroup = String(a.acceleration.x)+String(",")+String(a.acceleration.y)+String(",")+String(a.acceleration.z)+String(",")+String(g.gyro.x)+String(",")+String(g.gyro.y)+String(",")+String(g.gyro.z);

  // PUBLISH to the MQTT Broker (topic = Acceleration X)
  if (client.publish(mpu_datagroup, datagroup.c_str())) {
      Serial.println("MPU Datas are sent!");
  }
  // Again, client.publish will return a boolean value depending on whether it succeded or not.
  // If the message failed to send, we will try again, as the connection may have broken.
  else{
    Serial.println("Acceleration failed to send. Reconnecting to MQTT Broker and trying again");
    client.connect(clientID, mqtt_username, mqtt_password);
    delay(10); // This delay ensures that client.publish doesn't clash with the client.connect call
    client.publish(mpu_datagroup, datagroup.c_str());
  }
  
}
