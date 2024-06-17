import cv2
import numpy as np

# 動画ファイルのパス
video_path = 'output.avi'  # ここに動画ファイルのパスを入力してください

# 動画ファイルからキャプチャを作成
cap = cv2.VideoCapture(video_path)

# 固定フレーム番号を設定
fixed_frame_number = 50

# 指定されたフレーム番号に移動
cap.set(cv2.CAP_PROP_POS_FRAMES, fixed_frame_number)

# フレームを取得
ret, original_img = cap.read()

if not ret:
    print(f"Failed to read frame at position {fixed_frame_number}")
    cap.release()
    cv2.destroyAllWindows()
    exit()

# ウィンドウの名前設定
cv2.namedWindow('video image', cv2.WINDOW_NORMAL)

# トラックバーのコールバック関数
def nothing(x):
    pass

# トラックバーをウィンドウに作成
cv2.createTrackbar('Threshold', 'video image', 0, 255, nothing)

while True:
    # 画像をコピーして使用
    img = original_img.copy()
    height, width, _ = img.shape

    img = img[height//2:, :]
    red_point_x = width // 2

    # 画像処理：グレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # トラックバーの値を取得
    threshold_value = cv2.getTrackbarPos('Threshold', 'video image')

    # 二値化
    _, binary = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY_INV)

    # 大津の二値化
    _, otsu_binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Pixel Accuracyの計算
    total_pixels = gray.size
    correct_pixels = np.sum(binary == otsu_binary)
    pixel_accuracy = correct_pixels / total_pixels

    # Pixel Accuracyを画面に表示
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, f"Pixel Accuracy: {pixel_accuracy:}", (10, 120), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(img, f"sikiti {threshold_value}:", (10, 80), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # 画像処理結果の表示
    cv2.imshow('change sikiti Image', binary)
    cv2.imshow('Otsu Binary Image', otsu_binary)

    # カメラの画像の出力
    cv2.imshow('video image', img)

    # 繰り返し分から抜けるためのif文
    key = cv2.waitKey(1)  # 1を渡すと1ミリ秒待つ
    if key == 27:  # 27はEscキーのASCIIコード
        break

# メモリを解放して終了するためのコマンド
cap.release()
cv2.destroyAllWindows()

