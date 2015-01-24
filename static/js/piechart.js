var pie_config1 = {
           series: {
		        pie: {
		            innerRadius: 0.3,
		            show: true,
		            label: {
                    show: true,
                    radius: 0.85,
					formatter: function(label, series){
                        return '<div style="font-size:8pt;text-align:center;padding:2px;color:#000;">'+Math.round(series.percent)+'%</div>';
                    }

                    }
		        }
		    },
		     grid: {
      			  hoverable: true,
        		  clickable: true
    			},
    		tooltip: true,
			tooltipOpts: {
				content: function(label, series) {
		            var label_split =label.split('|');
		            var label_new = "";
		            if(label_split[1])
		            {
						label_new = label_split[1];
		            }
		            else
		            {
						label_new = label_split[0];
		            }
	            	return label_new;
				}, // show percentages, rounding to 2 decimal places
				shifts: {
					x: 20,
					y: 0
				},
				defaultTheme: false,

			},
		legend: {
        show: true,
        labelFormatter: function(label, series) {
            var percent= Math.round(series.percent);
            var number= series.data[0][1];
            var label_split =label.split('|');
            var label_new = "";
            if(label_split[2])
            {
				label_new = label_split[0] + '<a id="'+label_split[3].trim()+'"  data-toggle="popover" style="cursor: pointer; cursor: hand;" title="" data-content="'+label_split[2]+'"  data-placement="left" data-trigger="hover">?</a>';
            }
            else
            {
				label_new = label_split[0] ;
            }
            return(label_new);
        },
         position: "se"
        }
    } ;





function pie_action_taken (div_id,data_list,data_total)
{

var piechart_data1 = [
{ label: "Monitor |"+abbrNum(Math.round(data_list[0]),0)+" bot hits",  data: Math.round((data_list[0]/data_total)*100), color: "#aad42f"},
{ label: "Show Captcha |"+abbrNum(Math.round(data_list[1]),0) +" bot hits",  data: Math.round((data_list[1]/data_total)*100), color: "#6e9fba"},
{ label: "Block |"+abbrNum(Math.round(data_list[2]),0) +" bot hits",  data: Math.round((data_list[2]/data_total)*100), color: "#f7b563"},
{ label: "Feed Fake Data |"+abbrNum(Math.round(data_list[3]),0) +" bot hits",  data: Math.round((data_list[3]/data_total)*100), color: "#ed5509"},
	];


$.plot($(div_id), piechart_data1,pie_config1 );


	}

