import copy

import time
import traceback

from zlgsendcan.crc import crc_check
from zlgsendcan.parseDBC import GlobleValue, DbcInit, get_signal_data1
from zlgsendcan.zlgcan1 import *
import threading

from utils.log_util import loginfo


# 获取dbc文件解析的db对象做成全局变量调用
def get_dbc_db(dbc_path):
    # GlobleValue.dbc_init = get_signal_data1(dbc_path).db  # 初始化解析dbc文件
    return get_signal_data1(dbc_path).db


class MessageDate:
    def __init__(self, can_type, chanl, brate: dict):
        """

        :param can_type: 1、can 2、canfd
        :param chanl: 0,1
        :param brate: {'zcy':'500kbps 80%','sjy':'2Mbps 80%‘}注意如果自定义波特率格式如下
                        {'zcy':'自定义','sjy':‘500Kbps(85%),2.0Mbps(80%),(20,00000520,00000106)’}
        """
        GlobleValue.can_conf['chan'] = chanl
        GlobleValue.can_conf['zcy'] = brate['zcy']
        GlobleValue.can_conf['can_type'] = can_type
        GlobleValue.can_conf['sjy'] = brate['sjy']

        self.zcanlib = ZCAN()
        # self.testcantype = 1  # 0:CAN; 1:canfd
        self.handle = self.zcanlib.OpenDevice(ZCAN_USBCANFD_200U, 0, 0)
        if self.handle == INVALID_DEVICE_HANDLE:
            # msgbox = QMessageBox(QMessageBox.Critical, '错误', "请检查周立功是否连接或重复开启！")
            # msgbox.adjustSize()
            # msgbox.show()
            # msgbox.exec_()
            print('"请检查周立功是否连接或重复开启！')
            print("Open CANFD Device failed!")
            # exit(0)
        print("device handle:%d." % (self.handle))
        info = self.zcanlib.GetDeviceInf(self.handle)
        print("Device Information:\n%s" % (info))

        # Start CAN
        self.chn_handle = canfd_start(self.zcanlib, self.handle, GlobleValue.can_conf['chan'],
                                      GlobleValue.can_conf)
        print("channel handle:%d." % (self.chn_handle))

    # 检查设备是否在线
    def check_device_online(self):
        return self.zcanlib.DeviceOnLine(self.handle)

    def clear_buffer(self):
        ret = self.zcanlib.ClearBuffer(self.chn_handle)
        if ret == 1:
            print("ClearBuffer success! ")

    def close_device(self):
        # Close CAN
        ret = self.zcanlib.ResetCAN(self.chn_handle)
        if ret == 1:
            print("ResetCAN success! ")
        # Close Device
        ret = self.zcanlib.CloseDevice(self.handle)
        if ret == 1:
            print("CloseDevice success! ")
        GlobleValue.global_msg3 = {}


# auto send
def auto_send_msg(ob, data, data_len):
    def fun(ctime):
        for index in range(data_len):
            AutoCAN_A = ZCANFD_AUTO_TRANSMIT_OBJ()
            AutoCAN_A.enable = 1  # enable
            AutoCAN_A.index = index
            AutoCAN_A.interval = int(ctime)  # ms
            AutoCAN_A.obj.frame.can_id = ob.message_frame_id
            AutoCAN_A.obj.transmit_type = 0
            AutoCAN_A.obj.frame.eff = 0
            AutoCAN_A.obj.frame.rtr = 0
            AutoCAN_A.obj.frame.len = ob.message_length
            for j in range(AutoCAN_A.obj.frame.len):
                AutoCAN_A.obj.frame.data[j] = data[index][j]
            AutoCAN_A_delay = ZCANFD_AUTO_TRANSMIT_OBJ_PARAM()
            AutoCAN_A_delay.index = AutoCAN_A.index
            AutoCAN_A_delay.type = 1
            AutoCAN_A_delay.value = 100

    return fun


