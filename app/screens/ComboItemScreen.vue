<template>
  <div id="bt-combo-item-box">
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
</template>

<script>
import axios from 'axios'
import ComboItem from '../components/ComboItem.vue';

export default {
  components: {ComboItem},
  data() {
    return {
      titleText: 'Run ngrok',
      titleColor: '#000000',
      titleSize: '26px',
      desText: 'App setup -> App proxy -> change proxy URL',
      desColor: '#000000',
      desSize: '20px',
      btnText: '',
      btnColor: '',
      btnBackground: '',
      btnBorder: '',
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
    console.log('heeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
    const urlGet = 'https://dungtien111.myshopify.com/apps/bt/oath2-ex/get-customization'
    await axios.post(urlGet, {
      jsonrpc: "2.0",
      params: {
        shop: 'dungtien111',
      },
    }).then(res => {
      let data = JSON.parse(res.data.result)
      console.log(data)
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


    const url = window.location.origin + window.location.pathname + '.js'
    await axios.get(url).then(res => {
      let exist = this.data.find(item => {
        return item.key == res.data.id
      })
      if (!exist) {
        this.data[0] = {
          key: res.data.id,
          name: res.data.title,
          url: res.data.featured_image || res.data.images[0],
          price: res.data.price,
          compare: res.data.compare_at_price,
          isActive: true,
        }
      }
    })
  }
}
</script>

<style scoped>
#bt-combo-item-box {
  width: 50%;
  margin: 0 auto;
}
</style>