<template>
    <v-container>
        <v-card class="mx-auto" max-width="95%">
            <v-card-text>
                <p class="display-1 text--primary">Speak Out Tool</p>
                <v-form>
                    <v-textarea
                        v-model="speakText"
                        ref="speakTextInput"
                        clearable
                        clear-icon="mdi-close-circle"
                        row-height="2"
                        auto-grow
                        label="输入朗读文本"
                    ></v-textarea>
                    <div v-if="words.length > 0">
                        <v-progress-linear
                            height="25"
                            color="success"
                            striped
                            :value="progressIndex / words.length * 100"
                        >
                            <template>
                                <strong>{{progressIndex}} / {{words.length}}</strong>
                            </template>
                        </v-progress-linear>
                        <v-chip
                            v-for="(word, index) in words"
                            v-bind:key="index"
                            link
                            small
                            class="ma-2"
                            :color="currentIndex === index ? `green` : `undefined`"
                            @click="speakClick(index)"
                            @click:close="remove(index)"
                        >{{word}}</v-chip>
                    </div>
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
                                :disabled="useYoudao"
                                :items="availableVoices"
                                :item-text="item => item.lang + `: ` + item.name"
                                return-object
                            ></v-combobox>
                        </v-col>
                        <v-col>
                            <v-switch
                                v-model="useYoudao"
                                :label="`是否使用有道`"
                                inset
                            ></v-switch>
                        </v-col>
                    </v-row>
                </v-form>
            </v-card-text>
            <v-card-actions>
                <v-btn
                    text
                    ref="speakOutButton"
                    @click="speakOut"
                    :disabled="words.length === 0"
                >{{speakCaption}}</v-btn>
                <v-btn text ref="injectButton" @click="injectWords">Inject</v-btn>
                <v-btn text @click="clearAllTimeout(); words = [];">Clear</v-btn>
                <v-btn text @click="clearAllTimeout(); $router.push('/tool/history')">History</v-btn>
                <v-btn text @click="clearAllTimeout(); $router.push('/tool/dict')">Dict</v-btn>
                <v-btn text @click="randomNum()">Num</v-btn>
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
        currentIndex: -1,
        speakCaption: "Speak",
        timeoutHandlers: [],
        separator: ",",
        availableVoices: [],
        utter: new SpeechSynthesisUtterance(),
        useYoudao: true,
        audio: new Audio(),
        wordDelay: 1,
        arrowJump: 0
    }),
    computed: {
        progressIndex: function() {
            // More flexible to handle the data props
            return this.currentIndex + 1;
        }
    },
    methods: {
        ...mapMutations(["showSnackbar"]),
        injectWords() {
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
        },
        clearAllTimeout() {
            while (this.timeoutHandlers.length > 0) {
                clearTimeout(this.timeoutHandlers.pop());
            }
        },
        nextSpeak(index) {
            // Finish the recursion when iteration reach the end
            if (index + 1 < this.words.length) {
                if (this.speakCaption === "Speaking") {
                    // Clear all time out events to make it mutual exclusive for the concurrency of two events
                    this.clearAllTimeout();
                    // Collect timeout event handlers
                    this.timeoutHandlers.push(
                        setTimeout(() => {
                            this.speak(++index, false);
                        }, this.wordDelay * 1000)
                    );
                }
            } else {
                this.speakCaption = "Speak";
                // this.currentIndex = -1;
            }
        },
        speak(index, clearTimeoutHandle) {
            if (clearTimeoutHandle) {
                this.clearAllTimeout();
            }
            this.speakCaption = "Speaking";
            this.currentIndex = index;
            if (this.availableVoices.length === 0 || this.useYoudao) {
                this.audio.src = `/youdao/dictvoice?audio=${this.words[index]}&type=1`;
                this.audio.play();
                this.audio.onended = () => {
                    this.nextSpeak(index);
                };
            } else {
                this.utter.text = this.words[index];
                window.speechSynthesis.speak(this.utter);
                // Resolve speak's asynchronous problem
                this.utter.onend = () => {
                    this.nextSpeak(index);
                };
            }
        },
        speakClick(index) {
            if (this.currentIndex === index) {
                this.speakOut();
                // Only when tbe program is speaking, it need to reset
                if (this.speakCaption === "Speak") {
                    this.currentIndex = -1;
                }
            } else {
                this.speak(index, true);
            }
        },
        speakOut() {
            if (this.words.length === 0) {
                this.showSnackbar({
                    color: "error",
                    message: "No injection found from input text for speaker!"
                });
            } else {
                if (this.currentIndex === -1) {
                    // Reset to the first one element
                    this.currentIndex = 0;
                }
                if (this.speakCaption === "Speaking") {
                    this.clearAllTimeout();
                    this.speakCaption = "Speak";
                } else if (this.speakCaption === "Speak") {
                    this.speakCaption = "Speaking";
                    this.speak(this.currentIndex, true);
                }
            }
        },
        randomNum() {
            let setting = JSON.parse(localStorage.getItem('setting'));
            let numMin = setting.random_num_min || 0;
            let numMax = setting.random_num_max || 100;
            let arr = [];
            for(let i=0; i<20; i++) {
                let num = numMin + (numMax - numMin) * Math.random();
                arr.push(Math.round(num))
            }
            this.speakText = arr.join(', ');
        }
    },
    created() {
        if (!window.speechSynthesis) {
            // For browsers' compatibility
            return;
        }
        let vm = this;
        function initVoice() {
            vm.availableVoices = window.speechSynthesis
                .getVoices()
                .filter(v => v.lang.match(/^en-/g));
            if (vm.availableVoices.length === 0) {
                vm.showSnackbar({
                    color: "error",
                    message:
                        "No speaker voice found for en-, system will take youdao as an alternate"
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

        // Load from history by history id
        let historyId = this.$route.query.historyId;
        if (historyId) {
            // Get word from remote server.
            this.$axios
                .get(`/backend/api/tool/history/${historyId}`)
                .then(res => {
                    if (res.data.rc === 0 && res.data.data) {
                        this.speakText = res.data.data.content;
                    }
                });
        }
        // Load from dict by dictSkip and dictLimit
        let dictKeyword = this.$route.query.dictKeyword;
        let dictSkip = this.$route.query.dictSkip;
        let dictLimit = this.$route.query.dictLimit;
        if (dictLimit) {
            // Get word from remote server.
            this.$axios
                .get(
                    `/backend/api/words/fuzzy?keyword=${dictKeyword}&skip=${dictSkip}&limit=${dictLimit}`
                )
                .then(response => {
                    if (response.data.rc === 0) {
                        // 调用 callback 返回建议列表的数据
                        this.words = [];
                        response.data.data.forEach(element => {
                            this.words.push(element.name);
                        });
                        this.speakText = this.words.join(", ");
                    }
                });
        }
    },
    mounted() {
        // speakOutButton
        window.onkeydown = e => {
            // 用户每次按键都会触发该事件，所以对于组合键的检测，需要配合使用onkeydown和onkeyup事件来实现
            if (e.key === "Control") {
                this.ctrlKeyHoldOn = true;
            }
            // 用户按 "Control + space" 组合键后，模拟点击Speak按钮
            // 或者当用户交点不在speak text input上时，按space，也可以模拟点击Speak按钮
            if (
                (this.ctrlKeyHoldOn && e.code === "Space") ||
                (!this.$refs.speakTextInput.isFocused && e.code === "Space")
            ) {
                this.$refs.speakOutButton.click(
                    document.createEvent("MouseEvent")
                );
            }
            // arrow key press
            if (/^Arrow/.test(e.code)) {
                clearTimeout(this.arrowTimeout);
                if (e.code === "ArrowLeft") {
                    this.arrowJump--;
                } else if (e.code === "ArrowRight") {
                    this.arrowJump++;
                }
                this.arrowTimeout = setTimeout(() => {
                    let idx = this.currentIndex + this.arrowJump;
                    if (idx < 0) {
                        idx = 0;
                    } else if (idx >= this.words.length) {
                        idx = this.words.length - 1;
                    }
                    this.speakClick(idx);
                    this.arrowJump = 0;
                }, 500);
            }
        };
        window.onkeyup = e => {
            // 重置组合键
            if (e.key === "Control") {
                this.ctrlKeyHoldOn = false;
            }
        };
    }
};
</script>
