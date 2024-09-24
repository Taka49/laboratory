import os
import glob
import time
import numpy as np
import matplotlib.pyplot as plt # type: ignore
import librosa
import librosa.display

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
            librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='linear')
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