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
      name: 'home',
      component: HomePage,
      meta: {
        title: 'Super Quiz'
      }
    },
    {
      path: '/admintools',
      name: 'admintools',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: AdminToolsPage,
      meta: {
        title: 'Administration'
      }
    },
    {
      path: '/newquiz',
      name: 'newquiz',
      component: NewQuizPage,
      meta: {
        title: 'Démarrer le quiz'
      }
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView,
      meta: {
        title: 'A propos'
      }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage,
      meta: {
        title: 'Connexion'
      }
    },
    {
      path: '/quiz',
      name: 'quiz',
      component: QuestionManager,
      meta: {
        title: 'Quiz'
      }
    },
    {
      path: '/postquestion',
      name: 'postquestion',
      component: PostQuestionPage,
      meta: {
        title: 'Ajouter une question'
      }
    },
    {
      path: '/putquestion',
      name: 'putquestion',
      component: PutQuestionPage,
      meta: {
        title: 'Modifier une question'
      }
    },
    {
      path: '/score',
      name: 'score',
      component: ScorePage,
      meta: {
        title: 'Resultat'
      }
    },
    {
      path: '/showquestions',
      name: 'showquestions',
      component: ShowQuestionsPage,
      meta: {
        title: 'Liste des questions'
      }
    },
    {
      path: '/disconnect',
      name: 'disconnect',
      component: DisconnectPage,
    },
    {
      path: '/questiondetail',
      name: 'questiondetail',
      component: QuestionDetailPage,
      meta: {
        title: 'Détail de la question'
      }
    },
    {
      path: '/:catchAll(.*)*',
      name: "PageNotFound",
      component: PageNotFound,
      meta: {
        title: 'Erreur 404: Not Found'
      }
    },

  ]
})

export default router
