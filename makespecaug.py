import os
import glob
import time
import numpy as np
import matplotlib.pyplot as plt # type: ignore
import librosa
import librosa.display
import random
import audiomentations as augments # type: ignore
from audiomentations import SpecCompose, SpecChannelShuffle, SpecFrequencyMask # type: ignore

random.seed(111)

def spec_augment(spec: np.ndarray, num_mask=1, 
                 freq_masking_max_percentage=0.1, time_masking_max_percentage=0.1):
    spec = spec.copy()
    for i in range(num_mask):
        all_frames_num, all_freqs_num = spec.shape

        # 周波数マスキング
        freq_percentage = random.uniform(0.0, freq_masking_max_percentage)
        num_freqs_to_mask = int(freq_percentage * all_freqs_num)
        f0 = np.random.uniform(low=0.0, high=all_freqs_num - num_freqs_to_mask)
        f0 = int(f0)
        spec[:, f0:f0 + num_freqs_to_mask] = 0

        # 時間マスキング
        time_percentage = random.uniform(0.0, time_masking_max_percentage)
        num_frames_to_mask = int(time_percentage * all_frames_num)
        t0 = np.random.uniform(low=0.0, high=all_frames_num - num_frames_to_mask)
        t0 = int(t0)
        spec[t0:t0 + num_frames_to_mask, :] = 0
    
    return spec

# 変換の指定
transform = augments.Compose([
    augments.AddGaussianNoise(min_amplitude=0.0001, max_amplitude=0.0005, p=1),
    augments.Gain(min_gain_db=-65, max_gain_db=-40, p=1)
])


# ベースフォルダパスを指定
base_folder = 'C:/Users/path'
start_time = time.time()
# ベースフォルダ内のすべてのフォルダに対して処理を行う
for root, dirs, files in os.walk(base_folder):
    for folder in dirs:
        folder_path = os.path.join(root, folder)
        output_folder = folder_path + '_spec'
        os.makedirs(output_folder, exist_ok=True)

        # WAVファイルを取得
        wav_files = glob.glob(os.path.join(folder_path, '*.wav'))
        
        for wav_file in wav_files:
            # 音声ファイルを読み込む
            y, sr = librosa.load(wav_file, sr=None)

            # ノイズとピッチシフトを付加
            #y = transform(y, sample_rate=sr)

            win_length = 1024
            hop_length = 512
            n_fft = win_length
            window = 'hamming'
            stft = librosa.stft(y, n_fft=n_fft, hop_length=hop_length, 
                                win_length=win_length, window=window, center=True)
            amplitude = np.abs(stft)
            D = librosa.amplitude_to_db(amplitude, ref=np.max)

            # スペクトログラムを表示する
            plt.figure(figsize=(D.shape[1], D.shape[0]), dpi=1)
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
            librosa.display.specshow(spec_augment(D), sr=sr, x_axis='time', y_axis='linear')
            plt.ylim(20000, 192000)
            plt.axis('off')
            output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(wav_file))[0] + '.png')
            plt.savefig(output_file, bbox_inches='tight', pad_inches=0)

            # プロットをクリア
            plt.clf()
            plt.close()

        print(f'フォルダ {folder} のスペクトログラムの変換が完了しました。')
end_time = time.time()

# 処理時間を表示
elapsed_time = end_time - start_time
print('すべてのスペクトログラムの変換が完了しました')
print(elapsed_time)