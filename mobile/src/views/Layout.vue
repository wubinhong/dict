<template>
    <!-- 该页面为登录进去后的布局页面 -->
    <v-app>
        <v-navigation-drawer v-model="drawer" app clipped>
            <v-list dense>
                <!-- <v-list-item link @click="$router.push('/home/dashboard')"> -->
                <v-list-item link @click="go('/dashboard')">
                    <v-list-item-action>
                        <v-icon>mdi-view-dashboard</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Dashboard</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item link @click="go('/dashboard2')">
                    <v-list-item-action>
                        <v-icon>mdi-view-dashboard</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Dashboard2</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item link @click="go('/tool')">
                    <v-list-item-action>
                        <v-icon>mdi-account-supervisor</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Tool</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item link @click="go('/admin')">
                    <v-list-item-action>
                        <v-icon>mdi-account-supervisor</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Admin</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item link @click="go('/home/settings')">
                    <v-list-item-action>
                        <v-icon>mdi-settings</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Settings</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item link @click="go('/about')">
                    <v-list-item-action>
                        <v-icon>mdi-settings</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>About Page</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item link @click="go('/login')">
                    <v-list-item-action>
                        <v-icon>mdi-settings</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Login Page</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>

        <v-app-bar app clipped-left :collapse-on-scroll="collapseOnScroll">
            <v-app-bar-nav-icon @click.stop="drawer = !drawer"/>
            <v-toolbar-title>私人字典({{admin.name}})</v-toolbar-title>
            <v-spacer/>
            <v-switch v-model="collapseOnScroll" inset hide-details :label="``"></v-switch>
            <v-btn icon color="pink" @click="logout">
                <v-icon>mdi-exit-to-app</v-icon>
            </v-btn>
        </v-app-bar>

        <v-content>
            <router-view/>
        </v-content>

        <v-footer app v-show="false">
            <span>&copy; 2019</span>
        </v-footer>
    </v-app>
</template>

<script>
    export default {
        props: {},
        data: () => ({
            drawer: null,
            collapseOnScroll: false,
            admin: localStorage.getItem(window.location.host + '_admin') ? JSON.parse(localStorage.getItem(window.location.host + '_admin')) : {}
        }),
        methods: {
            go(path) {
                if (this.$route.path !== path) {
                    this.$router.push({path: path});
                }
            },
            logout() {
                this.$axios.delete(`/backend/api/auth/logout`).then(response => {
                    if (response.data.rc === 0) {
                        localStorage.removeItem(window.location.host + '_admin');
                        window.location.href = '/login';
                    }
                });
            }
        },
        created() {
            this.$vuetify.theme.dark = true;
        }
    };
</script>