# dbc发送
def canfd_msg(ob, data, chanl):
    try:

        data = [data] if type(data[0]) != list else data
        data_len = len(data)
        # print('=============',data_len)
        canfd_msgs = (ZCANDataObj * data_len)()
        # memset(byref(canfd_msgs), 0, sizeof(canfd_msgs))
        # canfd_msgs = (ZCAN_TransmitFD_Data * 10)()
        for i in range(data_len):
            canfd_msgs[i].dataType = 1  # can/canfd frame
            # canfd_msgs[i].chnl = int(GlobleValue.can_conf['chan'])  # can_channel
            canfd_msgs[i].chnl = int(chanl)  # can_channel
            canfd_msgs[i].zcanfddata.flag.frameType = 1 if GlobleValue.can_conf[
                                                               'can_type'] == 'canfd' else 0  # 0-can,1-canfd
            # canfd_msgs[i].zcanfddata.frame.eff = 0
            # canfd_msgs[i].zcanfddata.frame.rtr = 0
            # canfd_msgs[i].zcanfddata.frame.brs = 1
            # canfd_msgs[i].zcanfddata.frame.esi = 0
            # canfd_msgs[i].zcanfddata.frame.__pad = 0x20  # 队列发送，当值为0x20时，单位为ms;  当值为0x30时，单位是100us。
            # canfd_msgs[i].zcanfddata.frame.__res0 = 0x1388  # 帧间隔低位,定时100ms
            # canfd_msgs[i].zcanfddata.frame.__res1 = 0x00  # 帧间隔高位
            canfd_msgs[i].zcanfddata.flag.txDelay = 0  # 0不添加延迟，1添加延时
            canfd_msgs[i].zcanfddata.flag.transmitType = 0  # 发送方式，0-正常发送
            canfd_msgs[i].zcanfddata.flag.txEchoRequest = 1  # 发送回显请求，0-不回显，1-回显
            canfd_msgs[i].zcanfddata.frame.can_id = ob.message_frame_id
            canfd_msgs[i].zcanfddata.frame.len = ob.message_length
            canfd_msgs[i].zcanfddata.flag.txEchoed = 1
            # for x in data:
            for j in range(ob.message_length):
                canfd_msgs[i].zcanfddata.frame.data[j] = data[i][j]
        return canfd_msgs, data_len
    except Exception as e:
        print('canfd_msg组装数据错误==', e, data, ob.message_length, ob.message_frame_id)


# 普通发送
def canfd_msg_power(idx, data, chanl):
    data_len = len(data)
    canfd_msgs = (ZCANDataObj * data_len)()
    for i in range(data_len):
        canfd_msgs[i].dataType = 1  # can/canfd frame
        # canfd_msgs[i].chnl = int(GlobleValue.can_conf['chan'])  # can_channel
        canfd_msgs[i].chnl = int(chanl)  # can_channel
        canfd_msgs[i].zcanfddata.flag.frameType = 1 if GlobleValue.can_conf[
                                                           'can_type'] == 'canfd' else 0  # 0-can,1-canfd
        canfd_msgs[i].zcanfddata.flag.txDelay = 0  # 不添加延迟
        canfd_msgs[i].zcanfddata.flag.transmitType = 0  # 发送方式，0-正常发送
        canfd_msgs[i].zcanfddata.flag.txEchoRequest = 1  # 发送回显请求，0-不回显，1-回显
        canfd_msgs[i].zcanfddata.frame.can_id = int(idx, 16)
        canfd_msgs[i].zcanfddata.frame.len = 8
        canfd_msgs[i].zcanfddata.flag.txEchoed = 1  # 0发送txEchoed
        for j in range(8):
            canfd_msgs[i].zcanfddata.frame.data[j] = data[j]
    return canfd_msgs, data_len


