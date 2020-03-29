"use strict";

import Vue from 'vue';
import axios from "axios";
import store from '../store/index.js'

// Full config:  https://github.com/axios/axios#request-config
// axios.defaults.baseURL = process.env.baseURL || process.env.apiUrl || '';
// axios.defaults.headers.common['Authorization'] = AUTH_TOKEN;
// axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

let config = {
    // baseURL: process.env.baseURL || process.env.apiUrl || ""
    // timeout: 60 * 1000, // Timeout
    // withCredentials: true, // Check cross-site Access-Control
};

const _axios = axios.create(config);

_axios.interceptors.request.use(
    function (config) {
        // Do something before request is sent
        let admin = localStorage.getItem(window.location.host + '_admin');
        if (admin) {
            config.headers = { ...config.headers, 'x-hucat-token': JSON.parse(admin).token }
        }
        return config;
    },
    function (error) {
        // Do something with request error
        return Promise.reject(error);
    }
);

// Add a response interceptor
_axios.interceptors.response.use(
    function (response) {
        // Do something with response data
        // Handle unauth access action
        if (response.data.rc === 10000 || response.data.rc === 10001) {
            store.commit('showSnackbar', { color: 'error', message: response.data.msg });
            if (window.location.pathname !== '/login') {
                window.location.href = '/login';
            }
        } else if (response.data.rc != 0) { // Handle server error
            store.commit('showSnackbar', { color: 'error', message: response.data.msg });
        }
        return response;
    },
    function (error) {
        // Do something with response error
        store.commit('showSnackbar', { color: 'error', message: error.message });
        return Promise.reject(error);
    }
);

Plugin.install = function (Vue) {
    Vue.axios = _axios;
    window.axios = _axios;
    Object.defineProperties(Vue.prototype, {
        axios: {
            get() {
                return _axios;
            }
        },
        $axios: {
            get() {
                return _axios;
            }
        },
    });
};

Vue.use(Plugin);

export default Plugin;

// eslint-disable-next-line no-console
// console.log(Vue.axios)
