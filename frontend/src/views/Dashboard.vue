<template>
    <div style="margin: auto; max-width: 850px;">
        <h2>私人字典</h2>
        <div id="searchBox" style="margin: 10px 0;">
            <el-autocomplete
                popper-class="my-autocomplete"
                v-model="keyword"
                :fetch-suggestions="querySearch"
                placeholder="请输入单词关键字，支持按单词、同义词、中文解释、相关词、近形词等内容模糊搜索"
                @select="handleSelect"
            >
                <i class="el-icon-search el-input__icon" slot="suffix" @click="handleIconClick"></i>
                <template slot-scope="{ item }">
                    <!-- 变相处理数据为空的情况 -->
                    <div
                        style="color: #E6A23C;"
                        v-if="item._id == null"
                    >没有匹配的单词，点击本条可添加单词 [ {{item.name}} ] 到下方表单！</div>
                    <!-- 有数据时 -->
                    <div v-else>
                        <el-row class="name">
                          <el-col :span="12"><div>{{ item.name }}</div></el-col>
                          <el-col :span="12">
                            <div class="name-operation"><a
                                  class="el-link--danger"
                                  href="javascript:void(0)"
                                  @click="onWordDelete"
                              >删除</a>
                            </div>
                          </el-col>
                        </el-row>
                        <el-breadcrumb separator-class="el-icon-arrow-right" class="word-detail">
                            <el-breadcrumb-item>{{ item.derivation }}</el-breadcrumb-item>
                            <el-breadcrumb-item>{{ item.chinese }}</el-breadcrumb-item>
                            <el-breadcrumb-item>{{ item.thesauri }}</el-breadcrumb-item>
                            <el-breadcrumb-item>{{ item.related_words }}</el-breadcrumb-item>
                            <el-breadcrumb-item>{{ item.similar_shaped_words }}</el-breadcrumb-item>
                            <el-breadcrumb-item>{{ item.comment }}</el-breadcrumb-item>
                        </el-breadcrumb>
                    </div>
                </template>
            </el-autocomplete>
        </div>

        <div class="my-card-panel">
            <el-form :rules="rules" ref="word" :model="word" label-width="60px">
                <el-form-item label="单词" prop="name">
                    <el-input @keyup.enter.native="onWordSave" v-model="word.name"></el-input>
                </el-form-item>
                <el-form-item label="词根">
                    <el-input @keyup.enter.native="onWordSave" v-model="word.derivation"></el-input>
                </el-form-item>
                <el-form-item label="中文">
                    <el-input @keyup.enter.native="onWordSave" v-model="word.chinese"></el-input>
                </el-form-item>
                <el-form-item label="同义词">
                    <el-input @keyup.enter.native="onWordSave" v-model="word.thesauri"></el-input>
                </el-form-item>
                <el-form-item label="相关词">
                    <el-input @keyup.enter.native="onWordSave" v-model="word.related_words"></el-input>
                </el-form-item>
                <el-form-item label="近形词">
                    <el-input @keyup.enter.native="onWordSave" v-model="word.similar_shaped_words"></el-input>
                </el-form-item>
                <el-form-item label="备注">
                    <el-input @keyup.enter.native="onWordSave" v-model="word.comment"></el-input>
                </el-form-item>

                <el-form-item>
                    <el-button type="primary" @click="onWordSave">保存</el-button>
                    <el-button @click="onWordReset">重置</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<!-- 注意：加了scoped，则无法正常覆盖element原来的样式，这种做法适用于自定义组件的情况（css也是纯粹自己写的情况） -->
<!-- <style lang="less" scoped> -->
<style lang="less">
#searchBox .el-autocomplete {
    // color: red;
    width: 100%;
}

.my-autocomplete {
    li {
        line-height: normal;
        padding: 0 20px;
        .name {
            padding: 5px 0;
            .name-operation {
                text-align: right;
            }
        }
        .word-detail {
            font-size: 12px;
            padding: 5px 0;
        }
        .el-breadcrumb__inner {
            color: #b4b4b4;
        }
        .el-link--danger {
            color: #f56c6c;
        }
    }
}

.my-card-panel {
    margin: 10px 0;
    padding: 40px;
    box-shadow: rgba(0, 0, 0, 0.1) 0 2px 12px 0;
    border-radius: 4px;
}
</style>

<script>
export default {
    name: "Dashboard",
    data() {
        return {
            keyword: "",
            word: {},
            rules: {
                name: [
                    { required: true, message: "单词名必填", trigger: "blur" }
                ]
            }
        };
    },
    methods: {
        querySearch(queryString, cb) {
            // handle case for: queryString == undefined
            queryString = queryString || ''
            this.$axios
                .get(`/backend/words/fuzzy?keyword=${queryString}&skip=0&limit=20`)
                .then(response => {
                    if (response.status === 200 && response.data.rc === 0) {
                        // 调用 callback 返回建议列表的数据
                        let words = response.data.data;
                        // 当数据为空时，推一条空数据进去，在模板那里根据这条空数据哪里生成一个处理空数据的element
                        if (words.length == 0) {
                            words.push({ _id: null, name: queryString });
                        }
                        cb(words);
                    } else {
                        // console.error(response);
                    }
                });
        },
        createFilter(queryString) {
            return restaurant => {
                return (
                    restaurant.value
                        .toLowerCase()
                        .indexOf(queryString.toLowerCase()) === 0
                );
            };
        },
        handleSelect(item) {
            this.word = item;
            // console.dir("handleSelect", item);
        },
        onWordSave() {
            let vm = this;
            let w = this.word;
            this.$refs.word.validate(valid => {
                if (valid) {
                    this.$axios
                        .put(`/backend/words/${ w.name }`, w)
                        .then(response => {
                            if (
                                response.status === 200 &&
                                response.data.rc === 0
                            ) {
                                vm.$message({
                                    message: "保存成功",
                                    type: "success",
                                    duration: 1000
                                });
                                vm.word = {};
                            } else {
                                vm.$message.error(response.data.msg);
                            }
                        });
                }
            });
        },
        onWordReset() {
            this.word = {};
        },
        onWordDelete() {
            this.$confirm("此操作将永久删除单词, 是否继续?", "提示", {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning"
            }).then(() => {
                let vm = this;
                let w = this.word;
                
                this.$axios
                    .delete(`/backend/words/${w.name}`)
                    .then(response => {
                        if (response.status === 200 && response.data.rc === 0) {
                            vm.$message({
                                message: "删除成功",
                                type: "success",
                                duration: 1000
                            });
                        } else {
                            vm.$message.error(response.data.msg);
                        }
                    });
            });
        },
        handleIconClick() {}
    },
    mounted() {

    }
};
</script>
