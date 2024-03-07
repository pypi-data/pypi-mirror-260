__version__ = "1.1.0"

'''
////////////////////////////////////////////////////////////
//  Ver.1.1.0 (2023.06.12)    Python 3.8以降対応 
////////////////////////////////////////////////////////////
●AcaPyインスタンス時のボード情報表示の項目追加（DeviceNo, CustomID, FpgaVer, SerialNo）
●プロパティの値の取得方法をAcapLib2から直接取得するように変更

【AcapLib2 Ver.7.3.2対応】
●以下、メソッドの追加
　get_bit_assign_ex(), get_camera_category_feature_list(), get_camera_feature_info(), get_camera_property_list()
  , get_last_error_ex(), 
  regist_frame_end_callback(), regist_grab_end_callback(), regist_gpin_callback(), regist_overwrite_callback(), regist_timeout_callback(), regist_device_alm_callback()
  set_bit_assign_ex(), get_enable_board_ch_list()

●ACL_CAM_FEATURE_INFO構造体, ACL_CAM_PROPERTY_LIST構造体, ACL_CAM_FEATURE_LIST構造体, ACAPERRORINFOEX構造体の追加     

●以下、プロパティの追加
　connection_num, data_mask_ex, debug_print_enabled, encoder_abs_mp_count, 
  encoder_rlt_all_count, encoder_rlt_count, external_trigger_polarity 
  fan_rpm, port_a_assign, port_b_assign, port_c_assign, port_d_assign, port_e_assign, 
  port_f_assign, port_g_assign, port_h_assign, port_i_assign, port_j_assign, 
  serial_read_wait_time, tag, 
  external_trigger_chatter_separate

●以下、プロパティの削除
  cxp_acquision_start_address, cxp_acquision_start_value, cxp_acquision_stop_address, cxp_acquision_stop_valueプロパティの削除

●その他
  カメラが接続されていないチャンネルを指定したときに、is_openedプロパティがFalseにならないバグを修正
  set_power_supplyのタイムアウト時間の初期値を3000mSecから6000mSecへ変更
  set_dma_option_ex(), get_dma_option_ex()は非対応


////////////////////////////////////////////////////////////
//  Ver.1.0.1 (2023.06.12) 
////////////////////////////////////////////////////////////
●ベースとなる acaplib2.py の修正に伴うバージョンアップ（修正内容はacaplib2.pyを参照）

////////////////////////////////////////////////////////////
//  Ver.1.0.0  (2021.06.8) 
////////////////////////////////////////////////////////////
●正式版初版

////////////////////////////////////////////////////////////
//  Ver.0.0.12  (2021.04.12) 
////////////////////////////////////////////////////////////
●プレビュー版
'''
import re

import numpy as np
import sys
import time
#import platform
import signal

import threading



#from ctypes import *
#import ctypes
from typing import Union, List, Tuple

from acapy import acaplib2

# pylint: disable=W0311

# クラス名の置き換え(継承)
class ACL_BUFF_INFO_RESIZE(acaplib2.ACL_BUFF_INFO_RESIZE):
    '''ACL_BUFF_INFO_RESIZE Structure'''
    def __init__(self):
        super().__init__()

class ACL_BUFF_INFO_ROI(acaplib2.ACL_BUFF_INFO_ROI):
    '''ACL_BUFF_INFO_ROI Structure'''
    def __init__(self):
        super().__init__()

class ACL_REGION(acaplib2.ACL_REGION):
    '''ACL_REGION Structure'''
    def __init__(self):
        super().__init__()

# -------------------------------------------------------------------
# Ver.1.0.2 (AcapLib2 Ver.8.0.0対応版)
class ACL_BUFF_INFO_DIVIDE(acaplib2.ACL_BUFF_INFO_DIVIDE):
    '''ACL_BUFF_INFO_DIVIDE Structure'''
    def __init__(self):
        super().__init__()

class ACL_CAM_FEATURE_INFO(acaplib2.ACL_CAM_FEATURE_INFO):
    '''ACL_CAM_FEATURE_INFO Structure'''
    pass

class ACL_CAM_PROPERTY_LIST(acaplib2.ACL_CAM_PROPERTY_LIST):
    '''ACL_CAM_PROPERTY_LIST Structure'''
    pass

class ACL_CAM_FEATURE_LIST(acaplib2.ACL_CAM_FEATURE_LIST):
    '''ACL_CAM_FEATURE_LIST Structure'''
    #super().__init__()
    pass

class ACAPERRORINFOEX(acaplib2.ACAPERRORINFOEX):
    '''ACAPERRORINFOEX Structure'''
    pass

