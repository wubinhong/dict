<template>
    <v-content>
        <v-container>
            <v-card class="mx-auto pa-6">
                <v-card-title class="headline">Storage设置</v-card-title>
                <v-form ref="form" lazy-validation>
                    <v-row>
                        <v-col>
                            <v-text-field
                                v-model="storage.random_num_min"
                                type="number"
                                label="最小随机数字位数"
                            ></v-text-field>
                        </v-col>
                        <v-col>
                            <v-text-field
                                v-model="storage.random_num_max"
                                type="number"
                                label="最大随机数字位数"
                            ></v-text-field>
                        </v-col>
                    </v-row>
                    <v-switch
                        v-model="storage.updated_time_on"
                        :label="`是否更新时间`"
                        inset
                    ></v-switch>
                    <v-slider
                        v-model="storage.hardship"
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
            storage: JSON.parse(localStorage.getItem("setting")) || {},
        };
    },
    methods: {
        ...mapMutations(["showSnackbar"]),
        onLocalStorageSave() {
            localStorage.setItem("setting", JSON.stringify(this.storage));
            this.showSnackbar({ color: "success", message: "保存成功！" });
        },
    },
    created() {
        if (!JSON.parse(localStorage.getItem("setting"))) {
            localStorage.setItem("setting", "{}");
        }
    },
};
</script>
