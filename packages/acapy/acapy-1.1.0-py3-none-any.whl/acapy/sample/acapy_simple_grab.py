'''acapy simple grab sample'''

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
ret = capture.load_inifile("./AreaSensor_mono.ini")
if ret == 0:
    # iniファイルの読込に失敗したとき(ファイルが見つからない、ファイルの設定が異なるなど)
    print("Load inifile error")
    capture.dispose()
    sys.exit(0)

# 画像表示ウィンドウ作成(sキー入力:Snap, gキー入力:Grab, qキー入力:終了)
WINDOW_TITLE = "AcaPy Sample [\"g\"=grab,\"q\"=quit]"
cv2.namedWindow(WINDOW_TITLE, cv2.WINDOW_NORMAL)

# ----------------------------------------------------------------
# 画像取込

while True:
    # 前回取得した画像の次の画像から今回までの画像を取得
    ret, frames, count, frame_no = capture.read_frames()

    if frames is not None:
        # 最新の画像を表示
        print(f"[grab] FrameNo={frame_no}, count={count}, error_info={ret}")
        cv2.imshow (WINDOW_TITLE, frames[count - 1] )

    # キー入力
    key = cv2.waitKey(1) & 0xFF

    if key == ord('g'):
        # grab(連続画像取得)
        if capture.is_grab is True:
            # grab中のときはgrabを停止する
            capture.grab_stop()
            print("[grab stop]")

        else:
            # grab中でないときはGrabを開始する
            capture.grab_start()
            print("[grab start]")

    elif key == ord('q') or key == 27: # q もしくは escキーで終了
        if capture.is_grab is True:
            # grab中のときはgrabを停止する
            capture.grab_stop()
            print("[grab stop]")
        break

capture.dispose() # AcaPyクラスのリソースの解放
cv2.destroyAllWindows()
