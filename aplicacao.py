#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np
from enlaceRx import *

serialName = "COM7"         


def main():
    try:
        print("Iniciou o main")
        
        com1 = enlace(serialName)
        
    
        
        com1.enable()
       
        print("Abriu a comunicação")
        
        lista_recebidos = []
        
        controlador = 0

        print("esperando 1 byte de sacrifício")         
        rxBuffer, nRx = com1.getData(1) 
        com1.rx.clearBuffer() 
        time.sleep(.1) 
        

        while True:    
            
            rxLen = com1.rx.getBufferLen()
            rxBuffer, nRx = com1.getData(rxLen)
            if rxBuffer == b'\03':
                break
            
            
            if nRx>0:
                print(rxBuffer)
                lista_recebidos.append(rxBuffer)
                while True:
                    com1.sendData(np.asarray(rxBuffer))
                    while com1.tx.threadMutex==True:
                        continue
                    com1.rx.clearBuffer()
                    break
            
                    
        print(lista_recebidos)
        print(len(lista_recebidos))
        #lista_recebidos = lista_recebidos.pop()
        
        com1.sendData(np.asarray((len(lista_recebidos)).to_bytes(2, byteorder='big')))
        while com1.tx.threadMutex==True:
            continue
        com1.rx.clearBuffer()

        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
            

            

        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

if __name__ == "__main__":
    main()
