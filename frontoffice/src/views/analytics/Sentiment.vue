<template>
  <div class="animated fadeIn">
    <div class="row">
      <div class="col">
        <div class="card card-accent-danger">
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
                  <td>Parking should be unbundled - i.e. you pay if you want to use it. Lots and lots of young people and seniors would love to live in housing where they're not implicitly paying for parking they don't use and lots of them don't need or want a car, particularly if they're living right near the Caltrain.</td>
                  <td>
                    <span class="badge badge-success">Positive</span>
                  </td>
                  <td>0.91</td>
                </tr>
                <tr>
                  <td>All new multifamily housing should come with at least one zipcar.</td>
                  <td>
                    <span class="badge badge-default">Neutral</span>
                  </td>
                  <td>0.20</td>
                </tr>
                <tr>
                  <td>We should work with companies like Lyft and Uber to create "on-demand" shuttles. I.e. cars or vans could pick up multiple passengers where and when they need it, instead of running a mindless shuttle that is inflexible and often not useful.</td>
                  <td>
                    <span class="badge badge-danger">Negative</span>
                  </td>
                  <td>-0.60</td>
                </tr>
                <tr>
                  <td>Without convenient neighborhood-based public transit to and from schools, many parents are going to continue to drive their children to and from school, thus adding to traffic problems.</td>
                  <td>
                    <span class="badge badge-danger">Negative</span>
                  </td>
                  <td>-0.54</td>
                </tr>
                <tr>
                  <td>Part of the problem with mixed use development is that the FAR for the housing portion is really small. We should be encouraging ground floor retail + 3 floors of housing or retail + commercial + 2 floors of housing. But the current restrictions don't allow you to build that much housing, which exacerbates the jobs housing imbalance.</td>                
                  <td>
                    <span class="badge badge-success">Positive</span>
                  </td>
                  <td>-0.73</td>
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

export default {
  name: 'sentiment',
  components: {
    ScatterChart
  }
}
</script>
