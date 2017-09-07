<template>
  <div class="animated fadeIn" id="new-project">
    
    <div class="card">
      <div class="card-header">
        Create a New Project
      </div>
      <div class="card-body">
        <form>
          <div class="row no-gutters">
            <div class="col-md-4 col-lg-3 col-xl-2">
              <div class="list-group" id="myList" role="tablist">
                <a class="list-group-item list-group-item-action active" data-toggle="list" href="#home" role="tab">Project Name</a>
                <a class="list-group-item list-group-item-action" data-toggle="list" href="#profile" role="tab">Data Set and Format Definition</a>
              </div>
            </div>
            <div class="col-md-8 col-lg-9 col-xl-10">
              <div class="tab-content">
                <div class="tab-pane active" id="home" role="tabpanel">
                  <div class="row">
                    <div class="col-md-8">
                      <div class="form-group">
                        <label>Project Name</label>
                        <input type="text" class="form-control">
                      </div>
                      <div class="form-group">
                        <label>Project Description</label>
                        <textarea class="form-control" rows="4"></textarea>
                      </div>
                    </div>
                    <div class="col-md-4">
                      <div id="accordion" role="tablist">
                        <div class="card">
                          <div class="card-header" role="tab" id="headingOne">
                            <h5 class="mb-0">
                              <a data-toggle="collapse" href="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                                Privacy Settings
                              </a>
                            </h5>
                          </div>

                          <div id="collapseOne" class="collapse show" role="tabpanel" aria-labelledby="headingOne" data-parent="#accordion">
                            <div class="card-body">
                              Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry richardson ad squid. 3 wolf moon officia aute, non cupidatat skateboard dolor brunch. Food truck quinoa nesciunt laborum eiusmod. Brunch 3 wolf moon tempor, sunt aliqua put a bird on it squid single-origin coffee nulla assumenda shoreditch et. Nihil anim keffiyeh helvetica, craft beer labore wes anderson cred nesciunt sapiente ea proident. Ad vegan excepteur butcher vice lomo. Leggings occaecat craft beer farm-to-table, raw denim aesthetic synth nesciunt you probably haven't heard of them accusamus labore sustainable VHS.
                            </div>
                          </div>
                        </div>
                        <div class="card">
                          <div class="card-header" role="tab" id="headingTwo">
                            <h5 class="mb-0">
                              <a class="collapsed" data-toggle="collapse" href="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                                Folder Location
                              </a>
                            </h5>
                          </div>
                          <div id="collapseTwo" class="collapse" role="tabpanel" aria-labelledby="headingTwo" data-parent="#accordion">
                            <div class="card-body">
                              Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry richardson ad squid. 3 wolf moon officia aute, non cupidatat skateboard dolor brunch. Food truck quinoa nesciunt laborum eiusmod. Brunch 3 wolf moon tempor, sunt aliqua put a bird on it squid single-origin coffee nulla assumenda shoreditch et. Nihil anim keffiyeh helvetica, craft beer labore wes anderson cred nesciunt sapiente ea proident. Ad vegan excepteur butcher vice lomo. Leggings occaecat craft beer farm-to-table, raw denim aesthetic synth nesciunt you probably haven't heard of them accusamus labore sustainable VHS.
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="tab-pane" id="profile" role="tabpanel">

                </div>
              </div>
            </div>
          </div>
          <!--<tabs>
            <tab name="Project Information" :selected="true">
              <div class="row">
                <div class="col-md-8">
                  <div class="form-group">
                    <label>Project Name</label>
                    <input type="text" class="form-control">
                  </div>
                  <div class="form-group">
                    <label>Project Description</label>
                    <textarea class="form-control" rows="4"></textarea>
                  </div>
                </div>
                <div class="col-md-4">
                  <div id="accordion" role="tablist">
                    <div class="card">
                      <div class="card-header" role="tab" id="headingOne">
                        <h5 class="mb-0">
                          <a data-toggle="collapse" href="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                            Privacy Settings
                          </a>
                        </h5>
                      </div>

                      <div id="collapseOne" class="collapse show" role="tabpanel" aria-labelledby="headingOne" data-parent="#accordion">
                        <div class="card-body">
                          Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry richardson ad squid. 3 wolf moon officia aute, non cupidatat skateboard dolor brunch. Food truck quinoa nesciunt laborum eiusmod. Brunch 3 wolf moon tempor, sunt aliqua put a bird on it squid single-origin coffee nulla assumenda shoreditch et. Nihil anim keffiyeh helvetica, craft beer labore wes anderson cred nesciunt sapiente ea proident. Ad vegan excepteur butcher vice lomo. Leggings occaecat craft beer farm-to-table, raw denim aesthetic synth nesciunt you probably haven't heard of them accusamus labore sustainable VHS.
                        </div>
                      </div>
                    </div>
                    <div class="card">
                      <div class="card-header" role="tab" id="headingTwo">
                        <h5 class="mb-0">
                          <a class="collapsed" data-toggle="collapse" href="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                            Folder Location
                          </a>
                        </h5>
                      </div>
                      <div id="collapseTwo" class="collapse" role="tabpanel" aria-labelledby="headingTwo" data-parent="#accordion">
                        <div class="card-body">
                          Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry richardson ad squid. 3 wolf moon officia aute, non cupidatat skateboard dolor brunch. Food truck quinoa nesciunt laborum eiusmod. Brunch 3 wolf moon tempor, sunt aliqua put a bird on it squid single-origin coffee nulla assumenda shoreditch et. Nihil anim keffiyeh helvetica, craft beer labore wes anderson cred nesciunt sapiente ea proident. Ad vegan excepteur butcher vice lomo. Leggings occaecat craft beer farm-to-table, raw denim aesthetic synth nesciunt you probably haven't heard of them accusamus labore sustainable VHS.
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </tab>
            <tab name="Data Set and Format Definition">
              <h1>Here is the content for the about our culture tab.</h1>
            </tab>
          </tabs>-->
        </form>
      </div>
    </div>

  </div>
</template>

<script>

import tabs from '../../components/TabbedPanel/TabbedPanel'

export default {
  name: 'new-project',
  components: {
    tabs
  }
}

</script>
