#include <Arduino.h>

#include "HX711.h"

// Libraries to get time from NTP Server
#include <WiFi.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

// Libraries for SD card
#include "FS.h"
#include <SPIFFS.h>
#include <SPI.h>

#include <PubSubClient.h>

#include <ArduinoJson.h>

#define STORE_FILE_PATH "/datalog.txt"
#define NW_CONFIG_FILE "/config.txt"
#define PROTOCOL "MQTT"

#define NO_DATA_CHANGE_FOR_45SEC_TIMEOUT 15000 //15Seconds // 45000 // 45 sec
#define LOG_INTERVAL 500                       // 1000                     // take logs every 1 sec
#define MEASUREMENT_SUCCESSFUL_TIMEOUT 180000  // 180000  // 180sec full readings
#define TIMEOUT_120_SEC  120000

#define SEND_LED 22
#define NW_CONNECTED_LED 25
#define START_MEASUREMENT_LED 26
#define STOP_MEASUREMENT_LED 21
#define BUZZER 4
#define BAT_LOW 27
#define BAT_SENSE 35
#define WEIGHT_THRESHOLD  2000

#define CALIBRATION_FACTOR  1283254


#define ADC_MAX 4095.0f
#define ADC_REF 3.3f

int32_t readingWeight[MEASUREMENT_SUCCESSFUL_TIMEOUT / LOG_INTERVAL] = {0};
int32_t readingTime[MEASUREMENT_SUCCESSFUL_TIMEOUT / LOG_INTERVAL] = {0};

// Replace with your network credentials
///const char *ssid = "Logsun";
//const char *password = "lgs202021";

// Add your MQTT Broker IP address, example:
// const char* mqtt_server = "192.168.1.144";
//const char *mqtt_server = "192.168.1.106";

char ssid[15];
char password[15];
char mqtt_server[18];
char mqtt_port[6];
char mqtt_username[15];
char mqtt_password[15];

uint32_t Port=0;
IPAddress MQTT_Broker;

String SSID ="", PASSWD = "", BRO_IP="", BRO_PORT="", BRO_USERNAME="", BRO_PASSWORD="";
String NW_Config_Data ="";

// Define NTP Client to get time
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP);
WiFiClient espClient;
PubSubClient client(espClient);

long lastMsg = 0;
char msg[50];
int value = 0;

float B_Volt = 0.0f;
uint32_t ADC_Count=0;


// Variables to save date and time
String formattedDate;
String dayStamp;
String timeStamp;

typedef enum _STATES_
{
  IDLE = 0,
  READ_MEASUREMENT_DATA,
  CHECK_FOR_IS_WEIGHT_INCREASING,
  CHECK_FOR_SAME_DATA_FOR_45SEC_TIMEOUT,
  CHECK_FOR_SAME_DATA_FOR_120SEC_TIMEOUT,
  WAIT_FOR_SOMETIME_TO_TAKE_NEXT_LOG_AND_CHECK_TIMEOUT,
  OVER_WEIGHT_DETECTED,
} eSTATES;

eSTATES currState = IDLE;

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 32;
const int LOADCELL_SCK_PIN = 33;

HX711 scale;

bool startMeasurementFlag = false, stopMeasurementFlag = false, measurementStarted = false;
bool overWeightDetectedFlag = false;
bool Zero_Flag = false;


float currWeight = 0, Initial_Weight=0.0f;
float avgValOfWeight = 0;
int currentWeight, prevWeight;
// Save reading number on RTC memory
RTC_DATA_ATTR int readingID = 0;

String weightFileData;

uint32_t millisForMeasurement = 0, millisForDifferentDataRx = 0, miilisToCalculateTime = 0;
uint32_t currMillisTimeForData = 0;


void GetDataTimeFromNtpServer(String &dateTime);
void writeFile(fs::FS &fs, const char *path, const char *message);
void appendFile(fs::FS &fs, const char *path, const char *message);
void readFile(fs::FS &fs, const char *path, String *message);
void deleteFile(fs::FS &fs, const char *path);
void logtoSPIFFS_flashMemory();
void LoadCellLoop();
void setup_wifi();
void Setup_Mode();
void Read_Param();
void callback(char *topic, byte *message, unsigned int length);
void reconnect();
String ENDF1(const String &p_line, int &p_start, char p_delimiter);
String ENDF2(const String &p_line, int &p_start, String p_delimiter);

