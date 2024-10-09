#ifndef _SI1151_H_
#define _SI1151_H_

#include <stdint.h>
#include <stdbool.h>

#define SI1151_ADDR 0x53

/************	Command			**************/
#define SI1151_RESET_CMD_CTR 0x00
#define SI1151_RESET_SW 0x01
#define SI1151_FORCE 0x11
#define SI1151_PAUSE 0x12
#define SI1151_START 0x13
#define SI1151_PARAM_QUERY 0x40 // Reads the parameter register located at PARAM_ADDRESS and store results in RESPONSE1 the address is 0x40|PARAM_ADRRESS
#define SI1151_PARAM_SET 0x80   // Writes the value in INPUT0 to the parameter register located at PARAM_ADDRESS the address is 0x80|PARAM_ADRRESS

/************	Registers		*************/

#define SI1151_PART_ID 0x00

#define SI1151_HOSTIN_0 0x0A
#define SI1151_COMMAND 0x0B
#define SI1151_IRQ_ENABLE 0x0F
#define SI1151_RESPONSE_0 0x11
#define SI1151_RESPONSE_1 0x10

#define SI1151_IRQ_STATUS 0x12
#define SI1151_HOSTOUT_0 0x13
#define SI1151_HOSTOUT_1 0x14
#define SI1151_HOSTOUT_2 0x15
#define SI1151_HOSTOUT_3 0x16
#define SI1151_HOSTOUT_4 0x17
#define SI1151_HOSTOUT_5 0x18
#define SI1151_HOSTOUT_6 0x19
#define SI1151_HOSTOUT_7 0x1A
#define SI1151_HOSTOUT_8 0x1B
#define SI1151_HOSTOUT_9 0x1C
#define SI1151_HOSTOUT_10 0x1D
#define SI1151_HOSTOUT_11 0x1E
#define SI1151_HOSTOUT_12 0x1F
#define SI1151_HOSTOUT_13 0x20
#define SI1151_HOSTOUT_14 0x21
#define SI1151_HOSTOUT_15 0x22
#define SI1151_HOSTOUT_16 0x23
#define SI1151_HOSTOUT_17 0x24
#define SI1151_HOSTOUT_18 0x25
#define SI1151_HOSTOUT_19 0x26
#define SI1151_HOSTOUT_20 0x27
#define SI1151_HOSTOUT_21 0x28
#define SI1151_HOSTOUT_22 0x29
#define SI1151_HOSTOUT_23 0x2A
#define SI1151_HOSTOUT_24 0x2B
#define SI1151_HOSTOUT_25 0x2C

/************	Parameters		************/

#define SI1151_I2C_ADDR 0x00
#define SI1151_CHAN_LIST 0x01

#define SI1151_ADCCONFIG_0 0x02
#define SI1151_ADCSENS_0 0x03
#define SI1151_ADCPOST_0 0x04
#define SI1151_MEASCONFIG_0 0x05

#define SI1151_ADCCONFIG_1 0x06
#define SI1151_ADCPOST_1 0x08
#define SI1151_ADCSENS_1 0x07
#define SI1151_MEASCONFIG_1 0x09

#define SI1151_ADCCONFIG_2 0x0A
#define SI1151_ADCSENS_2 0x0B
#define SI1151_ADCPOST_2 0x0C
#define SI1151_MEASCONFIG_2 0x0D

#define SI1151_ADCCONFIG_3 0x0E
#define SI1151_ADCSENS_3 0x0F
#define SI1151_ADCPOST_3 0x10
#define SI1151_MEASCONFIG_3 0x11

#define SI1151_ADCCONFIG_4 0x12
#define SI1151_ADCSENS_4 0x13
#define SI1151_ADCPOST_4 0x14
#define SI1151_MEASCONFIG_4 0x15

#define SI1151_ADCCONFIG_5 0x16
#define SI1151_ADCSENS_5 0x17
#define SI1151_ADCPOST_5 0x18
#define SI1151_MEASCONFIG_5 0x19

#define SI1151_MEASRATE_H 0x1A
#define SI1151_MEASRATE_L 0x1B
#define SI1151_MEASCOUNT_0 0x1C
#define SI1151_MEASCOUNT_1 0x1D
#define SI1151_MEASCOUNT_2 0x1E

#define SI1151_LED1_A 0x1F
#define SI1151_LED1_B 0x20
#define SI1151_LED2_A 0x21
#define SI1151_LED2_B 0x22
#define SI1151_LED3_A 0x23
#define SI1151_LED3_B 0x24

#define SI1151_THRESHOLD0_H 0x25
#define SI1151_THRESHOLD0_L 0x26
#define SI1151_THRESHOLD1_H 0x27
#define SI1151_THRESHOLD1_L 0x28
#define SI1151_THRESHOLD2_H 0x29
#define SI1151_THRESHOLD2_L 0x2A

#define SI1151_BURST 0x2B

/**************************	Functions	****************************/
/**
 *
 *
 * */
bool SI1151_getID(void);

/**
 *
 *
 * */

int SI1151_init(void);

/**
 *
 *
 *  */
void SI1151_SetParam(uint8_t reg, uint8_t value);

/**
 *
 *
 * */
void SI1151_writeToTheCommandRegister(uint8_t value_to_write);

/**
 *
 *
 * */
uint8_t SI1151_readRegister8(uint8_t reg);

/**
 *
 *
 * */
uint16_t SI1151_readRegister16(uint8_t reg);

/**
 *
 *
 * */
void SI1151_readIrLight(uint16_t *ir);

/**
 *
 *
 * */

void SI1151_readVisLight(uint16_t *vis);

/**
 *
 *
 * */
void SI1151_Reset(uint8_t which_reset);

#endif