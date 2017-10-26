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
            <div>
              <bubble-chart/>
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
                  <th>Cluster</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Remove and place the grass on the waterfront park lawn and continued to fix roads</td>
                  <td><span class="badge badge-primary">Cluster 0</span></td>
                </tr>
                <tr>
                  <td>Remove and place the grass on the waterfront park lawn and continued to fix roads</td>
                  <td><span class="badge badge-primary">Cluster 0</span></td>
                </tr>
                <tr>
                  <td>No Trash, couches in roads</td>
                  <td><span class="badge badge-primary">Cluster 0</span></td>
                </tr>
                <tr>
                  <td>Fix roads and homeless</td>
                  <td><span class="badge badge-primary">Cluster 0</span></td>
                </tr>
                <tr>
                  <td>Violence in Schools need to stop</td>
                  <td><span class="badge badge-warning">Cluster 1</span></td>
                </tr>
                <tr>
                  <td>Soltrans needs to run later at night</td>
                  <td><span class="badge badge-warning">Cluster 1</span></td>
                </tr>
                <tr>
                  <td>Provide more programing for adults in need of a shelter</td>
                  <td><span class="badge badge-warning">Cluster 1</span></td>
                </tr>
                <tr>
                  <td>Help w/ littering project</td>
                  <td><span class="badge badge-danger">Cluster 2</span></td>
                </tr>
                <tr>
                  <td>Create attractive buildings</td>
                  <td><span class="badge badge-danger">Cluster 2</span></td>
                </tr>
                <tr>
                  <td>Public Marketing campaign to support new buildings</td>
                  <td><span class="badge badge-danger">Cluster 2</span></td>
                </tr>
                <tr>
                  <td>Streets clean up, dirty - looks ghetto</td>
                  <td><span class="badge badge-success">Cluster 3</span></td>
                </tr>
                <tr>
                  <td>Street pavements, require home owners to maintain landscapes</td>
                  <td><span class="badge badge-success">Cluster 3</span></td>
                </tr>
                <tr>
                  <td>Street repair</td>
                  <td><span class="badge badge-success">Cluster 3</span></td>
                </tr>
                <tr>
                  <td>Fix trash problem</td>
                  <td><span class="badge badge-info">Cluster 4</span></td>
                </tr>
                <tr>
                  <td>Fix the Cemetary</td>
                  <td><span class="badge badge-info">Cluster 4</span></td>
                </tr>
                <tr>
                  <td>Fix schools</td>
                  <td><span class="badge badge-info">Cluster 4</span></td>
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

export default {
  name: 'similar',
  components: {
    BubbleChart,
    dropdown
  }
}
</script>
