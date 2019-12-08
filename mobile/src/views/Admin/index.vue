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
                    ref="queryInput"
                    label="请输入关键字，支持按用户名、昵称还有token模糊匹配"
                    filled
                    shaped
                    :loading="loading"
                >
                    <!-- <v-icon slot="prepend" color="green">mdi-magnify</v-icon> -->
                    <v-icon slot="append">mdi-magnify</v-icon>
                </v-text-field>

                <v-btn fab fixed top right color="indigo" class="add-btn" @click="go()">
                    <v-icon dark>mdi-plus</v-icon>
                </v-btn>

                <v-simple-table fixed-header height="700px">
                    <template v-slot:default>
                        <thead>
                            <tr>
                                <th class="text-left">Name</th>
                                <th class="text-left">详情</th>
                                <th class="text-left">操作</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(admin, index) in admins" :key="index">
                                <td>{{ admin.name }}</td>
                                <td>
                                    <ul>
                                        <li>{{ admin.nick }}</li>
                                        <li>{{ admin.token }}</li>
                                        <li>{{ admin.login_time }}</li>
                                    </ul>
                                </td>
                                <td>
                                    <v-btn color="indigo" fab small @click="go(admin._id)">
                                        <v-icon>mdi-pencil</v-icon>
                                    </v-btn>
                                    <v-btn color="pink" fab small @click="onDeleteConfirm(admin._id)">
                                        <v-icon>mdi-delete</v-icon>
                                    </v-btn>
                                </td>
                            </tr>
                            <tr v-if="!loading && !noMoreData" @click="loadMoreData">
                                <td colspan="3">
                                    <v-alert
                                        :color="`success`"
                                        style="margin: 16px 0; text-align: center; cursor: pointer;"
                                        outlined
                                        text
                                    >点击加载更多数据。。。</v-alert>
                                </td>
                            </tr>
                        </tbody>
                    </template>
                </v-simple-table>
            </v-col>
        </v-row>

        <v-row justify="center">
            <v-dialog v-model="dialog" persistent max-width="320">
                <v-card>
                    <v-card-title class="headline">删除管理员！</v-card-title>
                    <v-card-text>此操作将永久删除该管理员, 是否继续?</v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="green darken-1" text @click="onDelete">确定</v-btn>
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
        loading: true,
        admins: [],
        dialog: false,
        deleteId: ""
    }),
    methods: {
        ...mapMutations(["showSnackbar"]),
        go(id) {
            // console.log(word);
            this.$router.push({
                name: `adminDetail`,
                query: { id: id }
            });
        },
        scrollAdmins(admins, keyword, skip, cb) {
            keyword = keyword.trim();
            this.$axios
                .get(
                    `/backend/api/admins/fuzzy?keyword=${keyword}&skip=${skip}&limit=${this.limit}`
                )
                .then(response => {
                    if (response.data.rc === 0) {
                        // 调用 callback 返回建议列表的数据
                        admins.push(...response.data.data);
                        if (response.data.data.length < this.limit) {
                            this.noMoreData = true;
                        } else {
                            this.noMoreData = false;
                        }
                    }
                    if (cb) {
                        cb(response.data.data, admins);
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
                this.scrollAdmins([], keyword, this.skip, ajaxAdmins => {
                    this.admins = ajaxAdmins;
                    this.loading = false;
                });
            }, timeout);
        },
        loadMoreData() {
            if (this.noMoreData) {
                this.showSnackbar({
                    color: "error",
                    message: "No more data!"
                });
            } else {
                this.skip += this.limit;
                this.scrollAdmins(this.admins, this.keyword, this.skip);
            }
        },
        onDeleteConfirm(_id) {
            this.dialog = true;
            this.deleteId = _id;
        },
        onDelete() {
            let vm = this;
            this.$axios
                .delete(`/backend/api/admins/${this.deleteId}`)
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
    }
};
</script>

<style lang="scss" scoped>
.add-btn {
    margin-top: 70px;
}
@media screen and (max-width: 375px) {
    .add-btn {
        margin-top: 60px;
    }
}
</style>
