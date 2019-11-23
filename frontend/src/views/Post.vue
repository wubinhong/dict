<template>
    <div>
        <div>这是Post</div>
        <div>Get params: {{$route.params}}</div>
        <div>Get query: {{$route.query}}</div>
        <div>props.id: {{id}}</div>
    </div>
</template>

<script>
export default {
    name: "Post",
    props: ["id"]
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
