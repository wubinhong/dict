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

        <v-app-bar app clipped-left>
            <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
            <v-toolbar-title>私人字典</v-toolbar-title>
            <v-spacer />
            <v-btn color="indigo" dark fab small @click="$router.go(-1)">
                <v-icon>mdi-arrow-left</v-icon>
            </v-btn>
        </v-app-bar>

        <v-content>
            <router-view />
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
        drawer: null
    }),
    methods: {
        go(path) {
            if (this.$route.path !== path) {
                this.$router.push({ path: path });
            }
        }
    },
    created() {
        this.$vuetify.theme.dark = true;
    }
};
</script>
