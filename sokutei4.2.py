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

# 各変数の初期値設定
font = cv2.FONT_HERSHEY_SIMPLEX

# ウィンドウの名前設定
cv2.namedWindow('video image', cv2.WINDOW_NORMAL)
cv2.namedWindow('Cropped Image', cv2.WINDOW_NORMAL)
cv2.namedWindow('change sikiti Image', cv2.WINDOW_NORMAL)

# トラックバーのコールバック関数
def nothing(x):
    pass

# トラックバーをウィンドウに作成
cv2.createTrackbar('Threshold', 'video image', 0, 255, nothing)
cv2.createTrackbar('crop_x', 'Cropped Image', 0, original_img.shape[1], nothing)
cv2.createTrackbar('crop_y', 'Cropped Image', 0, original_img.shape[0], nothing)

while True:
    # 画像をコピーして使用
    img = original_img.copy()
    height, width, _ = img.shape

#    img = cv2.resize(img0, (int(width*0.5), int(height*0.5)))
#    height, width, _ = img.shape

    # 下半分を使用
    img = img[height//2:, :]
    
    # 画像処理：グレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # トラックバーの値を取得
    threshold_value = cv2.getTrackbarPos('Threshold', 'video image')
    crop_x = cv2.getTrackbarPos('crop_x', 'Cropped Image')
    crop_y = cv2.getTrackbarPos('crop_y', 'Cropped Image')

    # 二値化
    _, binary = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

    # 大津の二値化
#    _, otsu_binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    _, otsu_binary = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    
    # 二値化結果の一致率を計算
    intersection = np.logical_and(binary, otsu_binary)
    union = np.logical_or(binary, otsu_binary)
    iou = np.sum(intersection) / np.sum(union)

  #  intersection2 = np.logical_and(binary, img)
   # union2 = np.logical_or(binary, img)
   # iou2 = np.sum(intersection) / np.sum(union)


    # 一致率を画面に表示
    cv2.putText(img, f"IOU: {iou:.2f}", (10, 120), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(img, f"sikiti {threshold_value}:", (10, 80), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
    

   # cv2.putText(img, f"IOU: {iou:.2f}", (10, 120-70), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
 #   cv2.putText(img, f"sikiti {threshold_value}:", (10, 80-70), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
 
    # トリミング
    crop_x = min(crop_x, width - 100)
    crop_y = min(crop_y, height - 100)
    crop_img = img[crop_y:crop_y+30, crop_x:crop_x+300]

    # トリミングされた範囲に枠を描画
    cv2.rectangle(img, (crop_x, crop_y), (crop_x + 300, crop_y + 30), (0, 255, 0), 2)

    # トリミングされた画像を表示
    cv2.imshow('Cropped Image', crop_img)

    # change sikiti Imageも同じ範囲でトリミング
    cropped_binary = binary[crop_y:crop_y+1, crop_x:crop_x+300]

    # 二値化されたピクセル数をカウント
    white_pixel_count = np.sum(cropped_binary == 255)
    
    # ピクセル数を表示
#    cv2.putText(cropped_binary, f"White Pixels: {white_pixel_count}", (10, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    print(white_pixel_count)
    
    cv2.imshow('change sikiti Image', binary)


    # トリミングされた二値化画像を表示
    cv2.imshow('change sikiti Image2', cropped_binary)

    # 画像処理結果の表示
    cv2.imshow('Otsu Binary Image', otsu_binary)
    cv2.imshow('video image', img)

    # 繰り返し分から抜けるためのif文
    key = cv2.waitKey(1)  # 1を渡すと1ミリ秒待つ
    if key == 27:  # 27はEscキーのASCIIコード
        break

# メモリを解放して終了するためのコマンド
cap.release()
cv2.destroyAllWindows()

