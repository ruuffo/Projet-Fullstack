import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import NewQuizPage from '../views/NewQuizPage.vue'
import LoginPage from '../views/LoginPage.vue'
import AdminToolsPage from '../views/AdminToolsPage.vue'
import QuestionManager from '../views/QuestionManager.vue'
import ScorePage from '../views/ScorePage.vue'
import DisconnectPage from '../views/Disconnect.vue'
import AboutView from '../views/AboutView.vue'
import QuestionDetailPage from '../views/QuestionDetail.vue'
import PageNotFound from '../views/PageNotFound.vue'
import PostQuestionPage from '../views/PostQuestionPage.vue'
import PutQuestionPage from '../views/PutQuestionPage.vue'
import ShowQuestionsPage from '../views/ShowQuestionsPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Super Quiz',
      component: HomePage
    },
    {
      path: '/admintools',
      name: 'Administration',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: AdminToolsPage
    },
    {
      path: '/newquiz',
      name: 'Commencer le quiz',
      component: NewQuizPage
    },
    {
      path: '/about',
      name: 'A propos',
      component: AboutView
    },
    {
      path: '/login',
      name: 'Connexion',
      component: LoginPage
    },
    {
      path: '/quiz',
      name: 'Quiz',
      component: QuestionManager
    },
    {
      path: '/postquestion',
      name: 'Ajouter une question',
      component: PostQuestionPage
    },
    {
      path: '/putquestion',
      name: 'Modifier une question',
      component: PutQuestionPage
    },
    {
      path: '/score',
      name: 'Score',
      component: ScorePage
    },
    {
      path: '/showquestions',
      name: 'Liste des questions',
      component: ShowQuestionsPage
    },
    {
      path: '/disconnect',
      name: 'disconnect',
      component: DisconnectPage,
    },
    {
      path: '/questiondetail',
      name: 'Détail de la question',
      component: QuestionDetailPage
    },
    {
      path: '/:catchAll(.*)*',
      name: "Erreur 404: page not found",
      component: PageNotFound
    },

  ]
})

router.beforeEach((to, from, next) => {
  document.title = to.name;
  next();
});

export default router
