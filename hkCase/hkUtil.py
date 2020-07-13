import numpy as np
import os
import ctypes
import time

'''
    python操作海康sdk
'''

# 获取所有的库文件到一个列表
path = "lib/win64/"

# 连接参数
ip = "192.168.120.155"
port = 8000
username = "admin"
password = "quickhigh123456"


def file_name(file_dir):
    pathss = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            pathss.append(path + file)
    return pathss


dll_list = file_name(path)

lUserID = 0
lChannel = 1


def callCpp(func_name, *args):
    for HK_dll in dll_list:
        try:
            lib = ctypes.cdll.LoadLibrary(HK_dll)
            try:
                value = eval("lib.%s" % func_name)(*args)
                # print("调用的库："+HK_dll)
                # print("执行成功,返回值："+str(value))
                return value
            except:
                continue
        except:
            # print("库文件载入失败："+HK_dll)
            continue
    # print("没有找到接口！")
    return False


# region 登入
# 定义登入结构体
class LPNET_DVR_DEVICEINFO_V30(ctypes.Structure):
    _fields_ = [
        ("sSerialNumber", ctypes.c_byte * 48),
        ("byAlarmInPortNum", ctypes.c_byte),
        ("byAlarmOutPortNum", ctypes.c_byte),
        ("byDiskNum", ctypes.c_byte),
        ("byDVRType", ctypes.c_byte),
        ("byChanNum", ctypes.c_byte),
        ("byStartChan", ctypes.c_byte),
        ("byAudioChanNum", ctypes.c_byte),
        ("byIPChanNum", ctypes.c_byte),
        ("byZeroChanNum", ctypes.c_byte),
        ("byMainProto", ctypes.c_byte),
        ("bySubProto", ctypes.c_byte),
        ("bySupport", ctypes.c_byte),
        ("bySupport1", ctypes.c_byte),
        ("bySupport2", ctypes.c_byte),
        ("wDevType", ctypes.c_uint16),
        ("bySupport3", ctypes.c_byte),
        ("byMultiStreamProto", ctypes.c_byte),
        ("byStartDChan", ctypes.c_byte),
        ("byStartDTalkChan", ctypes.c_byte),
        ("byHighDChanNum", ctypes.c_byte),
        ("bySupport4", ctypes.c_byte),
        ("byLanguageType", ctypes.c_byte),
        ("byVoiceInChanNum", ctypes.c_byte),
        ("byStartVoiceInChanNo", ctypes.c_byte),
        ("byRes3", ctypes.c_byte * 2),
        ("byMirrorChanNum", ctypes.c_byte),
        ("wStartMirrorChanNo", ctypes.c_uint16),
        ("byRes2", ctypes.c_byte * 2)]


# 用户注册设备 并登入，需要修改IP,账号、密码
def NET_DVR_Login_V30(sDVRIP=ip, wDVRPort=port, sUserName=username, sPassword=password):
    init_res = callCpp("NET_DVR_Init")  # SDK初始化
    if init_res:
        print("SDK初始化成功")
        error_info = callCpp("NET_DVR_GetLastError")
    else:
        error_info = callCpp("NET_DVR_GetLastError")
        print("SDK初始化错误：" + str(error_info))
        return False

    set_overtime = callCpp("NET_DVR_SetConnectTime", 5000, 4)  # 设置超时
    if set_overtime:
        print("设置超时时间成功")
    else:
        error_info = callCpp("NET_DVR_GetLastError")
        print("设置超时错误信息：" + str(error_info))
        return False

    # 用户注册设备
    # c++传递进去的是byte型数据，需要转成byte型传进去，否则会乱码
    sDVRIP = bytes(sDVRIP, "ascii")
    sUserName = bytes(sUserName, "ascii")
    sPassword = bytes(sPassword, "ascii")
    print("数据转化成功")
    DeviceInfo = LPNET_DVR_DEVICEINFO_V30()
    print(DeviceInfo)
    lUserID = callCpp("NET_DVR_Login_V30", sDVRIP, wDVRPort, sUserName, sPassword, ctypes.byref(DeviceInfo))
    print("登录成功，用户ID：" + str(lUserID))
    if lUserID == -1:
        error_info = callCpp("NET_DVR_GetLastError")
        print("登录错误信息：" + str(error_info))
        return error_info
    else:
        return lUserID


