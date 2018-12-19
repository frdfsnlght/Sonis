import Vue from 'vue'
import Vuex from 'vuex'

import wifi from './modules/wifi'

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        wifi: wifi,
    },
    
    state: {
        connected: false,
        settings: {},
        error: false,
        notification: false,
        notificationColor: 'info',
        notificationTimeout: 4000,
        isConsole: location.hostname === 'localhost',
    },
    
    mutations: {
        socket_connect(state) {
            state.connected = true
        },
        socket_disconnect(state) {
            state.connected = false
        },
        
        socket_settings(state, settings) {
            state.settings = settings
            if (! settings.autoConsole) {
                if (settings.isConsole !== state.isConsole) {
                    state.isConsole = settings.isConsole
                    console.log('Client is now ' + (state.isConsole ? '' : 'NOT ') + 'running as console.')
                }
            }
        },
        
        setError(state, error) {
            state.error = error
        },
        
        clearError(state) {
            state.error = false
        },
        
        notify(state, options) {
            if (typeof(options) == 'string') {
                state.notification = options
                state.notificationColor = 'info'
                state.notificationTimeout = 4000
            } else if (options instanceof Object) {
                state.notification = options.text
                state.notificationColor = options.color ? options.color : 'info'
                state.notificationTimeout = options.timeout ? options.timeout : 4000
            }
        },
        
        clearNotification(state) {
            state.notification = false
        },
        
    },
    
    actions: {
        
    }
    
})
