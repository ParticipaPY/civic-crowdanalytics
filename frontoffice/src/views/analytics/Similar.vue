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
                <bubble-chart/>
              </tabbed-panel-tab>
              <tabbed-panel-tab header="Word Cloud">
                <div id="clouddiv">
                  <wordcloud :data="defaultWords" nameKey="name" valueKey="value" ref="cloud" :wordClick="wordClick"></wordcloud>
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
                  <th>Content</th>
                  <th>Cluster</th>
                  <th>Legends</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Remove and place the grass on the waterfront park lawn and continued to fix roads</td>
                  <td><span class="badge badge-primary">Cluster 0</span></td>
                  <td>need, fix, streets</td>
                </tr>
                <tr>
                  <td>Remove and place the grass on the waterfront park lawn and continued to fix roads</td>
                  <td><span class="badge badge-primary">Cluster 0</span></td>
                  <td>need, fix, streets</td>
                </tr>
                <tr>
                  <td>No Trash, couches in roads</td>
                  <td><span class="badge badge-primary">Cluster 0</span></td>
                  <td>need, fix, streets</td>
                </tr>
                <tr>
                  <td>Fix roads and homeless</td>
                  <td><span class="badge badge-primary">Cluster 0</span></td>
                  <td>need, fix, streets</td>
                </tr>
                <tr>
                  <td>Violence in Schools need to stop</td>
                  <td><span class="badge badge-warning">Cluster 1</span></td>
                  <td>roads, fix, need</td>
                </tr>
                <tr>
                  <td>Soltrans needs to run later at night</td>
                  <td><span class="badge badge-warning">Cluster 1</span></td>
                  <td>roads, fix, need</td>
                </tr>
                <tr>
                  <td>Provide more programing for adults in need of a shelter</td>
                  <td><span class="badge badge-warning">Cluster 1</span></td>
                  <td>roads, fix, need</td>
                </tr>
                <tr>
                  <td>Help w/ littering project</td>
                  <td><span class="badge badge-danger">Cluster 2</span></td>
                  <td>street, roads, need</td>
                </tr>
                <tr>
                  <td>Create attractive buildings</td>
                  <td><span class="badge badge-danger">Cluster 2</span></td>
                  <td>street, roads, need</td>
                </tr>
                <tr>
                  <td>Public Marketing campaign to support new buildings</td>
                  <td><span class="badge badge-danger">Cluster 2</span></td>
                  <td>street, roads, need</td>
                </tr>
                <tr>
                  <td>Streets clean up, dirty - looks ghetto</td>
                  <td><span class="badge badge-success">Cluster 3</span></td>
                  <td>streets, need, roads</td>
                </tr>
                <tr>
                  <td>Street pavements, require home owners to maintain landscapes</td>
                  <td><span class="badge badge-success">Cluster 3</span></td>
                  <td>streets, need, roads</td>
                </tr>
                <tr>
                  <td>Street repair</td>
                  <td><span class="badge badge-success">Cluster 3</span></td>
                  <td>streets, need, roads</td>
                </tr>
                <tr>
                  <td>Fix trash problem</td>
                  <td><span class="badge badge-info">Cluster 4</span></td>
                  <td>fix, streets, need</td>
                </tr>
                <tr>
                  <td>Fix the Cemetary</td>
                  <td><span class="badge badge-info">Cluster 4</span></td>
                  <td>fix, streets, need</td>
                </tr>
                <tr>
                  <td>Fix schools</td>
                  <td><span class="badge badge-info">Cluster 4</span></td>
                  <td>fix, streets, need</td>
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

export default {
  name: 'similar',
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
    }
  },
  watch: {
    activeTab (val) {
      if (val === 1 && !this.wordCloudWasRendered) {
        setTimeout(() => { this.renderWordcloud() }, 500)
      }
    }
  },
  data: function () {
    return {
      activeTab: 0,
      wordCloudWasRendered: false,
      defaultWords: [
        {
          'name': 'Cat',
          'value': 26
        },
        {
          'name': 'fish',
          'value': 19
        },
        {
          'name': 'things',
          'value': 18
        },
        {
          'name': 'look',
          'value': 16
        },
        {
          'name': 'two',
          'value': 15
        },
        {
          'name': 'fun',
          'value': 9
        },
        {
          'name': 'know',
          'value': 9
        },
        {
          'name': 'good',
          'value': 9
        },
        {
          'name': 'play',
          'value': 6
        }
      ]
    }
  }
}

</script>
