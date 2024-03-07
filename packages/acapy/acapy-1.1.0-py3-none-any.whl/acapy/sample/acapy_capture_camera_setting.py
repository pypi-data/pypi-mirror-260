'''acapy camera control sample'''

import sys

import acapy    # AcaPyクラス
from acapy import cameracontrol as cam # カメラ設定用

# **************************************************************
# AcaPyクラスのインスタンス(ボードの設定を行う)
# **************************************************************
capture = acapy.AcaPy()

if capture.is_opened is False:
    # 画像入力ボードが見つからないときは終了
    print("Board or Camera not recognized.")
    sys.exit(0)

# iniファイル（ボード設定ファイル）の読込、AcapLib2のiniファイルと共通です。
# iniファイルは実際に使用するカメラ用のファイルを指定してください。
ret = capture.load_inifile("./AreaSensor_mono.ini")
if ret == 0:
    # iniファイルの読込に失敗したとき(ファイルが見つからない、ファイルの設定が異なるなど)
    print("Load inifile error")
    sys.exit(0)

# ボードの設定例（AcaPyクラスのプロパティで値を設定）
capture.width = 640
capture.height = 480

# プロパティの値を設定したときは、reflect_param()メソッドの実行が必要になります。
capture.reflect_param() 

# ボードの設定をiniファイルに保存
capture.save_inifile("./AreaSensor_mono_save.ini")

# ボードの設定値の取得例（AcaPyクラスのプロパティで値を取得）
capture_width = capture.width   # 画像の幅
capture_height = capture.height # 画像の高さ
capture_camera_bit = capture.camera_bit # 画像のビット数

print("-------------------------------------------------")
# 取込む画像情報を表示
print(f"Capture Image Info: {capture_width} x {capture_height} x {capture_camera_bit}bit")
print("[Capture properties]")
# ボードに設定されている値一覧を表示
print(capture.get_acapy_properties_text())

# **************************************************************
# CameraControlクラスのインスタンス(カメラの設定を行う)
# **************************************************************

# AcaPyクラスオブジェクトからCameraControl用クラスをインスタンスする
camera = cam.CameraControl(capture)

# カメラの設定例（set_value(設定値の文字列, 値)を指定して設定）
ret = camera.set_value('Width', 640)
ret = camera.set_value('Height', 480)
# Commandの実行例(set_value(設定値の文字列))、設定値のカメラへの保存例
#ret = camera.set_value('UserSetSave')

# カメラ設定値の取得例（get_value(設定値の文字列)を実行して取得）
ret, camera_width, value_info = camera.get_value('Width')
ret, camera_height, value_info = camera.get_value('Height')
ret, camera_pixelformat, value_info = camera.get_value('PixelFormat')

print("-------------------------------------------------")
# カメラの画像情報を表示
print(f"Camera Image Info: {camera_width} x {camera_height} x {camera_pixelformat}")
print("[Camera setting]")

# カメラに設定されている値一覧を表示
print(camera.get_camera_category_feature_text())

# **************************************************************
# 画像の取込
# **************************************************************
ret, img = capture.snap()
if ret == acapy.AcaPy.OK:
    # 画像が取得できたとき
    print(img)

capture.dispose() # AcaPyクラスのリソースの解放
