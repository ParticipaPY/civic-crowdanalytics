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
                  <td>Campaign to promote positive things in Vallejo. Why is needed? Highlight the best in Vallejo.</td>                
                  <td>
                    <span class="badge badge-success">Positive</span>
                  </td>
                  <td>0.9584</td>
                </tr>
                <tr>
                  <td>I want to help special kids because I love little kids and want to help them.  Why is needed? It is needed because they need help to learn.</td>
                  <td>
                    <span class="badge badge-success">Positive</span>
                  </td>
                  <td>0.9538</td>
                </tr>
                <tr>
                  <td>Restore the downtown and make it more attractive.  Why is needed? To make Vallejo a better place.</td>
                  <td>
                    <span class="badge badge-success">Positive</span>
                  </td>
                  <td>0.9022</td>
                </tr>
                <tr>
                  <td>Community Park. To have a nicer park for everyone  Why is needed?To enjoy scenery and kids who want to play safe.</td>
                  <td>
                    <span class="badge badge-success">Positive</span>
                  </td>
                  <td>0.8934</td>
                </tr>
                <tr>
                  <td>Vallejo Beautification.  Why is needed? To improve tourism and support community.</td>
                  <td>
                    <span class="badge badge-success">Positive</span>
                  </td>
                  <td>0.886</td>
                </tr>
                <tr>
                  <td>Bring in more people with stable incomes.</td>                
                  <td>
                    <span class="badge badge-default">Neutral</span>
                  </td>
                  <td>0.296</td>
                </tr>
                <tr>
                  <td>More policing. Why is needed? Prevent crimes.</td>                
                  <td>
                    <span class="badge badge-default">Neutral</span>
                  </td>
                  <td>0.0258</td>
                </tr>
                <tr>
                  <td>Multi youth sports complex @ East Vallejo  Little League. Why is needed? Create revenue</td>                
                  <td>
                    <span class="badge badge-default">Neutral</span>
                  </td>
                  <td>0.2111</td>
                </tr>
                <tr>
                  <td>Fix schools.</td>                
                  <td>
                    <span class="badge badge-default">Neutral</span>
                  </td>
                  <td>0.0</td>
                </tr>
                <tr>
                  <td>Keep farmers market open until 5pm.</td>                
                  <td>
                    <span class="badge badge-default">Neutral</span>
                  </td>
                  <td>0.0</td>
                </tr>
                <tr>
                  <td>Road repair because we have bad roads.</td>                
                  <td>
                    <span class="badge badge-danger">Negative</span>
                  </td>
                  <td>-0.5423</td>
                </tr>
                <tr>
                  <td>Less gentrification and police brutality.</td>                
                  <td>
                    <span class="badge badge-danger">Negative</span>
                  </td>
                  <td>-0.577</td>
                </tr>
                <tr>
                  <td>Violence in Schools need to stop.</td>                
                  <td>
                    <span class="badge badge-danger">Negative</span>
                  </td>
                  <td>-0.743</td>
                </tr>
                <tr>
                  <td>End crime. Why is needed? Because there are a lot of robberies.</td>                
                  <td>
                    <span class="badge badge-danger">Negative</span>
                  </td>
                  <td>-0.7906</td>
                </tr>
                <tr>
                  <td>End police brutality. Why is needed? Stop beating black and brown people.</td>                
                  <td>
                    <span class="badge badge-danger">Negative</span>
                  </td>
                  <td>-0.9217</td>
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
