#include "include/board.h"
#include "lib/io.h"
#include "lib/uart.h"
#include "lib/util.h"
#include "lib/i2c.h"
#include "lib/timer.h"
#include "lib/timer.h"
#include "libshield/SI1151.h"

#define delay_us(us) timer_wait_us(_TIM3, us)

volatile char cmd;

static void on_cmd_received(char c)
{
    cmd = c;
}

uint16_t ir_light;
uint16_t vis_light;

int main(void)
{

    uart_init(_USART2, 115200, UART_8N1, on_cmd_received);
    int ress = i2c_master_init(_I2C1);
    SI1151_getID();
    // uart_printf(_USART2,"\r\n Hello World i2c=%d",ress);
    SI1151_init();

    while (1)
    {

        // wait a 1 second
        delay_us(1000000);
        delay_us(1000000);
        SI1151_readIrLight(&ir_light);
        SI1151_readVisLight(&vis_light);
        uart_printf(_USART2, "\n \r%d ", ir_light);
        uart_printf(_USART2, "\n \r%d ", vis_light);
        delay_us(1000000);
        delay_us(1000000);
        delay_us(1000000);

        // blocking while, waiting to receive a character
        // while (!cmd) ;
        /* switch (cmd) {

             case 'i':
                 SI1151_readIrLight(&ir_light);
                 uart_printf(_USART2,"\n \r%d ",ir_light);
                 cmd = 0;
                 break;

             case 'v':
                 SI1151_readVisLight(&vis_light);
                 uart_printf(_USART2,"\n \r%d ",vis_light);
                 cmd = 0;
                 break;

             default:

                 break;
         }*/
    }

    return 0;
}
