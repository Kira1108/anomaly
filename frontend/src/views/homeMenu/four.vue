<template>
  <div class="view4">
    <div class="view4_center">
      <div class="pupList_tips">
        <p>设置</p>
      </div>
      <div class="time_set">
        <p>网页刷新时间</p>
        <div class="select flexCenter">
          <el-select v-model="value" placeholder="请选择" @change="onRefreshTime">
            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
          <div class="screen flexCenter" style="cursor: pointer;">筛选</div>
        </div>
      </div>
      <!-- <div class="time_set">
        <p>词库修改</p>
        <div class="select flexCenter">
          <el-select v-model="value" placeholder="请选择">
            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
          <div class="screen flexCenter">词库</div>
        </div>
      </div> -->
      <div class="time_set">
        <p>词库修改</p>
        <div class="upload">
          <el-upload action="https://jsonplaceholder.typicode.com/posts/" list-type="picture-card"
            :on-preview="handlePictureCardPreview" :on-remove="handleRemove">
            <i class="el-icon-plus"></i>
          </el-upload>
          <el-dialog :visible.sync="dialogVisible">
            <img width="100%" :src="dialogImageUrl" alt="">
          </el-dialog>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script>
// @ is an alias to /src

export default {
  data() {
    return {
      options: [{
        value: '5000',
        label: '5S'
      }, {
        value: '10000',
        label: '10S'
      }, {
        value: '20000',
        label: '20S'
      }, {
        value: '60000',
        label: '60S'
      }, {
        value: '300000',
        label: '300S'
      }],
      value: '',
      dialogImageUrl: '',
      dialogVisible: false
    }
  },
  methods: {
    handleRemove(file, fileList) {
      console.log(file, fileList);
    },
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
    },
    onRefreshTime (e) {
      sessionStorage.setItem('flushTime',e)
      this.$message({
          message: '操作成功',
          type: 'success'
        });
      console.log(e);
    }
  }
}
</script>
<style scoped>

</style>