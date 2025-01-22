#include <M5Core2.h>
#include <WiFi.h>
#include <ESP_Mail_Client.h>
#define AUTHOR_EMAIL "dtfbbearlord@gmail.com"
#define AUTHOR_PASSWORD "zuvluvymtdvcrcuq"
#define RECIPIENT_EMAIL "dheyab.asad@gmail.com"
#define SMTP_HOST "smtp.gmail.com"
#define SMTP_PORT 465
#include <WiFiMulti.h>
WiFiMulti WiFiMulti;
const char *ssid = "iPhone (8)";//whatever the wifi name is
const char *password = "nugget69";//whatever the wifi password is
const char* NTP_SERVER = "ntp.jst.mfeed.ad.jp";
const char* TZ = "JST-4";//adjust the time zone in reference to the japanese time zone. 
const char* SSID = "iPhone (8)";
const char* PASSWORD = "nugget69";
#define REPORTING_PERIOD_MS 1000

const uint8_t FONT_NUMBER = 2; // 16px ASCII Font
const uint8_t FONT_SIZE = 16;

const bool LCD_ENABLE = true;
const bool SD_ENABLE = false;
const bool SERIAL_ENABLE = true;
const bool I2C_ENABLE = true;

RTC_TimeTypeDef rtcTime;
RTC_DateTypeDef rtcDate;

RTC_TimeTypeDef TimeStruct2;


#include <Wire.h>
#include "MAX30100_PulseOximeter.h"
#define REPORTING_PERIOD_MS 1000
double sum{0},counter{0},average{0},x{0};
PulseOximeter pox;
uint32_t tsLastReport = 0;
RTC_TimeTypeDef TimeStruct;

#define adult_male 1/4.5
#define adult_female 0.25
#define lower_limit 30.0
#define upper_limit 120.0
#define conversion_rate 0.25


SMTPSession smtp;

void smtpCallback(SMTP_Status status);

extern bool setRTC(const char*, const char*);
extern void getRTC(RTC_DateTypeDef&, RTC_TimeTypeDef&);
extern void printDateTime(const RTC_DateTypeDef&, const RTC_TimeTypeDef&);

volatile bool checktimer = false;
int hours(0),minutes(0);

// Defines the buttons. Colors in format {bg, text, outline}
ButtonColors on_clrs = {RED, WHITE, WHITE};
ButtonColors off_clrs = {BLACK, WHITE, WHITE};

Button alarmTimer(0, 0, 0, 0, false, "Alarm Timer", off_clrs, on_clrs, MC_DATUM);
Button HAdetection(0, 0, 0, 0, false, "Heart attack", off_clrs, on_clrs, MC_DATUM);
Button stressRelieve(0, 0, 0, 0, false, "Box breath", off_clrs, on_clrs, MC_DATUM);
Button RelaxBreath(0, 0, 0, 0, false, "Relax Breath", off_clrs, on_clrs, MC_DATUM);

Button incHour(0, 0, 0, 0, false, "H+", off_clrs, on_clrs, MC_DATUM);
Button decHour(0, 0, 0, 0, false, "H-", off_clrs, on_clrs, MC_DATUM);
Button incMin(0, 0, 0, 0, false, "M+", off_clrs, on_clrs, MC_DATUM);
Button decMin(0, 0, 0, 0, false, "M-", off_clrs, on_clrs, MC_DATUM);
Button leave(0, 0, 0, 0, false, "leave time", off_clrs, on_clrs, MC_DATUM);

