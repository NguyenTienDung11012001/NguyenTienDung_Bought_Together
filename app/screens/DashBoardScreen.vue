<template>
  <div id="dash-board">
    <SideBar :comp="activeComp"></SideBar>
    <NavBar :user_image="user_image"></NavBar>
    <div id="main">
      <component :is="activeComp"></component>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import SideBar from '../components/SideBar.vue';
import NavBar from '../components/NavBar.vue';
import Store from '../components/Store.vue';
import StoreSetting from '../components/StoreSetting.vue';
import Customization from '../components/Customization.vue';
import InstallationGuide from '../components/InstallationGuide.vue';

export default {
  components: {
    SideBar,
    NavBar,
    Store,
    StoreSetting,
    Customization,
    InstallationGuide,
  },
  data() {
    return {
      currentComponent: window.app_settings.name,
      user_name: window.app_settings.user_name,
      user_image: window.app_settings.user_image,
      curPath: window.location.pathname,
      activeComp: '',
    }
  },
  methods: {
    setComponent() {
      this.curPath = window.location.pathname
      switch (this.curPath) {
        case '/dashboard/customization':
          this.activeComp = "Customization"
          break
        case '/dashboard/installation-guide':
          this.activeComp = 'InstallationGuide'
          break
        case '/dashboard/store':
          this.activeComp = 'Store'
          break
        default:
          if (this.curPath.startsWith('/dashboard/store/')) {
            let store_name = this.curPath.substring('/dashboard/store/'.length);
            const stores = window.app_settings.stores
            const exists = stores.some(item => item.name === store_name);
            if (exists) {
              window.app_settings.store = store_name
              this.activeComp = 'StoreSetting'
            }
          }
      }
    }
  },
  created() {
    this.setComponent()
    window.addEventListener('click', () => {
      this.setComponent()
    });

    window.addEventListener('popstate', () => {
      this.setComponent()
    });
  },
  watch: {

  },
}
</script>

<style scoped>
#dash-board {
  width: 100%;
  min-height: 1003px;
  display: flex;
  flex-direction: row;
  background-color: #F4F4F4;
}

#dash-board #main {
  width: 100%;
  margin: 103px 25px 34px 301px;
}
</style>