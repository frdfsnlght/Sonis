
import logging, os, time, subprocess

from .bus import bus
from .config import config


_logger = logging.getLogger('Core')


class CoreError(Exception):
    pass

def getStatistics():
    stats = {
    }
    
    cmd = config.get('core', 'diskFreeCommand').split(' ')
    cmd = [p if p != '{}' else config.getpath('core', 'diskFreePath') for p in cmd]
    out = subprocess.run(cmd,
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT,
            universal_newlines = True)
    if out.returncode != 0:
        _logger.error('Error trying to get disk free: {}'.format(out.stdout))
    lines = out.stdout.splitlines()
    stats['diskFree'] = float(lines[-1].strip().replace('%', ''))
    
    return stats
            
def restartX():
    cmd = config.get('core', 'restartXCommand').split(' ')
    out = subprocess.run(cmd,
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT,
            universal_newlines = True)
    if out.returncode != 0:
        _logger.error('Error trying to restart X: {}'.format(out.stdout))
        
def restart():
    cmd = config.get('core', 'restartCommand').split(' ')
    out = subprocess.run(cmd,
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT,
            universal_newlines = True)
    if out.returncode != 0:
        _logger.error('Error trying to restart: {}'.format(out.stdout))
        
def shutdown():
    cmd = config.get('core', 'shutdownCommand').split(' ')
    out = subprocess.run(cmd,
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT,
            universal_newlines = True)
    if out.returncode != 0:
        _logger.error('Error trying to shutdown: {}'.format(out.stdout))
    
