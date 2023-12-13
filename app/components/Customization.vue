<template>
  <div id="setting-comp" class="main-comp">
    <div class="setting-title">
      <span>Customization</span>
      <div>
        <div class="btn">Discard</div>
        <div class="btn primary" @click="save">Save</div>
      </div>
    </div>
    <div class="custom-main">
      <div class="custom-main-left">
        <div class="custom-left-box">
          <div class="custom-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none">
              <g clip-path="url(#clip0_3_7364)">
                <path fill-rule="evenodd" clip-rule="evenodd"
                      d="M0 6C0 2.6865 2.6865 0 6 0C9.3135 0 12 2.6865 12 6C12 9.3135 9.3135 12 6 12C2.6865 12 0 9.3135 0 6ZM6.67501 7.20115H5.39337V7.11654C5.39992 5.93719 5.68836 5.76447 6.21774 5.44746C6.27369 5.41396 6.33232 5.37885 6.3936 5.34077C6.83188 5.06548 7.16874 4.71775 7.16874 4.21065C7.16874 3.64197 6.72322 3.27251 6.16903 3.27251C5.6583 3.27251 5.1748 3.51123 5.1422 4.1922H3.78223C3.81845 2.81578 4.90852 2.1 6.17627 2.1C7.55994 2.1 8.51256 2.96825 8.51256 4.19254C8.51256 5.02202 8.09601 5.56534 7.42954 5.96378C7.37879 5.99491 7.33125 6.02353 7.28673 6.05034C6.81326 6.33539 6.68163 6.41464 6.67501 7.11654V7.20115ZM6.77747 9.00841C6.77384 9.45031 6.40801 9.80528 5.98059 9.80528C5.53869 9.80528 5.18009 9.45031 5.18372 9.00841C5.18009 8.57375 5.53869 8.21877 5.98059 8.21877C6.40801 8.21877 6.77384 8.57375 6.77747 9.00841Z"
                      fill="#5C5F62"/>
              </g>
              <defs>
                <clipPath id="clip0_3_7364">
                  <rect width="12" height="12" fill="white"/>
                </clipPath>
              </defs>
            </svg>
            <span>General Configuration</span>
          </div>
          <div class="custom-control">
            <div class="custom-control-input">
              <span>Widget Title</span>
              <a-input v-model:value="titleText"/>
            </div>
            <div class="custom-control-2col">
              <div class="custom-control-color">
                <span>Title color</span>
                <div>
                  <input type="color" v-model="titleColor">
                  {{ titleColor }}
                </div>
              </div>
              <div class="custom-control-number">
                <span>Title font size (px)</span>
                <a-input-number id="inputNumber" v-model:value="titleSize" :min="18" :max="38"/>
              </div>
            </div>
          </div>
          <div class="custom-control">
            <div class="custom-control-input">
              <span>Widget description</span>
              <a-input v-model:value="desText"/>
            </div>
            <div class="custom-control-2col">
              <div class="custom-control-color">
                <span>Description color</span>
                <div>
                  <input type="color" v-model="desColor">
                  {{ desColor }}
                </div>
              </div>
              <div class="custom-control-number">
                <span>Description font size (px)</span>
                <a-input-number id="inputNumber" v-model:value="desSize" :min="12" :max="32"/>
              </div>
            </div>
          </div>
        </div>
        <div class="custom-left-box">
          <div class="custom-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none">
              <g clip-path="url(#clip0_3_7364)">
                <path fill-rule="evenodd" clip-rule="evenodd"
                      d="M0 6C0 2.6865 2.6865 0 6 0C9.3135 0 12 2.6865 12 6C12 9.3135 9.3135 12 6 12C2.6865 12 0 9.3135 0 6ZM6.67501 7.20115H5.39337V7.11654C5.39992 5.93719 5.68836 5.76447 6.21774 5.44746C6.27369 5.41396 6.33232 5.37885 6.3936 5.34077C6.83188 5.06548 7.16874 4.71775 7.16874 4.21065C7.16874 3.64197 6.72322 3.27251 6.16903 3.27251C5.6583 3.27251 5.1748 3.51123 5.1422 4.1922H3.78223C3.81845 2.81578 4.90852 2.1 6.17627 2.1C7.55994 2.1 8.51256 2.96825 8.51256 4.19254C8.51256 5.02202 8.09601 5.56534 7.42954 5.96378C7.37879 5.99491 7.33125 6.02353 7.28673 6.05034C6.81326 6.33539 6.68163 6.41464 6.67501 7.11654V7.20115ZM6.77747 9.00841C6.77384 9.45031 6.40801 9.80528 5.98059 9.80528C5.53869 9.80528 5.18009 9.45031 5.18372 9.00841C5.18009 8.57375 5.53869 8.21877 5.98059 8.21877C6.40801 8.21877 6.77384 8.57375 6.77747 9.00841Z"
                      fill="#5C5F62"/>
              </g>
              <defs>
                <clipPath id="clip0_3_7364">
                  <rect width="12" height="12" fill="white"/>
                </clipPath>
              </defs>
            </svg>
            <span>Button Configuration</span>
          </div>
          <div class="custom-control">
            <div class="custom-control-input">
              <span>Button text</span>
              <a-input v-model:value="btnText"/>
            </div>
            <div class="custom-control-2col">
              <div class="custom-control-color">
                <span>Button text color</span>
                <div>
                  <input type="color" v-model="btnColor">
                  {{ btnColor }}
                </div>
              </div>
              <div class="custom-control-color">
                <span>Button background color (px)</span>
                <div>
                  <input type="color" v-model="btnBackground">
                  {{ btnBackground }}
                </div>
              </div>
            </div>
            <div class="custom-control-color-l">
              <span>Button border color</span>
              <div>
                <input type="color" v-model="btnBorder">
                {{ btnBorder }}
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="custom-main-right">
        <div class="custom-title">
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none">
            <g clip-path="url(#clip0_3_7364)">
              <path fill-rule="evenodd" clip-rule="evenodd"
                    d="M0 6C0 2.6865 2.6865 0 6 0C9.3135 0 12 2.6865 12 6C12 9.3135 9.3135 12 6 12C2.6865 12 0 9.3135 0 6ZM6.67501 7.20115H5.39337V7.11654C5.39992 5.93719 5.68836 5.76447 6.21774 5.44746C6.27369 5.41396 6.33232 5.37885 6.3936 5.34077C6.83188 5.06548 7.16874 4.71775 7.16874 4.21065C7.16874 3.64197 6.72322 3.27251 6.16903 3.27251C5.6583 3.27251 5.1748 3.51123 5.1422 4.1922H3.78223C3.81845 2.81578 4.90852 2.1 6.17627 2.1C7.55994 2.1 8.51256 2.96825 8.51256 4.19254C8.51256 5.02202 8.09601 5.56534 7.42954 5.96378C7.37879 5.99491 7.33125 6.02353 7.28673 6.05034C6.81326 6.33539 6.68163 6.41464 6.67501 7.11654V7.20115ZM6.77747 9.00841C6.77384 9.45031 6.40801 9.80528 5.98059 9.80528C5.53869 9.80528 5.18009 9.45031 5.18372 9.00841C5.18009 8.57375 5.53869 8.21877 5.98059 8.21877C6.40801 8.21877 6.77384 8.57375 6.77747 9.00841Z"
                    fill="#5C5F62"/>
            </g>
            <defs>
              <clipPath id="clip0_3_7364">
                <rect width="12" height="12" fill="white"/>
              </clipPath>
            </defs>
          </svg>
          <span>Preview</span>
        </div>
        <ComboItem :titleText="titleText"
                   :titleColor="titleColor"
                   :titleSize="titleSize"
                   :desText="desText"
                   :desColor="desColor"
                   :desSize="desSize"
                   :btnText="btnText"
                   :btnColor="btnColor"
                   :btnBackground="btnBackground"
                   :btnBorder="btnBorder"
                   :data="data"/>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import ComboItem from './ComboItem.vue';

