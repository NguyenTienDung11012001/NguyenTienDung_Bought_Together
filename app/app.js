import {createApp, h} from 'vue/dist/vue.esm-bundler';
import App from './App.vue'
import 'ant-design-vue/dist/antd.css';
import './main.css'
import Antd from 'ant-design-vue';

import DashBoardScreen from "./screens/DashBoardScreen.vue";

var app = createApp({
    name: 'App',
    render: () => {
        return <App/>
    }
})
app.use(Antd).mount('#app')



