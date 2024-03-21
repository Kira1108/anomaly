<template>
  <div id="app" >
    <router-view />
  </div>
</template>

<style lang="scss">
// #app {
//   font-family: Avenir, Helvetica, Arial, sans-serif;
//   -webkit-font-smoothing: antialiased;
//   -moz-osx-font-smoothing: grayscale;
//   text-align: center;
//   color: #2c3e50;
// }

// nav {
//   padding: 30px;

//   a {
//     font-weight: bold;
//     color: #2c3e50;

//     &.router-link-exact-active {
//       color: #42b983;
//     }
//   }
// }
.scrool_app::-webkit-scrollbar {
  /*滚动条整体*/
  width: 10px;
  border-radius: 5px;
}

.scrool_app::-webkit-scrollbar-track {
  /*滚动条轨道*/
  background: rgba(18, 22, 27, .5);
}

.scrool_app::-webkit-scrollbar-thumb {
  /*滚动条里面的滑块*/
  border-radius: 10px;
}

.scrool_app::-webkit-scrollbar-thumb:hover {
  /*滚动条鼠标事件，鼠标放上去出现的事件*/
  background: rgba(9, 14, 36, 0.8);
}
</style>
