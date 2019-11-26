<template>
    <!-- class="fill-height" can make child element justify to center in verticle -->
    <!-- <v-container class="fill-height" fluid> -->
    <v-container>
        <v-row>
            <v-col cols="12">
                <!-- <v-text-field color="success" loading disabled dark></v-text-field> -->
                <v-text-field
                    v-model="keyword"
                    @input="querySearch(keyword)"
                    label="请输入单词"
                    filled
                    shaped
                >
                    <!-- <v-icon slot="prepend" color="green">mdi-magnify</v-icon> -->
                    <v-icon slot="append" color="red">mdi-magnify</v-icon>
                </v-text-field>

                <v-simple-table dense fixed-header height="450px" v-if="words.length !== 0">
                    <template v-slot:default>
                        <thead>
                            <tr>
                                <th class="text-left">Name</th>
                                <th class="text-left">详情</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(word, index) in words" :key="index" @click="go(word)">
                                <td>{{ word.name }}</td>
                                <td>
                                    {{ word.derivation }} > {{ word.chinese }} > {{ word.thesauri }} >
                                    {{ word.related_words }} > {{ word.similar_shaped_words }} > {{ word.comment }}
                                </td>
                            </tr>
                        </tbody>
                    </template>
                </v-simple-table>

                <v-btn v-else color="pink" dark fab @click="onAddNewWord">
                        <v-icon>mdi-plus</v-icon>
                    </v-btn>

            </v-col>
        </v-row>
    </v-container>
</template>

<script>
export default {
    data: () => ({
        keyword: "",
        words: []
    }),
    methods: {
        go(word) {
            // console.log(word);
            this.$router.push({
                path: `/dashboard/word`,
                query: word
            });
        },
        querySearch(keyword) {
            // 用户输入停顿后再请求，而不是输入有变化就请求，防止频繁请求服务器
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
                            console.log(this)
                        } else {
                            // console.error(response);
                        }
                    });
            }, 1000);
        },
        onAddNewWord() {
            this.$router.push({name: 'wordDetail', query: {name: this.keyword}})
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
                } else {
                    // console.error(response);
                }
            });
    }
};
</script>

<style lang="scss">
</style>
