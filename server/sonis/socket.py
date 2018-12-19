
import functools, logging, re
from flask import request, session
from flask_socketio import SocketIO, emit

from .config import config
from .bus import bus
from . import core
from . import wifi
from . import settings


socket = SocketIO()
_logger = logging.getLogger('Socket')
_consoleSessionId = None


class ValidationError(Exception):
    pass
    
def success(d = None, **kwargs):
    out = {'error': False, **kwargs}
    if type(d) is dict:
        out = {**out, **d}
    return out

def error(msg):
    return {'error': str(msg)}

def socketEmit(*args, **kwargs):
    if not socket.server: return
    socket.emit(*args, **kwargs)

#--------------------------------
# decorators
#

def validate(rules):
    def wrap(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            if isinstance(args[0], dict):
                try:
                    validateParams(args[0], rules)
                    return f(*args, **kwargs)
                except ValidationError as e:
                    return error(e)
            else:
                return f(*args, **kwargs)
        return wrapped
    return wrap

#--------------------------------
# helpers
#

def validateParams(params, rules):
    for param, rule in rules.items():
        if param in params:
            if not isinstance(params[param], rule[0]):
                if params[param] is not None or (len(rule) > 1 and rule[1]):
                    raise ValidationError('{} is not of type {}'.format(param, str(rule[0])))
        else:
            if len(rule) == 1 or rule[1]:
                raise ValidationError('{} is required'.format(param))
    
#================================================================
# socket events
# These events represent the client-side API
#

#-------------------------------
# special
#
    
@socket.on_error_default  # handles all namespaces without an explicit error handler
def _socket_default_error_handler(e):
    _logger.exception(e)
    return error('An internal error has ocurred!')
    
@socket.on('connect')
def _socket_connect():
    global _consoleSessionId
    _logger.info('Connection opened from {}'.format(request.remote_addr))
    emit('settings', settings.export())
    emit('wifi_state', wifi.state)
    bus.emit('socket/connect', request)
    if request.remote_addr == '127.0.0.1':
        newConnect = _consoleSessionId != request.sid
        _consoleSessionId = request.sid
        if newConnect:
            bus.emit('socket/consoleConnect')

@socket.on('disconnect')
def _socket_disconnect():
    global _consoleSessionId
    _logger.info('Connection closed from {}'.format(request.remote_addr))
    bus.emit('socket/disconnect', request)
    if request.sid == _consoleSessionId:
        _consoleSessionId = None
        bus.emit('socket/consoleDisconnect')

#-------------------------------
# core
#

@socket.on('core_statistics')
def _socket_core_statistics():
    _logger.debug('recv core_statistics')
    return success(core.getStatistics())
    
@socket.on('core_restartX')
def _socket_core_restartX():
    _logger.debug('recv core_restartX')
    _logger.info('Client requested restart X')
    try:
        core.restartX()
        return success()
    except core.CoreError as e:
        return error(e)

@socket.on('core_restart')
def _socket_core_restart():
    _logger.debug('recv core_restart')
    _logger.info('Client requested restart')
    try:
        core.restart()
        return success()
    except core.CoreError as e:
        return error(e)

@socket.on('core_shutdown')
def _socket_core_shutdown():
    _logger.debug('recv core_shutdown')
    _logger.info('Client requested shutdown')
    try:
        core.shutdown()
        return success()
    except core.CoreError as e:
        return error(e)

#-------------------------------
# wifi
#
        
@socket.on('wifi_getNetworks')
def _socket_wifi_getNetworks():
    _logger.debug('recv wifi_getNetworks')
    return success(networks = wifi.getNetworks())
    
@socket.on('wifi_connectToNetwork')
def _socket_wifi_connectToNetwork(params):
    _logger.debug('recv wifi_connectToNetwork')
    wifi.connectToNetwork(params)
    return success()
    
@socket.on('wifi_disconnectFromNetwork')
def _socket_wifi_disconnectFromNetwork(ssid):
    _logger.debug('recv wifi_disconnectFromNetwork')
    wifi.disconnectFromNetwork(ssid)
    return success()
    
@socket.on('wifi_forgetNetwork')
def _socket_wifi_forgetNetwork(ssid):
    _logger.debug('recv wifi_forgetNetwork')
    wifi.forgetNetwork(ssid)
    return success()

#-------------------------------
# settings
#

@socket.on('settings_set')
@validate({
    'key': [str, True],
    'value': [(str, bool, int, float), True],
})
def socket_settings_set(params):
    _logger.debug('recv settings_set')
    try:
        settings.set(params['key'], params['value'])
        return success()
    except ValueError as e:
        return error(e)
        
    
    
#================================================================
# bus events
#
    
#-------------------------------
# misc
#
    
@bus.on('settings/loaded')
@bus.on('settings/changed')
def _but_settings_loaded():
    socketEmit('settings', settings.export())
    
#-------------------------------
# wifi
#

@bus.on('wifi/state')
def _bus_wifi_state(state):
    socketEmit('wifi_state', state)
    

