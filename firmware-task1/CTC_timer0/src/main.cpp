#include <avr/io.h>
void to_delay_1ms_CTC(void){
  // set target to 124 [for 1ms with 64 prescaler at 8Mhz]
  OCR0=124;
  TCCR0 = (1<<WGM01) | (1<<CS01) | (1<<CS00); // CTC mode, Prescaler 64
  
  while((TIFR & (1<<OCF0)) == 0); // Wait for Output Compare Flag
  TCCR0 = 0; // Stop timer
  TIFR = (1<<OCF0); // Clear OCF0 flag

}
int main(void){
    //connect led to PB0
    DDRB|=(1<<0) ;// set PB0 as output  ['|' bitWise ope as setter]
    PORTB=0x00 ;//turn off initially
    
    while(1){
      //toggle ledd
      PORTB^=(1<<0); // xor bitwise ope used in toggling 
      
      // 500ms toggle period and we made a 1ms delay
      //then loop calling 1ms delay
      for(uint16_t i = 0 ; i<500 ; i++){
         to_delay_1ms_CTC();
      }
    }
  return 0;
}
