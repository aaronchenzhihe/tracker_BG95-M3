from usr import Qth
import _thread
import dataCall
import utime
import log

logApp = log.getLogger("examp")

def App_devEventCb(event, result):
    logApp.info('dev event:{} result:{}'.format(event, result))
    if(2== event and 0 == result):
        Qth.otaRequest()

def App_cmdRecvTransCb(value):
    ret = Qth.sendTrans(1, value)
    logApp.info('recvTrans value:{} ret:{}'.format(value, ret))

def App_cmdRecvTslCb(value):
    logApp.info('recvTsl:{}'.format(value))
    for cmdId, val in value.items():
        logApp.info('recvTsl {}:{}'.format(cmdId, val))
def App_cmdReadTslCb(ids, pkgId):
    logApp.info('readTsl ids:{} pkgId:{}'.format(ids, pkgId))
    value=dict()
    for id in ids:
        if 1 == id:
            value[1]=180.25
        elif 2 == id:
            value[2]=30
        elif 3 == id:
            value[3]=True
    Qth.ackTsl(1, value, pkgId)

def App_cmdRecvTslServerCb(serverId, value, pkgId):
    logApp.info('recvTslServer serverId:{} value:{} pkgId:{}'.format(serverId, value, pkgId))
    Qth.ackTslServer(1, serverId, value, pkgId)

def App_otaPlanCb(plans):
    logApp.info('otaPlan:{}'.format(plans))
    Qth.otaAction(1)

def App_fotaResultCb(comp_no, result):
    logApp.info('fotaResult comp_no:{} result:{}'.format(comp_no, result))
    
def App_sotaInfoCb(comp_no, version, url,fileSize, md5, crc):   # fileSize是可选参数
    logApp.info('sotaInfo comp_no:{} version:{} url:{} fileSize:{} md5:{} crc:{}'.format(comp_no, version, url,fileSize, md5, crc))
    # 当使用url下载固件完成，且MCU更新完毕后，需要获取MCU最新的版本信息，并通过setMcuVer进行更新
    Qth.setMcuVer('MCU1', 'V1.0.0', App_sotaInfoCb, App_sotaResultCb)

def App_sotaResultCb(comp_no, result):
    logApp.info('sotaResult comp_no:{} result:{}'.format(comp_no, result))

def Qth_tslSend():
    static_var = 0
    while True:       
        # 先判断连接云平台状态
        if Qth.state():
            Qth.sendTsl(1, {1: static_var})   #用户任务，每30秒上报精油剩余容量     
            static_var+=1
        utime.sleep(30)

if __name__ == '__main__':
    dataCall.setAutoActivate(1, 1)
    dataCall.setAutoConnect(1, 1)
    Qth.init()
    Qth.setProductInfo('p11pUv','MUYxbkpuWkVuR0Zz')

    eventOtaCb={
            'otaPlan':App_otaPlanCb,
            'fotaResult':App_fotaResultCb
            }
    eventCb={
        'devEvent':App_devEventCb, 
        'recvTrans':App_cmdRecvTransCb, 
        'recvTsl':App_cmdRecvTslCb, 
        'readTsl':App_cmdReadTslCb, 
        'readTslServer':App_cmdRecvTslServerCb,
        'ota':eventOtaCb
        }
    Qth.setEventCb(eventCb)
    Qth.setAppVer('V1.0.1', App_sotaResultCb)
    Qth.setMcuVer('MCU1', 'V1.1', App_sotaInfoCb, App_sotaResultCb)
    Qth.setMcuVer('MCU2', 'V2.1', App_sotaInfoCb, App_sotaResultCb)
    Qth.start()
    #pid = _thread.start_new_thread(Qth_tslSend, ())
    #logApp.info('Qth_tslSend thread:{} start'.format(pid))