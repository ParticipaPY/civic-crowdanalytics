<template>
  <div class="sidebar">
    <nav class="sidebar-nav">
      <ul class="nav">
        <li class="nav-item">
          <router-link :to="'/dashboard'" class="nav-link"><i class="icon-grid"></i> Dashboard</router-link>
        </li>
        <li class="nav-item nav-dropdown">
          <a href="#" class="nav-link nav-dropdown-toggle" @click="handleClick"><i class="icon-briefcase"></i>Projects</a>
          <ul class="nav-dropdown-items">
            <li class="nav-item" v-for="project in projects">
              <router-link :to="'/dashboard/projects/'+project.id" class="nav-link"><i class="icon-briefcase"></i> {{project.name}}</router-link>
            </li>
            <li class="nav-item">
              <router-link :to="'/dashboard/projects/new'" class="nav-link"><i class="fa fa-plus-circle font-lg"></i> New project</router-link>
            </li>
          </ul>
        </li>
        <li class="nav-item">
          <a href="#" class="nav-link"><i class="icon-chart"></i> Dataset</a>
        </li>
        <li class="nav-item">
          <a href="#" class="nav-link"><i class="icon-user"></i> Team</a>
        </li>
        <li class="nav-item">
          <a href="#" class="nav-link"><i class="icon-doc"></i> Press</a>
        </li>
        <li class="nav-item">
          <a href="#" class="nav-link"><i class="icon-bubbles"></i> Contact</a>
        </li>
        <li class="nav-item">
          <a href="#" class="nav-link"><i class="icon-question"></i> Help</a>
        </li>
        <li class="nav-item">
          <a href="#" class="nav-link"><i class="icon-info"></i> About</a>
        </li>
      </ul>
    </nav>
  </div>
</template>
<script>

import {Backend} from '../Backend'

export default {
  name: 'sidebar',
  components: {
    Backend
  },
  methods: {
    handleClick (e) {
      e.preventDefault()
      e.target.parentElement.classList.toggle('open')
    }
  },
  created: function () {
    Backend.projects().then(
      response => {
        this.projects = response.data
      }
    ).catch(
      e => {
        console.log(e)
      }
    )
  },
  data () {
    return {
      projects: []
    }
  }
}
</script>

<style lang="css">
  .nav-link {
    cursor:pointer;
  }
</style>