class ZlgSend:

    def __init__(self, handle, data, dbc_file, chanl=0, pro_name=None, is_key=False):
        GlobleValue.thread_run = True
        self.dbc_prase_obj = get_dbc_db(dbc_file)
        if not is_key:
            for k, v in data.items():
                thread_list = []
                if k not in ['cycle_time', 'send_num', 'msg_id', 'is_crc', 'chanl']:
                    ctime = data.get('cycle_time')
                    sendnum = data['send_num']
                    is_crc = '0' if data.get('is_crc') is None else data.get('is_crc')
                    for sn, sv in v.items():
                        if isinstance(sv, dict):
                            sigchange_th = ThreadSingChange(self.dbc_prase_obj, chanl)
                            sigchange_th.flag = True
                            exit = threading.Event()

                            sig_th = threading.Thread(target=sigchange_th.runn,
                                                      args=(handle, k, v, ctime, sendnum, exit, is_crc, pro_name,
                                                            dbc_file), daemon=True)
                            sig_th.start()
                            thread_list.append(sigchange_th)
                            thread_list.append(sig_th)
                            thread_list.append(exit.isSet())
                            # GlobleValue.thread_obj[k] = thread_list
                            GlobleValue.thread_obj[k] = thread_list
                            break
                    else:
                        ob = DbcInit(k, v, self.dbc_prase_obj)
                        if is_crc == '1':
                            # 动态导入crc模块，然后强制重载该模块，这样就会更新内存中缓存数据
                            # module_name = "CRC_Check.crc"
                            # my_module = importlib.import_module(module_name)
                            # importlib.reload(my_module)
                            result = crc_check(pro_name, k, v, self.dbc_prase_obj)
                        else:
                            # ob.crc = True if is_crc == '1' else False
                            # ob.pro_name = pro_name
                            # dbc解析出来的数据
                            result = ob.dbc_parser()
                        if isinstance(result, str):
                            # msgbox = QMessageBox(QMessageBox.Critical, '错误', result)
                            # msgbox.adjustSize()
                            # msgbox.exec_()
                            return
                        # 数据对象

                        data_obj, data_len = canfd_msg(ob, result, chanl)
                        msg_th = ThreadStep(data_obj, ctime, sendnum, data_len)
                        msg_th.flag = True
                        th = threading.Thread(target=msg_th.runn, args=[handle],
                                              daemon=True)
                        th.start()
                        thread_list.append(msg_th)
                        thread_list.append(th)
                        # thread_list.append(exit.isSet())
                        # GlobleValue.thread_obj[k] = thread_list
                        GlobleValue.thread_obj[k] = thread_list
        else:
            for k, v in data.items():
                if k not in ['cycle_time', 'send_num', 'msg_id', 'is_crc']:
                    ctime = data['cycle_time']
                    a = int(ctime) if ctime != 'null' else 0
                    if data['is_crc'] == '1':
                        # module_name = "CRC_Check.crc"
                        # my_module = importlib.import_module(module_name)
                        # importlib.reload(my_module)
                        result = crc_check(pro_name, k, v)
                    else:
                        ob = DbcInit(k, v, self.dbc_prase_obj)
                        # ob.crc = True if data['is_crc'] == '1' else False
                        # ob.pro_name = pro_name
                        # dbc解析出来的数据
                        result = ob.dbc_parser()
                    data_obj, _ = canfd_msg(ob, result, chanl)
                    ret = handle.zcanlib.TransmitData(handle.chn_handle, data_obj, 1)
                    time.sleep(a / 1000)


