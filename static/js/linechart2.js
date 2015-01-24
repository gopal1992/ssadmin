



$(function () {





var piechart_data2 = [
    { label: "Browser Integrity Check Failed",  data: 35, color: "#4e5361"},
    { label: "Rate Limiting Threshold Exceeded",  data: 13, color: "#949fb0"},
    { label: "HTTP Request Integrity Check Failed",  data: 30, color: "#fcb25d"},
    { label: "Aggregator Bot Traffic",  data: 15, color: "#44c2b9"},
    { label: "Behavioral Integrity Check Failed",  data: 7, color: "#a646a3"}
];






    $.plot($("#chartPie2"), piechart_data2, {
           series: {
		        pie: {
		            innerRadius: 0.6,
		            show: true
		        }
		    },
		     grid: {
      			  hoverable: true,
        		  clickable: true
    			},
         legend: {
            labelBoxBorderColor: "none" ,
    		position: "se"
         }
    });





});





//
// $(function() {
//
// 		var sin = [],
// 			cos = [],
// 			xax=  [];
//
// 			xax= [	[1, "Jan"],
// 					[2, "Feb"],
// 					[3, "Mar"],
// 					[4, "Apr"],
// 					[5, "May"],
// 					[6, "Jun"],
// 					[7, "Jul"],
// 					[8, "Aug"],
// 					[9, "Sep"],
// 					[10, "Oct"],
// 					[11, "Nov"],
// 					[12, "Dec"]
// 				];
//
// 			sin= [	[1, 100],
// 					[2, 1023],
// 					[3, 10342],
// 					[4, 100031],
// 					[5, 123442],
// 					[6, 2242424],
// 					[7, 242424],
// 					[8, 13131313],
// 					[9, 3123131],
// 					[10, 13131313],
// 					[11, 1131313],
// 					[12, 13131133]
// 				];
// 			cos = [	[1, 102120],
// 					[2, 1312423],
// 					[3, 103214342],
// 					[4, 102214331],
// 					[5, 1232144442],
// 					[6, 22421425624],
// 					[7, 24242146624],
// 					[8, 131361313],
// 					[9, 3163131],
// 					[10, 131331313],
// 					[11, 13133113],
// 					[12, 13153133]
// 				];
// 		var y_min_value =  parseFloat("0");
// 		var y_max_value = parseFloat("131531313133");
//
// 		var plot = $.plot("#dashboardConversions", [
// 			{ data: sin, label: "sin(x)"},
// 			{ data: cos, label: "cos(x)"}
// 		], {
// 			series: {
// 				lines: {
// 					show: true
// 				},
// 				points: {
// 					show: true
// 				}
// 			},
// 			grid: {
// 				hoverable: true,
// 				clickable: true
// 			},
// 			yaxis: {
//
// 				ticks: [1,10,100,1000,10000,100000],
//                  transform:  function(v) {return v*10; /*move away from zero*/}
// 			},
// 			xaxis: {
// 			ticks:xax ,
// 				font: {
// 					size: 12,
// 					family: "Open Sans, Arial",
// 					color: "#697695"
// 				}
// 				}
// 		});
//
// 		$("<div id='tooltip'></div>").css({
// 			position: "absolute",
// 			display: "none",
// 			border: "1px solid #fdd",
// 			padding: "2px",
// 			"background-color": "#fee",
// 			opacity: 0.80
// 		}).appendTo("body");
//
// 		$("#dashboardConversions").bind("plothover", function (event, pos, item) {
//
//
// 				if (item) {
// 					var x = item.datapoint[0].toFixed(2),
// 						y = item.datapoint[1].toFixed(2);
//
// 					$("#tooltip").html(item.series.label + " of " + x + " = " + y)
// 						.css({top: item.pageY+5, left: item.pageX+5})
// 						.fadeIn(200);
// 				} else {
// 					$("#tooltip").hide();
// 				}
//
// 		});
//
//
//
// 		// Add the Flot version string to the footer
//
//
// 	});
