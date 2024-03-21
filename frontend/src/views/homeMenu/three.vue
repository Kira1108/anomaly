<template>
  <div class="view2 view3">
    <div class="viee3_choice">
      <div class="choice_left" :class="active == 0 ? 'active_left' : ''" @click="onActive(0)">
        不法信息监控
      </div>
      <div class="choice_right" :class="active == 1 ? 'active_right' : ''" @click="onActive(1)">
        涉黄图片监控
      </div>
      <div class="choice_ai" :class="active == 2 ? 'active_ai_s' : ''" @click="onActive(2)">
        AI纯文本识别分析
      </div>
    </div>
    <div class="view2_top">
      <div class="timeWorp flexCenter">
        <p>时间选择：</p>
        <!-- <el-time-picker is-range v-model="timeVal" range-separator="至" start-placeholder="开始时间" end-placeholder="结束时间"
          placeholder="选择时间范围">
        </el-time-picker> -->
        <el-date-picker v-model="timeVal" type="daterange" start-placeholder="开始日期" end-placeholder="结束日期"
          :default-time="['00:00:00', '23:59:59']" @change="onData">
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
        <p>违规列表</p>
      </div>
      <div class="from" v-if="isfrom == 0">
        <ul class="from_title">
          <li><span>IP / URL</span></li>
          <li><span>图片</span></li>
          <li><span>OCR文字</span></li>
          <li><span>是否违规</span></li>
          <li><span>检测时间</span></li>
        </ul>
        <ul class="list" v-for="(item, index) in itemData.slice(0, 6)" :key="index">
          <li>
            {{ item.ip_address }}
          </li>
          <li>
            <img :src="'data:image/jpeg;base64,' + item.image_path" alt="" />
          </li>
          <li>
            {{ item.sensitive_words }}
          </li>
          <li>
            {{ item.sensitive ? "是" : "否" }}
          </li>
          <li>
            {{ item.create_time }}
          </li>
        </ul>
      </div>
      <div class="from" v-if="isfrom == 1">
        <ul class="from_title">
          <li><span>IP / URL</span></li>
          <li><span>类别</span></li>

          <li><span>图片</span></li>
          <li><span>是否违规</span></li>
          <li><span>检测时间</span></li>
        </ul>
        <ul class="list" v-for="(item, index) in sexImgData.slice(0, 6)" :key="index">
          <li>
            {{ item.ip_address }}
          </li>
          <li>
            {{ item.is_abnormal ? "含不法信息图片" : "不含不法信息图片" }}
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
      <div class="from" v-if="isfrom == 2">
        <ul class="from_title">
          <li><span>IP / URL</span></li>
          <li><span>文字</span></li>
          <li><span>是否违规</span></li>
          <li><span>检测时间</span></li>
        </ul>
        <ul class="list" v-for="(item, index) in itemData.slice(0, 6)" :key="index">
          <li>
            {{ item.ip_address }}
          </li>
          <li>
            {{ item.sensitive_words }}
          </li>
          <li>
            {{ item.sensitive ? "是" : "否" }}
          </li>
          <li>
            {{ item.create_time }}
          </li>
        </ul>
      </div>
      <div class="page_worp" style="margin-top: 40px; padding: 0">
        <div class="page_sum">共 {{ total }} 条信息</div>
        <el-pagination layout="prev, pager, next" :total="total" @current-change="handleCurrentChange"
          :current-page.sync="limit" :page-size="6">
        </el-pagination>
      </div>
    </div>
  </div>
</template>
 
<script>
// @ is an alias to /src

