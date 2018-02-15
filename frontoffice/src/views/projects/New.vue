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
                      <input type="checkbox" id="analysis_category" name="analysis_category" v-model="analysis.include" value="classification">
                      <label for="analysis_category"></label>
                      Classification
                    </div>
                    <div>
                      <label>
                        Language:
                        <input class="long" type="text" v-model="analysis.classification.language">
                        <span>Language on which documents are written. Only English and Spanish are supported natively. If you use another language, the module will first translate each document to english (using Google Translate AJAX API)</span>
                      </label>
                      <label>
                        Number of folds for cross validation:
                        <input type="number" min="1" v-model.number="analysis.classification.n_folds">
                        <span>Number of folds to be used in k-fold cross validation technique for choosing different sets as 'train docs'.</span>
                      </label>
                      <label>
                        Vocabulary size:
                        <input type="number" min="1" v-model.number="analysis.classification.vocab_size">
                        <span>The size of the vocabulary set that will be used for extracting features out of the docs.</span>
                      </label>
                      <label>
                        Type of Classifier:
                        <select v-model="analysis.classification.t_classifier">
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
                      <input type="checkbox" id="analysis_sentiment" name="analysis_sentiment" v-model="analysis.include" value="sentiment">
                      <label for="analysis_sentiment"></label>
                      Sentiment Analysis
                    </div>
                    <div>
                      <label>
                        Language:
                        <input class="long" type="text" v-model="analysis.sentiment.language">
                        <span>Language on which documents are written. Only English and Spanish are supported natively. If you use another language, the module will first translate each document to english (using Google Translate AJAX API)</span>
                      </label>
                      <label>
                        Inferior limit for neural interval:
                        <input type="number" min="-1.00" max="0.00" step="0.01" v-model.number="analysis.sentiment.neu_inf_lim">
                        <span>If a doc's polarity score is lower than this paramenter, then the sentiment is considered negative.</span>
                      </label>
                      <label>
                        Superior limit for neural interval:
                        <input type="number" min="0.00" max="1.00" step="0.01" v-model.number="analysis.sentiment.neu_sup_lim">
                        <span>If a doc's polarity score is greater than this parameter, then the seniment is considered positive.</span>
                      </label>
                    </div>
                  </div>
                </div>
                <!-- CONCEPT -->
                <div class="col-md-6 analysis-block">
                  <div class="wrapper">
                    <div class="title">
                      <input type="checkbox" id="analysis_concept" name="analysis_concept" v-model="analysis.include" value="concept">
                      <label for="analysis_concept"></label>
                      Concept Ocurrences
                    </div>
                    <div>
                      <label>
                        Language:
                        <input class="long" type="text" v-model="analysis.concept.language">
                        <span>Language on which documents are written. Only English and Spanish are supported natively. If you use another language, the module will first translate each document to english (using Google Translate AJAX API)</span>
                      </label>
                      <label>
                        Number of concepts to extract:
                        <input type="number" min="1" v-model.number="analysis.concept.num_concepts">
                        <span>The number of concepts to extract.</span>
                      </label>
                      <label>
                        Context words that should not be considered:
                        <textarea row="4" v-model="analysis.concept.context_words"></textarea>
                        <span>List of context-specific words that should notbe considered in the analysis (comma separated)</span>
                      </label>
                      <label>
                        N-gram Range
                        <div class="sublabel">
                          Min: <input type="number" v-model.number="analysis.concept.ngram_range[0]">
                          Max: <input type="number" v-model.number="analysis.concept.ngram_range[1]">
                        </div>
                        <span>The lower and upper boundary of the range of n-values for different n-grams to be extracted.</span>
                      </label>
                      <label>
                        Part of Speech Tags:
                        <textarea row="4" v-model="analysis.concept.pos_vec"></textarea>
                        <span>List of tags related with the part-of-speech that should be considered in the analysis. Please check <a href="http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html" target="_blank">http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html</a> for a complete list of tags.</span>
                      </label>
                      <label>
                        <input type="checkbox" v-model="analysis.concept.consider_urls"> Consider Urls
                        <span>Whether URLs should be removed or not.</span>
                      </label>
                    </div>
                  </div>
                </div>
                <!-- CLUSTER -->
                <div class="col-md-6 analysis-block">
                  <div class="wrapper">
                    <div class="title">
                      <input type="checkbox" id="analysis_cluster" name="analysis_cluster" v-model="analysis.include" value="clustering">
                      <label for="analysis_cluster"></label>
                      Clustering
                    </div>
                    <div>
                      <label>
                        Language:
                        <input class="long" type="text" v-model="analysis.clustering.language">
                        <span>Language on which documents are written. Only English and Spanish are supported natively. If you use another language, the module will first translate each document to english (using Google Translate AJAX API)</span>
                      </label>
                      <label>
                        Number of clusters:
                        <input type="number" min="1" v-model.number="analysis.clustering.num_clusters">
                        <span>The number of clusters in which the documents will be grouped.</span>
                      </label>
                      <label>
                        Context Words that should not be considered:
                        <textarea row="4" v-model="analysis.clustering.context_words"></textarea>
                        <span>List of context-specific words that should notbe considered in the analysis (comma separated)</span>
                      </label>
                      <label>
                        N-gram Range
                        <div class="sublabel">
                          Min: <input type="number" v-model.number="analysis.clustering.ngram_range[0]">
                          Max: <input type="number" v-model="analysis.clustering.ngram_range[1]">
                        </div>
                        <span>The lower and upper boundary of the range of n-values for different n-grams to be extracted.</span>
                      </label>
                      <label>
                        Minimum document frequency:
                        <input type="number" min="0.00" max="1.00" step="0.01" v-model.number="analysis.clustering.min_df">
                        <span>The minimum number of documents that any term is contained in. It can either be an integer which sets the number specifically, or a decimal between 0 and 1 which is interpreted as a percentage of all documents.</span>
                      </label>
                      <label>
                        Maximun document frequency:
                        <input type="number" min="0.00" max="1.00" step="0.01" v-model.number="analysis.clustering.max_df">
                        <span>The maximum number of documents that any term is contained in. It can either be an integer which sets the number specifically, or a decimal between 0 and 1 which is interpreted as a percentage of all documents.</span>
                      </label>
                      <label>
                        Algorithm:
                        <select v-model="analysis.clustering.algorithm">
                          <option value="k-means">K-means</option>
                          <option value="agglomerative">Agglomerative</option>
                        </select>
                        <span>Clustering algorithm use to group documents.</span>
                      </label>
                      <label>
                        <input type="checkbox" v-model="analysis.clustering.consider_urls"> Consider Urls
                        <span>Whether URLs should be removed or not.</span>
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
      analysis: {
        include: [],
        sentiment: {
          neu_inf_lim: -0.3,
          neu_sup_lim: 0.3,
          language: 'english'
        },
        classification: {
          n_folds: 10,
          vocab_size: 500,
          t_classifier: 'NB',
          language: 'english'
        },
        concept: {
          num_concepts: 5,
          context_words: [],
          ngram_range: [1, 1],
          pos_vec: ['NN', 'NNP'],
          consider_urls: false,
          language: 'english'
        },
        clustering: {
          num_clusters: 5,
          context_words: [],
          ngram_range: [1, 1],
          min_df: 0.1,
          max_df: 0.9,
          consider_urls: false,
          language: 'english',
          algorithm: 'k-means'
        }
      },
      showAlert: false
    }
  },

  methods: {
    nextPage: function () {
      if (this.$refs.wiz.currentTab() === 2) {
        this.generateAttributes()
      } else {
        if (this.$refs.wiz.currentTab() === 1 && this.dataset.file === null) {
          this.$snotify.error('You need to add a dataset file.')
        } else {
          this.$refs.wiz.index += 1
          this.$refs.wiz.selectIndex(this.$refs.wiz.index)
        }
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
    formatAnalysisConfig: function () {
      // Stringify arrays for Concept and Clustering
      if (this.analysis.concept.context_words === 'string') {
        this.analysis.concept.context_words = this.analysis.concept.context_words.split(',').map(s => s.trim())
      }
      if (typeof this.analysis.concept.pos_vec === 'string') {
        this.analysis.concept.pos_vec = this.analysis.concept.pos_vec.split(',').map(s => s.trim())
      }
      if (this.analysis.clustering.context_words === 'string') {
        this.analysis.clustering.context_words = this.analysis.concept.context_words.split(',').map(s => s.trim())
      }
      // Convert JavaScript booleans to integers
      this.analysis.concept.consider_urls = this.analysis.concept.consider_urls ? 1 : 0
      this.analysis.clustering.consider_urls = this.analysis.clustering.consider_urls ? 1 : 0
    },
    createProject: function () {
      if (this.analysis.include.length > 0) {
        var toor = this
        Backend.postDataset(this.dataset, this.attributes).then(
          response => {
            let datasetId = response.data.id
            Backend.postProject(this.project, datasetId).then(
              response => {
                let projectName = response.data.name
                let projectId = response.data.id
                let analysisArray = []
                toor.formatAnalysisConfig()
                // Add configs to axios queue
                if (toor.analysis.include.indexOf('sentiment') > -1) analysisArray.push(Backend.postSentimentAnalysis(projectName, projectId, datasetId, toor.analysis.sentiment))
                if (toor.analysis.include.indexOf('concept') > -1) analysisArray.push(Backend.postConceptExtraction(projectName, projectId, datasetId, toor.analysis.concept))
                if (toor.analysis.include.indexOf('classification') > -1) analysisArray.push(Backend.postDocumentClassification(projectName, projectId, datasetId, toor.analysis.classification))
                if (toor.analysis.include.indexOf('clustering') > -1) analysisArray.push(Backend.postDocumentClustering(projectName, projectId, datasetId, toor.analysis.clustering))
                axios.all(analysisArray).then(axios.spread(
                  results => {
                    toor.$snotify.success('Project created successfully. You\'ll see your data soon.')
                    this.$router.push({ name: 'Project Home', params: { projectId: projectId } })
                  }
                )).catch(
                  e => toor.$snotify.error('Error creating project')
                )
              }
            ).catch(
              e => toor.$snotify.error('Error creating project')
            )
          }
        ).catch(
          e => toor.$snotify.error('Error creating project')
        )
      } else {
        this.$snotify.error('Error creating project. Please select at least one analysis.')
      }
    }
  }
}

</script>
