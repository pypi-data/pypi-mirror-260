'''Camera Control Module'''

from typing import Union, List, Tuple

from enum import Enum
from dataclasses import dataclass, field

import acapy


__version__ = "1.1.0"

'''
////////////////////////////////////////////////////////////
//  Ver.1.1.0  (2023.06.8)    Python 3.8以降対応
////////////////////////////////////////////////////////////
●新規追加
　GenICam対応カメラ（ACapLib2Ver.8.1.0対応ではCoaXPressカメラのみ）のパラメータ設定用クラスの追加

'''

class FeatureType(Enum):
    '''Enum indicating the type of setting value
    '''
    Value = 0
    Base = 1
    Integer = 2
    Boolean = 3
    Command = 4
    Float = 5
    String = 6
    Register = 7
    Category = 8
    Enumeration = 9
    EnumEntry = 10

class Visibility(Enum):
    '''Element defines the user level'''
    Beginner = 0
    Expert = 1
    Guru = 2
    Invisible = 3

class NoValue(Enum):
    '''NoValue

    Parameters
    ----------
    Enum : Enum
        For no value enum.
    '''
    def __repr__(self):
        #return '<%s.%s>' % (self.__class__.__name__, self.name)
        return f"{self.__class__.__name__}.{self.name}"

class AccessMode(NoValue):
    '''Access mode'''
    NI = b'NI'
    NA = b'NA'
    WO = b'WO'
    RO = b'RO'
    RW = b'RW'

#class ACL_CAM_FEATURE_INFO(Structure):
#	_fields_ = [
#		("nType",			c_int),
#		("nEntryStrNum",	c_int),
#		("EntryStr",		(c_char * 128) * 32),
#		("AccessMode",		c_char * 32),
#		("ValueMax",		c_double),
#		("ValueMin",		c_double),
#		("ValueInc",		c_double)
#		]

@dataclass
class ValueInfo:
    '''Set value information'''
    category: str       = ''    # category名
    name: str           = ''    # feature名
    value: Union[str, int, float, bool]        = ''    # 設定値
    description: str    = ''    # パラメータの説明
    type: FeatureType   = FeatureType.Value # featureの種類
    access_mode: AccessMode = AccessMode.NI # アクセスモード RW, RO, WO
    enum_list:list      = field(default_factory=list)    # 設定値enumのlist
    min: float          = 0.0   # 最小値
    max: float          = 0.0   # 最大値
    increment: float    = 0.0   # 最小設定分解能

#class ValueInfo(Structure):
#	_fields_ = [
#		("name",		str),
#		("value",	    str),
#		("type",		FeatureType),
#		("access_mode",	AccessMode),
#		("enum_list",	list),
#		("max",		    float),
#		("min",		    float),
#		("increment",	float)
#		]

