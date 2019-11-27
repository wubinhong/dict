<template>
    <div id="app">
        <!-- <h2>Basic page</h2> -->
        <router-view />
        <snackbar-store />
    </div>
</template>

<script>
import SnackbarStore from "@/components/SnackbarStore.vue";
export default {
    components: {
        SnackbarStore
    }
};
</script>
