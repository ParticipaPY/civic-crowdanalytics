<template>
  <div class="animated fadeIn">
    <div class="row">
      <div class="col">
        <div class="card card-accent-success">
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
              <line-chart :analysis-id="conceptId"/>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <div class="card">
          <div class="card-header">
            Concepts
          </div>
          <div class="card-block">
            <form action="" method="post" class="form-horizontal">
              <div class="form-group row">
                <div class="col">
                  <div class="input-group">
                    <span class="input-group-btn">
                      <button type="button" class="btn btn-primary"><i class="fa fa-search"></i> Search</button>
                    </span>
                    <input type="text" id="input1-group2" name="input1-group2" class="form-control" placeholder="Search concept" v-model="tableSearchTerm">
                  </div>
                </div>
              </div>
            </form>
            <vue-good-table :columns="tableColumns" :rows="tableRows" :defaultSortBy="{field: 'occurrences', type: 'desc'}" :globalSearch="true" :paginate="true" :externalSearchQuery="tableSearchTerm" styleClass="table table-striped table-responsive" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import LineChart from '../charts/LineChart'
import {Backend} from '../../Backend'
import { dropdown } from 'vue-strap'

export default {
  name: 'concept',
  components: {
    LineChart,
    dropdown
  },
  data () {
    return {
      data: [],
      parsed: [],
      labels: [],
      labelData: [],
      conceptId: 0,
      tableSearchTerm: '',
      tableColumns: [
        {
          label: 'Concept',
          field: 'concept',
          filtereable: true
        },
        {
          label: 'Occurrences',
          field: 'occurrences',
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
      this.parsed = parsed
      console.log(this.parsed)
      this.tableRows = this.parsed
      if (parsed.length > 0) {
        for (let o of parsed) {
          this.labels.push(o.concept)
          this.labelData.push(o.occurrences)
        }
      }
    }
  },
  mounted () {
    Backend.getConceptExtraction(this.$route.params.analysisId).then(
      response => {
        this.data = response.data.result
        this.formatDataset(this.data)
        this.conceptId = this.$route.params.analysisId
      }
    ).catch(
      e => {
        this.$router.push('/login')
      }
    )
  }
}
</script>
