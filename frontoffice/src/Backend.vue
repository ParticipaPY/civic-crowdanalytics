<script>

  import axios from 'axios'

  export const Backend = axios.create({
    baseURL: 'http://159.203.77.35:8080/api',
    headers: {
      Authorization: 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MTI2NjU3MDIsImVtYWlsIjoiIiwidXNlcl9pZCI6MSwidXNlcm5hbWUiOiJhZG1pbiJ9.TbEVtAvx2zkFOq6QFrN6yJFVdQeG4sdnnm578e8wo7c',
      Accept: 'application/json'
    }
  })
  
  Backend.projects = function () {
    return this.get('projects/')
  }

  Backend.postProject = function (project, dataset, attributes) {
    var server = this
    let datasetFd = new FormData()
    datasetFd.append('name', dataset.name)
    datasetFd.append('file', dataset.file, dataset.file.fileName)
    server.post('datasets/', datasetFd, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }).then(
      response => {
        var datasetId = response.data.id
        for (let attr of attributes) {
          server.post('attributes/', {
            name: attr.name,
            attribute_type: attr.type,
            included_in_analysis: attr.include,
            dataset: datasetId
          })
        }
        server.post('projects/', {
          name: project.name,
          description: project.description,
          dataset: [datasetId],
          visibility: project.visibility,
          people_editing: project.people_editing
        }).then(
          response => {
            // MANUAL ANALYSIS FOR NOW
            server.post('analysis/sentiment-analysis/', {
              name: project.name + ' - Sentiment Analysis',
              project: response.data.id,
              dataset: datasetId,
              arguments: {'neu_inf_lim': -0.2, 'neu_sup_lim': 0.2}
            }).then(
              response => { console.log(response) }
            ).catch(e => console.error(e))
            server.post('analysis/doc-classification/', {
              name: project.name + ' - Classification',
              project: response.data.id,
              dataset: datasetId,
              arguments: {}
            }).then(
              response => { console.log(response) }
            ).catch(e => console.error(e))
            server.post('analysis/doc-clustering/', {
              name: project.name + ' - Clustering',
              project: response.data.id,
              dataset: datasetId,
              arguments: {}
            }).then(
              response => { console.log(response) }
            ).catch(e => console.error(e))
            server.post('analysis/concept-extraction/', {
              name: project.name + ' - Concept Extraction',
              project: response.data.id,
              dataset: datasetId,
              arguments: {}
            }).then(
              response => { console.log(response) }
            ).catch(e => console.error(e))
            return true
          }
        ).catch(
          e => {
            console.error(e)
          }
        )
      }
    ).catch(
      e => {
        console.error(e)
      }
    )
  }

</script>
