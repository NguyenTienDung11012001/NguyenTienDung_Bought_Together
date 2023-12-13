<template>
  <div class="custom-right-box">
    <div class="right-box-main">
                        <span class="rb-main-title" :style="{ color: titleColor, fontSize: titleSize + 'px' }">
                            {{ titleText }}
                        </span>
      <span class="rb-main-des" :style="{ color: desColor, fontSize: desSize + 'px' }">
                            {{ desText }}
                        </span>
      <div class="right-box-cart">
        <div class="rb-cart-imgs">
          <div v-for="item in activeProducts" :key="item.key" class="rb-cart-image">
            <img :src="item.url" .alt="item.name">
          </div>
        </div>
        <div class="rb-cart-buy">
          <div class="rb-cart-price">
            <span>Total:</span>
            <span style="color: #FF0000;">${{ priceTotal }}</span>
            <span style="color: #848484; text-decoration: line-through;">${{ priceCompare }}</span>
          </div>
          <div class="rb-cart-btn"
               :style="{ color: btnColor, backgroundColor: btnBackground, borderColor: btnBorder }">
            {{ btnText }}
          </div>
        </div>
      </div>
    </div>
    <div class="right-box-products">
      <div v-for="item in data" :key="item.key">
        <a-checkbox v-model:checked="item.isActive">{{ item.name }}</a-checkbox>
        <span style="color: #FF0000;">${{ item.price }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['titleText', 'titleColor', 'titleSize',
    'desText', 'desColor', 'desSize',
    'btnText', 'btnColor', 'btnBackground', 'btnBorder',
    'data',
  ],
  computed: {
    activeProducts() {
      return this.data.filter(item => item.isActive)
    },
    priceTotal() {
      return this.getPrice('price')
    },
    priceCompare() {
      return this.getPrice('compare')
    },
  },
  methods: {
    getPrice(type) {
      let initialValue = 0
      return this.activeProducts.reduce(
          (acc, cur) => acc + cur[type],
          initialValue
      )
    },
  },
}
</script>

<style scoped>
.custom-right-box {
  display: flex;
  padding: 16px 20px;
  flex-direction: column;
  align-items: flex-start;
  gap: 16px;
  border-radius: 6px;
  border: 1px solid #E2E2E2;
  background: #FFF;
  width: 100%;
}

.right-box-main {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  width: 100%;
}

.rb-main-title {
  text-align: center;
  font-family: Inter;
  font-style: normal;
  font-weight: 700;
  line-height: 22px;
  /* 110% */
}

.rb-main-des {
  text-align: center;
  font-family: Inter;
  font-style: normal;
  font-weight: 400;
  line-height: 22px;
  /* 157.143% */
}

.right-box-cart {
  display: flex;
  align-items: center;
  width: 100%;
}

.rb-cart-imgs {
  flex-grow: 1;
  display: flex;
  flex-wrap: wrap;
}

.rb-cart-image {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.rb-cart-image:not(:first-child)::before {
  content: '+';
  color: #000;
  text-align: center;
  font-family: Inter;
  font-size: 13px;
  font-style: normal;
  font-weight: 600;
  width: 33px;
}

.rb-cart-image img {
  width: 61px;
  height: 61px;
  border-radius: 6px;
}

.rb-cart-buy {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px;
  width: 157px;
}

.rb-cart-price {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  gap: 6px;
  font-family: Inter;
  font-size: 16px;
  font-style: normal;
  font-weight: 600;
  line-height: 22px;
  /* 137.5% */
}

.rb-cart-btn {
  display: flex;
  width: 157px;
  padding: 4px 12px;
  justify-content: center;
  align-items: center;
  gap: 10px;
  border-radius: 6px;
  border: 1px solid;
  font-weight: 600;
  font-family: Inter;
}
</style>