# -------------------------------------------------------------------
class AcaPy():
    '''Python bindings for AVALDATA AcapLib2
    '''

    # クラス変数
    OK : int = acaplib2.ACL_RTN_OK		# エラーなし
    ERROR : int = acaplib2.ACL_RTN_ERROR	# エラーあり

    def __init__(self, board_id: int=0, ch: int=1, debug_print: bool=True):
        '''Initialize the device

        Parameters
        ----------
        board_id : int
            Specify board number(0, 1, 2, ...) which is set up
        ch : int
            The channel(1, 2, 3, ...) to open  
        debug_print : bool
            True to output debug information.

        Returns
        -------
            AcaPy class object

        '''


        # SIGINTシグナルを無視(Ctrl+Cでの終了の抑制)
        signal.signal(signal.SIGINT, signal.SIG_IGN)

        # プロパティ初期値

        # AcapLib2のDLLファイルバージョンの取得
        ret, self.__acaplib2_version = acaplib2.AcapGetFileVersion(acaplib2._acap_dll_path)
        #self.__acaplib2_version = self.__acaplib2_version.split('.')

        # プロパティの値の初期値設定
        self.__hHandle = acaplib2.INVALID_HANDLE_VALUE
        self.__board_name = b''
        self.__board_id = board_id
        self.__ch = ch
        self.__mem_num : int = 4
        self.__timeout = 1000

        self.__device = 0
        self.__custom = 0
        self.__channel_num = 0
        self.__serial_no = 0

        self.__create_ring_buffer_flag = False

        self.__disposed = True

        # ▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽
        # AcapLib2 Ver.8.0.0より設定不要
        #self.__cxp_acquision_start_address = 0
        #self.__cxp_acquision_start_value = 0
        #self.__cxp_acquision_stop_address = 0
        #self.__cxp_acquision_stop_value = 0
        #self.__cxp_pixel_format_address = 0
        #self.__cxp_pixel_format = 0
        # △△△△△△△△△△△△△△△△△△△△△△△△△△△△△△△△△△△△△△△△△

        #self.__driver_name = 0
        #self.__hw_protect = 0

        # self.__images : List[np.ndarray] = []
        # #**********************************************************

        self.__is_opened : bool = False
        self.__is_grab : bool = False
        self.__last_frame_no = 0
        self.__input_num = 0

        self.__is_serial_open = False

        self.__debug_print = debug_print

        self.__have_started_grab = False # 1度でもgrab_startを行ったらTrue(プログラム起動時のframe_noが残っているのを回避)

        # -------------------------------------------------------------------
        # Ver.1.0.2 (AcapLib2 Ver.8.0.0対応版)

        #【AcapLib2 Ver.7.3.1対応】

        #self.__acquisition_stop = 0 # ACL_ACQUISITION_STOP

        #【AcapLib2 Ver.7.3.2対応】
        #●AcapGetCameraFeatureInfo()関数、AcapGetCameraCategoryFeatureList()関数、AcapGetCameraPropertyList()関数、AcapGetLastErrorCodeEx()関数の追加

        # 新規追加
        self.__serial_read_wait_time = 0.2
        self.__tag = ""   # 汎用プロパティ

        # -------------------------------------------------------------------

        # ボード情報の取得
        ret, bdInfo = acaplib2.AcapGetBoardInfoEx()
        if ret != AcaPy.OK:
            self.print_last_error()

        boardnum = bdInfo.nBoardNum
        if boardnum == 0:
            boardnum = 1 # Virtualを許容するため

        # 指定されたボード番号の検索
        board_index = None
        for i in range(boardnum):
            if board_id == bdInfo.boardIndex[i].nBoardID:
                board_index = bdInfo.boardIndex[i]
                break

        if board_index is None:
            # 指定されたボード番号が見つからなかったとき
            return

        # ch == 0 の全チャンネルオープンは非対応
        if ch < 1:
            return      
        # チャンネル番号の確認→nChannelNumが正しい値が拾えない場合があるため、エラーチェックをしない
        #if ch > board_index.nChannelNum:
        #    return

        # プロパティの値を取得
        self.__board_id = board_id
        self.__board_name = board_index.pBoardName
        self.__device = board_index.nDevice
        self.__custom = board_index.nCustom
        self.__channel_num = board_index.nChannelNum
        self.__serial_no = board_index.nSerialNo

        self.__ch = ch

        # コールバック関数の初期化
        self.__callback_func = None
        self.__frame_end_callback = None
        self.__frame_copy_flag = False
        self.__grab_start_callback = None
        self.__grab_end_callback = None
        self.__gpin_callback = None
        #self.__overflow_callback = None
        self.__overwrite_callback = None
        self.__timeout_callback = None
        self.__device_alm_callback = None

        self.__thread_polling = None

        # ボードオープン
        self.__hHandle = acaplib2.AcapOpen(board_index.pBoardName, board_index.nBoardID, ch)
        if self.__hHandle == acaplib2.INVALID_HANDLE_VALUE:
            # 二重オープンなど
            self.print_last_error()
            #self.__disposed = True #
            #Open出来ていないので、Disposeの必要なし（クラスのインスタンスとしては残ってしまう）
            return
        else:
            # ボードがオープン出来たとき
            #self._debug_print("OS:", platform.system(), platform.version()) #
            #Windows11だと正しく拾えない
            self.__disposed = False # Disposeしていない（Disposeする必要がある）
            self._debug_print("Python version: " + sys.version + "\n" + "AcaPy version: " + __version__ + "\n" + "AcapLib2 version: " + self.__acaplib2_version + "\n" + "AcapOpen: boardname={0}, bordID={1}, Ch={2}, handle={3}, DeviceNo={4}, CustomID={5}, FpgaVer={6}, SerialNo={7}".format(acaplib2.byte_decode(board_index.pBoardName), board_index.nBoardID, ch, self.__hHandle, hex(board_index.nDevice), hex(board_index.nCustom), hex(board_index.nFpgaVer), board_index.nSerialNo))
   
        # カメラの接続確認（カメラの電源が入っているか？を確認）
        if acaplib2.byte_decode(board_index.pBoardName) != "Virtual":
            if self.camera_state != 1:
                # カメラが接続されていてもPoCLがOffの場合は、ここに入る
                self._debug_print(f"{acaplib2.byte_decode(board_index.pBoardName)} (bordID={board_index.nBoardID} Ch={ch}) Camera not connected")
                #return  # ここで抜けない
            else:
                # カメラを認識した場合
                self.__is_opened = True
        else:
            # Virtualのとき
            self.__is_opened = True

        #self.__is_opened = True
        self.__reflect_param_flag = True # reflect_paramが必要な場合はTrue
        self.__create_ring_buffer_flag = True # create_ring_buffer()が必要な場合はTrue

        # イベント登録
        old_debug_print = self.__debug_print
        self.__debug_print = False # ボードにより非対応IDがあるため、エラー表示を一時非表示にする。
        ret = self._set_event(acaplib2.ACL_INT_GRABSTART, 1) # 各フレームの取込開始時にあがるイベント
        ret = self._set_event(acaplib2.ACL_INT_FRAMEEND, 1)
        ret = self._set_event(acaplib2.ACL_INT_GRABEND, 1)
        ret = self._set_event(acaplib2.ACL_INT_GPIN, 1)
        ret = self._set_event(acaplib2.ACL_INT_DEVICE_ALM, 1)
        self.__debug_print = old_debug_print # エラー表示を元に戻す。

    def dispose(self):
        '''Releases resources inside the class.
        '''
        if self.__disposed is True:
            return

        if self.is_opened is True:
            if self.is_grab is True:
                self.grab_abort()

        self.serial_close()

        # 値の反映の待ち時間を０にする(AcapSetBufferAddress()が影響を受ける)
        #self.cxp_bdlink_timeout = 0
        #self.cxp_camlink_timeout = 0

        if self.__hHandle != acaplib2.INVALID_HANDLE_VALUE:
            # バッファを解除
            #acaplib2.AcapSetBufferAddress(
            #    self.__hHandle, 
            #    self.__ch, 
            #    acaplib2.ACL_IMAGE_PTR, 
            #    0, 
            #    0)
            # イベント解除
            old_debug_print = self.__debug_print
            self.__debug_print = False # ボードにより非対応IDがあるため、エラー表示を一時非表示にする。
            self._set_event(acaplib2.ACL_INT_GRABSTART, 0)
            self._set_event(acaplib2.ACL_INT_FRAMEEND, 0)
            self._set_event(acaplib2.ACL_INT_GRABEND, 0)
            self._set_event(acaplib2.ACL_INT_GPIN, 0)
            self._set_event(acaplib2.ACL_INT_DEVICE_ALM, 0)
            self.__debug_print = old_debug_print # エラー表示を元に戻す。

            # ボードクローズ
            ret = acaplib2.AcapClose(self.__hHandle, self.__ch)
            if ret == 1:
                self._debug_print(f"AcapClose ID={self.board_id} CH={self.ch}")
                self.__is_opened = False

        self.__is_grab = False # frame_endのwhileのフラグ
        self.__disposed = True

    def __del__(self):
        self.dispose()

    ##############################################################

    def _callback_proc(self, nCH, ulEvent, nFrame, nIndex):
        '''コールバック'''
        # AcapLib2のコールバックのnFrame, nIndexの値はqueueされた値なので、時間にズレが生じる場合がある。

        if (ulEvent & acaplib2.ACL_INT_GPIN) == acaplib2.ACL_INT_GPIN:
            if self.__gpin_callback is not None:
                ret, gpin_polarity = acaplib2.AcapGetInfo(self.__hHandle, self.__ch, acaplib2.ACL_GPIN_POL, 0)
                self._callback_handler(self.__gpin_callback, self, gpin_polarity)

        if (ulEvent & acaplib2.ACL_INT_TIMEOUT) == acaplib2.ACL_INT_TIMEOUT:
            if self.__timeout_callback is not None:
                self._callback_handler(self.__timeout_callback, self)

        if (ulEvent & acaplib2.ACL_INT_DEVICE_ALM) == acaplib2.ACL_INT_DEVICE_ALM:
            if self.__device_alm_callback is not None:
                ret, alarm_status = self.get_info(acaplib2.ACL_ALARM_STATUS)
                self._callback_handler(self.__device_alm_callback, self, alarm_status)

        if (ulEvent & acaplib2.ACL_INT_GRABSTART) == acaplib2.ACL_INT_GRABSTART:
            if self.__grab_start_callback is not None:
                self._callback_handler(self.__grab_start_callback, self)
        
    def _regist_callback_func(self):
        if self.__callback_func is not None:
            return
        self.__callback_func = acaplib2.callback_functionType(self._callback_proc) # __callback_func がガベコレされないようにするのが重要

        ret = acaplib2.AcapRegistCallback(self.__hHandle, self.__ch, (acaplib2.ACL_INT_GRABSTART | acaplib2.ACL_INT_GPIN | acaplib2.ACL_INT_TIMEOUT | acaplib2.ACL_INT_DEVICE_ALM), self.__callback_func)
        if ret != AcaPy.OK:
            self.print_last_error()

    def _callback_handler(self, func, *args):

        ret = 0

        if func is None:
            return ret

        try:
            ret = func(*args)
        except Exception as ex:
            self._debug_print(f"[Callback Error ID={self.board_id} CH={self.ch}] {ex}")

        return ret

    def regist_frame_end_callback(self, frame_end_func, frame_copy_flag: bool=False):
        '''Register a callback function for FrameEnd.

        Parameters
        ----------
        frame_end_func : Function
            Function called by callback function
        frame_copy_flag : bool
            Specifies whether or not to copy and retrieve image data.
            True : Copy  
            False :Not copy(Default)

        '''
        #self._regist_callback_func() # AcapLib2のコールバックの登録
        self.__frame_end_callback = frame_end_func
        self.__frame_copy_flag = frame_copy_flag

    def _regist_grab_start_callback(self, grab_start_func):
        '''Register a callback function for GrabStart.

        Parameters
        ----------
        grab_start_func : Function
            Function called by callback function
        '''
        self.__grab_start_callback = grab_start_func

    def regist_grab_end_callback(self, grab_end_func):
        '''Register a callback function for GrabEnd.

        Parameters
        ----------
        grab_end_func : Function
            Function called by callback function
        '''
        self.__grab_end_callback = grab_end_func

    def regist_gpin_callback(self, gpin_func):
        '''Register a callback function for GPIN.

        Parameters
        ----------
        gpin_func : Function
            Function called by callback function
        '''
        self._regist_callback_func()
        self.__gpin_callback = gpin_func

    def regist_overwrite_callback(self, overwrite_func):
        '''Register a callback function for OverWrite.

        Parameters
        ----------
        overwrite_func : Function
            Function called by callback function
        '''
        #self._regist_callback_func()
        self.__overwrite_callback = overwrite_func

    def regist_timeout_callback(self, timeout_func):
        '''Register a callback function for TimeOut.

        Parameters
        ----------
        timeout_func : Function
            Function called by callback function
        '''
        self._regist_callback_func()
        self.__timeout_callback = timeout_func

    def regist_device_alm_callback(self, device_alm_func):
        '''Register a callback function for device alarm.

        Parameters
        ----------
        device_alm_func : Function
            Function called by callback function
        '''
        self._regist_callback_func()
        self.__device_alm_callback = device_alm_func       

    @property
    def is_opened(self):
        '''Gets true if the grabber board is open.'''
        return self.__is_opened 

    @property
    def is_grab(self):
        '''Gets true when in a grab.'''
        return self.__is_grab

    @property
    def acaplib2_version(self):
        '''Get the version of AcapLib2.'''
        return self.__acaplib2_version 

    @property
    def handle(self):
        '''Get a library handle for AcapLib2.'''
        return self.__hHandle 

    @property
    def board_id(self):
        '''Get the configured board ID.'''
        return self.__board_id

    @property
    def board_name(self):
        '''Get the name of the board in use.'''
        return self.__board_name

    @property
    def device(self):
        '''Get the device name.'''
        return self.__device

    @property
    def custom(self):
        '''Get the FPGA customization number.'''
        return self.__custom

    @property
    def channel_num(self):
        '''Get the total number of channels on the board.'''
        return self.__channel_num

    @property
    def serial_no(self):
        '''Get the serial number of the board.'''
        return self.__serial_no

    @property
    def ch(self):
        '''Get the specified channel number.'''
        return self.__ch

    @property
    def scan_system(self):
        _, value = self.get_info(acaplib2.ACL_SCAN_SYSTEM)
        return value
    @scan_system.setter
    def scan_system(self, value: int):
        '''Get or set the type of camera(area or line).

        Parameters
        ----------
        value : int
            0 : Area sensor
            1 : Line sensor
        '''
        _ = self.set_info(acaplib2.ACL_SCAN_SYSTEM, value)

    @property
    def width(self):
        _, value = self.get_info(acaplib2.ACL_X_SIZE)
        return value
    @width.setter
    def width(self, value: int):
        '''Gets or set the number of pixels for the width of the image to be acquired.
        '''
        ret = self.set_info(acaplib2.ACL_X_SIZE, value)
        if ret == acaplib2.ACL_RTN_OK:
            # リングバッファの確保が必要
            self.__create_ring_buffer_flag = True

    @property
    def height(self):
        _, value = self.get_info(acaplib2.ACL_Y_SIZE)
        return value
    @height.setter
    def height(self, value: int):
        '''Gets or set the number of pixels for the height of the image to be acquired.
        '''        
        ret = self.set_info(acaplib2.ACL_Y_SIZE, value)
        if ret == acaplib2.ACL_RTN_OK:
            ret = self.set_info(acaplib2.ACL_Y_TOTAL, value)
            if ret == acaplib2.ACL_RTN_OK:
                # リングバッファの確保が必要
                self.__create_ring_buffer_flag = True

    @property
    def mem_num(self):
        return self.__mem_num
    @mem_num.setter
    def mem_num(self, value: int):
        '''Get or set the number of images in the ring buffer.'''

        ret = self.set_info(acaplib2.ACL_MEM_NUM, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__mem_num = value
            # リングバッファの確保が必要
            self.__create_ring_buffer_flag = True

    @property
    def x_delay(self):
        _, value = self.get_info(acaplib2.ACL_X_DELAY)
        return value
    @x_delay.setter
    def x_delay(self, value: int):
        '''Get or set the X-direction delay of camera input'''
        _ = self.set_info(acaplib2.ACL_X_DELAY, value)

    @property
    def y_delay(self):
        _, value = self.get_info(acaplib2.ACL_Y_DELAY)
        return value
    @y_delay.setter
    def y_delay(self, value: int):
        '''Get or set the X-direction delay of camera input'''
        _ = self.set_info(acaplib2.ACL_Y_DELAY, value)

    @property
    def y_total(self):
        _, value = self.get_info(acaplib2.ACL_Y_TOTAL)
        return value
    @y_total.setter
    def y_total(self, value: int):
        '''Get or set the number of lines to be input from the camera.'''
        _ = self.set_info(acaplib2.ACL_Y_TOTAL, value)

    @property
    def camera_bit(self):
        _, value = self.get_info(acaplib2.ACL_CAM_BIT)
        return value
    @camera_bit.setter
    def camera_bit(self, value: int):
        '''Gets or set the number of bits in the camera image.'''
        ret = self.set_info(acaplib2.ACL_CAM_BIT, value)
        if ret == acaplib2.ACL_RTN_OK:
            # リングバッファの確保が必要
            self.__create_ring_buffer_flag = True 

    @property
    def board_bit(self):
        _, value = self.get_info(acaplib2.ACL_BOARD_BIT)
        return value

    @property
    def pix_shift(self):
        _, value = self.get_info(acaplib2.ACL_PIX_SHIFT)
        return value
    @pix_shift.setter
    def pix_shift(self, value: int):
        '''Get or set the number of bits to be right-shifted in the camera image data.'''
        _ = self.set_info(acaplib2.ACL_PIX_SHIFT, value)

    @property
    def timeout(self):
        return self.__timeout
    @timeout.setter
    def timeout(self, value: int):
        '''Get or set the timeout period in milliseconds for waiting for image input.'''
        ret = self.set_info(acaplib2.ACL_TIME_OUT, value, 1) #reflect_param()が不要のため
        if ret == acaplib2.ACL_RTN_OK:
            self.__timeout = value

    @property
    def cc_polarity(self):
        _, value = self.get_info(acaplib2.ACL_EXP_POL)
        return value
    @cc_polarity.setter
    def cc_polarity(self, value: int):
        '''Get or set the output logic of the exposure signal.'''
        _ = self.set_info(acaplib2.ACL_EXP_POL, value)#, 1)

    @property
    def trigger_polarity(self):
        return self.cc_polarity
    @trigger_polarity.setter
    def trigger_polarity(self, value: int):
        '''Get or set the output logic of the exposure signal.'''
        self.cc_polarity = value

    @property
    def cc1_polarity(self):
        _, value = self.get_info(acaplib2.ACL_CC1_LEVEL)
        return value
    @cc1_polarity.setter
    def cc1_polarity(self, value: int):
        '''Get or set the signal output level of CC1.'''
        _ = self.set_info(acaplib2.ACL_CC1_LEVEL, value, 1) #直接設定、reflect_param()が不要のため

    @property
    def cc2_polarity(self):
        _, value = self.get_info(acaplib2.ACL_CC2_LEVEL)
        return value
    @cc2_polarity.setter
    def cc2_polarity(self, value: int):
        '''Get or set the signal output level of CC2.'''
        _ = self.set_info(acaplib2.ACL_CC2_LEVEL, value, 1) #直接設定、reflect_param()が不要のため

    @property
    def cc3_polarity(self):
        _, value = self.get_info(acaplib2.ACL_CC3_LEVEL)
        return value
    @cc3_polarity.setter
    def cc3_polarity(self, value: int):
        '''Get or set the signal output level of CC3.'''
        _ = self.set_info(acaplib2.ACL_CC3_LEVEL, value, 1) #直接設定、reflect_param()が不要のため

    @property
    def cc4_polarity(self):
        _, value = self.get_info(acaplib2.ACL_CC4_LEVEL)
        return value
    @cc4_polarity.setter
    def cc4_polarity(self, value: int):
        '''Get or set the signal output level of CC4.'''
        _ = self.set_info(acaplib2.ACL_CC4_LEVEL, value, 1) #直接設定、reflect_param()が不要のため

    @property
    def cc_cycle(self):
        _, value = self.get_info(acaplib2.ACL_EXP_CYCLE)
        return value
    @cc_cycle.setter
    def cc_cycle(self, value: int):
        '''Get or set the exposure cycle.'''
        if value <= self.exposure:
            #self._debug_print("[Error] set cc_cycle: 'cc_cycle'({0}) must be
            #larger than 'exposure'({1}).".format(value, self.exposure))
            self._debug_print(f"[Error ID={self.board_id} CH={self.ch}] set cc_cycle: 'cc_cycle'({value}) must be larger  than 'exposure'({self.exposure}).")
            return
        _ = self.set_info(acaplib2.ACL_EXP_CYCLE, value)#, 1)

    @property
    def cc_cycle_ex(self):
        _, value = self.get_info(acaplib2.ACL_EXP_CYCLE_EX)
        return value
    @cc_cycle_ex.setter
    def cc_cycle_ex(self, value: int):
        '''Get or set the exposure cycle(100nsec).'''
        if value <= self.exposure_ex:
            self._debug_print(f"[Error ID={self.board_id} CH={self.ch}] set cc_cycle_ex: 'cc_cycle_ex'({value}) must be larger  than 'exposure_ex'({self.exposure_ex}).")
            return
        _ = self.set_info(acaplib2.ACL_EXP_CYCLE_EX, value)#, 1)

    @property
    def exposure(self):
        _, value = self.get_info(acaplib2.ACL_EXPOSURE)
        return value
    @exposure.setter
    def exposure(self, value: int):
        '''Get or set the exposure time.'''
        if value >= self.cc_cycle:
            self._debug_print(f"[Error ID={self.board_id} CH={self.ch}] set exposure: 'exposure'({value}) must be smaller than 'cc_cycle'({self.cc_cycle}).")
            return
        _ = self.set_info(acaplib2.ACL_EXPOSURE, value)#, 1)
      
    @property
    def exposure_ex(self):
        _, value = self.get_info(acaplib2.ACL_EXPOSURE_EX)
        return value
    @exposure_ex.setter
    def exposure_ex(self, value: int):
        '''Get or set the exposure time(100nsec).'''
        if value >= self.cc_cycle_ex:
            self._debug_print("[Error ID={self.board_id} CH={self.ch}] set exposure_ex: 'exposure_ex'({value}) must be smaller than 'cc_cycle_ex'({self.cc_cycle_ex}).")
            return
        _ = self.set_info(acaplib2.ACL_EXPOSURE_EX, value)#, 1)  
        
    def _set_register(self, reg_type, adress, value):
        ret = acaplib2.AcapSetReg(self.__hHandle, self.__ch, reg_type, adress, value)
        return ret

    def _get_register(self, reg_type, adress):
        ret, regData = acaplib2.AcapGetReg(self.__hHandle, self.__ch, reg_type, adress)
        return ret, regData.value

    @property
    def exposure_reg_ex(self):
        _, regData = self._get_register(0, 0) # ボード種別の取得
        if regData == 0x7DF1606F:
            _, regData = self._get_register(0, 0x10804 + self.__ch * 0x1000)
        else:
            _, regData = self._get_register(0, 0x18 + self.__ch * 0x1000)
        return regData

    @exposure_reg_ex.setter
    def exposure_reg_ex(self, value: int):
        '''Get or set the exposure time via registers(100nsec).'''
        if value >= self.cc_cycle_ex:
            self._debug_print("[Error ID={self.board_id} CH={self.ch}] set exposure_reg_ex: 'exposure_reg_ex'({value}) must be smaller than 'cc_cycle_ex'({self.cc_cycle_ex}).")
            return
   
        _, regData = self._get_register(0, 0) # ボード種別の取得
        if regData == 0x7DF1606F:   # 36124系
            _ = self._set_register(0, 0x10804 + self.__ch * 0x1000, value)
        else:                       # それ以外
            _ = self._set_register(0, 0x18 + self.__ch * 0x1000, value)

    @property
    def cc_delay(self):
        _, value = self.get_info(acaplib2.ACL_CC_DELAY)
        return value
    @cc_delay.setter
    def cc_delay(self, value: int):
        '''Get or set the delay time(usec) for the exposure signal output.'''
        _ = self.set_info(acaplib2.ACL_CC_DELAY, value)

    @property
    def cc_out_no(self):
        _, value = self.get_info(acaplib2.ACL_EXP_CC_OUT)
        return value
    @cc_out_no.setter
    def cc_out_no(self, value: int):
        '''Get or set the channel for the exposure signal.'''
        _ = self.set_info(acaplib2.ACL_EXP_CC_OUT, value)

    @property
    def rolling_shutter(self):
        _, value = self.get_info(acaplib2.ACL_ROLLING_SHUTTER)
        return value
    @rolling_shutter.setter
    def rolling_shutter(self, value: int):
        '''Get or set to use or not use the rolling shutter.'''
        _ = self.set_info(acaplib2.ACL_ROLLING_SHUTTER, value)

    @property
    def external_trigger_enable(self):
        _, value = self.get_info(acaplib2.ACL_EXT_EN)
        return value
    @external_trigger_enable.setter
    def external_trigger_enable(self, value: int):
        '''Get or set the signal to be used for the external trigger.'''
        _ = self.set_info(acaplib2.ACL_EXT_EN, value)

    @property
    def external_trigger_mode(self):
        _, value = self.get_info(acaplib2.ACL_EXT_MODE)
        return value
    @external_trigger_mode.setter
    def external_trigger_mode(self, value: int):
        '''Get or set the method of outputting the CC signal with a single external trigger.'''
        _ = self.set_info(acaplib2.ACL_EXT_MODE, value)

    @property
    def external_trigger_chatter(self):
        _, value = self.get_info(acaplib2.ACL_EXT_CHATTER)
        return value
    @external_trigger_chatter.setter
    def external_trigger_chatter(self, value: int):
        '''Get or set the external trigger detection disable time(usec).'''
        _ = self.set_info(acaplib2.ACL_EXT_CHATTER, value)

    @property
    def external_trigger_delay(self):
        _, value = self.get_info(acaplib2.ACL_EXT_DELAY)
        return value
    @external_trigger_delay.setter
    def external_trigger_delay(self, value: int):
        '''Get or set the external trigger detection delay time.'''
        _ = self.set_info(acaplib2.ACL_EXT_DELAY, value)

    @property
    def encoder_enable(self):
        _, value = self.get_info(acaplib2.ACL_ENC_EN)
        return value
    @encoder_enable.setter
    def encoder_enable(self, value: int):
        '''Get or set the delay time(usec) for external trigger detection.
        0: Do not use the encoder
        1: Relative count mode
        2: Absolute count mode
        '''
        _ = self.set_info(acaplib2.ACL_ENC_EN, value)

    @property
    def encoder_start(self):
        _, value = self.get_info(acaplib2.ACL_ENC_START)
        return value
    @encoder_start.setter
    def encoder_start(self, value: int):
        '''Get or set how the external trigger is used by the encoder.'''
        _ = self.set_info(acaplib2.ACL_ENC_START, value)

    @property
    def encoder_mode(self):
        _, value = self.get_info(acaplib2.ACL_ENC_MODE)
        return value
    @encoder_mode.setter
    def encoder_mode(self, value: int):
        '''Get or set the operation mode of the encoder.'''
        _ = self.set_info(acaplib2.ACL_ENC_MODE, value)

    @property
    def encoder_phase(self):
        _, value = self.get_info(acaplib2.ACL_ENC_PHASE)
        return value
    @encoder_phase.setter
    def encoder_phase(self, value: int):
        '''Get or set the encoder input pulses.'''
        _ = self.set_info(acaplib2.ACL_ENC_PHASE, value)

    @property
    def encoder_rlt_all_count(self):
        '''Get the total count value when relative count is used.'''
        _, value = self.get_info(acaplib2.ACL_ENC_RLT_ALL_COUNT)
        return value

    @property
    def encoder_rlt_count(self):
        '''Get the relative count value when relative count is used.'''
        _, value = self.get_info(acaplib2.ACL_ENC_RLT_COUNT)
        return value

    @property
    def encoder_direction(self):
        _, value = self.get_info(acaplib2.ACL_ENC_DIRECTION)
        return value
    @encoder_direction.setter
    def encoder_direction(self, value: int):
        '''Get or set the rotation direction of the encoder.'''
        _ = self.set_info(acaplib2.ACL_ENC_DIRECTION, value)

    @property
    def encoder_z_phase(self):
        _, value = self.get_info(acaplib2.ACL_ENC_ZPHASE_EN)
        return value
    @encoder_z_phase.setter
    def encoder_z_phase(self, value: int):
        '''Get or set the use or non-use of phase Z for encoder startup.'''
        _ = self.set_info(acaplib2.ACL_ENC_ZPHASE_EN, value)

    @property
    def encoder_compare_reg_1(self):
        _, value = self.get_info(acaplib2.ACL_ENC_COMPARE_1)
        return value
    @encoder_compare_reg_1.setter
    def encoder_compare_reg_1(self, value: int):
        '''Get or set the number of encoder delay pulses.'''
        _ = self.set_info(acaplib2.ACL_ENC_COMPARE_1, value)

    @property
    def encoder_compare_reg_2(self):
        _, value = self.get_info(acaplib2.ACL_ENC_COMPARE_2)
        return value
    @encoder_compare_reg_2.setter
    def encoder_compare_reg_2(self, value: int):
        '''Get or set the number of dividing pulses of the encoder.'''
        _ = self.set_info(acaplib2.ACL_ENC_COMPARE_2, value)

    @property
    def encoder_abs_mode(self):
        _, value = self.get_info(acaplib2.ACL_ENC_ABS_MODE)
        return value
    @encoder_abs_mode.setter
    def encoder_abs_mode(self, value: int):
        '''Get or set the encoder absolute count mode.'''
        _ = self.set_info(acaplib2.ACL_ENC_ABS_MODE, value, 1) # memnumに意味なし(reflect_paramのフラグを立てない)

    # set/get_encoder_abs_multipointメソッドにしている
    #@property
    #def encoder_abs_mp_count(self):
    #    _, value = self.get_info(acaplib2.ACL_ENC_ABS_MP_COUNT)
    #    return value
    #@encoder_abs_mp_count.setter
    #def encoder_abs_mp_count(self, value: int):
    #    '''Get or set the encoder multipoint count.'''
    #    _ = self.set_info(acaplib2.ACL_ENC_ABS_MP_COUNT, value, 1)

    @property
    def encoder_abs_start(self):
        _, value = self.get_info(acaplib2.ACL_ENC_ABS_START)
        return value
    @encoder_abs_start.setter
    def encoder_abs_start(self, value: int):
        '''Get or set the status of the absolute count (operating or stopped).'''
        _ = self.set_info(acaplib2.ACL_ENC_ABS_START, value, 1) # memnumに意味なし(reflect_paramのフラグを立てない)

    @property
    def encoder_abs_count(self) -> int:
        '''Get the absolute count value of the encoder.'''
        _, count = self.get_info(acaplib2.ACL_ENC_ABS_COUNT)
        return count

    @property
    def strobe_enable(self):
        _, value = self.get_info(acaplib2.ACL_STROBE_EN)
        return value
    @strobe_enable.setter
    def strobe_enable(self, value: int):
        '''Get or set the strobe enable(1)/disable(0) setting.'''
        _ = self.set_info(acaplib2.ACL_STROBE_EN, value, 1) # memnumに意味なし(reflect_paramのフラグを立てない)

    @property
    def strobe_delay(self):
        _, value = self.get_info(acaplib2.ACL_STROBE_DELAY)
        return value
    @strobe_delay.setter
    def strobe_delay(self, value: int):
        '''Get or set the strobe signal output delay time(usec).'''
        _ = self.set_info(acaplib2.ACL_STROBE_DELAY, value)

    @property
    def strobe_time(self):
        _, value = self.get_info(acaplib2.ACL_STROBE_TIME)
        return value
    @strobe_time.setter
    def strobe_time(self, value):
        '''Get or set the strobe signal output time(usec).'''
        _ = self.set_info(acaplib2.ACL_STROBE_TIME, value)

    @property
    def reverse_dma_enable(self):
        _, value = self.get_info(acaplib2.ACL_REVERSE_DMA)
        return value
    @reverse_dma_enable.setter
    def reverse_dma_enable(self, value: int):
        '''Enables(1)/Disables(0) reverse DMA in the Y direction.'''
        _ = self.set_info(acaplib2.ACL_REVERSE_DMA, value)

    @property
    def dval_enable(self):
        _, value = self.get_info(acaplib2.ACL_DVAL_EN)
        return value
    @dval_enable.setter
    def dval_enable(self, value: int):
        '''Get or set whether or not to refer to the DVAL signal when inputting camera data.'''
        _ = self.set_info(acaplib2.ACL_DVAL_EN, value)

    @property
    def tap_num(self):
        _, value = self.get_info(acaplib2.ACL_TAP_NUM)
        return value
    @tap_num.setter
    def tap_num(self, value: int):
        '''Get or set the number of input taps.'''
        _ = self.set_info(acaplib2.ACL_TAP_NUM, value)

    @property
    def tap_arrange(self):
        _, value = self.get_info(acaplib2.ACL_TAP_ARRANGE)
        return value
    @tap_arrange.setter
    def tap_arrange(self, value: int):
        '''Get or set the tap rearrangement method for camera data input.'''
        _ = self.set_info(acaplib2.ACL_TAP_ARRANGE, value)

    @property
    def tap_arrange_x_size(self):
        _, value = self.get_info(acaplib2.ACL_ARRANGE_XSIZE)
        return value
    @tap_arrange_x_size.setter
    def tap_arrange_x_size(self, value: int):
        '''Get or set the total number of pixels that the camera outputs as one line.'''
        _ = self.set_info(acaplib2.ACL_ARRANGE_XSIZE, value)

    @property
    def tap_direction1(self):
        _, value = self.get_info(acaplib2.ACL_TAP_DIRECTION, 1)
        return value
    @tap_direction1.setter
    def tap_direction1(self, value: int):
        '''Get or set the input direction for Camera Link tap1.'''
        _ = self.set_info(acaplib2.ACL_TAP_DIRECTION, value, -1)

    @property
    def tap_direction2(self):
        _, value = self.get_info(acaplib2.ACL_TAP_DIRECTION, 2)
        return value
    @tap_direction2.setter
    def tap_direction2(self, value: int):
        '''Get or set the input direction for Camera Link tap2.'''
        _ = self.set_info(acaplib2.ACL_TAP_DIRECTION, value, -2)

    @property
    def tap_direction3(self):
        _, value = self.get_info(acaplib2.ACL_TAP_DIRECTION, 3)
        return value
    @tap_direction3.setter
    def tap_direction3(self, value: int):
        '''Get or set the input direction for Camera Link tap3.'''
        _ = self.set_info(acaplib2.ACL_TAP_DIRECTION, value, -3)

    @property
    def tap_direction4(self):
        _, value = self.get_info(acaplib2.ACL_TAP_DIRECTION, 4)
        return value
    @tap_direction4.setter
    def tap_direction4(self, value: int):
        '''Get or set the input direction for Camera Link tap4.'''
        _ = self.set_info(acaplib2.ACL_TAP_DIRECTION, value, -4)

    @property
    def tap_direction5(self):
        _, value = self.get_info(acaplib2.ACL_TAP_DIRECTION, 5)
        return value
    @tap_direction5.setter
    def tap_direction5(self, value: int):
        '''Get or set the input direction for Camera Link tap5.'''
        _ = self.set_info(acaplib2.ACL_TAP_DIRECTION, value, -5)

    @property
    def tap_direction6(self):
        _, value = self.get_info(acaplib2.ACL_TAP_DIRECTION, 6)
        return value
    @tap_direction6.setter
    def tap_direction6(self, value: int):
        '''Get or set the input direction for Camera Link tap6.'''
        _ = self.set_info(acaplib2.ACL_TAP_DIRECTION, value, -6)

    @property
    def tap_direction7(self):
        _, value = self.get_info(acaplib2.ACL_TAP_DIRECTION, 7)
        return value
    @tap_direction7.setter
    def tap_direction7(self, value: int):
        '''Get or set the input direction for Camera Link tap7.'''
        _ = self.set_info(acaplib2.ACL_TAP_DIRECTION, value, -7)

    @property
    def tap_direction8(self):
        _, value = self.get_info(acaplib2.ACL_TAP_DIRECTION, 8)
        return value
    @tap_direction8.setter
    def tap_direction8(self, value: int):
        '''Get or set the input direction for Camera Link tap8.'''
        _ = self.set_info(acaplib2.ACL_TAP_DIRECTION, value, -8)

    @property
    def tap_direction9(self): # 2023.08.31 追加
        _, value = self.get_info(acaplib2.ACL_TAP_DIRECTION, 9)
        return value
    @tap_direction9.setter
    def tap_direction9(self, value: int):
        '''Get or set the input direction for Camera Link tap9.'''
        _ = self.set_info(acaplib2.ACL_TAP_DIRECTION, value, -9)

    @property
    def tap_direction10(self): # 2023.08.31 追加
        _, value = self.get_info(acaplib2.ACL_TAP_DIRECTION, 10)
        return value
    @tap_direction10.setter
    def tap_direction10(self, value: int):
        '''Get or set the input direction for Camera Link tap10.'''
        _ = self.set_info(acaplib2.ACL_TAP_DIRECTION, value, -10)

    @property
    def sync_lt(self):
        _, value = self.get_info(acaplib2.ACL_SYNC_LT)
        return value
    @sync_lt.setter
    def sync_lt(self, value: int):
        '''Get or set whether or not to synchronize the exposure signal output with the SYNCLT input.'''
        _ = self.set_info(acaplib2.ACL_SYNC_LT, value)

    @property
    def gpout_sel(self):
        _, value = self.get_info(acaplib2.ACL_GPOUT_SEL)
        return value
    @gpout_sel.setter
    def gpout_sel(self, value: int):
        '''Get or set whether the output of the GP_OUT pin is a general-purpose output(1) or a capture flag(0).'''
        _ = self.set_info(acaplib2.ACL_GPOUT_SEL, value, 1) # memnumに意味なし(reflect_paramのフラグを立てない)

    @property
    def gpout_pol(self):
        _, value = self.get_info(acaplib2.ACL_GPOUT_POL)
        return value
    @gpout_pol.setter
    def gpout_pol(self, value: int):
        '''Get or set the output level of the GP_OUT pin.'''
        _ = self.set_info(acaplib2.ACL_GPOUT_POL, value, 1) # memnumに意味なし(reflect_paramのフラグを立てない)

    @property
    def interrupt_line(self):
        _, value = self.get_info(acaplib2.ACL_INTR_LINE)
        return value
    @interrupt_line.setter
    def interrupt_line(self, value: int):
        '''Get or set the count interval of the number of input lines for one frame.'''
        _ = self.set_info(acaplib2.ACL_INTR_LINE, value)

    @property
    def cc_enable(self):
        _, value = self.get_info(acaplib2.ACL_EXP_EN)
        return value
    @cc_enable.setter
    def cc_enable(self, value: int):
        '''Get or set whether the exposure signal output is enabled or disabled.'''
        self.trigger_enable = value

    @property
    def trigger_enable(self):
        _, value = self.get_info(acaplib2.ACL_EXP_EN)
        return value
    @trigger_enable.setter
    def trigger_enable(self, value: int):
        '''Get or set whether the exposure signal output is enabled or disabled.'''
        _ = self.set_info(acaplib2.ACL_EXP_EN, value)

    @property
    def data_mask_lower(self):
        _, value = self.get_info(acaplib2.ACL_DATA_MASK_LOWER)
        return value
    @data_mask_lower.setter
    def data_mask_lower(self, value: int):
        '''Get or set the mask value of Camera Link port (A to D).'''
        _ = self.set_info(acaplib2.ACL_DATA_MASK_LOWER, value)

    @property
    def data_mask_upper(self):
        _, value = self.get_info(acaplib2.ACL_DATA_MASK_UPPER)
        return value
    @data_mask_upper.setter
    def data_mask_upper(self, value: int):
        '''Get or set the mask value of Camera Link port (E to H).'''
        _ = self.set_info(acaplib2.ACL_DATA_MASK_UPPER, value)

    @property
    def encoder_count(self):
        '''Get the relative count value when using relative count.'''
        _, count = self.get_info(acaplib2.ACL_ENC_RLT_COUNT)
        return count

    @property
    def encoder_all_count(self):
        '''Get the total count value when using relative count.'''
        _, count = self.get_info(acaplib2.ACL_ENC_RLT_ALL_COUNT)
        return count

    @property
    def encoder_agr_count(self):
        '''Get the number of matched pulses when using relative count.'''
        _, count = self.get_info(acaplib2.ACL_ENC_AGR_COUNT)
        return count

    @property
    def a_cw_ccw(self):
        '''Get the rotation direction of phase A.'''
        _, count = self.get_info(acaplib2.ACL_A_CW_CCW)
        return count

    @property
    def b_cw_ccw(self):
        '''Get the rotation direction of phase B.'''
        _, count = self.get_info(acaplib2.ACL_B_CW_CCW)
        return count

    @property
    def freq_a(self):
        '''Get the frequency of phase A.'''
        _, count = self.get_info(acaplib2.ACL_FREQ_A)
        return count

    @property
    def freq_b(self):
        '''Get the frequency of phase B.'''
        _, count = self.get_info(acaplib2.ACL_FREQ_B)
        return count

    @property
    def freq_z(self):
        '''Get the frequency of phase Z.'''
        _, count = self.get_info(acaplib2.ACL_FREQ_Z)
        return count

    @property
    def freq_d(self): # 2023.08.31 追加
        '''Get the frequency of phase D.'''
        _, count = self.get_info(acaplib2.ACL_FREQ_D)
        return count

    @property
    def freq_e(self): # 2023.08.31 追加
        '''Get the frequency of phase E.'''
        _, count = self.get_info(acaplib2.ACL_FREQ_E)
        return count

    @property
    def freq_f(self): # 2023.08.31 追加
        '''Get the frequency of phase F.'''
        _, count = self.get_info(acaplib2.ACL_FREQ_F)
        return count

    @property
    def freq_g(self): # 2023.08.31 追加
        '''Get the frequency of phase G.'''
        _, count = self.get_info(acaplib2.ACL_FREQ_G)
        return count

    @property
    def freq_h(self): # 2023.08.31 追加
        '''Get the frequency of phase H.'''
        _, count = self.get_info(acaplib2.ACL_FREQ_H)
        return count

    @property
    def chatter_separate(self):
        _, value = self.get_info(acaplib2.ACL_EXT_CHATTER_SEPARATE)
        return value
    @chatter_separate.setter
    def chatter_separate(self, value):
        '''Get or set the setting method of the external trigger detection disable time.'''
        _ = self.set_info(acaplib2.ACL_EXT_CHATTER_SEPARATE, value)

    @property
    def gpin_pin_sel(self):
        _, value = self.get_info(acaplib2.ACL_GPIN_PIN_SEL)
        return value
    @gpin_pin_sel.setter
    def gpin_pin_sel(self, value: int):
        '''Get or set the external trigger pins that are assigned as GPIN interrupt to the specified channel.'''
        _ = self.set_info(acaplib2.ACL_GPIN_PIN_SEL, value, 1) # 直接設定, reflect_paramの必要なし

    @property
    def sync_ch(self):
        _, value = self.get_info(acaplib2.ACL_SYNC_CH)
        return value
    @sync_ch.setter
    def sync_ch(self, value: int):
        '''Get or set which channel to synchronize the acquisition of the specified channel with.'''
        _ = self.set_info(acaplib2.ACL_SYNC_CH, value)

    @property
    def bayer_enable(self):
        _, value = self.get_info(acaplib2.ACL_BAYER_ENABLE)
        return value
    @bayer_enable.setter
    def bayer_enable(self, value: int):
        '''Get or set the Enable/Disable setting for the Bayer transform.
        value : int
            0 : Bayer disable
            1 : Reserved (Software bayer) 
            2 : Hardware bayer
        '''
        _ = self.set_info(acaplib2.ACL_BAYER_ENABLE, value, 1) # 直接設定, reflect_paramの必要なし

    @property
    def bayer_grid(self):
        _, value = self.get_info(acaplib2.ACL_BAYER_GRID)
        return value
    @bayer_grid.setter
    def bayer_grid(self, value: int):
        '''Get or set the pattern for the start position of the Bayer transform.
        0:BGGR
        1:RGGB
        2:GBRG
        3:GRBG
        '''
        _ = self.set_info(acaplib2.ACL_BAYER_GRID, value, 1) # 直接設定, reflect_paramの必要なし

    @property
    def bayer_lut_edit(self):
        _, value = self.get_info(acaplib2.ACL_BAYER_LUT_EDIT)
        return value
    @bayer_lut_edit.setter
    def bayer_lut_edit(self, value: int):
        '''Get or set the edit status of the BayerLUT.'''
        self.set_info(acaplib2.ACL_BAYER_LUT_EDIT, value, 1) # 直接設定, reflect_paramの必要なし

    @property
    def bayer_lut_data(self):
        data = []
        for i in range(1024):
            ret, value = self.get_info(acaplib2.ACL_BAYER_LUT_DATA, i)
            if ret != AcaPy.OK:
                return None
            data.append(value)
        return data
    @bayer_lut_data.setter
    def bayer_lut_data(self, lut_data_list):
        '''Reads or writes the BayerLUT table data of the specified channel.'''
        if lut_data_list is None:
            return
        for i in range(len(lut_data_list)):
            ret = self.set_info(acaplib2.ACL_BAYER_LUT_DATA, lut_data_list[i], i)
            if ret != AcaPy.OK:
                return

    @property
    def bayer_input_bit(self):
        _, value = self.get_info(acaplib2.ACL_BAYER_INPUT_BIT)
        return value
    @bayer_input_bit.setter
    def bayer_input_bit(self, value: int):
        '''Get or set the input bit width of a single pixel in a Bayer image.'''
        _ = self.set_info(acaplib2.ACL_BAYER_INPUT_BIT, value, 1) # 直接設定, reflect_paramの必要なし

    @property
    def bayer_output_bit(self):
        _, value = self.get_info(acaplib2.ACL_BAYER_OUTPUT_BIT)
        return value
    @bayer_output_bit.setter
    def bayer_output_bit(self, value: int):
        '''Get or set the bit width of a single pixel of the image after Bayer conversion.'''
        _ = self.set_info(acaplib2.ACL_BAYER_OUTPUT_BIT, value, 1) # 直接設定, reflect_paramの必要なし

    @property
    def power_supply(self):
        _, value = self.get_info(acaplib2.ACL_POWER_SUPPLY)
        return value
    @power_supply.setter
    def power_supply(self, value: int):
        '''Get or set the status(ON:1, OFF:0) of power supply to the camera.'''
        self.set_info(acaplib2.ACL_POWER_SUPPLY, value, 3000)

        if value == 1:
            # 電源をONにしたとき
            if self.__hHandle != acaplib2.INVALID_HANDLE_VALUE:
                #ボードがオープンされていて、電源をONにしたとき
                if self.camera_state == 1:
                    # カメラの接続が確認できたとき
                    self.__is_opened = True # ボードオープンフラグをTrueにする

    @property
    def power_state(self):
        _, value = self.get_info(acaplib2.ACL_POWER_STATE)
        return value
    @power_state.setter
    def power_state(self, value: int):
        '''Get or set the camera power supply error status.'''
        return self.set_info(acaplib2.ACL_POWER_STATE, value, 1) # 直接設定, reflect_paramの必要なし


    @property
    def strobe_pol(self):
        _, value = self.get_info(acaplib2.ACL_STROBE_POL)
        return value
    @strobe_pol.setter
    def strobe_pol(self, value: int):
        '''Get or set strobe signal polarity.'''
        self.set_info(acaplib2.ACL_STROBE_POL, value)

    @property
    def vertical_remap(self):
        _, value = self.get_info(acaplib2.ACL_VERTICAL_REMAP)
        return value
    @vertical_remap.setter
    def vertical_remap(self, value: int):
        '''Get or set the VERTICAL REMAP (Y direction special DMA) and DUAL LINE enable/disable setting.'''
        _ = self.set_info(acaplib2.ACL_VERTICAL_REMAP, value)

    @property
    def express_link(self):
        '''Get the link width negotiated for the PCI-Express bus.'''
        _, value = self.get_info(acaplib2.ACL_EXPRESS_LINK)
        return value

    @property
    def fpga_version(self):
        '''Get the current FPGA version.'''
        _, value = self.get_info(acaplib2.ACL_FPGA_VERSION)
        return value

    @property
    def lval_delay(self):
        _, value = self.get_info(acaplib2.ACL_LVAL_DELAY)
        return value
    @lval_delay.setter
    def lval_delay(self, value: int):
        '''Get or set the input direction for each tap.'''
        _ = self.set_info(acaplib2.ACL_LVAL_DELAY, value)

    @property
    def line_reverse(self):
        _, value = self.get_info(acaplib2.ACL_LINE_REVERSE)
        return value
    @line_reverse.setter
    def line_reverse(self, value: int):
        '''Get ot set whether or not to flip the line data left or right.'''
        _ = self.set_info(acaplib2.ACL_LINE_REVERSE, value)

    @property
    def camera_state(self):
        '''Get the connection status of the camera.'''
        _, value = self.get_info(acaplib2.ACL_CAMERA_STATE)
        return value

    @property
    def gpin_pol(self):
        '''Get the GPIN level as Bit information.'''
        _, value = self.get_info(acaplib2.ACL_GPIN_POL)
        return value

    @property
    def board_error(self):
        '''Get the board error information by Bit information.'''
        _, value = self.get_info(acaplib2.ACL_BOARD_ERROR)
        return value

    @board_error.setter
    def board_error(self, value: int):
        '''Clears the board error of the specified channel.'''
        self.set_info(acaplib2.ACL_BOARD_ERROR, value)

    @property
    def start_frame_no(self):
        _, value = self.get_info(acaplib2.ACL_START_FRAME_NO)
        return value
    @start_frame_no.setter
    def start_frame_no(self, value: int):
        '''Get ot set the number of frames to be input from the buffer at the start of acquisition.'''
        _ = self.set_info(acaplib2.ACL_START_FRAME_NO, value, 1) # reflect_param()不要のため

    @property
    def cancel_initialize(self):
        _, value = self.get_info(acaplib2.ACL_CANCEL_INITIALIZE)
        return value
    @cancel_initialize.setter
    def cancel_initialize(self, value: int):
        '''Get ot set whether or not to cancel initialization and internal buffer allocation.'''
        self.set_info(acaplib2.ACL_CANCEL_INITIALIZE, value, 1) # 直接設定

    @property
    def buffer_zero_fill(self):
        _, value = self.get_info(acaplib2.ACL_BUFFER_ZERO_FILL)
        return value
    @buffer_zero_fill.setter
    def buffer_zero_fill(self, value: int):
        '''Get or set whether to clear the buffer to zero'''
        _ = self.set_info(acaplib2.ACL_BUFFER_ZERO_FILL, value, 1) # 直接設定

    @property
    def cc_stop(self):
        _, value = self.get_info(acaplib2.ACL_CC_STOP)
        return value
    @cc_stop.setter
    def cc_stop(self, value: int):
        '''Get or set the output/stop of CC after the input is stopped.'''
        _ = self.set_info(acaplib2.ACL_CC_STOP, value, 1) # 直接設定

    @property
    def lvds_cclk_sel(self):
        _, value = self.get_info(acaplib2.ACL_LVDS_CCLK_SEL)
        return value
    @lvds_cclk_sel.setter
    def lvds_cclk_sel(self, value: int):
        '''Get or set the camera drive clock'''
        _ = self.set_info(acaplib2.ACL_LVDS_CCLK_SEL, value, 1) # 直接設定

    @property
    def lvds_phase_sel(self):
        _, value = self.get_info(acaplib2.ACL_LVDS_PHASE_SEL)
        return value
    @lvds_phase_sel.setter
    def lvds_phase_sel(self, value: int):
        '''Get or set the phase setting of the input sampling.'''
        _ = self.set_info(acaplib2.ACL_LVDS_PHASE_SEL, value, 1) # 直接設定

    @property
    def lvds_synclt_sel(self):
        _, value = self.get_info(acaplib2.ACL_LVDS_SYNCLT_SEL)
        return value
    @lvds_synclt_sel.setter
    def lvds_synclt_sel(self, value: int):
        '''Get or set the direction of the SYNCLT pin.'''
        _ = self.set_info(acaplib2.ACL_LVDS_SYNCLT_SEL, value, 1) # 直接設定

    @property
    def count_cc(self):
        '''Get the number of output of CC1/trigger packet.'''
        _, value = self.get_info(acaplib2.ACL_COUNT_CC)
        return value

    @property
    def count_fval(self):
        '''Get the number of times FVAL is input.'''
        _, value = self.get_info(acaplib2.ACL_COUNT_FVAL)
        return value

    @property
    def count_lval(self):
        '''Get the number of LVAL inputs.'''
        _, value = self.get_info(acaplib2.ACL_COUNT_LVAL)
        return value

    @property
    def count_exttrig(self):
        '''Get the number of EXTTRIG (external trigger) inputs.'''
        _, value = self.get_info(acaplib2.ACL_COUNT_EXTTRIG)
        return value

    @property
    def interval_exttrig_1(self):
        '''Get the time of the recognized external trigger interval (the latest count value).'''
        _, value = self.get_info(acaplib2.ACL_INTERVAL_EXTTRIG_1)
        return value

    @property
    def interval_exttrig_2(self):
        '''Get the time of the recognized external trigger interval (the second most recent count value).'''
        _, value = self.get_info(acaplib2.ACL_INTERVAL_EXTTRIG_2)
        return value

    @property
    def interval_exttrig_3(self):
        '''Get the time of the recognized external trigger interval (the third most recent count value).'''
        _, value = self.get_info(acaplib2.ACL_INTERVAL_EXTTRIG_3)
        return value

    @property
    def interval_exttrig_4(self):
        '''Get the time of the recognized external trigger interval (the fourth most recent count value).'''
        _, value = self.get_info(acaplib2.ACL_INTERVAL_EXTTRIG_4)
        return value

    @property
    def virtual_comport(self):
        '''Get the virtual COM port number.'''
        _, value = self.get_info(acaplib2.ACL_VIRTUAL_COMPORT)
        return value

    @property
    def pocl_lite_enable(self):
        _, value = self.get_info(acaplib2.ACL_POCL_LITE_ENABLE)
        return value
    @pocl_lite_enable.setter
    def pocl_lite_enable(self, value: int):
        '''Get or set the setting values for PoCL-Lite camera connection.'''
        _ = self.set_info(acaplib2.ACL_POCL_LITE_ENABLE, value)

    @property
    def cxp_link_speed(self):
        _, value = self.get_info(acaplib2.ACL_CXP_BITRATE)
        return value
    @cxp_link_speed.setter
    def cxp_link_speed(self, value: int):
        '''Get or set the bit rate to and from the CoaXPress camera.'''
        #self.set_info(acaplib2._ACL_CXP_LINK_SPEED, value)
        _ = self.set_info(acaplib2.ACL_CXP_BITRATE, value)

    @property
    def cxp_bdlink_timeout(self):  # 2023.08.31 追加
        _, value = self.get_info(acaplib2.ACL_CXP_BDLINK_TIMEOUT)
        return value
    @cxp_bdlink_timeout.setter
    def cxp_bdlink_timeout(self, value: int):
        '''Get or set the timeout period for CXP_BDLINK.'''
        #_ = self.set_info(acaplib2.ACL_CXP_BDLINK_TIMEOUT, value, 1) # 直接設定ではダメ
        _ = self.set_info(acaplib2.ACL_CXP_BDLINK_TIMEOUT, value)
        #self.reflect_param() # cxp_bdlink_timeoutとcxp_camlink_timeoutは強制的にreflect_paramを行う

    @property
    def cxp_bitrate(self):
        _, value = self.get_info(acaplib2.ACL_CXP_BITRATE)
        return value
    @cxp_bitrate.setter
    def cxp_bitrate(self, value: int):
        '''Get or set the bit rate to and from the CoaXPress camera.'''
        _ = self.set_info(acaplib2.ACL_CXP_BITRATE, value)

    @property
    def cxp_camlink_timeout(self):  # 2023.08.31 追加
        _, value = self.get_info(acaplib2.ACL_CXP_CAMLINK_TIMEOUT)
        return value
    @cxp_camlink_timeout.setter
    def cxp_camlink_timeout(self, value: int):
        '''Get or set the timeout period for CXP_CAMLINK.'''
        _ = self.set_info(acaplib2.ACL_CXP_CAMLINK_TIMEOUT, value)
        #self.reflect_param() # cxp_bdlink_timeoutとcxp_camlink_timeoutは強制的にreflect_paramを行う

    @property
    def rgb_swap_enable(self):
        _, value = self.get_info(acaplib2.ACL_RGB_SWAP_ENABLE)
        return value
    @rgb_swap_enable.setter
    def rgb_swap_enable(self, value: int):
        _ = self.set_info(acaplib2.ACL_RGB_SWAP_ENABLE, value)

    @property
    def freq_lval(self):
        '''Get the frequency of LVAL.'''
        _, value = self.get_info(acaplib2.ACL_FREQ_LVAL)
        return value

    @property
    def freq_fval(self):
        '''Get the frequency of FVAL.'''
        _, value = self.get_info(acaplib2.ACL_FREQ_FVAL)
        return value

    @property
    def freq_opt1(self):  # 2023.08.31 追加
        '''Get the frequency of OPT1.'''
        _, value = self.get_info(acaplib2.ACL_FREQ_OPT1)
        return value

    @property
    def freq_opt2(self):  # 2023.08.31 追加
        '''Get the frequency of OPT2.'''
        _, value = self.get_info(acaplib2.ACL_FREQ_OPT2)
        return value

    @property
    def freq_opt3(self):  # 2023.08.31 追加
        '''Get the frequency of OPT3.'''
        _, value = self.get_info(acaplib2.ACL_FREQ_OPT3)
        return value

    @property
    def freq_opt4(self):  # 2023.08.31 追加
        '''Get the frequency of OPT4.'''
        _, value = self.get_info(acaplib2.ACL_FREQ_OPT4)
        return value

    @property
    def freq_opt5(self):  # 2023.08.31 追加
        '''Get the frequency of OPT5.'''
        _, value = self.get_info(acaplib2.ACL_FREQ_OPT5)
        return value

    @property
    def freq_opt6(self):  # 2023.08.31 追加
        '''Get the frequency of OPT6.'''
        _, value = self.get_info(acaplib2.ACL_FREQ_OPT6)
        return value

    @property
    def freq_opt7(self):  # 2023.08.31 追加
        '''Get the frequency of OPT7.'''
        _, value = self.get_info(acaplib2.ACL_FREQ_OPT7)
        return value

    @property
    def freq_opt8(self):  # 2023.08.31 追加
        '''Get the frequency of OPT8.'''
        _, value = self.get_info(acaplib2.ACL_FREQ_OPT8)
        return value


    @property
    def freq_ttl1(self):
        '''Get the frequency of TTL1.'''
        _, value = self.get_info(acaplib2.ACL_FREQ_TTL1)
        return value

    @property
    def freq_ttl2(self):
        '''Get the frequency of TTL2.'''
        _, value = self.get_info(acaplib2.ACL_FREQ_TTL2)
        return value

    @property
    def freq_ttl3(self):  # 2023.08.31 追加
        '''Get the frequency of TTL3.'''
        _, value = self.get_info(acaplib2.ACL_FREQ_TTL3)
        return value

    @property
    def freq_ttl4(self):  # 2023.08.31 追加
        '''Get the frequency of TTL4.'''
        _, value = self.get_info(acaplib2.ACL_FREQ_TTL4)
        return value

    @property
    def freq_ttl5(self):  # 2023.08.31 追加
        '''Get the frequency of TTL5.'''
        _, value = self.get_info(acaplib2.ACL_FREQ_TTL5)
        return value

    @property
    def freq_ttl6(self):  # 2023.08.31 追加
        '''Get the frequency of TTL6.'''
        _, value = self.get_info(acaplib2.ACL_FREQ_TTL6)
        return value

    @property
    def freq_ttl7(self):  # 2023.08.31 追加
        '''Get the frequency of TTL7.'''
        _, value = self.get_info(acaplib2.ACL_FREQ_TTL7)
        return value

    @property
    def freq_ttl8(self):  # 2023.08.31 追加
        '''Get the frequency of TTL7.'''
        _, value = self.get_info(acaplib2.ACL_FREQ_TTL8)
        return value



    @property
    def fifo_full(self):
        '''Get the status of the FIFO on the frame grabber board.'''
        _, value = self.get_info(acaplib2.ACL_FIFO_FULL)
        return value

    @property
    def board_temp(self):
        '''Get the temperature of the frame grabber board(APX-3334 only). '''
        _, value = self.get_info(acaplib2.ACL_BOARD_TEMP)
        return value

    @property
    def fpga_temp(self):
        '''Get the temperature of the FPGA.'''
        _, value = self.get_info(acaplib2.ACL_FPGA_TEMP)
        return value

    @property
    def capture_flag(self):
        '''Gets the capture status (capturing(1) or stopped(0)).'''
        _, value = self.get_info(acaplib2.ACL_CAPTURE_FLAG)
        return value

    @property
    def narrow10bit_enable(self):
        _, value = self.get_info(acaplib2.ACL_NARROW10BIT_ENABLE)
        return value
    @narrow10bit_enable.setter
    def narrow10bit_enable(self, value):
        '''Get or set enable/disable for data stuffing transfer.'''
        _ = self.set_info(acaplib2.ACL_NARROW10BIT_ENABLE, value)  


    # Ver.7.2.3
    @property
    def infrared_enable(self):
        _, value = self.get_info(acaplib2.ACL_INFRARED_ENABLE)
        return value
    @infrared_enable.setter
    def infrared_enable(self, value: int):
        '''Get or set the enable/disable status of RGBI.'''
        _ = self.set_info(acaplib2.ACL_INFRARED_ENABLE, value)  

    # -------------------------------------------------------------------
    # Ver.1.0.2 (AcapLib2 Ver.8.0.0対応版)

    @property
    def serial_read_wait_time(self):
        return self.__serial_read_wait_time
    @serial_read_wait_time.setter
    def serial_read_wait_time(self, value):
        '''Get or set the time to wait for the completion of serial communication reception.'''
        self.__serial_read_wait_time = value

    @property
    def debug_print_enabled(self):
        return self.__debug_print
    @debug_print_enabled.setter
    def debug_print_enabled(self, value):
        '''Get or set the settings for displaying(True)/hiding(False) error information on the console screen.'''
        self.__debug_print = value

    @property
    def fan_rpm(self):
        '''Get fan speed(rpm)'''
        _, value = self.get_info(acaplib2.ACL_FAN_RPM)
        return value

    #【AcapLib2 Ver.7.3.1対応】
    @property
    def port_a_assign(self):
        _, value = self.get_info(acaplib2.ACL_PORT_A_ASSIGN) # ACL_PORT_A_ASSIGN
        return value
    @port_a_assign.setter
    def port_a_assign(self, value: int):
        '''Gets or sets the PortA assignment settings.'''
        _ = self.set_info(acaplib2.ACL_PORT_A_ASSIGN, value)  

    @property
    def port_b_assign(self):
        _, value = self.get_info(acaplib2.ACL_PORT_B_ASSIGN) # ACL_PORT_B_ASSIGN
        return value
    @port_b_assign.setter
    def port_b_assign(self, value: int):
        '''Gets or sets the PortB assignment settings.'''
        _ = self.set_info(acaplib2.ACL_PORT_B_ASSIGN, value)  

    @property
    def port_c_assign(self):
        _, value = self.get_info(acaplib2.ACL_PORT_C_ASSIGN) # ACL_PORT_C_ASSIGN
        return value
    @port_c_assign.setter
    def port_c_assign(self, value: int):
        '''Gets or sets the PortC assignment settings.'''
        _ = self.set_info(acaplib2.ACL_PORT_C_ASSIGN, value)  

    @property
    def port_d_assign(self):
        _, value = self.get_info(acaplib2.ACL_PORT_D_ASSIGN) # ACL_PORT_D_ASSIGN
        return value
    @port_d_assign.setter
    def port_d_assign(self, value: int):
        '''Gets or sets the PortD assignment settings.'''
        _ = self.set_info(acaplib2.ACL_PORT_D_ASSIGN, value)  

    @property
    def port_e_assign(self):
        _, value = self.get_info(acaplib2.ACL_PORT_E_ASSIGN) # ACL_PORT_E_ASSIGN
        return value
    @port_e_assign.setter
    def port_e_assign(self, value: int):
        '''Gets or sets the PortE assignment settings.'''
        _ = self.set_info(acaplib2.ACL_PORT_E_ASSIGN, value)  

    @property
    def port_f_assign(self):
        _, value = self.get_info(acaplib2.ACL_PORT_F_ASSIGN) # ACL_PORT_F_ASSIGN
        return value
    @port_f_assign.setter
    def port_f_assign(self, value: int):
        '''Gets or sets the PortF assignment settings.'''
        _ = self.set_info(acaplib2.ACL_PORT_F_ASSIGN, value)  

    @property
    def port_g_assign(self):
        _, value = self.get_info(acaplib2.ACL_PORT_G_ASSIGN) # ACL_PORT_G_ASSIGN
        return value
    @port_g_assign.setter
    def port_g_assign(self, value: int):
        '''Gets or sets the PortG assignment settings.'''
        _ = self.set_info(acaplib2.ACL_PORT_G_ASSIGN, value)  

    @property
    def port_h_assign(self):
        _, value = self.get_info(acaplib2.ACL_PORT_H_ASSIGN) # ACL_PORT_H_ASSIGN
        return value
    @port_h_assign.setter
    def port_h_assign(self, value: int):
        '''Gets or sets the PortH assignment settings.'''
        _ = self.set_info(acaplib2.ACL_PORT_H_ASSIGN, value)  

    @property
    def port_i_assign(self):
        _, value = self.get_info(acaplib2.ACL_PORT_I_ASSIGN) # ACL_PORT_I_ASSIGN
        return value
    @port_i_assign.setter
    def port_i_assign(self, value: int):
        '''Gets or sets the PortI assignment settings.'''
        _ = self.set_info(acaplib2.ACL_PORT_I_ASSIGN, value)  

    @property
    def port_j_assign(self):
        _, value = self.get_info(acaplib2.ACL_PORT_J_ASSIGN) # ACL_PORT_J_ASSIGN
        return value
    @port_j_assign.setter
    def port_j_assign(self, value: int):
        '''Gets or sets the PortJ assignment settings.'''
        _ = self.set_info(acaplib2.ACL_PORT_J_ASSIGN, value)  


    @property
    def data_mask_ex(self):
        _, value = self.get_info(acaplib2.ACL_DATA_MASK_EX)          # ACL_DATA_MASK_EX
        return value
    @data_mask_ex.setter
    def data_mask_ex(self, value: int):
        '''Gets or sets the input data mask (ACL_DATA_MASK_EX).'''
        _ = self.set_info(acaplib2.ACL_DATA_MASK_EX, value)  

    # AcapLib2 Ver.8.0.0 以降、本 ID は設定不要
    #@property
    #def acquisition_stop(self):
    #    return self.__acquisition_stop
    #@acquisition_stop.setter
    #def acquisition_stop(self, value : int):
    #    ret = self.set_info(acaplib2.ACL_ACQUISITION_STOP, value)
    #    if ret == acaplib2.ACL_RTN_OK:
    #        self.__acquisition_stop = value

    @property
    def cxp_acquisition_control(self):
        _, value = self.get_info(acaplib2.ACL_CXP_ACQUISITION_CONTROL)  # ACL_CXP_ACQUISITION_CONTROL
        return value
    @cxp_acquisition_control.setter
    def cxp_acquisition_control(self, value: int):
        '''Gets or sets the Acquisition Start/Stop or not(ACL_CXP_ACQUISITION_CONTROL).'''
        _ = self.set_info(acaplib2.ACL_CXP_ACQUISITION_CONTROL, value)

    @property
    def external_trigger_polarity(self):
        _, value = self.get_info(acaplib2.ACL_EXT_POL)  # ACL_EXT_POL
        return value
    @external_trigger_polarity.setter
    def external_trigger_polarity(self, value: int):
        '''Gets or sets the external trigger polarity (ACL_EXT_POL).'''
        _ = self.set_info(acaplib2.ACL_EXT_POL, value)

    @property
    def cxp_connection_num(self):
        _, value = self.get_info(acaplib2.ACL_CXP_CONNECTION_NUM)
        return value
    @cxp_connection_num.setter
    def cxp_connection_num(self, value: int):
        '''Gets or sets the number of connections (ACL_CXP_CONNECTION_NUM).'''
        _ = self.set_info(acaplib2.ACL_CXP_CONNECTION_NUM, value)  

    # -------------------------------------------------------------------
    # 2023.08.04 追加
    @property
    def tag(self):
        return self.__tag
    @tag.setter
    def tag(self, value):
        '''Gets or sets the generic property.'''
        self.__tag = value

    # -------------------------------------------------------------------
    # 2023.08.31 追加
    @property
    def external_trigger_chatter_separate(self):
        _, value = self.get_info(acaplib2.ACL_EXT_CHATTER_SEPARATE)  # ACL_EXT_CHATTER_SEPARATE
        return value
    @external_trigger_chatter_separate.setter
    def external_trigger_chatter_separate(self, value: int):
        '''Gets or sets the external trigger detection invalidation time(ACL_EXT_CHATTER_SEPARATE).'''
        _ = self.set_info(acaplib2.ACL_EXT_CHATTER_SEPARATE, value)

    
    @property
    def alarm_status(self):  # 2023.08.31 追加
        '''Get capture board alarm information.'''
        _, value = self.get_info(acaplib2.ACL_ALARM_STATUS)
        return value
    @alarm_status.setter
    def alarm_status(self, value: int):
        '''Resets the alarm information on the capture board.'''
        _ = self.set_info(acaplib2.ACL_ALARM_STATUS, value, 1) # 直接設定


    # -------------------------------------------------------------------
    # Ver.1.1.0 (AcapLib2 Ver.8.2.0対応版)
    #ACL_CXP_PHY_ERROR_COUNT         = 0x1A23	# PHY Error Count
    #ACL_FRAME_NO                    = 0x1A24	# キャプチャ済みフレーム番号
    #ACL_LINE_NO                     = 0x1A25	# キャプチャ済みライン番号

    @property
    def cxp_phy_error_count(self):  # 2023.11.20 追加
        '''Get PHY error count.'''
        _, value = self.get_info(acaplib2.ACL_CXP_PHY_ERROR_COUNT)
        return value

    @property
    def frame_no(self):  # 2023.11.20 追加
        '''Get Captured Frame Number.'''
        _, value = self.get_info(acaplib2.ACL_FRAME_NO)
        return value

    @property
    def line_no(self):  # 2023.11.20 追加
        '''Get Captured Line Number.'''
        _, value = self.get_info(acaplib2.ACL_LINE_NO)
        return value


    ##############################################################
    # Meathod
    ##############################################################
   
    @staticmethod
    def bgr2rgb(bgr_image: np.ndarray) -> np.ndarray:
        '''Converts the data sequence of a color image from BGR to RGB or RGB to BGR.

        Parameters
        ----------
        bgr_image : ndarray
            Color image with data sequence BGR

        Returns
        -------
        rgb_image : np.ndarray
            Color image with RGB data sequence
        '''
        return acaplib2.bgr2rgb(bgr_image)

    @staticmethod
    def get_boardInfo() -> Tuple[int, acaplib2.ACAPBOARDINFOEX]:
        '''Get the information of the connected board.

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error 
        board_info : acaplib2.ACAPBOARDINFOEX
            Board Information  
        '''
        return acaplib2.AcapGetBoardInfoEx()

    @staticmethod
    def get_enable_board_ch_list() -> List[Tuple[int, int, str, int]]:
        '''Get the available board list information.

        Returns
        -------
        board_ch_list : List[Tuple[int, int, str, int]
            board_id : int
                Board Number
            ch : int
                Channel Number
            board_name : int
                Board name
            serial_no : int
                Board serial no

        '''
        _, info = acaplib2.AcapGetBoardInfoEx()

        boardnum = info.nBoardNum
        if boardnum == 0:
            boardnum = 1 # Virtualを許容するため

        info_list = []
        for i in range(boardnum):
            for ch in range(info.boardIndex[i].nChannelNum):
                info_list.append((info.boardIndex[i].nBoardID, ch + 1, acaplib2.byte_decode(info.boardIndex[i].pBoardNam), info.boardIndex[i].nSerialNo))

        return info_list




    def get_info(self, value_id: int, mem_num: int=0) -> Tuple[int, int]:
        '''Get the setting value of the board by specifying the setting ID.

        Parameters
        ----------
        value_id : int
            ID of the value to set
        mem_num : int
            The meaning changes depending on the value_id.

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error 
        value : int
            Get value of ID
        '''
        try:
            ret, value = acaplib2.AcapGetInfo(self.__hHandle, self.__ch, value_id, mem_num)
        except OSError as ose:
            self._debug_print(f"AcapGetInfo Error ID: {value_id: #X}", str(ose))
            return 0, 0
        except Exception as ex:
            self._debug_print(f"AcapGetInfo Error ID: {value_id: #X}", str(ex))
            return 0, 0

        if ret != self.OK:
            value = 0
            #self._debug_print("[Not Implemented] get_info: value_id =",
            #acaplib2.get_error_name(value_id))
            self._debug_print(f"[Not Implemented ID={self.board_id} CH={self.ch}] get_info: value_id =", acaplib2.get_error_name(value_id))
            
            #error_info = self.get_last_error()
            #if (error_info.dwBoardErrorCode & acaplib2.ACL_3300_NOT_SUPPORT)
            #!= acaplib2.ACL_3300_NOT_SUPPORT:
            #    self._debug_print("[Not Implemented] get_info: value_id =",
            #    acaplib2.get_error_name(value_id))
            #else:
            #    pass
        return ret, value

    def set_info(self, value_id: int, value: int, mem_num: int=-1) -> int:
        '''Set the setting value of the board by specifying the setting ID.

        Parameters
        ----------
        value_id : int
            ID of the value to set.
        value : int
            Setting value of the board.
        mem_num : int
            The meaning changes depending on the value_id.

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error 
        '''

        #if self.capture_flag == 1:
        #    print("set_info のGrab中", self.capture_flag)
            #return

        try:
            ret, ret_value = acaplib2.AcapGetInfo(self.__hHandle, self.__ch, value_id, 0)
            #print("set_info のGrab中AcapGetInfo", ret)
        except OSError as ose:
            self._debug_print(f"AcapGetInfo Error ID: {value_id: #X}", str(ose))
            return 0
        except Exception as ex:
            self._debug_print(f"AcapGetInfo Error ID: {value_id: #X}", str(ex))
            return 0

        if value == ret_value:
            return ret

        # mem_numの値が負の場合は、reflect_paramを後でまとめて行う。
        # mem_numの値が0以上の場合は、reflect_paramをAcapSetInfo内で行う。
        if mem_num < 0:
            self.__reflect_param_flag = True
        
        try:
            ret = acaplib2.AcapSetInfo(self.__hHandle, self.__ch, value_id, mem_num, value)
        except OSError as ose:
            self._debug_print(f"AcapSetInfo Error ID: {value_id: #X}", str(ose))
            return 0
        except Exception as ex:
            self._debug_print(f"AcapSetInfo Error ID: {value_id: #X}", str(ex))
            return 0

        #print("set_info のGrab中AcapSetInfo", ret, self.capture_flag)
        if ret != self.OK:
            self.print_last_error()
        return ret

    #def refrect_param(self, wait_time : float = 3.0, force_execution : bool =
    #False) -> int:
    #    '''(未使用)旧バージョンの互換用'''
    #    return self.reflect_param(wait_time, force_execution)

    def reflect_param(self, force_execution: bool=False) -> int:
        '''Reflects the set values on the board.

        Parameters
        ----------
        force_execution : bool
            True:  Force execution.
            False: Execute based on internal flags. 

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error 
        '''

        if force_execution == False:
            # 設定変更をしていない場合は、設定の反映を行わない
            if self.__reflect_param_flag == False:
                return self.OK

        # リングバッファの確保
        if self.__create_ring_buffer_flag == True:
            self.create_ring_buffer() # 外部メモリの登録を行うとAcapReflectParamが必要になるので、AcapReflectParamより先に行う

        self.__reflect_param_flag = False

        ret = acaplib2.AcapReflectParam(self.__hHandle, self.__ch)

        return ret

    def _select_file(self, inifilename: str) -> int:
        '''Load the board configuration file (ini file).

        Parameters
        ----------
        inifilename : str
            Path of the board configuration file (ini file).
 
        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error 
        '''

        # バッファ確保を行わない
        #self.set_info(acaplib2.ACL_CANCEL_INITIALIZE, 1)
        #self.__reflect_param_flag = True # reflect_patamが必要

        ret = acaplib2.AcapSelectFile(self.__hHandle, self.__ch, inifilename)
        if ret != acaplib2.ACL_RTN_OK:
            self.print_last_error()
            return ret
        
        # 各種情報の取得(使用頻度の高い値をメンバ変数で持っておく)
        ret, self.__timeout = self.get_info(acaplib2.ACL_TIME_OUT)
        ret, self.__mem_num = self.get_info(acaplib2.ACL_MEM_NUM)

        #ret, self.__driver_name = self.get_info(acaplib2.ACL_DRIVER_NAME)
        #ret, self.__hw_protect = self.get_info(acaplib2.ACL_HW_PROTECT)

        # リングバッファの確保が必要（reflect_param()関数内で実行される）
        self.__create_ring_buffer_flag = True
        
        ret = self.reflect_param() # 外部バッファの登録を行うため、reflect_paramが必要
        if ret != self.OK:
            self.print_last_error()      

        # 設定値の反映
        #ret = self.reflect_param() # create_ring_buffer中で行われている

        return self.OK
        
    def load_inifile(self, inifilename: str) -> int:
        '''Load the board configuration file (ini file).

        Parameters
        ----------
        inifilename : str
            Path of the board configuration file (ini file).

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error 
        '''

        # カメラが接続されていなくてもiniファイルの読込は行う
        #if self.__is_opened is False:
        #    self._debug_print(f"[load_inifile error ID={self.board_id} CH={self.ch}] Capture board is not opened.")
        #    return 0

        ret = self._select_file(inifilename)

        return ret

    def save_inifile(self, inifilename: str) -> int:
        '''Save the board configuration file (ini file).

        Parameters
        ----------
        inifilename : str
            Path of the board configuration file (ini file).
        
        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error 
        '''

        ret = acaplib2.AcapSelectFile(self.__hHandle, self.__ch, inifilename, 1)
        if ret != acaplib2.ACL_RTN_OK:
            _ = self.print_last_error()
            return 0

        return ret

    def set_power_supply(self, value: int, wait_time: int=6000) -> int:
        '''Controls the power supply to the camera

        Parameters
        ----------
        value : int
            Power OFF (0)
            Power ON  (1)
        wait_time : int
            This is the time to wait after changing the power supply to the camera until the camera clock is checked.          
        
        Returns
        -------
        ret : int
            Error information
        '''
        if wait_time < 100:
            wait_time = 100

        return self.set_info(acaplib2.ACL_POWER_SUPPLY, value, wait_time)

    def _frame_end_polling(self, input_num: int=0):
        '''FrameEndのポーリング
        AcaPyのFrameEndのコールバック用

        Parameters
        ----------
        input_num : int
            Set the input method for the image.(Grabの指定枚数)
        
        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error 
        '''

        # Snap(input_num == 1)のときは、このポーリングを呼んでいない

        ret = 1 # while self.__is_grab:の部分で、self.__is_grab = Falseとなり、read_framesが呼ばれない事があるので、必ず１にする

        if input_num >= 0:
            # 指定枚取込の場合
            if self.__frame_end_callback is not None:

                while self.__is_grab:
                #while self.capture_flag:
                    #ret, frames, count, total_frame_count =
                    #self.read_frames_old2(self.__frame_copy_flag) #
                    #現在のフレーム番号を取得
                    ret, frames, count, total_frame_count = self.read_frames(self.__frame_copy_flag) # 現在のフレーム番号を取得
                    if (ret != 0) and (total_frame_count != 0):
                        self._callback_handler(self.__frame_end_callback, self, frames, count, total_frame_count, ret)
                  
                # 最後の残フレームを確認
                if ret != 0:
                    ret, frames, count, total_frame_count = self.read_frames(self.__frame_copy_flag, False) # 現在のフレーム番号を取得
                    
                    if (ret != 0) and (total_frame_count != 0):
                        self._callback_handler(self.__frame_end_callback, self, frames, count, total_frame_count, ret)
                
            ## GrabEndコールバック
            #if self.__grab_end_callback is not None:
            #    self._callback_handler(self.__grab_end_callback, self)

    def grab_start(self, input_num : int = 0) -> int:
        '''Start image input.

        Parameters
        ----------
        input_num : int
            Set the input method for the image.
        
        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error 
        '''

        #if len(self.__images) == 0:
        #    self.create_ring_buffer()

        if self.__is_opened is False:  
            self._debug_print(f"[grab_start error ID={self.board_id} CH={self.ch}] Capture board is not opened.")
            return 0

        if self.__reflect_param_flag == True:
            self.reflect_param()

        #self.__input_num = input_num
        self.__last_frame_no = 0

        if self.capture_flag == 1:
            ret = self.grab_abort()
            if ret == 0:
                return AcaPy.ERROR

        self.__input_num = input_num
        ret = acaplib2.AcapGrabStart(self.__hHandle, self.__ch, input_num)
        if ret != AcaPy.OK:
            #AcapGrabStartに失敗した場合
            err = self.print_last_error()

        # 1度でもgrab_startを行ったらTrue(プログラム起動時のframe_noが残っているのを回避)
        self.__have_started_grab = True # AcapGrabStartを１回でも実行した(frame_noがリセットされた)

        self.__is_grab = True

        # コールバック関数が登録されているかどうかは、_frame_end_polling内で確認
        self.__thread_polling = threading.Thread(target=self._frame_end_polling, 
            args=(input_num,),
            daemon = True)
        self.__thread_polling.start()

        return ret

    def grab_stop(self) -> int:
        '''Stop image input.

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error 
        '''

        if self.__is_opened is False:
            self._debug_print(f"[grab_stop error ID={self.board_id} CH={self.ch}] Capture board is not opened.")
            return 0

        #Snapでないとき、AcapGrabStopより先にフラグを変えておく
        if (self.__input_num == 0):
            # 指定枚でないとき、AcapGrabStopより先にフラグを変えておく
            self.__is_grab = False
            # ↑の値がスレッドに反映されるまで、時間が必要 -> スレッドのjoinで終了待ちを入れた
            if self.__thread_polling is not None:
                # ポーリングスレッド終了待ち
                self.__thread_polling.join(self.timeout)
                self.__thread_polling = None

        ret = acaplib2.AcapGrabStop(self.__hHandle, self.__ch)
        
        self.__is_grab = False

        abort_flag = False

        if ret == AcaPy.OK:

            if self.__thread_polling is not None:
                # ポーリングスレッド終了待ち
                if self.__thread_polling.is_alive() is True:
                    self.__thread_polling.join(self.timeout)
                self.__thread_polling = None

        #if ret != AcaPy.OK:
        else:
            #AcapGrabStopに失敗した場合
            err = self.print_last_error()

            self.grab_abort() # 追加
            abort_flag = True

            if (err.dwBoardErrorCode & 0xFF) == 0x08:
                #TimeOutコールバック
                th_timeout = threading.Thread(target=self._callback_handler, 
                    args=(self.__timeout_callback, self),
                    daemon = True)
                th_timeout.start()
            
        # GrabEndコールバック
        if abort_flag is False: # abortしたときは、grab_abortからGrabEndを呼ぶ
            if self.__grab_end_callback is not None:
                #self._callback_handler(self.__grab_end_callback, self)
                th_grab_end = threading.Thread(target=self._callback_handler, 
                    args=(self.__grab_end_callback, self),
                    daemon = True)
                th_grab_end.start()

        return ret

    def grab_abort(self) -> int:
        '''Abort image input.

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error
        '''

        if self.__is_opened is False:
            self._debug_print(f"[grab_abort error ID={self.board_id} CH={self.ch}] Capture board is not opened.")
            return 0

        if (self.__input_num == 0):
            # 指定枚でないとき、AcapGrabAbortより先にフラグを変えておく
            self.__is_grab = False
            # ↑の値がスレッドに反映されるまで、時間が必要 -> スレッドのjoinで終了待ちを入れた

            if self.__thread_polling is not None:
                # ポーリングスレッド終了待ち
                self.__thread_polling.join(self.timeout)
                self.__thread_polling = None

        ret = acaplib2.AcapGrabAbort(self.__hHandle, self.__ch)

        self.__is_grab = False
        if self.__thread_polling is not None:
            # ポーリングスレッド終了待ち
            if self.__thread_polling.is_alive() is True:
                self.__thread_polling.join(self.timeout)
                self.__thread_polling = None

        ## AcapGrabAbortより先にフラグを変えておく
        #self.__is_grab = False

        #ret = acaplib2.AcapGrabAbort(self.__hHandle, self.__ch)

        ## __is_grabの値がスレッドに反映されるまで、時間が必要 -> スレッドのjoinで終了待ちを入れた
        #if self.__thread_polling is not None:
        #    # ポーリングスレッド終了待ち
        #    self.__thread_polling.join(self.timeout)
        #    self.__thread_polling = None

        if ret != AcaPy.OK:
            #AcapGrabAbortに失敗した場合
            err = self.print_last_error()
            if (err.dwBoardErrorCode & 0xFF) == 0x08:
                self._callback_handler(self.__timeout_callback, self)   # TimeOutコールバック

        # GrabEndコールバック
        if self.__grab_end_callback is not None:
            #self._callback_handler(self.__grab_end_callback, self)
            th = threading.Thread(target=self._callback_handler, 
                args=(self.__grab_end_callback, self),
                daemon = True)
            th.start()

        return ret

    def wait_grab_start(self, timeout : int = -1) -> int:
        '''Wait for Grab to start.

        Parameters
        ----------
        timeout : int
            Timeout period(mSec)
            When 'timeout' < 0, the timeout time in the ini file setting is used.

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error
        '''

        if timeout < 0:
            timeout = self.__timeout

        return acaplib2.AcapWaitEvent(self.__hHandle, self.__ch, acaplib2.ACL_INT_GRABSTART, timeout)

    def wait_frame_changed(self, timeout : int = -1) -> Tuple[int, int, int]:
        '''Wait for the completion of frame image input.

        Parameters
        ----------
        timeout : int
            Timeout period(mSec)
            When 'timeout' < 0, the timeout time in the ini file setting is used.

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error
        frane_num : int
            Number of frames acquired
        index : int
            Current memory index number(1, 2, 3・・・)

        '''
        # 最初はFrameEndで待つが、待てていないときは、ポーリングで切り替わりを待つ

        if timeout < 0:
            timeout = self.__timeout

        # 現在、取得が完了しているフレーム枚数
        #_, old_frame_no, _, _ = self.get_frame_no()
        ret, old_frame_no, _, index = self.get_frame_no()

        if ((self.__input_num != 0) and (self.__input_num == old_frame_no)) or (self.__is_grab is False):
            # すでに撮影が終了しているので、何もしないで返す
            return AcaPy.OK, old_frame_no, index

        #ret = acaplib2.AcapWaitEvent(self.__hHandle, self.__ch,
        #acaplib2.ACL_INT_FRAMEEND, timeout)
        #if ret != AcaPy.OK:
        #    #AcapWaitEventに失敗した場合
        #    print("AcapWaitEventに失敗")
        #    self.print_last_error()

        ret_wait_frame_end = self.wait_frame_end()
        
        ret, new_frame_no, _, index = self.get_frame_no()

        if old_frame_no == new_frame_no:
            for i in range(1000): # 最大1000回待つ
                time.sleep(0.0001)
                ret, new_frame_no, _, index = self.get_frame_no()
                #print(f"************* wait_frame_changed retryTimes={i+1}, old_frame_no={old_frame_no} new_frame_no={new_frame_no}")
                if old_frame_no != new_frame_no:
                    #print(f"************* wait_frame_changed retryTimes={i+1}
                    #old_frame_no={old_frame_no} new_frame_no={new_frame_no}")
                    break
                if self.__is_grab is False:
                    break # スレッド処理のため、値の反映が遅れる場合があるため、ここでも確認する。
        else:
            #print(f"************* wait_frame_changed
            #old_frame_no={old_frame_no} new_frame_no={new_frame_no}")
            pass

        return ret, new_frame_no, index

    def wait_frame_end(self, timeout : int = -1) -> int:
        '''Wait for the completion of frame image input.

        Parameters
        ----------
        timeout : int
            Timeout period(mSec)
            When 'timeout' < 0, the timeout time in the ini file setting is used.

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error
        '''

        #if self.capture_flag == 0:
        if self.__is_grab is False:
            return AcaPy.OK # Grab終了後のため、OKとする

        if timeout < 0:
            timeout = self.__timeout

        if self.__is_grab is True:
            ret = acaplib2.AcapWaitEvent(self.__hHandle, self.__ch, acaplib2.ACL_INT_FRAMEEND, timeout)
            if ret != AcaPy.OK:
                #AcapWaitEventに失敗した場合（タイムアウトなど）
                self.print_last_error()
        else:
            #return AcaPy.ERROR
            return AcaPy.OK # Grab終了後のため、OKとする

        return ret

    def wait_grab_end(self, timeout : int = -1) -> int:
        '''Wait for the image input to stop.

        Parameters
        ----------
        timeout : int
            Timeout period(mSec)
            When 'timeout' < 0, the timeout time in the ini file setting is used.

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error
        '''

        if self.capture_flag == 0: # 遅れてきたコールバックも含めてGrabが完了しているとき
            return 1
        elif self.__is_grab == False:
            # print("********************* コールバックのお釣り **********************")
            pass

        if timeout < 0:
            timeout = self.__timeout
            #if self.__input_num != 0:
            #    timeout = self.__timeout * self.__input_num

        ret = acaplib2.AcapWaitEvent(self.__hHandle, self.__ch, acaplib2.ACL_INT_GRABEND, timeout)
        if ret != AcaPy.OK:
            #AcapWaitEventに失敗した場合
            self.print_last_error()

        self.__is_grab = False

        return ret

    def wait_gpin(self, timeout : int = -1) -> int:
        '''Wait for gpin.

        Parameters
        ----------
        timeout : int
            Timeout period(mSec)
            When 'timeout' < 0, the timeout time in the ini file setting is used.

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error
        '''

        if timeout < 0:
            timeout = self.__timeout

        return acaplib2.AcapWaitEvent(self.__hHandle, self.__ch, acaplib2.ACL_INT_GPIN, timeout)

    def get_frame_no(self) -> Tuple[int, int, int , int]:
        '''Get the current frame number, line number, and memory index number.

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error
        frame_no : int
            Current frame number
        line : int
            Current line number
        index : int
            Current memory index number(1, 2, 3・・・)
        '''

        if self.__have_started_grab == False: # AcapLib2側でカウント値がリセットされないため。暫定対応
            return 1, 0, 0, 0

        return acaplib2.AcapGetFrameNo(self.__hHandle, self.__ch)
    
    def read(self, copy : bool = False, wait_frame : bool = True) -> Tuple[int, Union[np.ndarray, None], int, int]:
        '''Get the frame image currently being input during Grab.

        Parameters
        ----------
        copy : bool
            Specifies whether or not to copy and retrieve image data.
            True : Copy  
            False :Not copy 
        wait_frame : bool
            Specifies whether to wait for the frame input to complete.
            True : Wait  
            False :Don't wait           
        
        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error
        frame : np.ndarray
            Frame image
        frame_no : int
            Current frame number
        line : int
            Number of lines that have been entered
        '''

        if self.__have_started_grab == False:
            # まだ、grab_startを１回も行っていない
            return self.ERROR, None, 0, 0

        if wait_frame == True:
            #ret = self.wait_frame_end() # フレームの入力完了を待つ
            ret, _, _ = self.wait_frame_changed() # フレームの入力完了を待つ
            if ret != self.OK: # タイムアウトエラー
                self._debug_print(f"[Error ID={self.board_id} CH={self.ch}] wait_frame_end: Time out")
                return ret, None, 0, 0

        # 現在のフレーム番号の取得
        ret, frame_no, line, index = self.get_frame_no()
        if ret != self.OK:
            return ret, None, 0, 0

        frame = self.__images[index - 1] # 画像データ(ndarray)

        if copy == True:
            frame = frame.copy()

        return ret, frame, frame_no, line

    def read_frames(self, copy : bool = False, wait_frame : bool = True) -> Tuple[int, Union[List[np.ndarray], None], int, int]:
        
        '''
        Get the frame image from the previous frame image to the current frame image during Grab.

        Parameters
        ----------
        copy : bool
            Specifies whether or not to copy and retrieve image data.
            True : Copy  
            False :Not copy 
        wait_frame : bool
            Specifies whether to wait for the frame input to complete.
            True : Wait  
            False :Don't wait    

        Returns
        ----------
        ret : int
            Error information(success(1), Failure(0, Time out), Frame overwritten(< 0))
        frames : List[np.ndarray]
            Array of frame images from the previous frame image to the current frame image.
        count : int
            Number of frame images acquired.
        frame_no : int
            Frame number where the current input was completed.
        '''

        last_last_frame_no = self.__last_frame_no

        # 現在のフレーム番号の取得
        ret, frame_no, _, index = self.get_frame_no()
        #print(f"read_frames_1:ret={ret} frame_no={frame_no} index={index}")

        if wait_frame is True:
            if frame_no == last_last_frame_no:
                ret, frame_no, index = self.wait_frame_changed()
        else:
            if frame_no == last_last_frame_no:
                return self.ERROR, None, 0, 0

        self.__last_frame_no = frame_no # self.__last_frame_noを別スレッドで使うため、即代入
        count = frame_no - last_last_frame_no

        if count >= self.__mem_num: # 前回のフレーム番号との差が mem_num と同じときも上書き発生とする。
            if self.__input_num != self.__mem_num: #MEM_NUMとGrabの取込枚数が同じときは、上書きは発生しない
                ret = self.__mem_num - count - 1 # 不足した枚数を負で返す、１フレーム分追加
                if self.__overwrite_callback is not None:
                    # オーバーライトのコールバックが登録されているときは、コールバックを投げる
                    self._callback_handler(self.__overwrite_callback, self, count, frame_no, -ret)
                else:
                    # コールバックが登録されていないときは、ワーニングを表示する
                    self._debug_print(f"[Warning ID={self.__board_id} CH={self.__ch}] read_frames: {-ret} frames overwritten")
        else:
            ret = self.OK

        if count <= 0:
            return self.ERROR, None, 0, 0

        frames = []

        # 前回のフレーム番号の次から、現在のフレーム番号までを処理する
        index -= 1 # 1始まりから０始まりに修正

        for fno in range(last_last_frame_no + 1, frame_no + 1):
            index_no = (index + fno - frame_no + self.__mem_num) % self.__mem_num
            image = self.__images[index_no] # 画像データ(ndarray)
            if copy == True:
                frames.append(image.copy())
            else:
                frames.append(image)

        return ret, frames, count, frame_no   
    
    def create_ring_buffer(self):
        #リングバッファの確保（mem_numの設定時、サイズ変更時に同時に行う）
        '''Allocate ring buffers.
        Executed when changing mem_num or image size settings.

        Returns
        -------
        int
            Error information
            1 : OK
            0 : Error
        '''

        # AcapSetBufferAddress()関数での待ち時間をなくす
        #old_cxp_bdlink_timeout = self.cxp_bdlink_timeout
        #old_cxp_camlink_timeout = self.cxp_camlink_timeout
        #self.cxp_bdlink_timeout = 0
        #self.cxp_camlink_timeout = 0

        # バッファを解除
        ret = acaplib2.AcapSetBufferAddress(
            self.__hHandle, 
            self.__ch, 
            acaplib2.ACL_IMAGE_PTR,
            0,
            None)

        # 待ち時間を元に戻す
        #self.cxp_bdlink_timeout = old_cxp_bdlink_timeout
        #self.cxp_camlink_timeout = old_cxp_camlink_timeout

        #self.__reflect_param_flag = True

        if ret != self.OK:
            self.print_last_error()

        self.__images = acaplib2.CreateRingBuf(self.__hHandle, self.__ch, self.__mem_num)

        for i in range(self.__mem_num):

            # 外部バッファの登録（登録後、reflect paramが必要）
            ret = acaplib2.AcapSetBufferAddress(
                self.__hHandle, 
                self.__ch, 
                acaplib2.ACL_IMAGE_PTR, 
                -(i + 1), 
                acaplib2.GetImageBufPointer(self.__images[i]))
            if ret != self.OK:
                # 最初の１回目だけLastErrorを表示する
                if i == 0:
                    self.print_last_error()
                # 毎回エラーを表示する
                self._debug_print(f"[Error ID={self.board_id} CH={self.ch}] AcapSetBufferAddress")
                
        #ret = self.reflect_param()
        #if ret != self.OK:
        #    self.print_last_error()

        self.__reflect_param_flag = True
        self.__create_ring_buffer_flag = False

        return ret

    def get_image_data(self, index : int) -> Union[np.ndarray, None]:
        '''
        Get the data of the ring buffer by specifying the index number(0, 1, 2...).

        Parameters
        ----------
        index : int
            Index number of the ring buffer(0, 1, 2...)

        Returns
        ----------
        image : np.ndarray
            data of the ring buffer
        '''

        if index >= len(self.__images) or index < 0:
            return None

        return self.__images[index]

    def snap(self, copy : bool = False) -> Tuple[int, Union[np.ndarray, None]]:
        '''Get a single image.(For continuous acquisition, use Grab.)

        Parameters
        ----------
        copy : bool
            Specifies whether or not to copy and retrieve image data.
            True : Copy  
            False :Not copy 

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error
        frame : np.ndarray
            Frame image
        '''

        if self.capture_flag == 1:
            # すでにGrab中の場合
            ret = self.grab_abort()
            if ret == 0:
                return AcaPy.ERROR, None

        # 入力開始
        if self.grab_start(1) != AcaPy.OK:
            return AcaPy.ERROR, None

        # 入力停止
        ret = self.grab_stop() # Grab中のときは、Grab中のフレームのFrameEndを待つ
        if ret != AcaPy.OK:
            self.print_last_error()
            return ret, None

        # フレーム画像の読込
        ret, image, _, _ = self.read(copy, False) # False: grab_stopでFrameEndを待っているため、ここでは待たない
        if ret != AcaPy.OK:
            self.print_last_error()
            self.grab_stop() # Grab中のときは、Grab中のフレームのFrameEndを待つ
            return AcaPy.ERROR, None

        #if self.__frame_end_callback is not None:
        #    #self._callback_handler(self.__frame_end_callback, self, [image],
        #    1, 1, ret)
        #    subthread = threading.Thread(
        #        target=self._callback_handler,
        #        args=(self.__frame_end_callback, self, [image], 1, 1, ret))
        #    subthread.start()

        # 現在のフレーム番号の取得
        return ret, image

    def count_reset(self) -> int:
        '''Reset all counters.

        Returns
        -------
        int
            Error information
            1 : OK
            0 : Error
        '''
        return self.set_info(acaplib2.ACL_COUNT_RESET, 0, 1)

    def cxp_link_reset(self) -> int:
        '''Establishes the camera connection (reinitialization) for the connected camera.

        Returns
        -------
        int
            Error information
            1 : OK
            0 : Error
        '''
        return self.set_info(acaplib2.ACL_CXP_LINK_RESET, 0)
 
    def opt_link_reset(self) -> int:
        '''This command resets (reinitializes) the Opt-C:Link board.

        Returns
        -------
        int
            Error information
            1 : OK
            0 : Error
        '''
        return self.set_info(acaplib2.ACL_OPT_LINK_RESET, 0, 0) 

    def is_read_only_property(self, attr):
        '''read onlyかどうかを調べる'''
        v = getattr(self, attr)
        try:
            setattr(self, attr,v)
            return False
        except AttributeError:
            return True

    def get_acapy_properties_text(self) -> str:
        '''Get a list of property values set in the acapy class.

        Returns
        -------
        str
            Text of the list of property values set in the acapy class.
        '''

        old_bebug_print = self.__debug_print
        self.__debug_print = False # IDの取得（プロパティ値の取得）部分で、IDが無い時にエラーを表示してしまうのを抑制

        properties_text = ""

        properties = dir(self)

        pare = r'\'.*\''  # 'に囲まれている任意の文字

        for p in properties:
            if p == "OK" or p == "ERROR": # この２つだけ除外しきれないので、手作業で除外
                continue 

            pro = getattr(self, p) # 文字列からメソッド、プロパティを生成
            if callable(pro) is False: # callable: 関数かどうか
                if p.startswith("_") is False:

                    ## ReadOnlyかどうか？ この情報を取得すると画像が表示できなくなるため、コメントアウト
                    #ro = self.is_read_only_property(p) # read onlyかどうか？調べる -> 処理が遅いのでなし
                    #rw_str = "RW  "
                    rw_str = ""
                    #if ro == True:
                    #    rw_str = "RO  "

                    key_len = len(p)
                    tab_count = key_len // 8
                    tab_count = 4 - tab_count
                    if tab_count < 1:
                        tab_count = 1
                    type_find = re.findall(pare, str(type(pro))) # ' ' で囲まれている部分を取得（リストで取得される）
                    if len(type_find) > 0:
                        type_find = type_find[0]
                    if 'str' in type_find:
                        pro = "'" + pro + "'"
                    properties_text += p + "\t" * tab_count + str(type_find[1:-1]) + "\t" + rw_str + str(pro) + "\n"
          
        self.__debug_print = old_bebug_print
                    
        return properties_text

    def _debug_print(self, str1, str2 = "", str3 = "", str4 = "", str5 = ""):
        if self.__debug_print == False:
            return
        print(str1, str2, str3, str4, str5)

    def get_last_error(self, error_reset : bool = False) -> acaplib2.ACAPERRORINFO:
        '''Get information about the last error that occurred.

        Parameters
        ----------
        error_reset : bool
            When True, resets the stored value.

        Returns
        -------
        error_info : acaplib2.ACAPERRORINFO
            error-information structure

        '''
        return acaplib2.AcapGetLastErrorCode(error_reset)

    #def print_last_error(self) -> acaplib2.ACAPERRORINFO:
    #    '''Print the last error information that occurred in the terminal.

    #    Returns
    #    -------
    #    error_info : acaplib2.ACAPERRORINFO
    #        error-information structure
    #    '''
    #    error_info = self.get_last_error()

    #    extend_error = str(acaplib2.get_error_name(error_info.dwExtendErrorCode))
    #    if extend_error == "NO_ERROR":
    #        extend_error = ""

    #    msg = f"------------- Error ID={self.board_id} CH={self.ch} ---------------\n" + \
    #        "Common\t:" + str(acaplib2.get_error_name(error_info.dwCommonErrorCode)) + "\n" + \
    #        "Board\t:" + str(acaplib2.get_error_name(error_info.dwBoardErrorCode & 0x00FF)) + "\n" + \
    #        "Extend\t:" + extend_error + "\n"

    #    if self.tag != "":
    #        msg += "Tag\t:" + str(self.tag) + "\n"

    #    msg += "---------------------------------------------"

    #    #self._debug_print(
    #    #    f"------------- Error ID={self.board_id} CH={self.ch}
    #    #    ---------------\n" +
    #    #    "Common\t:"+
    #    #    str(acaplib2.get_error_name(error_info.dwCommonErrorCode)) + "\n"
    #    #    +
    #    #    "Board\t:" +
    #    #    str(acaplib2.get_error_name(error_info.dwBoardErrorCode & 0x00FF))
    #    #    + "\n" +
    #    #    "Extend\t:" + extend_error + "\n" +
    #    #    "---------------------------------------------"
    #    #    )
    #    self._debug_print(msg)

    #    return error_info

    def print_last_error(self) -> acaplib2.ACAPERRORINFOEX:
        '''Print the last error information that occurred in the terminal.

        Returns
        -------
        error_info : acaplib2.ACAPERRORINFO
            error-information structure
        '''
        error_info_ex = self.get_last_error_ex()

        extend_error = str(acaplib2.get_error_name(error_info_ex.dwExtendErrorCode))
        if extend_error == "NO_ERROR":
            extend_error = ""

        msg = f"------------- Error ID={self.board_id} CH={self.ch} ---------------\n" + \
            "Common\t:" + str(acaplib2.get_error_name(error_info_ex.dwCommonErrorCode)) + "\n" + \
            "Board\t:" + str(acaplib2.get_error_name(error_info_ex.dwBoardErrorCode & 0x00FF)) + "\n" + \
            "Extend\t:" + extend_error + "\n"

        if self.tag != "":
            msg += "Tag\t:" + str(self.tag) + "\n"

        msg += "---------------------------------------------"

        self._debug_print(msg)

        return error_info_ex

    def _set_event(self, event_id : int, event_enable : int) -> int:
        '''Registering interrupt events

        Parameters
        ----------
        event_id : int
            Specify the interrupt to register event notification.
            acaplib2.ACL_INT_GRABSTART
            acaplib2.ACL_INT_FRAMEEND
            acaplib2.ACL_INT_GRABEND
            acaplib2.ACL_INT_GPIN
        event_enable : int
            0:Exclude
            1:Registration

        Returns
        -------
        ret : int
            Error information
        '''
        ret = acaplib2.AcapSetEvent(self.__hHandle, self.__ch, 
                event_id, event_enable)
        if ret != self.OK:
            self.print_last_error()
        return ret

    def set_shutter_trigger(self, exp_cycle : int, exposure : int, exp_pol : int, exp_unit : int, cc_sel : int) -> int:
        '''Setting the area sensor shutter trigger

        Parameters
        ----------
        exp_cycle : int
            CC output cycle (1uSec unit)
        exposure : int
            CC Output width (1uSec unit)
        exp_pol : int
            Output logic
            0:negative logic
            1:positive logic
        exp_unit : int
            Non support
        cc_sel : int
            Number of the CC signal to be output

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error
        '''
        ret = acaplib2.AcapSetShutterTrigger(self.__hHandle, self.__ch, 
                exp_cycle, exposure, exp_pol, exp_unit, cc_sel)
        if ret != self.OK:
            self.print_last_error()
        return ret

    def get_shutter_trigger(self) -> Tuple[int, int, int, int, int, int]:
        '''Get the shutter trigger setting.

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error
        exp_cycle : int
            CC output cycle (1uSec unit)
        exposure : int
            CC Output width (1uSec unit)
        exp_pol : int
            Output logic
            0:negative logic
            1:positive logic
        exp_unit : int
            Non support
        cc_sel : int
            Number of the CC signal to be output
        '''
        ret = acaplib2.AcapGetShutterTrigger(self.__hHandle, self.__ch)
        if ret[0] != self.OK:
            self.print_last_error()
        return ret

    def set_line_trigger(self, exp_cycle : int, exposure : int, exp_pol : int) -> int:
        '''Set up the line trigger

        Parameters
        ----------
        exp_cycle : int
            CC output cycle (1uSec unit)
        exposure : int
            CC Output width (1uSec unit)
        exp_pol : int
            Output logic
            0:negative logic
            1:positive logic

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error
        '''
        ret = acaplib2.AcapSetLineTrigger(self.__hHandle, self.__ch, exp_cycle, exposure, exp_pol)
        if ret != self.OK:
            self.print_last_error()
        return ret

    def get_line_trigger(self) -> Tuple[int, int, int, int]:
        '''Get line trigger setting

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error
        exp_cycle : int
            CC output cycle (1uSec unit)
        exposure : int
            CC Output width (1uSec unit)
        exp_pol : int
            Output logic
            0:negative logic
            1:positive logic
        '''
        # -> exp_cycle, exposure, exp_pol, exp_unit, cc_sel
        ret = acaplib2.AcapGetLineTrigger(self.__hHandle, self.__ch)
        if ret[0] != self.OK:
            self.print_last_error()
        return ret

    def set_external_trigger(self, exp_trg_en : int, ext_trg_mode : int, ext_trg_dly : int, ext_trg_chatter : int, timeout : int) -> int:
        '''External trigger setting

        Parameters
        ----------
        exp_trg_en : int
            Select the signal to be used as an external trigger
            0 : Disable
            1: TTL trigger
            2: Differential trigger (shared with encoder)
            3: New differential trigger
            4: OPT trigger
        ext_trg_mode : int
            External trigger mode
            0 : Mode in which CC is output once by one external trigger (Continuous external trigger mode)
            1 : Mode in which CC is output periodically by one external trigger (single shot external trigger mode)
        ext_trg_dly : int
            External trigger detection delay time (1uSec unit)
        ext_trg_chatter : int
            External trigger detection disable time (1uSec unit)
        timeout : int
            Detection standby time (1mSec unit)

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error
        '''
        ret = acaplib2.AcapSetExternalTrigger(self.__hHandle, self.__ch, exp_trg_en, ext_trg_mode, ext_trg_dly, ext_trg_chatter, timeout)
        if ret != self.OK:
            self.print_last_error()
        return ret

    def get_external_trigger(self) -> Tuple[int, int, int, int, int, int]:
        '''Get external trigger setting

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error
        exp_trg_en : int
            Select the signal to be used as an external trigger
            0 : Disable
            1: TTL trigger
            2: Differential trigger (shared with encoder)
            3: New differential trigger
            4: OPT trigger
        ext_trg_mode : int
            External trigger mode
            0 : Mode in which CC is output once by one external trigger (Continuous external trigger mode)
            1 : Mode in which CC is output periodically by one external trigger (single shot external trigger mode)
        ext_trg_dly : int
            External trigger detection delay time (1uSec unit)
        ext_trg_chatter : int
            External trigger detection disable time (1uSec unit)
        timeout : int
            Detection standby time (1mSec unit)
        '''
        # -> exp_cycle, exposure, exp_pol, exp_unit, cc_sel
        ret = acaplib2.AcapGetExternalTrigger(self.__hHandle, self.__ch)
        if ret[0] != self.OK:
            self.print_last_error()
        return ret

    def set_strobe(self, strobe_en : int, strobe_delay : int, strobe_time : int) -> int:
        '''Strobe setting

        Parameters
        ----------
        strobe_en : int
            Strobe Use setting
            0 : Disable
            1: Enabled
        strobe_delay : int
            Delay time until strobe pulse is output (1uSec unit) 0~65535
        strobe_time : int
            Strobe pulse output time (1uSec unit) 0~65535

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error
        '''
        ret = acaplib2.AcapSetStrobe(self.__hHandle, self.__ch, strobe_en, strobe_delay, strobe_time)
        if ret != self.OK:
            self.print_last_error()
        return ret

    def get_strobe(self) -> Tuple[int, int, int, int]:
        '''Get strobe setting

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error
        strobe_en : int
            Strobe Use setting
            0 : Disable
            1: Enabled
        strobe_delay : int
            Delay time until strobe pulse is output (1uSec unit) 0~65535
        strobe_time : int
            Strobe pulse output time (1uSec unit) 0~65535
        '''
        ret = acaplib2.AcapGetStrobe(self.__hHandle, self.__ch)
        if ret[0] != self.OK:
            self.print_last_error()
        return ret

    def set_encoder(self, enc_enable : int, enc_mode : int, enc_start : int, enc_phase : int, enc_direction : int, z_phase_enable : int, compare1 : int, compare2 : int) -> int:
        '''Encoder settings

        Parameters
        ----------
        enc_enable : int
            Encoder use setting
            0 : Disable
            1: Enabled
        enc_mode : int
            Encoder mode
            0 : Encoder scan mode
            1 : Encoder line selection mode
        enc_start : int
            How to start the encoder
            0 : Start the encoder by CPU
            1 : Start the encoder with an external trigger
            2 : Start the encoder with the CPU and use the external trigger as matching pulses
        enc_phase : int
            Encoder phase
            0 : AB phase
            1 : A phase
        enc_direction : int
            Encoder rotation direction
            0 : CW
            1 : CCW
        z_phase_enable : int
            Z-phase usage settings
            0 : Not used
            1 : Use
        compare1 : int
            Comparison register 1 (delay pulse setting) 0~4294967295
        compare2 : int
            Comparison register 2 (interval pulse setting) 1~4294967295

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error
        '''
        ret = acaplib2.AcapSetEncoder(self.__hHandle, self.__ch, enc_enable, enc_mode, enc_start, enc_phase, enc_direction, z_phase_enable, compare1, compare2)
        if ret != self.OK:
            self.print_last_error()
        return ret

    def get_encoder(self) -> Tuple[int, int, int, int, int, int, int, int, int, int]:
        '''Get the encoder setting value

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error
        enc_enable : int
            Encoder use setting
            0 : Disable
            1: Enabled
        enc_mode : int
            Encoder mode
            0 : Encoder scan mode
            1 : Encoder line selection mode
        enc_start : int
            How to start the encoder
            0 : Start the encoder by CPU
            1 : Start the encoder with an external trigger
            2 : Start the encoder with the CPU and use the external trigger as matching pulses
        enc_phase : int
            Encoder phase
            0 : AB phase
            1 : A phase
        enc_direction : int
            Encoder rotation direction
            0 : CW
            1 : CCW
        z_phase_enable : int
            Z-phase usage settings
            0 : Not used
            1 : Use
        compare1 : int
            Comparison register 1 (delay pulse setting) 0~4294967295
        compare2 : int
            Comparison register 2 (interval pulse setting) 1~4294967295
        comp2_count : int
            Encoder count value
        '''
        ret = acaplib2.AcapGetEncoder(self.__hHandle, self.__ch)
        if ret[0] != self.OK:
            self.print_last_error()
        return ret

    def set_encoder_abs_multipoint(self, point_no : int, abs_count : int) -> int:
        '''Set the multipoint value of the encoder absolute count.

        Parameters
        ----------
        point_no : int
            Multipoint number
        abs_count : int
            Absolute count value

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error
        '''
        return self.set_info(acaplib2.ACL_ENC_ABS_MP_COUNT, abs_count, point_no)

    def get_encoder_abs_multipoint(self, point_no : int) -> Tuple[int, int]:
        '''Get the multipoint value of the encoder absolute count.

        Parameters
        ----------
        point_no : int
            Multipoint number

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error
        abs_count : int
            Absolute count value
        '''
        return self.get_info(acaplib2.ACL_ENC_ABS_MP_COUNT, point_no)

    def set_bit_assign_ex(self, bit_assign_info : acaplib2.BITASSIGNINFO) -> int: # Ver.1.0.2で追加
        '''Input image sorting settings.

        Parameters
        ----------
        bit_assign_info : acaplib2.BITASSIGNINFO
           Structure that stores sorting information

        Returns
        -------
        int
            Error information
            1 : OK
            0 : Error
        '''
        ret = acaplib2.AcapSetBitAssignEx(self.__hHandle, self.__ch, bit_assign_info)
        #ret = acaplib2.AcapSetBitAssignEx(self.__hHandle, self.__ch,
        #id(bit_assign_info))
        if ret != self.OK:
            self.print_last_error()
        return ret

    def get_bit_assign_ex(self) -> Tuple[int, acaplib2.BITASSIGNINFO]: # Ver.1.0.2で追加
        '''Get input image sorting settings.

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error
        bit_assign_info : acaplib2.BITASSIGNINFO
            Input image sorting
        '''
        ret = acaplib2.AcapGetBitAssignEx(self.__hHandle, self.__ch)
        if ret[0] != self.OK:
            self.print_last_error()
        return ret

    # 非対応
    #def set_dma_option_ex(self, mem_num : int, acl_buffer_info) -> int:
    #    '''Sets the DMA method.

    #    Parameters
    #    ----------
    #    mem_num : int
    #        Set the number of the buffer to be transferred by special DMA.
    #    acl_buffer_info
    #        Structure indicating buffer information to be transferred by special DMA
    #        The structure to be specified depends on the transfer method.
    #            ACL_BUFF_INFO_RESIZE structure : Different size DMA
    #            ACL_BUFF_INFO_ROI structure    : Nonlinear DMA(ROI)
    #            ACL_BUFF_INFO_DIVIDE structure : Buffer partitioning DMA

    #    Returns
    #    -------
    #    int
    #        Error information
    #        1 : OK
    #        0 : Error      
    #    '''
    #    ret = acaplib2.AcapSetDmaOptionEx(self.__hHandle, self.__ch, mem_num, acl_buffer_info)
    #    if ret != self.OK:
    #        self.print_last_error()
    #    else:
    #        self.__reflect_param_flag = True # reflect_paramが必要な場合はTrue
    #    return ret

    # 非対応
    #def get_dma_option_ex(self, mem_num : int):
    #    '''Get extended transfer format settings

    #    Parameters
    #    ----------
    #    mem_num : int
    #        Set the number of the buffer to retrieve information from. 0 or less will result in an error.

    #    Returns
    #    -------
    #    int
    #        Error information
    #        1 : OK
    #        0 : Error
    #    '''
    #    ret = acaplib2.AcapGetDmaOptionEx(self.__hHandle, self.__ch, mem_num)
    #    if ret[0] != self.OK:
    #        self.print_last_error()
    #    return ret

    def _serial_set_parameter(self, baud_rate = 9600, data_bit = 8, parity = 0, stop_bit = 0, flow = 0) -> int:
        
        # Open後にしか設定できない
        if self.__is_serial_open == False:
            return self.ERROR

        ret = acaplib2.AcapSerialSetParameter(self.__hHandle, self.__ch, 
            baud_rate, data_bit, parity, stop_bit, flow)

        if ret != self.OK:
            self.print_last_error()

        return ret

    def serial_get_parameter(self) -> Tuple[int, int, int, int, int, int]:
        '''Get the parameters for serial communication.

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error            
        baud_rate : int
            baud rate
        data_bit : int
            Data bits (5 to 8) are stored.
        parity : int
            The parity setting information is stored.
            0 : None
            1 : Odd number
            2 : Even number
            3 : Mark
            4 : Space
        stop_bit : int
            Stop bit
            0 : 1bit
            1 : 1.5bit
            2 : 2bit
        flow : int
            Flow control information
            0 : None
            1 : Xon / Xoff
            2 : Hardware
        '''
        baud_rate = 0
        data_bit = 0
        parity = 0
        stop_bit = 0
        flow = 0
        
        # Open後にしか取得できない
        if self.__is_serial_open == False:
            return self.ERROR, baud_rate, data_bit, parity, stop_bit, flow

        # ret, npBaudRate.value, npDataBit.value, npParity.value,
        # npStopBit.value, npFlow.value
        ret, baud_rate, data_bit, parity, stop_bit, flow = acaplib2.AcapSerialGetParameter(self.__hHandle, self.__ch)

        if ret != self.OK:
            self.print_last_error()

        return ret, baud_rate, data_bit, parity, stop_bit, flow

    def serial_open(self, baud_rate : int = 9600, data_bit : int = 8, parity : int = 0, stop_bit : int = 0, flow : int = 0) -> int:
        '''Open the serial port.

        Parameters
        ----------
        baud_rate : int
            Baud rate
        baud_rate : int
            Baud rate
            9600,19200,38400,57600,115200
        data_bit : int
            Data bit(8 only)
        parity : int
            Parity(0 only)
            0 : None
            1 : Odd number
            2 : Even number
            3 : Mark
            4 : Space
        stop_bit : int
            Stop bit(0 only)
            0 : 1bit
            1 : 1.5bit
            2 : 2bit
        flow : int
            Flow control information(0 only)
            0 : None
            1 : Xon / Xoff
            2 : Hardware

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error   
        '''
        
        if self.__is_serial_open is False:
            ret = acaplib2.AcapSerialOpen(self.__hHandle, self.__ch)
            if ret != self.OK:
                self.print_last_error()
                return self.ERROR
        else:
            ret = 1

        self.__is_serial_open = True

        ret = self._serial_set_parameter(baud_rate, data_bit, parity, stop_bit, flow)

        return ret

    def serial_close(self) -> int:
        '''Close the serial port.

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error   
        '''

        if self.__is_serial_open == False:
            return 0
            #pass

        if self.__hHandle == acaplib2.INVALID_HANDLE_VALUE:
            return 0

        ret = acaplib2.AcapSerialClose(self.__hHandle, self.__ch)
        if ret != self.OK:
            self.print_last_error()

        self.__is_serial_open = False

        return ret

    def serial_write(self, write_command : str, asc : bool = True, start_str : str = "", end_str : str = "\r") -> int:
        
        '''Serial transmission

        Parameters
        ----------
        write_command : str
            Commands to be sent to serial
        asc : bool
            Specifies the code for characters to be written (sent) to the serial.
            False : Hexadecimal (HEX) notation
            True : ASCII
        start_str : str
            Can be specified when 'asc' is TRUE.
            Command start string (ASCII notation)
        end_str : str
            Can be specified when 'asc' is TRUE.
            Command terminator string (ASCII notation)

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error 
        '''
        ret = acaplib2.AcapSerialWrite(self.__hHandle, self.__ch, asc, write_command, start_str, end_str)
        if ret != self.OK:
            self.print_last_error()
        return ret
  
    def serial_read(self, asc : bool = True, time_out : int = 100, buffer_size : int = 511, end_str : Union[str, None] = None) -> Tuple[int, str, int]:
        '''Serial Reception

        Parameters
        ----------
        asc : bool
            Specifies the code for characters to be written (sent) to the serial.
            False : Hexadecimal (HEX) notation
            True : ASCII
        time_out : int
            Specifies the timeout [mSec] until the end of the received data buffer matches the terminated string.
            If 0 is specified, the data is received without waiting.
        buffer_size : int
            Specifies the command string storage buffer size.
        end_str : Union[str, None]
            Set the command terminator string.

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error 
        read_command : str
            Received command string
        read_bytes
            Size of the received string (in bytes)
        '''

        recieve = ""
        recieve_flag = True
        recieve_size = 0
        zero_count = 0

        ret = acaplib2.ACL_RTN_ERROR

        while recieve_flag == True:
            ret, text, str_len = acaplib2.AcapSerialRead(self.__hHandle, self.__ch, asc, time_out, buffer_size, end_str)
            recieve += text
            recieve_size += str_len
            if str_len == 0:
                time.sleep(self.__serial_read_wait_time)
                zero_count += 1
            else:
                zero_count = 0
            if zero_count >= 2 or end_str is not None:
                # 2回連続で受信バッファが何も無ければ受信を抜ける、最後はここで抜ける
                recieve_flag = False #念のため
                break

        if ret != acaplib2.ACL_RTN_OK and end_str is None:
            if recieve_size > 0:
                ret = acaplib2.ACL_RTN_OK

        return ret, recieve, recieve_size


    def set_gpout(self, output_level : int) -> int:
        '''Set the GPOUT level.

        Parameters
        ----------
        output_level : int
            GPOUT level

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error 
        '''

        ret = acaplib2.AcapSetGPOut(self.__hHandle, self.__ch, output_level)
        if ret != self.OK:
            self.print_last_error()
        return ret


    def get_gpout(self) -> Tuple[int, int]:
        '''Get the GPOUT level.

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error 
        output_level : int
            GPOUT level
        '''
        ret = acaplib2.AcapGetGPOut(self.__hHandle, self.__ch)
        if ret[0] != self.OK:
            self.print_last_error()
        return ret

    # -------------------------------------------------------------------
    # Ver.1.0.2 (AcapLib2 Ver.8.0.0対応版)

    #【AcapLib2 Ver.7.3.2対応】
    #AVALCAPLIB2DLL int WINAPI AcapGetCameraFeatureInfo(HANDLE hDev, int nCh, char* pFeatureName, int nOption, PACL_CAM_FEATURE_INFO pFeatureInfo);
    def get_camera_feature_info(self, pFeatureName : str, nOption : int) -> Tuple[int, acaplib2.ACL_CAM_FEATURE_INFO]:
        '''Get the parameter information of the Feature at the level specified by nOption.

        Parameters
        ----------
        pFeatureName : str
            Specify the Featurename to be acquired.
        nOption : int
            Specify the acquisition level.
            0: Beginner
            1: Expert
            2: Guru
            3: Get the entire FeatureList. (including Invisible)

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error 
        pFeatureInfo : ACL_CAM_FEATURE_INFO
            Camera feature info
        '''
        ret, pFeatureInfo = acaplib2.AcapGetCameraFeatureInfo(self.__hHandle, self.__ch, pFeatureName, nOption)
        if ret != self.OK:
            self.print_last_error()
        return ret, pFeatureInfo

    #AVALCAPLIB2DLL int WINAPI AcapGetCameraCategoryFeatureList(HANDLE hDev,int nCh, char* pCategoryName, int nOption, PACL_CAM_FEATURE_LIST pList);
    def get_camera_category_feature_list(self, pCategoryName : str, nOption : int) -> Tuple[int, acaplib2.ACL_CAM_FEATURE_LIST]:
        '''Get the Feature name under the category specified in pCategoryName.

        Parameters
        ----------
        pCategoryName : str
            Specify the Category/Feature to be acquired.
        nOption : int
            Specify the acquisition level.
            0: Beginner
            1: Expert
            2: Guru
            3: Get the entire FeatureList. (including Invisible)

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error 
        pList : ACL_CAM_FEATURE_LIST
            Get a list of Category/Features.
        '''
        ret, pList = acaplib2.AcapGetCameraCategoryFeatureList(self.__hHandle, self.__ch, pCategoryName, nOption)
        if ret != self.OK:
            self.print_last_error()
        return ret, pList


    #AVALCAPLIB2DLL int WINAPI AcapGetCameraPropertyList(HANDLE hDev, int nCh, char* pCategoryName, int nOption, PACL_CAM_PROPERTY_LIST pPropList);
    def get_camera_property_list(self, pCategoryName : str, nOption : int) -> Tuple[int, acaplib2.ACL_CAM_PROPERTY_LIST]:
        '''Get property information for the category specified in pCategoryName.

        Parameters
        ----------
        pCategoryName : str
            Specify the Category/Feature to be acquired.
        nOption : int
            reserved

        Returns
        -------
        ret : int
            Error information
            1 : OK
            0 : Error 
        pPropList : ACL_CAM_PROPERTY_LIST
            Get a list of Category/Features.
        '''
        ret, pPropList = acaplib2.AcapGetCameraPropertyList(self.__hHandle, self.__ch, pCategoryName, nOption)
        if ret != self.OK:
            self.print_last_error()
        return ret, pPropList

    #AVALCAPLIB2DLL int WINAPI AcapGetLastErrorCodeEx(int nCh, PACAPERRORINFOEX pAcapErrInfoEx, BOOL bErrReset);
    def get_last_error_ex(self, bErrReset : bool = False) -> acaplib2.ACAPERRORINFOEX:
        '''Returns the error that occurred immediately before this function was called.

        Parameters
        ----------
        bErrReset : bool
            Reset the value stored in the structure.

        Returns
        -------
        pAcapErrInfoEx : ACAPERRORINFOEX
            Get the structure that stores error information.
        '''
        pAcapErrInfoEx = acaplib2.AcapGetLastErrorCodeEx(self.__ch, bErrReset)

        return pAcapErrInfoEx

    # -------------------------------------------------------------------
