window.onload = function () {

var chart = new CanvasJS.Chart("my_chart", {
	animationEnabled: true,
	theme: "light2",
	title:{
		text: "My Latest Rounds"
	},
	axisY:{
		includeZero: false
	},
	data: [{
		type: "line",
		dataPoints: [
		    { y: 650, indexLabel: "lowest",markerColor: "DarkSlateGrey", markerType: "cross"},
			{ y: 700,},
			{ y: 750},
			{ y: 800 },
			{ y: 850 },
			{ y: 900 },
			{ y: 950 },
			{ y: 1000 },
			{ y: 1050 },
			{ y: 1100 },
			{ y: 1150 },
			{ y: 1200, indexLabel: "highest",markerColor: "red", markerType: "triangle" }
		]
	}]
});
chart.render();
}