<template>
  <div class="animated fadeIn">
    <div class="row">
      <div class="col-md-8">
        <div class="row" id="top-cards">
          <div class="col-md-3">
            <div class="card card-inverse card-success">
              <div class="card-block p-3 clearfix">
                <div class="float-left">
                  <h2 class="card-title"><b>3</b></h2>
                  <p class="card-text">Active projects</p>
                </div>
                <div class="h1 text-muted text-right">
                  <i class="icon-briefcase"></i>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card card-inverse card-primary">
              <div class="card-block p-3 clearfix">
                <div class="float-left">
                  <h2 class="card-title"><b>5</b></h2>
                  <p class="card-text">Archived projects</p>
                </div>
                <div class="h1 text-muted text-right">
                  <i class="icon-folder"></i>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card card-inverse card-warning">
              <div class="card-block p-3 clearfix">
                <div class="float-left">
                  <h2 class="card-title"><b>25</b></h2>
                  <p class="card-text">Datasets</p>
                </div>
                <div class="h1 text-muted text-right">
                  <i class="icon-chart"></i>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card card-inverse card-danger">
              <div class="card-block p-3 clearfix">
                <div class="float-left">
                  <h2 class="card-title"><b>50</b></h2>
                  <p class="card-text">Analysis reports</p>
                </div>
                <div class="h1 text-muted text-right">
                  <i class="icon-docs"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col">
            <router-link :to="'/dashboard/projects/new'" class="btn btn-primary"><i class="fa fa-plus-circle font-lg"></i> New project</router-link>
          </div>
        </div>
        
        <div class="row" id="project-box" v-for="project in projects">
          <div class="col-md-12 title">
            <input type="checkbox" :name="'project_check_' + project.id" :id="'project_check_' + project.id" v-model="selectedProjects" :value="project.id">
            <label :for="'project_check_' + project.id"></label>
            <router-link :to='{ name: "Project Home", params: { projectId: project.id }}'>{{project.name}}</router-link>
            <div class="actions">
              <a @click="toggleDetails($event)">Hide Details</a>
              <a href="#">Edit</a>
            </div>
          </div>
          <transition name="slide-fade">
            <div class="details">
              <div class="col-md-12">
                <div class="meta">
                  <div><i class="fa fa-user"></i>Project Owner: <strong>{{ fullName(project.owner.first_name, project.owner.last_name) }}</strong></div>
                  <div><i class="fa fa-calendar"></i>Created Date: <strong>{{project.created | shortDate}}</strong></div>
                  <div><i class="fa fa-calendar"></i>Last Modified: <strong>{{project.modified | shortDate}}</strong></div>
                  <div><i class="fa fa-database"></i>Data Sets: <strong>{{ project.datasets.length }} {{ project.datasets.length == 1 ? 'set' : 'sets' }}</strong></div>
                  <div><i class="fa fa-file-text"></i>Analysis: <strong>{{ project.analysis.length }}</strong></div>
                </div>
              </div>
              <div class="col-md-12">
                <p class="subtitle"><strong>Team Members</strong></p>
                <div class="faces" v-for="user in project.users">
                  <img src="static/img/avatars/6.jpg">
                </div>
              </div>
              <div class="col-md-12" style="display:none">
                <p class="subtitle"><strong>Latest Analysis Reports</strong></p>
                <table>
                  <thead>
                    <tr>
                      <th>Report Name</th>
                      <th>Analysis Type</th>
                      <th>Date Created</th>
                      <th>Created By</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><i class="fa fa-file-text"></i><a href="#">Third Analysis Report Dolor.pdf</a></td>
                      <td>Category - Cluster</td>
                      <td>Jan 20, 2015</td>
                      <td>John Blacksmith</td>
                    </tr>
                    <tr>
                      <td><i class="fa fa-file-text"></i><a href="#">Second Analysis Report Ipsum.pdf</a></td>
                      <td>Category - Concept</td>
                      <td>Jan 17, 2015</td>
                      <td>Rebecca Roberts</td>
                    </tr>
                    <tr>
                      <td><i class="fa fa-file-text"></i><a href="#">First Analysis Report Lorem.pdf</a></td>
                      <td>Sentiment Analysis</td>
                      <td>Nov 13, 2015</td>
                      <td>Tim Brown</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </transition>
        </div>
      </div>
      <div class="col-md-4">
        <div id="notifications">
          <h1>Notifications</h1>
          <ul>
            <li>
              <div class="h1 icon"><i class="icon-doc"></i></div>
              <p>You have been invited by <strong>Meredith Sandler</strong> to join project <strong>Lorem Ipsum Dolor Project Name</strong>.</p>
              <div class="time">5 minutes ago</div>
              <div class="clearfix">&nbsp;</div>
            </li>
            <li>
              <div class="h1 icon"><i class="icon-doc"></i></div>
              <p>You have been invited by <strong>Meredith Sandler</strong> to join project <strong>Lorem Ipsum Dolor Project Name</strong>.</p>
              <div class="time">5 minutes ago</div>
              <div class="clearfix">&nbsp;</div>
            </li>
            <li>
              <div class="h1 icon"><i class="icon-doc"></i></div>
              <p>You have been invited by <strong>Meredith Sandler</strong> to join project <strong>Lorem Ipsum Dolor Project Name</strong>.</p>
              <div class="time">5 minutes ago</div>
              <div class="clearfix">&nbsp;</div>
            </li>
            <li>
              <div class="h1 icon"><i class="icon-doc"></i></div>
              <p>You have been invited by <strong>Meredith Sandler</strong> to join project <strong>Lorem Ipsum Dolor Project Name</strong>.</p>
              <div class="time">5 minutes ago</div>
              <div class="clearfix">&nbsp;</div>
            </li>
            <li>
              <div class="h1 icon"><i class="icon-doc"></i></div>
              <p>You have been invited by <strong>Meredith Sandler</strong> to join project <strong>Lorem Ipsum Dolor Project Name</strong>.</p>
              <div class="time">5 minutes ago</div>
              <div class="clearfix">&nbsp;</div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {Backend} from '../Backend'
import moment from 'moment'

export default {
  name: 'dashboardnew',
  components: {
    moment
  },
  methods: {
    toggleDetails (event) {
      console.log(event)
    },
    fullName (first, last) {
      return first + ' ' + last
    }
  },
  created: function () {
    Backend.projects().then(
      response => {
        this.projects = response.data
      }
    ).catch(
      e => {
        console.log(e)
      }
    )
  },
  data () {
    return {
      selectedProjects: [],
      projects: []
    }
  },
  filters: {
    shortDate: function (date) {
      return moment(date).format('MMM Do, YYYY')
    }
  }
}
</script>
