import os


def create_conf():
    usrp = os.path.expanduser('~')
    if os.path.exists(usrp + '/.qqbot-tmp'):
        pass
    else:
        os.makedirs(usrp + '/.qqbot-tmp')

    g = open(usrp + '/.qqbot-tmp/v2.3.conf', 'w')
    f = open('conf.txt', 'r')
    g.write(f.read())