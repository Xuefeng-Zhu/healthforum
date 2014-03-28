var app = angular.module('myapp', ['ngRoute','ngAnimate', 'ngSanitize', 'mgcrea.ngStrap']);

app.config(['$routeProvider',
	function($routeProvider) {
		$routeProvider.
		when('/', {
			templateUrl: 'partials/description.html',
			controller: 'DescriptionCtrl'
		}).
		when('/sideeffect', {
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


app.controller('MainCtrl', function($scope) {

});

'use strict';

app.controller('SelectDemoCtrl', function($scope, $http) {

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

app.controller('DescriptionCtrl', function($scope, $http){
	$scope.description = {name: 'A', manufacture:'xxxx', price:'$18'}
});

app.controller('SideEffectCtrl', function($scope, $http){
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
