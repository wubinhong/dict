<template>
    <v-container>
        <v-card class="mx-auto" max-width="80%">
            <v-card-text>
                <p class="display-1 text--primary">Speak Out Tool</p>
                <v-form>
                    <v-textarea
                        v-model="utter.text"
                        clearable
                        clear-icon="mdi-close-circle"
                        row-height="2"
                        auto-grow
                        label="输入朗读文本"
                    ></v-textarea>
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
        utter: new SpeechSynthesisUtterance()
    }),
    methods: {
        ...mapMutations(["showSnackbar"]),
        speakOut() {
            if (!this.utter.text) {
                this.showSnackbar({
                    color: "error",
                    message: "Please input text for speaker!"
                });
            }
            window.speechSynthesis.speak(this.utter);
        }
    },
    created() {
        let vm = this;
        function initVoice() {
            let availableVoices = window.speechSynthesis
                .getVoices()
                .filter(v => v.name === "Google UK English Female");
            if (!availableVoices) {
                vm.showSnackbar({
                    color: "error",
                    message:
                        "No speaker voice found for Google UK English Male!"
                });
            } else {
                vm.utter.voice = availableVoices[0];
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
