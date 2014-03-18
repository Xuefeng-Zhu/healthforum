var app = angular.module('mgcrea.ngStrapDocs', ['ngAnimate', 'ngSanitize', 'mgcrea.ngStrap']);

app.controller('MainCtrl', function($scope) {
});

'use strict';

angular.module('mgcrea.ngStrapDocs')

.controller('SelectDemoCtrl', function($scope, $http) {

  $scope.selectedIcon = '';
  $scope.selectedIcons = ['Globe', 'Heart'];
  $scope.icons = [
    {value: 'Relevance', label: '<i class="fa fa-plus"></i> Relevance'},
    {value: 'Letter', label: '<i class="fa fa-sort-alpha-asc"></i> Letter'},
    {value: 'Most Review', label: '<i class="fa fa-comment"></i> Most Review'},
  ];


});

