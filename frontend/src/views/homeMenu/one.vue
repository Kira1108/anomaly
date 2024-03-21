<template>
  <div class="view1">
    <div class="pupWorp">
      <div @click="onTwo">
        <img src="../../assets/images/pup_bj1.png" alt="" />
        <ul class="pup_num">
          <p class="blue_p">{{ window_count }}</p>
          <i></i>
          <span>疑似弹窗事件</span>
        </ul>
      </div>
      <div @click="onThree">
        <img src="../../assets/images/pup_bj.png" alt="" />
        <ul class="pup_num">
          <p class="yellow_p">{{ text_count }}</p>
          <i></i>
          <span>疑是不法信息数量</span>
        </ul>
      </div>
      <div>
        <img src="../../assets/images/pup_bj3.png" alt="" />
        <ul class="pup_num">
          <p class="gray_p">{{ sex_count }}</p>
          <i></i>
          <span>已检测的图片数量</span>
        </ul>
      </div>
      <div>
        <img src="../../assets/images/pup_bj2.png" alt="" />
        <ul class="pup_num">
          <p class="green_p">{{ orc }}</p>
          <i></i>
          <span>已检测OCR文字数量</span>
        </ul>
      </div>
    </div>
    <div class="pupList">
      <div class="pupList_tips">
        <p>弹窗违规列表</p>
      </div>
      <div class="listWorp">
        <div
          class="list"
          v-for="(item, index) in itemData.slice(0, 10)"
          :key="index"
        >
          <img :src="'data:image/jpeg;base64,' + item.image_path" alt="" />
          <div class="ip">
            <i>IP / URL</i>
            <p>{{ item.ip_address }}</p>
          </div>
          <div class="time">{{ item.time }}</div>
        </div>
      </div>
    </div>
    <div class="page_worp">
      <div class="page_sum">共 {{ total }} 条信息</div>
      <el-pagination
        layout="prev, pager, next"
        :total="total"
        @current-change="handleCurrentChange"
        :page-size="10"
      >
      </el-pagination>
    </div>
  </div>
</template>
  
<script>
import util from "../../util";
export default {
  data() {
    return {
      list: [],
      orc: "",
      text_count: "",
      sex_count: "",
      window_count: "",

      timeVal: "",
      page: "1", //当前页
      size: "10", //当前页几条数据
      start_time: "", //开始时间
      end_time: "", //结束时间
      total: "", //总条数上限
      itemData: [], //表格数据,
      timer:null,
    };
  },
  mounted() {
    let windowVal = {
      page: "1",
      size: "10",
      // start_time: this.start_time,
      // end_time: this.end_time,
    };

    //拿到页面存储的刷新时间
    let flushTime = Number(sessionStorage.getItem("flushTime"));
    console.log(flushTime);
    if (flushTime == 0) {
      console.log(flushTime, 111);
      this.fgetOcrCountg();
      this.fgetTextCountg();
      this.fgetSexCountg();
      this.fgetWindowCountg();

      this.fpostWindow(windowVal);
    } else {
      this.fgetOcrCountg();
      this.fgetTextCountg();
      this.fgetSexCountg();
      this.fgetWindowCountg();

      this.fpostWindow(windowVal);

     this.timer = window.setInterval(() => {
        setTimeout(() => {
          this.fgetOcrCountg();
          this.fgetTextCountg();
          this.fgetSexCountg();
          this.fgetWindowCountg();

          this.fpostWindow(windowVal);
        }, 0);
      }, flushTime);

      // 清除定时器
      this.$once("hook:beforeDestroy", () => {
        clearInterval(this.timer);
      });
    }
  },
  methods: {
    onTwo() {
      this.$router.push("/two");
      util.$emit("num", 1);
    },
    onThree() {
      this.$router.push("/three");
      util.$emit("num", 2);
    },

    //列表接口
    fpostWindow(data) {
      this.api.postWindow(data).then((res) => {
        this.itemData = res.data.items;
        console.log(this.itemData);
        this.total = res.data.total;
        this.itemData.forEach((el, index) => {
          this.api.getImgUrl({ full_path: el.image_path }).then((res) => {
            this.itemData[index].image_path = res.data.b64_image;
          });
        });
        // this.itemData.forEach((el,index)=>{
        //   this.api.getImgUrl({ full_path: el.image_path}).then(res => {
        //     this.itemData[index].image_path=res.data.b64_image
        // })
        // })
      });
    },
    handleCurrentChange(val) {
      this.limit = val;
      let windowVal = {
        page: val,
        size: this.size,
      };
      this.fpostWindow(windowVal);
    },
    //统计数量接口
    fgetOcrCountg() {
      this.api.getOcrCountg().then((res) => {
        this.orc = res.data.data;
      });
    },
    fgetTextCountg() {
      this.api.getTextCountg().then((res) => {
        this.text_count = res.data.data;
      });
    },
    fgetSexCountg() {
      this.api.getSexCountg().then((res) => {
        this.sex_count = res.data.data;
      });
    },
    fgetWindowCountg() {
      this.api.getWindowCountg().then((res) => {
        this.window_count = res.data.data;
      });
    },
  },
};
</script>
<style scoped>
</style>