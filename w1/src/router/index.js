import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Site from '../views/Site.vue'
import Login from '../views/Login.vue'
import Errors from '../views/Errors.vue'
import Register from '../views/Register.vue'
import Backend from '../views/backend/Backend.vue'
import ArticleDetail from '../views/ArticleDetail.vue'
import AddArticle from '../views/backend/AddArticle.vue'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'Created',
        component: Home
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/register',
        name: 'Register',
        component: Register
    },
    {
        path: '/home',
        name: 'Home',
        component: Home
    },
    {
        path: '/site/:username',
        name: 'Site',
        component: Site
    },
    {
        path: '/site/:username/category/:category_id',
        name: 'SiteCategory',
        component: Site
    },
    {
        path: '/site/:username/tag/:tag_id',
        name: 'SiteTag',
        component: Site
    },
    {
        path: '/site/:username/article/:article_id',
        name: 'ArticleDetail',
        component: ArticleDetail
    },
    {
        path: '/backend',
        name: 'Backend',
        component: Backend
    },
    {
        path: '/add_article',
        name: 'AddArticle',
        component: AddArticle
    },
    {
        path: '*',
        name: 'Errors',
        component: Errors
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router