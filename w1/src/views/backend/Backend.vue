<template>
    <div class="backend" v-if="isLoading">
        <nav class="navbar navbar-inverse">
            <div class="container-fluid">
                <!-- Brand and toggle get grouped for better mobile display -->
                <div class="navbar-header">
                    <a :href="'/site/' + username" class="navbar-brand">{{ site_title }}</a>
                </div>

                <!-- Collect the nav links, forms, and other content for toggling -->
                <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                    <ul class="nav navbar-nav">
                        <li><a href="" @click="goPage('/home')">主页</a></li>
                    </ul>
                    <form class="navbar-form navbar-left">
                        <div class="form-group">
                            <label for="search"></label>
                            <input type="text" id="search" class="form-control" placeholder="输入关键字" v-model="search">&nbsp;
                        </div>
                        <input type="button" class="btn btn-default" value="搜索" @click="test">
                    </form>
                    <ul class="nav navbar-nav navbar-right">
                        <li v-if="token"><a>{{ username }}</a></li>
                        <li class="dropdown" v-if="token">
                            <a class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">更多操作 <span class="caret"></span></a>
                            <ul class="dropdown-menu">
                                <li><a href="" data-toggle="modal" data-target=".bs-example-modal-lg">修改密码</a></li>
                                <li><a href="" data-toggle="modal" data-target=".bs-example-modal-sm">修改头像</a></li>
                                <li><a>后台管理</a></li>
                                <li role="separator" class="divider"></li>
                                <li><a href="" @click="logout">退出登录</a></li>
                            </ul>
                            <SetPassword/>
                            <SetAvatar/>
                        </li>
                        <li v-if="!token"><a href="" @click="goPage('/register')">注册</a></li>
                        <li v-if="!token"><a href="" @click="goPage('/login')">登录</a></li>
                    </ul>
                </div><!-- /.navbar-collapse -->
            </div><!-- /.container-fluid -->
        </nav>
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-2">
                    <div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">
                        <div class="panel panel-default">
                            <div class="panel-heading" role="tab" id="headingOne">
                                <h4 class="panel-title">
                                    <a role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                                        更多操作
                                    </a>
                                </h4>
                            </div>
                            <div id="collapseOne" class="panel-collapse collapse in" role="tabpanel" aria-labelledby="headingOne">
                                <div class="panel-body">
                                    <a href="" @click="goPage('/add_article')">添加文章</a>
                                </div>
                            </div>
                            <div id="collapseOne" class="panel-collapse collapse in" role="tabpanel" aria-labelledby="headingOne">
                                <div class="panel-body">
                                    <a href="">联系客服</a>
                                </div>
                            </div>
                            <div id="collapseOne" class="panel-collapse collapse in" role="tabpanel" aria-labelledby="headingOne">
                                <div class="panel-body">
                                    <a href="">意见反馈</a>
                                </div>
                            </div>
                            <div id="collapseOne" class="panel-collapse collapse in" role="tabpanel" aria-labelledby="headingOne">
                                <div class="panel-body">
                                    <a href="">&nbsp;&nbsp;&nbsp;其他</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-10">
                    <div>

                        <!-- Nav tabs -->
                        <ul class="nav nav-tabs" role="tablist">
                            <li role="presentation" class="active"><a href="#article" aria-controls="article" role="tab" data-toggle="tab">文章</a></li>
                            <li role="presentation"><a href="#vip" aria-controls="vip" role="tab" data-toggle="tab">会员</a></li>
                            <li role="presentation"><a href="#draft" aria-controls="draft" role="tab" data-toggle="tab">草稿</a></li>
                            <li role="presentation"><a href="#settings" aria-controls="settings" role="tab" data-toggle="tab">设置</a></li>
                        </ul>

                        <!-- Tab panes -->
                        <div class="tab-content">
                            <div role="tabpanel" class="tab-pane fade in active" id="article">
                                <table class="table table-hover table-striped">
                                    <thead>
                                        <tr>
                                            <th>&nbsp;&nbsp;文章标题</th>
                                            <th>点赞数</th>
                                            <th>评论数</th>
                                            <th>操作</th>
                                            <th>操作</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="article in article_list">
                                            <td>
                                                <a :href="'/site/' + article.site_name + '/article/' + article.id">
                                                    {{ article.title }}
                                                </a>
                                            </td>
                                            <td>&nbsp;&nbsp;&nbsp;&nbsp;{{ article.up_num }}</td>
                                            <td>&nbsp;&nbsp;&nbsp;&nbsp;{{ article.comment_num }}</td>
                                            <td>
                                                <a>编辑</a>
                                            </td>
                                            <td>
                                                <a>删除</a>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            <div role="tabpanel" class="tab-pane fade" id="vip">
                                <table class="table table-hover table-striped">
                                    <thead>
                                        <tr>
                                            <th></th>
                                            <th>会员价格</th>
                                            <th>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;会员权益</th>
                                            <th>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;操作</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>限时免费会员</td>
                                            <td>&nbsp;&nbsp;&nbsp;￥&nbsp;0</td>
                                            <td>更多精品推荐与月刊等你浏览</td>
                                            <td>
                                                <button @click="vip">支付订单</button>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            <div role="tabpanel" class="tab-pane fade" id="draft"></div>
                            <div role="tabpanel" class="tab-pane fade" id="settings"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
    import SetAvatar from "../../components/SetAvatar";
    import SetPassword from "../../components/SetPassword";
    export default {
        name: "Backend",
        data() {
            return {
                username: '',
                site_title: '',
                article_list: [],
                search: '',
                token: '',
                isLoading: false
            }
        },
        created() {
            this.username = this.$cookies.get('username')
            this.token = this.$cookies.get('token')
            this.site_title = this.$cookies.get('username') + '的博客'
            this.$axios.get(this.$settings.base_url+'/backend/?blog__site_name='+this.$cookies.get('username'), {headers: {Authorization: 'JWT '+this.$cookies.get('token')}}).then(response => {
                if (response.data.result) {
                    setTimeout(() => {alert('请先登录才能进入')},400)
                    setTimeout(() => {this.$router.push('/login')},600)
                }
                else {
                    this.article_list = response.data
                    this.isLoading = true
                }
            })
        },
        methods: {
            logout() {
                this.$cookies.remove('username')
                this.$cookies.remove('token')
                this.username = ''
                this.token = ''
            },
            test() {
                if (this.search) {
                    this.$router.push('/home/?search=' + this.search)
                    this.search = ''
                }
                else{
                    alert("关键字不能为空!")
                }
            },
            vip() {
                let formDateObj = new FormData();
                formDateObj.append('username', this.username);
                this.$axios.put(this.$settings.base_url+'/vip/'+this.username+'/', formDateObj).then(response => {
                    if (response.data.code) {
                        alert(response.data.msg)
                    }
                    else {
                        $.each(response.data.msg, (index,obj) => {
                            alert(obj[0])
                        })
                    }
                })
            },
            goPage(url_path) {
                this.$router.push(url_path)
            }
        },
        components: {
            SetPassword,
            SetAvatar
        }
    }
</script>


<style lang="less" scoped>
    @import '~bootstrap/less/bootstrap.less';

    .backend {
        font-size: 14px;
        line-height: 1.42857143;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
</style>