# 等差发送
class ThreadSingChange:
    def __init__(self, dbc_prase_obj, chanl):
        self.flag = False
        self.dbc_prase_obj = dbc_prase_obj
        self.chanl = chanl

    def runn(self, ob1, k, v, ctime, sendnnum, exit, is_crc, pro_name, dbc_file=None):
        try:

            self.calusig(ob1, k, v, ctime, sendnnum, exit, is_crc, pro_name)

        except Exception as e:
            print('信号发送错误-----------》', e)

    # 等差发送计算逻辑
    def calusig(self, ob1, k, v, ctime, sendnnum, exit, is_crc, pro_name):
        siglist = []
        for sk, sv in v.items():
            b = {}
            if isinstance(sv, dict):
                b[sk] = sv
                siglist.append(b)
        c_siglist = copy.deepcopy(siglist)
        len_sig = len(siglist)
        if len_sig == 1:
            for sk, sv in v.items():
                if isinstance(sv, dict):
                    ob = DbcInit(k, v, db_obj=self.dbc_prase_obj)
                    # ob.crc = True if is_crc == '1' else False
                    # ob.pro_name = pro_name
                    step_value = float(sv['步长'])
                    min_value = float(sv['最小值'])
                    max_value = float(sv['最大值'])
                    if ctime is None:
                        a = ob.message_cycle_time
                    else:
                        a = int(ctime) if ctime != 'null' else 0
                    f = 0
                    c = 0
                    while GlobleValue.thread_run and self.flag:
                        v[sk] = min_value
                        if sendnnum != '-1':
                            if f <= int(sendnnum):
                                f += 1
                            else:
                                break
                        if min_value > max_value:
                            v[sk] = float(sv['最小值'])
                            min_value = float(sv['最小值'])
                        # dbc解析出来的数据
                        if is_crc == '1':
                            # module_name = "CRC_Check.crc"
                            # my_module = importlib.import_module(module_name)
                            # importlib.reload(my_module)
                            result = crc_check(pro_name, k, v)
                        else:
                            result = ob.dbc_parser(v)
                        # 数据对象
                        data_obj, data_len = canfd_msg(ob, result, self.chanl)
                        # for t in range(data_len):
                        if ob.crc:
                            if c > 14:
                                c = 0
                            ret = ob1.zcanlib.TransmitData(ob1.chn_handle, data_obj[c], 1)
                            time.sleep(a / 1000)
                            c += 1
                        else:
                            for t in range(data_len):
                                ret = ob1.zcanlib.TransmitData(ob1.chn_handle, data_obj[t], 1)
                                time.sleep(a / 1000)
                        min_value += step_value
                        # print("Tranmit CANFD Num: %d." % ret)
        else:
            for sk, sv in v.items():
                if isinstance(sv, dict):
                    ob = DbcInit(k, v, db_obj=self.dbc_prase_obj)
                    # ob.crc = True if is_crc == '1' else False
                    # ob.pro_name = pro_name
                    step_value = float(sv['步长'])
                    min_value = float(sv['最小值'])
                    max_value = float(sv['最大值'])
                    a = int(ctime) if ctime != 'null' else 0
                    f = 0
                    c = 0
                    v2_k = None
                    v2_v = None
                    for sig2, v2 in c_siglist[1].items():
                        v2_k = sig2
                        v2_v = v2
                    step_value2 = float(v2_v['步长'])
                    min_value2 = float(v2_v['最小值'])
                    max_value2 = float(v2_v['最大值'])
                    while GlobleValue.thread_run and self.flag:
                        v[sk] = min_value
                        v[v2_k] = min_value2

                        if sendnnum != '-1':
                            if f <= int(sendnnum):
                                f += 1
                            else:
                                break
                        if min_value > max_value:
                            v[sk] = float(sv['最小值'])
                            min_value = float(sv['最小值'])
                            min_value2 = float(v2_v['最小值'])
                            v[v2_k] = float(v2_v['最小值'])
                        # dbc解析出来的数据

                        if is_crc == '1':
                            # module_name = "CRC_Check.crc"
                            # my_module = importlib.import_module(module_name)
                            # importlib.reload(my_module)
                            result = crc_check(pro_name, k, v)
                        else:
                            result = ob.dbc_parser(v)
                        # 数据对象
                        data_obj, data_len = canfd_msg(ob, result, self.chanl)
                        # for t in range(data_len):
                        if ob.crc:
                            if c > 14:
                                c = 0
                            ret = ob1.zcanlib.TransmitData(ob1.chn_handle, data_obj[c], 1)
                            time.sleep(a / 1000)
                            c += 1
                        else:
                            for t in range(data_len):
                                ret = ob1.zcanlib.TransmitData(ob1.chn_handle, data_obj[t], 1)
                                time.sleep(a / 1000)
                        min_value += step_value
                        # print("Tranmit CANFD Num: %d." % ret)


# 普通发送
class NormalTransmission:
    def __init__(self, data, data_len):

        self.data = data
        self.data_len = data_len

    def runn(self, obj):
        while GlobleValue.flag_send:
            try:

                for t in range(self.data_len):
                    ret = obj.zcanlib.TransmitData(obj.chn_handle, self.data[t], 1)
            except Exception as e:
                loginfo().error(traceback.format_exc())
                traceback.print_exc()
                print("发送线程异常")


