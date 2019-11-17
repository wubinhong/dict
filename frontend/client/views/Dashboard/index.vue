<template>
    <div>
        <h2>私人字典</h2>
        <div id="searchBox" style="margin: 10px 0;">
            <el-autocomplete
                popper-class="my-autocomplete"
                v-model="keyword"
                :fetch-suggestions="querySearch"
                placeholder="请输入单词关键字，支持按单词、同义词、中文解释、相关词、近形词等内容模糊搜索"
                @select="handleSelect">
                <i
                    class="el-icon-edit el-input__icon"
                    slot="suffix"
                    @click="handleIconClick">
                </i>
                <template slot-scope="{ item }">
                    <div class="name">{{ item.name }}</div>
                    <el-breadcrumb separator-class="el-icon-arrow-right">
                        <el-breadcrumb-item class="word-detail">{{ item.derivation }}</el-breadcrumb-item>
                        <el-breadcrumb-item class="word-detail">{{ item.chinese }}</el-breadcrumb-item>
                        <el-breadcrumb-item class="word-detail">{{ item.thesauri }}</el-breadcrumb-item>
                        <el-breadcrumb-item class="word-detail">{{ item.related_words }}</el-breadcrumb-item>
                        <el-breadcrumb-item class="word-detail">{{ item.similar_shaped_words }}</el-breadcrumb-item>
                        <el-breadcrumb-item class="word-detail">{{ item.comment }}</el-breadcrumb-item>

                        <el-breadcrumb-item class="word-operation"><a href="javascript:void(0)" @click="onWordDelete">删除</a></el-breadcrumb-item>
                    </el-breadcrumb>
                </template>
            </el-autocomplete>
        </div>

        <div class="my-card-panel">
            <el-form ref="form" :model="word" label-width="80px">
                <el-form-item label="单词">
                    <el-input v-model="word.name"></el-input>
                </el-form-item>
                <el-form-item label="词根">
                    <el-input v-model="word.derivation"></el-input>
                </el-form-item>
                <el-form-item label="中文解释">
                    <el-input v-model="word.chinese"></el-input>
                </el-form-item>
                <el-form-item label="同义词">
                    <el-input v-model="word.thesauri"></el-input>
                </el-form-item>
                <el-form-item label="相关词">
                    <el-input v-model="word.related_words"></el-input>
                </el-form-item>
                <el-form-item label="近形词">
                    <el-input v-model="word.similar_shaped_words"></el-input>
                </el-form-item>
                <el-form-item label="备注">
                    <el-input v-model="word.comment"></el-input>
                </el-form-item>

                <el-form-item>
                    <el-button type="primary" @click="onWordSave">保存</el-button>
                    <el-button @click="onWordReset">重置</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<style scoped lang="scss">
    #searchBox .el-autocomplete {
        color: red;
        width: 100%;
    }

    .my-autocomplete {
        li {
            line-height: normal;
            padding: 7px;

            .name {
                text-overflow: ellipsis;
                overflow: hidden;
            }

            .word-detail {
                font-size: 12px;
                color: #b4b4b4;
            }
            .word-operation {
                color: black;
            }

            .highlighted .addr {
                color: #ddd;
            }

        }
    }

    .my-card-panel {
        margin: 10px 0;
        padding: 40px;
        box-shadow: rgba(0, 0, 0, 0.1) 0 2px 12px 0;
        border-radius: 4px
    }
</style>

<script>
    export default {
        data() {
            return {
                restaurants: [],
                keyword: '',
                word: {}
            };
        },
        methods: {
            querySearch(queryString, cb) {
                this.$axios.get(String.format("/backend/words/fuzzy?keyword={0}&skip={1}&limit={2}",
                    queryString, 0, 20))
                    .then(response => {
                        if (response.status === 200 && response.data.rc === 0) {
                            // 调用 callback 返回建议列表的数据
                            cb(response.data.data);
                        } else {
                            console.error(response);
                        }
                    });
            },
            createFilter(queryString) {
                return (restaurant) => {
                    return (restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
                };
            },
            handleSelect(item) {
                this.word = item;
                console.dir('select', item);
            },
            onWordSave(e) {
                let vm = this;
                let w = this.word;
                this.$axios.put(String.format('/backend/words/{0}', w.name), w).then(response => {
                    if(response.status === 200 && response.data.rc === 0) {
                        vm.$message({
                            message: '保存成功',
                            type: 'success',
                            duration: 1000
                        });
                    } else {
                        vm.$message.error(response.data.msg);
                    }
                });
            },
            onWordReset(e) {
                this.word = {};
            },
            onWordDelete(e) {
                this.$confirm('此操作将永久删除单词, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    let vm = this;
                    let w = this.word;
                    this.$axios.delete(String.format('/backend/words/{0}', w.name)).then(response => {
                        if(response.status === 200 && response.data.rc === 0) {
                            vm.$message({
                                message: '删除成功',
                                type: 'success',
                                duration: 1000
                            });
                        } else {
                            vm.$message.error(response.data.msg);
                        }
                    });
                });

            },
            handleIconClick(ev) {
                console.log(ev);
            }
        },
        mounted() {
            console.log('mounted!');
        }
    }
</script>
