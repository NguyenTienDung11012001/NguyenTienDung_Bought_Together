<template>
  <a
      :id="id"
      class="item"
      :class="{ active: isActive }"
      :href="path"
  >
    {{ imgSvg }}
    <span>{{ message }}</span>
  </a>
</template>

<script>
export default {
  props: {
    id: {
      type: String,
      required: true
    },
    imgSvg: {
      type: String,
      required: true
    },
    message: {
      type: String,
      default: 'Menu Title Here',
      required: true
    },
    isActive: {
      type: Boolean,
      required: true,
    },
    path: {
      type: String,
      default: '/',
      required: true,
    }
  },
}
</script>

<style scoped>
.item {
  display: flex;
  padding: 12px;
  align-items: center;
  gap: 12px;
  align-self: stretch;
}

.item:hover {
  border-radius: 12px;
  background: #ECECEC;
  cursor: pointer;
}

.item.active {
  border-radius: 12px;
  background: #ECECEC;
}

.item img {
  width: 24px;
  height: 24px;
}

.item span {
  color: #939393;
  font-family: Be Vietnam Pro;
  font-size: 14px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
}
</style>