import Vue from 'vue'
import Router from 'vue-router'

// Containers
import Full from '@/containers/Full'

// Views
import Dashboard from '@/views/Dashboard'
import DashboardNew from '@/views/DashboardNew'
import Projects from '@/views/Projects'

// Views - Analytics
// import Sentiment from '@/views/analytics/Sentiment'
import Category from '@/views/analytics/Category'
// import Concept from '@/views/analytics/Concept'
import Similar from '@/views/analytics/Similar'

// Views - Projects
import New from '@/views/projects/New'

// Sentiment Analysis
import Analysis from '@/views/sentiment/Analysis'

// Concept Axtraction
import Extraction from '@/views/concept/Extraction'

Vue.use(Router)

export default new Router({
  mode: 'hash',
  linkActiveClass: 'open active',
  scrollBehavior: () => ({ y: 0 }),
  routes: [
    {
      path: '/',
      redirect: '/dashboard',
      name: 'Home',
      component: Full,
      children: [
        {
          path: 'dashboard',
          name: 'Dashboard',
          component: DashboardNew
        },
        {
          path: '/dashboard',
          redirect: '/dashboard/sentiment',
          name: 'Dashboard',
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
                  component: New
                },
                {
                  path: 'vallejo-2017',
                  name: 'Vallejo 2017',
                  component: Dashboard
                },
                {
                  path: 'vallejo-2017',
                  redirect: '/vallejo-2017/sentiment',
                  name: 'Vallejo 2017',
                  component: {
                    render (c) { return c('router-view') }
                  },
                  children: [
                    {
                      path: 'sentiment',
                      name: 'Sentiment Analysis',
                      component: Analysis
                    },
                    {
                      path: 'concept',
                      name: 'Concept Extraction',
                      component: Extraction
                    },
                    {
                      path: 'category',
                      name: 'Category Summary',
                      component: Category
                    },
                    {
                      path: 'similar',
                      name: 'Similar Ideas',
                      component: Similar
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
