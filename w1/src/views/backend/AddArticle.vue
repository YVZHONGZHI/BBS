<template>
    <div class="add_article" v-if="isLoading">
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
                                    <a href="" @click="goPage('/backend')">后台管理</a>
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
                    <h3>添加文章</h3>
                    <form action="" method="post" enctype="multipart/form-data">
                        <label for="title">文章标题</label>
                        <div>
                            <input type="text" name="title" id="title" class="form-control">
                        </div>
                        <br>
                        <p>文章内容</p>
                        <div>
                            <vue-editor useCustomImageHandler @image-added="handleImageAdded" v-model="content"></vue-editor>
                        </div>
                        <br>
                        <p>文章分类</p>
                        <div>
                            <label v-for="category in category_list">
                                <input type="radio" name="category" :value="category.id">{{ category.name }}&nbsp;
                            </label>
                        </div>
                        <br>
                        <p>文章标签</p>
                        <div>
                            <label v-for="tag in tag_list">
                                <input type="checkbox" name="tag" :value="tag.id">{{ tag.name }}&nbsp;
                            </label>
                        </div>
                        <br>
                        <input type="button" value="取消" class="btn btn-info">&nbsp;
                        <input type="button" value="提交" class="btn btn-danger" @click="add_article">
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
    import SetAvatar from "../../components/SetAvatar";
    import SetPassword from "../../components/SetPassword";
    import { VueEditor } from "vue2-editor";
    export default {
        name: "AddArticle",
        data() {
            return {
                username: '',
                site_title: '',
                category_list: [],
                tag_list: [],
                content: '',
                search: '',
                token: '',
                isLoading: false
            }
        },
        created() {
            this.username = this.$cookies.get('username')
            this.token = this.$cookies.get('token')
            this.site_title = this.$cookies.get('username') + '的博客'
            this.$axios.get(this.$settings.base_url+'/add_article_created/'+this.$cookies.get('username')+'/', {headers: {Authorization: 'JWT '+this.$cookies.get('token')}}).then(response => {
                if (response.data.result) {
                    setTimeout(() => {alert('请先登录才能进入')},400)
                    setTimeout(() => {this.$router.push('/login')},600)
                }
                else {
                    this.category_list = response.data.category_list
                    this.tag_list = response.data.tag_list
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
            handleImageAdded(file, Editor, cursorLocation, resetUploader) {
                let formDateObj = new FormData();
                formDateObj.append('imgFile', file);
                this.$axios.post(this.$settings.base_url+'/upload_image/', formDateObj).then(response => {
                    Editor.insertEmbed(cursorLocation, 'image', this.$settings.base_url + response.data.url)
                    resetUploader()
                })
            },
            add_article() {
                let formDateObj = new FormData();
                $.each($('form').serializeArray(), (index, obj) => {
                    formDateObj.append(obj.name, obj.value)
                })
                formDateObj.append('username', this.username);
                formDateObj.append('content', this.content);
                this.$axios.post(this.$settings.base_url+'/add_article/', formDateObj).then(() => {
                    this.$router.push('/backend')
                })
            },
            goPage(url_path) {
                this.$router.push(url_path)
            }
        },
        components: {
            SetPassword,
            SetAvatar,
            VueEditor
        }
    }
</script>


<style lang="less" scoped>
    @import '~bootstrap/less/bootstrap.less';

    .add_article {
        font-size: 14px;
        line-height: 1.42857143;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
</style>