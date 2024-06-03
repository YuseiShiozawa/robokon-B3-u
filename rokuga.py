import cv2
import time

# ビデオキャプチャオブジェクトを作成
cap = cv2.VideoCapture(4)

# フレームレートの設定
cap.set(cv2.CAP_PROP_FPS, 30)
# 解像度の設定 (例として640x480を使用)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# オート機能をすべてオフ
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_AUTO_WB, 0)

# ビデオの保存設定
fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.avi', fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))
out = cv2.VideoWriter('autoff1.avi', fourcc, 30.0, (640, 480))
# カウントダウンの時間（秒）
countdown_time = 5

# カウントダウンの開始時間
start_time = time.time()

# カウントダウン中の映像表示
while time.time() - start_time < countdown_time:
    ret, frame = cap.read()
    if ret:
        # 残り時間を計算
        remaining_time = int(countdown_time - (time.time() - start_time))
        
        # カウントダウンの秒数をフレームに描画
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, f'Count down: {remaining_time}s', (50, 50), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        
        # フレームを表示
        cv2.imshow('frame', frame)
        
        # Escキーが押された場合は終了
        if cv2.waitKey(1) & 0xFF == 27:
            cap.release()
            cv2.destroyAllWindows()
            exit()
    else:
        break

print('録画開始!')

# 録画開始
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        # フレームを書き込み
        out.write(frame)
        
        # フレームを表示
        cv2.imshow('frame', frame)
        
        # Escキーが押された場合、録画を停止
        if cv2.waitKey(1) == 27:  # 27はEscキーのASCIIコード
            break
    else:
        break

# リソースを解放
cap.release()
out.release()
cv2.destroyAllWindows()

