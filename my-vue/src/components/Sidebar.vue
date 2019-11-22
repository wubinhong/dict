<template>
    <div>
        侧边栏组件
        <ul>
            <li><router-link to="/dashboard">Dashbaord</router-link></li>
            <li><router-link to="/post/1?score=23">Post</router-link></li>
            <li><router-link to="/settings">Settings</router-link></li>
        </ul>
    </div>
</template>

<script>
export default {
    name: "Sidebar",
    props: {
        msg: String
    }
};
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>