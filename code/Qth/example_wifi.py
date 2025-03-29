import network
import log
from usr import qth_init
from usr import qth_config
from usr import qth_bus
logApp = log.getLogger("examp")
def App_devEventCb(event, result):
    logApp.info('dev event:{} result:{}'.format(event, result))

def App_cmdRecvTransCb(value):
    ret = qth_bus.sendTrans(1, value)
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
    qth_bus.ackTsl(1, value, pkgId)

def App_cmdRecvTslServerCb(serverId, value, pkgId):
    logApp.info('recvTslServer serverId:{} value:{} pkgId:{}'.format(serverId, value, pkgId))
    qth_bus.ackTslServer(1, serverId, value, pkgId)

def App_otaPlanCb(plans):
    logApp.info('otaPlan:{}'.format(plans))

def App_fotaResultCb(comp_no, result):
    logApp.info('fotaResult comp_no:{} result:{}'.format(comp_no, result))
    
def App_sotaInfoCb(comp_no, version, url,fileSize, md5, crc):   # fileSize是可选参数
    logApp.info('sotaInfo comp_no:{} version:{} url:{} fileSize:{} md5:{} crc:{}'.format(comp_no, version, url,fileSize, md5, crc))
    # 当使用url下载固件完成，且MCU更新完毕后，需要获取MCU最新的版本信息，并通过setMcuVer进行更新

def App_sotaResultCb(comp_no, result):
    logApp.info('sotaResult comp_no:{} result:{}'.format(comp_no, result))

if __name__ == '__main__':
    nic = network.WLAN(network.STA_MODE)
    nic.connect(ssid="JC",password="cyf7fufhcy")
    qth_init.init()
    qth_config.setProductInfo('p11pUv','MUYxbkpuWkVuR0Zz')

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
    qth_config.setEventCb(eventCb)

    qth_init.start()