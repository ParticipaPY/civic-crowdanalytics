<template>
  <div class="animated fadeIn">
    <div class="row">
      <div class="col">
        <div class="card card-accent-danger">
          <div class="card-header">
            Click on the sentiment labels to filter the graph
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
                    <input type="text" id="input1-group2" name="input1-group2" class="form-control" placeholder="Search idea" v-model="tableSearchTerm">
                  </div>
                </div>
              </div>
            </form>
            <vue-good-table :columns="tableColumns" :rows="tableRows" :defaultSortBy="{field: 'score', type: 'desc'}" :globalSearch="true" :paginate="true" :externalSearchQuery="tableSearchTerm" styleClass="table table-striped table-responsive">
              <template slot="table-row" scope="props">
                <td class="readmore"><read-more more-str="Read more" :text="props.row.idea" less-str="Read less" :max-chars="400"></read-more></td>
                <td><span :class="'badge ' + (props.row.sentiment == 'Positive' ? 'badge-success' : (props.row.sentiment == 'Neutral' ? 'badge-default' : 'badge-danger'))">{{props.row.sentiment}}</span></td>
                <td>{{props.row.score}}</td>
              </template>
            </vue-good-table>
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
      sentimentId: 0,
      tableSearchTerm: '',
      tableColumns: [
        {
          label: 'Content',
          field: 'idea',
          filtereable: true,
          width: '70%'
        },
        {
          label: 'Aggegate Sentiment',
          field: 'sentiment',
          filtereable: false
        },
        {
          label: 'Aggregate Score',
          field: 'score',
          type: 'number',
          filtereable: true
        }
      ],
      tableRows: []
    }
  },
  methods: {
    formatDataset: function () {
      let parsed = JSON.parse(this.data)
      let ret = []
      if (parsed.length > 0) {
        this.tableRows = parsed[0].ideas
        let positiveParsed = _.filter(parsed, (v, k) => v.sentiment === 'pos')[0]
        let neutralParsed = _.filter(parsed, (v, k) => v.sentiment === 'neu')[0]
        let negativeParsed = _.filter(parsed, (v, k) => v.sentiment === 'neg')[0]
        positiveParsed.ideas = _.orderBy(positiveParsed.ideas, ['score'], ['desc'])
        neutralParsed.ideas = _.orderBy(neutralParsed.ideas, ['score'], ['desc'])
        negativeParsed.ideas = _.orderBy(negativeParsed.ideas, ['score'], ['desc'])
        for (let pos of positiveParsed.ideas) {
          pos.sentiment = 'Positive'
        }
        for (let neu of neutralParsed.ideas) {
          neu.sentiment = 'Neutral'
        }
        for (let neg of negativeParsed.ideas) {
          neg.sentiment = 'Negative'
        }
        this.tableRows = this.tableRows.concat(positiveParsed.ideas, neutralParsed.ideas, negativeParsed.ideas)
      }
      return ret
    }
  },
  mounted () {
    Backend.getSentimentAnalysis(this.$route.params.analysisId).then(
      response => {
        this.data = response.data.result
        this.formatDataset(this.data)
        this.sentimentId = parseInt(this.$route.params.analysisId)
      }
    ).catch(
      e => {
        console.log(e)
      }
    )
  }
}
</script>
