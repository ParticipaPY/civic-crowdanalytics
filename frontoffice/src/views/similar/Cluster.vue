<template>
  <div class="animated fadeIn">
    <div class="row">
      <div class="col">
        <div class="card card-accent-warning">
          <div class="card-header">
            <dropdown class="float-right" type="transparent p-1">
              <i slot="button" class="icon-options-vertical"></i>
              <div slot="dropdown-menu" class="dropdown-menu dropdown-menu-right">
                <a class="dropdown-item" href="#">Print Chart</a>
                <li><a class="dropdown-item" href="#">Download as PNG Image</a></li>
                <li><a class="dropdown-item" href="#">Download as JPEG Image</a></li>
                <li><a class="dropdown-item" href="#">Download as SVG Image</a></li>
                <li><a class="dropdown-item" href="#">Download as PDF Document</a></li>
              </div>
            </dropdown>
          </div>
          <div class="card-block">
            <tabbed-panel v-model="activeTab" ref="graphCloudPanel" navStyle="pill">
              <tabbed-panel-tab header="Graph">
                <bubble-chart :analysis-id="clusterId"/>
              </tabbed-panel-tab>
              <tabbed-panel-tab header="Word Cloud">
                <div id="clouddiv">
                  <wordcloud :data="topTerms" nameKey="name" valueKey="value" ref="cloud" :wordClick="wordClick"></wordcloud>
                </div>
              </tabbed-panel-tab>
            </tabbed-panel>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <div class="card">
          <div class="card-header">
            Ideas
          </div>
          <div class="card-block">
            <form action="" method="post" class="form-horizontal">
              <div class="form-group row">
                <div class="col">
                  <div class="input-group">
                    <span class="input-group-btn">
                      <button type="button" class="btn btn-primary"><i class="fa fa-search"></i> Search</button>
                    </span>
                    <input type="text" id="input1-group2" name="input1-group2" class="form-control" placeholder="Search idea">
                  </div>
                </div>
              </div>
            </form>
            <table class="table table-striped table-responsive">
              <thead>
                <tr>
                  <th style="width:70%">Content</th>
                  <th>Cluster</th>
                  <th>Legends</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in flattened">
                  <td class="readmore"><read-more more-str="Read more" :text="item.content" less-str="Read less" :max-chars="400"></read-more></td>
                  <td><span :class="'badge ' + item.class">{{ item.cluster }}</span></td>
                  <td>{{ item.legends }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import BubbleChart from '../charts/BubbleChart'

import { dropdown } from 'vue-strap'
import tabbedPanel from '../../components/TabbedPanel/TabbedPanel'
import tabbedPanelTab from '../../components/TabbedPanel/Tab'
import wordcloud from 'vue-wordcloud'

import {Backend} from '../../Backend'
import _ from 'lodash'

export default {
  name: 'cluster',
  components: {
    BubbleChart,
    dropdown,
    wordcloud,
    tabbedPanel,
    tabbedPanelTab
  },
  methods: {
    renderWordcloud: function () {
      this.$el.querySelector('#clouddiv svg').remove()
      this.$refs.cloud.getSize()
      this.$refs.cloud.chart = this.$refs.cloud.createChart()
      this.$refs.cloud.renderChart()
      this.wordCloudWasRendered = true
    },
    wordClick: function (text, vm) {
      console.log(text)
      console.log(vm)
    },
    formatDataset: function () {
      let parsed = JSON.parse(this.data)
      if (parsed.length > 0) {
        for (let i in parsed) {
          for (let j of parsed[i].ideas) {
            let newobj = {}
            newobj.content = j.idea
            newobj.cluster = 'Cluster ' + i
            newobj.class = this.classArray[i]
            newobj.legends = _.map(parsed[i].top_terms, (t) => { return t.term }).join(', ')
            this.flattened.push(newobj)
          }
          for (let k of parsed[i].top_terms) {
            let newobj = {}
            newobj.name = k.term
            newobj.value = k.score
            this.topTerms.push(newobj)
          }
        }
      }
    }
  },
  watch: {
    activeTab (val) {
      if (val === 1 && !this.wordCloudWasRendered) {
        setTimeout(() => { this.renderWordcloud() }, 500)
      }
    },
    topTerms (n, o) {
      if (this.topTerms.length > 0) {
        this.renderWordcloud()
      }
    }
  },
  data: function () {
    return {
      flattened: [],
      classArray: ['badge-primary', 'badge-warning', 'badge-danger', 'badge-success', 'badge-info'],
      activeTab: 0,
      clusterId: 0,
      wordCloudWasRendered: false,
      topTermsHasFinishedLoading: false,
      topTerms: []
    }
  },
  mounted () {
    Backend.getDocumentClustering(this.$route.params.analysisId).then(
      response => {
        this.data = response.data.result
        this.formatDataset(this.data)
        this.clusterId = parseInt(this.$route.params.analysisId)
      }
    ).catch(
      e => {
        console.log(e)
      }
    )
  }
}

</script>
