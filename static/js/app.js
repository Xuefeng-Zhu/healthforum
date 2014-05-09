var apiUrl = "http://localhost:5000"
var app = angular.module('myapp', ['ngRoute','ngAnimate', 'ngSanitize', 'ngCookies', 'mgcrea.ngStrap', 'toggle-switch']);

app.config(['$routeProvider',
	function($routeProvider) {
		$routeProvider.
		when('/', {
			templateUrl: 'partials/help.html',
		}).
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


app.controller('MainCtrl', function($scope, $http, $aside, $alert, $location, $cookies) {

	if ($cookies.visited != "true"){
		runIntro();
		$cookies.visited = "true";
	}

	if ($cookies.user){
		$scope.user = angular.fromJson($cookies.user);
	}

	$scope.searchText = "";
	$scope.searchMode = true;

	$http.get(apiUrl + '/drugs/all').success(function(data){
		$scope.drugs = data;
	});
	
	$scope.intro = runIntro;

	$scope.getList = function(viewValue) {
		if (viewValue.length == 0){
			return;
		}
		return $http.get(apiUrl + '/drugs/list/' + $scope.searchText)
		.then(function(res) {
			return res.data;
		});
	}

	$scope.search = function(){
		if ($scope.searchText.length == 0){
			return;
		}
		console.log($scope.searchText);
		$http.get(apiUrl + '/drugs/result/' + $scope.searchText).success(function(data){
			$scope.drugs = data;
		});
	}

	var loginAside;
	var signupAside;
	$scope.logAside = function(){
		loginAside = $aside({scope: $scope, template: 'partials/account.html'});
	}

	$scope.signAside = function(){
		signupAside = $aside({scope: $scope, template: 'partials/signup.html'});
	}

	$scope.createAcount = function(){
		var email = $('#EmailR').val();
		var password1 = $('#Password1').val();
		var password2 = $('#Password2').val();
		var first = $('#First').val();
		var last = $('#Last').val();

		if (password1 != password2){
			$alert({title: 'Error!', content: "passwords do not match", placement: 'top-left', type: 'danger', show: true, duration: 3});			
			return;
		}
		var data = {'email': email, 'password': password1, 'first': first, 'last': last, 'isDoctor': false};
		$http.post(apiUrl + '/registration/user', data).success(function(data){
			$alert({title: 'Success!', content: data.message, placement: 'top-left', type: 'success', show: true, duration: 3});
			signupAside.hide();
		})
		.error(function(data){
			$alert({title: 'Error!', content: data.message, placement: 'top-left', type: 'danger', show: true, duration: 3});
		});
	}

	$scope.login = function(){
		data = {'email': $('#Email').val(), 'password': $('#Password').val()};
		$http.post(apiUrl + '/login/user', data).success(function(data){
			$alert({title: 'Success!', content: "Hi, " + data.first_name + ". You are logining in.", placement: 'top-left', type: 'success', show: true, duration: 3});
			$scope.user = {name: data.first_name, id: data.id}
			$cookies.user = angular.toJson($scope.user); 
			console.log($cookies.user)
			loginAside.hide();
		})
		.error(function(data){
			$alert({title: 'Error!', content: data.message, placement: 'top-left', type: 'danger', show: true, duration: 3});
		});
	}

	$scope.logout = function(){
		delete $scope.user;
		delete $cookies.user;
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

	$http.get(apiUrl + '/drugs/info/'+ $scope.drugName).success(function(data){
		$scope.description = data;
	});	

});

app.controller('SideEffectCtrl', function($scope, $http, $routeParams){
	$scope.drugName = $routeParams["drugName"];
	$scope.panel = "panel panel-info";

	$scope.$watch('searchMode', function(){
		$http.get(apiUrl + '/drugs/' + $scope.drugName + ($scope.searchMode ? '/patient' : '/doctor')).success(function(data){
			$scope.effects = data.sideEffects;
		});	
		$scope.panel = $scope.searchMode ? "panel panel-info" : "panel panel-success"
	}, true);

});

app.controller('CommentsCtrl', function($scope, $http, $routeParams){
	$scope.drugName = $routeParams["drugName"];

	$http.get(apiUrl + '/comments/get/'+ $scope.drugName).success(function(data){
		$scope.comments = data;
	});	

	$scope.subComment = function(){
		console.log($('.summernote').code())
	}

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
