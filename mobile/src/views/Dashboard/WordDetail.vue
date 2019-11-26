<template>
    <v-container>
        <v-row>
            <v-col>
                <v-alert
                    :type="alert.type"
                    v-show="alert.showed"
                    outlined
                    text
                    dismissible
                >{{alert.message}}</v-alert>
                <v-form ref="form" v-model="valid" lazy-validation>
                    <v-text-field v-model="word.name" :rules="nameRules" label="单词"></v-text-field>

                    <v-text-field v-model="word.derivation" label="词根"></v-text-field>
                    <v-text-field v-model="word.chinese" label="中文"></v-text-field>
                    <v-text-field v-model="word.thesauri" label="同义词"></v-text-field>
                    <v-text-field v-model="word.related_words" label="相关词"></v-text-field>
                    <v-text-field v-model="word.similar_shaped_words" label="近形词"></v-text-field>
                    <v-text-field v-model="word.comment" label="备注"></v-text-field>

                    <v-btn :disabled="!valid" color="primary" class="mr-4" @click="onWordSave">保存</v-btn>
                    <v-btn color="warning" class="mr-4" @click="onWordReset">重置</v-btn>
                    <v-btn color="teal" class="m4-4" @click="$router.go(-1)">
                        <v-icon dark>mdi-arrow-left</v-icon>返回
                    </v-btn>
                </v-form>
            </v-col>
        </v-row>
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
        alert: {
            showed: false,
            message: "I'm a success alert."
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
                            vm.alert = {
                                showed: true,
                                type: 'success',
                                message: response.data.msg
                            };
                            clearTimeout(vm.timeouter);
                            setTimeout(() => {
                                vm.$router.go(-1)
                            }, 1000);
                        } else {
                            vm.alert = {
                                showed: true,
                                type: 'error',
                                message: response.data.msg
                            };
                        }
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