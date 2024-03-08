
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
        

        print("esperando 1 byte de sacrifício")         
        rxBuffer, nRx = com1.getData(1) 
        com1.rx.clearBuffer() 
        time.sleep(.1) 
        
        identificador = 7
        nimg = 1

        target_time = time.time() + 10
        while nimg <= 2:
            while True:    
        

                rxBuffer, nRx = com1.getData(10)


                if nRx > 0:
                    
                    if rxBuffer[0] == 1:
                        
                        if rxBuffer[1] == identificador:
                            npacotes = rxBuffer[2]
                            
                            break
                else:
                    if  time.time() >= target_time:
                        msg = b'\05\00\00\00\00\00\00\00\00\00\xAA\xBB\xAA\xBB'
                        com1.sendData(np.asarray(msg))
                        while com1.tx.threadMutex == True:
                                continue
                        print("-------------------------")
                        print("Comunicação encerrada por time out")
                        print("-------------------------")
                        com1.disable()
                

            msg = b'\02\00\00\00\00\00\00\00\00\00\xAA\xBB\xAA\xBB'

            com1.sendData(np.asarray(msg))

            while com1.tx.threadMutex == True:
                continue
            
            imagem = b''
            nideal = 1
            i = 0

            rxBuffer, _ = com1.getData(4)

            while True:
                if i == 0:
                    target_time = time.time() + 10
                    i = 1

                rxBuffer, nRx = com1.getData(10)

            

                if nRx > 0:

                    if rxBuffer[0] == 3:
                    
                        npacote = rxBuffer[1]
                        if npacote != nideal:
                            msg = b'\06\00\00\00\00\00\00\00\00\00\xAA\xBB\xAA\xBB'
                            com1.sendData(np.asarray(msg))
                            while com1.tx.threadMutex == True:
                                continue
                            nideal = nideal - 1
                            i = 0
                            print('Erro de pacote fora de ordem')
                        else:
                            tpacotes = rxBuffer[2]
                            tamdados = rxBuffer[3]
                        
                        rxBuffer, nRx = com1.getData(tamdados)
                        print(rxBuffer)
                        final, nRx = com1.getData(4)
                        
                        if rxBuffer == 0:
                            msg = b'\06\00\00\00\00\00\00\00\00\00\xAA\xBB\xAA\xBB'
                            com1.sendData(np.asarray(msg))
                            while com1.tx.threadMutex == True:
                                continue
                            nideal = nideal - 1
                            i = 0
                            
                            print('Erro de tamanho de payload errado')
                        elif final != b'\xAA\xBB\xAA\xBB':
                            msg = b'\06\00\00\00\00\00\00\00\00\00\xAA\xBB\xAA\xBB'
                            com1.sendData(np.asarray(msg))
                            while com1.tx.threadMutex == True:
                                continue
                            nideal = nideal - 1
                            i = 0
                            print('Erro de EOP com problema')
                        else:
                            if nRx > 0:
                                imagem += rxBuffer
                                msg = b'\04\00\00\00\00\00\00\00\00\00\xAA\xBB\xAA\xBB'
                                msg = msg[:1] + (npacote).to_bytes(1, byteorder="big")[-1:] + msg[2:]
                                com1.sendData(np.asarray(msg))
                                i = 0
                                while com1.tx.threadMutex == True:
                                    continue
                else:
                    if  time.time() >= target_time:
                        msg = b'\05\00\00\00\00\00\00\00\00\00\xAA\xBB\xAA\xBB'
                        com1.sendData(np.asarray(msg))
                        while com1.tx.threadMutex == True:
                                continue
                        print("-------------------------")
                        print("Comunicação encerrada por time out")
                        print("-------------------------")
                        com1.disable()
                nideal += 1
                if nideal == npacotes+1:
                    break
            if nimg == 1:
                imageW = './Recebidos/download.jpg'
                nimg +=1
            else:
                imageW = './Recebidos/download2.jpg'
            f = open(imageW, 'wb')
            f.write(imagem)
            print("A mensagem foi recebida")



        print("-------------------------")
        print("Comunicação encerrada final")
        print("-------------------------")
        com1.disable()
            

            

        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

if __name__ == "__main__":
    main()
