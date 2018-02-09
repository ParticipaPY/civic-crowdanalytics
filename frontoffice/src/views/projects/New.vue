<template>
  <div class="animated fadeIn" id="new-project">
    <div class="card">
      <div class="card-header">
        Create a New Project
      </div>
      <div class="card-body">
        <form>
          <tabbed-panel v-model="wizActiveTab" :tab-click="false" ref="wiz">
            <tabbed-panel-tab header="Project Name">
              <div class="row">
                <div class="col-xl-9">
                  <div class="form-group">
                    <label>Project Name</label>
                    <input type="text" class="form-control" v-model="project.name">
                  </div>
                  <div class="form-group">
                    <label>Project Description</label>
                    <textarea class="form-control" rows="4" v-model="project.description"></textarea>
                  </div>
                  <div class="form-group">
                    <label>Project Owner</label><br>
                    <button type="button" class="btn btn-primary btn-sm btn-avatar"><img src="http://via.placeholder.com/100x100" class="avatar-tiny">Jessica Williams (Me)</button><br>
                    <small>Work with a team? <a href="#">Invite people to join your project</a>.</small>
                  </div>
                  <div class="form-group">
                    <label>Start Date</label><br>
                    <button type="button" class="btn btn-sm btn-cal"><i class="fa fa-calendar"></i>Today</button><br>
                    <small>Want to set a future date for the project? <a href="#">Click here to enable date-picker</a>.</small>
                  </div>
                </div>
                <div class="col-xl-3 remove-padding">
                  <accordion id="settings" :one-at-atime="false">
                    <panel is-open header="Privacy Settings">
                      <div class="form-group">
                        <label>Project visibility</label>
                        <select class="form-control form-control-sm" v-model="project.visibility">
                          <option value="1">Public</option>
                          <option value="2">Private</option>
                          <option value="3">Team</option>
                        </select>
                        <div class="form-check">
                          <label class="form-check-label">
                            <input class="form-check-input" type="checkbox" v-model="project.people_editing" value="1">
                            Allow people to edit
                          </label>
                        </div>
                      </div>
                    </panel>
                    <panel is-open header="Folder Location">
                      <button-group id="folders" v-model="project.location" type="primary">
                        <radio selected-value="1"><i class="fa fa-folder fa-lg"></i>Project Lorem</radio>
                        <radio selected-value="2"><i class="fa fa-folder fa-lg"></i>Project Ipsum</radio>
                        <radio selected-value="3"><i class="fa fa-folder fa-lg"></i>Project Dolor</radio>
                        <radio selected-value="4"><i class="fa fa-folder fa-lg"></i>Project Sit Amet</radio>
                        <radio selected-value="5"><i class="fa fa-folder fa-lg"></i>Project Consectetur</radio>
                        <radio selected-value="6"><i class="fa fa-folder fa-lg"></i>Project Insipidus</radio>
                        <radio selected-value="7"><i class="fa fa-folder fa-lg"></i>Project Neglementur</radio>
                        <radio selected-value="8"><i class="fa fa-folder fa-lg"></i>Project Setentiae</radio>
                      </button-group>
                      <button class="btn btn-new-folder"><i class="fa fa-plus-square fa-lg"></i>Add New Folder</button>
                    </panel>
                  </accordion>
                </div>
              </div>
            </tabbed-panel-tab>
            <tabbed-panel-tab header="Data Set and Format Definition">
              <div class="row">
                <div class="col-xl-9">
                  <div class="form-group">
                    <label>Data Set Name</label>
                    <input type="text" class="form-control" v-model="dataset.name">
                  </div>
                  <div class="form-group" v-if="columns.length==0">
                    <label>Select Data Set File</label>
                    <input type="file" @change="onFileAdd">
                    <small>Want to add training data set? <a href="#">Click here to add</a>.</small>
                  </div>
                </div>
              </div>
              <div class="row" v-if="columns.length>0">
                <div class="col-xl-10 offset-xl-1 dataset-preview">
                  <div class="row dataset-preview-header">
                    <div class="col-md-2">
                      Columns
                    </div>
                    <div class="col-md-10">
                      Column Settings and Details
                    </div>
                  </div>
                  <div class="row dataset-preview-content">
                    <div class="col-xl-12" style="padding:0">
                      <tabbed-panel v-model="activeColumn">
                        <template v-for="column in columns">
                          <tabbed-panel-tab :header="column">
                            <div class="row">
                              <div class="col-xl-12">
                                <div class="row">
                                  <div class="col-md-3">
                                    <p><strong>Type</strong></p>
                                    <input type="radio" :id="column + '_columnType'" :name="column + '_columnType'" value="1" checked> String<br>
                                    <input type="radio" :id="column + '_columnType'" :name="column + '_columnType'" value="2"> Number<br>
                                    <input type="radio" :id="column + '_columnType'" :name="column + '_columnType'" value="3"> Date & Time<br>
                                    <br>
                                    <input type="checkbox" :id="column + '_include'" :name="column + '_include'" value="include"> Include in analysis
                                  </div>
                                  <div class="col-md-9 data-value">
                                    <p><strong>Column Data Value</strong></p>
                                    <div>
                                      
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </tabbed-panel-tab>
                        </template>
                      </tabbed-panel>
                    </div>
                  </div>
                </div>
              </div>
            </tabbed-panel-tab>
            <tabbed-panel-tab header="Analysis Configuration">
              <div class="row analysis-config">
                <!-- CATEGORY -->
                <div class="col-md-6 analysis-block">
                  <div class="wrapper">
                    <div class="title">
                      <input type="checkbox" id="analysis_category" name="analysis_category">
                      <label for="analysis_category"></label>
                      Classification
                    </div>
                    <div>
                      <label>
                        Language:
                        <input class="long" type="text" value="English">
                        <span>Language on which documents are written. Only English and Spanish are supported natively. If you use another language, the module will first translate each document to english (using Google Translate AJAX API)</span>
                      </label>
                      <label>
                        Number of folds for cross validation:
                        <input type="number" min="1" value="10">
                        <span>Number of folds to be used in k-fold cross validation technique for choosing different sets as 'train docs'.</span>
                      </label>
                      <label>
                        Vocabulary size:
                        <input type="number" min="1" value="500">
                        <span>The size of the vocabulary set that will be used for extracting features out of the docs.</span>
                      </label>
                      <label>
                        Type of Classifier:
                        <select>
                          <option value="NB">Naive Bayes</option>
                          <option value="DT">Decision Tree</option>
                          <option value="RF">Random Forest</option>
                          <option value="SVM">Support Vector Machine</option>
                        </select>
                        <span>The type of classifier model used.</span>
                      </label>
                    </div>
                  </div>
                </div>
                <!-- SENTIMENT -->
                <div class="col-md-6 analysis-block">
                  <div class="wrapper">
                    <div class="title">
                      <input type="checkbox" id="analysis_sentiment" name="analysis_sentiment">
                      <label for="analysis_sentiment"></label>
                      Sentiment Analysis
                    </div>
                    <div>
                      <label>
                        Language:
                        <input class="long" type="text" value="English">
                        <span>Language on which documents are written. Only English and Spanish are supported natively. If you use another language, the module will first translate each document to english (using Google Translate AJAX API)</span>
                      </label>
                      <label>
                        Inferior limit for neural interval:
                        <input type="number" min="-1.00" max="0.00" step="0.01" value="-0.30">
                        <span>If a doc's polarity score is lower than this paramenter, then the sentiment is considered negative.</span>
                      </label>
                      <label>
                        Superior limit for neural interval:
                        <input type="number" min="0.00" max="1.00" step="0.01" value="0.30">
                        <span>If a doc's polarity score is greater than this parameter, then the seniment is considered positive.</span>
                      </label>
                    </div>
                  </div>
                </div>
                <!-- CONCEPT -->
                <div class="col-md-6 analysis-block">
                  <div class="wrapper">
                    <div class="title">
                      <input type="checkbox" id="analysis_concept" name="analysis_concept">
                      <label for="analysis_concept"></label>
                      Concept Ocurrences
                    </div>
                    <div>
                      <label>
                        Language:
                        <input class="long" type="text" value="English">
                        <span>Language on which documents are written. Only English and Spanish are supported natively. If you use another language, the module will first translate each document to english (using Google Translate AJAX API)</span>
                      </label>
                      <label>
                        Number of concepts to extract:
                        <input type="number" min="1" value="5">
                        <span>The number of concepts to extract.</span>
                      </label>
                      <label>
                        Context words that should not be considered:
                        <textarea row="4"></textarea>
                        <span>List of context-specific words that should notbe considered in the analysis (comma separated)</span>
                      </label>
                      <label>
                        N-gram Range
                        <div class="sublabel">
                          Min: <input type="number" value="1">
                          Max: <input type="number" value="1">
                        </div>
                        <span>The lower and upper boundary of the range of n-values for different n-grams to be extracted.</span>
                      </label>
                      <label>
                        Part of Speech Tags:
                        <textarea row="4"></textarea>
                        <span>List of tags related with the part-of-speech that should be considered in the analysis. Please check <a href="http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html" target="_blank">http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html</a> for a complete list of tags.</span>
                      </label>
                      <label>
                        <input type="checkbox"> Consider Urls
                        <span>Whether URLs should be removed or not.</span>
                      </label>
                    </div>
                  </div>
                </div>
                <!-- CLUSTER -->
                <div class="col-md-6 analysis-block">
                  <div class="wrapper">
                    <div class="title">
                      <input type="checkbox" id="analysis_cluster" name="analysis_cluster">
                      <label for="analysis_cluster"></label>
                      Clustering
                    </div>
                    <div>
                      <label>
                        Language:
                        <input class="long" type="text" value="English">
                        <span>Language on which documents are written. Only English and Spanish are supported natively. If you use another language, the module will first translate each document to english (using Google Translate AJAX API)</span>
                      </label>
                      <label>
                        Number of clusters:
                        <input type="number" min="1" value="5">
                        <span>The number of clusters in which the documents will be grouped.</span>
                      </label>
                      <label>
                        Context Words that should not be considered:
                        <textarea row="4"></textarea>
                        <span>List of context-specific words that should notbe considered in the analysis (comma separated)</span>
                      </label>
                      <label>
                        N-gram Range
                        <div class="sublabel">
                          Min: <input type="number" value="1">
                          Max: <input type="number" value="1">
                        </div>
                        <span>The lower and upper boundary of the range of n-values for different n-grams to be extracted.</span>
                      </label>
                      <label>
                        Minimum document frequency:
                        <input type="number" min="0.00" max="1.00" step="0.01" value="0.1">
                        <span>The minimum number of documents that any term is contained in. It can either be an integer which sets the number specifically, or a decimal between 0 and 1 which is interpreted as a percentage of all documents.</span>
                      </label>
                      <label>
                        Maximun document frequency:
                        <input type="number" min="0.00" max="1.00" step="0.01" value="0.9">
                        <span>The maximum number of documents that any term is contained in. It can either be an integer which sets the number specifically, or a decimal between 0 and 1 which is interpreted as a percentage of all documents.</span>
                      </label>
                      <label>
                        Algorythm:
                        <select>
                          <option value="k-means">K-means</option>
                          <option value="agglomerative">Agglomerative</option>
                        </select>
                        <span>Clustering algorithm use to group documents.</span>
                      </label>
                      <label>
                        <input type="checkbox"> Consider Urls
                        <span>Whether URLs should be removed or not.</span>
                      </label>
                      <label>
                        <input type="checkbox"> Use inverse document frequency
                        <span>If true, it will use TF-IDF vectorization for feature extraction. If false it will use only TF.</span>
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </tabbed-panel-tab>
          </tabbed-panel>
        </form>
      </div>
      <div class="card-footer">
        <button class="btn btn-default btn-primary float-left" v-on:click="prevPage()">Previous</button>
        <button class="btn btn-default btn-primary float-right" v-on:click="nextPage()">Next</button>
        <button class="btn btn-default btn-success float-right">Save as Draft</button>
      </div>
    </div>

  </div>
