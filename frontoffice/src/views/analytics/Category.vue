<template>
  <div class="animated fadeIn">
    <div class="row">
      <div class="col">
        <div class="card card-accent-primary">
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
              <bar-chart/>
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
                  <th>Subcategory 1</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Free public transportation</td>
                  <td>public transit</td>
                  <td>incentive to use public transit</td>
                </tr>
                <tr>
                  <td>Enforce distracted driving laws</td>
                  <td>private transit</td>
                  <td>law enforcement</td>
                </tr>
                <tr>
                  <td>Protected bike lanes which only bikes and resident cars (with sticker) could access especially along midtwon to hanson way</td>
                  <td>non-motor powered transit</td>
                  <td>infrastructure for non-motor powered transit</td>
                </tr>
                <tr>
                  <td>More protected bike-friendly streets and boulevards</td>
                  <td>non-motor powered transit</td>
                  <td>infrastructure for non-motor powered transit</td>
                </tr>
                <tr>
                  <td>More bike friendly streets</td>                
                  <td>non-motor powered transit</td>
                  <td>infrastructure for non-motor powered transit</td>
                </tr>
                <tr>
                  <td>Safer crossing in busier streets like el camino and alma</td>                
                  <td>non-motor powered transit</td>
                  <td>infrastructure for non-motor powered transit</td>
                </tr>
                <tr>
                  <td>Safer bicycle parking near retail spaces</td>                
                  <td>non-motor powered transit</td>
                  <td>infrastructure for non-motor powered transit</td>
                </tr>
                <tr>
                  <td>Safe ride sharing apps exclusively reserved to known community people</td>                
                  <td>non-motor powered transit</td>
                  <td>public transit</td>
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

import { dropdown } from 'vue-strap'

export default {
  name: 'category',
  components: {
    BarChart,
    dropdown
  }
}
</script>
