<template>
  <div class="animated fadeIn">
    <div class="row">
      <!-- <div class="col">
        <div class="card card-accent-primary">
          <div class="card-block p-3 clearfix">
            <!-- <i class="fa fa-cogs bg-primary p-3 font-2xl mr-3 float-left"></i> 
            <div class="h1 text-muted text-right">
              <i class="icon-people"></i>
            </div>
            <h2 class="card-title"><b>850</b></h2>
            <p class="card-text">Participants</p>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="card card-accent-success">
          <div class="card-block p-3 clearfix">
            <!-- <i class="fa fa-cogs bg-primary p-3 font-2xl mr-3 float-left"></i>
            <div class="h1 text-muted text-right">
              <i class="icon-speech"></i>
            </div>
            <h2 class="card-title"><b>230</b></h2>
            <p class="card-text">Ideas</p>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="card card-accent-warning">
          <div class="card-block p-3 clearfix">
            <!-- <i class="fa fa-cogs bg-primary p-3 font-2xl mr-3 float-left"></i>
            <div class="h1 text-muted text-right">
              <i class="icon-bubbles"></i>
            </div>
            <h2 class="card-title"><b>400</b></h2>
            <p class="card-text">Comments</p>
          </div>
        </div>
      </div><!--/.col-->
      <div class="col-sm-6 col-lg-3">
        <div class="card card-inverse card-success">
          <div class="card-block p-3 clearfix">
            <div class="h1 text-muted text-right">
              <i class="icon-graph"></i>
            </div>
            <h2 class="card-title"><b>15</b></h2>
            <p class="card-text">Unique concepts</p>
          </div>
          <!-- <card-line1-chart-example class="chart-wrapper px-3" style="height:70px;" height="70"/> -->
          <div class="card-footer px-3 py-2">
            <router-link :to="'concept'" class="font-weight-bold font-xs btn-block text-muted" append><i class="fa fa-angle-right float-right font-lg"></i> View More</router-link>
          </div>
        </div>
      </div><!--/.col-->
      <div class="col-sm-6 col-lg-3">
        <div class="card card-inverse card-primary">
          <div class="card-block p-3 clearfix">
            <div class="h1 text-muted text-right">
              <i class="icon-chart"></i>
            </div>
            <h2 class="card-title"><b>267</b></h2>
            <p class="card-text">Avg. ideas per category</p>
          </div>
          <div class="card-footer px-3 py-2">
            <router-link :to="'category'" class="font-weight-bold font-xs btn-block text-muted" append><i class="fa fa-angle-right float-right font-lg"></i> View More</router-link>
          </div>
          <!-- <card-line1-chart-example class="chart-wrapper px-3" style="height:70px;" height="70"/> -->
        </div>
      </div><!--/.col-->
      <div class="col-sm-6 col-lg-3">
        <div class="card card-inverse card-warning">
          <div class="card-block p-3 clearfix">
            <div class="h1 text-muted text-right">
              <i class="icon-share"></i>
            </div>
            <h2 class="card-title"><b>5</b></h2>
            <p class="card-text">Clusters of Ideas</p>
          </div>
          <div class="card-footer px-3 py-2">
            <router-link :to="'similar'" class="font-weight-bold font-xs btn-block text-muted" append><i class="fa fa-angle-right float-right font-lg"></i> View More</router-link>
          </div>
          <!-- <card-line1-chart-example class="chart-wrapper px-3" style="height:70px;" height="70"/> -->
        </div>
      </div><!--/.col-->
      <div class="col-sm-6 col-lg-3">
        <div class="card card-inverse card-danger">
          <div class="card-block p-3 clearfix">
            <div class="h1 text-muted text-right">
              <i class="icon-equalizer"></i>
            </div>
            <!-- <div class="btn-group float-right">
              <dropdown class="float-right" type="transparent p-0">
                <i slot="button" class="icon-settings"></i>
                <div slot="dropdown-menu" class="dropdown-menu dropdown-menu-right">
                  <a class="dropdown-item" href="#">Action</a>
                  <a class="dropdown-item" href="#">Another action</a>
                  <a class="dropdown-item" href="#">Something else here</a>
                </div>
              </dropdown>
            </div>  -->
            <h2 class="card-title"><b>0.177</b></h2>
            <p class="card-text">Overall sentiment</p>
          </div>
          <!-- <card-bar-chart-example class="chart-wrapper px-3" style="height:70px;" height="70"/> -->
          <div class="card-footer px-3 py-2">
            <router-link :to="{name: 'Sentiment Analysis', params: {analysisId: 1}}" class="font-weight-bold font-xs btn-block text-muted"><i class="fa fa-angle-right float-right font-lg"></i> View More</router-link>
          </div>
        </div>
      </div><!--/.col-->
    </div><!--/.row-->
    
    <div class="">
    <div class="row">
      <div class="col-sm-12 col-lg-6">
        <div class="card card-accent-success">
          <div class="card-header">
            Concept Occurrences
            <dropdown class="float-right" type="transparent p-1">
              <i slot="button" class="icon-options-vertical"></i>
              <div slot="dropdown-menu" class="dropdown-menu dropdown-menu-right">
                <router-link class="dropdown-item" :to="'/dashboard/projects/vallejo-2017/concept'">View Fullscreen</router-link>
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
      <div class="col-sm-12 col-lg-6">
        <div class="card card-accent-primary">
          <div class="card-header">
            Category Summary
            <dropdown class="float-right" type="transparent p-1">
              <i slot="button" class="icon-options-vertical"></i>
              <div slot="dropdown-menu" class="dropdown-menu dropdown-menu-right">
                <router-link class="dropdown-item" :to="'/dashboard/projects/vallejo-2017/category'">View Fullscreen</router-link>
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
      <div class="col-sm-12 col-lg-6">
        <div class="card card-accent-warning">
          <div class="card-header">
            Clusters of Ideas
            <dropdown class="float-right" type="transparent p-1">
              <i slot="button" class="icon-options-vertical"></i>
              <div slot="dropdown-menu" class="dropdown-menu dropdown-menu-right">
                <router-link class="dropdown-item" :to="'/dashboard/projects/vallejo-2017/similar'">View Fullscreen</router-link>
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
      <div class="col-sm-12 col-lg-6">
        <div class="card card-accent-danger">
          <div class="card-header">
            Sentiment Analysis
            <dropdown class="float-right" type="transparent p-1">
              <i slot="button" class="icon-options-vertical"></i>
              <div slot="dropdown-menu" class="dropdown-menu dropdown-menu-right">
                <router-link class="dropdown-item" :to="{name: 'Sentiment Analysis', params: {analysisId: 1}}">View Fullscreen</router-link>
                <a class="dropdown-item" href="#">Print Chart</a>
                <li><a class="dropdown-item" href="#">Download as PNG Image</a></li>
                <li><a class="dropdown-item" href="#">Download as JPEG Image</a></li>
                <li><a class="dropdown-item" href="#">Download as SVG Image</a></li>
                <li><a class="dropdown-item" href="#">Download as PDF Document</a></li>
              </div>
            </dropdown>
          </div>
          <div class="card-block">
              <scatter-chart :analysis-id="sentimentId" />
          </div>
        </div>
      </div>
    </div>
    </div>

  </div>
