<script>

  import axios from 'axios'

  export const Backend = axios.create({
    baseURL: 'http://159.203.77.35:8080/api',
    headers: {
      Accept: 'application/json'
    }
  })

  Backend.token = null

  Backend.auth = function () {
    if (this.token === null) {
      this.post('/auth/', {
        username: 'admin',
        password: '238k74i1Ct'
      }).then(
        response => {
          Backend.token = response.data.token
          Backend.defaults.headers.common['Authorization'] = 'JWT ' + response.data.token
        }
      ).catch(
        e => console.log(e)
      )
    }
  }

  Backend.interceptors.request.use(Backend.auth())
  
  Backend.projects = function () {
    return this.get('projects/')
  }

  Backend.getProjectSummary = function (projectId) {
    return this.get('/projects/' + projectId)
  }

  Backend.postDataset = function (dataset, attributes) {
    let datasetFd = new FormData()
    let attributesFd = []
    for (let attr of attributes) {
      let item = {}
      item.name = attr.name
      item.attribute_type = attr.attribute_type
      item.included_in_analysis = attr.included_in_analysis
      attributesFd.push(item)
    }
    datasetFd.append('name', dataset.name)
    datasetFd.append('file', dataset.file, dataset.file.fileName)
    datasetFd.append('attributes', JSON.stringify(attributesFd))
    return this.post('datasets/', datasetFd)
  }
  Backend.postProject = function (project, datasetId) {
    let projectFd = new FormData()
    let datasets = [datasetId]
    projectFd.append('name', project.name)
    projectFd.append('description', project.description)
    projectFd.append('datasets', JSON.stringify(datasets))
    projectFd.append('visibility', project.visibility)
    projectFd.append('people_editing', project.people_editing)
    return this.post('projects/', projectFd)
  }
  Backend.postSentimentAnalysis = function (projectName, projectId, datasetId) {
    let sentimentAnalysisFd = new FormData()
    let argumentsFd = {'neu_inf_lim': -0.2, 'neu_sup_lim': 0.2}
    sentimentAnalysisFd.append('name', projectName + ' - Sentiment Analysis')
    sentimentAnalysisFd.append('project_id', projectId)
    sentimentAnalysisFd.append('dataset_id', datasetId)
    sentimentAnalysisFd.append('arguments', JSON.stringify(argumentsFd))
    /*
    return this.post('analysis/sentiment-analysis/', {
      name: projectName + ' - Sentiment Analysis',
      project: projectId,
      dataset: datasetId,
      arguments: {'neu_inf_lim': -0.2, 'neu_sup_lim': 0.2}
    })
    */
    return this.post('analysis/sentiment-analysis/', sentimentAnalysisFd)
  }
  Backend.postDocumentClassification = function (projectName, projectId, datasetId) {
    let docClassificationFd = new FormData()
    let argumentsFd = {}
    docClassificationFd.append('name', projectName + ' - Classification')
    docClassificationFd.append('project_id', projectId)
    docClassificationFd.append('dataset_id', datasetId)
    docClassificationFd.append('arguments', JSON.stringify(argumentsFd))
    /*
    return this.post('analysis/doc-classification/', {
      name: projectName + ' - Classification',
      project: projectId,
      dataset: datasetId,
      arguments: {}
    })
    */
    return this.post('analysis/doc-classification/', docClassificationFd)
  }
  Backend.postDocumentClustering = function (projectName, projectId, datasetId) {
    let docClusteringFd = new FormData()
    let argumentsFd = {}
    docClusteringFd.append('name', projectName + ' - Clustering')
    docClusteringFd.append('project_id', projectId)
    docClusteringFd.append('dataset_id', datasetId)
    docClusteringFd.append('arguments', JSON.stringify(argumentsFd))
    /*
    return this.post('analysis/doc-clustering/', {
      name: projectName + ' - Clustering',
      project: projectId,
      dataset: datasetId,
      arguments: {}
    })
    */
    return this.post('analysis/doc-clustering/', docClusteringFd)
  }
  Backend.postConceptExtraction = function (projectName, projectId, datasetId) {
    let conceptExtractionFd = new FormData()
    let argumentsFd = {}
    conceptExtractionFd.append('name', projectName + ' - Concept Extraction')
    conceptExtractionFd.append('project_id', projectId)
    conceptExtractionFd.append('dataset_id', datasetId)
    conceptExtractionFd.append('arguments', JSON.stringify(argumentsFd))
    /*
    return this.post('analysis/concept-extraction/', {
      name: projectName + ' - Concept Extraction',
      project: projectId,
      dataset: datasetId,
      arguments: {}
    })
    */
    return this.post('analysis/concept-extraction/', conceptExtractionFd)
  }

  Backend.getSentimentAnalysis = function (id) {
    return this.get('/analysis/sentiment-analysis/' + id)
  }
  Backend.getConceptExtraction = function (id) {
    return this.get('/analysis/concept-extraction/' + id)
  }
  Backend.getDocumentClassification = function (id) {
    return this.get('/analysis/doc-classification/' + id)
  }
  Backend.getDocumentClustering = function (id) {
    return this.get('/analysis/doc-clustering/' + id)
  }

</script>
