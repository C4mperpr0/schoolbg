import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from datetime import datetime, timedelta
import time

from threading import Thread
class bThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

def ping(local_ip):
    command = ['ping', ('-n' if platform.system().lower()=='windows' else '-c'), '1', local_ip]
    return subprocess.call(command, shell=(platform.system().lower()=='windows')) == 0 # does shell=True always work to prevent window from opening? https://stackoverflow.com/questions/1813872/running-a-process-in-pythonw-with-popen-without-a-console 

def try_ip_range(ipString):
    ip = []
    insertLen = ipString.lower().count('x')
    for i in range(10**insertLen):
        cur_ip = ipString.lower()
        insert_ip = ' '*(insertLen-len(str(i))) + str(i)
        for n in str(insert_ip):
            cur_ip = cur_ip.replace('x', n, 1).replace(' ', '')

        ip.append(cur_ip)

    global r
    r = {'active': [], 'inactive': []}

    global iplist
    iplist = iter(ip)

    global wait_time
    wait_time = timedelta(seconds=6)
    global worker_count
    worker_count = 50 # pls not more than 50, 100 crashed hard
    global progress
    progress = 0

    def ip_check_worker(worker_id):
        global progress
        while 1:
            try:
                ip = next(iplist)
            except StopIteration:
                return 0
            if any([int(i) > 256 for i in ip.split('.')]):
                continue
            p = bThread(target=ping, args=(ip,))
            p.start()
            s = datetime.now()
            while 1:
                if p.is_alive() and ( wait_time > ( datetime.now()-s ) ):
                    time.sleep(0.5)
                else:
                    if ( wait_time < ( datetime.now()-s ) ):
                        ipstatus = p.join(0)
                        ipstatus = False
                    else:
                        ipstatus = p.join()
                    if ipstatus:
                        r['active'].append(ip)
                    else:
                        r['inactive'].append(ip)
                    progress += 1
                    break
    workers = []
    for i in range(worker_count):
        workers.append(Thread(target=ip_check_worker, args=(i,)))
        workers[-1].start()
    while 1:
        print(f'{int((progress*100)/len(ip))}% | {len(workers)} workers running...')
        for w in range(len(workers)):
            if not workers[w].is_alive():
                workers[w].join()
                workers.pop(w)
                break
            if w == 0:
                time.sleep(0.5)
        if len(workers) == 0:
            break

    return r

def ipscan(ipString):
    data = try_ip_range(ipString)
    print("Active IPs:")
    for i in data['active']:
        print(i)
    print(f"Inactive IPs: {len(data['inactive'])}")



















