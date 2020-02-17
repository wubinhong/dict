<template>
    <v-container>
        <v-card class="mx-auto" max-width="80%">
            <v-card-text>
                <p class="display-1 text--primary">Speak Out Tool</p>
                <v-form>
                    <v-textarea
                        v-model="speakText"
                        clearable
                        clear-icon="mdi-close-circle"
                        row-height="2"
                        auto-grow
                        label="输入朗读文本"
                    ></v-textarea>
                    <v-slider
                        v-model="wordDelay"
                        :label="`阅读延时（毫秒）`"
                        thumb-label
                        style="padding: 12px 0"
                        color="orange darken-3"
                        thumb-color="red"
                        max="10"
                        prepend-icon="mdi-shield-star-outline"
                    >
                        <template v-slot:append>
                            <v-tooltip top>
                                <template v-slot:activator="{ on }">
                                    <v-icon v-on="on">mdi-help-circle-outline</v-icon>
                                </template>
                                以逗号为分隔，没读完一个词组，停顿读时间
                            </v-tooltip>
                        </template>
                    </v-slider>
                </v-form>
            </v-card-text>
            <v-card-actions>
                <v-btn text @click="speakOut">Speak</v-btn>
            </v-card-actions>
        </v-card>
    </v-container>
</template>

<script>
import { mapMutations } from "vuex";

export default {
    data: () => ({
        speakText: "",
        utter: new SpeechSynthesisUtterance(),
        wordDelay: 1
    }),
    methods: {
        ...mapMutations(["showSnackbar"]),
        speakWords(words) {
            if (words && words.length > 0) {
                this.utter.text = words.shift(0);
                window.speechSynthesis.speak(this.utter);
                setTimeout(() => {
                    this.speakWords(words);
                }, this.wordDelay * 1000);
            }
        },
        speakOut() {
            if (!this.speakText) {
                this.showSnackbar({
                    color: "error",
                    message: "Please input text for speaker!"
                });
            } else {
                let words = this.speakText.replace("\n", ",").split(",");
                // let words = this.speakText.split(',');
                for (let i = 0; i < words.length; i++) {
                    const word = words[i];
                    words[i] = word.trim();
                }
                this.speakWords(words);
            }
        }
    },
    created() {
        let vm = this;
        function initVoice() {
            let availableVoices = window.speechSynthesis
                .getVoices()
                .filter(v => v.lang === "en-US");
            if (availableVoices && availableVoices.length > 0) {
                vm.utter.voice = availableVoices.pop();
            } else {
                vm.showSnackbar({
                    color: "error",
                    message:
                        "No speaker voice found for Google UK English Male!"
                });
            }
        }

        // list of languages is probably not loaded, wait for it
        if (window.speechSynthesis.getVoices().length == 0) {
            window.speechSynthesis.addEventListener(
                "voiceschanged",
                function() {
                    initVoice();
                }
            );
        } else {
            // languages list available, no need to wait
            initVoice();
        }
    },
    mounted() {}
};
</script>
