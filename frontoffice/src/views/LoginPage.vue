<template>
  <div class="loginWrapper">
    <div class="animated fadeIn">
      <div class="loginbox">
        <span class="titleLogo"><span>Civic</span> <span>Crowd</span>Analytics<sup>®</sup></span>
        <div>
          <label>Username</label>
          <input id="userfield" type="text" v-model="username">
        </div>
        <div>
          <label>Password</label>
          <input id="passfield" type="password" v-model="password" @keyup.enter="login()">
        </div>
        <button id="loginbtn" class="btn btn-default btn-primary" type="submit" @click="login()">Login</button>
        <p><router-link :to="'/signup'">Not a member? Sign up!</router-link></p>
      </div>
    </div>
  </div>
</template>
<script>
import {Backend} from '@/Backend'

export default {
  name: 'login',
  components: {
    Backend
  },
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    login: function () {
      this.disableFields()
      Backend.login(this.username, this.password).then((response) => {
        Backend.token = response.data.token
        Backend.username = this.username
        Backend.password = this.password
        this.$snotify.success('Signed in successfully')
        this.enableFields()
        this.$router.push({ name: 'Dashboard' })
      }).catch(() => {
        this.enableFields()
        this.$snotify.error('Invalid username or password')
      })
    },
    disableFields: function () {
      document.getElementById('userfield').setAttribute('readonly', 'readonly')
      document.getElementById('passfield').setAttribute('readonly', 'readonly')
      document.getElementById('loginbtn').setAttribute('disabled', 'disabled')
    },
    enableFields: function () {
      document.getElementById('userfield').removeAttribute('readonly')
      document.getElementById('passfield').removeAttribute('readonly')
      document.getElementById('loginbtn').removeAttribute('disabled')
    }
  }
}
</script>