// For performance measurement (Single tap on bottom-right button)
uint32_t startTime;
uint32_t times = 0;
void setup() {
 M5.begin();
 connectwifi();
 const bool result = setRTC(TZ, NTP_SERVER);//the setRTC function is important for synchronizing the M5stack RTC with abu dhabi time
 M5.Rtc.begin(); 

 alarmTimer.addHandler(settime, E_TAP);
 HAdetection.addHandler(HeartAttack, E_TAP);
 stressRelieve.addHandler(userGuide2, E_TAP);
 RelaxBreath.addHandler(Relaxbreath, E_TAP);
 incHour.addHandler(incrementhour, E_TAP);
 decHour.addHandler(decrementhour, E_TAP);
 incMin.addHandler(incrementmin, E_TAP);
 decMin.addHandler(decrementmin, E_TAP);
 leave.addHandler(leavealarm, E_TAP);
 
 printfunctionsmenu();

}
void incrementhour(Event& e)
{
 hours++;
 if (hours>23){
 hours = 0;
 }
 M5.Lcd.clear(BLACK);
 printincrement();
 M5.Lcd.setCursor(200, 50);
 M5.Lcd.printf("Time : %02d:%02d\n", hours, minutes);
}
void decrementhour(Event& e)
{
 hours--;
 if (hours<0){
 hours = 0;
 }
 M5.Lcd.clear(BLACK);
 printincrement();
 M5.Lcd.setCursor(200, 50);
 M5.Lcd.printf("Time : %02d:%02d\n", hours, minutes);
}
void incrementmin(Event& e)
{
 minutes++;
 if (minutes>59){
 hours++;
 }
 M5.Lcd.clear(BLACK);
 printincrement();
 M5.Lcd.setCursor(200, 50);
 M5.Lcd.printf("Time : %02d:%02d\n", hours, minutes);
}
void decrementmin(Event& e)
{
 minutes--;
 if (minutes<0){
 minutes = 0;
 }
 M5.Lcd.clear(BLACK);
 printincrement();
 M5.Lcd.setCursor(200, 50);
 M5.Lcd.printf("Time : %02d:%02d\n", hours, minutes);
}
void leavealarm(Event& e)
{
 checktimer = true;
 M5.Lcd.clear(BLACK);
 printfunctionsmenu();
}
void loop() {
 M5.update();
 checktime();//constantly checks whether or not the alarm set by the user equals the RTC clock
}

void printfunctionsmenu()//prints main menu
{
 decHour.hide();
 incHour.hide();
 decMin.hide();
 incMin.hide();
 leave.hide();
 alarmTimer.set(0, 0, (M5.Lcd.width()/2)-5, (M5.Lcd.height()/2)-5);
 HAdetection.set((M5.Lcd.width()/2)+5, 0, (M5.Lcd.width()/2)-5, (M5.Lcd.height()/2)-5);
 stressRelieve.set(0, (M5.Lcd.height()/2)+5, (M5.Lcd.width()/2)-5, (M5.Lcd.height()/2)-5);
 RelaxBreath.set((M5.Lcd.width()/2)+5, (M5.Lcd.height()/2)+5, (M5.Lcd.width()/2)-5, (M5.Lcd.height()/2)-5);
 alarmTimer.draw();
 HAdetection.draw();
 stressRelieve.draw();
 RelaxBreath.draw();
}

void HeartAttack(Event& e) { //function for the heart attack detection algorithm button
 
M5.Lcd.clear(BLACK);
M5.Lcd.clear(BLACK);
 M5.Lcd.setTextColor(BLUE);
 M5.Lcd.setTextSize(1);
 M5.Lcd.setCursor(65, 10);
 M5.Lcd.println("Instructions:");
 M5.Lcd.setCursor(10, 30);
 M5.Lcd.printf("1.Inhale for 7 seconds,hold your breath and exhale");
 M5.Lcd.setCursor(10, 70);
 M5.Lcd.printf("2.Keep your finger on the heart rate sensor at all times");
 M5.Lcd.setCursor(10, 150);
 M5.Lcd.println("Duration of practice: 59 seconds");
 M5.Lcd.setCursor(10, 200);
 M5.Lcd.println("The practice is starting in 2 seconds"); 
 delay(3000);
 M5.Spk.begin(); // Initialize the speaker. 
 M5.Spk.DingDong();
 M5.Lcd.setCursor(0, 0);
 M5.Lcd.setTextSize(1);
heart_attack_detection();
delay(1000);
M5.Lcd.clear(BLACK);
printfunctionsmenu();

}
void userGuide2(Event& e) { //function for box breath button
 
M5.Lcd.clear(BLACK);
breathExercise();

}
void Relaxbreath(Event& e) { //function for the relax breath button
 
M5.Lcd.clear(BLACK);
time();
relaxation_algorithm();
M5.Lcd.clear(BLACK);
printfunctionsmenu();


}

