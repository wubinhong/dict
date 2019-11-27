<template>
    <v-container>
        <v-row>
            <v-col>
                <v-hover>
                    <template v-slot="{ hover }">
                        <v-card :elevation="hover ? 24 : 6" class="mx-auto pa-6">
                            <v-form ref="form" v-model="valid" lazy-validation>
                                <v-text-field v-model="word.name" :rules="nameRules" label="单词"></v-text-field>

                                <v-text-field v-model="word.derivation" label="词根"></v-text-field>
                                <v-text-field v-model="word.chinese" label="中文"></v-text-field>
                                <v-text-field v-model="word.thesauri" label="同义词"></v-text-field>
                                <v-text-field v-model="word.related_words" label="相关词"></v-text-field>
                                <v-text-field v-model="word.similar_shaped_words" label="近形词"></v-text-field>
                                <v-text-field v-model="word.comment" label="备注"></v-text-field>

                                <v-btn
                                    :disabled="!valid"
                                    color="primary"
                                    class="mr-4"
                                    @click="onWordSave"
                                >保存</v-btn>
                                <v-btn color="warning" class="mr-4" @click="onWordReset">重置</v-btn>
                                <v-btn color="teal" class="mr-4" @click="$router.go(-1)">
                                    <v-icon dark>mdi-arrow-left</v-icon>返回
                                </v-btn>
                            </v-form>
                        </v-card>
                    </template>
                </v-hover>
            </v-col>
        </v-row>
        <v-snackbar
            v-model="snackbar.showed"
            top
            multi-line
            :color="snackbar.color"
            :timeout="snackbar.timeout"
        >
            {{ snackbar.message }}
            <v-btn dark text @click="snackbar.showed = false">Close</v-btn>
        </v-snackbar>
    </v-container>
</template>

<script>
export default {
    data: () => ({
        valid: true,
        word: {
            thesauri: ""
        },
        nameRules: [
            v => !!v || "Name is required",
            v => (v && v.length <= 10) || "Name must be less than 10 characters"
        ],
        snackbar: {
            showed: false,
            color: 'success',
            timeout: 1000,
            message: "Snack bar message!"
        }
    }),

    methods: {
        onWordSave() {
            // console.log(this.word, this.$refs.form);
            if (this.$refs.form.validate()) {
                let vm = this;
                let w = this.word;
                this.$axios
                    .put(`/backend/words/${w.name}`, w)
                    .then(response => {
                        if (response.status === 200 && response.data.rc === 0) {
                            vm.$router.go(-1);
                        } else {
                            vm.snackbar = {
                                ...vm.snackbar,
                                showed: true,
                                color: "error",
                                message: response.data.msg
                            };
                            clearTimeout(vm.timeout)
                            vm.timeout = setTimeout(() => {
                                vm.snackbar.showed = false
                            }, 1000);
                            
                        }
                    }).catch(response => {
                        // Expand operation, avoid override other default props, .e.g. timeout
                        vm.snackbar = {...vm.snackbar, showed: true, ...{
                            message: response.response.statusText
                        }}
                    });
            }
        },
        onWordReset() {
            this.$refs.form.reset();
        }
    },
    created() {
        this.word = this.$route.query;
    },
    mounted: () => {
        // console.log('mounted', this)
    }
};
</script>