class CameraControl():
    '''Class for camera configuration'''
    # GenICamによりカメラを制御するクラス

    def __init__(self, acapy_obj : acapy.AcaPy, visibility : Visibility = Visibility.Invisible, serial_read_wait_time : float = 0.0):
        '''Initialize the camera setting class.

        Parameters
        ----------
        acapy_obj : acapy
            acapy class object
        visibility : Visibility, optional
            User level, by default Visibility.Invisible
        serial_read_wait_time : float, optional
            Latency of serial communications(Sec), by default 0
        '''

        self.__disposed = True
        
        self.__acapy = acapy_obj

        if self.__acapy is None:
            return

        self.__disposed = False

        # シリアルがオープンしている場合は一旦閉じる
        self.__acapy.serial_close()

        ret = self.__acapy.serial_open()

        if ret != 1:
            self.__acapy = None
            return

        self.__visibility = visibility
        self.__serial_read_wait_time = serial_read_wait_time

    def dispose(self):
        '''Releases resources inside the class.
        '''
        if self.__disposed is True:
            return

        if self.__acapy is None:
            return

        self.__acapy.serial_close()

        self.__disposed = True
        self.__acapy = None

    def __del__(self):

        ###if self.__acapy is None:
        ###    return

        ###self.__acapy.serial_close()

        #self.dispose() # ここで処理すると、__del__が呼ばれるタイミングが遅れるので、制御しづらい
        pass

    @property
    def serial_read_wait_time(self) -> float:
        '''Get or set the time(mSec) to wait for the completion of serial communication reception.

        Returns
        -------
        float
            Wait time (msec)
        '''
        return self.__serial_read_wait_time
    @serial_read_wait_time.setter
    def serial_read_wait_time(self, value : float):
        self.__serial_read_wait_time = value

    def __get_camera_category_feature_node(self, parent_node : Union[list, None], visibility : Visibility):

        #user_level = Visibility.Invisible.value #  全 FeatureList を取得

        if self.__acapy is None:
            return None

        old__debug_print = self.__acapy.debug_print_enabled

        if parent_node is not None:
            ret, category_feature_list = self.__acapy.get_camera_category_feature_list(parent_node[0], visibility.value)
        else:
            # 最上位ノードのとき
            #ret, category_feature_list = self.__acapy.get_camera_category_feature_list(None, visibility.value)
            ret, category_feature_list = self.__acapy.get_camera_category_feature_list("", visibility.value)
            # デバッグ表示をオフにする
            self.__acapy.debug_print_enabled = False

        category_list = []
        if category_feature_list.CategoryNum > 0:
            for i in range(category_feature_list.CategoryNum):
                category_list.append([acapy.acaplib2.byte_decode(category_feature_list.CategoryName[i].value)])

        feature_list = []
        if category_feature_list.FeatureNum > 0:
            for i in range(category_feature_list.FeatureNum):
                name = acapy.acaplib2.byte_decode(category_feature_list.FeatureName[i].value)
                #if self.serial_write(name, True, "GenICam", None) != 1:
                if self.serial_write(name, True, "GenICam", "") != 1:
                    feature_list.append([name])
                else:
                    ret, read_str, _ = self.serial_read(True, 100, 256, None)
                    feature_list.append([name, read_str])

        # 子ノードの追加
        # 子ノードを再帰的に呼び出す
        for c in category_list:
            self.__get_camera_category_feature_node(c, visibility)
        for f in feature_list:
            self.__get_camera_category_feature_node(f, visibility)

        if parent_node is None:
            # デバッグ表示を元に戻す
            self.__acapy.debug_print_enabled = old__debug_print
            return ret, [category_list, feature_list]
        else:
            if len(category_list) > 0 or len(feature_list) > 0: # 両方ないときは追加しない
                parent_node.append([category_list, feature_list])
            return ret, parent_node

    def __list_to_text(self, list_obj):
        '''リストから文字列へ変換する'''
        list_text = " ["

        for txt in list_obj:
            list_text += "'" + txt + "', "

        # 最後の２文字分(", ")を置き換える
        return list_text[:-2] + "]"

    def __get_camera_category_feature_text(self, node, node_text : str, level = 0, description_enabled : bool = False) -> str:
        # ノード一覧のテキストを作成する

        if self.__acapy is None:
            return ""
        
        if len(node) == 0:
            return ""

        category = node[0]
        feature = node[1]

        tab_text = "    " # '\t'

        # category一覧の表示
        for c in category:
            if len(c) > 1:
                if isinstance(c[1], list):
                    node_text += tab_text * level + "(+)" + c[0] + "\n"
                    node_text = self.__get_camera_category_feature_text(c[1], node_text, level + 1, description_enabled)# + "\n"
                else:
                    node_text += tab_text * level + "(+)" + c[0] + '\t' + c[1] + "\n"

        # feature一覧の表示
        for f in feature:

            #access_mode, value_type, enum_list = self.get_feature_value_info(f[0])
            value_name = f[0]

            # 一時的にエラーを非表示にする
            old__debug_print = self.__acapy.debug_print_enabled
            self.__acapy.debug_print_enabled = False
            _, _, value_info = self.get_value(value_name)
            self.__acapy.debug_print_enabled = old__debug_print

            # value_info.
            # name: str           = ''    # feature名
            # value: str          = ''    # 設定値
            # type  FeatureType   = FeatureType.Value # featureの種類
            # access_mode: AccessMode = AccessMode.NI # アクセスモード RW, RO, WO
            # enum_list:list[str] = field(default_factory=list)    # 設定値enumのlist
            # max: float          = 0.0   # 最大値
            # min: float          = 0.0   # 最小値
            # increment: float    = 0.0   # 最小設定分解能

            description = ""
            if description_enabled == True:
                # Descriptionは表示しない方が見やすい
                if value_info is not None:
                    if value_info.description is not None:
                        description = "\t# " + value_info.description

            value_name = "'" + value_name + "'"
                        
            if len(f) > 1: # 設定値があるとき
                if isinstance(f[1], list):
                    # 子ノードがある場合
                    node_text += tab_text * level + value_name + "\n"
                    node_text = self.__get_camera_category_feature_text(f[1], node_text, level + 1, description_enabled)# + "\n"

                else:
                    if len(value_info.enum_list) > 0:
                        # 値がenumのとき
                        node_text += tab_text * level + f"{value_name:32s} {value_info.type.name:12s} {value_info.access_mode.name:3s}'{value_info.value}'" + self.__list_to_text(value_info.enum_list) + description +  "\n"
                    else:
                        # 値設定のとき
                        if value_info.access_mode == AccessMode.RW or value_info.access_mode == AccessMode.WO:
                            # 書込み可能のとき
                            if value_info.type == FeatureType.Float or value_info.type == FeatureType.Integer:
                                # 数値書込みのとき
                                node_text += tab_text * level + f"{value_name:32s} {value_info.type.name:12s} {value_info.access_mode.name:3s}{value_info.value} [{value_info.min} -> {value_info.max} : Inc {value_info.increment}]" + description + "\n"
                            else:
                                ###################################################################
                                #node_text += tab_text * level + f"{value_name:32s} {value_info.type.name:12s} {value_info.access_mode.name:3s}" + f[1] + description + "\n"
                                node_text += tab_text * level + f"{value_name:32s} {value_info.type.name:12s} {value_info.access_mode.name:3s}{value_info.value}" + description + "\n"
                        else:
                            #node_text += tab_text * level + f"{value_name:32s} {value_info.type.name:12s} {value_info.access_mode.name:3s}" + f[1] + description + "\n"
                            if value_info.type == FeatureType.EnumEntry or value_info.type == FeatureType.Enumeration or value_info.type == FeatureType.String:
                                # 文字列のとき
                                node_text += tab_text * level + f"{value_name:32s} {value_info.type.name:12s} {value_info.access_mode.name:3s}'{value_info.value}'" + description + "\n"
                            else:
                                node_text += tab_text * level + f"{value_name:32s} {value_info.type.name:12s} {value_info.access_mode.name:3s}{value_info.value}" + description + "\n"

            elif len(f) == 1: # 設定値が無いとき
                if value_info is not None:
                    node_text += tab_text * level + f"{value_name:32s} {value_info.type.name:12s} {value_info.access_mode.name:3s}" + description + "\n"
                else:
                    node_text += tab_text * level + f"{value_name:32s}" + description + "\n"

        return node_text

    #def get_camera_category_feature_text(self, visibility : Visibility = Visibility.Invisible, description_enabled : bool = False) -> str:
    def get_camera_category_feature_text(self, visibility : Visibility = None, description_enabled : bool = False) -> str:
        '''Get the text of category and feature information set in the camera.

        Parameters
        ----------
        visibility : Visibility, optional
            User level, by default Visibility.Invisible
        description_enabled : bool, optional
            Specifies whether or not to display the description., by default False

        Returns
        -------
        str
            Text displaying camera settings by category.
        '''
        if self.__acapy is None:
            # AcaPyオブジェクトが渡されていないとき
            return ""

        if self.__acapy.is_opened == False:
            # カメラが認識されていないとき
            return ""

        if visibility is None:
            visibility = self.__visibility

        ret, camera_category_feature_node = self.__get_camera_category_feature_node(None, visibility) # type: ignore

        ret = self.__get_camera_category_feature_text(camera_category_feature_node, "", 0, description_enabled)

        return ret

    def __get_camera_feature_list(self, parent_node, node, node_list, level = 0):
        # ノード一覧のテキストを作成する

        if self.__acapy is None:
            return
        
        if len(node) == 0:
            return

        category = node[0]
        feature = node[1]

        # category一覧の表示
        for c in category:
            if len(c) > 1:
                if isinstance(c[1], list):
                    #node_text = self.__get_camera_category_feature_text(c[1], node_text, level + 1)# + "\n"
                    #print(f"Category: {c[0]}")
                    self.__get_camera_feature_list(c[0], c[1], node_list, level + 1)# + "\n"
                else:
                    #node_text += tab_text * level + "(+)" + c[0], '\t', c[1] + "\n"
                    pass

        # feature一覧の表示
        for f in feature:

            value_name = f[0]

            # 一時的にエラーを非表示にする
            old__debug_print = self.__acapy.debug_print_enabled
            self.__acapy.debug_print_enabled = False
            # 値の取得
            ret, _, value_info = self.get_value(value_name)
            # エラー表示を元に戻す
            self.__acapy.debug_print_enabled = old__debug_print

            if ret == False and len(value_name) > 0:
                value_info = ValueInfo()
                value_info.name = value_name

            value_info.category = parent_node
            node_list.append(value_info)

            if len(f) > 1:
                if isinstance(f[1], list):
                    # 子ノードがある場合
                    self.__get_camera_feature_list(f[0], f[1], node_list, level + 1)

    def get_camera_feature_list(self, visibility : Visibility = None) -> List[ValueInfo]:
        '''Get a list of values set for the camera.

        Parameters
        ----------
        visibility : Visibility, optional
            User level, by default None

        Returns
        -------
        List[ValueInfo]
            Get a list of camera setting value information.
        '''
        if visibility is None:
            visibility = self.__visibility

        # AcapLib2からノード情報を取得
        _, camera_category_feature_node = self.__get_camera_category_feature_node(None, visibility) # type: ignore
        # ノード情報からfeatureのみの情報をlistで取得する
        node_list : List[ValueInfo] = []
        self.__get_camera_feature_list(None, camera_category_feature_node, node_list)

        return node_list

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
        if self.__acapy is None:
            return 0

        old_wait_time = self.__acapy.serial_read_wait_time
        self.__acapy.serial_read_wait_time = self.__serial_read_wait_time # シリアル通信の待ち時間を一時的に0にする

        # ----------------------------------------------------------------------
        ret = self.__acapy.serial_write(write_command, asc, start_str, end_str)
        # ----------------------------------------------------------------------

        self.__acapy.serial_read_wait_time = old_wait_time

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
        read_bytes : int
            Size of the received string (in bytes)
        '''

        if self.__acapy is None:
            return 0, "", 0

        old_wait_time = self.__acapy.serial_read_wait_time
        self.__acapy.serial_read_wait_time = self.__serial_read_wait_time # シリアル通信の待ち時間を一時的に0にする

        # ----------------------------------------------------------------------
        ret = self.__acapy.serial_read(asc, time_out, buffer_size, end_str)
        # ----------------------------------------------------------------------

        self.__acapy.serial_read_wait_time = old_wait_time

        return ret

    def __try_int(self, value) -> int:
        '''
        文字列からintへ変換（エラー処理付き）
        '''
        int_value = 0
        try:
            int_value = int(value)
        except Exception as ex:
            pass

        return int_value

    def get_value(self, value_name : str) -> Tuple[bool, Union[int, float, str, bool, None], ValueInfo]:
        '''Get the camera setting value.

        Parameters
        ----------
        value_name : str
            Camera feature name

        Returns
        -------
        bool
            Error message
            True : OK
            False : Error 
        Union[int, float, str, bool, None]
            Camera setting value
        ValueInfo
            Value information
        '''

        value_info = ValueInfo()
        value_info.name = value_name

        if self.__acapy is None:
            return False, None, value_info #None

        # ---------------------------------------------------------------------
        # 値の取得
        ret = 0
        value = ''

        # 一時的にエラーを強制的に非表示
        old__debug_print = self.__acapy.debug_print_enabled
        self.__acapy.debug_print_enabled = False

        if self.serial_write(value_name, True, "GenICam", "") == 1:
            ret, read_str, _ = self.serial_read(True, 100, 256, "")
            value = read_str

        else:
            pass

        # 元に戻す
        self.__acapy.debug_print_enabled = old__debug_print

        # 仮代入（後で型変換を行う）
        value_info.value = value

        # 値の情報の取得
        ret, feature_info = self.__acapy.get_camera_feature_info(value_name, 0)
        if ret != 1:
            return False, None, value_info #None
            #return False, value_info.value, value_info

        #name: str           = ''    # feature名
        #value: str          = ''    # 設定値
        #type  FeatureType   = FeatureType.Value # featureの種類
        #access_mode: AccessMode = AccessMode.NI # アクセスモード RW, RO, WO
        #enum_list:list[str] = field(default_factory=list)    # 設定値enumのlist
        #max: float          = 0.0   # 最大値
        #min: float          = 0.0   # 最小値
        #increment: float    = 0.0   # 最小設定分解能

        value_info.type = FeatureType(feature_info.nType)

        value_info.access_mode = AccessMode[acapy.acaplib2.byte_decode(feature_info.AccessMode)]

        value_info.max = feature_info.ValueMax
        value_info.min = feature_info.ValueMin
        value_info.increment = feature_info.ValueInc

        # Descriptionの追加
        ret, property_list = self.__acapy.get_camera_property_list(value_name, Visibility.Invisible.value)
        for i in range(property_list.PropertyNum):
            txt = acapy.acaplib2.byte_decode(property_list.PropertyName[i].value)
            if txt == 'Description':
                des = acapy.acaplib2.byte_decode(property_list.PropertyValue[i].value) # Description
                des = des.replace('\n', '') # 改行の削除
                des = des.replace('\t', '') # タブの削除
                #print(f"{value_name}: {des}")
                value_info.description = des
                break

        # enumの追加
        if (feature_info.nType == FeatureType.Enumeration.value or
            feature_info.nType == FeatureType.EnumEntry.value):
            if feature_info.AccessMode != AccessMode.RO.value:
                enum_list = []
                for i in range(feature_info.nEntryStrNum):
                    enum_list.append(f"{acapy.acaplib2.byte_decode(feature_info.EntryStr[i].value)}")
                value_info.enum_list = enum_list

        # --------------------------------------------------------
        # value, max, min, incrementの型変換を行う
        #Integer = 2
        #Boolean = 3
        if value_info.type == FeatureType.Integer:
            value_info.value = self.__try_int(value_info.value)
            value_info.min = self.__try_int(value_info.min)
            value_info.max = self.__try_int(value_info.max)
            value_info.increment = self.__try_int(value_info.increment)
        elif value_info.type == FeatureType.Boolean:
            if value_info.value == "true":
                value_info.value = True
            else:
                value_info.value = False

        return True, value_info.value, value_info
    
    def set_value(self, value_name : str, value : Union[int, float, str, bool, None] = None) -> bool:
        '''Set the camera value.

        Parameters
        ----------
        value_name : str
            Camera feature name
        value : Union[int, float, str, bool, None], optional
            Setting value, by default None

        Returns
        -------
        bool
            Error message
            True : OK
            False : Error 
        '''

        if self.__acapy is None:
            return False

        # 設定値の情報を取得
        _, _, value_info = self.get_value(value_name)

        if (value_info.access_mode != AccessMode.RW and
            value_info.access_mode != AccessMode.WO):
            # 書込みモードでないときは何もしない
            return False

        if (value_info.type == FeatureType.Enumeration or
            value_info.type == FeatureType.EnumEntry):
            # Enumのとき
            if (value in [e for e in value_info.enum_list]) is False:
                # Enumに指定した値がないとき
                return False

            # 値の設定
            if self.serial_write(value_name + " " + str(value), True, "GenICam", "") != 1:
                return False

        elif value_info.type == FeatureType.Command:
            # コマンドのとき
            if self.serial_write(value_name + " Execute", True, "GenICam", "") != 1:
                return False

        else:
            # Boolのとき
            if value_info.type == FeatureType.Boolean:
                # True/False を true/false に変換する
                value = str(value).lower()

            # 値設定のとき
            if value_info.type == FeatureType.Integer:
                # Integerの値を設定するとき、増分(Inc)のチェック
                if value_info.increment > 0:
                    # valueがintかチェック
                    ret = isinstance(value, int)
                    if ret is False:
                        self.__acapy._debug_print("[set_value error]", f"value({value}) must be of type int.")
                        return False

                    # valueが割り切れるかチェック
                    if (int(value) % value_info.increment) != 0: # type: ignore
                        self.__acapy._debug_print("[set_value error]", f"value({value}) must be divisible by {value_info.increment}.")
                        return False

            if self.serial_write(value_name + " " + str(value), True, "GenICam", "") != 1:
                return False

        return True
