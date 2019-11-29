<template>
    <!-- class="fill-height" can make child element justify to center in verticle -->
    <!-- <v-container class="fill-height" fluid> -->
    <v-container>
        <v-alert
            :type="alert.type"
            v-show="alert.showed"
            outlined
            text
            dismissible
        >{{alert.message}}</v-alert>
        <v-row>
            <v-col cols="12">
                <!-- <v-text-field color="success" loading disabled dark></v-text-field> -->
                <v-text-field
                    v-model="keyword"
                    @input="querySearch(keyword)"
                    ref="queryInput"
                    label="请输入单词"
                    filled
                    shaped
                    :loading="loading"
                >
                    <!-- <v-icon slot="prepend" color="green">mdi-magnify</v-icon> -->
                    <v-icon slot="append">mdi-magnify</v-icon>
                </v-text-field>

                <v-simple-table fixed-header height="600px" v-if="words.length !== 0">
                    <template v-slot:default>
                        <thead>
                            <tr>
                                <th class="text-left">Name</th>
                                <th class="text-left">详情</th>
                                <th class="text-left">操作</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(word, index) in words" :key="index">
                                <td>{{ word.name }}</td>
                                <td @click="go(word)">
                                    {{ word.derivation }} > {{ word.chinese }} > {{ word.thesauri }} >
                                    {{ word.related_words }} > {{ word.similar_shaped_words }} > {{ word.comment }}
                                </td>
                                <td>
                                    <v-btn
                                        x-small
                                        outlined
                                        color="error"
                                        @click="onWordDeleteConfirm(word)"
                                    >删除</v-btn>
                                </td>
                            </tr>
                        </tbody>
                    </template>
                </v-simple-table>

                <div v-else class="d-flex pa-2">
                    <v-btn color="pink" width="100%" @click="onNewWordAdd">添加该单词到单词库</v-btn>
                </div>
            </v-col>
        </v-row>
        <v-row justify="center">
            <v-dialog v-model="dialog" persistent max-width="320">
                <v-card>
                    <v-card-title class="headline">删除单词！</v-card-title>
                    <v-card-text>此操作将永久删除单词, 是否继续?</v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="green darken-1" text @click="onWordDelete">确定</v-btn>
                        <v-btn color="green darken-1" text @click="dialog = false">取消</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-row>
    </v-container>
</template>

<script>
export default {
    data: () => ({
        keyword: "",
        loading: false,
        words: [],
        dialog: false,
        alert: {
            showed: false,
            message: "Alert message!"
        }
    }),
    methods: {
        go(word) {
            // console.log(word);
            this.$router.push({
                path: `/dashboard/word`,
                query: word
            });
        },
        querySearch(keyword, timeout) {
            // 用户输入停顿后再请求，而不是输入有变化就请求，防止频繁请求服务器
            timeout = timeout || 500;
            clearTimeout(this.timeout);
            this.timeout = setTimeout(() => {
                this.loading = true;
                this.$axios
                    .get(
                        `/backend/words/fuzzy?keyword=${keyword}&skip=0&limit=20`
                    )
                    .then(response => {
                        if (response.status === 200 && response.data.rc === 0) {
                            // 调用 callback 返回建议列表的数据
                            this.words = response.data.data;
                        }
                        this.loading = false;
                    });
            }, timeout);
        },
        onNewWordAdd() {
            this.$router.push({
                name: "wordDetail",
                query: { name: this.keyword }
            });
        },
        onWordDeleteConfirm(word) {
            this.dialog = true;
            this.deleteWordName = word.name;
        },
        onWordDelete() {
            let vm = this;
            this.$axios
                .delete(`/backend/words/${this.deleteWordName}`)
                .then(response => {
                    if (response.status === 200 && response.data.rc === 0) {
                        vm.dialog = false;
                        vm.querySearch(vm.keyword, 0); // Reload data
                        vm.alert = {
                            showed: true,
                            type: "success",
                            message: response.data.msg
                        };
                        clearTimeout(vm.timeout2);
                        vm.timeout2 = setTimeout(() => {
                            vm.alert.showed = false;
                        }, 1000);
                    }
                });
        }
    },
    created() {
        // queryString = queryString || ''
        this.$axios
            .get(`/backend/words/fuzzy?keyword=${this.keyword}&skip=0&limit=20`)
            .then(response => {
                if (response.status === 200 && response.data.rc === 0) {
                    // 调用 callback 返回建议列表的数据
                    this.words = response.data.data;
                }
            });
    },
    mounted() {
        // Focus on query input automatically when page loaded.
        this.$refs.queryInput.focus();
        window.onkeyup = e => {
            // 用户按 "/" 键后，自动focus搜索框
            if (e.key === "/") {
                this.$refs.queryInput.focus();
            }
        };
    }
};
</script>

<style lang="scss">
</style>
