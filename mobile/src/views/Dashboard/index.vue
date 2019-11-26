<template>
    <!-- class="fill-height" can make child element justify to center in verticle -->
    <!-- <v-container class="fill-height" fluid> -->
    <v-container>
        <v-row>
            <v-col cols="12">
                <!-- <v-text-field color="success" loading disabled dark></v-text-field> -->
                <v-text-field v-model="keyword" label="请输入单词">
                    <!-- <v-icon slot="append" color="red">mdi-plus</v-icon> -->
                    <v-icon slot="prepend" color="green">mdi-magnify</v-icon>
                </v-text-field>

                <v-simple-table dense>
                    <template v-slot:default>
                        <thead>
                            <tr>
                                <th class="text-left">Name</th>
                                <th class="text-left">词根</th>
                                <th class="text-left">中文</th>
                                <th class="text-left">同义词</th>
                                <th class="text-left">相关词</th>
                                <th class="text-left">近形词</th>
                                <th class="text-left">备注</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(item, index) in desserts" :key="index" @click="go(item)">
                                <td>{{ item.name }}</td>
                                <td>{{ item.derivation }}</td>
                                <td>{{ item.chinese }}</td>
                                <td>{{ item.thesauri }}</td>
                                <td>{{ item.related_words }}</td>
                                <td>{{ item.similar_shaped_words }}</td>
                                <td>{{ item.comment }}</td>
                            </tr>
                        </tbody>
                    </template>
                </v-simple-table>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
export default {
    data: () => ({
        keyword: "",
        desserts: [
            {
                name: "Frozen",
                derivation: "Fron + zen",
                chinese: "冻结",
                thesauri: "freeze",
                related_words: "ice",
                similar_shaped_words: "forest",
                comment: "备注"
            },
            {
                name: "Frozen",
                derivation: "Fron + zen",
                chinese: "冻结",
                thesauri: "freeze",
                related_words: "ice",
                similar_shaped_words: "forest",
                comment: "备注"
            },
            {
                name: "Frozen",
                derivation: "Fron + zen",
                chinese: "冻结",
                thesauri: "freeze",
                related_words: "ice",
                similar_shaped_words: "forest",
                comment: "备注"
            },
            {
                name: "Frozen",
                derivation: "Fron + zen",
                chinese: "冻结",
                thesauri: "freeze",
                related_words: "ice",
                similar_shaped_words: "forest",
                comment: "备注"
            }
        ]
    }),
    methods: {
        go(item) {
            // console.log(item);
            this.$router.push({path: `/dashboard/word/${item.name}`, query: item});
        }
    }
};
</script>

<style lang="scss">

</style>
