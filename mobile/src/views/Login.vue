<template>
    <v-app>
        <v-content>
            <v-container class="fill-height" fluid>
                <v-row align="center" justify="center">
                    <v-col cols="12" sm="8" md="4">
                        <v-card class="elevation-12">
                            <v-toolbar color="primary" dark flat>
                                <v-toolbar-title>欢迎登录</v-toolbar-title>
                                <v-spacer />
                            </v-toolbar>
                            <v-card-text>
                                <v-form>
                                    <v-text-field
                                        label="Login"
                                        v-model="name"
                                        type="text">
                                        <v-icon slot="prepend">mdi-account</v-icon>
                                        </v-text-field>

                                    <v-text-field
                                        label="Password"
                                        v-model="password"
                                        type="password">
                                        <v-icon slot="prepend">mdi-lock</v-icon>
                                    </v-text-field>
                                </v-form>
                            </v-card-text>
                            <v-card-actions>
                                <v-spacer />
                                <v-btn color="primary" ref="loginBtn" @click="login">登录</v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-col>
                </v-row>
            </v-container>
        </v-content>
    </v-app>
</template>

<script>
import { mapMutations } from "vuex";

export default {
    data: () => ({
        name: '',
        password: ''
    }),
    methods: {
        ...mapMutations(["showSnackbar"]),
        login() {
            if(this.name && this.password) {
                this.$axios
                    .post(`/backend/api/auth/login`, {
                        name: this.name, password: this.password
                    })
                    .then(response => {
                        if (response.data.rc === 0) {
                            localStorage.setItem('admin', JSON.stringify(response.data.data));
                           this.$router.push('/')
                            // window.location.href = '/';
                        }
                    });
            } else {
                this.showSnackbar({
                    color: "error",
                    message: '用户名、密码必填'
                });
            }
        }
    },
    created() {
        this.$vuetify.theme.dark = true;
    },
    mounted: function() {
        window.onkeydown = e => {
            // 用户按 "enter"后，自动提交表单
            if (e.key === "Enter") {
                this.$refs.loginBtn.click(document.createEvent("MouseEvent"));
            }
        };
    }
};
</script>