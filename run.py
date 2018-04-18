import config
from qqbot import QQBotSlot as qqbotslot,RunBot
import ASF_IPC as asf

ipc_address = 'http://192.168.1.224/'
ipc_password = 'wanglz970915'
api = asf.IPC(ipc_address, ipc_password)

type = []
config.create_conf()


def send(command):
    try:
        res = api.command(command)
    except Exception as e:
        if hasattr(e, 'message'):
            res = e.message
        else:
            res = e.__class__.__name__
    if not isinstance(res, str):
        res = str(res)
    return res



@qqbotslot
def onQQMessage(bot, contact, member, content):
    if bot.isMe(contact, member):
        pass


def onQQMessage(bot, contact, member, content):

    if content:
        res = send(content)
        bot.SendTo(contact, res)
    elif content == 'botstop':
        bot.Stop()




if __name__ == '__main__':
    RunBot()