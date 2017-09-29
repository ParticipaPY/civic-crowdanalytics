<template>
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
    </div>
    <div class="col-xl-3 remove-padding">
      <accordion :one-at-atime="false" type="info">
        <panel is-open type="primary">
          <strong slot="header"><u>Panel #1</u></strong>
          ...
        </panel>
        <panel header="Panel #2">
          ...
        </panel>
        <panel header="Panel #3">
          ...
        </panel>
        <panel header="Panel #4">
          ...
        </panel>
      </accordion>
      <div id="accordion" role="tablist">
        <div class="card">
          <div class="card-header" role="tab" id="headingOne">
              <a data-toggle="collapse" href="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                Privacy Settings
              </a>
          </div>

          <div id="collapseOne" class="collapse show" role="tabpanel" aria-labelledby="headingOne" data-parent="#accordion">
            <div class="card-body inner">
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
            </div>
          </div>
        </div>
        <div class="card">
          <div class="card-header" role="tab" id="headingTwo">
              <a class="collapsed" data-toggle="collapse" href="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                Folder Location
              </a>
          </div>
          <div id="collapseTwo" class="collapse show" role="tabpanel" aria-labelledby="headingTwo" data-parent="#accordion">
            <div class="card-body inner">
              
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

// import { accordion, panel } from 'vue-strap'

export default {
  name: 'projectname'
}
</script>
