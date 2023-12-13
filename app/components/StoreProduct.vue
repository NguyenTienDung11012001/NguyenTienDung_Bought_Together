<template>
  <div class="alert-box" :class="{show: isAlertShow}">You have reach the product limitation. Please remove any products
    from the list to continue selecting
  </div>
  <div class="main-comp-item">
    <div class="main-comp-header">
      <div class="main-comp-title">
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
        <span>{{ widgetTitle }} </span>
      </div>
      <div class="main-comp-search">
        <i class="fa-solid fa-magnifying-glass"></i>
        <a-auto-complete
            v-model:value="searchValue"
            :bordered="false"
            placeholder="Search product by name"
            @search="onSearch"
            @focus="onFocus"
            @blur="onBlur"
            size="large"
            class="input"
        />
        <div class="search-box" v-show="isSearching">
          <div class="search-box-item" v-for="item in dataSearchBox" :key="item.key" @click="addFromSearch(item)">
            <div>
              <img :src="item.url" alt="">
              <div>
                <span class="title"> {{ item.title }} </span>
                <span class="des">$ {{ item.price }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="selected"><span>{{ selectedProducts }} selected</span></div>
      </div>
    </div>
    <div @click="deleteProducts" v-show="isDeleteShow" class="remove-btn">Remove selected product(s)</div>
    <a-table :columns="columns"
             :data-source="dataTable"
             :row-selection="rowSelection"
             :pagination="false"
             style="width: 100%;" size="small"
             :rowClassName="!isWidgetEnable ? 'disabled-row' : ''">
      <template #headerCell="{ title }">
        <template v-if="title">
          <strong>{{ title }}</strong>
        </template>
      </template>
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'url'">
          <img :src="record.url" :alt="record.title" :style="!isWidgetEnable && 'opacity: 0.2'">
        </template>
        <template v-if="column.key === 'price'">
          ${{ record.price }}
        </template>
        <template v-if="column.key === 'compare'">
          ${{ record.compare }}
        </template>
      </template>
    </a-table>
  </div>
</template>

<script>
import axios from 'axios'
import _ from 'lodash'

export default {
  props: {
    isWidgetEnable: Boolean,
    widgetTitle: String,
    data: Object,
    typeTable: String,
    save: Number,
    discard: Number,
  },
  data() {
    return {
      isAlertShow: false,
      productLimit: 6,
      isSearching: false,
      searchValue: '',
      isDeleteShow: false,
      rows: [],
      selectedProducts: 0,
      rowSelection: {
        hideSelectAll: !this.isWidgetEnable,
        onChange: this.onChange,
      },
      columns: [
        {
          title: 'Image',
          dataIndex: 'url',
          key: 'url',
          width: '70px',
        },
        {
          title: 'Product Name',
          dataIndex: 'title',
          key: 'title',
          width: '40%',
        },
        {
          title: 'Price',
          dataIndex: 'price',
          key: 'price',
        },
        {
          title: 'Compare At Price',
          dataIndex: 'compare',
          key: 'compare',
        },
        {
          title: 'In Stock',
          dataIndex: 'stock',
          key: 'stock',
        },
      ],
      dataSearchBox: [],
      dataTable: this.data ? JSON.parse(JSON.stringify(this.data)) : [],
    }
  },
  methods: {
    async saveToDatabse(){
      const url = 'https://odoo.website/oath2-ex/save-product'
      await axios.post(url, {
        jsonrpc: "2.0",
        params: {
          "shop": window.app_settings.store,
          "data": this.dataTable,
          "type": this.typeTable,
        },
      }).then((response) => {
        console.log(response)
      }).catch((error) => {
        console.log(error)
      })
    },
    onSearch: _.debounce(function (searchText) {
      this.dataSearchBox = []
      this.searchProduct(searchText)
    }, 300),
    async searchProduct(searchText) {
      const url = 'https://odoo.website/oath2-ex/search-product'
      await axios.post(url, {
        jsonrpc: "2.0",
        params: {
          "keyword": searchText,
          "shop": window.app_settings.store
        },
      }).then((response) => {
        response.data.result.forEach(item => {
          let alternative_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Red_X.svg/2048px-Red_X.svg.png'
          let url = item.node.product.featuredImage ? item.node.product.featuredImage.url || alternative_url : alternative_url
          this.dataSearchBox.push({
            key: item.node.id,
            title: item.node.product.title,
            url: url,
            price: item.node.price,
            compare: item.node.compareAtPrice,
            quantity: item.node.inventoryQuantity
          })
        })
      }).catch((error) => {
        console.log(error)
      })
    },
    onFocus() {
      this.isSearching = true
      this.searchProduct()
    },
    onBlur() {
      setTimeout(() => {
        this.isSearching = false
        this.dataSearchBox = []
        this.searchValue = []
      }, 10);
    },
    addFromSearch(item) {
      if (this.dataTable.length < this.productLimit) {
        let isExist = this.dataTable.find(product => product.key === item.key);
        if (!isExist)
          this.dataTable.push(item)
      } else {
        if (!this.isAlertShow) {
          this.isAlertShow = true
          setTimeout(() => {
            this.isAlertShow = false
          }, 3000);
        }
      }
      this.isSearching = false
    },
    onChange(selectedRowKeys){
      console.log(selectedRowKeys)
      this.selectedProducts = selectedRowKeys.length
      if (selectedRowKeys.length) {
        this.isDeleteShow = true
        this.rows = selectedRowKeys
      } else {
        this.isDeleteShow = false
        this.rows = []
      }
    },
    deleteProducts() {
      this.dataTable = this.dataTable.filter(item => !this.rows.includes(item.key));
      this.isDeleteShow = false
      this.rows = []
      this.selectedProducts = 0
    },
  },
  watch: {
    data(){
      this.dataTable = this.data ? JSON.parse(JSON.stringify(this.data)) : []
    },
    isWidgetEnable() {
      this.rowSelection.hideSelectAll = !this.isWidgetEnable
    },
    save(){
      this.saveToDatabse()
    },
    discard(){
      this.dataTable = this.data ? JSON.parse(JSON.stringify(this.data)) : []
    },
  },
};
</script>

<style scoped>
.alert-box {
  position: fixed;
  left: calc(50% + 138px);
  top: 0;
  transform: translate(-50%, -100%);
  transition: all 0.2s ease-out;
  border: 1px solid #EB1F1F;
  background: #F4E3E3;
  padding: 6px 12px;
  justify-content: center;
  align-items: center;
  color: #EB1F1F;
  font-family: Inter, sans-serif;
  font-size: 10px;
  font-style: normal;
  font-weight: 500;
  line-height: 20px; /* 200% */
  display: inline-flex;
  visibility: hidden;
}

.alert-box.show {
  top: 100px;
  visibility: visible;
}

img {
  width: 33px;
}

.main-comp-header {
  display: flex;
  height: 80px;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
  align-self: stretch;
}

.main-comp-title {
  display: flex;
  width: 682px;
  align-items: center;
  gap: 10px;
}

.main-comp-title span {
  color: #202223;
  font-feature-settings: 'clig' off, 'liga' off;
  font-family: Inter, sans-serif;
  font-size: 18px;
  font-style: normal;
  font-weight: 500;
  line-height: 28px;
  /* 155.556% */
}

.main-comp-search {
  display: flex;
  position: relative;
  width: 100%;
}

.main-comp-search .input {
  display: flex;
  align-items: center;
  padding-left: 32px;
  border: 1px solid #E6E6E6;
  border-radius: 6px 0 0 6px;
  width: 100%;
}

.search-box {
  position: absolute;
  left: 0;
  top: 44px;
  width: calc(100% - 120px);
  display: flex;
  padding: 8px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 4px;
  border-radius: 0 0 6px 6px;
  border: 1px solid #D1D1D1;
  background-color: #fff;
  z-index: 10;
}

.search-box-item {
  display: flex;
  padding: 12px 16px;
  align-items: center;
  gap: 16px;
  align-self: stretch;
  border-radius: 8px;
  background: var(--background-color);
}

.search-box-item > div {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  flex: 1 0 0;
}

.search-box-item:hover {
  cursor: pointer;
  background: #E9F6FF;
}

.search-box-item img {
  width: 44px;
  height: 44px;
  border-radius: 4px;
}

.search-box-item > div > div {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
  flex: 1 0 0;
}

.search-box-item .title {
  align-self: stretch;
  color: #1C1C1E;
  line-height: 20px;
}

.search-box .des {
  align-self: stretch;
  color: #636366;
  font-size: 12px;
  font-weight: 400;
  line-height: 18px;
}

.main-comp-search i {
  position: absolute;
  top: 14px;
  left: 12px;
  opacity: 0.3;
  z-index: 1;
}

.main-comp-search .selected {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 120px;
  height: 44px;
  border-radius: 0 6px 6px 0;
  border-top: 1px solid #E6E6E6;
  border-right: 1px solid #E6E6E6;
  border-bottom: 1px solid #E6E6E6;
}

.main-comp-search span {
  font-family: Inter, sans-serif;
  font-size: 14px;
  line-height: 22px;
  /* 157.143% */
}

.remove-btn {
  color: red;
  user-select: none;
}

.remove-btn:hover {
  cursor: pointer;
  text-decoration: underline;
}
</style>