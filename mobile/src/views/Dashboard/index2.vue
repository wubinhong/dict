<template>
    <!-- class="fill-height" can make child element justify to center in verticle -->
    <!-- <v-container class="fill-height" fluid> -->
    <v-container>
        <v-card max-width="700" class="mx-auto">
            <v-text-field
                v-model="keyword"
                @input="querySearch(keyword)"
                label="请输入单词，支持按所有字段模糊查询"
                filled
                fixed-header
                color="yellow"
            >
                <!-- <v-icon slot="prepend" color="green">mdi-magnify</v-icon> -->
                <v-icon slot="append">mdi-magnify</v-icon>
            </v-text-field>

            <v-list two-line>
                <v-list-item-group v-if="words.length !== 0" active-class="yellow--text">
                    <template v-for="(word, index) in words">
                        <v-list-item :key="word.name">
                            <template>
                                <v-list-item-content>
                                    <v-list-item-title v-text="word.name"></v-list-item-title>
                                    <v-list-item-subtitle v-text="word.derivation"></v-list-item-subtitle>
                                    <!-- <v-list-item-subtitle v-text="word.chinese"></v-list-item-subtitle> -->
                                    <v-list-item-action-text
                                        @click="go(word)"
                                    >{{word.chinese}} > {{word.thesauri}} > {{word.related_words}} > {{word.similar_shaped_words}} > word.comment</v-list-item-action-text>
                                </v-list-item-content>

                                <v-list-item-action>
                                    <!-- <v-list-item-action-text v-text=""></v-list-item-action-text> -->
                                    <v-btn small outlined fab color="red lighten-1" @click="onWordDeleteConfirm(word)">
                                        <v-icon>mdi-delete</v-icon>
                                    </v-btn>
                                </v-list-item-action>
                            </template>
                        </v-list-item>
                        <v-divider v-if="index + 1 < words.length" :key="index"></v-divider>
                    </template>
                </v-list-item-group>

                <div v-else class="d-flex pa-2">
                    <v-btn color="pink" width="100%" @click="onNewWordAdd">
                        添加该单词到单词库
                    </v-btn>
                </div>
            </v-list>
        </v-card>

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
        words: [],
        dialog: false,
        snackbar: {
            showed: false,
            color: 'success',
            timeout: 1000,
            message: "Snack bar message!"
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
            timeout = timeout || 1000;
            clearTimeout(this.timeout);
            this.timeout = setTimeout(() => {
                this.$axios
                    .get(
                        `/backend/words/fuzzy?keyword=${keyword}&skip=0&limit=20`
                    )
                    .then(response => {
                        if (response.status === 200 && response.data.rc === 0) {
                            // 调用 callback 返回建议列表的数据
                            this.words = response.data.data;
                        } else {
                            // console.error(response);
                        }
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
                        vm.snackbar = {
                            showed: true,
                            color: "success",
                            message: response.data.msg
                        };
                        clearTimeout(vm.timeout2);
                        vm.timeout2 = setTimeout(() => {
                            vm.snackbar.showed = false;
                        }, 1000);
                    } else {
                        vm.snackbar = {
                            showed: true,
                            color: "error",
                            message: response.data.msg
                        };
                        clearTimeout(vm.timeout2);
                        vm.timeout2 = setTimeout(() => {
                            vm.snackbar.showed = false;
                        }, 1000);
                    }
                });
        }
    },
    created() {
        // queryString = queryString || ''
        let vm = this;
        this.$axios
            .get(`/backend/words/fuzzy?keyword=${this.keyword}&skip=0&limit=20`)
            .then(response => {
                if (response.status === 200 && response.data.rc === 0) {
                    // 调用 callback 返回建议列表的数据
                    this.words = response.data.data;
                } else {
                    vm.alert = {
                        showed: true,
                        type: "error",
                        message: response.data.msg
                    };
                    clearTimeout(vm.timeout);
                    vm.timeout = setTimeout(() => {
                        vm.alert.showed = false;
                    }, 1000);
                }
            });
    }
};
</script>

<style lang="scss">
</style>
