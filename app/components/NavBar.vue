<template>
  <div id="navbar">
    <div class="navbar-img">
      <img
          :src="imgSrc"
          alt="">
    </div>
  </div>


</template>

<script>
export default {
  props: {
    user_image: String,
  },
  data() {
    return {
      imgSrc: 'data:image/jpeg;base64,' + this.user_image,
    }
  },
}
</script>

<style scoped>
#navbar {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  position: fixed;
  width: 100%;
  height: 58px;
  flex-shrink: 0;
  background-color: #FFFFFF;
  z-index: 10;
}

#navbar .navbar-img {
  width: 34px;
  height: 34px;
  border-radius: 34px;
  margin-right: 25px;
  overflow: hidden;
}

#navbar .navbar-img img {
  width: 100%;
  height: 100%;
}
</style>