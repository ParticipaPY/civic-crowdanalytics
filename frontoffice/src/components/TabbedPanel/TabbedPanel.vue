<template>
  <div>
    <div class="row no-gutters tabbedPanelPanes" v-if="navStyle=='pane'">
      <div class="col-md-4 col-lg-3 col-xl-2 shadow">
        <ul class="list-group">
          <template v-for="header in headers">
            <li data-toggle="list" role="tab" :class="['list-group-item list-group-item-action',{active:header.active, disabled:header.disabled}]" @click.prevent="select(header)">
              <slot name="header"><a href="#" v-html="header.header"></a></slot>
            </li>
          </template>
        </ul>
      </div>
      <div class="col-md-8 col-lg-9 col-xl-10">
        <div class="tab-content">
          <slot></slot>
        </div>
      </div>
    </div>
    <div class="row no-gutters tabbedPanelPills" v-if="navStyle=='pill'">
      <div class="col-sm-12">
        <ul class="list-group">
          <template v-for="header in headers">
            <li data-toggle="list" role="tab" :class="['list-group-item list-group-item-action',{active:header.active, disabled:header.disabled}]" @click.prevent="select(header)">
              <slot name="header"><a href="#" v-html="header.header"></a></slot>
            </li>
          </template>
        </ul>
      </div>
      <div class="col-sm-12">
        <div class="tab-content">
          <slot></slot>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'tabbedPanel',

  props: {
    // effect: {type: String, default: 'fadein'},
    justified: false,
    navStyle: {type: String, default: 'pane'},
    value: {type: Number, default: 0},
    tabClick: {type: Boolean, default: true}
  },
  data () {
    var index = this.value || 0
    return {
      index,
      headers: [],
      tabs: []
    }
  },
  watch: {
    index (val) {
      this.$emit('active', val)
      this.$emit('input', val)
    },
    value (val) {
      this.index = val
    }
  },
  computed: {
    show () { return this.tabs[this.index] || this.tabs[0] }
  },
  methods: {
    select (tab) {
      if (this.tabClick === true && !tab.disabled) {
        this.index = this.tabs.indexOf(tab)
        this.$emit('clickFunction')
      }
    },
    selectIndex (val) {
      this.index = val
    },
    currentTab () {
      return this.index
    }
  },
  created () {
    this._isTabs = true
  }
}
</script>
