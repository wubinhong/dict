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
                        :label="`阅读延时`"
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
                    <v-row>
                        <v-col>
                            <v-text-field v-model="separator" label="分隔符"></v-text-field>
                        </v-col>
                        <v-col>
                            <v-combobox
                                label="Voice"
                                v-model="utter.voice"
                                :items="availableVoices"
                                :item-text="item => item.lang + `: ` + item.name"
                                return-object
                            ></v-combobox>
                        </v-col>
                    </v-row>
                </v-form>
            </v-card-text>
            <v-card-actions>
                <v-btn text @click="speakOut">{{speakCaption}}</v-btn>
                <v-btn text @click="words = []; speakWords()">Stop</v-btn>
            </v-card-actions>
        </v-card>
    </v-container>
</template>

<script>
import { mapMutations } from "vuex";

export default {
    data: () => ({
        speakText: "",
        words: [],
        speakCaption: "Speak",
        separator: ",",
        availableVoices: [],
        utter: new SpeechSynthesisUtterance(),
        wordDelay: 1
    }),
    methods: {
        ...mapMutations(["showSnackbar"]),
        speakWords() {
            if (this.words.length > 0) {
                if (this.speakCaption === "Speaking") {
                    this.utter.text = this.words.shift(0);
                    window.speechSynthesis.speak(this.utter);
                    // Resolve speak's asynchronous problem
                    this.utter.onend = () => {
                        // Take effect instantly for last iteration
                        if (this.words.length === 0) {
                            this.speakWords();
                        } else {
                            setTimeout(() => {
                                this.speakWords();
                            }, this.wordDelay * 1000);
                        }
                    };
                }
            } else {
                this.speakCaption = "Speak";
            }
        },
        speakOut() {
            if (!this.speakText) {
                this.showSnackbar({
                    color: "error",
                    message: "Please input text for speaker!"
                });
            } else {
                if (this.words.length == 0) {
                    this.words = [];
                    this.speakText
                        .replace(/(\r\n|\n|\r|>|:)/g, this.separator)
                        .split(this.separator)
                        .forEach(w => {
                            w = w.trim();
                            if (w) {
                                this.words.push(w);
                            }
                        });
                    this.speakCaption = "Speaking";
                    this.speakWords();
                } else if (this.speakCaption === "Speaking") {
                    this.speakCaption = "Pause";
                } else if (this.speakCaption === "Pause") {
                    this.speakCaption = "Speaking";
                    this.speakWords();
                }
            }
        }
    },
    created() {
        let vm = this;
        function initVoice() {
            vm.availableVoices = window.speechSynthesis
                .getVoices()
                .filter(v => v.lang.match(/^en-/g));
            if (vm.availableVoices.length === 0) {
                vm.showSnackbar({
                    color: "error",
                    message: "No speaker voice found for en-!"
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
