'''acapy callback sample'''

import sys
import queue

import cv2      # OpenCV
import acapy    # AcaPy

# 表示用フレーム画像
#frame = None
# 画像表示用フレーム画像のキュー
q_frames = queue.Queue(maxsize=1)

# ---------------------------------------------------------------------
# 【コールバック関数】
# ※サブスレッドで呼び出されます
#   サブスレッドから直接GUI表示はできません。

def capture_frame_end(capture, frames, count, total_frame_count, error_info):
    '''ACL_INT_FRAMEENDのコールバック関数

    Parameters
    ----------
    capture : AcaPy class
        コールバック元のAcaPyクラスオブジェクト
    frames : List[ndarray]
        前回の次のフレームから今回のフレームまでの画像データのリスト
    count : int
        framesに格納されたフレーム画像の枚数
    total_frame_count : int
        取込開始から取得した画像の総枚数
    error_info : int
        エラー情報。1のときエラーなし、負のとき上書きされたフレーム枚数
    '''
    # 各フレーム画像の取込が完了したときに発生
    # error_infoの値が負のときは、フレーム画像の上書きが発生しています。
    # 　-> AcaPyクラスのリングバッファの面数(mem_numプロパティの値)を大きくしてください。
    print(f"[frame_end callback] board_id={capture.board_id}, ch={capture.ch}, FrameNo={total_frame_count}, count={count}, error_info={error_info}")

    if error_info != 0:
        for f in frames:
            #########################################################
            # ここで、取得した各フレーム画像(f)に対して画像処理を行う
            #########################################################
            pass

        if q_frames.qsize() >= q_frames.maxsize:
            _ = q_frames.get() # キューがいっぱいの場合、表示用画像データを１枚捨てる
        q_frames.put(frames[count - 1]) # 最新の画像を表示用画像データに追加

def capture_grab_end(capture):
    '''ACL_INT_GRABENDのコールバック関数

    Parameters
    ----------
    capture : AcaPy class
        コールバック元のAcaPyクラスオブジェクト
    '''
    # grab_start()メソッドで枚数指定分の画像取込が完了したときに発生
    print(f"[grab_end callback] board_id={capture.board_id}, ch={capture.ch}")

def capture_gpin(capture, gpin_polarity):
    '''ACL_INT_GPINのコールバック関数

    Parameters
    ----------
    capture : AcaPy class
        コールバック元のAcaPyクラスオブジェクト
    gpin_polarity : int
        GPINのレベル
    '''
    # GPINの入力があったときに発生
    print(f"[gpin callback] board_id={capture.board_id}, \
          ch={capture.ch}, gpin_polarity={gpin_polarity}")

def capture_overwrite(capture, count, total_frame_count, overwrite_count):
    '''オーバーライトのコールバック関数

    Parameters
    ----------
    capture : AcaPy class
        コールバック元のAcaPyクラスオブジェクト
    count : int
        前回から今回まで取得した画像の枚数
    total_frame_count : int
        取込開始から取得した画像の総枚数
    overwrite_countt : int
        上書きされた画像の枚数
    '''
    # Overwrite(画像データの上書き)が発生したときに発生
    print(f"[overwrite callback] board_id={capture.board_id}, ch={capture.ch}")

def capture_timeout(capture):
    '''ACL_INT_TIMEOUTのコールバック関数

    Parameters
    ----------
    capture : AcaPy class
        コールバック元のAcaPyクラスオブジェクト
    '''
    # Timeoutがあったときに発生
    print(f"[timeout callback] board_id={capture.board_id}, ch={capture.ch}")
    capture.print_last_error() # 最後に発生したエラーの表示

def capture_device_alm(capture, alarm_status):
    '''ACL_INT_DEVICE_ALMのコールバック関数

    Parameters
    ----------
    capture : AcaPy class
        コールバック元のAcaPyクラスオブジェクト
    alarm_status : int
        アラームの内容  
        BIT3 サーマルシャットダウンアラーム
        BIT2 FAN 回転数アラーム
        BIT1 FPGA 温度アラーム
        BIT0 基板周辺温度アラーム
    '''
    # DeviceAlarmがあったときに発生
    print("************************************************************")
    print("*********************** DEVICE ALARM ***********************")
    print("************************************************************")
    print(f"[device_alm callback] board_id={capture.board_id}, \
          ch={capture.ch}, alarm_status={alarm_status}")
    print("************************************************************")

# ----------------------------------------------------------------
# ボードの設定

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
# コールバック関数の登録

# FrameEndのコールバック関数を登録
capture.regist_frame_end_callback(capture_frame_end)
# GrabEndのコールバック関数を登録
capture.regist_grab_end_callback(capture_grab_end)
# GPINのコールバック関数を登録
capture.regist_gpin_callback(capture_gpin)
# Overwrite(画像データの上書き発生)のコールバック関数を登録
capture.regist_overwrite_callback(capture_overwrite)
# Timeoutのコールバック関数を登録
capture.regist_timeout_callback(capture_timeout)
# DeviceAlarmのコールバック関数を登録
capture.regist_device_alm_callback(capture_device_alm)

# ----------------------------------------------------------------
# 画像取込

# 画像表示ウィンドウ作成(sキー入力:Snap, gキー入力:Grab, qキー入力:終了)
WINDOW_TITLE = "AcaPy Sample [\"s\"=snap,\"g\"=grab,\"q\"=quit]"
cv2.namedWindow(WINDOW_TITLE, cv2.WINDOW_NORMAL)

while True:

    # キー入力
    key = cv2.waitKey(30) & 0xFF

    if key == ord('s'):
        # snap(画像１枚の取得)
        if capture.is_grab is True:
            # grab中のときはgrabを停止する
            capture.grab_stop()
            print("[grab stop]")

        print("[snap]")
        capture.snap()

    elif key == ord('g'):
        # grab(連続画像取得)
        if capture.is_grab is True:
            # grab中のときはgrabを停止する
            capture.grab_stop()
            print("[grab stop]")

        else:
            # grab中でないときはGrabを開始する
            capture.grab_start()
            print("[grab start]")

    elif key == ord('q') or key == 27:  # q もしくは escキーで終了
        # quit
        if capture.is_grab is True:
            # grab中のときはgrabを停止する
            capture.grab_stop()
            print("[grab stop]")

        print("[quit]")
        break

    # 画像の表示（画像データはコールバック関数(サブスレッド)で取得している）
    if q_frames.empty() is False:
        frame = q_frames.get()
        cv2.imshow(WINDOW_TITLE, frame)

capture.dispose() # AcaPyクラスのリソースの解放
cv2.destroyAllWindows()