void printincrement() //this prints out the buttons for setting the alarm after the user presses the alarm timer button.
{
 M5.Lcd.clear(BLACK);
 alarmTimer.hide();
 HAdetection.hide();
 stressRelieve.hide();
 RelaxBreath.hide();
 decHour.set(0, (M5.Lcd.height()/4), (M5.Lcd.width()/2)-5, (M5.Lcd.height()/4)-5);
 incHour.set(0, 0, (M5.Lcd.width()/2)-5, (M5.Lcd.height()/4)-5);
 decMin.set(0, (M5.Lcd.height()/4)+5+(M5.Lcd.height()/4)+(M5.Lcd.height()/4), (M5.Lcd.width()/2)-5, (M5.Lcd.height()/4)-5);
 incMin.set(0, (M5.Lcd.height()/4)+5+(M5.Lcd.height()/4), (M5.Lcd.width()/2)-5, (M5.Lcd.height()/4)-5);
 leave.set((M5.Lcd.width()/2)+5, (M5.Lcd.height()/2)+5, (M5.Lcd.width()/2)-5, (M5.Lcd.height()/2)-5);
 decHour.draw();
 incHour.draw();
 decMin.draw();
 incMin.draw();
 leave.draw();
 M5.Lcd.setCursor(200, 50);
 M5.Lcd.printf("Time : %02d:%02d\n", hours, minutes);
}
void settime(Event& e)//calls the function which prints out the alarm setting buttons.
{
 printincrement();
 M5.Lcd.setCursor(200, 50);
 M5.Lcd.printf("Time : %02d:%02d\n", hours, minutes);
 
}

void connectWiFi(const char* ssid, const char* password) {
 Serial.printf("Connecting to %s ", ssid);
 WiFi.begin(ssid, password);
 while (WiFi.status() != WL_CONNECTED) {
 delay(500);
 Serial.print(".");
 }
 Serial.println(" CONNECTED");
}

void disconnectWiFi(void) {
 WiFi.disconnect(true);
 WiFi.mode(WIFI_OFF);
}

void setRTCDate(const struct tm& timeInfo) {//important for synchronizing the RTC clock with abu dhabi time
 static RTC_DateTypeDef d;

 d.WeekDay = timeInfo.tm_wday;
 d.Month = timeInfo.tm_mon + 1;
 d.Date = timeInfo.tm_mday;
 d.Year = timeInfo.tm_year + 1900;
 M5.Rtc.SetDate(&d);
}

void setRTCTime(const struct tm& timeInfo) {//important for synchronizing the RTC clock with abu dhabi time
 static RTC_TimeTypeDef t;

 t.Hours = timeInfo.tm_hour;
 t.Minutes = timeInfo.tm_min;
 t.Seconds = timeInfo.tm_sec;
 M5.Rtc.SetTime(&t);
}

void onBeatDetected()
{
 Serial.println("Beat!");
}

bool setRTC(const char* tz, const char* server) {//important for synchronizing the RTC clock with abu dhabi time
 static struct tm timeInfo;

 connectWiFi(ssid, password);
 configTzTime(tz, server);
 const bool isSucceeded = getLocalTime(&timeInfo);
 if (isSucceeded) {
 setRTCDate(timeInfo);
 setRTCTime(timeInfo);
 }
 return isSucceeded;
}

void getRTC(RTC_DateTypeDef& d, RTC_TimeTypeDef& t) {//important for synchronizing the RTC clock with abu dhabi time
 M5.Rtc.GetDate(&d);
 M5.Rtc.GetTime(&t);
}

void printDateTime(const RTC_DateTypeDef& d, const RTC_TimeTypeDef& t) { //this is a function that prints out the RTC time. Not used in our main code but still helpful if needed.
 static const char *wd[] = {"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"};

 M5.Lcd.printf("Date : %04d/%02d/%02d(%s)\n", d.Year, d.Month, d.Date, wd[d.WeekDay]);
 M5.Lcd.printf("Time : %02d:%02d:%02d\n", t.Hours, t.Minutes, t.Seconds);
}
void checktime()//checks whether the alarm set by the user equals the RTC clock
{
 if (checktimer == 1) {
 
 getRTC(rtcDate, rtcTime);

 if (rtcTime.Hours==hours && rtcTime.Minutes ==minutes){
 Serial.println("sending email");
 sendemail();
 checktimer = false;
 }
 }
 
}

