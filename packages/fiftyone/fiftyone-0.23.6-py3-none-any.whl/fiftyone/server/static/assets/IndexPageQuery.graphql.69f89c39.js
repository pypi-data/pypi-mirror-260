const g=function(){var l={defaultValue:null,kind:"LocalArgument",name:"count"},n={defaultValue:null,kind:"LocalArgument",name:"cursor"},e={defaultValue:"",kind:"LocalArgument",name:"search"},s={alias:null,args:null,kind:"ScalarField",name:"colorBy",storageKey:null},r={alias:null,args:null,kind:"ScalarField",name:"colorPool",storageKey:null},a={alias:null,args:null,kind:"ScalarField",name:"colorscale",storageKey:null},i={alias:null,args:null,kind:"ScalarField",name:"multicolorKeypoints",storageKey:null},o={alias:null,args:null,kind:"ScalarField",name:"showSkeletons",storageKey:null},t={alias:null,args:null,kind:"ScalarField",name:"total",storageKey:null},u={alias:"allDatasets",args:[{kind:"Literal",name:"search",value:""}],concreteType:"DatasetStrConnection",kind:"LinkedField",name:"datasets",plural:!1,selections:[t],storageKey:'datasets(search:"")'},d=[{kind:"Variable",name:"after",variableName:"cursor"},{kind:"Variable",name:"first",variableName:"count"},{kind:"Variable",name:"search",variableName:"search"}];return{fragment:{argumentDefinitions:[l,n,e],kind:"Fragment",metadata:null,name:"IndexPageQuery",selections:[{alias:null,args:null,concreteType:"AppConfig",kind:"LinkedField",name:"config",plural:!1,selections:[s,r,a,i,o],storageKey:null},u,{args:null,kind:"FragmentSpread",name:"NavFragment"},{args:null,kind:"FragmentSpread",name:"configFragment"}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:[e,l,n],kind:"Operation",name:"IndexPageQuery",selections:[{alias:null,args:null,concreteType:"AppConfig",kind:"LinkedField",name:"config",plural:!1,selections:[s,r,a,i,o,{alias:null,args:null,kind:"ScalarField",name:"gridZoom",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"lightningThreshold",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"loopVideos",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"notebookHeight",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"plugins",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"showConfidence",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"showIndex",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"showLabel",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"showTooltip",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"sidebarMode",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"theme",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"timezone",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"useFrameNumber",storageKey:null}],storageKey:null},u,{alias:null,args:d,concreteType:"DatasetStrConnection",kind:"LinkedField",name:"datasets",plural:!1,selections:[t,{alias:null,args:null,concreteType:"DatasetStrEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"cursor",storageKey:null},{alias:null,args:null,concreteType:"Dataset",kind:"LinkedField",name:"node",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"DatasetStrPageInfo",kind:"LinkedField",name:"pageInfo",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"endCursor",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"hasNextPage",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:d,filters:["search"],handle:"connection",key:"DatasetsList_query_datasets",kind:"LinkedHandle",name:"datasets"},{alias:null,args:null,kind:"ScalarField",name:"context",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"dev",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"doNotTrack",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"uid",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"version",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"teamsSubmission",storageKey:null},a]},params:{cacheID:"48daf769c05cc9baadf930a245bcdfaa",id:null,metadata:{},name:"IndexPageQuery",operationKind:"query",text:`query IndexPageQuery(
  $search: String = ""
  $count: Int
  $cursor: String
) {
  config {
    colorBy
    colorPool
    colorscale
    multicolorKeypoints
    showSkeletons
  }
  allDatasets: datasets(search: "") {
    total
  }
  ...NavFragment
  ...configFragment
}

fragment NavDatasets on Query {
  datasets(search: $search, first: $count, after: $cursor) {
    total
    edges {
      cursor
      node {
        name
        id
        __typename
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}

fragment NavFragment on Query {
  ...NavDatasets
  ...NavGA
  teamsSubmission
}

fragment NavGA on Query {
  context
  dev
  doNotTrack
  uid
  version
}

fragment configFragment on Query {
  config {
    colorBy
    colorPool
    colorscale
    gridZoom
    lightningThreshold
    loopVideos
    multicolorKeypoints
    notebookHeight
    plugins
    showConfidence
    showIndex
    showLabel
    showSkeletons
    showTooltip
    sidebarMode
    theme
    timezone
    useFrameNumber
  }
  colorscale
}
`}}}();g.hash="d84cfaac426f2730610de9dd1814da58";export{g as default};
