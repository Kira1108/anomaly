<template>
  <div class="home">
    <header>
      <div class="logo ">
        <!-- <img src="../assets/images/logo.png" alt=""> -->
        <h2>人工智能不法信息识别系统</h2>
      </div>
      <div class="time_worp">
        <img src="../assets/images/data_icon.png" class="data_icon" alt="">
        <p>{{timeTxt}}</p>
        <div class="division"></div>
        <p>{{week}}</p>
        <div class="division_1"></div>
        <div class="head flexCenter">
          <img src="../assets/images/user_IMG.png" class="head_portrait" alt="">
          <div style="margin-left: 10px;">
            <span>欢迎您使用</span>
            <i>管理员 <img src="../assets/images/Shape_icon.png" alt=""> </i>
          </div>  
        </div>
        <div class="division_1"></div>
        <div @click="onSign" style="cursor: pointer;">
          <img src="../assets/images/go_icon.png" alt="">
        </div>
      </div>
    </header>
    <div class="view">
      <div class="menu-left">
        <!-- <router-link to="" active-class="active">
              <img src="../assets/images/menu1.png" alt="">
              首页
            </router-link>
            <router-link to="">
              <img src="../assets/images/menu2.png" alt="">
              异常弹窗警告</router-link>
            <router-link to="">
              <img src="../assets/images/menu3.png" alt="">
              不法信息监控</router-link>
            <router-link to="">
              <img src="../assets/images/menu4.png" alt="">
              系统设置</router-link> -->
        <div class="link " :class="classActive == 0 ? 'link_active':'' " @click="onClass(0)">
          <div class="flexCenter">
            <img src="../assets/images/menu1.png" alt="" v-if="classActive != 0">
          </div>
          <span>首页</span>
        </div>
        <div class="link" :class="classActive == 1 ? 'link_active1':'' " @click="onClass(1)">
          <div class="flexCenter">
            <img src="../assets/images/menu2.png" alt="" v-if="classActive != 1">
          </div>
          <span>异常弹窗警告</span>
        </div>
        <div class="link" :class="classActive == 2 ? 'link_active2':'' " @click="onClass(2)">
          <div class="flexCenter">
            <img src="../assets/images/menu3.png" alt="" v-if="classActive != 2">
          </div>
          <span>不法信息监控</span>
        </div>
        <div class="link" :class="classActive == 3 ? 'link_active3':'' " @click="onClass(3)">
          <div class="flexCenter">
            <img src="../assets/images/menu4.png" alt="" v-if="classActive != 3">
          </div>
          <span>系统设置</span>
        </div>
      </div>
      <router-view />
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import util from "../util";
export default {
  data() {
    return {
      classActive: 0,
      timeTxt:'',
      week:''
    }
  },
  mounted() {
    util.$on('num', res => {
      if (res == 1) {
        this.classActive = 1
      } else {
        this.classActive = 2
      }
    });
    this.getCurrentTime()
  },
  methods: {
    onClass(num) {
      this.classActive = num
      if (num == 0) {
        this.$router.push('/one')
      } else if (num == 1) {
        this.$router.push('/two')
      } else if (num == 2) {
        this.$router.push('/three')
      } else if (num == 3) {
        this.$router.push('/four')
      }
    },
    getCurrentTime() {
      //获取当前时间并打印
      let date = new Date();
      let yy = new Date().getFullYear();
      let mm = new Date().getMonth() + 1;
      let dd = new Date().getDate();
      this.timeTxt = yy + '.' + mm + '.' + dd ;
      this.week = "星期" + "日一二三四五六".charAt(date.getDay());
    },
    onSign () {
      sessionStorage.removeItem('token')
      setTimeout(() => {
        this.$router.push('./login.vue')
        this.$message({
          message: '退出成功',
          type: 'success'
        });
      }, 0);
    }
  },
  beforeDestroy() {
    util.$off('num')
  },

}
</script>
<style scoped>

</style>