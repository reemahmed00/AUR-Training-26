#include <avr/io.h>
#include<util/delay.h>

/*
1. f_PWM = 8 Mhz / (256 * 8)
2. Non-Inverted Duty Cycle = ((OCR + 1) / 256) * 100%
OCR0+1=(25*256)/100 THEN OCR0=63
     
 */
void fastPwm(void){
  //set OC0 == PB0 as output pin
  DDRB|=(1<<PB3);

  OCR0=63;
   TCCR0 = (1 << WGM00) | (1 << WGM01) | // Fast PWM Mode
            (1 << COM01) |                 // Non-Inverted (Clear OC0 on Compare)
            (1 << CS01);                   // Prescaler = 8 (CS01=1, CS00=0)

}
int main(void){
  //INIT FAST PWM 
  fastPwm();

  while(1){
    // increase brightness fade in
    for(uint8_t brightness = 63 ; brightness<255 ; brightness++ ){
      OCR0=brightness;
      _delay_ms(10);  // visible fade 
    }
   // fade out
    for(uint8_t brightness = 255; brightness > 63; brightness--){
      OCR0 = brightness;
      _delay_ms(10); // Wait 10ms for a visible fade
    }
      
  }

  return 0 ; 
}