</template>

<script>
import {Backend} from '../../Backend'

import tabbedPanel from '../../components/TabbedPanel/TabbedPanel'
import tabbedPanelTab from '../../components/TabbedPanel/Tab'

import { accordion, panel, radio, buttonGroup } from 'vue-strap'
import Papa from 'papaparse'
import axios from 'axios'
// import LineNavigator from 'line-navigator'

export default {
  name: 'new-project',
  components: {
    tabbedPanel,
    tabbedPanelTab,
    accordion,
    panel,
    radio,
    buttonGroup,
    alert
  },
  computed: {
    project_visibility () {
      return this.project.visibility
    }
  },
  watch: {
    project_visibility (val) {
      this.project.visibility = parseInt(val)
    }
  },
  data () {
    return {
      columns: [],
      attributes: [],
      parsedDataset: [],
      wizActiveTab: 0,
      project: {
        name: '',
        description: '',
        location: '',
        visibility: 1,
        people_editing: false
      },
      dataset: {
        name: '',
        file: null
      },
      showAlert: false
    }
  },

  methods: {
    nextPage: function () {
      if (this.$refs.wiz.currentTab() === 2) {
        this.generateAttributes()
      } else {
        this.$refs.wiz.index += 1
        this.$refs.wiz.selectIndex(this.$refs.wiz.index)
      }
    },
    prevPage: function () {
      if (this.$refs.wiz.index > 0) {
        this.$refs.wiz.index -= 1
        this.$refs.wiz.selectIndex(this.$refs.wiz.index)
      }
    },
    onFileAdd: function (e) {
      var file = e.target.files || e.dataTransfer.files
      if (!file.length) return
      this.columns = []
      this.readFile(file[0])
      this.assignFile(file[0])
    },
    readFile: function (f) {
      // let parent = this
      // var navigator = new LineNavigator(f)
      console.log(Math.round(f.size / 1024))
      var reader = new FileReader()
      reader.onload = (e) => {
        var type = this.checkType(f)
        switch (type) {
          case 'csv':
            this.parseCsv(e.target.result)
            break
          default:
            console.error('Unknown format')
        }
      }
      reader.readAsText(f)
      /*
      navigator.readSomeLines(0, function handler (err, index, lines, isEof, progress) {
        if (err) throw err
        for (var i = 0; i < lines.length; i++) {
          var line = lines[i]
          console.log(line)
        }
      })
      */
    },
    assignFile: function (f) {
      var reader = new FileReader()
      reader.readAsDataURL(f)
      this.dataset.file = f
    },
    parseJson: function (json) {
      var parsed = JSON.parse(json)
      var keys = Object.keys(parsed[0])
      for (let k of keys) {
        this.columns.push(k)
      }
      this.parsedDataset = parsed.slice(0)
    },
    parseCsv: function (csv) {
      this.columns = Papa.parse(csv, {preview: 1}).data[0]
      this.parsedDataset = Papa.parse(csv, {header: true}).data
    },
    checkType: function (f) {
      switch (f.type) {
        case 'text/tab-separated-values':
        case 'application/vnd.ms-excel':
        case 'text/csv':
        case 'application/csv':
          return 'csv'
        default:
          var name = f.name
          var ext = name.split('.')[1]
          return ext
      }
    },
    generateAttributes: function () {
      this.attributes = []
      var cols = this.columns
      for (let k of cols) {
        var name = k + '_columnType'
        var els = document.getElementsByName(name)
        var datatype = null
        for (let e of els) {
          if (e.checked) {
            datatype = e.value
          }
        }
        var meta = {}
        meta.name = k
        meta.attribute_type = parseInt(datatype)
        meta.included_in_analysis = document.getElementById(k + '_include').checked || false
        this.attributes.push(meta)
      }
      this.createProject()
    },
    createProject: function () {
      var toor = this
      Backend.postDataset(this.dataset, this.attributes).then(
        response => {
          let datasetId = response.data.id
          Backend.postProject(this.project, datasetId).then(
            response => {
              let projectName = response.data.name
              let projectId = response.data.id
              axios.all([Backend.postSentimentAnalysis(projectName, projectId, datasetId), Backend.postDocumentClassification(projectName, projectId, datasetId), Backend.postDocumentClustering(projectName, projectId, datasetId), Backend.postConceptExtraction(projectName, projectId, datasetId)]).then(axios.spread(
                results => {
                  this.$router.push({ name: 'Project Home', params: { projectId: projectId } })
                  toor.showAlert = true
                }
              )).catch(
                e => console.log(e)
              )
            }
          ).catch(
            e => console.log(e)
          )
        }
      ).catch(
        e => console.log(e)
      )
      // this.showAlert = Backend.postProject(this.project, this.dataset, this.attributes)
    }
  }
}

</script>