# 普通发送封装给ide创建脚本使用
def original_send_msg(zlginit, idx, valuelist, chan):
    valuelist = [int(i, 16) for i in valuelist.split(',')]
    for i in chan:
        data_obj1, data_len = canfd_msg_power(idx, valuelist, i)
        power = NormalTransmission(data_obj1, data_len)
        GlobleValue.flag_send = True
        th1 = threading.Thread(target=power.runn, args=[zlginit], name=power, daemon=True)
        th1.start()


# dbc发送
class ThreadStep:
    def __init__(self, data, ctime, sendnnum, data_len):
        self.flag = False
        self.data = data
        self.ctime = ctime
        self.sendnnum = str(sendnnum)
        self.data_len = data_len
        # self.update = False

    def runn(self, ob1):
        if self.sendnnum == '-1':
            while GlobleValue.thread_run and self.flag:
                try:
                    # if self.update:
                    #     ob1.clear_buffer()
                    #     self.update = False
                    for t in range(self.data_len):
                        ret = ob1.zcanlib.TransmitData(ob1.chn_handle, self.data[t], 1)
                        if self.ctime is None:
                            self.a = ob1.message_cycle_time
                        else:
                            self.a = int(self.ctime) if self.ctime != 'null' else 0
                        time.sleep(self.a / 1000)
                    else:
                        if self.sendnnum != '-1':
                            for i in range(int(self.sendnnum)):
                                ret = ob1.zcanlib.TransmitData(ob1.chn_handle, self.data[t], 1)
                                time.sleep(self.a / 1000)
                            # print("Tranmit CANFD Num: %d." % ret)
                            self.flag = False
                            # print("Tranmit CANFD Num: %d." % ret)
                except Exception as e:
                    print('信号发送错误-----------》', e)
            print('停止信号发送！！')
        else:
            f = 0
            while f < int(self.sendnnum):
                try:
                    ret = ob1.zcanlib.TransmitData(ob1.chn_handle, self.data, self.data_len)
                    self.a = int(self.ctime) if self.ctime != 'null' else 0
                    time.sleep(self.a / 1000)
                    f += 1
                    # print("Tranmit CANFD Num: %d." % ret)
                except Exception as e:
                    print('信号发送错误-----------》', e)


# 修改正在发送中的信号值
def update_signal_value(data_variable, message, signal, value: str, cycle_time=None, dbc_path=None, chanl='0'):
    # data_variable[message]['cycle_time'] = cycle_time
    data_variable[message][message][signal] = value
    ob = DbcInit(message, data_variable[message][message], get_dbc_db(dbc_path))
    result = ob.dbc_parser()
    data_obj, _ = canfd_msg(ob, result, chanl)
    GlobleValue.thread_obj[message][0].data = data_obj
    if cycle_time is not None:
        GlobleValue.thread_obj[message][0].ctime = cycle_time
    else:
        GlobleValue.thread_obj[message][0].ctime = ob.message_cycle_time


if __name__ == '__main__':
    # 周立功发送信号
    zlg_init = MessageDate('can', [0], {'zcy': '500kbps 80%', 'sjy': '2Mbps 80%'})
    # GlobleValue.zlginit = zlg_init
    # dbcpath = 'D:/广汽项目/A8E&GMC400_Proj_IHU_PFET_CMX V1.34.dbc'
    # get_dbc_db(dbcpath)
    # # 信号变化等差发送只需将对应的信号值改成{'步长':1,'最大值':1,'最小值':0}
    # msgdata = {'GW_BCS_2_B': {'GW_BCS_2_B': {'BCS_VehSpdVD': '1', 'BCS_VehSpd': '123'}, 'cycle_time': 10,
    #                           'msg_id': '0x260(608)', 'is_crc': '0', 'send_num': '-1'}}
    # for k, v in msgdata.items():
    #     ZlgSend(zlg_init, v, dbcpath)
    # # 修改信号值
    # update_signal_value(msgdata, 'GW_BCS_2_B', 'BCS_VehSpd', '120', cycle_time=50)
    # update_signal_value(msgdata, 'GW_BCS_2_B', 'BCS_VehSpd', '120', cycle_time=None)
    #
    # time.sleep(10)