# endregion

# region 预览
# 定义预览结构体
class NET_DVR_PREVIEWINFO(ctypes.Structure):
    _fields_ = [
        ("lChannel", ctypes.c_long),
        ("lLinkMode", ctypes.c_long),
        ("hPlayWnd", ctypes.c_void_p),
        ("sMultiCastIP", ctypes.c_char_p),
        ("byProtoType", ctypes.c_byte),
        ("byRes", ctypes.c_byte * 3)]


# 预览实现
def Preview():
    lpPreviewInfo = NET_DVR_PREVIEWINFO()
    # hPlayWnd需要输入创建图形窗口的handle,没有输入无法实现BMP抓图
    lpPreviewInfo.hPlayWnd = None
    lpPreviewInfo.lChannel = 1
    lpPreviewInfo.dwLinkMode = 0
    lpPreviewInfo.sMultiCastIP = None
    m_lRealHandle = callCpp("NET_DVR_RealPlay_V30", lUserID, ctypes.byref(lpPreviewInfo), None, None, True)
    if (m_lRealHandle < 0):
        error_info = callCpp("NET_DVR_GetLastError")
        print("预览失败：" + str(error_info))
    else:
        print("预览成功")
    return m_lRealHandle


# endregion


# # region 抓图
# # BMP抓图预览的时候hPlayWnd显示窗口不能为none
# def Get_BMPPicture():
#     sBmpPicFileName = bytes("pytest.bmp", "ascii")
#     if(callCpp("NET_DVR_CapturePicture",m_lRealHandle,sBmpPicFileName)==False):
#         error_info = callCpp("NET_DVR_GetLastError")
#         print("抓图失败：" + str(error_info))
#     else:
#         print("抓图成功")
#
# 抓图数据结构体
class NET_DVR_JPEGPARA(ctypes.Structure):
    _fields_ = [
        ("wPicSize", ctypes.c_ushort),
        ("wPicQuality", ctypes.c_ushort)]


# jpeg抓图hPlayWnd显示窗口能为none，存在缺点采集图片速度慢
def Get_JPEGpicture(savefile):
    sJpegPicFileName = bytes(savefile, "ascii")
    print("===sJpegPicFileName:", sJpegPicFileName)
    lpJpegPara = NET_DVR_JPEGPARA()    # 抓图数据 结构体
    lpJpegPara.wPicSize = 0
    lpJpegPara.wPicQuality = 0
    print(lpJpegPara)
    if (callCpp("NET_DVR_CaptureJPEGPicture", lUserID, lChannel, ctypes.byref(lpJpegPara), sJpegPicFileName) == False):
        error_info = callCpp("NET_DVR_GetLastError")
        print("抓图失败：" + str(error_info))
    else:
        print("抓图成功")


# endregion

# 定义光学变倍结构体

# 光学变倍结构体
class NET_DVR_FOCUSMODE_CFG(ctypes.Structure):
    _fields_ = [
        ("dwSize", ctypes.c_uint32),
        ("byFocusMode", ctypes.c_byte),
        ("byAutoFocusMode", ctypes.c_byte),
        ("wMinFocusDistance", ctypes.c_uint16),
        ("byZoomSpeedLevel", ctypes.c_byte),
        ("byFocusSpeedLevel", ctypes.c_byte),
        ("byOpticalZoom", ctypes.c_byte),
        ("byDigtitalZoom", ctypes.c_byte),
        ("fOpticalZoomLevel", ctypes.c_float),
        ("dwFocusPos", ctypes.c_uint32),
        ("byFocusDefinitionDisplay", ctypes.c_byte),
        ("byFocusSensitivity", ctypes.c_byte),
        ("byRes1", ctypes.c_byte * 2),
        ("dwRelativeFocusPos", ctypes.c_uint32),
        ("byRes", ctypes.c_byte * 48)]


