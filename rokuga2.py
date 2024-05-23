import cv2

# 録画されたビデオファイルを開く
cap = cv2.VideoCapture('output.avi')

if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        # フレームを表示
        cv2.imshow('Recorded Video', frame)
        
        # 'q'キーが押された場合、再生を停止
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

# リソースを解放
cap.release()
cv2.destroyAllWindows()

