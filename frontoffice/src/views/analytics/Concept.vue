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
                  <td>Parking</td>
                  <td>80</td>
                </tr>
                <tr>
                  <td>Cars</td>
                  <td>60</td>
                </tr>
                <tr>
                  <td>Drive</td>
                  <td>56</td>
                </tr>
                <tr>
                  <td>People</td>
                  <td>55</td>
                </tr>
                <tr>
                  <td>Reduce</td>
                  <td>43</td>
                </tr>
                <tr>
                  <td>Road</td>                
                  <td>38</td>
                </tr>
                <tr>
                  <td>Bike</td>                
                  <td>33</td>
                </tr>
                <tr>
                  <td>Park</td>                
                  <td>28</td>
                </tr>
                <tr>
                  <td>Buses</td>                
                  <td>20</td>
                </tr>
                <tr>
                  <td>Walk</td>                
                  <td>18</td>
                </tr>
                <tr>
                  <td>Avenue</td>                
                  <td>17</td>
                </tr>
                <tr>
                  <td>Allow</td>                
                  <td>10</td>
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
