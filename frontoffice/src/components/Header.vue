<template>
  <navbar>
    <ul class="nav navbar-nav d-md-down-none">
      <li class="nav-item">
        <a class="nav-link navbar-toggler sidebar-toggler" href="#" @click="sidebarMinimize">&#9776;</a>
      </li>
    </ul>
    <button class="navbar-toggler mobile-sidebar-toggler d-lg-none" type="button" @click="mobileSidebarToggle">&#9776;</button>    
    <span class="titleLogo"><span>Civic</span> <span>Crowd</span>Analytics<sup>®</sup></span>
    <ul class="nav navbar-nav ml-auto">
      <dropdown size="nav">
        <span slot="button">
          <div style="cursor:pointer">
            <img src="static/img/avatars/6.jpg" class="img-avatar" alt="avatar-user">
            <i class="fa fa-caret-down" style="margin-right:10px"></i>
          </div>
        </span>    
          <div slot="dropdown-menu" class="dropdown-menu dropdown-menu-right">

            <div class="row" style="margin-left: 0px; margin-right: -25px; margin-bottom:10px">

              <div class="col-sm-7" >

                <div class="row" style=" margin-left: 0px; margin-right: -25px; margin-top: 15px;">
                  <div style="color:white"><span style="display:block;text-overflow: ellipsis;width: 155px;overflow: hidden; white-space: nowrap;">{{ DisplayName () }}</span></div>
                </div>

                <div class="row" style="margin-bottom: 5px; margin-left: 10px; margin-right: -25px;">
                  <a style="color:silver  ; font-size: 13px">{{ DisplayUsername () }}</a>
                </div>
              
              </div>

              <div class="col-sm-4" >
                <button @click="logout" type="button" class="btn btn-outline-danger" style="margin-top: 20px; margin-left: -10px;font-size: 10px"><i class="icon fa fa-power-off" style="color.hover: white; margin-right:5px"></i>LOGOUT</button>
              </div>

            </div>

            <li class="dropdown-divider"></li>

            <div class="row">
              <div class="col-lg-12 btn-group-vertical" >
                  <button type="button" class="nav-item btn btn-outline-primary text-left" @click="openModal('0')" style="font-size: 13px; height:40px">My Profile</button>
                  <button type="button" class="nav-item btn btn-outline-primary text-left" @click="openModal('1')" style="font-size: 13px; height:40px">Settings</button>
              </div>
            </div>

            <div id="wrapper" class="container"> 
             <modal v-if="showModal"> 
              <h3 slot="header" class="modal-title"> {{ modalTitle }} </h3>
               <div slot="footer">
                  <button type="button" class="btn btn-outline-info" @click="closeModal()"> Close </button>
               </div>
             </modal>
            </div>

          </div>
      </dropdown>
    </ul>
  </navbar>
</template>

<script>

import navbar from './Navbar'
import { alert, dropdown } from 'vue-strap'
import Modal from './Modal'
import {Backend} from '@/Backend'

export default {
  name: 'header',
  components: {
    navbar,
    dropdown,
    alert,
    Modal
  },
  data () {
    return {
      showModal: false,
      flName: '',
      modalTitle: ''
    }
  },
  methods: {
    click () {
      // do nothing
    },
    DisplayUsername () {
      return Backend.username
    },
    DisplayName () {
      Backend.UserData()
      .then(response => {
        const data = response.data
        for (let key in data) {
          const user = data[key]
          if (user.username === Backend.username) {
            this.flName = user.first_name + ' ' + user.last_name
            break
          }
        }
      }).catch(e => { console.log(e) })
      return this.flName
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
    },
    openModal (id) {
      if (id === '0') {
        this.modalTitle = 'My Profile'
      } else {
        this.modalTitle = 'Settings'
      }
      this.showModal = true
    },
    closeModal () {
      this.showModal = false
    },
    logout () {
      Backend.token = null
      Backend.username = ''
      this.$router.push({ name: 'Login' })
    }
  }
}
</script>
