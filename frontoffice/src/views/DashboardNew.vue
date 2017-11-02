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
export default {
  name: 'dashboardnew'
}
</script>
