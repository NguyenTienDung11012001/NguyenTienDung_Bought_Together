<template>
  <div id="store-comp" class="main-comp">
    <span class="title">WELCOME, {{ user_name }}</span>
    <div class="main-comp-body">
      <div class="main-comp-item">
        <div class="box-btns" v-show="isBtnsShow">
          <a-button @click="enableStores">Enable selected store(s)</a-button>
          <a-button @click="disableStores">Disable selected store(s)</a-button>
        </div>
        <a-table :columns="columns" :data-source="data" :row-selection="rowSelection" :pagination="false"
                 style="width: 100%;" size="small">
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'name'">
              <a @click="gotoStore(record.key)">{{ record.name }}</a>
            </template>
            <template v-else-if="column.key === 'status'">
              <a-switch @click="changeStatus(record.key, record.status)" v-model:checked="record.status" checked-children="ON" un-checked-children="OFF"/>
            </template>
          </template>
        </a-table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      user_name: window.app_settings.user_name,
      isBtnsShow: false,
      rows: [],
      rowSelection: {
        onSelect: this.onSelect,
        onSelectAll: this.onSelectAll,
      },
      columns: [
        {
          title: 'Store',
          width: '60%',
          dataIndex: 'name',
          key: 'name',

        },
        {
          title: 'Products Included',
          width: '157px',
          dataIndex: 'included',
          key: 'included',
        },
        {
          title: 'Status',
          width: '124px',
          dataIndex: 'status',
          key: 'status',
        },
      ],
      data: window.app_settings.stores,
    }
  },
  methods: {
    onSelect(record, selected, selectedRows) {
      if (selectedRows.length) {
        this.isBtnsShow = true
        this.rows = selectedRows.map(item => item.key)
      } else {
        this.isBtnsShow = false
        this.rows = []
      }
    },
    onSelectAll(selected, selectedRows, changeRows) {
      if (selected) {
        this.isBtnsShow = true
        this.rows = selectedRows.map(item => item.key)
      } else {
        this.isBtnsShow = false
        this.rows = []
      }
    },
    async changeStatus(store, status) {
      console.log(store, status)
      const url = 'https://odoo.website/oath2-ex/change-store-status'
      await axios.post(url, {
        jsonrpc: "2.0",
        params: {
          store: store,
          status: status,
        },
      })
    },
    enableStores() {
      this.rows.forEach(store => {
        this.changeStatus(store, true)
      })

      this.data.forEach(item => {
        if(this.rows.includes(item.key)){
          item.status = true
        }
      })
    },
    disableStores() {
      this.rows.forEach(store => {
        this.changeStatus(store, false)
      })

      this.data.forEach(item => {
        if(this.rows.includes(item.key)){
          item.status = false
        }
      })
    },
    gotoStore(store) {
      let url = '/dashboard/store/' + store
      history.pushState({}, '', url)
    },
  },
};
</script>

<style scoped>
.box-btns {
  display: flex;
  align-items: center;
  gap: 30px;
}

.box-btns button {
  border-radius: 6px;
  color: #1890FF;
}
</style>