/* Callback function to get the Email sending status */
void smtpCallback(SMTP_Status status){
 /* Print the current status */
 Serial.println(status.info());

 /* Print the sending result */
 if (status.success()){
 Serial.println("----------------");
 ESP_MAIL_PRINTF("Message sent success: %d\n", status.completedCount());

 ESP_MAIL_PRINTF("Message sent failled: %d\n", status.failedCount());
 Serial.println("Message sent succesful!");
 Serial.println("----------------\n");
 struct tm dt;

 for (size_t i = 0; i < smtp.sendingResult.size(); i++){
 /* Get the result item */
 SMTP_Result result = smtp.sendingResult.getItem(i);
 time_t ts = (time_t)result.timestamp;
 localtime_r(&ts, &dt);

 ESP_MAIL_PRINTF("Message No: %d\n", i + 1);
 ESP_MAIL_PRINTF("Status: %s\n", result.completed ? "success" : "failed");
 ESP_MAIL_PRINTF("Date/Time: %d/%d/%d %d:%d:%d\n", dt.tm_year + 1900, dt.tm_mon + 1, dt.tm_mday, dt.tm_hour, dt.tm_min, dt.tm_sec);
 ESP_MAIL_PRINTF("Recipient: %s\n", result.recipients.c_str());
 ESP_MAIL_PRINTF("Subject: %s\n", result.subject.c_str());
 }
 Serial.println("----------------\n");
 }
}

