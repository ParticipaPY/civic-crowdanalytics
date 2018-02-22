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
          <input id="passfield" type="password" v-model="password">
        </div>
        <div>
          <label>Password confirmation</label>
          <input id="confirmfield" type="password" v-model="confirmation" @keyup.enter="signup()">
        </div>
        <button id="loginbtn" class="btn btn-default btn-primary" type="submit" @click="signup()">Sign Up</button>
        <p><router-link :to="'/login'">Alread a member? Sign in!</router-link></p>
      </div>
    </div>
  </div>
</template>
<script>
import {Backend} from '@/Backend'

export default {
  name: 'signup',
  components: {
    Backend
  },
  data () {
    return {
      username: '',
      password: '',
      confirmation: ''
    }
  },
  methods: {
    signup: function () {
      this.disableFields()
      if (this.password === this.confirmation) {
        Backend.signup(this.username, this.password).then((response) => {
          Backend.token = response.data.token
          Backend.username = this.username
          Backend.password = this.password
          this.$snotify.success('Signed up successfully. Welcome!')
          this.enableFields()
          this.$router.push({ name: 'Dashboard' })
        }).catch(() => {
          this.enableFields()
          this.$snotify.error('A user with that username already exists')
        })
      } else {
        this.enableFields()
        this.$snotify.error('Passwords do not match')
      }
    },
    disableFields: function () {
      document.getElementById('userfield').setAttribute('readonly', 'readonly')
      document.getElementById('passfield').setAttribute('readonly', 'readonly')
      document.getElementById('confirmfield').setAttribute('readonly', 'readonly')
      document.getElementById('loginbtn').setAttribute('disabled', 'disabled')
    },
    enableFields: function () {
      document.getElementById('userfield').removeAttribute('readonly')
      document.getElementById('passfield').removeAttribute('readonly')
      document.getElementById('confirmfield').removeAttribute('readonly')
      document.getElementById('loginbtn').removeAttribute('disabled')
    }
  }
}
</script>
