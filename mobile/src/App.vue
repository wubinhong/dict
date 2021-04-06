<template>
    <div id="app">
        <!-- <h2>Basic page</h2> -->
        <router-view />
        <!-- <snackbar-store /> -->
        <v-snackbar class="v-application"
            top
            v-model="snackbar.showed"
            :multi-line="snackbar.multiline"
            :vertical="snackbar.vertical"
            :color="snackbar.color"
            :timeout="snackbar.timeout"
        >
            {{ snackbar.message }}
            <v-btn dark text @click="snackbar.showed = false">Close</v-btn>
        </v-snackbar>
    </div>
</template>

<script>
// import SnackbarStore from "@/components/SnackbarStore.vue";
export default {
    components: {
        // SnackbarStore
    },
    computed: {
        snackbar() {
            // console.log("computed.", this.$store.state.snackbar);
            // 注意：此处为关键，snackbar不能放在data里，否则store里修改数据时，不会自动触发更新(reactive)
            // 另外，如果使用从外部注入component的方式，不然会生成2个snackbar，timeout=0时，可以看到，
            // 关掉前面的snackbar后，里面还有一个，怎么也关不掉
            return this.$store.state.snackbar;
        }
    },
    created() {
        // Generally handle the default setting object stored in the local storage.
        if (!JSON.parse(localStorage.getItem("setting"))) {
            localStorage.setItem("setting", "{}");
        }
    }
};
</script>
