<template>
    <div>
        <h2>Hi,22 I'm a "Vue-Element-Starter".</h2>
        <el-autocomplete
            popper-class="my-autocomplete"
            v-model="state"
            :fetch-suggestions="querySearch"
            placeholder="请输入内容"
            @select="handleSelect">
            <i
                class="el-icon-edit el-input__icon"
                slot="suffix"
                @click="handleIconClick">
            </i>
            <template slot-scope="{ item }">
                <div class="name">{{ item.value }}</div>
                <span class="addr">{{ item.address }}</span>
            </template>
        </el-autocomplete>
        <hr>
        <ul>
            <li v-for="word in words">
                {{ word }}
            </li>
        </ul>
    </div>
</template>

<style scoped lang="scss">
    .my-autocomplete {
        li {
            line-height: normal;
            padding: 7px;

            .name {
                text-overflow: ellipsis;
                overflow: hidden;
            }

            .addr {
                font-size: 12px;
                color: #b4b4b4;
            }

            .highlighted .addr {
                color: #ddd;
            }

        }
    }
</style>

<script>
    export default {
        data() {
            return {
                restaurants: [],
                state: '',
                words: []
            };
        },
        methods: {
            querySearch(queryString, cb) {
                var restaurants = this.restaurants;
                var results = queryString ? restaurants.filter(this.createFilter(queryString)) : restaurants;
                // 调用 callback 返回建议列表的数据
                cb(results);
            },
            createFilter(queryString) {
                return (restaurant) => {
                    return (restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
                };
            },
            loadAll() {
                return [
                    {"value": "三全鲜食（北新泾店）", "address": "长宁区新渔路144号"},
                    {"value": "Hot honey 首尔炸鸡（仙霞路）", "address": "上海市长宁区淞虹路661号"},
                    {"value": "新旺角茶餐厅", "address": "上海市普陀区真北路988号创邑金沙谷6号楼113"},
                    {"value": "泷千家(天山西路店)", "address": "天山西路438号"},
                    {"value": "胖仙女纸杯蛋糕（上海凌空店）", "address": "上海市长宁区金钟路968号1幢18号楼一层商铺18-101"},
                    {"value": "贡茶", "address": "上海市长宁区金钟路633号"},
                    {"value": "豪大大香鸡排超级奶爸", "address": "上海市嘉定区曹安公路曹安路1685号"},
                    {"value": "茶芝兰（奶茶，手抓饼）", "address": "上海市普陀区同普路1435号"},
                    {"value": "十二泷町", "address": "上海市北翟路1444弄81号B幢-107"},
                    {"value": "星移浓缩咖啡", "address": "上海市嘉定区新郁路817号"},
                    {"value": "阿姨奶茶/豪大大", "address": "嘉定区曹安路1611号"},
                    {"value": "新麦甜四季甜品炸鸡", "address": "嘉定区曹安公路2383弄55号"},
                    {"value": "Monica摩托主题咖啡店", "address": "嘉定区江桥镇曹安公路2409号1F，2383弄62号1F"},
                    {"value": "浮生若茶（凌空soho店）", "address": "上海长宁区金钟路968号9号楼地下一层"},
                    {"value": "NONO JUICE  鲜榨果汁", "address": "上海市长宁区天山西路119号"},
                    {"value": "CoCo都可(北新泾店）", "address": "上海市长宁区仙霞西路"},
                    {"value": "快乐柠檬（神州智慧店）", "address": "上海市长宁区天山西路567号1层R117号店铺"},
                    {"value": "Merci Paul cafe", "address": "上海市普陀区光复西路丹巴路28弄6号楼819"},
                    {"value": "猫山王（西郊百联店）", "address": "上海市长宁区仙霞西路88号第一层G05-F01-1-306"},
                    {"value": "枪会山", "address": "上海市普陀区棕榈路"},
                    {"value": "纵食", "address": "元丰天山花园(东门) 双流路267号"}
                ];
            },
            handleSelect(item) {
                console.log(item);
            },
            handleIconClick(ev) {
                console.log(ev);
            }
        },
        mounted() {
            this.restaurants = this.loadAll();
            this.$axios.get("http://localhost:5000/words/fuzzy?keyword=cend&skip=0&limit=3")
                .then(response => (this.words = response.data.data));
        }
    }
</script>
