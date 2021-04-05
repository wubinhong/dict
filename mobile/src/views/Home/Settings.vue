<template>
    <v-content>
        <v-container>
            <v-card class="mx-auto pa-6">
                <v-card-title class="headline">Storage设置</v-card-title>
                <v-form ref="form" lazy-validation>
                    <v-text-field v-model="storage.rand_num_bit" type="number" label="随机数字位数"></v-text-field>
                    <v-switch
                        v-model="storage.updated_time_on"
                        :label="`是否更新时间`"
                        inset
                    ></v-switch>
                    <v-slider
                        v-model="storage.default_hardship"
                        :label="`单词默认难度`"
                        thumb-label
                        style="padding: 0"
                        color="orange darken-3"
                        thumb-color="red"
                        prepend-icon="mdi-shield-star-outline"
                    >
                        <template v-slot:append>
                            <v-tooltip top>
                                <template v-slot:activator="{ on }">
                                    <v-icon v-on="on"
                                        >mdi-help-circle-outline</v-icon
                                    >
                                </template>
                                对单词的陌生程度，值越大，在列表里排名越靠前！
                            </v-tooltip>
                        </template>
                    </v-slider>
                    <v-btn
                        color="primary"
                        class="mr-4"
                        @click="onLocalStorageSave"
                        ref="submitBtn"
                        >保存</v-btn
                    >
                    <v-btn color="teal" class="mr-4" @click="$router.go(-1)">
                        <v-icon dark>mdi-arrow-left</v-icon>返回
                    </v-btn>
                </v-form>
            </v-card>
        </v-container>
    </v-content>
</template>

<script>
import { mapMutations } from "vuex";

export default {
    data: () => {
        return {
            msg: "个人设置",
            storage: {
                default_hardship: localStorage.getItem("default_hardship") || 0,
                rand_num_bit: localStorage.getItem('default_rand_num_bit')
            },
        };
    },
    methods: {
        ...mapMutations(["showSnackbar"]),
        onLocalStorageSave() {
            localStorage.setItem(
                "default_hardship",
                this.storage.default_hardship
            );
            localStorage.setItem(
                "default_updated_time_on",
                this.storage.updated_time_on
            );
            localStorage.setItem(
                "default_rand_num_bit",
                this.storage.rand_num_bit
            );
            this.showSnackbar({ color: "success", message: "保存成功！" });
        },
    },
    created() {
        let on = localStorage.getItem("default_updated_time_on") || false;
        if (typeof on === "string") {
            on = eval(on);
        }
        this.storage.updated_time_on = on;
    },
};
</script>
