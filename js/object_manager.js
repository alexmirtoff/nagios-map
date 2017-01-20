/*
* (c) 2016 Alex Mirtoff
* e-mail: alex@mirtoff.ru
* OOONETMAP
*
*/


ymaps.ready(init);

var sessionId;
$.ajaxSetup({ cache: false });

$.ajax({
        type: 'GET',
        url: 'sessions.php',
        async: false,
        success : function(data) {
	    sessionId = data
        }
});
	                        

function init () {
    var myMap = new ymaps.Map('map', {
            center: [45.044502, 41.969065],
            zoom: 10
        }, {
            searchControlProvider: 'yandex#search'
        }),
    loadingObjectManager = new ymaps.LoadingObjectManager('https://n.*****.ru/netmap/get_obj.php?bbox=%b&callback=cb', {
        clusterize: true,
        clusterHasBalloon: true,

        groupByCoordinates: true,
        geoObjectOpenBalloonOnClick: true,
        clusterDisableClickZoom: true,
        clusterBalloonContentLayout: "cluster#balloonAccordion"
        
	});

    //loadingObjectManager.objects.options.set('preset', 'islands#blueDotIcon');
setupPresets();

function setupPresets () {
            ymaps.option.presetStorage
	            .add('l2#up', {
	         	   iconLayout: 'default#image',
		            iconImageHref: 'img/40x20/L2-UP.png',
		            iconImageSize: [30, 15],
		            iconImageOffset: [-10, 0]
	            })
	            .add('game#healthIcon', {
		            iconLayout: 'default#image',
		            iconImageHref: './images/health.png',
		            iconImageSize: [30, 30],
		            iconImageOffset: [-15, -15]
		    })
		            .add('game#jumpIcon', {
		            iconLayout: 'default#image',
		            iconImageHref: './images/jump.png',
		            iconImageSize: [30, 30],
		            iconImageOffset: [-15, -15]
		    });
}


    loadingObjectManager.objects.options.set('preset', 'l2#up');

    loadingObjectManager.clusters.options.set('preset', 'islands#blueClusterIcons');


    myMap.geoObjects.add(loadingObjectManager);

//    myMap.events.add('boundschange', function (event) {
//	    if (event.get('newZoom') != event.get('oldZoom')) {
//            alert('Уровень масштабирования изменился');
//              if (typeof myPolyline !== 'undefined') {
//                  myMap.geoObjects.removeAll(myPolyline);
//	          draw();}
//			        }
//});

function checkFile()
{
    $.ajax({
        type: 'HEAD',
        url: `tmp/${sessionId}.json`,
        async: false,
        error : function(){
        setTimeout(function(){ checkFile(); }, 3000);
        },
        success : function(data) {
            draw();
        }
   });
}
                                                                                        
$(function() {
    checkFile();
});

//draw();

function draw() {
//console.log(loadingObjectManager.objects.getAll());

function getSelectedValues(callback) {
	$.getJSON(`tmp/${sessionId}.json`, function (data) {
		var dataArray = [];
		$.each(data.features, function (key, item) {                
	        	var latitude = data.features[key].geometry.coordinates[0];
		        var longitude = data.features[key].geometry.coordinates[1];
		        var id = data.features[key].id;
		        var tempArray = []

			tempArray.push(id, latitude, longitude);
		        dataArray.push(id);
		 });                            
  	callback(dataArray);
	});
}



getSelectedValues(function(values) {
	        
	        $.ajax({
	    	    type: "POST",
	    	    url: "get_parent.php",
	    	    async: true,
                    cache: false,
                    headers: { "cache-control": "no-cache" },
	    	    data: {values},
	    	    success: function(data){
	    	    var routes = $.parseJSON(data);
//	    	    console.log(data);
	    	    
	    	    st(routes);
	    	    }
		
		
	});
	
});


function st(routes) {
    
    var coords = []
        
    for(var i=0; i<routes.length; i++){
       //   console.log(routes[i].latitude);
          var myPolyline = new ymaps.Polyline([
          
          [routes[i].latitude, routes[i].longitude], [routes[i].parent_latitude, routes[i].parent_longitude]],
      {
         balloonContent: "Ломаная линия"
     }, {
     balloonCloseButton: false,
     strokeColor: "#2650C5",
     strokeWidth: 0.9,
     strokeOpacity: 0.7
     });

myMap.geoObjects.add(myPolyline);
}
}}


}