export default {
  components: {ComboItem},
  data() {
    return {
      titleText: 'You may also like...',
      titleColor: '#000000',
      titleSize: '20',
      desText: 'Good deals only for you!',
      desColor: '#000000',
      desSize: '14',
      btnText: 'Buy now',
      btnColor: '#FFFFFF',
      btnBackground: '#1890FF',
      btnBorder: '#1890FF',
      data: [
        {
          key: '8107909349601',
          name: "The Multi-location Snowboard",
          url: "//cdn.shopify.com/s/files/1/0670/1603/2481/products/Main_0a4e9096-021a-4c1e-8750-24b233166a12.jpg?v=1697006079",
          price: 73000,
          compare: 100000,
          isActive: true,
        },
        {
          key: '8107909415137',
          name: "The Multi-managed Snowboard",
          url: "//cdn.shopify.com/s/files/1/0670/1603/2481/products/Main_9129b69a-0c7b-4f66-b6cf-c4222f18028a.jpg?v=1697006079",
          price: 63000,
          compare: 100000,
          isActive: true,
        },
        {
          key: '8107909054689',
          name: "The Collection Snowboard: Hydrogen",
          url: "//cdn.shopify.com/s/files/1/0670/1603/2481/products/Main_0a40b01b-5021-48c1-80d1-aa8ab4876d3d.jpg?v=1697006078",
          price: 60000,
          compare: 100000,
          isActive: true,
        },
      ],
    }
  },
  async mounted() {
    const url = 'https://odoo.website/oath2-ex/get-customization'
    await axios.post(url, {
      jsonrpc: "2.0",
      params: {
        shop: 'dungtien111',
      },
    }).then(res => {
      let data = JSON.parse(res.data.result)
      this.titleText = data.titleText
      this.titleColor = data.titleColor
      this.titleSize = data.titleSize
      this.desText = data.desText
      this.desColor = data.desColor
      this.desSize = data.desSize
      this.btnText = data.btnText
      this.btnColor = data.btnColor
      this.btnBackground = data.btnBackground
      this.btnBorder = data.btnBorder
    })
  },
  methods: {
    async save() {
      let data = {
        'titleText': this.titleText,
        'titleColor': this.titleColor,
        'titleSize': this.titleSize,
        'desText': this.desText,
        'desColor': this.desColor,
        'desSize': this.desSize,
        'btnText': this.btnText,
        'btnColor': this.btnColor,
        'btnBackground': this.btnBackground,
        'btnBorder': this.btnBorder,
      }
      const url = 'https://odoo.website/oath2-ex/save-customization'
      await axios.post(url, {
        jsonrpc: "2.0",
        params: {
          shop: 'dungtien111',
          data: JSON.stringify(data),
        },
      })
    }
  },
}
</script>

