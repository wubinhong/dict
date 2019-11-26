<template>
    <div id="app">
        <!-- <img src="./assets/logo.png" /> -->
        <!-- Basic layout -->
        <el-container>
            <el-aside class="my-aside" style="width: 200px; background: #EBEEF5;">
                <Sidebar />
            </el-aside>
            <el-container>
                <el-header style="background: #324157; color: white;">
                    <Header msg="这是Header"></Header>
                </el-header>
                <el-main style>
                    <router-view></router-view>
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>

<script>
import Sidebar from "./components/Sidebar.vue";
import Header from "./components/Header.vue";


export default {
    name: "app",
    components: {
        Sidebar,
        Header
    }
};
</script>

<style lang="less">
/** 高度撑满屏幕，需要父子容器都要: height: 100%; */
html,
body {
    margin: 0;
    padding: 0;
    height: 100%;
    font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
}
#app {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    height: 100%;
}
.el-container {
    height: 100%;
}

/* hide aside when screen is smaller than a certain widht */
@media screen and (max-width: 1024px) {
    .my-aside {
        display: none !important;
    }
}
</style>