export default {
  data() {
    return {
      timeVal: "",
      active: 0,
      active_left: true,
      active_right: false,
      isfrom: 0, //显示的哪个表单
      keyID:0, //表单的唯一KEY

      limit: 1, //当前页
      offset: "6", //当前页几条数据

      page: "1", //当前页
      size: "6", //当前页几条数据

      start_time: "", //开始时间
      end_time: "", //结束时间
      total: "", //总条数上限
      itemData: [], //表格数据

      sexImgData: [], //色情图片表格数据

      key2: "",
      timer: null,
    };
  },
  mounted() {
    var textVal = {
      page: "1",
      size: "6",
    };

    let flushTime = Number(sessionStorage.getItem("flushTime"));
    if (flushTime == 0) {
      this.fpostText(textVal);
    } else {
      this.fpostText(textVal);

      this.limit = 1;
      this.timeVal = "";

      this.timer = window.setInterval(() => {
        setTimeout(() => {
          this.onScreen(false)
        }, 0);
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
        if (this.keyID == 0) {
          let textVal = {
            page: "1",
            size: this.size,
          };
          this.fpostText(textVal);
        } else if (this.keyID == 1) {
          let textVal = {
            page: "1",
            size: this.size,
          };
          this.fpostSexImg(textVal);
        } else {
          let textVal = {
            page: "1",
            size: this.size,
          };
          this.fpostText(textVal);
        }
      }
    },
    // "endDay"(newVal2) {
    //   if (newVal2 == null) {
    //   /* 获取当前时间工具类：DateUtils.formatStandardDate */
    //     this.endDay = this.DateUtils.formatStandardDate(new Date());
    //     this.startDay=this.DateUtils.formatStandardDate(new Date());
    //   }
    // },
  },

  methods: {
    onActive(key) {
      let flushTime = Number(sessionStorage.getItem("flushTime"));

      this.keyID = key;
      if (key == 0) {
        this.active = 0;
        this.isfrom = 0;
        this.limit=1
        this.timeVal = "";
        this.start_time = "";
        this.end_time = "";

        if (this.start_time == "" || this.end_time == "") {
          let textVal = {
            page: this.limit,
            size: this.size,
          };
          this.fpostText(textVal);
        }
      } else if (key == 1) {
        this.active = 1;
        this.isfrom = 1;
        //重置page页码 调用色情图片接口
        this.limit = 1;
        this.timeVal = "";
        this.start_time = "";
        this.end_time = "";
        if (flushTime == 0) {
          if (this.start_time == "" || this.end_time == "") {
            let textVal = {
              page: this.limit,
              size: this.size,
            };
            this.fpostSexImg(textVal);
          }
        } else {
          if (this.start_time == "" || this.end_time == "") {
            let textVal = {
              page: this.limit,
              size: this.size,
            };
            this.fpostSexImg(textVal);
          }
          // this.key2 = window.setInterval(() => {
          //   setTimeout(() => {
          //     if (this.start_time == "" || this.end_time == "") {
          //       let textVal = {
          //         page: this.page,
          //         size: this.size,
          //       };
          //       this.fpostSexImg(textVal);
          //     }
          //   }, 0);
          // }, flushTime);
        }
      } else {
        this.active = 2;
        this.isfrom = 2;
        //重置page页码 调用色情图片接口
        this.limit = 1;
        this.timeVal = "";
        this.start_time = "";
        this.end_time = "";
        (this.timeVal = ""), (this.start_time = ""), (this.end_time = "");
        if (this.start_time == "" || this.end_time == "") {
          let textVal = {
            page: this.limit,
            size: this.size,
          };
          this.fpostText(textVal);
        }
      }
    },
    fpostText(data) {
      this.api.postText(data).then((res) => {
        this.itemData = res.data.items;
        this.itemData.forEach((el, index) => {
          this.api.getImgUrl({ full_path: el.image_path }).then((res) => {
            this.itemData[index].create_time = this.ftimeFormatSeconds(
              el.create_time
            );
            this.itemData[index].image_path = res.data.b64_image;
          });
        });
        console.log(this.itemData);
        this.total = res.data.total;
      });
    },
    fpostSexImg(data) {
      this.api.postSexImg(data).then((res) => {
        this.sexImgData = res.data.items;
        this.total = res.data.total;
        this.sexImgData.forEach((el, index) => {
          this.api.getImgUrl({ full_path: el.image_path }).then((res) => {
            this.sexImgData[index].create_time = this.ftimeFormatSeconds(
              el.create_time
            );
            this.sexImgData[index].image_path = res.data.b64_image;
          });
        });
      });
    },
    //时间选择赋值
    onData(val) {
      //转为时间戳加上八小时再转回来
      this.start_time =  new Date(new Date(val[0]).getTime()+(8*3600*1000)).toISOString();
      this.end_time =  new Date(new Date(val[1]).getTime()+(8*3600*1000)).toISOString();
    },
    handleCurrentChange(val) {
      this.limit = val;
      if (this.keyID == 0) {
        if (this.start_time == "" || this.end_time == "") {
          let textVal = {
            page: val,
            size: this.size,
          };
          this.fpostText(textVal);
        } else {
          let textVal = {
            page: val,
            size: this.size,
            start_time: this.start_time,
            end_time: this.end_time,
          };
          this.fpostText(textVal);
        }
      } else if (this.keyID == 1) {
        if (this.start_time == "" || this.end_time == "") {
          let textVal = {
            page: val,
            size: this.size,
          };
          this.fpostSexImg(textVal);
        } else {
          let textVal = {
            page: val,
            size: this.size,
            start_time: this.start_time,
            end_time: this.end_time,
          };
          this.fpostSexImg(textVal);
        }
      } else {
        if (this.start_time == "" || this.end_time == "") {
          let textVal = {
            page: val,
            size: this.size,
          };
          this.fpostText(textVal);
        } else {
          let textVal = {
            page: val,
            size: this.size,
            start_time: this.start_time,
            end_time: this.end_time,
          };
          this.fpostText(textVal);
        }
      }
    },
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
    //筛选
    onScreen(click) {
      console.log(click,222,this.limit);
      if (this.keyID == 0) {
        if (this.start_time == "" || this.end_time == "") {
          let textVal = {
            page: click?1:this.limit,
            size: this.size,
          };
          this.fpostText(textVal);
        } else {
          let textVal = {
            page:  click?1:this.limit,
            size: this.size,
            start_time: this.start_time,
            end_time: this.end_time,
          };
          this.fpostText(textVal);
        }
      } else if (this.keyID == 1) {
        if (this.start_time == "" || this.end_time == "") {
          let textVal = {
            page: click?1:this.limit,
            size: this.size,
          };
          this.fpostSexImg(textVal);
        } else {
          let textVal = {
            page: click?1:this.limit,
            size: this.size,
            start_time: this.start_time,
            end_time: this.end_time,
          };
          this.fpostSexImg(textVal);
        }
      } else {
        if (this.start_time == "" || this.end_time == "") {
          let textVal = {
            page:  click?1:this.limit,
            size: this.size,
          };
          this.fpostText(textVal);
        } else {
          let textVal = {
            page:  click?1:this.limit,
            size: this.size,
            start_time: this.start_time,
            end_time: this.end_time,
          };
          this.fpostText(textVal);
        }
      }
    },
  },
};
</script>
<style scoped>

</style>