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
              <scatter-chart/>
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
                <tr>
                  <td>I want to help special kids because I love little kids and want to help them.  Why is needed? It is needed because they need help to learn.</td>
                  <td>
                    <span class="badge badge-success">Positive</span>
                  </td>
                  <td>0.9538</td>
                </tr>
                <tr>
                  <td>Vallejo Beautification.  Why is needed? To improve tourism and support community.</td>
                  <td>
                    <span class="badge badge-default">Positive</span>
                  </td>
                  <td>0.886</td>
                </tr>
                <tr>
                  <td>Restore the downtown and make it more attractive.  Why is needed? To make Vallejo a better place.</td>
                  <td>
                    <span class="badge badge-danger">Positive</span>
                  </td>
                  <td>0.9022</td>
                </tr>
                <tr>
                  <td>Community Park. To have a nicer park for everyone  Why is needed?To enjoy scenery and kids who want to play safe.</td>
                  <td>
                    <span class="badge badge-danger">Positive</span>
                  </td>
                  <td>0.8934</td>
                </tr>
                <tr>
                  <td>Campaign to promote positive things in Vallejo. Why is needed? Highlight the best in Vallejo.</td>                
                  <td>
                    <span class="badge badge-success">Positive</span>
                  </td>
                  <td>0.9584</td>
                </tr>
                <tr>
                  <td>Most work commuters are coming from the South Bay. Why not run some county-wide shuttles that pick people up from Sunnyvale, San Jose, etc and take them to work in the Stanford Research Park? Some companies there can afford their own shuttle systems, but others can't. Can the TMA help them pool resources to establish a multi-company or public shuttles to the South Bay?</td>                
                  <td>
                    <span class="badge badge-default">Neutral</span>
                  </td>
                  <td>-0.10</td>
                </tr>
                <tr>
                  <td>All new development should be required to add some bike parking. Stanford shopping center is really lacking in this.</td>                
                  <td>
                    <span class="badge badge-danger">Negative</span>
                  </td>
                  <td>-0.68</td>
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

import { dropdown } from 'vue-strap'

export default {
  name: 'sentiment',
  components: {
    ScatterChart,
    dropdown
  }
}
</script>
