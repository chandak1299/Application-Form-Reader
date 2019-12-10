/* This program was created by ScottC on 8/5/2012 to receive serial 
signals from a computer to turn on/off 1-9 LEDs */
const int phase_status =13,stepPin = 9,dirPin = 8,led =2,ir_sensor=3;
const int capacity=60;
int arr[capacity];
int i =0;
bool status =0;
int current_position =1,steps=600;
int ir_sensor_delay_time =1;

void change_position(int new_position){
    int delta_position=new_position - current_position;
    bool dir=0;
    
    if (delta_position > 0) dir = 0;
    else dir = 1;
    
    digitalWrite(dirPin,dir);                                //Enables the motor to move in a perticular direction
                                                            // for one full rotation required 200 pulses
    for(int x = 0; x < (steps*abs(delta_position)); x++){
    digitalWrite(stepPin,HIGH);
    delayMicroseconds(500);
    digitalWrite(stepPin,LOW);
    delayMicroseconds(500);
    }
    current_position = new_position;
}

void setup() { 
   pinMode(phase_status,OUTPUT);
   pinMode(stepPin,OUTPUT);
   pinMode(dirPin,OUTPUT);
   pinMode(led,OUTPUT);
   pinMode(ir_sensor,OUTPUT);
   pinMode(A0,INPUT);
   Serial.begin(9600);
   byte byteRead;
   while (true){
    if (Serial.available()){
    byteRead = Serial.read();     //You have to subtract '0' from the read Byte to convert from text to a number.
    byteRead=byteRead-'0';
    arr[i]= byteRead;
    i++;
    if(i==(capacity - 1))
    {
      arr[capacity-1]=9;
      break;
      }
    else if (byteRead==9) 
    {
      arr[i]=9;
      break;
    }
   } 
   }
  digitalWrite(phase_status,HIGH);  
}
 

int j =0;
void loop() {
    
    if (j<capacity){
      if (arr[j]==9){
         j= capacity;
      }
      else change_position(arr[j]);
   /*   {
         digitalWrite(dirPin,1);                                //Enables the motor to move in a perticular direction
                                                            // for one full rotation required 200 pulses
    for(int x = 0; x < steps; x++){
    digitalWrite(stepPin,HIGH);
    delayMicroseconds(500);
    digitalWrite(stepPin,LOW);
    delayMicroseconds(500);
    }*/
      digitalWrite(ir_sensor,HIGH);
      digitalWrite(led,HIGH);
      delay(1000);
      digitalWrite(led,LOW);
      
    
    while (1){
    int value1=analogRead(A0);
    if(value1 >= 500)
    {
      delay(ir_sensor_delay_time);
    }
    else  
    {
      while (1)
      {
        value1=analogRead(A0);
        if (value1 <= 500)
        {
          delay (ir_sensor_delay_time); 
        }
        else 
        {
          break;
        }
      }
      break; 
    }
    }
    digitalWrite(ir_sensor,LOW);
    delay(2000);  
      j++; 
    }
  
 }
