int feedmot=5,cb2sensor1out=12,cb1sensor1out=7,seesaw1=2,seesaw2=4,cbout1=10,photorelay=3,cbout2=9,phase_status_pin=13,led=11;  //cb2sensor2out=8,
//cbsensor1in=A0
//to connserve pins cbsensor2=7 and feedmot2=6 can be grounded

void setup() 
{
  Serial.begin(9600);
  pinMode(feedmot,OUTPUT);
  pinMode(seesaw1,OUTPUT);
  pinMode(seesaw2,OUTPUT);
  pinMode(A0,INPUT);
  pinMode(A1,INPUT);
  pinMode(A2,INPUT);
  pinMode(cb1sensor1out,OUTPUT);
  pinMode(cb2sensor1out,OUTPUT);
  pinMode(cbout1,OUTPUT);
  pinMode(cbout2,OUTPUT);
  pinMode(photorelay,OUTPUT);
  pinMode(phase_status_pin,INPUT);
  pinMode(led,OUTPUT);
  
  
}
int delay_time_for_seesaw_motor=1000;     // change accordingly
char current_seesaw_status = 'b';
int ir_sensor_delay_time =1;             // change accordingly
int photo_relay_time = 50;                // change accordingly

void change_seesaw_status(char status)  // takes char 'b' or 'f' as input
{
  if (status=='b')
  {
    if(current_seesaw_status==status)
    {
      
    }
    else 
    {
      digitalWrite(seesaw1,LOW);
      digitalWrite(seesaw2,HIGH);
      delay (delay_time_for_seesaw_motor);    
      digitalWrite(seesaw1,LOW);
      digitalWrite(seesaw2,LOW);
      current_seesaw_status = 'b';
    }
  }
   if (status=='f')
   {
    if(current_seesaw_status==status)
    {
      
    }
    else 
    {
      digitalWrite(seesaw1,HIGH);
      digitalWrite(seesaw2,LOW);
      delay (delay_time_for_seesaw_motor);
      digitalWrite(seesaw1,LOW);
      digitalWrite(seesaw2,LOW);
      current_seesaw_status = 'f';
    }
  }
}




void loop() {
 bool phase_status = digitalRead(phase_status_pin); 
if (phase_status==0)
{
  digitalWrite(feedmot,HIGH);
  digitalWrite(cb1sensor1out,HIGH);
  digitalWrite(cb2sensor1out,HIGH);
  //digitalWrite(cb2sensor2out,HIGH);
  digitalWrite(cbout1,LOW);
  digitalWrite(cbout2,HIGH);
  digitalWrite(photorelay,LOW);
  digitalWrite(led,LOW);
  
  
  change_seesaw_status('f');

  
  while (1)
  {
    int value=analogRead(A0);
    if(value >= 500)
    {
      delay(ir_sensor_delay_time);
    }
    else 
    {
      Serial.write("cb1sensor1 executed\n");
      break;
    }
  }
  digitalWrite(cbout2,LOW);
  change_seesaw_status('b');
  

  while (1)
  {
    int value1=analogRead(A1);
    if(value1 >= 500)
    {
      delay(ir_sensor_delay_time);
    }
    else  
    {
      Serial.write("cb2sensor1 executed for the first time\n");
      while (1)
      {
        value1=analogRead(A1);
        if (value1 <= 500)
        {
          delay (ir_sensor_delay_time); 
        }
        else 
        {
          Serial.write("cb2sensor1 executed for the second time\n");
          break;
        }
      }
      break; 
    }
  }
  delay(100);
  digitalWrite(cbout1,HIGH);
  digitalWrite(cbout2,HIGH);
  delay(2000);
  digitalWrite(photorelay,HIGH);
  delay(photo_relay_time);
  digitalWrite(photorelay,LOW);
  delay(2000);
  digitalWrite(cbout1,LOW);
  digitalWrite(cbout2,LOW);
  digitalWrite(led,HIGH);
  delay(3000); 
  digitalWrite(led,LOW);
 
}
else {
  change_seesaw_status('f');
  digitalWrite(feedmot,HIGH);
  digitalWrite(cb1sensor1out,LOW);
  digitalWrite(cb2sensor1out,LOW);
  digitalWrite(cbout1,LOW);
  digitalWrite(cbout2,LOW);
  digitalWrite(photorelay,LOW);
  digitalWrite(led,LOW);
  
}
}
