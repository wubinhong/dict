import Vue from 'vue'
import { Container, Header, Aside, Main, Row, Col, Form, FormItem, Input, Autocomplete, Button, Breadcrumb, BreadcrumbItem, Message, MessageBox } from 'element-ui'

Vue.use(Container)
Vue.use(Header)
Vue.use(Aside)
Vue.use(Main)
Vue.use(Row)
Vue.use(Col)
Vue.use(Form)
Vue.use(FormItem)
Vue.use(Input)
Vue.use(Autocomplete)
Vue.use(Breadcrumb)
Vue.use(BreadcrumbItem)
Vue.use(Button)
// Vue.use(Message) // 别use，否则刷新页面时，会自动弹出一个alert框，太尼玛蛋疼了

Vue.prototype.$message = Message
Vue.prototype.$confirm = MessageBox.confirm
// eslint-disable-next-line no-console
console.log(Vue.prototype.$confirm);
