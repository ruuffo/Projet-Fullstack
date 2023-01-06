import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import AboutView from '../views/AboutView.vue'
import NewQuizPage from '../views/NewQuizPage.vue'
import LoginPage from '../views/LoginPage.vue'
import AdminToolsPage from '../views/AdminToolsPage.vue'
import QuestionManager from '../views/QuestionManager.vue'
import ScorePage from '../views/ScorePage.vue'
import DisconnectPage from '../views/Disconnect.vue'
import PageNotFound from '../views/PageNotFound.vue'
import PostQuestionPage from '../views/PostQuestionPage.vue'
import ShowQuestionsPage from '../views/ShowQuestionsPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: AboutView
    },
    {
      path: '/admintools',
      name: 'admintools',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: AdminToolsPage
    },
    {
      path: '/newquiz',
      name: 'newquiz',
      component: NewQuizPage
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage
    },
    {
      path: '/quiz',
      name: 'quiz',
      component: QuestionManager
    },
    {
      path: '/postquestion',
      name: 'postquestion',
      component: PostQuestionPage
    },
    {
      path: '/score',
      name: 'score',
      component: ScorePage
    },
    {
      path: '/showquestions',
      name: 'showquestions',
      component: ShowQuestionsPage
    },
    {
      path: '/disconnect',
      name: 'disconnect',
      component: DisconnectPage
    },
    {
      path: '/:catchAll(.*)*',
      name: "PageNotFound",
      component: PageNotFound
    },

  ]
})

export default router
