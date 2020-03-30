import Vue from 'vue';
import Router from 'vue-router';
import ProjectView from './views/Project.vue';
import ProjectDetailView from './views/ProjectDetail.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'project',
      component: ProjectView,
    },
    {
      path: '/projects/:projectId/',
      name: 'project-detail',
      component: ProjectDetailView,
      props: true,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/About.vue'),
    },
  ],
});
