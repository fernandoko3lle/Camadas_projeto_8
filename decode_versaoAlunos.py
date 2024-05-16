
#Importe todas as bibliotecas
from suaBibSignal import *
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time


#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

    #*****************************instruções********************************
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    # algo como:
    signal = signalMeu() 
       
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:

    sd.default.samplerate = 44100 #taxa de amostragem
    sd.default.channels = 2 #numCanais # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas.
    #Muitas vezes a gravação retorna uma lista de listas. Você poderá ter que tratar o sinal gravado para ter apenas uma lista.

    duration =  2  #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic  

    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisições) durante a gravação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação
    #faca um print na tela dizendo que a captação comecará em n segundos. e então 
    #use um time.sleep para a espera.
   
    freqDeAmostragem = sd.default.samplerate
    numAmostras = int(duration * freqDeAmostragem)

    # coeficientes de G_z achados no MATLAB
    num = [0.001547, 0.00149]
    den = [1, -1.89, 0.8928]

    # Filtro para o sinal de áudio
    def filtro(entrada, num, den):
        # Inicializa o sinal de saída com zeros do mesmo tamanho do sinal de entrada
        saida = [0] * len(entrada)
        
        # Aplica a equação a diferenças para cada amostra do sinal de entrada
        for k in range(len(entrada)):
            # Calcula a contribuição do numerador (B)
            # Nota: ajuste os índices para corresponder à equação 𝑌[k] = 𝑎𝑈[k−1] + 𝑏𝑈[k−2]
            if k - 1 >= 0:
                saida[k] += num[0] * entrada[k-1]  # Coeficiente 'a' multiplicando U[k-1]
            if k - 2 >= 0:
                saida[k] += num[1] * entrada[k-2]  # Coeficiente 'b' multiplicando U[k-2]
            
            # Calcula a contribuição do denominador (A)
            # Nota: ajuste os índices para corresponder à equação 𝑌[k] = −d𝑌[k−1] − e𝑌[k−2]
            if k - 1 >= 0:
                saida[k] -= den[1] * saida[k-1]  # Coeficiente '-d' multiplicando Y[k-1]
            if k - 2 >= 0:
                saida[k] -= den[2] * saida[k-2]  # Coeficiente '-e' multiplicando Y[k-2]

        return saida


    #A seguir, faca um print informando que a gravacao foi inicializada

    #para gravar, utilize
    print("Gravação iniciada...")
    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
    sd.wait()
    print("...     FIM")

    print(f'audio: {audio}')

    audio_ = audio.flatten()

    # Plota o sinal de áudio original
    xf, yf = signal.calcFFT(audio_, freqDeAmostragem)
    plt.figure()
    plt.plot(xf, yf)
    plt.legend('Antes')
    plt.xlabel('Frequência (Hz)') 
    plt.ylabel('Amplitude')
    plt.title('Fourier do sinal de áudio')
    

    audio_filt = filtro(audio_, num, den) # já esta no formato de lista 
   

    # Plota o sinal de áudio filtrado
    xf, yf = signal.calcFFT(audio_filt, freqDeAmostragem)
    plt.figure()
    plt.plot(xf, yf)
    plt.legend('Depois')
    plt.xlabel('Frequência (Hz)') 
    plt.ylabel('Amplitude')
    plt.title('Fourier do sinal de áudio')


    #Agora você terá que analisar os valores xf e yf e encontrar em quais frequências estão os maiores valores (picos de yf) de da transformada.
    #Encontrando essas frequências de maior presença (encontre pelo menos as 5 mais presentes, ou seja, as 5 frequências que apresentam os maiores picos de yf). 
    #Cuidado, algumas frequências podem gerar mais de um pico devido a interferências na tranmissão. Quando isso ocorre, esses picos estão próximos. Voce pode desprezar um dos picos se houver outro muito próximo (5 Hz). 
    #Alguns dos picos  (na verdade 2 deles) devem ser bem próximos às frequências do DTMF enviadas!
    #Para descobrir a tecla pressionada, você deve encontrar na tabela DTMF frquências que coincidem com as 2 das 5 que você selecionou.
    #Provavelmente, se tudo deu certo, 2 picos serao PRÓXIMOS aos valores da tabela. Os demais serão picos de ruídos.

   
    plt.show()

if __name__ == "__main__":
    main()
