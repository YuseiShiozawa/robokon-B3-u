#include <Wire.h>                     // ライブラリのインクルード
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);  // PCA9685のI2Cアドレスを指定

#define SERVOMIN 500    // 最小パルス幅(μs)
#define SERVOMAX 2400   // 最大パルス幅(μs)


int Servo_pin0 = 0;      // サーボ接続ピンを0番に
int Servo_pin3 = 3;
int Servo_pin4 = 4;
int Servo_pin6 = 6;
int angle0;
int angle3;
int angle4;
int angle6;

void setup() {

  pwm.begin();         // 初期設定
  pwm.setPWMFreq(50);  // PWM周期を50Hzに設定
  delay(1000);
  
}

void loop() {
  
  angle0 = 210;
  angle0 = map(angle0,0, 180, 500, 2400);  // 角度(0~180)をパルス幅(500~2400μs)に変換
  pwm.writeMicroseconds(Servo_pin0, angle0);        // サーボを動作させる
  delay(2000);

  angle4 = 210;   //MAX 220,210=180do
  angle4 = map(angle4,0, 180, 500, 2400);  // 角度(0~180)をパルス幅(500~2400μs)に変換
  pwm.writeMicroseconds(Servo_pin4, angle4);        // サーボを動作させる
  delay(2000);

  angle6 = 0;   //MAX 220,210=180do
  angle6 = map(angle6,0, 180, 500, 2400);  // 角度(0~180)をパルス幅(500~2400μs)に変換
  pwm.writeMicroseconds(Servo_pin6, angle6);        // サーボを動作させる
  delay(2000);
  angle6 = 180;   //MAX 220,210=180do
  angle6 = map(angle6,0, 180, 500, 2400);  // 角度(0~180)をパルス幅(500~2400μs)に変換
  pwm.writeMicroseconds(Servo_pin6, angle6);        // サーボを動作させる
  delay(2000);


  /*angle0 = 180;
  angle0 = map(angle0,0,180, 500, 2400);
  pwm.writeMicroseconds(Servo_pin0, angle0);
  delay(2000);*/


  angle3 = 0;
  angle3 = map(angle3,0, 180, SERVOMIN, SERVOMAX);  // 角度(0~180)をパルス幅(500~2400μs)に変換
  pwm.writeMicroseconds(Servo_pin3, angle3);        // サーボを動作させる
  delay(1000);

  angle3 = 180;
  angle3 = map(angle3,0, 180, SERVOMIN, SERVOMAX);
  pwm.writeMicroseconds(Servo_pin3, angle3);
  delay(1000);

}
