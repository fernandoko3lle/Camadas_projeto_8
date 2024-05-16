
#Importe todas as bibliotecas
from suaBibSignal import *
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
import time
from scipy.signal import butter, lfilter, freqz




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
    t = np.linspace(0, 2, sd.default.samplerate*duration, endpoint=False)

    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisições) durante a gravação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação
    #faca um print na tela dizendo que a captação comecará em n segundos. e então 
    #use um time.sleep para a espera.
   
    freqDeAmostragem = sd.default.samplerate
    numAmostras = int(duration * freqDeAmostragem)

    # Parâmetros do filtro
    order = 10
    fs = freqDeAmostragem       # taxa de amostragem, Hz
    cutoff = 4000    # frequência de corte desejada do filtro, Hz

    # Função para normaçização
    def normaliza(audio):
        max_amplitude = np.max(np.abs(audio))
        if max_amplitude == 0:
            normalized_audio = audio  # ou alternativamente, set para zero se preferir
        else:
            normalized_audio = audio / max_amplitude
            return normalized_audio

    # Função para o design do filtro passa-baixa Butterworth
    def butter_lowpass(cutoff, fs, order):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a

    # Função para aplicar o filtro
    def butter_lowpass_filter(data, cutoff, fs, order):
        b, a = butter_lowpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y

    # #Início da gravação / carreramento do sinal
    # print("Gravação iniciada...")
    # audio_grav = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
    # sd.wait()
    # print("...     FIM")

    # #Salvando o áudio em um arquivo WAV
    # nome_arquivo = 'audio_gravado.wav'
    # sf.write(nome_arquivo, audio_grav, freqDeAmostragem)
    # print(f"Áudio salvo como {nome_arquivo}.")

    # Lendo arquivo de audio previamente gravado
    audio, fs = sf.read('audio_gravado.wav')

    # Grafico 1 - original normalizado:
    plt.figure()
    plt.plot(t, normaliza(audio))
    plt.title('Sinal de Áudio Original')
    plt.xlabel('tempo')
    plt.ylabel('sinal de audio')
    plt.grid()

    # Grafico teste - original/freq
    xft, yft = signal.calcFFT(audio, freqDeAmostragem)
    plt.figure()
    plt.plot(xft, yft)
    plt.xlabel('Frequência (Hz)') 
    plt.ylabel('Amplitude')
    plt.title('Fourier do sinal de áudio original')


    # Aplicação do filtro
    audio_ = audio.flatten() # verificar se é necessário
    filtered_data = normaliza(butter_lowpass_filter(audio_, cutoff, fs, order))

    # Grafico 2 - filtrado/tempo:
    plt.figure()
    plt.plot(t, filtered_data)
    plt.title('Sinal de Áudio filtrado')
    plt.xlabel('tempo')
    plt.ylabel('sinal de audio')
    plt.grid()

    # Grafico 3 - filtrado/freq:
    xf, yf = signal.calcFFT(filtered_data, freqDeAmostragem)
    plt.figure()
    plt.plot(xf, yf)
    plt.xlabel('Frequência (Hz)') 
    plt.ylabel('Amplitude')
    plt.title('Fourier do sinal de áudio filtrado')


    # Modulação em AM a 14.000Hz
    f_portadora = 14000
    duracao = len(filtered_data) / fs
    t_portadora = np.linspace(0, duracao, len(filtered_data))
    portadora = np.sin(2 * np.pi * f_portadora * t_portadora)
    sinal_modulado = normaliza((0 + filtered_data) * portadora)

    #Salvando o áudio modulado em um arquivo WAV
    nome_arquivo = 'audio_gravado_modulado.wav'
    sf.write(nome_arquivo, sinal_modulado, freqDeAmostragem)
    print(f"Áudio modulado salvo como {nome_arquivo}.")

    # Grafico 4 - modulado/tempo:
    plt.figure()
    plt.plot(t, sinal_modulado)
    plt.title('Sinal de Áudio Modulado')
    plt.xlabel('tempo')
    plt.ylabel('sinal de audio')
    plt.grid()

    # Grafico 5 - modulado/freq:
    xf2, yf2 = signal.calcFFT(sinal_modulado, freqDeAmostragem)
    plt.figure()
    plt.plot(xf2, yf2)
    plt.xlabel('Frequência (Hz)') 
    plt.ylabel('Amplitude')
    plt.title('Fourier do sinal de áudio modulado')
    plt.show()

    # Reprodução do audio
    print('Reprodução iniciada...')
    sd.play(filtered_data, freqDeAmostragem)
    print('Reprodução finalizada.')


if __name__ == "__main__":
    main()
