<template>
    <!-- class="fill-height" can make child element justify to center in verticle -->
    <!-- <v-container class="fill-height" fluid> -->
    <v-container>
        <v-card max-width="700" class="mx-auto">
            <v-text-field
                v-model="keyword"
                @input="querySearch(keyword)"
                ref="queryInput"
                label="请输入单词，支持按所有字段模糊查询"
                filled
                hide-details
                clearable
                clear-icon="mdi-close-circle"
                :loading="loading"
            >
                <!-- <v-icon slot="prepend" color="green">mdi-magnify</v-icon> -->
                <v-icon slot="append" v-show="!keyword">mdi-magnify</v-icon>
                <v-icon slot="append" v-show="keyword" @click="play(keyword)">mdi-volume-high</v-icon>
            </v-text-field>

            <v-list two-line dense>
                <v-list-item-group
                    v-model="selected"
                    multiple
                    v-if="words && words.length !== 0"
                    active-class="blue--text"
                >
                    <template v-for="(word, index) in words">
                        <v-list-item :key="word.name">
                            <template v-slot:default="{ active, toggle }">
                                <v-list-item-content @click="play(word.name, active)">
                                    <div>
                                        <v-list-item-title v-text="word.name"></v-list-item-title>
                                        <v-list-item-subtitle v-text="word.derivation"></v-list-item-subtitle>
                                    </div>
                                    <v-list-item-action-text
                                        v-show="showDetail"
                                    >{{word.chinese}} > {{word.thesauri}} > {{word.related_words}} > {{word.similar_shaped_words}} > {{word.comment}} > {{word.hardship}}</v-list-item-action-text>
                                </v-list-item-content>

                                <!-- <v-list-item-action>
                                    <v-list-item-action-text v-text="xx"></v-list-item-action-text>
                                    <v-btn small outlined fab color="red lighten-1">
                                        <v-icon>mdi-delete</v-icon>
                                    </v-btn>
                                </v-list-item-action>-->
                            </template>
                        </v-list-item>
                        <v-divider v-if="index + 1 < words.length" :key="index"></v-divider>
                    </template>
                </v-list-item-group>

                <!-- 解决组件初次加载时，页面会闪一下添加单词按钮 -->
                <div v-else-if="!loading" class="d-flex pa-2">
                    <v-btn color="indigo" width="100%" @click="onNewWordAdd(keyword)">添加该单词到单词库</v-btn>
                </div>
            </v-list>
        </v-card>

        <v-alert
            text
            outlined
            prominent
            type="warning"
            style="margin-top: 20px; text-align: center;"
            border="left"
            v-if="noMoreData"
        >你碰到我底线了！</v-alert>

        <v-speed-dial
            v-model="fab"
            :bottom="`bottom`"
            fixed
            right="right"
            direction="top"
            transition="slide-y-reverse-transition"
        >
            <template v-slot:activator>
                <v-btn v-model="fab" color="blue darken-2" dark fab>
                    <v-icon v-if="fab">mdi-close</v-icon>
                    <v-icon v-else>mdi-settings</v-icon>
                </v-btn>
            </template>
            <v-btn fab dark small color="green" @click="toggleShowWordDetail">
                <v-icon v-if="showDetail">mdi-eye</v-icon>
                <v-icon v-else>mdi-eye-off</v-icon>
            </v-btn>
            <v-btn fab small color="blue" @click="onWordViewConfirm()" v-if="selected.length > 0">
                <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn fab small color="pink" @click="onWordDeleteConfirm()" v-if="selected.length > 0">
                <v-icon>mdi-delete</v-icon>
            </v-btn>
            <v-btn fab dark small color="indigo" @click="onNewWordAdd()">
                <v-icon>mdi-plus</v-icon>
            </v-btn>
            <v-btn fab dark small color="red" @click="scrollToTop">
                <v-icon>mdi-chevron-up</v-icon>
            </v-btn>
        </v-speed-dial>

        <v-row justify="center">
            <v-dialog v-model="dialog2" persistent max-width="320">
                <v-card>
                    <v-card-title class="headline">编辑单词！</v-card-title>
                    <v-card-text>
                        点击编辑以下选中单词
                        <ul v-for="selected_word in selected_words" :key="selected_word.id">
                            <router-link
                                :to="{path: '/dashboard/word', query: {name: selected_word.name}}"
                            >
                                <li>{{selected_word.name}}</li>
                            </router-link>
                        </ul>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="green darken-1" text @click="dialog2 = false">关闭</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-row>
        <v-row justify="center">
            <v-dialog v-model="dialog" persistent max-width="320">
                <v-card>
                    <v-card-title class="headline">删除单词！</v-card-title>
                    <v-card-text>
                        此操作将永久删除以下单词, 是否继续?
                        <ul v-for="selected_word in selected_words" :key="selected_word.id">
                            <li>{{selected_word.name}}</li>
                        </ul>
                    </v-card-text>
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
import { mapMutations } from "vuex";

