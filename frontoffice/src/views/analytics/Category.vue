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
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Music teaching program. People volunteering to teach about music. Why is needed? Music allows people to have creative freedom.</td>
                  <td>Education & Training</td>
                </tr>
                <tr>
                  <td>Book clubs for kids, Bookstore for all. Book club for kids and community. Why is needed? To promote reading.</td>
                  <td>Education & Training</td>
                </tr>
                <tr>
                  <td>Summer youth program. Why is needed? Keep kids busy.</td>
                  <td>Education & Training</td>
                </tr>
                <tr>
                  <td>Funding school. More funding to the schools equipment. Why is needed? Some schools have really old equipment.</td>
                  <td>Education & Training</td>
                </tr>
                <tr>
                  <td>Cleaning grounds, landscaping and enforcing cleaniness around Vallejo.</td>
                  <td>City Infrastructure</td>
                </tr>
                <tr>
                  <td>Paint buildings, give us something to look at, fix infastrcuture, make Vallejo beautiful.</td>
                  <td>City Infrastructure</td>
                </tr>
                <tr>
                  <td>Fix potholes, better lighting, decent bar, keep golf course.</td>
                  <td>City Infrastructure</td>
                </tr>
                <tr>
                  <td>New Street Lights. Remove and replace old street lights. Why is needed? Because the lights are damage.</td>
                  <td>City Infrastructure</td>
                </tr>
                <tr>
                  <td>Youth activities, paving potholes.</td>
                  <td>Parks & Recreation</td>
                </tr>
                <tr>
                  <td>Better parks and cheaper bus prices.</td>
                  <td>Parks & Recreation</td>
                </tr>
                <tr>
                  <td>More things to do in Vallejo.</td>
                  <td>Parks & Recreation</td>
                </tr>
                <tr>
                  <td>Public Kayak launch.</td>
                  <td>Parks & Recreation</td>
                </tr>
                <tr>
                  <td>Better neighborhood watch.</td>
                  <td>Public Safety</td>
                </tr>
                <tr>
                  <td>Reduce Gang activities in schools.</td>
                  <td>Public Safety</td>
                </tr>
                <tr>
                  <td>Double the police force.</td>
                  <td>Public Safety</td>
                </tr>
                <tr>
                  <td>Smoking ashtrays in front of establishments.</td>
                  <td>Public Safety</td>
                </tr>
                <tr>
                  <td>Childcare for library customers.</td>
                  <td>Social Services</td>
                </tr>
                <tr>
                  <td>A program to help homeless people eventually become independent.</td>
                  <td>Social Services</td>
                </tr>
                <tr>
                  <td>Improve senior center.</td>
                  <td>Social Services</td>
                </tr>
                <tr>
                  <td>Urban Farm, expand the pilot project.</td>
                  <td>Social Services</td>
                </tr>
                <tr>
                  <td>Better roads, more public art.</td>
                  <td>Transportation</td>
                </tr>
                <tr>
                  <td>More charging stations for electric vechicles and cheaper transit.</td>
                  <td>Transportation</td>
                </tr>
                <tr>
                  <td>Bike lanes, Bike Repair stations, bicycle racks, free bicycles for rent, Bicycle festival.</td>
                  <td>Transportation</td>
                </tr>
                <tr>
                  <td>City funded buses to improve transportation at late night hours.</td>
                  <td>Transportation</td>
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