<style scoped>
.custom-main {
  display: flex;
  width: 100%;
  padding: 16px 22px;
  align-items: flex-start;
  gap: 30px;
  border: 1px solid #E2E2E2;
  background: #FFF;
}

.custom-main-left,
.custom-main-right {
  width: 50%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;

}

.custom-main-left {
  gap: 30px;
  flex: 1 0 0;
  border-right: 1px solid #BFBFBF;
  padding: 16px 30px 16px 22px;
}

.custom-left-box {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 24px;
  align-self: stretch;
}

.custom-title {
  display: flex;
  height: 28px;
  align-items: center;
  gap: 10px;
  align-self: stretch;
}

.custom-title > span {
  color: #202223;
  font-feature-settings: 'clig' off, 'liga' off;
  font-family: Inter, sans-serif;
  font-size: 18px;
  font-style: normal;
  font-weight: 500;
  line-height: 28px;
  /* 155.556% */
}

.custom-control {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 12px;
  align-self: stretch;
}

.custom-control-input {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
  align-self: stretch;
}

.custom-control-input > span {
  color: #1C1C1E;
  font-family: Inter, sans-serif;
  font-size: 16px;
  font-style: normal;
  font-weight: 600;
  line-height: 22px;
  /* 137.5% */
}

.custom-control-2col {
  display: flex;
  align-items: center;
  gap: 16px;
  align-self: stretch;
}

.custom-control-2col > div {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  flex: 1 0 0;
}

.custom-control-color-l {
  display: flex;
  flex-direction: column;
}

.custom-control-number,
.custom-control-color,
.custom-control-color-l {
  color: #1C1C1E;
  font-family: Inter, sans-serif;
  font-size: 12px;
  font-style: normal;
  font-weight: 500;
  line-height: 22px;
  /* 183.333% */
  width: 100%;
}

.custom-control-number > div,
.custom-control-color > div,
.custom-control-color-l > div {
  width: 100%;
  border: 1px solid #939393;
  border-radius: 6px;
  height: 38px;
  display: flex;
  flex-direction: row;
  padding: 8px 12px 10px 8px;
  align-items: center;
  gap: 10px;
  align-self: stretch;
  justify-content: flex-start;
}

.custom-main-right {
  gap: 24px;
  padding: 16px 22px 16px 30px;
}
</style>