# 获取光学变倍值
def get_CamZoom():
    m_struFocusModeCfg = NET_DVR_FOCUSMODE_CFG()
    m_struFocusModeCfg.byRes
    dwReturned = ctypes.c_uint16(0)
    print(callCpp("NET_DVR_GetDVRConfig"))
    if (callCpp("NET_DVR_GetDVRConfig", lUserID, 3305, lChannel, ctypes.byref(m_struFocusModeCfg), 76,
                ctypes.byref(dwReturned)) == False):
        error_info = callCpp("NET_DVR_GetLastError")
        print("光学变倍获取失败：" + str(error_info))
        ctypes.ARRAY()
    else:
        print("光学变倍获取成功")
    return m_struFocusModeCfg.fOpticalZoomLevel


# 修改光学变倍值
def Change_CamZoom(zoomScale):
    m_struFocusModeCfg = NET_DVR_FOCUSMODE_CFG()
    dwReturned = ctypes.c_uint16(0)
    print(callCpp("NET_DVR_GetDVRConfig"))
    if (callCpp("NET_DVR_GetDVRConfig", lUserID, 3305, lChannel, ctypes.byref(m_struFocusModeCfg), 76,
                ctypes.byref(dwReturned)) == False):
        error_info = callCpp("NET_DVR_GetLastError")
        print("光学变倍获取失败：" + str(error_info))
    else:
        print("光学变倍获取成功")
        print("当前光学变倍值：" + str(m_struFocusModeCfg.fOpticalZoomLevel))
        m_struFocusModeCfg.fOpticalZoomLevel = zoomScale
        if (callCpp("NET_DVR_SetDVRConfig", lUserID, 3306, lChannel, ctypes.byref(m_struFocusModeCfg), 76) == False):
            error_info = callCpp("NET_DVR_GetLastError")
            print("光学变倍修改失败：" + str(error_info))
        else:
            print("光学变倍修改成功;修改后的数据为：" + str(m_struFocusModeCfg.fOpticalZoomLevel))


# 透传接口输入参数结构体
class NET_DVR_XML_CONFIG_INPUT(ctypes.Structure):
    _fields_ = [
        ("dwSize", ctypes.c_uint32),
        ("lpRequestUrl", ctypes.c_void_p),
        ("dwRequestUrlLen", ctypes.c_uint32),
        ("lpInBuffer", ctypes.c_void_p),
        ("dwInBufferSize", ctypes.c_uint32),
        ("dwRecvTimeOut", ctypes.c_uint32),
        ("byForceEncrpt", ctypes.c_byte),
        ("byRes", ctypes.c_byte * 31), ]


# 透传接口输出参数结构体
class NET_DVR_XML_CONFIG_OUTPUT(ctypes.Structure):
    _fields_ = [
        ("dwSize", ctypes.c_uint32),
        ("lpOutBuffer", ctypes.c_void_p),
        ("dwOutBufferSize", ctypes.c_uint32),
        ("dwReturnedXMLSize", ctypes.c_uint32),
        ("lpStatusBuffer", ctypes.c_void_p),
        ("dwStatusSize", ctypes.c_uint32),
        ("byRes", ctypes.c_byte * 31)]


