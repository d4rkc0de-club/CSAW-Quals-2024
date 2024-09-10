import numpy as np
import librosa

FILE_PATH = '256.wav'
N = 256
DELAY_1 = 48
DELAY_2 = 57

class EchoDecoder:
    def __init__(self, signal, chunk_size, freq_d0, freq_d1):
        self.signal = signal
        self.chunk_size = chunk_size
        self.freq_d0 = freq_d0
        self.freq_d1 = freq_d1
        self.num_chunks = len(signal) // chunk_size
        self.chunked_signal = self.signal[:self.num_chunks * self.chunk_size].reshape(self.num_chunks, self.chunk_size)

    def _compute_rceps(self, chunk):
        spectrum = np.fft.fft(chunk)
        log_spectrum = np.log(np.abs(spectrum) + 1e-6)
        rceps = np.fft.ifft(log_spectrum).real
        return rceps

    def _decode_chunk(self, chunk):
        rceps = self._compute_rceps(chunk)
        return int(rceps[self.freq_d1] > rceps[self.freq_d0])

    def decode(self):
        binary_data = [str(self._decode_chunk(chunk)) for chunk in self.chunked_signal]
        num_bytes = self.num_chunks // 8
        binary_data_chunks = np.array(binary_data[:8 * num_bytes]).reshape(num_bytes, 8)
        ascii_chars = [chr(int(''.join(bits), 2)) for bits in binary_data_chunks]
        message = ''.join(ascii_chars)
        return message

def main():
    data, sample_rate = librosa.load(FILE_PATH, sr=None)
    L = len(data) // N
    decoder = EchoDecoder(data, L, DELAY_1, DELAY_2)
    decoded_message = decoder.decode()
    print(decoded_message)

if __name__ == "__main__":
    main()

