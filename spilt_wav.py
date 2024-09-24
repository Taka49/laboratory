from pydub import AudioSegment # type: ignore
import os

def split_wav(input_file):
    # wavファイルの読み込み
    sound = AudioSegment.from_wav(input_file)

    # セグメントの長さを指定（１秒＝1000）
    segment_length = 1000  # 1 second in milliseconds

    # ファルダの作成
    input_filename_without_extension = os.path.splitext(os.path.basename(input_file))[0]
    output_folder = f"{input_filename_without_extension}"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # wavファイルの分割実行
    for i, start_time in enumerate(range(0, len(sound), segment_length)):
        segment = sound[start_time: start_time + segment_length]
        output_file = os.path.join(output_folder, f"{input_filename_without_extension}_{i + 1:03d}.wav")
        segment.export(output_file, format="wav")

# フォルダ全体で実行
def process_directory(directory):
    # ファイルの取得
    file_list = [filename for filename in os.listdir(directory) if filename.lower().endswith(".wav")]

    # フォルダ内のwavファイルすべてに実行
    for filename in file_list:
        input_file = os.path.join(directory, filename)
        split_wav(input_file)


if __name__ == "__main__":
    input_directory = "C:/Users/path"  
    process_directory(input_directory)
    print('end')
