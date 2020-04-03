<template>
    <v-container>
        <v-card>
            <v-card-text>
                <v-form ref="form" v-model="valid" lazy-validation>
                    <v-text-field
                        v-model="history.title"
                        :rules="titleRules"
                        :counter="30"
                        label="输入历史标题"
                        required
                    ></v-text-field>
                    <v-textarea
                        v-model="history.content"
                        :rules="contentRules"
                        clearable
                        clear-icon="mdi-close-circle"
                        row-height="2"
                        auto-grow
                        label="输入历史内容"
                    ></v-textarea>
                </v-form>
            </v-card-text>
            <v-card-actions>
                <v-btn
                    text
                    color="success"
                    :disabled="!valid"
                    @click="saveHistoryForm(history)"
                >Save</v-btn>
            </v-card-actions>
        </v-card>
        <br />

        <v-card>
            <v-text-field
                v-model="keyword"
                @input="queryHistory(keyword)"
                ref="queryInput"
                label="请输入单词，支持按内容模糊查询"
                filled
                hide-details
                clearable
                clear-icon="mdi-close-circle"
                :loading="loading"
            ></v-text-field>
            <v-list>
                <v-list-group v-for="h in histories" :key="h.title" prepend-icon="mdi-basket-fill">
                    <template v-slot:activator>
                        <v-list-item-content>
                            <v-list-item-title v-text="h.title"></v-list-item-title>
                        </v-list-item-content>
                    </template>
                    <v-list-item>
                        <v-list-item-content>
                            <v-card-text>
                                <pre v-if="!historyEditable">{{h.content}}</pre>
                                <v-textarea
                                    v-if="historyEditable"
                                    v-model="h.content"
                                    clearable
                                    clear-icon="mdi-close-circle"
                                    row-height="2"
                                    auto-grow
                                    label="历史内容"
                                ></v-textarea>
                            </v-card-text>
                            <v-card-actions>
                                <v-btn text color="blue" @click="injectWords(h._id)">Inject</v-btn>
                                <v-btn
                                    text
                                    color="success"
                                    v-if="!historyEditable"
                                    @click="historyEditable = !historyEditable"
                                >Edit</v-btn>
                                <v-btn
                                    text
                                    color="success"
                                    v-else
                                    @click="saveHistory(h); historyEditable = !historyEditable"
                                >Save</v-btn>
                                <v-btn text color="error" @click="deleteConfirm(h._id)">Delete</v-btn>
                            </v-card-actions>
                        </v-list-item-content>
                    </v-list-item>
                </v-list-group>
            </v-list>
        </v-card>

        <v-dialog v-model="dialogShowed" persistent max-width="320">
            <v-card>
                <v-card-title class="headline">删除历史！</v-card-title>
                <v-card-text>此操作将永久删除该条历史记录, 是否继续?</v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="green darken-1" text @click="deleteHistory">确定</v-btn>
                    <v-btn color="green darken-1" text @click="dialogShowed = false">取消</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-container>
</template>

<script>
import { mapMutations } from "vuex";

export default {
    data: () => ({
        valid: true,
        titleRules: [
            v => !!v || "Title is required",
            v =>
                (v && v.length <= 30) || "Title must be less than 30 characters"
        ],
        contentRules: [v => !!v || "Content is required"],
        history: {},
        keyword: "",
        skip: 0,
        limit: 20,
        noMoreData: false,
        loading: true,
        histories: [],
        historyEditable: false,
        dialogShowed: false,
    }),
    methods: {
        ...mapMutations(["showSnackbar"]),
        injectWords(historyId) {
            this.$router.push({
                path: "/tool",
                query: { historyId: historyId }
            });
        },
        saveHistoryForm(history) {
            if (this.$refs.form.validate()) {
                this.saveHistory(history, res => {
                    if (res.status === 200 && res.data.rc === 0) {
                        this.$refs.form.reset();
                    }
                });
            }
        },
        saveHistory(history, cb) {
            this.$axios
                .put(`/backend/api/tool/histories`, history)
                .then(response => {
                    if (response.status === 200 && response.data.rc === 0) {
                        this.queryHistory(this.keyword, 0);
                        this.showSnackbar({
                            color: "success",
                            message: "Save history successfully!"
                        });
                    }
                    if (cb) {
                        cb(response);
                    }
                });
        },
        deleteConfirm(id) {
            this.dialogShowed = true;
            this.deleteHistoryId = id;
        },
        deleteHistory() {
            this.$axios
                .delete(`/backend/api/tool/history/${this.deleteHistoryId}`)
                .then(response => {
                    if (response.status === 200 && response.data.rc === 0) {
                        this.dialogShowed = false;
                        this.queryHistory(this.keyword, 0); // Reload data
                        this.showSnackbar({
                            color: "success",
                            message: response.data.msg
                        });
                    }
                });
        },
        scrollHistories(histories, keyword, skip, cb) {
            keyword = keyword ? keyword.trim() : "";
            this.$axios
                .get(
                    `/backend/api/tool/histories/fuzzy?keyword=${keyword}&skip=${skip}&limit=${this.limit}`
                )
                .then(response => {
                    if (response.data.rc === 0) {
                        // 调用 callback 返回建议列表的数据
                        histories.push(...response.data.data);
                    }
                    if (cb) {
                        cb(response.data.data, histories);
                    }
                });
        },
        queryHistory(keyword, timeout) {
            // 用户输入停顿后再请求，而不是输入有变化就请求，防止频繁请求服务器
            timeout = timeout || 500;
            clearTimeout(this.timeout);
            this.timeout = setTimeout(() => {
                this.loading = true;
                this.skip = 0;
                this.noMoreData = false;
                this.scrollHistories([], keyword, this.skip, ajaxHistories => {
                    this.selected = [];
                    this.histories = ajaxHistories;
                    this.loading = false;
                });
            }, timeout);
        }
    },
    created() {
        this.queryHistory(this.keyword, 0);
    },
    mounted() {
        // Infinite scroll implement
        window.onscroll = () => {
            let element = document.documentElement;
            // 是用差值解决 huawei pad pro 滑动时，无法触底的问题
            let offset =
                element.offsetHeight - (element.scrollTop + window.innerHeight);
            if (!this.noMoreData && offset < 2) {
                //appending data to the array
                this.skip += this.limit;
                this.scrollHistories(
                    this.histories,
                    this.keyword,
                    this.skip,
                    ajaxWords => {
                        if (ajaxWords.length === 0) {
                            this.noMoreData = true;
                        }
                    }
                );
            }
        };
    }
};
</script>

<style lang="scss" scoped>
// 去掉不能选文本，不然mac不能使用三个手指点击look up单词了
.v-list-item {
    user-select: text;
}
</style>