<template>
  <div class="animated fadeIn">
    <div class="row">
      <div class="col">
        <div class="card card-accent-danger">
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
            <div>
              <scatter-chart :analysis-id="sentimentId"/>
            </div>
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
                  <th>Aggregate Sentiment</th>
                  <th>Aggregate Score</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in positiveData">
                  <td>{{item.idea}}</td>
                  <td>
                    <span class="badge badge-success">Positive</span>
                  </td>
                  <td>{{item.score}}</td>
                </tr>
                <tr v-for="item in neutralData">
                  <td>{{item.idea}}</td>
                  <td>
                    <span class="badge badge-default">Neutral</span>
                  </td>
                  <td>{{item.score}}</td>
                </tr>
                <tr v-for="item in negativeData">
                  <td>{{item.idea}}</td>
                  <td>
                    <span class="badge badge-danger">Negative</span>
                  </td>
                  <td>{{item.score}}</td>
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

import ScatterChart from '../charts/ScatterChart'
import {Backend} from '../../Backend'
import { dropdown } from 'vue-strap'
import _ from 'lodash'

export default {
  name: 'sentiment',
  components: {
    ScatterChart,
    dropdown
  },
  data () {
    return {
      data: [],
      positiveData: [],
      neutralData: [],
      negativeData: [],
      sentimentId: 0
    }
  },
  methods: {
    formatDataset: function () {
      let parsed = JSON.parse(this.data)
      let ret = []
      if (parsed.length > 0) {
        let positiveParsed = _.filter(parsed, (v, k) => v.sentiment === 'pos')[0]
        let neutralParsed = _.filter(parsed, (v, k) => v.sentiment === 'neu')[0]
        let negativeParsed = _.filter(parsed, (v, k) => v.sentiment === 'neg')[0]
        positiveParsed.ideas = _.orderBy(positiveParsed.ideas, ['score'], ['desc'])
        neutralParsed.ideas = _.orderBy(neutralParsed.ideas, ['score'], ['desc'])
        negativeParsed.ideas = _.orderBy(negativeParsed.ideas, ['score'], ['desc'])
        for (let pos of positiveParsed.ideas) {
          let obj = {}
          obj.score = pos.score
          obj.idea = pos.idea
          this.positiveData.push(obj)
        }
        for (let neu of neutralParsed.ideas) {
          let obj = {}
          obj.score = neu.score
          obj.idea = neu.idea
          this.neutralData.push(obj)
        }
        for (let neg of negativeParsed.ideas) {
          let obj = {}
          obj.score = neg.score
          obj.idea = neg.idea
          this.negativeData.push(obj)
        }
        ret.push(this.positiveData, this.neutralData, this.negativeData)
      }
      return ret
    }
  },
  mounted () {
    Backend.getSentimentAnalysis(this.$route.params.analysisId).then(
      response => {
        this.data = response.data.result
        this.formatDataset(this.data)
        this.sentimentId = this.$route.params.analysisId
      }
    ).catch(
      e => {
        console.log(e)
      }
    )
  }
}
</script>
