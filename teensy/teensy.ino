/*
 * rosserial Servo Control Example
 *
 * This sketch demonstrates the control of hobby R/C servos
 * using ROS and the arduiono
 * 
 * For the full tutorial write up, visit
 * www.ros.org/wiki/rosserial_arduino_demos
 *
 * For more information on the Arduino Servo Library
 * Checkout :
 * http://www.arduino.cc/en/Reference/Servo
 */

//#define USE_TEENSY_HW_SERIAL

#if (ARDUINO >= 100)
 #include <Arduino.h>
#else
 #include <WProgram.h>
#endif

#include <Servo.h> 
#include <ros.h>
#include <std_msgs/Float64.h>

#define min(a,b) \
   ({ __typeof__ (a) _a = (a); \
       __typeof__ (b) _b = (b); \
     _a < _b ? _a : _b; })

#define max(a,b) \
   ({ __typeof__ (a) _a = (a); \
       __typeof__ (b) _b = (b); \
     _a > _b ? _a : _b; })

#define AUTO_DETACH     false
#define MAX_ANGLE       179
#define MIN_ANGLE       1
#define DEFAULT_ANGLE   90

#define servoHLu_PIN  4
#define servoHLd_PIN  3
#define servoHRu_PIN  6
#define servoHRd_PIN  5
#define servoFLu_PIN  22
#define servoFLd_PIN  23
#define servoFRu_PIN  20
#define servoFRd_PIN  21

ros::NodeHandle  nh;

Servo servoFRu;
Servo servoFLu;
Servo servoFRd;
Servo servoFLd;
Servo servoHRu;
Servo servoHLu;
Servo servoHRd;
Servo servoHLd;

void auto_detach(Servo* servo, int pin, double data) {
  
    const int attach_threshold = 2;
    const int detach_threshold = 10;
    
    if(data > attach_threshold && !servo->attached()) {
      servo->attach(pin);
    } else if(data < detach_threshold && servo->attached()) {
      servo->detach();
    }
}

void servo_uR(const std_msgs::Float64& cmd_msg) {
  if(AUTO_DETACH) {
    auto_detach(&servoFRu, servoFRu_PIN, (double) cmd_msg.data);
  }
  servoFRu.write((double) min(max(90+cmd_msg.data,MIN_ANGLE),MAX_ANGLE));
}

void servo_uL(const std_msgs::Float64& cmd_msg) {
  if(AUTO_DETACH) {
    auto_detach(&servoFLu, servoFLu_PIN, (double) cmd_msg.data);
  }
  servoFLu.write((double) min(max(90+cmd_msg.data,MIN_ANGLE),MAX_ANGLE));
}

void servo_fR(const std_msgs::Float64& cmd_msg) {
  if(AUTO_DETACH) {
    auto_detach(&servoFRd, servoFRd_PIN, (double) cmd_msg.data);
  }
  servoFRd.write((double) min(max(90-cmd_msg.data,MIN_ANGLE),MAX_ANGLE));
}

void servo_fL(const std_msgs::Float64& cmd_msg) {
  if(AUTO_DETACH) {
    auto_detach(&servoFLd, servoFLd_PIN, (double) cmd_msg.data);
  }
  servoFLd.write((double) min(max(90+cmd_msg.data,MIN_ANGLE),MAX_ANGLE));
}

void servo_sR(const std_msgs::Float64& cmd_msg) {
  if(AUTO_DETACH) {
    auto_detach(&servoHLu, servoHLu_PIN, (double) cmd_msg.data);
  }
  servoHRu.write((double) min(max(90-cmd_msg.data,MIN_ANGLE),MAX_ANGLE));
}

void servo_sL(const std_msgs::Float64& cmd_msg) {
  if(AUTO_DETACH) {
    auto_detach(&servoHLu, servoHLu_PIN, (double) cmd_msg.data);
  }
  servoHLu.write((double) min(max(90+cmd_msg.data,MIN_ANGLE),MAX_ANGLE));
}

void servo_lR(const std_msgs::Float64& cmd_msg) {
  if(AUTO_DETACH) {
    auto_detach(&servoHRd, servoHRd_PIN, (double) cmd_msg.data);
  }
  servoHRd.write((double) min(max(90-cmd_msg.data,MIN_ANGLE),MAX_ANGLE));
}

void servo_lL(const std_msgs::Float64& cmd_msg) {
  if(AUTO_DETACH) {
    auto_detach(&servoHLd, servoHLd_PIN, (double) cmd_msg.data);
  }
  servoHLd.write((double) min(max(90+cmd_msg.data,MIN_ANGLE),MAX_ANGLE));
}


ros::Subscriber<std_msgs::Float64> servoUR("/robot/upper_arm_R_joint/cmd_pos", servo_uR);
ros::Subscriber<std_msgs::Float64> servoUL("/robot/upper_arm_L_joint/cmd_pos", servo_uL);
ros::Subscriber<std_msgs::Float64> servoFR("/robot/forearm_R_joint/cmd_pos", servo_fR);
ros::Subscriber<std_msgs::Float64> servoFL("/robot/forearm_L_joint/cmd_pos", servo_fL);
ros::Subscriber<std_msgs::Float64> servoSR("/robot/shin_R_joint/cmd_pos", servo_sR);
ros::Subscriber<std_msgs::Float64> servoSL("/robot/shin_L_joint/cmd_pos", servo_sL);
ros::Subscriber<std_msgs::Float64> servoLR("/robot/shin_lower_R_joint/cmd_pos", servo_lR);
ros::Subscriber<std_msgs::Float64> servoLL("/robot/shin_lower_L_joint/cmd_pos", servo_lL);


void setup(){
  
  // Board LED
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH-digitalRead(13));

  nh.initNode();
  nh.subscribe(servoFR);
  nh.subscribe(servoFL);
  nh.subscribe(servoUR);
  nh.subscribe(servoUL);
  nh.subscribe(servoSR);
  nh.subscribe(servoSL);
  nh.subscribe(servoLR);
  nh.subscribe(servoLL);

  if(!AUTO_DETACH) {
    servoHLu.attach(servoHLu_PIN);
    servoHLd.attach(servoHLd_PIN);
    servoHRu.attach(servoHRu_PIN);
    servoHRd.attach(servoHRd_PIN);
    servoFLu.attach(servoFLu_PIN);
    servoFLd.attach(servoFLd_PIN);
    servoFRu.attach(servoFRu_PIN);
    servoFRd.attach(servoFRd_PIN);

    servoHLu.write(DEFAULT_ANGLE);
    servoHLd.write(DEFAULT_ANGLE);
    servoHRu.write(DEFAULT_ANGLE);
    servoHRd.write(DEFAULT_ANGLE);
    servoFLu.write(DEFAULT_ANGLE);
    servoFLd.write(DEFAULT_ANGLE);
    servoFRu.write(DEFAULT_ANGLE);
    servoFRd.write(DEFAULT_ANGLE);
  }
    
}

void loop(){
  nh.spinOnce();
  delay(1);
}
