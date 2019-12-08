<template>
    <v-container>
        <v-row>
            <v-col>
                <v-hover>
                    <template v-slot="{ hover }">
                        <v-card :elevation="hover ? 24 : 6" class="mx-auto pa-6">
                            <v-form ref="form" v-model="valid" lazy-validation>
                                <v-text-field v-model="admin.name" :rules="nameRules" label="用户名"></v-text-field>
                                <v-text-field v-model="admin.nick" label="昵称"></v-text-field>
                                <v-text-field v-model="admin.new_password" label="密码，系统默认不显示密码，要重置密码的话，可以直接填写"></v-text-field>
                                <v-btn
                                    :disabled="!valid"
                                    color="primary"
                                    class="mr-4"
                                    @click="onSave"
                                    ref="submitBtn"
                                >保存</v-btn>
                                <v-btn color="warning" class="mr-4" @click="onReset">重置</v-btn>
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
        admin: {},
        nameRules: [
            v => !!v || "Name is required",
            v =>
                (v && v.length <= 100) ||
                "Name must be less than 100 characters"
        ],
        ctrlKeyHoldOn: false
    }),

    methods: {
        onSave() {
            if (this.$refs.form.validate()) {
                let vm = this;
                let w = this.admin;
                this.$axios
                    .put(`/backend/api/admins`, w)
                    .then(response => {
                        if (response.status === 200 && response.data.rc === 0) {
                            vm.$router.go(-1);
                        }
                    });
            }
        },
        onReset() {
            this.$refs.form.reset();
        }
    },
    created() {
        let id = this.$route.query.id;
        if (id) {
            // Get Admin from remote server.
            this.$axios.get(`/backend/api/admins/${id}`).then(res => {
                if (res.data.rc === 0 && res.data.data) {
                    this.admin = res.data.data;
                } else {
                    this.admin = {};
                }
            });
        } else {
            // 新建
            this.admin = {};
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
