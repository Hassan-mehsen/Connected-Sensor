#include "SI1151.h"
#include "lib/i2c.h"
#include "lib/uart.h"
#include "lib/timer.h"

#define delay_us(us) timer_wait_us(_TIM3, us)

bool SI1151_getID(void)

{
	// This function is impleted to verify the identity of the sensor
	int i2c_status;
	uint8_t buff[1];
	buff[0] = SI1151_PART_ID;
	buff[0] = SI1151_readRegister8(SI1151_PART_ID);

	if (buff[0] != 0x51)
	{
		uart_printf(_USART2, "\r\nID not confirmed please connect the right sensor 'SI1151' ");
		return false;
	}

	else
	{
		uart_puts(_USART2, "\r\nBuilding a more connected world !");
		return true;
	}
}

void SI1151_SetParam(uint8_t reg, uint8_t value)
{
	uint8_t buff[2];
	int cmd_ctr = 0;
	int counter = 0;
	int i2c_status = -9;
	buff[0] = SI1151_RESPONSE_0;

	do
	{

		// reading the value of the counter in RESPONSE0 register and storing this value in cmd_ctr
		i2c_status = i2c_read(I2C1, SI1151_ADDR, buff, 1);
		if (i2c_status != I2C_OK)
		{
			uart_printf(_USART2, "\n \r Error while first reading in SI1151_SetParam function , i2c=%d", i2c_status);
		}
		cmd_ctr = buff[0];

		// writting the value in HOSTIN0 register to bo transfered by the command register to the wanted parameter
		buff[0] = SI1151_HOSTIN_0;
		buff[1] = value;

		i2c_status = i2c_write(I2C1, SI1151_ADDR, buff, 2);
		if (i2c_status != I2C_OK)
		{
			uart_printf(_USART2, "\n \r Error while first wrinting in SI1151_SetParam function , i2c=%d", i2c_status);
		}

		SI1151_Reset(SI1151_RESET_CMD_CTR);

		// point on the wanted parameter
		buff[0] = SI1151_COMMAND;
		buff[1] = (reg | (0x2 << 6));

		i2c_status = i2c_write(I2C1, SI1151_ADDR, buff, 2);
		if (i2c_status != I2C_OK)
		{
			uart_printf(_USART2, "\n \r Error while second wrinting in SI1151_SetParam function , i2c=%d", i2c_status);
		}

		// reading the value of the counter in RESPONSE0 register after sending the command and storing this value in counter (cmd_ctr should be less than counter)
		buff[0] = SI1151_RESPONSE_0;
		i2c_status = i2c_read(I2C1, SI1151_ADDR, buff, 1);
		if (i2c_status != I2C_OK)
		{
			uart_printf(_USART2, "\n \r Error while second reading in SI1151_SetParam function , i2c=%d", i2c_status);
		}
		counter = buff[0];

	} while (counter > cmd_ctr);
}

void SI1151_writeToTheCommandRegister(uint8_t value_to_write)
{
	int i2c_status = -9;
	uint8_t buff[2];
	int cmd_ctr = 0;
	int counter = 0;
	buff[0] = SI1151_RESPONSE_0;

	SI1151_Reset(SI1151_RESET_CMD_CTR);

	do
	{
		i2c_status = i2c_read(I2C1, SI1151_ADDR, buff, 1);
		delay_us(50);
		if (i2c_status != I2C_OK)
		{
			uart_printf(_USART2, "\n \r Error while first reading in SI1151_SetParam function , i2c=%d", i2c_status);
		}
		cmd_ctr = buff[0];

		buff[0] = SI1151_COMMAND;
		buff[1] = value_to_write;

		i2c_status = i2c_write(I2C1, SI1151_ADDR, buff, 2);
		if (i2c_status != I2C_OK)
		{
			uart_printf(_USART2, "\n \r Error while first wrinting in SI1151_writeToTheCommandRegister, i2c=%d", i2c_status);
		}

		buff[0] = SI1151_RESPONSE_0;
		i2c_status = i2c_read(I2C1, SI1151_ADDR, buff, 1);
		delay_us(50);
		if (i2c_status != I2C_OK)
		{
			uart_printf(_USART2, "\n \r Error while second reading in SI1151_SetParam function , i2c=%d", i2c_status);
		}
		counter = buff[0];

	} while (counter > cmd_ctr);
}

uint8_t SI1151_readRegister8(uint8_t reg)
{
	int i2c_status;
	uint8_t buff[1] = {reg};
	uint8_t value_of_register;

	i2c_status = i2c_write(_I2C1, SI1151_ADDR, buff, 1);

	if (i2c_status != I2C_OK)
	{
		uart_printf(_USART2, "\n \r Error while wrinting in SI1145_readRegister function , i2c=%d", i2c_status);
	}

	delay_us(10);

	i2c_status = i2c_read(_I2C1, SI1151_ADDR, &value_of_register, 2);
	delay_us(50);

	if (i2c_status != I2C_OK)
	{
		uart_printf(_USART2, "\n \r Error while reading in SI1145_readRegister function, i2c=%d", i2c_status);
	}

	// value_of_register = (i2c_status==I2C_OK) ? buff[0] : 0 ;

	return value_of_register;
}

