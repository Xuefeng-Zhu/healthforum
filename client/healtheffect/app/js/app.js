var app = angular.module('mgcrea.ngStrapDocs', ['ngAnimate', 'ngSanitize', 'mgcrea.ngStrap']);

app.controller('MainCtrl', function($scope) {
});

'use strict';

angular.module('mgcrea.ngStrapDocs')

.controller('SelectDemoCtrl', function($scope, $http) {

  $scope.selectedIcon = '';
  $scope.icons = [
    {value: 'Relevance', label: '<i class="fa fa-plus"></i> Relevance'},
    {value: 'Letter', label: '<i class="fa fa-sort-alpha-asc"></i> Letter'},
    {value: 'Most Review', label: '<i class="fa fa-comment"></i> Most Review'}
  ];

  $scope.drugs = [
  {name: 'A', concise:'Demo, Demo, Demo, Demo Demo, Demo, Demo, Demo Demo, Demo, Demo, Demo'},
  {name: 'B', concise:'Demo, Demo, Demo, Demo Demo, Demo, Demo, Demo Demo, Demo, Demo, Demo'},
  {name: 'C', concise:'Demo, Demo, Demo, Demo Demo, Demo, Demo, Demo Demo, Demo, Demo, Demo'},
  {name: 'D', concise:'Demo, Demo, Demo, Demo Demo, Demo, Demo, Demo Demo, Demo, Demo, Demo'},
  {name: 'E', concise:'Demo, Demo, Demo, Demo Demo, Demo, Demo, Demo Demo, Demo, Demo, Demo'},
  {name: 'F', concise:'Demo, Demo, Demo, Demo Demo, Demo, Demo, Demo Demo, Demo, Demo, Demo'},
  {name: 'G', concise:'Demo, Demo, Demo, Demo Demo, Demo, Demo, Demo Demo, Demo, Demo, Demo'},
  {name: 'H', concise:'Demo, Demo, Demo, Demo Demo, Demo, Demo, Demo Demo, Demo, Demo, Demo'},
  {name: 'I', concise:'Demo, Demo, Demo, Demo Demo, Demo, Demo, Demo Demo, Demo, Demo, Demo'},
  {name: 'J', concise:'Demo, Demo, Demo, Demo Demo, Demo, Demo, Demo Demo, Demo, Demo, Demo'},
  {name: 'K', concise:'Demo, Demo, Demo, Demo Demo, Demo, Demo, Demo Demo, Demo, Demo, Demo'},
  ];


});