export default {
    data: () => ({
        keyword: "",
        skip: 0,
        limit: 20,
        noMoreData: false,
        words: [],
        selected: [],
        selected_words: [],
        dialog: false,
        dialog2: false,
        loading: true,
        fab: false
    }),
    computed: {
        showDetail() {
            return this.$store.state.setting.showWordDetail;
        }
    },
    methods: {
        ...mapMutations([
            "showSnackbar",
            "closeSnackbar",
            "toggleShowWordDetail"
        ]),
        play(name, active) {
            if (!active) {
                // 注意：此时的active是上一次的状态，所以需要取反
                new Audio(`/youdao/dictvoice?audio=${name}&type=1`).play();
            }
        },
        scrollWords(words, keyword, skip, cb) {
            keyword = keyword ? keyword.trim() : "";
            this.$axios
                .get(
                    `/backend/api/words/fuzzy?keyword=${keyword}&skip=${skip}&limit=${this.limit}`
                )
                .then(response => {
                    if (response.data.rc === 0) {
                        // 调用 callback 返回建议列表的数据
                        words.push(...response.data.data);
                    }
                    if (cb) {
                        cb(response.data.data, words);
                    }
                });
        },
        querySearch(keyword, timeout) {
            // 用户输入停顿后再请求，而不是输入有变化就请求，防止频繁请求服务器
            timeout = timeout || 500;
            clearTimeout(this.timeout);
            this.timeout = setTimeout(() => {
                this.loading = true;
                this.skip = 0;
                this.noMoreData = false;
                this.scrollWords([], keyword, this.skip, ajaxWords => {
                    this.selected = [];
                    this.words = ajaxWords;
                    this.loading = false;
                });
            }, timeout);
        },
        onNewWordAdd(name) {
            this.$router.push({
                name: "wordDetail",
                query: { name: name }
            });
        },
        onWordViewConfirm() {
            this.selected_words = [];
            this.selected.forEach(idx => {
                this.selected_words.push(this.words[idx]);
            });
            this.dialog2 = true;
        },
        onWordDeleteConfirm() {
            this.selected_words = [];
            this.selected.forEach(idx => {
                this.selected_words.push(this.words[idx]);
            });
            this.dialog = true;
        },
        onWordDelete() {
            let vm = this;
            this.$axios
                .delete(`/backend/api/words/batch`, {
                    data: this.selected_words.map(w => w._id)
                })
                .then(response => {
                    if (response.status === 200 && response.data.rc === 0) {
                        vm.dialog = false;
                        vm.querySearch(vm.keyword, 0); // Reload data
                        this.showSnackbar({
                            color: "success",
                            message: response.data.msg
                        });
                    }
                });
        },
        scrollToTop() {
            window.scrollTo({ top: 0, left: 0, behavior: "smooth" });
        }
    },
    created() {
        this.querySearch(this.keyword, 0);
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
        // Infinite scroll implement
        window.onscroll = () => {
            let element = document.documentElement;
            let reachBottomOfWindow =
                element.scrollTop + window.innerHeight === element.offsetHeight;
            if (!this.noMoreData && reachBottomOfWindow) {
                //appending data to the array
                this.skip += this.limit;
                this.scrollWords(
                    this.words,
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
