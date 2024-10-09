import serial
import time
import threading
import save_data


"""
    this module is written to manage communication between the HMI and the S1151 sensor 
    in this module we recieve the data from the sensor and we process data and we send order to the sensor
    these features are managed in an asynchronous manner by a thread  

"""

class serial_link():
    def __init__(self,port_name,baude_rate):
        self.port_name=port_name
        self.baude_rate=baude_rate
        self.serial_link= None
        self.counter=0
        self.index=0
        self.stop_reading = False
        self.buffer_size= 6
        self.buffer_data=[None] * self.buffer_size
        self.List_size = 10
        self.IR_List=[None] * self.List_size
        self.VIS_List=[None]* self.List_size
        self.IR_List_index = 0
        self.VIS_List_index = 0
        self.IR_current_value=None
        self.VIs_current_value=None
        self.read_thread= None     
        

    def serialConnect(self):
        try:
            self.serial_link=serial.Serial(self.port_name,self.baude_rate,timeout=1)
            time.sleep(0.1)
            print("The carte is successfuly connected!")

        except serial.SerialException as e:
            print("Druring connection exception {}",e)


    
    def serialRead(self): 
        try:  
            self.serialConnect()
            while not self.stop_reading:
                 if self.serial_link.in_waiting > 0 :
                    data=self.serial_link.readline().decode('utf-8').replace('\r', '').strip()
                    self.buffer_data[self.index]=data
                    self.index = (self.index +1)% self.buffer_size
                    print(self.buffer_data)
                    self.dataClean()
                    time.sleep(1)
                    
        except Exception as e:
                print("exception : {}",e)

    
    def serialWrite(self,commad):
        try:
            self.serialConnect()
            self.stop_reading= True
            self.serial_link.write(commad.encode('utf-8'))
            print("The command ",commad," was sent")
        except Exception as e:
            print("Exception {}",e)
        finally:
            time.sleep(1)
            self.stop_reading= False
            self.serialClose()

    def serialReadThread(self):
        self.read_thread=threading.Thread(target=self.serialRead)
        self.read_thread.start()


    def serialClose(self):
        try:
            self.serial_link.close()
            print("The serial connection is closed")
        except Exception as e:
            print("During close Exception {}",e)


    def dataClean(self):
        #while self.serial_link : 
        if self.buffer_data[5]:

            for i in range (0,self.buffer_size-1):
                if (i%2 == 0):
                    self.IR_List[self.IR_List_index] = self.buffer_data[i]
                    self.IR_List[self.IR_List_index] = self.convert_to_int(self.IR_List[self.IR_List_index])
                    self.IR_current_value = self.IR_List[self.IR_List_index]
                    self.IR_List_index = (self.IR_List_index + 1) % self.List_size
                    #print(self.buffer_data[i])

                elif (i%2 != 0):
                    self.VIS_List[self.VIS_List_index] = self.buffer_data[i]
                    self.VIS_List[self.VIS_List_index] = self.convert_to_int(self.VIS_List[self.VIS_List_index])
                    self.VIs_current_value = self.VIS_List[self.VIS_List_index]
                    self.VIS_List_index = (self.VIS_List_index + 1) % self.List_size
                    #print(self.buffer_data[i])
            
            


    def save_data_to_db(self): #, column_1_name,column_2_name,data_1,data_2
        try:
            self.db = save_data.saveData("SI1151_Grove_Sensor.db")
            self.db.create_table()
            self.db.insert_data("infrared_value","visible_value",self.IR_current_value,self.VIs_current_value)
            return True
        except Exception as e:
            print("Erreur lors de la connexion à la base de données:", e)
            return False 
        finally:
            self.db.close()




    def get_all_data(self):
      
        try :  
            self.db = save_data.saveData("SI1151_Grove_Sensor.db")
            self.db.create_table()
            return self.db.fetch_data()
        except Exception as e:
            print("Error during getting the data")
        finally:
            self.db.close()

    def export_data(self):
        try :  

            self.db = save_data.saveData("SI1151_Grove_Sensor.db")
            self.db.create_table()
            self.db.export_to_csv("Data.csv")
        except Exception as e:
            print("Error during getting the data")
        finally:
            self.db.close()


    def convert_to_int(self,value):
            
            try : 
                if isinstance(value,str):
                    value.replace('\r', ' ')
                    value= int(float(value))
                    return value

            except(ValueError,TypeError):
               print ("Conversion à échouer")
               return 0