# 区域局部聚焦和局部曝光功能：矩形区域坐标左上角和右下角（startX,startY,endX,endY）
# flag=1局部聚焦功能，flag!=1局部曝光功能
def RegionalCorrection(startX, startY, endX, endY, flag=1):
    # #定义传输内容
    if (flag == 1):
        choise = "regionalFocus"
    else:
        choise = "regionalExposure"
    inUrl = "PUT /ISAPI/Image/channels/1/" + choise
    inPutBuffer = "<" + choise + "><StartPoint><positionX>" + str(startX) + "</positionX><positionY>" + str(
        startY) + "</positionY></StartPoint><EndPoint><positionX>" + str(endX) + "</positionX><positionY>" + str(
        endY) + "</positionY></EndPoint></" + choise + ">"

    szUrl = (ctypes.c_char * 256)()
    struInput = NET_DVR_XML_CONFIG_INPUT()
    struOuput = NET_DVR_XML_CONFIG_OUTPUT()
    struInput.dwSize = ctypes.sizeof(struInput)
    struOuput.dwSize = ctypes.sizeof(struOuput)
    dwBufferLen = 1024 * 1024
    pBuffer = (ctypes.c_char * dwBufferLen)()
    # _____________________________________________put________________________________________________________
    csCommand = bytes(inUrl, "ascii")
    ctypes.memmove(szUrl, csCommand, len(csCommand))
    struInput.lpRequestUrl = ctypes.cast(szUrl, ctypes.c_void_p)
    struInput.dwRequestUrlLen = len(szUrl)

    m_csInputParam = bytes(inPutBuffer, "ascii")
    dwInBufferLen = 1024 * 1024
    pInBuffer = (ctypes.c_byte * dwInBufferLen)()
    ctypes.memmove(pInBuffer, m_csInputParam, len(m_csInputParam))
    struInput.lpInBuffer = ctypes.cast(pInBuffer, ctypes.c_void_p)
    struInput.dwInBufferSize = len(m_csInputParam)

    struOuput.lpStatusBuffer = ctypes.cast(pBuffer, ctypes.c_void_p)
    struOuput.dwStatusSize = dwBufferLen

    if (callCpp("NET_DVR_STDXMLConfig", lUserID, ctypes.byref(struInput), ctypes.byref(struOuput))):
        error_info = callCpp("NET_DVR_GetLastError")
        print("上传成功：" + str(error_info))
    else:
        error_info = callCpp("NET_DVR_GetLastError")
        print("上传失败：错误号为" + str(error_info))


# 海康相机激活参数结构体
class NET_DVR_ACTIVATECFG(ctypes.Structure):
    _fields_ = [
        ("dwSize", ctypes.c_uint32),
        ("sPassword", ctypes.c_byte * 16),
        ("byRes", ctypes.c_byte * 108)]


# 海康相机激活
def OnActivateDevice():
    init_res = callCpp("NET_DVR_Init")  # SDK初始化
    if init_res:
        print("SDK初始化成功")
        error_info = callCpp("NET_DVR_GetLastError")
    else:
        error_info = callCpp("NET_DVR_GetLastError")
        print("SDK初始化错误：" + str(error_info))
        return False

    set_overtime = callCpp("NET_DVR_SetConnectTime", 5000, 4)  # 设置超时
    if set_overtime:
        print("设置超时时间成功")
    else:
        error_info = callCpp("NET_DVR_GetLastError")
        print("设置超时错误信息：" + str(error_info))
        return False

    szLan = (ctypes.c_char * 256)()
    pwd = bytes('guoji123', "ascii")  # 相机激活所需密码
    DevAddr = bytes('192.168.1.64', "ascii")  # 相机初始默认IP地址
    struActivateCfg = NET_DVR_ACTIVATECFG()
    struActivateCfg.dwSize = ctypes.sizeof(struActivateCfg)
    ctypes.memmove(struActivateCfg.sPassword, pwd, len(pwd))
    if (callCpp("NET_DVR_ActivateDevice", DevAddr, 8000, ctypes.byref(struActivateCfg))):
        error_info = callCpp("NET_DVR_GetLastError")
        print("激活成功：" + str(error_info))
    else:
        error_info = callCpp("NET_DVR_GetLastError")
        print("激活失败：" + str(error_info))


if __name__ == '__main__':
    # OnActivateDevice()#海康相机激活
    # 相机登入print(ctypes.sizeof(NET_DVR_FOCUSMODE_CFG))
    lUserID = NET_DVR_Login_V30()
    # 相机预览
    m_lRealHandle = Preview()
    # Get_JPEGpicture()
    # Change_CamZoom(1)

    # 区域局部聚焦和局部曝光功能：矩形区域坐标左上角和右下角（startX,startY,endX,endY）
    # flag=1局部聚焦功能，flag!=1局部曝光功能
    # RegionalCorrection(20, 20, 50, 50, flag=1)

    # 批量抓图
    for i in range(0, 5):
        savefile = "frame_" + str(i) + ".jpg"
        start = time.time()
        Get_JPEGpicture(savefile)
        print("耗时：", time.time() - start)
