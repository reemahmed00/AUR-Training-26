#include <avr/io.h>
#include <avr/interrupt.h> 

// runs when the button is pressed
ISR(INT0_vect) {
    PORTB ^= (1 << PB0); // Toggle PB0
}

int main(void) {
    // led (PB0) as output
    DDRB |= (1 << PB0);
    PORTB &= ~(1 << PB0); // Ensure led starts OFF bit-masking 

    // Button (PD2/INT0) as input
    DDRD &= ~(1 << PD2); 
    PORTD |= (1 << PD2); //internal pull-up resistor

    // INT0 to trigger on FALLING EDGE
    // ISC01 = 1, ISC00 = 0
    MCUCR |= (1 << ISC01);
    MCUCR &= ~(1 << ISC00);

    // INT0 in the General Interrupt Control Register
    GICR |= (1 << INT0); 

    sei(); 

    while (1) {
        // The CPU will just sit here, waiting for the button press
    }
    
    return 0;
}