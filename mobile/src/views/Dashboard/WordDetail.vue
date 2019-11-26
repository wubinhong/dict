<template>
    <v-container>
        <v-row>
            <v-col>
                <v-form ref="form" v-model="valid" lazy-validation>
                    <v-text-field v-model="word.name" :rules="nameRules" label="单词"></v-text-field>

                    <v-text-field v-model="word.derivation" label="词根"></v-text-field>
                    <v-text-field v-model="word.chinese" label="中文"></v-text-field>
                    <v-text-field v-model="word.thesauri" label="同义词"></v-text-field>
                    <v-text-field v-model="word.related_words" label="相关词"></v-text-field>
                    <v-text-field v-model="word.similar_shaped_words" label="近形词"></v-text-field>
                    <v-text-field v-model="word.comment" label="备注"></v-text-field>

                    <v-btn :disabled="!valid" color="primary" class="mr-4" @click="onWordSave">保存</v-btn>

                    <v-btn color="warning" class="mr-4" @click="onWordReset">重置</v-btn>
                </v-form>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
export default {
    data: () => ({
        valid: true,
        word: {
            thesauri: ''
        },
        nameRules: [
            v => !!v || "Name is required",
            v => (v && v.length <= 10) || "Name must be less than 10 characters"
        ]   
    }),

    methods: {
        onWordSave() {
            // console.log(this.word)
            if (this.$refs.form.validate()) {
                this.snackbar = true;
            }
        },
        onWordReset() {
            this.$refs.form.reset();
        }
    },
    created() {
        this.word = this.$route.query
    },
    mounted: () => {
        // console.log('mounted', this)
    }
};
</script>