void sendemail()//function which sends an email to the user to remind them to take their medication. 
{
 smtp.debug(1);

 /* Set the callback function to get the sending results */
 smtp.callback(smtpCallback);

 /* Declare the session config data */
 ESP_Mail_Session session;

 /* Set the session config */
 session.server.host_name = SMTP_HOST;
 session.server.port = SMTP_PORT;
 session.login.email = AUTHOR_EMAIL;
 session.login.password = AUTHOR_PASSWORD;
 session.login.user_domain = "";

 /* Declare the message class */
 SMTP_Message message;

 /* Set the message headers */
 message.sender.name = "ESP";
 message.sender.email = AUTHOR_EMAIL;
 message.subject = "ESP Test Email";
 message.addRecipient("Dheyab", RECIPIENT_EMAIL);
 

 String htmlMsg = "this is a reminder for the user to take their medication. Please take your [REDACTED] medicine. sent from an ESP32 Board";
 message.html.content = htmlMsg.c_str();
 message.html.content = htmlMsg.c_str();
 message.text.charSet = "us-ascii";
 message.html.transfer_encoding = Content_Transfer_Encoding::enc_7bit;


 /* Connect to server with the session config */
 if(!smtp.connect(&session))
 return;

 /* Start sending Email and close the session */
 if (!MailClient.sendMail(&smtp, &message))
 Serial.println("Error sending Email, " + smtp.errorReason());
}
void sleep() {
M5.Axp.DeepSleep(SLEEP_SEC(5)); //Wake up after 5 seconds of deep sleep, the CPU will reboot and the program will start from the beginning. 
}
//Main function for detection of heart attacks
void heart_attack_detection()
{
int control_value{0};
int time_control{0};
int counter_consec{0};
double average1{0};
int detection=0;
double difference{-100};
 M5.begin();
 //Connecting to the heart sensor
 Serial.begin(115200);
 Serial.print("Initializing pulse oximeter..");
 delay(3000);

 // Initialize the PulseOximeter instance
 // Failures are generally due to an improper I2C wiring, missing power supply
 // or wrong target chip
 if (!pox.begin()) {
 Serial.println("FAILED");
 for(;;);
 } else {
 Serial.println("SUCCESS");
 }
 pox.setIRLedCurrent(MAX30100_LED_CURR_7_6MA);
 // Register a callback for the beat detection
 pox.setOnBeatDetectedCallback(onBeatDetected);
 //Keeps running while time_control is equal to zero.For this specific program,we want it to run while heart attack not detected.
 while (time_control==0)
 {
 
 pox.update();
 if (millis() - tsLastReport > REPORTING_PERIOD_MS) {
 Serial.print("Heart rate:");
 Serial.print(pox.getHeartRate());
 Serial.print("bpm / SpO2:");
 x=pox.getHeartRate();
 
 File outputFile = SD.open("/file.txt", FILE_WRITE);

 outputFile.println(x);
 
 
 Serial.print(pox.getSpO2());
 Serial.println("%");
 //Getting sum of all heart rates
 sum = sum + pox.getHeartRate();
 //Incrementing counter by 1
 counter = counter +1;
 //Checking if counter is equal to 15
 if (counter==15)
 {
 
 Serial.print(" The average is : ");
 average = sum/counter;
 Serial.print(average);
  //initializing counter and sum to zero after calculating the averages
 counter = 0;
 sum =0;
 if (counter_consec==0) //if counter_consec is 1 ,this means average1 and average are storing the same value
 {
 //keeping value of average in average 1.This will be used for later comparison next time conditions for comparison is required
 average1=average;

 counter_consec=counter_consec+1; 
 }
 else
 {
 counter_consec=0;
 }
 //Checking if two consecutive averages are lower than lower limit
 if ((counter_consec==0) && (average1<=lower_limit) && (average<=lower_limit))
 {
 //If attack detected, the following piece of code is activated
 int ccounter(0);
 while (detection==0 || ccounter != 2)
 {
 int attack=1;
 
 //M5.update();
 M5.Lcd.clear(RED);
 M5.Axp.SetLDOEnable(3, true); //Open the vibration. 
 delay(1000);
 M5.Axp.SetLDOEnable(3, false); //Open the vibration. 
 delay(1000);
 ccounter++;
 if (ccounter==2)
 {
 detection=1;
 sendemailHA();
 sleep();
 
 }
 }
 sleep();
 }
 //Checking if upper_limit of heart attack has been reached and launching procedure when heart attack has been detected.
 if ((counter_consec==0) && (average1>=upper_limit) && (average>=upper_limit))
 {
 int ccounter = 0;
 while (detection==0 || ccounter!=2)
 {
 int attack=1;
 //M5.update();
 M5.Lcd.clear(RED);
 M5.Axp.SetLDOEnable(3, true); //Open the vibration. 
 delay(1000);
 M5.Axp.SetLDOEnable(3, false); //Open the vibration. 
 delay(1000);
 if (ccounter==2)
 {
 detection=1;
 sleep();
 
 }
ccounter++; 
 } 
 sleep();
 }

 }
 //Printing out the information on the M5 Stack about heart rate and breath rate of user
 M5.lcd.clear();
 M5.Lcd.setCursor(10, 10);
 M5.Lcd.setTextColor(GREEN);
 M5.lcd.printf("Heart rate:");
 M5.Lcd.setCursor(180, 10);
 M5.lcd.print(pox.getHeartRate());
 int breath_rate = (pox.getHeartRate()*conversion_rate);
 M5.Lcd.setCursor(10, 50);
 M5.Lcd.setTextColor(GREEN);
 M5.lcd.printf("Conversion rate:");
 M5.Lcd.setCursor(220, 50);
 M5.lcd.print(conversion_rate);
 M5.Lcd.setCursor(10, 100);
 M5.lcd.printf("Breath rate");
 M5.Lcd.setCursor(180, 100);
 M5.lcd.print(breath_rate);
 M5.lcd.setCursor(10,150);
 M5.lcd.printf("Average");
 M5.lcd.setCursor(180,150);
 M5.lcd.print(average);
 Serial.print(breath_rate);
 
 
 tsLastReport = millis();

 if (difference==0)
 {
 M5.Lcd.clear(WHITE);
 M5.Lcd.setCursor(0, 10);
 M5.Lcd.setTextSize(4);
 M5.Lcd.setTextColor(RED);
 M5.Lcd.printf("The practice is over");
 time_control=1;
 control_value=2;
 M5.Spk.begin(); // Initialize the speaker.
 M5.Spk.DingDong();
 sleep();
 }
 
 }
 } 
}
void connectwifi()
{
 int sum = 0;
 M5.begin(); // Init M5Core. 
 
 WiFiMulti.addAP(
 "iPhone (8)",
 "nugget69"); // Add wifi configuration information. 
 M5.lcd.printf(
 "Waiting connect to WiFi: %s ...",
 ssid); // Serial port output format string. 
 while (WiFiMulti.run() !=
 WL_CONNECTED) { // If the connection to wifi is not established
 // successfully. 
 Serial.println("Still not connected ");
 delay(1000);
 sum += 1;
 if (sum == 8) M5.lcd.print("Conncet failed!");
 }
 M5.lcd.println("\nWiFi connected");
 M5.lcd.print("IP address: ");
 M5.lcd.println(WiFi.localIP()); // The serial port outputs the IP address // of the M5Core. 
 M5.Lcd.clear(BLACK);
}

