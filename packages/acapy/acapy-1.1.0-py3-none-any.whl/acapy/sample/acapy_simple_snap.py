'''acapy simple snap sample'''

import sys

import cv2      # OpenCV
import acapy    # AcaPy

# ----------------------------------------------------------------
# AcaPyクラスのインスタンス
capture = acapy.AcaPy()

if capture.is_opened is False:
    # 画像入力ボードが見つからないときは終了
    print("Board or Camera not recognized.")
    capture.dispose()
    sys.exit(0)

# iniファイル（ボード設定ファイル）の読込、AcapLib2のiniファイルと共通です。
# iniファイルは実際に使用するカメラ用のファイルを指定してください。
ret = capture.load_inifile("./AreaSensor_mono.ini")
if ret == 0:
    # iniファイルの読込に失敗したとき(ファイルが見つからない、ファイルの設定が異なるなど)
    print("Load inifile error")
    capture.dispose()
    sys.exit(0)

# ----------------------------------------------------------------
# 画像取込

# 画像表示ウィンドウ作成(sキー入力:Snap, qキー入力:終了)
WINDOW_TITLE = "AcaPy Sample [\"s\"=snap,\"q\"=quit]"
cv2.namedWindow(WINDOW_TITLE, cv2.WINDOW_NORMAL)

while True:

    # キー入力
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        # snap(画像１枚の取得)
        print("[snap]")
        ret, frame = capture.snap()
        if frame is not None:
            cv2.imshow(WINDOW_TITLE, frame)
    elif key == ord('q') or key == 27: # q もしくは escキーで終了
        # quit
        print("[quit]")
        break

capture.dispose() # AcaPyクラスのリソースの解放
cv2.destroyAllWindows()
