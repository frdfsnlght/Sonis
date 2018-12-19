#!/usr/bin/python3

import eventlet
eventlet.monkey_patch()

import sys, os, signal, logging, argparse
from threading import Thread, Event

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sonis.config

config = sonis.config.load()

import sonis.logging

sonis.logging.configure()
logger = logging.getLogger('Server')

from sonis.bus import bus
import sonis.daemon as daemon
import sonis.wifi
import sonis.settings

from sonis.db import initializeDB, db
import sonis.core

from sonis.app import app
from sonis.socket import socket

webThread = None
exitEvent = Event()


def catchSIGTERM(signum, stackframe):
    logger.info('caught SIGTERM')
    exitEvent.set()
    
def catchSIGINT(signum, stackframe):
    logger.info('caught SIGINT')
    exitEvent.set()
    
def webThreadLoop():
    host = config.get('server', 'listenAddress')
    port = config.get('server', 'listenPort')
    logger.info('Web thread started on ' + host + ':' + port)
    socket.init_app(app, async_mode='eventlet')
    socket.run(
        app,
        host = host,
        port = port,
        debug = config.getboolean('server', 'socketIODebug'),
        use_reloader  = False
    )
    logger.info('Web thread stopped')

def startServer():
    logger.info('Server starting')
    
    initializeDB()

    signal.signal(signal.SIGTERM, catchSIGTERM)
    signal.signal(signal.SIGINT, catchSIGINT)

    bus.emit('server/start1')
    bus.emit('server/start2')
    
    # start threads
    
    webThread = Thread(target = webThreadLoop, name = 'WebThread')
    webThread.daemon = True
    webThread.start()

    logger.info('Server started')
    
    # wait for the end
    while not exitEvent.is_set():
        exitEvent.wait(1)
        bus.emit('server/tick')
        
    bus.emit('server/stop')
    
    db.close()
    
    logger.info('Server stopped')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Sonis server')
    parser.add_argument('cmd', choices = ['start', 'stop', 'restart', 'status', 'debug'],
                        help = 'the command to run')
    args = parser.parse_args()
    
    if args.cmd == 'start':
        daemon.start(startServer)
    elif args.cmd == 'stop':
        daemon.stop()
    elif args.cmd == 'restart':
        daemon.restart(startServer)
    elif args.cmd == 'status':
        daemon.status()
    elif args.cmd == 'debug':
        startServer()
    sys.exit(0)

        