//Algorithm for stress relief 
void relaxation_algorithm()
{
int control_value{0};
int time_control{0};
int counter_consec{0};
double average1{0};
//  Connecting to the heart sensor
 double difference{-100};
 Serial.begin(115200);
 Serial.print("Initializing pulse oximeter..");
 delay(3000);
 // Initialize the PulseOximeter instance
 // Failures are generally due to an improper I2C wiring, missing power supply
 // or wrong target chip
 if (!pox.begin()) {
 Serial.println("FAILED");
 for(;;);
 } else {
 Serial.println("SUCCESS");
 }
 pox.setIRLedCurrent(MAX30100_LED_CURR_7_6MA);
 // Register a callback for the beat detection
 pox.setOnBeatDetectedCallback(onBeatDetected);
  //The loop will keep on running as long as time_control is zero.Time_control is actually controlled by a timer here
 while (time_control==0)
 {
 
 pox.update();
 if (millis() - tsLastReport > REPORTING_PERIOD_MS) {
 Serial.print("Heart rate:");
 Serial.print(pox.getHeartRate());
 Serial.print("bpm / SpO2:");
 x=pox.getHeartRate();
 
 File outputFile = SD.open("/file.txt", FILE_WRITE);

 outputFile.println(x);
 
 
 Serial.print(pox.getSpO2());
 Serial.println("%");
 sum = sum + pox.getHeartRate();
 counter = counter +1;
  //Calculating averages after every 10 readings
 if (counter==10)
 {
 
 Serial.print(" The average is : ");
 average = sum/counter;
 Serial.print(average);
 counter = 0;
 sum =0;
 }
 //If average is greater than 120,screen will flash red followed by black
 if (average>120)
 {
 M5.Lcd.clear(RED); 
 M5.Lcd.clear(BLACK);
 }
 //if average is greater than 60,screen will flash yellow and black
 else if (average>60)
 {
 M5.Lcd.clear(YELLOW); 
 M5.Lcd.clear(BLACK);
 }
 //if average is greater than 30,screen will flash green
 else if (average>30)
 {
 M5.Lcd.clear(GREEN); 
 M5.Lcd.clear(BLACK);
 }


 tsLastReport = millis();
 M5.Rtc.GetTime(&TimeStruct); 
 M5.Lcd.clear(BLACK);
 M5.Lcd.setCursor(10, 200);
 M5.Lcd.printf("Time: %02d : %02d : %02d/n",TimeStruct.Hours, TimeStruct.Minutes, TimeStruct.Seconds);
 //Checking if timer is equal to 1 minute
 difference=TimeStruct.Seconds-59;
 //If One minute has passed since the beginning of the practice,the device will print it's the end of the practice and reboot   
 if (difference==0)
 {
 M5.Lcd.clear(WHITE);
 M5.Lcd.setCursor(0, 10);
 M5.Lcd.setTextSize(1);
 M5.Lcd.setTextColor(RED);
 M5.Lcd.printf("The practice is over");
 delay(3000);
 time_control=1;
 control_value=2;
 M5.Spk.begin(); // Initialize the speaker. 
 M5.Spk.DingDong();
 //sleep();
 M5.Lcd.clear(BLACK);
 sleep();
 }
 
 }
 } 
}