function bad_bot_traffic (div_id,data_list,data_total)
{
var piechart_data2 = [
    { label: "Browser Integrity Check Failed | "+ abbrNum(Math.round(data_list[0]),0) +" bot hits | Non-browser traffic claiming to be coming from a browser | hovdt1 ",  data: Math.round((data_list[0]/data_total)*100), color: "#4e5361"},
  	{ label: "Rate Limiting Threshold Exceeded | "+ abbrNum(Math.round(data_list[1]),0) +" bot hits| Traffic exceeded defined rate limits | hovdt2",  data: Math.round((data_list[1]/data_total)*100), color: "#913037"},
    { label: "HTTP_Request Integrity Check Failed | "+ abbrNum(Math.round(data_list[2]),0) +" bot hits",  data: Math.round((data_list[2]/data_total)*100), color: "#8F7B3B"},
    { label: "Aggregator Bot Traffic | "+ abbrNum(Math.round(data_list[3]),0) +" bot hits",  data: Math.round((data_list[3]/data_total)*100), color: "#44c2b9"},
    { label: "Behavioral Integrity Check Failed | "+ abbrNum(Math.round(data_list[4]),0) +" bot hits",  data: Math.round((data_list[4]/data_total)*100), color: "#a646a3"}
];
$.plot($(div_id), piechart_data2,pie_config1 );
}
function bad_bot_traffic_bar(div_id,data_list,data_total)
{
  var d1_1 = [
        [1325376000000, Math.round((data_list[0]/data_total)*100)],
        [1328054400000, 0],
        [1330560000000, 0],
        [1333238400000, 0],
        [1335830000000, 0]

    ];

    var d1_2 = [
        [1325376000000, 0],
        [1328054400000, Math.round((data_list[1]/data_total)*100)],
        [1330560000000, 0],
        [1333238400000, 0],
        [1335830000000, 0]
    ];

    var d1_3 = [
        [1325376000000, 0],
        [1328054400000, 0],
        [1330560000000, Math.round((data_list[2]/data_total)*100)],
        [1333238400000, 0],
        [1335830400000, 0]
    ];

       var d1_4 = [
        [1325376000000, 0],
        [1328054400000, 0],
        [1330560000000, 0],
        [1333238400000, Math.round((data_list[3]/data_total)*100)],
        [1335830400000, 0]
    ];

       var d1_5 = [
        [1325376000000, 0],
        [1328054400000, 0],
        [1330560000000, 0],
        [1333238400000, 0],
        [1335830400000, Math.round((data_list[4]/data_total)*100)]
    ];


    var data1 = [
        {
            label: "Browser Integrity Check Failed | | Non-browser traffic claiming to be coming from a browser | hovdt1",
            data: d1_1,
            bars: {
                show: true,
                barWidth: 12*24*60*60*300,
                fill: true,
                lineWidth: 1,
                order: 1,
                fillColor:  "#4e5361"
            },
            color: "#4e5361	"
        },
        {
            label: "Rate Limiting Threshold Exceeded | | Traffic exceeded defined rate limits | hovdt2",
            data: d1_2,
            bars: {
                show: true,
                barWidth: 12*24*60*60*300,
                fill: true,
                lineWidth: 1,
                order: 2,
                fillColor:  "#913037"
            },
            color: "#913037"
        },
        {
            label: "HTTP_Request Integrity Check Failed",
            data: d1_3,
            bars: {
                show: true,
                barWidth: 12*24*60*60*300,
                fill: true,
                lineWidth: 1,
                order: 3,
                fillColor:  "#8F7B3B"
            },
            color: "#8F7B3B"
        },

        {
            label: "Aggregator Bot Traffic",
            data: d1_4,
            bars: {
                show: true,
                barWidth: 12*24*60*60*300,
                fill: true,
                lineWidth: 1,
                order: 2,
                fillColor:  "#44c2b9"
            },
            color: "#44c2b9"
        },
        {
            label: "Behavioral Integrity Check Failed",
            data: d1_5,
            bars: {
                show: true,
                barWidth: 12*24*60*60*300,
                fill: true,
                lineWidth: 1,
                order: 3,
                fillColor:  "#a646a3"
            },
            color: "#a646a3"
        }


    ];

    $.plot($(div_id), data1, {
        xaxis: {
        	 min: (new Date(2011, 11, 15)).getTime(),
            max: (new Date(2012, 04, 18)).getTime(),
            mode: "time",
            timeformat: "%b",
            tickSize: [1, "month"],
            monthNames: ["("+Math.round((data_list[0]/data_total)*100)+"%)","("+Math.round((data_list[1]/data_total)*100)+"%)", "("+Math.round((data_list[2]/data_total)*100)+"%)", "("+Math.round((data_list[3]/data_total)*100)+"%)", "("+Math.round((data_list[4]/data_total)*100)+"%)"],
            tickLength: 0, // hide gridlines
  			axisLabel: 'Month',
            axisLabelUseCanvas: true,
            axisLabelFontSizePixels: 12,
            axisLabelFontFamily: 'Verdana, Arial, Helvetica, Tahoma, sans-serif',
            axisLabelPadding: 5
        },
        yaxis: {
        	ticks: [[10,"10%"],[20,"20%"],[30,"30%"],[40,"40%"],[50,"50%"],[60,"60%"],[70,"70%"],[80,"80%"],[90,"90%"],[100,"100%"]],
            axisLabelUseCanvas: true,
            axisLabelFontSizePixels: 12,
            axisLabelFontFamily: 'Verdana, Arial, Helvetica, Tahoma, sans-serif',
            axisLabelPadding: 5
        },
        grid: {
            hoverable: true,
            clickable: false,
            borderWidth: 1
        },
        legend: {
            container:$(".legendContainer"),
            labelFormatter: function(label, series) {
            var label_split =label.split('|');
            var label_new = "";
            if(label_split[2])
            {
				label_new = label_split[0] + '<a id="'+label_split[3].trim()+'"  data-toggle="popover" style="cursor: pointer; cursor: hand;" title="" data-content="'+label_split[2]+'"  data-placement="left" data-trigger="hover">?</a>';
            }
            else
            {
				label_new = label_split[0] ;
            }
            return(label_new);
			}
                  },
        series: {
            shadowSize: 1
        }
    });

    }


