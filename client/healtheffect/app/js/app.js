var app = angular.module('myapp', ['ngRoute','ngAnimate', 'ngSanitize', 'mgcrea.ngStrap']);

app.config(['$routeProvider',
	function($routeProvider) {
		$routeProvider.
		when('/', {
			templateUrl: 'partials/description.html',
			controller: 'DescriptionCtrl'
		}).
		when('/sideeffect/:drugName', {
			templateUrl: 'partials/sideeffect.html',
			controller: 'SideEffectCtrl'
		}).
		when('/comments', {
			templateUrl: 'partials/comments.html',
			controller: 'CommentsCtrl'
		}).
		otherwise({
			redirectTo: '/'
		});
	}]);


app.controller('MainCtrl', function($scope, $http) {

	$scope.searchText = "";
	$scope.drugList = ["a","ab"];

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

});

app.controller('DescriptionCtrl', function($scope, $http){
	$scope.description = {name: 'A', manufacture:'xxxx', price:'$18'}
});

app.controller('SideEffectCtrl', function($scope, $http, $routeParams){
	$scope.drugName = $routeParams["drugName"];
	$http.get('http://healthforum.herokuapp.com/drugs/drugName/patient').success(function(data){
		$scope.effects = data.effects;
	});	
	$scope.effects = [
	{name: 'A', links:[{name: 'Cnbeta', url:'http://www.Cnbeta.com'},{name: 'Google', url:'www.google.com'}]},
	{name: 'B', links:[{name: 'Cnbeta', url:'http://www.Cnbeta.com'},{name: 'Google', url:'www.google.com'}]}
	]
});

app.controller('CommentsCtrl', function($scope, $http){
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
