<template>
  <navbar>
    <ul class="nav navbar-nav d-md-down-none">
      <li class="nav-item">
        <a class="nav-link navbar-toggler sidebar-toggler" href="#" @click="sidebarMinimize">&#9776;</a>
      </li>
    </ul>
    <button class="navbar-toggler mobile-sidebar-toggler d-lg-none" type="button" @click="mobileSidebarToggle">&#9776;</button>    <span class="titleLogo"><span>Civic</span> <span>Crowd</span>Analytics<sup>®</sup></span>
    <ul class="nav navbar-nav ml-auto">
      <dropdown size="nav">
        <span slot="button">
          <img src="static/img/avatars/6.jpg" class="img-avatar" alt="avatar-user">
        </span>
        <div slot="dropdown-menu" class="dropdown-menu dropdown-menu-right">
          <div class="row">
            <div class="col-sm-7">
            </div>
            <div class="col-sm-1">
              <li class="mb-4"></li>
              <a class="btn btn-outline-primary" style="color:white; font-size: 10px"href="#"><i class="fa fa-power-off" style="color:rgb(171,12,12);">&nbsp&nbsp</i>LOGOUT</a>
            </div>
          </div>
          <li class="mb-4"></li>
          <li class="dropdown-divider mb-2"></li>
          <div class="col-xs-10 btn-group-vertical">
            <a class="btn btn-block text-left" style="font-size: 12px" href="#">My Profile</a>
            <a class="btn btn-block text-left" style="font-size: 12px" href="#">Settings</a>
          </div>
        </div>
      </dropdown>
    </ul>
  </navbar>
</template>

<script>

import navbar from './Navbar'
import { alert, dropdown } from 'vue-strap'

export default {
  name: 'header',
  components: {
    navbar,
    dropdown,
    alert
  },
  methods: {
    click () {
      // do nothing
    },
    sidebarToggle (e) {
      e.preventDefault()
      document.body.classList.toggle('sidebar-hidden')
    },
    sidebarMinimize (e) {
      e.preventDefault()
      document.body.classList.toggle('sidebar-minimized')
    },
    mobileSidebarToggle (e) {
      e.preventDefault()
      document.body.classList.toggle('sidebar-mobile-show')
    },
    asideToggle (e) {
      e.preventDefault()
      document.body.classList.toggle('aside-menu-hidden')
    }
  }
}
</script>
