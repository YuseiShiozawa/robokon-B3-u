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
selected_pixels = []
# ウィンドウの名前設定
cv2.namedWindow('video image', cv2.WINDOW_NORMAL)

# トラックバーのコールバック関数
def nothing(x):
    pass

# トラックバーをウィンドウに作成
cv2.createTrackbar('Threshold', 'video image', 0, 255, nothing)

def select_pixel(event, x, y, flags, param):
    global selected_pixels
    if event == cv2.EVENT_LBUTTONDOWN:
        selected_pixels.append((x, y))
        print(f"Pixel selected at: ({x}, {y})")

# マウスイベントを設定
cv2.setMouseCallback('video image', select_pixel)
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
    for (x, y) in selected_pixels:
        img[y - height // 2, x] = (0, 255, 0)

    # 選択されたピクセル数を表示
    cv2.putText(img, f"Selected Pixels: {len(selected_pixels)}", (10, 160), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
    # P-タイル法による二値化
    total_pixels = gray.size
    p_tile_percentage = 30  # 例えば30%を対象物とする
    target_pixels = total_pixels * p_tile_percentage / 100
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    cumulative_hist = np.cumsum(hist)
    p_tile_threshold = np.searchsorted(cumulative_hist, target_pixels)

    _, p_tile_binary = cv2.threshold(gray, p_tile_threshold, 255, cv2.THRESH_BINARY_INV)

    # 一致率を画面に表示
    cv2.putText(img, f"IOU: {iou}", (10, 120), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(img, f"sikiti {threshold_value}:", (10, 80), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(img, f"P-Tile Thresh: {p_tile_threshold}", (10, 160), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # 画像処理結果の表示
    cv2.imshow('change sikiti Image', binary)
    cv2.imshow('Otsu Binary Image', otsu_binary)
    cv2.imshow('P-Tile Binary Image', p_tile_binary)

    # カメラの画像の出力
    cv2.imshow('video image', img)

    # 繰り返し分から抜けるためのif文
    key = cv2.waitKey(1)  # 1を渡すと1ミリ秒待つ
    if key == 27:  # 27はEscキーのASCIIコード
        break

# メモリを解放して終了するためのコマンド
cap.release()
cv2.destroyAllWindows()

