'''acapy tkinter GUI sample'''

import sys

import tkinter as tk
from tkinter import filedialog
import numpy as np
from PIL import Image
import time

import acapy    # AcaPy
from acapy import graphicsbox

class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)

        self.master.title("AcaPy Tkinter Sample")   # ウィンドウタイトル
        self.master.geometry("600x400")             # ウィンドウサイズ(幅x高さ)

        # ウィンドウ画面の生成
        self.initialize_component()

        #AcaPyの初期化
        self.capture = None
        self.init_acapy()

        self.grab_update_id = None
        self.last_disp_image = None

    def __del__(self):
        if self.capture is not None:
            if self.capture.is_grab == True:
                # grab中のときはgrabを中断する
                self.capture.grab_abort()

            self.capture.dispose() # クラスリソースの解放

    def initialize_component(self):
        '''ウィンドウ画面の生成'''

        # メニューの追加
        self.menubar = tk.Menu(self)
        self.menubar.add_command(label= "BoadName")
        self.menubar.add_command(label= "Snap",         command = self.snap_click)
        self.menubar.add_command(label= "Grab",         command = self.grab_click)
        self.menubar.add_command(label= "Image Save",   command = self.save_click)
        # 表示(グリッド、輝度値、プロファイル)
        self.disp_grid_value = tk.BooleanVar(value = True)
        self.disp_bright_value = tk.BooleanVar(value = True)
        self.disp_profile_value = tk.BooleanVar(value = False)
        menu_disp = tk.Menu(self.menubar, tearoff = False)
        menu_disp.add_checkbutton(label = "Grid", command = self.menu_grid_click, variable = self.disp_grid_value)
        menu_disp.add_checkbutton(label = "Bright", command = self.menu_bright_click, variable = self.disp_bright_value)
        menu_disp.add_checkbutton(label = "Profile", command = self.menu_profile_click, variable = self.disp_profile_value)
        self.menubar.add_cascade(label="Disp", menu = menu_disp)
        self.master.config(menu = self.menubar) # type: ignore

        # ステータスバー
        frame_statusbar = tk.Frame(self.master, relief = tk.SUNKEN, bd = 2)
        self.label_framerate = tk.StringVar(value = "--ms/--fps")
        label = tk.Label(frame_statusbar, textvariable = self.label_framerate)
        label.pack(side = tk.RIGHT)
        frame_statusbar.pack(side = tk.BOTTOM, fill = tk.X)

        # GraphicsBoxの追加(オプション設定はtkinterのCanvasクラスと同じ)
        self.graphics = graphicsbox.GraphicsBox(self.master, bg = "dark cyan")
        self.graphics.pack(expand = True, fill = tk.BOTH)

    def init_acapy(self):
        ''' AcaPyの初期化'''
        # AcaPyクラスのインスタンス
        self.capture = acapy.AcaPy()

        self.menubar.entryconfigure(1, label = f"{self.capture.board_name.decode()} ch{self.capture.ch}")

        # iniファイルの読込
        inifilename = filedialog.askopenfilename(
		    title = "Load initial file",
		    filetypes = [("initial file", ".ini")] # ファイルフィルタ
		    )

        if len(inifilename) == 0:
            print("Load inifile error")
            self.capture.dispose()
            sys.exit(0)

        # iniファイルの読込、設定（AcapLib2のiniファイルと共通です）
        ret = self.capture.load_inifile(inifilename)
        if ret == 0:
            print("Load inifile error")
            self.capture.dispose()
            sys.exit(0)

        # GraphicsBoxへ画像全体が表示されるように設定
        self.graphics.zoom_fit(self.capture.width, self.capture.height)

    def snap_click(self):
        '''Snap:1画面取込(連続取込をする場合はGrabを使用のこと)'''

        if self.capture is None:
            return

        ret, frame = self.capture.snap()
        if ret == acapy.AcaPy.OK:
            # カラーの場合、BGRがRGBに変換される
            frame = acapy.AcaPy.bgr2rgb(frame)
            self.graphics.draw_image(frame)
            self.last_disp_image = frame

        self.graphics.focus()

    def grab_update(self, update_time):

        if self.capture is None:
            return    
        if self.capture.is_grab is False:
            return

        ret, frames, count, frame_no = self.capture.read_frames()
        print(f"FrameNo={frame_no}")

        if (frames is None) or (count == 0):
            return

        # 前回取得した画像の次の画像データから現在の画像データを処理する
        for frame in frames: 
            ###########################################
            # 画像処理する場合はここで、frame(numpy.ndarray)を処理する
            ###########################################
            pass

        # 最後に取得した画像の描画
        frame = frames[count - 1]
        # カラーの場合、BGRがRGBに変換される
        frame = acapy.AcaPy.bgr2rgb(frame)
        self.graphics.draw_image(frame)
        self.last_disp_image = frame

        # フレームレートの計算
        fps = frame_no / (time.perf_counter() - self.grab_start_time)
        if fps > 0:
            self.label_framerate.set(f"Frame count:{frame_no} / {1000.0/fps:.2f}ms / {fps:.2f}fps")
    
        # grab_updateメソッドの繰り返し
        self.grab_update_id = self.master.after(update_time, self.grab_update, update_time)

    def grab_click(self):
        '''Grab:連続画面取込'''

        if self.capture is None:
            return

        # grab(連続画像取得)
        if self.capture.is_grab == True:
            # grab中のときはgrabを停止する
            self.capture.grab_stop()
            if self.grab_update_id is not None:
                self.master.after_cancel(self.grab_update_id)

            # メニューの文字を変更
            self.menubar.entryconfigure(3, label = "Grab")
            # メニューを有効にする
            self.menubar.entryconfigure(2, state="normal")
            self.menubar.entryconfigure(4, state="normal")

        else:
            # grab中でないときはGrabを開始する

            self.last_frame_no = 0
            self.last_time = 0          # フレームレート計算用
            self.last_time_frame = 0    # フレームレート計算用

            # メニューの文字を変更
            self.menubar.entryconfigure(3, label = "Stop")
            # メニューを無効にする
            self.menubar.entryconfigure(2, state="disabled")
            self.menubar.entryconfigure(4, state="disabled")

            # 取り込み開始時間
            self.grab_start_time = time.perf_counter()

            # grabの開始
            self.capture.grab_start()

            # 3msec間隔でフレーム画像を確認する
            # 時間を短くすると画像の取りこぼしが少なくなりますが、GUIの動作が重くなります。
            self.grab_update(3)

    def save_click(self):
        '''名前を付けて最後に表示した画像を保存'''
        if self.last_disp_image is None:
            return

        filename = filedialog.asksaveasfilename(
            title = "画像を名前を付けて保存",
            filetypes = [("Bitmap", ".bmp"), ("PNG", ".png"), ("JPEG", ".jpg"), ("Tiff", ".tif") ], # ファイルフィルタ
            defaultextension = "bmp"
            )
        # ファイル名の指定が無いとき
        if len(filename) == 0:
            return
        # ndarrayをPILに変換して保存(日本語ファイル名対応)
        Image.fromarray(self.last_disp_image).save(filename)

    def menu_grid_click(self):
        ''' menuの Disp -> Grid をクリックしたとき '''
        self.graphics.grid_enabled = self.disp_grid_value.get()
        self.graphics.redraw_image()

    def menu_bright_click(self):
        ''' menuの Disp -> Bright をクリックしたとき '''
        self.graphics.bright_enabled = self.disp_bright_value.get()
        self.graphics.redraw_image()

    def menu_profile_click(self):
        ''' menuの Disp -> Profile をクリックしたとき '''
        self.graphics.profile_enabled = self.disp_profile_value.get()
        self.graphics.redraw_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master = root)
    app.mainloop()
