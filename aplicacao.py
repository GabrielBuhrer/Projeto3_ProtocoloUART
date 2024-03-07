
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

        print("esperando 1 byte de sacrifício")         
        rxBuffer, nRx = com1.getData(1) 
        com1.rx.clearBuffer() 
        time.sleep(.1) 
        
        identificador = b"\0A"

        while True:    
            
            head, nRx = com1.getData(10)

            if nRx > 0:
                if head[0] == "b\01":
                    if head[1] == identificador:
                        npacotes = head[2]
                        break

        msg = b'\02\00\00\00\00\00\00\00\00\00\AA\BB\AA\BB'

        com1.sendData(np.asarray(msg))

        while com1.tx.threadMutex == True:
            continue
        
        imagem = b''
        nideal = 1

        while True:

            head, nRx == com1.getData(10)

            if nRx > 0:
                if head[0] == b'\03':
                    npacote = int.from_bytes(head[1], byteordeer='big')
                    if npacote != nideal:
                        msg = b'\06\00\00\00\00\00\00\00\00\00\AA\BB\AA\BB'
                        com1.sendData(np.asarray(msg))
                        while com1.tx.threadMutex == True:
                            continue
                    else:
                        tpacotes = head[2]
                        tamdados = head[3]
                    
                    dados, nRx = com1.getData(tamdados)
                    final, nRx = com1.getData(4)
                    
                    if dados == 0:
                        msg = b'\06\00\00\00\00\00\00\00\00\00\AA\BB\AA\BB'
                        com1.sendData(np.asarray(msg))
                        while com1.tx.threadMutex == True:
                            continue
                    elif final != b'\AA\BB\AA\BB':
                        msg = b'\06\00\00\00\00\00\00\00\00\00\AA\BB\AA\BB'
                        com1.sendData(np.asarray(msg))
                        while com1.tx.threadMutex == True:
                            continue
                    else:
                        if nRx > 0:
                            imagem += dados

                            msg = b'\04\00\00\00\00\00\00\00\00\00\AA\BB\AA\BB'
                            msg = msg[:1] + (npacote).to_bytes(1, byteorder="big")[-1:] + msg[2:]
                            com1.sendData(np.asarray(msg))
                            while com1.tx.threadMutex == True:
                                continue

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
