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
              <line-chart/>
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
                    <input type="text" id="input1-group2" name="input1-group2" class="form-control" placeholder="Search concept">
                  </div>
                </div>
              </div>
            </form>
            <table class="table table-striped table-responsive">
              <thead>
                <tr>
                  <th>Concept</th>
                  <th>Occurrences</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Transportation</td>                
                  <td>348</td>
                </tr>
                <tr>
                  <td>Education & Training</td>
                  <td>297</td>
                </tr>
                <tr>
                  <td>Social Services</td>
                  <td>295</td>
                </tr>
                <tr>
                  <td>Parks & Recreation</td>
                  <td>253</td>
                </tr>
                <tr>
                  <td>City Infrastructure</td>
                  <td>245</td>
                </tr>
                <tr>
                  <td>Public Safety</td>
                  <td>164</td>
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

import LineChart from '../charts/LineChart'

import { dropdown } from 'vue-strap'

export default {
  name: 'concept',
  components: {
    LineChart,
    dropdown
  }
}
</script>
