<template>
  <div id="setting-comp" class="main-comp">
    <div class="setting-title">
      <span>Manual Recommendation</span>
      <div>
        <a @click="backBtn" class="btn">Back</a>
        <!-- Discard and save changes-->
        <div @click="discard++" class="btn">Discard</div>
        <div @click="save++" class="btn primary">Save</div>
      </div>
    </div>
    <div class="main-comp-body">
      <div class="setting-switch">
        <span>Enable Widget</span>
        <a-switch @click="changeStatus" v-model:checked="isEnable" checked-children="ON" un-checked-children="OFF"/>
      </div>
      <store-product :isWidgetEnable="isEnable" :data="dataRecommendTable" typeTable="recommendation" :discard="discard"
                     :save="save" widgetTitle="Choose recommendation product(s)"></store-product>
      <store-product :isWidgetEnable="isEnable" :data="dataExcludedTable" typeTable="excluded" :discard="discard"
                     :save="save" widgetTitle="Choose excluded product(s)"></store-product>
    </div>
  </div>
</template>

<script>
import StoreProduct from './StoreProduct.vue';
import axios from "axios";

export default {
  components: {
    StoreProduct,
  },
  data() {
    return {
      isEnable: false,
      dataRecommendTable: [],
      dataExcludedTable: [],
      discard: 0,
      save: 0,
    }
  },
  async created() {
    const url = 'https://odoo.website/oath2-ex/get-store-data'
    axios.post(url, {
      jsonrpc: "2.0",
      params: {
        "name": window.app_settings.store,
      },
    }).then(response => {
      this.isEnable = response.data.result.store_status
      this.dataRecommendTable = response.data.result.dataRecommendTable
      this.dataExcludedTable = response.data.result.dataExcludedTable
    })
  },
  methods: {
    async changeStatus() {
      const url = 'https://odoo.website/oath2-ex/change-store-status'
      await axios.post(url, {
        jsonrpc: "2.0",
        params: {
          store: window.app_settings.store,
          status: this.isEnable,
        },
      })
      this.$emit('changeStatus', this.isEnable)
    },
    backBtn() {
      history.back()
    }
  },
}
</script>

<style scoped>
.main-comp {
  position: relative;
}

.setting-switch {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.setting-switch span {
  color: #000;
  font-family: Inter, sans-serif;
  font-size: 18px;
  font-style: normal;
  font-weight: 600;
  line-height: 22px; /* 122.222% */
}
</style>