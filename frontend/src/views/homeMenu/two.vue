<template>
  <div class="view2">
    <div class="view2_top">
      <div class="timeWorp flexCenter">
        <p>时间选择：</p>
        <!-- <el-time-picker is-range v-model="timeVal" range-separator="至" start-placeholder="开始时间"
               end-placeholder="结束时间" placeholder="选择时间范围" change="onTime">
            </el-time-picker> -->
        <el-date-picker
          v-model="timeVal"
          type="daterange"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          :default-time="['00:00:00', '23:59:59']"
          @change="onData"
        >
        </el-date-picker>
      </div>
      <!-- <div class="ipt">
            <input type="text" placeholder="请输入关键词搜索">
         </div> -->
      <div class="screen flexCenter" @click="onScreen(true)">
        <img src="../../assets/images/screen_icon.png" alt="" />
        筛选
      </div>
    </div>
    <div class="view2_bttom">
      <div class="pupList_tips">
        <p>弹窗违规列表</p>
      </div>
      <div class="from">
        <ul class="from_title">
          <li><span>IP / URL</span></li>
          <li><span>图片</span></li>
          <li><span>是否弹窗</span></li>
          <li><span>检测时间</span></li>
        </ul>
        <ul class="list" v-for="(item, index) in itemData" :key="index">
          <li>
            {{ item.ip_address }}
          </li>
          <li>
            <img :src="'data:image/jpeg;base64,' + item.image_path" alt="" />
          </li>
          <li>
            {{ item.is_abnormal ? "是" : "否" }}
          </li>
          <li>
            {{ item.create_time }}
          </li>
        </ul>
      </div>
      <div class="page_worp" style="margin-top: 40px; padding: 0">
        <div class="page_sum">共 {{ total }} 条信息</div>
        <el-pagination
          layout="prev, pager, next"
          :total="total"
          @current-change="handleCurrentChange"
          :current-page.sync="limit"
          :page-size="6"
        >
        </el-pagination>
      </div>
    </div>
  </div>
</template>
  
<script>
import qs from "qs";
export default {
  data() {
    return {
      timeVal: "",
      page: "1", //当前页
      size: "6", //当前页几条数据
      start_time: "", //开始时间
      end_time: "", //结束时间
      total: "", //总条数上限
      itemData: [], //表格数据

      limit: 1, //当前页

      timer:null
    };
  },
  mounted() {
    var windowVal = {
      page: "1",
      size: "6",
    };

    let flushTime = Number(sessionStorage.getItem("flushTime"));
    if (flushTime == 0) {
   
      this.fpostWindow(windowVal);
    } else {

      this.fpostWindow(windowVal);

      this.timer = window.setInterval(() => {
     this.onScreen(false)
      }, flushTime);
    }

    // 清除定时器
    this.$once("hook:beforeDestroy", () => {
      clearInterval(this.timer);
    });
  },
  watch: {
    timeVal(newVal1) {
      if (newVal1 == null) {
        this.limit = 1;
        this.start_time = "";
        this.end_time = "";
        let windowVal = {
          page: "1",
          size: this.size,
        };
        this.fpostWindow(windowVal);
      }
    },
  },
  methods: {
    fpostWindow(data) {
      this.api.postWindow(data).then((res) => {
        this.itemData = res.data.items;
        this.total = res.data.total;
        this.itemData.forEach((el, index) => {
          this.api.getImgUrl({ full_path: el.image_path }).then((res) => {
            this.itemData[index].create_time = this.ftimeFormatSeconds(
              el.create_time
            );
            this.itemData[index].image_path = res.data.b64_image;
          });
        });

        // res.data.items.forEach((element,index )=> {
        //    console.log(element.image_path);
        // });
      });
    },
    //获得年月日时分秒
    //传入日期//例：2020-10-27T14:36:23
    ftimeFormatSeconds(time) {
      var d = time ? new Date(time) : new Date();
      var year = d.getFullYear();
      var month = d.getMonth() + 1;
      var day = d.getDate();
      var hours = d.getHours();
      var min = d.getMinutes();
      var seconds = d.getSeconds();

      if (month < 10) month = "0" + month;
      if (day < 10) day = "0" + day;
      if (hours < 0) hours = "0" + hours;
      if (min < 10) min = "0" + min;
      if (seconds < 10) seconds = "0" + seconds;

      return (
        year + "-" + month + "-" + day + " " + hours + ":" + min + ":" + seconds
      );
    },
    handleCurrentChange(val) {
      this.limit = val;
      if (this.start_time == "" || this.end_time == "") {
        let windowVal = {
          page: val,
          size: this.size,
        };
        this.fpostWindow(windowVal);
      } else {
        let windowVal = {
          page: val,
          size: this.size,
          start_time: this.start_time,
          end_time: this.end_time,
        };
        this.fpostWindow(windowVal);
      }
    },
    onData(val) {
      //转为时间戳加上八小时再转回来
      this.start_time =  new Date(new Date(val[0]).getTime()+(8*3600*1000)).toISOString();
      this.end_time =  new Date(new Date(val[1]).getTime()+(8*3600*1000)).toISOString();
    },
    //筛选
    onScreen(click) {
      if (this.start_time == "" || this.end_time == "") {
        let windowVal = {
          page:  click?1:this.limit,
          size: this.size,
        };
        this.fpostWindow(windowVal);
      } else {
        let windowVal = {
          page: click?1:this.limit,
          size: this.size,
          start_time: this.start_time,
          end_time: this.end_time,
        };
        this.fpostWindow(windowVal);
      }
    },
  },
};
</script>
<style scoped>
</style>