</template>

<script>

import {Backend} from '../Backend'

import BarChart from './charts/BarChart'
import HorizontalBarChart from './charts/HorizontalBarChart'
import LineChart from './charts/LineChart'
import ScatterChart from './charts/ScatterChart'
import BubbleChart from './charts/BubbleChart'

import { dropdown } from 'vue-strap'
import _ from 'lodash'

export default {
  name: 'projectDashboard',
  components: {
    BarChart,
    HorizontalBarChart,
    LineChart,
    ScatterChart,
    BubbleChart,
    dropdown,
    Backend
  },
  data () {
    return {
      project: {},
      sentimentId: 0,
      clusterId: 0,
      conceptId: 0,
      categoryId: 0
    }
  },
  methods: {

  },
  beforeRouteEnter: (to, from, next) => {
    next(vm => {
      Backend.getProjectSummary(to.params.projectId).then(
        response => {
          vm.project = response.data
          let sentimentAnalysisList = _.filter(vm.project.analysis, (v, k) => v.analysis_type === 1 && v.analysis_status === 3)[0]
          let documentClusteringList = _.filter(vm.project.analysis, (v, k) => v.analysis_type === 2 && v.analysis_status === 3)[0]
          let conceptExtractionList = _.filter(vm.project.analysis, (v, k) => v.analysis_type === 3 && v.analysis_status === 3)[0]
          let documentClassificationList = _.filter(vm.project.analysis, (v, k) => v.analysis_type === 4 && v.analysis_status === 3)[0]
          vm.sentimentId = sentimentAnalysisList.id
          vm.clusterId = documentClusteringList.id
          vm.conceptId = conceptExtractionList.id
          vm.categoryId = documentClassificationList.id
        }
      ).catch(
        e => {
          console.log(e)
        }
      )
    })
  }
}
</script>