void setup()
{
  Serial.begin(115200);

if (!SPIFFS.begin(true))
  {
    Serial.println("[SPIFFS] Flash memory mounting failed\n");
  }
  else
  {
    Serial.println("[SPIFFS] Flash memory mounted\n");
  }

  pinMode(SEND_LED, OUTPUT);
  pinMode(NW_CONNECTED_LED, OUTPUT);
  pinMode(START_MEASUREMENT_LED, OUTPUT);
  pinMode(STOP_MEASUREMENT_LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  pinMode(BAT_LOW,OUTPUT);
  digitalWrite(SEND_LED, HIGH);
  digitalWrite(NW_CONNECTED_LED, HIGH);
  digitalWrite(START_MEASUREMENT_LED, HIGH);
  digitalWrite(STOP_MEASUREMENT_LED, HIGH);
  digitalWrite(BUZZER, LOW);
  digitalWrite(BAT_LOW,HIGH);

 

  Read_Param();

  setup_wifi();

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  //client.connect("clientid",mqtt_username,mqtt_password);
  

  

  // Initialize a NTPClient to get time
  timeClient.begin();
  // Set offset time in seconds to adjust for your timezone, for example:
  // GMT +1 = 3600
  // GMT +8 = 28800
  // GMT -1 = -3600
  // GMT 0 = 0
  timeClient.setTimeOffset(19800);

  

  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  Serial.println("Press T to tare");
  // scale.set_scale(-441500); // Calibration Factor obtained from first sketch //106600
  // scale.set_scale(-443500);
  //Old factor by anil =>
  //New Factor at Logsun => 448788.03 or 448788
  scale.set_scale(CALIBRATION_FACTOR); //  1220174
    // scale.set_scale(380500); // accurate calibration by calibration code for new enclosure hardware.
  scale.tare(); // Reset the scale to 0

  Serial.print("Weight: ");
  Serial.print(scale.get_units(), 3); // Up to 3 decimal points
  Serial.println(" kg");              // Change this to kg and re-adjust the calibration factor if you follow lbs

  
}

void loop()
{
  static uint32_t previousMillis = 0;

  if (!client.connected())
  {
    digitalWrite(NW_CONNECTED_LED, HIGH);
    if (measurementStarted == false)
    {
      if ((WiFi.status() != WL_CONNECTED))
      {
        if ((millis() - previousMillis > 10000))
        {
          // Serial.print(millis());
          Serial.println("\nReconnecting to WiFi...");
          WiFi.disconnect();
          WiFi.reconnect();
          previousMillis = millis();
        }
      }
      else
      {
        Serial.println("Wifi connection successful!\n");
        reconnect();
      }
    }
  }
  else
  {
    digitalWrite(NW_CONNECTED_LED, LOW);
  }
  client.loop();

  ADC_Count = analogRead(BAT_SENSE);

  B_Volt = (BAT_SENSE/ADC_MAX)*ADC_REF;
  B_Volt *= 100.00;
  //Serial.println(B_Volt,6);
  //B_Volt *= 100;
  if(B_Volt<=1.65){
    digitalWrite(BAT_LOW,LOW);
  }
  else{
    digitalWrite(BAT_LOW,HIGH);
  }

  if (Serial.available())
  {
    char temp = Serial.read();
    Serial.println();
    // Serial.print("RX cmd:");
    Serial.println(temp);

    if(temp == 'S'){
      Setup_Mode();
    }
    if (temp == 't' || temp == 'T')
    {
      scale.tare(); // Reset the scale to zero
      Serial.println("Calibration done!");
    }
    else if (temp == '1')
    {
      digitalWrite(START_MEASUREMENT_LED, LOW);
      digitalWrite(STOP_MEASUREMENT_LED, HIGH);
      Serial.println("Start measurement cmd received!");
      weightFileData = "";
      readFile(SPIFFS, STORE_FILE_PATH, &weightFileData);
      if (weightFileData.indexOf("\r\n") > 0)
      {
        Serial.println(weightFileData);
        Serial.println("\nThere are records in the memory.");
        Serial.println("\nDo you want to delete saved logs? (Y/N)\n");
        return;
      }
      startMeasurementFlag = true;
      stopMeasurementFlag = false;
    }
    else if (temp == '2')
    {
      digitalWrite(STOP_MEASUREMENT_LED, LOW);
      digitalWrite(START_MEASUREMENT_LED, HIGH);
      Serial.println("Stop measurement cmd received!");
      stopMeasurementFlag = true;
      startMeasurementFlag = false;
    }
    else if (temp == '3')
    {
      digitalWrite(SEND_LED, LOW);
      delay(1000);
      Serial.println("send data cmd received!");
      weightFileData = "";
      readFile(SPIFFS, STORE_FILE_PATH, &weightFileData);
      Serial.println(weightFileData);
      digitalWrite(SEND_LED, HIGH);
      Serial.println("\nDo you want to delete saved logs? (Y/N)\n");
    }
    else if ((temp == 'y') || (temp == 'Y'))
    {
      Serial.println("Yes cmd received, to delete data log.");
      weightFileData = "";
      readFile(SPIFFS, STORE_FILE_PATH, &weightFileData);
      if (weightFileData.indexOf("\r\n") > 0)
      {
        deleteFile(SPIFFS, STORE_FILE_PATH);
        // writeFile(SPIFFS, STORE_FILE_PATH, "Reading ID, Date, Hour, Weight\n");
      }
      else
      {
        Serial.println("No logs available in memory to delete");
      }
    }
    else if ((temp == 'n') || (temp == 'N'))
    {
      Serial.println("No cmd received, logs are not deleted!");
    }
    else
    {
    }
  }
  LoadCellLoop();
}

void setup_wifi()
{

  char req='\0';
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to WiFi SSID: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
    if(Serial.available()){
      req = Serial.read();
      Serial.read();
      Serial.flush();
    }
    if(req == 'S'){
      Setup_Mode();
    }
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char *topic, byte *message, unsigned int length)
{
  StaticJsonDocument<100> CommandDoc;
  StaticJsonDocument<256> CommandRespDoc;
  StaticJsonDocument<256> DataDoc;
  StaticJsonDocument<256> DataDocStatus;
  String output, dataPacket;
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;

  for (int i = 0; i < length; i++)
  {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  // char temp = *messageTemp.c_str();

  if (String(topic) == "/Device/Command")
  {
    DeserializationError error = deserializeJson(CommandDoc, messageTemp.c_str());

    if (error)
    {
      Serial.print(F("deserializeJson() failed: "));
      Serial.println(error.c_str());
      return;
    }

    if (CommandDoc.containsKey("Calibration"))
    {
      const char *commandRx = CommandDoc["Calibration"];
      if (0 == strcmp(commandRx, "On"))
      // if (temp == 't' || temp == 'T')
      {
        scale.tare(); // Reset the scale to zero
        CommandRespDoc["Command"] = "OK";
        serializeJson(CommandRespDoc, output);
        client.publish("/PC/Command", output.c_str());
        Serial.println("Calibration done!");
      }
    }
    if (CommandDoc.containsKey("Command"))
    {
      const char *commandRx = CommandDoc["Command"];

      // Changes the output state according to the message
      if (0 == strcmp(commandRx, "On"))
      {
        Serial.println("Start measurement cmd received!");
        if (overWeightDetectedFlag == true)
        {
          CommandRespDoc["Command"] = "OW";
          serializeJson(CommandRespDoc, output);
          client.publish("/PC/Command", output.c_str());
          return;
        }
        weightFileData = "";
        readFile(SPIFFS, STORE_FILE_PATH, &weightFileData);
        if (weightFileData.indexOf("\r\n") > 0)
        {
          Serial.println(weightFileData);
          Serial.println("\nThere are records in the memory.");
          Serial.println("\nDo you want to delete saved logs? (Y/N)\n");
          CommandRespDoc["Command"] = "Alert";
          serializeJson(CommandRespDoc, output);
          client.publish("/PC/Command", output.c_str());
        }
        else
        {
          startMeasurementFlag = true;
          stopMeasurementFlag = false;
          Zero_Flag = true;
          digitalWrite(BUZZER, HIGH);
          delay(500);
          digitalWrite(BUZZER, LOW);
          digitalWrite(START_MEASUREMENT_LED, LOW);
          digitalWrite(STOP_MEASUREMENT_LED, HIGH);
          CommandRespDoc["Command"] = "Start";
          serializeJson(CommandRespDoc, output);
          client.publish("/PC/Command", output.c_str());
        }
      }
      else if (0 == strcmp(commandRx, "Off"))
      {
        digitalWrite(STOP_MEASUREMENT_LED, LOW);
        digitalWrite(START_MEASUREMENT_LED, HIGH);
        Serial.println("Stop measurement cmd received!");
        CommandRespDoc["Command"] = "OK";
        serializeJson(CommandRespDoc, output);
        client.publish("/PC/Command", output.c_str());
        stopMeasurementFlag = true;
        startMeasurementFlag = false;
      }
      else if(0 == strcmp(commandRx,"Constat"))
      {
        CommandRespDoc["Status"] = "True";
        dataPacket = "";
        serializeJson(CommandRespDoc, dataPacket);
        delay(100);
        client.publish("/PC/Command", dataPacket.c_str());
      }
    }
    if (CommandDoc.containsKey("Download"))
    {
      const char *commandRx = CommandDoc["Download"];
      // Changes the output state according to the message
      if (0 == strcmp(commandRx, "Yes"))
      {
        Serial.println("Yes cmd received, to delete data log.");
        DataDocStatus["Status"] = "Start";
        dataPacket = "";
        serializeJson(DataDocStatus, dataPacket);
        client.publish("/PC/Data", dataPacket.c_str());
        delay(50);
        weightFileData = "";
        readFile(SPIFFS, STORE_FILE_PATH, &weightFileData);
        if (weightFileData.indexOf("\r\n") > 0)
        {
          Serial.println("Logs found in memory!");
          int l_posn = 0;
          String endStr = ENDF2(weightFileData, l_posn, "\r\n");
          while (0 != strcmp(endStr.c_str(), ""))
          {
            Serial.print("data: ");
            Serial.println(endStr.c_str());
            int parsePos = 0;
            int dataId = ENDF1(endStr, parsePos, ',').toInt();
            int timeOfData = ENDF1(endStr, parsePos, ',').toInt();
            int weightData = ENDF1(endStr, parsePos, ',').toInt();
            DataDoc["ID"] = dataId;
            DataDoc["Weight"] = weightData;
            DataDoc["Time"] = timeOfData;
            dataPacket = "";
            serializeJson(DataDoc, dataPacket);
            client.publish("/PC/Data", dataPacket.c_str());
            digitalWrite(SEND_LED, LOW);
            delay(50);
            digitalWrite(SEND_LED, HIGH);
            endStr = ENDF2(weightFileData, l_posn, "\r\n");
          }
          deleteFile(SPIFFS, STORE_FILE_PATH);
          DataDocStatus["Status"] = "Finish";
          dataPacket = "";
          serializeJson(DataDocStatus, dataPacket);
          client.publish("/PC/Data", dataPacket.c_str());
        }
        else
        {
          CommandRespDoc["Command"] = "ERROR";
          serializeJson(CommandRespDoc, output);
          client.publish("/PC/Command", output.c_str());
          Serial.println("No logs available in memory to delete");
        }
      }
      else if (0 == strcmp(commandRx, "No"))
      {
        Serial.println("No cmd received, logs stored in memory!");
        // logs will store inside memory
        CommandRespDoc["Command"] = "OK";
        serializeJson(CommandRespDoc, output);
        client.publish("/PC/Command", output.c_str());
      }
      else
      {
      }
    }
    if (CommandDoc.containsKey("Response"))
    {
      const char *commandRx = CommandDoc["Response"];

      // Changes the output state according to the message
      if (0 == strcmp(commandRx, "Yes"))
      {
        Serial.println("Yes cmd received, to delete data log.");
        DataDocStatus["Status"] = "Start";
        dataPacket = "";
        serializeJson(DataDocStatus, dataPacket);
        client.publish("/PC/Data", dataPacket.c_str());
        delay(50);
        weightFileData = "";
        readFile(SPIFFS, STORE_FILE_PATH, &weightFileData);
        if (weightFileData.indexOf("\r\n") > 0)
        {
          Serial.println("Logs found in memory!");
          int l_posn = 0;
          String endStr = ENDF2(weightFileData, l_posn, "\r\n");
          while (0 != strcmp(endStr.c_str(), ""))
          {
            Serial.print("data: ");
            Serial.println(endStr.c_str());
            int parsePos = 0;
            int dataId = ENDF1(endStr, parsePos, ',').toInt();
            int timeOfData = ENDF1(endStr, parsePos, ',').toInt();
            int weightData = ENDF1(endStr, parsePos, ',').toInt();
            DataDoc["ID"] = dataId;
            DataDoc["Weight"] = weightData;
            DataDoc["Time"] = timeOfData;
            dataPacket = "";
            serializeJson(DataDoc, dataPacket);
            client.publish("/PC/Data", dataPacket.c_str());
            digitalWrite(SEND_LED, LOW);
            delay(50);
            digitalWrite(SEND_LED, HIGH);
            endStr = ENDF2(weightFileData, l_posn, "\r\n");
          }
          deleteFile(SPIFFS, STORE_FILE_PATH);
          DataDocStatus["Status"] = "Finish";
          dataPacket = "";
          serializeJson(DataDocStatus, dataPacket);
          client.publish("/PC/Data", dataPacket.c_str());
          delay(50);
          CommandRespDoc["Command"] = "OK";
          serializeJson(CommandRespDoc, output);
          client.publish("/PC/Command", output.c_str());
        }
        else
        {
          CommandRespDoc["Command"] = "ERROR";
          serializeJson(CommandRespDoc, output);
          client.publish("/PC/Command", output.c_str());
          Serial.println("No logs available in memory to delete");
        }
      }
      else if (0 == strcmp(commandRx, "No"))
      {
        Serial.println("No cmd received, deleting logs directly");
        // no received delete logs directly
        deleteFile(SPIFFS, STORE_FILE_PATH);
        // writeFile(SPIFFS, STORE_FILE_PATH, "Reading ID, Date, Hour, Weight\n");
        CommandRespDoc["Command"] = "OK";
        serializeJson(CommandRespDoc, output);
        client.publish("/PC/Command", output.c_str());
      }
      else
      {
      }
    }
  }
}

void reconnect()
{
  char req='\0';
  // Loop until we're reconnected
  while (!client.connected())
  {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    // if (client.connect("clientid"))
    if (client.connect("clientid",mqtt_username,mqtt_password))
    {
      Serial.println("connected!");
      // Subscribe
      client.subscribe("/Device/Command");
    }
    else
    {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
     if(Serial.available()){
      req = Serial.read();
      Serial.read();
      Serial.flush();
    }
    if(req == 'S'){
      Setup_Mode();
    }
  }
}

void GetDataTimeFromNtpServer(String &dateTime)
{
  while (!timeClient.update())
  {
    timeClient.forceUpdate();
  }
  // The formattedDate comes with the following format:
  // 2018-05-28T16:00:13Z
  // We need to extract date and time
  formattedDate = timeClient.getFormattedDate();
  // Serial.println(formattedDate);

  // Extract date
  int splitT = formattedDate.indexOf("T");
  dayStamp = formattedDate.substring(0, splitT);
  // Serial.print("DATE: ");
  // Serial.println(dayStamp);
  // Extract time
  timeStamp = formattedDate.substring(splitT + 1, formattedDate.length() - 1);
  // Serial.print("HOUR: ");
  // Serial.println(timeStamp);
  dateTime = dayStamp + " " + timeStamp;
}

void LoadCellLoop()
{
  static uint32_t lastMillis = 0;
  String currTimeStamp;
  StaticJsonDocument<256> CommandRespDoc;
  String output;

  switch (currState)
  {
  case IDLE:
    if (startMeasurementFlag == false)
    {
      currWeight = scale.get_units();
      // Serial.println(currWeight, 3); // Up to 3 decimal points
      currentWeight = (currWeight * 1000);
      prevWeight = currentWeight;
      if (currentWeight > WEIGHT_THRESHOLD) // check for over weight detection
      {
        currState = OVER_WEIGHT_DETECTED;
        if (overWeightDetectedFlag == false)
        {
          overWeightDetectedFlag = true;
          CommandRespDoc["Command"] = "OW";
          serializeJson(CommandRespDoc, output);
          client.publish("/PC/Command", output.c_str());
        }
        digitalWrite(BUZZER, HIGH);
        delay(1000);
        break;
      }
      else
      {
        if (overWeightDetectedFlag == true)
        {
          CommandRespDoc["Command"] = "No-OW";
          serializeJson(CommandRespDoc, output);
          client.publish("/PC/Command", output.c_str());
        }
        overWeightDetectedFlag = false;
      }
      delay(200);
    }
    else // if start measurement command received
    {
      Serial.println("Reading started successfully...");
      measurementStarted = true;
      readingID = 0;
      millisForMeasurement = millis(); // start 180sec period
      millisForDifferentDataRx = millis();
      miilisToCalculateTime = millis();
      currMillisTimeForData = 0;
      currState = READ_MEASUREMENT_DATA;
      break;
    }
    break;

  case READ_MEASUREMENT_DATA:
    if (startMeasurementFlag == true)
    {
      Serial.println("\nReading weight...");
      // GetDataTimeFromNtpServer(currTimeStamp);
      // Serial.print(currMillisTimeForData);
      // Serial.print("  ");
      // Serial.print("Weight: ");
      // for (int i = 0; i < 10; i++)
      // {
      //   currWeight = scale.get_units();
      //   // Serial.println(currWeight, 3); // Up to 3 decimal points
      //   avgValOfWeight = avgValOfWeight + currWeight;
      //   delay(10);
      // }
      // currentWeight = (avgValOfWeight / 10) * 1000; // averaging data
      // currentWeight = String(currWeight, 3);

      
      
      // Serial.print("Millis: ");
      // Serial.println(millis());
      currWeight = scale.get_units(1);
      currentWeight = (currWeight * 1000);
      // Serial.print("Millis: ");
      // Serial.println(millis());
      Serial.println(currentWeight);
      // Serial.println(currWeight, 3); // Up to 3 decimal points
      if (currentWeight > 3000) // check for over weight detection
      {
        currState = OVER_WEIGHT_DETECTED;
        break;
      }

      if(currentWeight > 5){
        Zero_Flag = false;
      }
      currMillisTimeForData = millis() - miilisToCalculateTime;
      Serial.println("readingID: " + String(readingID));
      readingWeight[readingID] = currentWeight;
      readingTime[readingID] = currMillisTimeForData;

      Serial.print("currMillisTimeForData: ");
      Serial.println(currMillisTimeForData);
      // logtoSPIFFS_flashMemory();

      // Increment readingID on every new reading
      readingID++;
      lastMillis = millis();
      // Serial.println("Weight (kg)");        // Change this to kg and re-adjust the calibration factor if you follow lbs
      currState = CHECK_FOR_IS_WEIGHT_INCREASING;
    }
    else
    {
      Serial.println("Measurement stopped successfully!");
      currState = IDLE;
    }
    break;

  case OVER_WEIGHT_DETECTED:
    if (startMeasurementFlag == true)
    {
      Serial.println("Stopping measurement, Over weight detected!");
      stopMeasurementFlag = true;
      startMeasurementFlag = false;
      measurementStarted = false;
      digitalWrite(STOP_MEASUREMENT_LED, LOW);
      digitalWrite(START_MEASUREMENT_LED, HIGH);
    }
    digitalWrite(BUZZER, LOW);
    delay(1000);
    currState = IDLE;
    break;

  case CHECK_FOR_IS_WEIGHT_INCREASING:
    // if (0 != currentWeight.compareTo(prevWeight)) // tollrance
    // {
    //   prevWeight = currentWeight;
    //   // Serial.println("weight is different");
    //   // Serial.println(prevWeight);
    //   // Serial.println(currentWeight);
    //   millisForDifferentDataRx = millis();
    // }
    // else if (0 != currentWeight.compareTo(prevWeight)) // tollrance
    // {
    //   prevWeight = currentWeight;
    //   // Serial.println("weight is different");
    //   // Serial.println(prevWeight);
    //   // Serial.println(currentWeight);
    //   millisForDifferentDataRx = millis();
    // }
    // Serial.print("abs(currentWeight - prevWeight): ");
    // Serial.println(abs(currentWeight - prevWeight));
    if (abs(currentWeight - prevWeight) <= 1) // tollrance
    {
      // Serial.println("weight is different");
      // Serial.println(prevWeight);
      // Serial.println(currentWeight);
      Serial.print("weight is same as previous since: ");
      Serial.println(millis() - millisForDifferentDataRx);
      Serial.println();
    }
    // else if ((prevWeight - currentWeight) < 1) // tollrance
    // {
    //   prevWeight = currentWeight;
    //   // Serial.println("weight is different");
    //   // Serial.println(prevWeight);
    //   // Serial.println(currentWeight);
    //   Serial.print("weight is same as previous since: ");
    //   Serial.println(millis() - millisForDifferentDataRx);
    //   // millisForDifferentDataRx = millis();
    // }
    else
    {
      // Serial.println("weight is different");
      // Serial.println(prevWeight);
      // Serial.println(currentWeight);
      millisForDifferentDataRx = millis();
      // Serial.print("weight is same as previous since: ");
      // Serial.println(millis() - millisForDifferentDataRx);
    }
    
    prevWeight = currentWeight;
    if(!Zero_Flag){
      currState = CHECK_FOR_SAME_DATA_FOR_45SEC_TIMEOUT;
    }
    else
    {
      currState = CHECK_FOR_SAME_DATA_FOR_120SEC_TIMEOUT;
    }
    
    break;

  case CHECK_FOR_SAME_DATA_FOR_45SEC_TIMEOUT:
    if (millis() - millisForDifferentDataRx >= NO_DATA_CHANGE_FOR_45SEC_TIMEOUT)
    {
      Serial.println("Stopping measurement, No weight is updated for 45 SEC");
      stopMeasurementFlag = true;
      startMeasurementFlag = false;
      measurementStarted = false;
      logtoSPIFFS_flashMemory();
      digitalWrite(BUZZER, HIGH);
      delay(250);
      digitalWrite(BUZZER, LOW);
      delay(250);
      digitalWrite(BUZZER, HIGH);
      delay(250);
      digitalWrite(BUZZER, LOW);
      delay(250);
      digitalWrite(STOP_MEASUREMENT_LED, LOW);
      digitalWrite(START_MEASUREMENT_LED, HIGH);
      CommandRespDoc["Command"] = "Download?";
      serializeJson(CommandRespDoc, output);
      client.publish("/PC/Command", output.c_str());
      memset(readingWeight, 0, sizeof(readingWeight));
      memset(readingTime, 0, sizeof(readingTime));
      // for (int i = 0; i < MEASUREMENT_SUCCESSFUL_TIMEOUT / LOG_INTERVAL; i++)
      // {
      //   Serial.print(i + 1);
      //   Serial.print(",");
      //   Serial.print(readingTime[i]);
      //   Serial.print(",");
      //   Serial.println(readingWeight[i]);
      // }
      currState = IDLE;
    }
    else
    {
      currState = WAIT_FOR_SOMETIME_TO_TAKE_NEXT_LOG_AND_CHECK_TIMEOUT;
    }
    break;

  case CHECK_FOR_SAME_DATA_FOR_120SEC_TIMEOUT:
    if (millis() - millisForDifferentDataRx >= TIMEOUT_120_SEC)
    {
      Serial.println("Stopping measurement, No weight is updated for 120 SEC");
      stopMeasurementFlag = true;
      startMeasurementFlag = false;
      measurementStarted = false;
      logtoSPIFFS_flashMemory();
      digitalWrite(BUZZER, HIGH);
      delay(250);
      digitalWrite(BUZZER, LOW);
      delay(250);
      digitalWrite(BUZZER, HIGH);
      delay(250);
      digitalWrite(BUZZER, LOW);
      delay(250);
      digitalWrite(STOP_MEASUREMENT_LED, LOW);
      digitalWrite(START_MEASUREMENT_LED, HIGH);
      CommandRespDoc["Command"] = "Download?";
      serializeJson(CommandRespDoc, output);
      client.publish("/PC/Command", output.c_str());
      memset(readingWeight, 0, sizeof(readingWeight));
      memset(readingTime, 0, sizeof(readingTime));
      // for (int i = 0; i < MEASUREMENT_SUCCESSFUL_TIMEOUT / LOG_INTERVAL; i++)
      // {
      //   Serial.print(i + 1);
      //   Serial.print(",");
      //   Serial.print(readingTime[i]);
      //   Serial.print(",");
      //   Serial.println(readingWeight[i]);
      // }
      currState = IDLE;
    }
    else
    {
      currState = WAIT_FOR_SOMETIME_TO_TAKE_NEXT_LOG_AND_CHECK_TIMEOUT;
    }
    break;

  case WAIT_FOR_SOMETIME_TO_TAKE_NEXT_LOG_AND_CHECK_TIMEOUT:
    if (millis() - millisForMeasurement >= MEASUREMENT_SUCCESSFUL_TIMEOUT)
    {
      Serial.println("Stopping measurement, 180 sec period is over for measurement");
      stopMeasurementFlag = true;
      startMeasurementFlag = false;
      measurementStarted = false;
      logtoSPIFFS_flashMemory();
      digitalWrite(BUZZER, HIGH);
      delay(250);
      digitalWrite(BUZZER, LOW);
      delay(250);
      digitalWrite(BUZZER, HIGH);
      delay(250);
      digitalWrite(BUZZER, LOW);
      delay(250);
      digitalWrite(STOP_MEASUREMENT_LED, LOW);
      digitalWrite(START_MEASUREMENT_LED, HIGH);
      CommandRespDoc["Command"] = "Download?";
      serializeJson(CommandRespDoc, output);
      client.publish("/PC/Command", output.c_str());
      millisForMeasurement = millis();
      memset(readingWeight, 0, sizeof(readingWeight));
      memset(readingTime, 0, sizeof(readingTime));
      // for (int i = 0; i < MEASUREMENT_SUCCESSFUL_TIMEOUT / LOG_INTERVAL; i++)
      // {
      //   Serial.print(i + 1);
      //   Serial.print(",");
      //   Serial.print(readingTime[i]);
      //   Serial.print(",");
      //   Serial.println(readingWeight[i]);
      // }
      currState = IDLE;
      break;
    }
    if (millis() - lastMillis >= LOG_INTERVAL)
    {
      // currMillisTimeForData = millis() - miilisToCalculateTime;
      // readingTime[readingID] = currMillisTimeForData;
      currState = READ_MEASUREMENT_DATA;
    }
    break;

  default:
    break;
  }
}

// Write the sensor readings on the SD card
void logtoSPIFFS_flashMemory()
{
  for (int i = 0; i < readingID; i++)
  {
    String dataMessage = "";
    // dataMessage = String(readingID) + "," + String(dayStamp) + "," + String(timeStamp) + "," +
    //               String(currWeight, 3) + "\r\n";
    dataMessage = String(i + 1) + "," + String(readingTime[i]) + "," +
                  String(readingWeight[i]) + "\r\n";
    Serial.print("Save data: ");
    Serial.print(dataMessage);
    appendFile(SPIFFS, STORE_FILE_PATH, dataMessage.c_str());
  }
}

// Write to the SD card (DON'T MODIFY THIS FUNCTION)
void writeFile(fs::FS &fs, const char *path, const char *message)
{
  Serial.printf("Writing file: %s\n", path);

  File file = fs.open(path, FILE_WRITE);
  if (!file)
  {
    Serial.println("Failed to open file for writing");
    return;
  }
  if (file.print(message))
  {
    Serial.println("File written");
  }
  else
  {
    Serial.println("Write failed");
  }
  file.close();
}

void readFile(fs::FS &fs, const char *path, String *message)
{
  File file = fs.open(path);

  if ((file == 0) || file.isDirectory())
  {
    Serial.println("File not found");
  }

  while (file.available() > 0)
  {
    *message = file.readString();
  }

  file.close();
}

// Append data to the SD card (DON'T MODIFY THIS FUNCTION)
void appendFile(fs::FS &fs, const char *path, const char *message)
{
  // Serial.printf("Appending to file: %s\n", path);

  File file = fs.open(path, FILE_APPEND);
  if (!file)
  {
    Serial.println("Failed to open file for appending");
    return;
  }
  if (file.print(message))
  {
    // Serial.println("Message appended");
  }
  else
  {
    Serial.println("Append failed");
  }
  file.close();
}

void deleteFile(fs::FS &fs, const char *path)
{
  Serial.printf("Deleting file: %s\n", path);
  if (fs.remove(path))
  {
    Serial.println("File deleted");
  }
  else
  {
    Serial.println("Delete failed");
  }
}

String ENDF1(const String &p_line, int &p_start, char p_delimiter)
{
  // Extract Next Delmited Field V2
  // Extract fields from a line one at a time based on a delimiter.
  // Because the line remains intact we don't fragment heap memory
  // p_start would normally start as 0
  // p_start increments as we move along the line
  // We return p_start = -1 with the last field

  // If we have already parsed the whole line then return null
  if (p_start == -1)
  {
    return "";
  }

  int l_start = p_start;
  int l_index = p_line.indexOf(p_delimiter, l_start);
  if (l_index == -1)
  { // last field of the data line
    p_start = l_index;
    return p_line.substring(l_start);
  }
  else
  { // take the next field off the data line
    p_start = l_index + 1;
    return p_line.substring(l_start, l_index); // Include, Exclude
  }
}

String ENDF2(const String &p_line, int &p_start, String p_delimiter)
{
  // Extract Next Delmited Field V2
  // Extract fields from a line one at a time based on a delimiter.
  // Because the line remains intact we don't fragment heap memory
  // p_start would normally start as 0
  // p_start increments as we move along the line
  // We return p_start = -1 with the last field

  // If we have already parsed the whole line then return null
  if (p_start == -1)
  {
    return "";
  }

  int l_start = p_start;
  int l_index = p_line.indexOf(p_delimiter.c_str(), l_start);
  if (l_index == -1)
  { // last field of the data line
    p_start = l_index;
    return p_line.substring(l_start);
  }
  else
  { // take the next field off the data line
    p_start = l_index + 2;
    return p_line.substring(l_start, l_index); // Include, Exclude
  }
}


void Setup_Mode(){
   Serial.println(PROTOCOL);
   String Config_Data ="";
   char seq= '\0';
    
  while (1)
  {


    while (!Serial.available())
    {
       digitalWrite(NW_CONNECTED_LED,HIGH);
    delay(75);
    digitalWrite(NW_CONNECTED_LED,LOW);
    delay(75);
    digitalWrite(NW_CONNECTED_LED,HIGH);
    delay(75);
    digitalWrite(NW_CONNECTED_LED,LOW);
    delay(75);
    digitalWrite(NW_CONNECTED_LED,HIGH);
    delay(75);
    digitalWrite(NW_CONNECTED_LED,LOW);
    delay(75);
    digitalWrite(NW_CONNECTED_LED,HIGH);
    delay(75);
    digitalWrite(NW_CONNECTED_LED,LOW);
    delay(75);
    digitalWrite(NW_CONNECTED_LED,HIGH);
    delay(75);
    digitalWrite(NW_CONNECTED_LED,LOW);
    delay(75);
    }
    seq = Serial.read();
    Serial.read();
    Serial.flush();
    switch (seq)
    {
      case 'W':
        while (!Serial.available());

      Config_Data = Serial.readString();
      Config_Data.trim();
      //Serial.print(Config_Data);
      writeFile(SPIFFS,NW_CONFIG_FILE,Config_Data.c_str());

   
        Serial.write('A');
        break;

            
  }

    if (seq == 'Q')
    {
      Serial.read();
      Serial.flush();
      ESP.restart();
    }
  }

  return;   
}


void Read_Param(){

  StaticJsonDocument<1024> Config;
  NW_Config_Data = "";
  readFile(SPIFFS,NW_CONFIG_FILE,&NW_Config_Data);

  //NW_Config_Data.remove(0,1);
  //NW_Config_Data.remove(NW_Config_Data.length()-1,1);
  Serial.println(NW_Config_Data);

  if(NW_Config_Data.indexOf("{")!= -1 && NW_Config_Data.indexOf("}")!= -1){
    DeserializationError err = deserializeJson(Config,NW_Config_Data.c_str());
  }
  else{
    Serial.println("Data not in proper JSON format");
    delay(2000);
    return;
  }
  

   const char*  ssid1 = Config["SSID"];
   const char*  password1 = Config["PASSWORD"];
   const char* mqtt_server1 = Config["BRO_IP"];
   const char* mqtt_port1 = Config["BRO_PORT"];
   const char* mqtt_username1 = Config["BRO_UNAME"];
   const char* mqtt_password1 = Config["BRO_PASSWD"]; 

   
  
  

  SSID = ssid1;
  PASSWD = password1;
  BRO_IP = mqtt_server1;
  BRO_PORT = mqtt_port1;
  BRO_USERNAME = mqtt_username1;
  BRO_PASSWORD = mqtt_password1;



  Serial.println(SSID);
  Serial.println(PASSWD);
  Serial.println(BRO_IP);
  Serial.println(BRO_PORT);
  Serial.println(BRO_USERNAME);
  Serial.println(BRO_PASSWORD);


  if(SSID.length()<=14){
    strcpy(ssid,ssid1);
  }
  else{
    Serial.println("SSID length too long");
  }

  if(PASSWD.length()<14){
    strcpy(password,password1);
  }
  else{
    Serial.println("WiFi Password length too long");
  }

  if(BRO_IP.length()<17){
    strcpy(mqtt_server,mqtt_server1);
  }
  else{
    Serial.println("Server IP length too long");
  }

  if(BRO_USERNAME.length()<14){
    strcpy(mqtt_username,mqtt_username1);
  }
  else{
    Serial.println("Broker Username length too long");
  }

  if(BRO_PASSWORD.length()<14){
    strcpy(mqtt_password,mqtt_password1);
  }
  else{
    Serial.println("Broker Password length too long");
  }

    
  Port = BRO_PORT.toInt();
  MQTT_Broker.fromString(BRO_IP);
  
}