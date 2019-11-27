<template>
    <div class="v-application">
        <v-snackbar
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
import { mapMutations } from "vuex";

export default {
    name: "SnackbarStore",
    computed: {
        snackbar() {
            // console.log("computed.", this.$store.state.snackbar);
            // 注意：此处为关键，snackbar不能放在data里，否则store里修改数据时，不会自动触发更新(reactive)
            return this.$store.state.snackbar;
        }
    },
    methods: {
        ...mapMutations(["closeSnackbar"])
    }
};
</script>