void breathExercise() {
 M5.Lcd.clear(TFT_BLACK);
 M5.Lcd.setTextSize(2);
 M5.Lcd.setCursor(60, 80);
 M5.Lcd.clear(TFT_BLACK);
/*disply a picture with instructions for box breathing*/
 M5.Lcd.drawJpgFile(SD,"/box1.jpg");
 delay(3000);
 int counter = 0;
while (counter<=1) {
/*First iteration for breathing in. Note that the picture for breathing in an breathing out repeats.*/
M5.Lcd.setTextColor(TFT_BLACK,TFT_WHITE);
M5.Lcd.clear(TFT_BLACK);
/*Upload a picture from SD card*/
M5.Lcd.drawJpgFile(SD,"/nature6.jpg");
M5.Lcd.setCursor(0, 60);
M5.Lcd.print("Breath in for four seconds");
/*Start vibration for the duration of breathing in*/
M5.Axp.SetLDOEnable(3, true);
/*Keep vibrating for 3 seconds*/
delay(3000);

M5.Lcd.clear(TFT_BLACK);
/*Upload a picture from SD card*/
M5.Lcd.drawJpgFile(SD,"/nature2.jpg");
M5.Lcd.setCursor(0, 60);
M5.Lcd.setTextColor(TFT_RED,TFT_WHITE);
M5.Lcd.println("Hold you breath for four seconds");
/*Stop vibration for the duration of holding the breath*/
M5.Axp.SetLDOEnable(3, false);
/*Keep the vibration off for 3 seconds*/
delay(3000);

M5.Lcd.clear(TFT_BLACK);
/*Upload a picture from SD card*/
M5.Lcd.drawJpgFile(SD,"/nature6.jpg");
M5.Lcd.setCursor(0, 60);
M5.Lcd.setTextColor(TFT_BLACK,TFT_WHITE);
M5.Lcd.println("Breath out for four seconds");
/*Start vibration for the duration of holding the breath*/
M5.Axp.SetLDOEnable(3, true);
/*Keep vibrating for 3 seconds*/ 
delay(3000);

M5.Lcd.clear(TFT_BLACK);
M5.Lcd.setCursor(0, 60);
/*Upload a picture from SD card*/
M5.Lcd.drawJpgFile(SD,"/nature2.jpg");
M5.Lcd.setTextColor(TFT_RED,TFT_WHITE);
M5.Lcd.println("Hold you breath for four seconds");
/*Stop vibration for the duration of holding the breath*/
M5.Axp.SetLDOEnable(3, false); 
/*Keep the vibration off for 3 seconds*/
delay(3000);

/*increment counter after each full iteration though the practice*/
counter++;
/*if the person practiced the box breathing for 3 iterations, exit the function*/

}
M5.Lcd.clear(BLACK);
delay(500);
M5.Lcd.println("thank you for taking a breath break");
delay(2000);
M5.Lcd.clear(BLACK);
printfunctionsmenu();
}


void time() {
M5.begin();
TimeStruct.Hours = 0;
TimeStruct.Minutes = 0;
TimeStruct.Seconds = 0;
M5.Rtc.SetTime(&TimeStruct);
}
void sendemailHA()/*this sends an email to the user's guardian and alerts them that the user experienced a heart attack. 
this function is called in the heart attack detection algorithm.*/

{
 smtp.debug(1);

 /* Set the callback function to get the sending results */
 smtp.callback(smtpCallback);

 /* Declare the session config data */
 ESP_Mail_Session session;

 /* Set the session config */
 session.server.host_name = SMTP_HOST;
 session.server.port = SMTP_PORT;
 session.login.email = AUTHOR_EMAIL;
 session.login.password = AUTHOR_PASSWORD;
 session.login.user_domain = "";

 /* Declare the message class */
 SMTP_Message message;

 /* Set the message headers */
 message.sender.name = "ESP";
 message.sender.email = AUTHOR_EMAIL;
 message.subject = "ESP Test Email";
 message.addRecipient("Dheyab", RECIPIENT_EMAIL);
 

 String htmlMsg = "This is to alert the user's guardian that the user underwent a heartattack. Please check on the patient. sent from an ESP32 Board";
 message.html.content = htmlMsg.c_str();
 message.html.content = htmlMsg.c_str();
 message.text.charSet = "us-ascii";
 message.html.transfer_encoding = Content_Transfer_Encoding::enc_7bit;

 

 /* Connect to server with the session config */
 if(!smtp.connect(&session))
 return;

 /* Start sending Email and close the session */
 if (!MailClient.sendMail(&smtp, &message))
 Serial.println("Error sending Email, " + smtp.errorReason());
}
