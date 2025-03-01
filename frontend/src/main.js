import { createApp } from 'vue'
import { createStore } from 'vuex'
import App from './App.vue'

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import "@fortawesome/fontawesome-free/css/all.min.css";

const store = createStore({
  state() { },
  mutations: {}
})

import router from "./router";

var app = createApp(App)
app.use(router)
app.use(store)
app.mount('#app')
