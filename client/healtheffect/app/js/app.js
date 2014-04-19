var app = angular.module('myapp', ['ngRoute','ngAnimate', 'ngSanitize', 'mgcrea.ngStrap', 'toggle-switch']);

app.config(['$routeProvider',
	function($routeProvider) {
		$routeProvider.
		when('/description/:drugName', {
			templateUrl: 'partials/description.html',
			controller: 'DescriptionCtrl'
		}).
		when('/sideeffect/:drugName', {
			templateUrl: 'partials/sideeffect.html',
			controller: 'SideEffectCtrl'
		}).
		when('/comments/:drugName', {
			templateUrl: 'partials/comments.html',
			controller: 'CommentsCtrl'
		}).
		otherwise({
			redirectTo: '/'
		});
	}]);


app.controller('MainCtrl', function($scope, $http) {

	$scope.searchText = "";
	$scope.searchMode = true;

	$http.get('http://healthforum.herokuapp.com/drugs/all').success(function(data){
		$scope.drugs = data;
	});
	
	$scope.getList = function(viewValue) {
		if (viewValue.length == 0){
			return;
		}
		return $http.get('http://healthforum.herokuapp.com/drugs/list/' + $scope.searchText)
		.then(function(res) {
			return res.data;
		});
	}

	$scope.search = function(){
		if ($scope.searchText.length == 0){
			return;
		}
		console.log($scope.searchText);
		$http.get('http://healthforum.herokuapp.com/drugs/result/' + $scope.searchText).success(function(data){
			$scope.drugs = data;
		});

	}
});

'use strict';

app.controller('SelectDemoCtrl', function($scope, $http) {

	$scope.selectedIcon = '';
	$scope.icons = [
	{value: 'Relevance', label: '<i class="fa fa-plus"></i> Relevance'},
	{value: 'Letter', label: '<i class="fa fa-sort-alpha-asc"></i> Letter'},
	{value: 'Most Review', label: '<i class="fa fa-comment"></i> Most Review'}
	];

	$scope.sDrug = function(name){
		$scope.selectDrug = name;
	}

});

app.controller('DescriptionCtrl', function($scope, $http, $routeParams){
	$scope.drugName = $routeParams["drugName"];

	$scope.description = {name: 'A', manufacture:'xxxx', price:'$18'}

	$http.get('http://mapi-us.iterar.co/api/' + $scope.drugName +'/doses.json', {headers: {'Authorization': 'Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=='}}).success(function(data){
		$scope.description.doses = data;
	});	

});

app.controller('SideEffectCtrl', function($scope, $http, $routeParams){
	$scope.drugName = $routeParams["drugName"];
	$scope.panel = "panel panel-info";

	$scope.$watch('searchMode', function(){
		$http.get('http://healthforum.herokuapp.com/drugs/' + $scope.drugName + ($scope.searchMode ? '/patient' : '/doctor')).success(function(data){
			$scope.effects = data.effects;
		});	
		$scope.panel = $scope.searchMode ? "panel panel-info" : "panel panel-success"
	}, true);

	$http.get('http://healthforum.herokuapp.com/drugs/' + $scope.drugName + ($scope.searchMode ? '/patient' : '/doctor')).success(function(data){
		$scope.effects = data.effects;
	});	
});

app.controller('CommentsCtrl', function($scope, $http, $routeParams){
	$scope.drugName = $routeParams["drugName"];

	$(document).ready(function() {
		$('.summernote').summernote({
			toolbar: [
            ['style', ['style']], // no style button
            ['style', ['bold', 'italic', 'underline', 'clear']],
            ['fontsize', ['fontsize']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['height', ['height']],
            ['insert', ['picture', 'link']], // no insert buttons
            ['table', ['table']], // no table button
            ['help', ['help']] //no help button
            ],
            height: 150

        });	});

})
