<template>
    <v-container>
        <v-row>
            <v-col>
                <v-hover>
                    <template v-slot="{ hover }">
                        <v-card :elevation="hover ? 24 : 6" class="mx-auto pa-6">
                            <v-form ref="form" v-model="valid" lazy-validation>
                                <v-text-field v-model="word.name" :rules="nameRules" label="单词">
                                    <template v-slot:append>
                                        <audio
                                            controls
                                            style="height: 30px; max-width: 100px;"
                                            hidden
                                            autoplay
                                            :src="`http://dict.youdao.com/dictvoice?audio=${word.name}&type=1`"
                                        >
                                            Your browser does not support the
                                            <code>audio</code> element.
                                        </audio>
                                    </template>
                                </v-text-field>

                                <v-text-field v-model="word.derivation" label="词根"></v-text-field>
                                <v-text-field v-model="word.chinese" label="中文"></v-text-field>
                                <v-text-field v-model="word.thesauri" label="同义词"></v-text-field>
                                <v-text-field v-model="word.related_words" label="相关词"></v-text-field>
                                <v-text-field v-model="word.similar_shaped_words" label="近形词"></v-text-field>
                                <v-text-field v-model="word.comment" label="备注"></v-text-field>
                                <v-slider
                                    v-model="word.hardship"
                                    :label="`难度`"
                                    thumb-label
                                    style="padding: 12px 0"
                                    color="orange darken-3"
                                    thumb-color="red"
                                    prepend-icon="mdi-shield-star-outline"
                                >
                                    <template v-slot:append>
                                        <v-tooltip top>
                                            <template v-slot:activator="{ on }">
                                                <v-icon v-on="on">mdi-help-circle-outline</v-icon>
                                            </template>
                                            对单词（ {{word.name}} ）的陌生程度，值越大，在列表里排名越靠前！
                                        </v-tooltip>
                                    </template>
                                </v-slider>
                                <v-btn
                                    :disabled="!valid"
                                    color="primary"
                                    class="mr-4"
                                    @click="onWordSave"
                                    ref="submitBtn"
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
            v =>
                (v && v.length <= 100) ||
                "Name must be less than 100 characters"
        ],
        ctrlKeyHoldOn: false
    }),

    methods: {
        onWordSave() {
            // console.log(this.word, this.$refs.form);
            if (this.$refs.form.validate()) {
                let vm = this;
                let w = this.word;
                this.$axios
                    .put(`/backend/api/words/${w.name}`, w)
                    .then(response => {
                        if (response.status === 200 && response.data.rc === 0) {
                            vm.$router.go(-1);
                        }
                    });
            }
        },
        onWordReset() {
            this.$refs.form.reset();
        }
    },
    created() {
        let name = this.$route.query.name;
        if (name) {
            // Get word from remote server.
            this.$axios.get(`/backend/api/words/${name}`).then(res => {
                if (res.data.rc === 0 && res.data.data) {
                    this.word = res.data.data;
                } else {
                    // 新建的单词，带了name参数过来
                    this.word = { name: name };
                }
            });
        } else {
            // 新建单词，没有name参数
            this.word = {};
        }
    },
    mounted: function() {
        window.onkeydown = e => {
            // 用户每次按键都会触发该事件，所以对于组合键的检测，需要配合使用onkeydown和onkeyup事件来实现
            if (e.key === "Meta" || e.key === "Control") {
                this.ctrlKeyHoldOn = true;
            }
            // 用户按 "Meta + enter"或者"Control + enter" 组合键后，自动提交表单
            if (this.ctrlKeyHoldOn && e.key === "Enter") {
                this.$refs.submitBtn.click(document.createEvent("MouseEvent"));
                // console.log(this.$refs.submitBtn.click())
            }
        };
        window.onkeyup = () => {
            // 重置组合键
            this.ctrlKeyHoldOn = false;
        };
    }
};
</script>
