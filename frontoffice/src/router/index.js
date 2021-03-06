import Vue from 'vue'
import Router from 'vue-router'

// Containers
import Full from '@/containers/Full'
import Login from '@/containers/Login'

// Views
// import Dashboard from '@/views/Dashboard'
import ProjectDashboard from '@/views/ProjectDashboard'
import DashboardNew from '@/views/DashboardNew'
import Projects from '@/views/Projects'

// Views - Analytics
// import Sentiment from '@/views/analytics/Sentiment'
import Category from '@/views/category/Classification'
// import Concept from '@/views/analytics/Concept'
import Similar from '@/views/similar/Cluster'

// Views - Projects
import New from '@/views/projects/New'

// Sentiment Analysis
import Analysis from '@/views/sentiment/Analysis'

// Concept Axtraction
import Extraction from '@/views/concept/Extraction'

import LoginPage from '@/views/LoginPage'
import SignUpPage from '@/views/SignUpPage'

Vue.use(Router)

export default new Router({
  mode: 'hash',
  linkActiveClass: 'open active',
  scrollBehavior: () => ({ y: 0 }),
  routes: [
    {
      path: '/',
      redirect: '/login',
      name: 'Login',
      component: Login,
      children: [
        {
          path: 'login',
          name: 'Login',
          component: LoginPage
        },
        {
          path: 'signup',
          name: 'Sign Up',
          component: SignUpPage
        }
      ]
    },
    {
      path: '/dashboard',
      redirect: '/dashboard',
      name: 'Home',
      meta: {
        breadcrumb: 'Home'
      },
      component: Full,
      children: [
        {
          path: '',
          name: 'Dashboard',
          meta: {
            breadcrumb: 'Dashboard'
          },
          component: DashboardNew
        },
        {
          path: '/dashboard',
          redirect: '/dashboard/sentiment',
          name: 'Dashboard',
          meta: {
            breadcrumb: 'Dashboard'
          },
          component: {
            render (c) { return c('router-view') }
          },
          children: [
            {
              path: 'projects',
              name: 'Projects',
              component: Projects
            },
            {
              path: 'projects',
              redirect: '/projects/new',
              name: 'Projects',
              component: {
                render (c) { return c('router-view') }
              },
              children: [
                {
                  path: 'new',
                  name: 'New Project',
                  component: New,
                  meta: {
                    breadcrumb: 'New Project'
                  }
                },
                {
                  path: ':projectId',
                  name: 'Project Home',
                  meta: {
                    breadcrumb: 'Project Dashboard'
                  },
                  component: ProjectDashboard
                },
                {
                  path: ':projectId',
                  name: 'Project Home',
                  meta: {
                    breadcrumb: 'Project Dashboard'
                  },
                  component: {
                    render (c) { return c('router-view') }
                  },
                  children: [
                    {
                      path: 'sentiment/:analysisId',
                      name: 'Sentiment Analysis',
                      component: Analysis,
                      meta: {
                        breadcrumb: 'Sentiment Analysis'
                      }
                    },
                    {
                      path: 'concept/:analysisId',
                      name: 'Concept Extraction',
                      component: Extraction,
                      meta: {
                        breadcrumb: 'Concept Extraction'
                      }
                    },
                    {
                      path: 'category/:analysisId',
                      name: 'Category Summary',
                      component: Category,
                      meta: {
                        breadcrumb: 'Category Summary'
                      }
                    },
                    {
                      path: 'similar/:analysisId',
                      name: 'Similar Ideas',
                      component: Similar,
                      meta: {
                        breadcrumb: 'Similar Ideas'
                      }
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
})
