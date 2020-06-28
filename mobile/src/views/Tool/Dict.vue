<template>
    <v-container>
        <v-card>
            <v-card-text>
                <v-form ref="form">
                    <v-text-field v-model="keyword" :counter="30" label="输入查询关键字"></v-text-field>
                    <v-row>
                        <v-col cols="12" md="6" sm="6">
                            <v-text-field v-model="page" label="Page" type="number" required dense></v-text-field>
                        </v-col>
                        <v-col cols="12" md="6" sm="6">
                            <v-text-field v-model="limit" label="Size" type="number" required dense></v-text-field>
                        </v-col>
                    </v-row>
                </v-form>
            </v-card-text>
            <v-card-actions>
                <v-btn text color="white" @click="queryDcit(keyword)">Search</v-btn>
                <v-btn text color="success" @click="injectWords()">Inject</v-btn>
            </v-card-actions>
        </v-card>
        <br />

        <v-card>
            <v-chip
                v-for="(word, index) in words"
                v-bind:key="index"
                link
                small
                class="ma-2"
            >{{word}}</v-chip>
        </v-card>
    </v-container>
</template>

<script>
export default {
    data: () => ({
        keyword: "",
        words: [],
        page: 0,
        limit: 50
    }),
    computed: {
        skip: function() {
            return this.page * this.limit;
        }
    },
    methods: {
        injectWords() {
            this.$router.push({
                path: "/tool",
                query: { dictKeyword: this.keyword, dictSkip: this.skip, dictLimit: this.limit }
            });
        },
        queryDcit(keyword, timeout, cb) {
            // 用户输入停顿后再请求，而不是输入有变化就请求，防止频繁请求服务器
            timeout = timeout || 500;
            clearTimeout(this.timeout);
            this.timeout = setTimeout(() => {
                keyword = keyword ? keyword.trim() : "";
                this.$axios
                    .get(
                        `/backend/api/words/fuzzy?keyword=${keyword}&skip=${this.skip}&limit=${this.limit}`
                    )
                    .then(response => {
                        if (response.data.rc === 0) {
                            // 调用 callback 返回建议列表的数据
                            this.words = [];
                            response.data.data.forEach(element => {
                                this.words.push(element.name);
                            });
                        }
                        if (cb) {
                            cb(response.data.data, this.words);
                        }
                    });
            }, timeout);
        }
    },
    created() {
        this.queryDcit(this.keyword, 0);
    }
};
</script>
