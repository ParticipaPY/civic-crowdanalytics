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
                  <td>city</td>                
                  <td>139</td>
                </tr>
                <tr>
                  <td>homeless</td>
                  <td>136</td>
                </tr>
                <tr>
                  <td>school</td>
                  <td>118</td>
                </tr>
                <tr>
                  <td>fix</td>
                  <td>110</td>
                </tr>
                <tr>
                  <td>community</td>
                  <td>98</td>
                </tr>
                <tr>
                  <td>help</td>
                  <td>80</td>
                </tr>
                <tr>
                  <td>youth</td>
                  <td>77</td>
                </tr>
                <tr>
                  <td>street</td>
                  <td>70</td>
                </tr>
                <tr>
                  <td>housing</td>
                  <td>66</td>
                </tr>
                <tr>
                  <td>repair</td>
                  <td>57</td>
                </tr>
                <tr>
                  <td>program</td>
                  <td>55</td>
                </tr>
                <tr>
                  <td>road</td>
                  <td>54</td>
                </tr>
                <tr>
                  <td>trash</td>
                  <td>53</td>
                </tr>
                <tr>
                  <td>park</td>
                  <td>53</td>
                </tr>
                <tr>
                  <td>center</td>
                  <td>51</td>
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
