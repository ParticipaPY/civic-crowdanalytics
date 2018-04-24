<template>
  <div class="animated fadeIn">
    <div class="row">
      <div class="col">
        <div class="card card-accent-primary">
          <div class="card-header"><!--
            <dropdown class="float-right" type="transparent p-1">
              <i slot="button" class="icon-options-vertical"></i>
              <div slot="dropdown-menu" class="dropdown-menu dropdown-menu-right">
                <a class="dropdown-item" href="#">Print Chart</a>
                <li><a class="dropdown-item" href="#">Download as PNG Image</a></li>
                <li><a class="dropdown-item" href="#">Download as JPEG Image</a></li>
                <li><a class="dropdown-item" href="#">Download as SVG Image</a></li>
                <li><a class="dropdown-item" href="#">Download as PDF Document</a></li>
              </div>
            </dropdown>-->
          </div>
          <div class="card-block">
            <div>
              <bar-chart :analysisId="categoryId"/>
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
                  <th>Main Category</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in flattened">
                  <td>{{ item.idea }}</td>
                  <td>{{ item.category }}</td>
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

import BarChart from '../charts/BarChart'
import {Backend} from '../../Backend'
import { dropdown } from 'vue-strap'

export default {
  name: 'classification',
  components: {
    BarChart,
    dropdown
  },
  data () {
    return {
      data: [],
      flattened: [],
      categoryId: 0
    }
  },
  methods: {
    formatDataset: function () {
      let parsed = JSON.parse(this.data)
      if (parsed.length > 0) {
        for (let cat of parsed) {
          for (let i of cat.ideas) {
            let newobj = {}
            newobj.category = cat.category
            newobj.idea = i.idea
            this.flattened.push(newobj)
          }
        }
      }
    }
  },
  mounted () {
    Backend.getDocumentClassification(this.$route.params.analysisId).then(
      response => {
        this.data = response.data.result
        this.formatDataset(this.data)
        this.categoryId = this.$route.params.analysisId
      }
    ).catch(
      e => {
        this.$router.push('/login')
      }
    )
  }
}
</script>
