<template>
  <div class="sidebar">
    <nav class="sidebar-nav">
      <ul class="nav">
        <li class="nav-item">
          <router-link :to="'/dashboard'" class="nav-link"><i class="icon-speedometer"></i> Dashboard</router-link>
        </li>
        <li class="nav-title">
          Analytics
        </li>
        <li class="nav-item">
          <router-link :to="'/dashboard/sentiment'" class="nav-link"><i class="icon-equalizer"></i> Sentiment Analysis</router-link>
        </li>
        <li class="nav-item">
          <router-link :to="'/dashboard/concept'" class="nav-link"><i class="icon-chart"></i> Concept Extraction</router-link>
        </li>
        <li class="nav-item">
          <router-link :to="'/dashboard/category'" class="nav-link"><i class="icon-menu"></i> Category Summary</router-link>
        </li>
        <li class="nav-item">
          <router-link :to="'/dashboard/similar'" class="nav-link"><i class="icon-notebook"></i> Show Similar Ideas</router-link>
        </li>
      </ul>
    </nav>
  </div>
</template>
<script>

export default {
  name: 'sidebar',
  methods: {
    handleClick (e) {
      e.preventDefault()
      e.target.parentElement.classList.toggle('open')
    }
  }
}
</script>

<style lang="css">
  .nav-link {
    cursor:pointer;
  }
</style>
