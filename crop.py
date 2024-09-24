from PIL import Image # type: ignore
import os
import time

def crop_and_save(image_path, output_path):
    # 画像の読み込み
    img = Image.open(image_path)
    width, height = img.size
    left = 0
    bottom = height - 512
    right = 512
    top = height
    # 画像をクロップ
    cropped_img = img.crop((left, bottom, right, top))
    # 切り取った画像を保存
    cropped_img.save(output_path)

def process_folder(input_folder):
    # フォルダ内のPNGファイルを処理
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".png"):
            input_path = os.path.join(input_folder, filename)
            # 同じファイルに保存するので、出力パスも同じに設定
            output_path = input_path
            crop_and_save(input_path, output_path)

def process_base_folder(base_folder):
    # ベースフォルダ内のサブフォルダを処理
    for subdir in os.listdir(base_folder):
        subdir_path = os.path.join(base_folder, subdir)
        if os.path.isdir(subdir_path):
            process_folder(subdir_path)

if __name__ == "__main__":
    start_time = time.time()
    # ベースフォルダのパス
    base_folder = 'C:/Users/path'
    # ベースフォルダ内のサブフォルダを処理
    process_base_folder(base_folder)
    print("切り取りが完了しました")
    end_time = time.time()
    # 処理時間を表示
    elapsed_time = end_time - start_time
    print(elapsed_time)
