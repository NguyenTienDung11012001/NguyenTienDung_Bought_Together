import {createApp, h} from 'vue/dist/vue.esm-bundler';
import ComboItemScreen from "./screens/ComboItemScreen.vue";
import 'ant-design-vue/dist/antd.css';
import Antd from "ant-design-vue";

var app = createApp({
    name: 'App',
    render: () => {
        return <ComboItemScreen/>
    }
})
app.use(Antd).mount('#app-storefront')

