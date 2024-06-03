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
red_point_radius = 5  # 点の半径（ピクセル）
red_point_x = 320  # 赤い点のX座標
blue_point_x1 = 100  # 左の青点
blue_point_y1 = 60
blue_point_x2 = 550  # 右の青点
blue_point_y2 = 60
font = cv2.FONT_HERSHEY_SIMPLEX
cy = 0
# ウィンドウの名前設定
cv2.namedWindow('video image', cv2.WINDOW_NORMAL)
cv2.namedWindow('Cropped Image', cv2.WINDOW_NORMAL)

# トラックバーのコールバック関数
def nothing(x):
    pass

# トラックバーをウィンドウに作成
cv2.createTrackbar('Threshold', 'video image', 0, 255, nothing)

# 切り抜き位置の設定（初期値）
cv2.createTrackbar('crop_x', 'Cropped Image', 0, original_img.shape[1], nothing)
cv2.createTrackbar('crop_y', 'Cropped Image', 0, original_img.shape[0], nothing)

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

    # 二値化結果の一致率を計算
    intersection = np.logical_and(binary, otsu_binary)
    union = np.logical_or(binary, otsu_binary)
    iou = np.sum(intersection) / np.sum(union)

    # 一致率を画面に表示
    cv2.putText(img, f"Threshold IOU: {iou:.2f}", (10, 120), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.putText(img, f"sikiti {_}:", (10, 80), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # 黒線の輪郭を見つける
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)  # 輪郭の内側の面積をareaに設定

      #  if area > 1000:  # 本来は100

            # 黒線の輪郭を描画
        cv2.drawContours(img, [contour], -1, (0, 0, 255), 2)

            # 黒線の中心を計算
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
                # 白点を描画
            cv2.circle(img, (cx, cy), red_point_radius, (255, 255, 255), -1)

                # 青い点を描画
            cv2.circle(img, (blue_point_x1, blue_point_y1), red_point_radius, (0, 255, 0), -1)
            cv2.circle(img, (blue_point_x2, blue_point_y2), red_point_radius, (0, 255, 0), -1)

                # 赤点と白点の距離を計算
            distance = (cx - red_point_x) * -1

                # 赤点と白点の距離を描画と出力
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, f"Distance {distance}:", (10, 40), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
            print(distance)

                # 青い点の座標と黒線の座標が重なる場合、点の色を緑に変更
            if 0 <= blue_point_y1 < img.shape[0] and 0 <= blue_point_x1 < img.shape[1]:
                if binary[blue_point_y1, blue_point_x1] == 0:
                    cv2.circle(img, (blue_point_x1, blue_point_y1), red_point_radius, (255, 0, 0), -1)

            if 0 <= blue_point_y2 < img.shape[0] and 0 <= blue_point_x2 < img.shape[1]:
                if binary[blue_point_y2, blue_point_x2] == 0:
                    cv2.circle(img, (blue_point_x2, blue_point_y2), red_point_radius, (255, 0, 0), -1)

    # 赤点の描画
    cv2.circle(img, (red_point_x, cy), red_point_radius, (0, 0, 255), -1)

    # トラックバーの値を取得
    crop_x = cv2.getTrackbarPos('crop_x', 'Cropped Image')
    crop_y = cv2.getTrackbarPos('crop_y', 'Cropped Image')

    # 切り抜き範囲が画像の範囲を超えないように調整
    crop_x = min(crop_x, width - 100)
    crop_y = min(crop_y, height - 100)

    # 任意の位置で画像を切り抜き（サイズは100x100）
    crop_img = img[crop_y:crop_y+100, crop_x:crop_x+300]

    # 格子を描画
    for i in range(0, 300, 2):  # 2ピクセルごとに
        # 横線
        cv2.line(crop_img, (0, i), (300, i), (255, 255, 255), 1)
        # 縦線
        cv2.line(crop_img, (i, 0), (i, 300), (255, 255, 255), 1)

    # 切り抜いた部分の各ピクセルの値を読み取る
    pixel_values = crop_img.reshape(-1, crop_img.shape[-1])  # (height * width, channels)
  #  print("Pixel values of cropped area:")
  #  print(pixel_values)

    # カメラの画像の出力
    cv2.imshow('video image', img)
    cv2.imshow('Cropped Image', crop_img)
    cv2.imshow('Binary Image', binary)
    cv2.imshow('Otsu Binary Image', otsu_binary)

    # 繰り返し分から抜けるためのif文
    key = cv2.waitKey(0)  # 0を渡すと無限に待つ
    if key == 27:  # 27はEscキーのASCIIコード
        break

# メモリを解放して終了するためのコマンド
cap.release()
cv2.destroyAllWindows()

