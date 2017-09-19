<template>
  <div class="animated fadeIn" id="new-project">
    
    <div class="card">
      <div class="card-header">
        Create a New Project
      </div>
      <div class="card-body">
        <form>
          <tabbed-panel v-model="activeTab">
            <tabbed-panel-tab header="Project Name">
              <div class="row">
                <div class="col-xl-9">
                  <div class="form-group">
                    <label>Project Name</label>
                    <input type="text" class="form-control">
                  </div>
                  <div class="form-group">
                    <label>Project Description</label>
                    <textarea class="form-control" rows="4"></textarea>
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
                        <select class="form-control form-control-sm">
                          <option>Public</option>
                          <option>Private</option>
                          <option>Team</option>
                        </select>
                        <div class="form-check">
                          <label class="form-check-label">
                            <input class="form-check-input" type="checkbox" value="">
                            Allow people to edit
                          </label>
                        </div>
                      </div>
                    </panel>
                    <panel is-open header="Folder Location">
                      <button-group id="folders" v-model="selectedFolder" type="primary">
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
                      </ul>
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
                    <input type="text" class="form-control">
                  </div>
                  <div class="form-group">
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
                                    <input type="radio" :name="column + '_columnType'" value="string" checked> String<br>
                                    <input type="radio" :name="column + '_columnType'" value="number"> Number<br>
                                    <input type="radio" :name="column + '_columnType'" value="datetime"> Date & Time
                                  </div>
                                  <div class="col-md-9 data-value">
                                    <p><strong>Column Data Value</strong></p>
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
          </tabbed-panel>
        </form>
      </div>
      <div class="card-footer">
        <button class="btn btn-default btn-primary float-left">Previous</button>
        <button class="btn btn-default btn-primary float-right">Next</button>
        <button class="btn btn-default btn-success float-right">Save as Draft</button>
      </div>
    </div>

  </div>
</template>

<script>

import tabbedPanel from '../../components/TabbedPanel/TabbedPanel'
import tabbedPanelTab from '../../components/TabbedPanel/Tab'

import { accordion, panel, radio, buttonGroup } from 'vue-strap'

export default {
  name: 'new-project',
  components: {
    tabbedPanel,
    tabbedPanelTab,
    accordion,
    panel,
    radio,
    buttonGroup
  },

  data () {
    return {
      columns: [],
      parsedDataset: []
    }
  },

  methods: {
    onFileAdd: function (e) {
      var file = e.target.files || e.dataTransfer.files
      if (!file.length) return
      this.readFile(file[0])
    },
    readFile: function (f) {
      var cols = this.columns
      var dataset = this.parsedDataset
      var reader = new FileReader()
      reader.onload = function (e) {
        var parsed = JSON.parse(e.target.result)
        var keys = Object.keys(parsed[0])
        var k = null
        for (k in keys) {
          cols.push(keys[k])
        }
        for (k in parsed) {
          dataset.push(parsed[k])
        }
      }
      reader.readAsText(f)
    }
  }
}

</script>