uint16_t SI1151_readRegister16(uint8_t reg)
{

	int i2c_status = -9;
	uint16_t x;
	uint8_t reg_data[1] = {reg};
	uint8_t data[2];

	i2c_status = i2c_write(I2C1, SI1151_ADDR, reg_data, 1);
	if (i2c_status != I2C_OK)
	{
		uart_printf(_USART2, "\n \r Error while wrinting in SI1151_readRegister16 function , i2c=%d", i2c_status);
	}

	i2c_status = i2c_read(_I2C1, SI1151_ADDR, data, 2);
	if (i2c_status != I2C_OK)
	{
		uart_printf(_USART2, "\n \r Error while reading in SI1151_readRegister16 function , i2c=%d", i2c_status);
	}
	delay_us(50);

	x = data[1];
	x <<= 8;
	x |= data[0];

	return x;
}

int SI1151_init(void)
{
	uint8_t buff[2];
	int i2c_status;

	delay_us(1000000);

	if (SI1151_getID() == false)
	{
		return -1;
	}

	// Standby mode
	SI1151_SetParam(SI1151_ADCCONFIG_0, 0x60);
	SI1151_SetParam(SI1151_MEASCONFIG_0, 0x00);
	SI1151_SetParam(SI1151_ADCPOST_0, 0x00);

	SI1151_SetParam(SI1151_ADCCONFIG_1, 0x61);
	SI1151_SetParam(SI1151_MEASCONFIG_1, 0x00);
	SI1151_SetParam(SI1151_ADCPOST_1, 0x00);

	SI1151_SetParam(SI1151_ADCCONFIG_2, 0x62);
	SI1151_SetParam(SI1151_MEASCONFIG_2, 0x00);
	SI1151_SetParam(SI1151_ADCPOST_2, 0x00);

	SI1151_SetParam(SI1151_ADCCONFIG_3, 0x6B);
	SI1151_SetParam(SI1151_MEASCONFIG_3, 0x00);
	SI1151_SetParam(SI1151_ADCPOST_3, 0x00);

	SI1151_SetParam(SI1151_ADCCONFIG_4, 0x6D);
	SI1151_SetParam(SI1151_MEASCONFIG_4, 0x00);
	SI1151_SetParam(SI1151_ADCPOST_4, 0x00);

	SI1151_writeToTheCommandRegister(SI1151_START);

	return 0;
}

void SI1151_readIrLight(uint16_t *ir)
{

	// write to the command register to exit the standby mode and enter the forced conversion mode

	SI1151_writeToTheCommandRegister(SI1151_FORCE);
	delay_us(50);

	// recover the data from the register

	uint8_t x = SI1151_readRegister8(SI1151_HOSTOUT_0);
	uint8_t y = SI1151_readRegister8(SI1151_HOSTOUT_1);

	*ir = y << 8;
	*ir = (y | x);
	
	if (*ir > 200 && *ir < 300)
	{
		*ir *= 3;
	}
	else if (*ir > 300 && *ir < 500)
	{
		*ir *= 5;
	}
	else if (*ir > 50 && *ir < 200)
	{
		*ir *= 2;
	}
}

void SI1151_readVisLight(uint16_t *vis)
{

	// write to the command register to exit the standby mode and enter the forced conversion mode
	SI1151_writeToTheCommandRegister(SI1151_FORCE);
	delay_us(50);

	// recover the data from the register
	uint8_t x = SI1151_readRegister8(SI1151_HOSTOUT_2);
	uint8_t y = SI1151_readRegister8(SI1151_HOSTOUT_3);

	*vis = y << 8;
	*vis = (y | x);
	
	if (*vis > 200 && *vis < 300)
	{
		*vis *= 3;
	}
	else if (*vis > 300 && *vis < 500)
	{
		*vis *= 5;
	}

	else if (*vis > 50 && *vis < 200)
	{
		*vis *= 2;
	}
}

void SI1151_Reset(uint8_t which_reset)
{
	uint8_t buff[2];
	int i2c_status = -9;

	buff[0] = SI1151_COMMAND;
	buff[1] = which_reset;

	i2c_status = i2c_write(I2C1, SI1151_ADDR, buff, 2);
	if (i2c_status != I2C_OK)
	{
		uart_printf(_USART2, "\n \r Error while first wrinting in SI1151_writeToTheCommandRegister, i2c=%d", i2c_status);
	}

	buff[0] = SI1151_RESPONSE_0;
	i2c_status = i2c_read(_I2C1, SI1151_ADDR, buff, 1);
	if (i2c_status != I2C_OK)
	{
		uart_printf(_USART2, "\n \r Error while reading in SI1145_readRegister function, i2c=%d", i2c_status);
	}

	if ((buff[0] << 4) != 0x00)
	{
		SI1151_Reset(which_reset);
	}
}
