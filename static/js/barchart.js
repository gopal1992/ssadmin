function bad_bot_traffic_bar_chart(div_id, data_list, data_total) {
    var d1_1 = [
        [1325376000000, data_list[0]],
        [1328054400000, 0],
        [1330560000000, 0],
        [1333238400000, 0]

    ];

    var d1_2 = [
        [1325376000000, 0],
        [1328054400000, data_list[1]],
        [1330560000000, 0],
        [1333238400000, 0]

    ];

    var d1_3 = [
        [1325376000000, 0],
        [1328054400000, 0],
        [1330560000000, data_list[2]],
        [1333238400000, 0]
    ];

    var d1_4 = [
        [1325376000000, 0],
        [1328054400000, 0],
        [1330560000000, 0],
        [1333238400000, data_list[3]]
    ];


    var data1 = [];
    if(data_list[0]){
    data1.push({
    	label: "Browser Integrity Check Failed | | Non-browser traffic claiming to be coming from a browser | hovdt1",
        data: d1_1,
        bars: {
            show: true,
            barWidth: 12 * 24 * 60 * 60 * 300,
            fill: true,
            lineWidth: 1,
            order: 1,
            fillColor: "#002eb8"
        },
        color: "#002eb8"
    });
    }
    if(data_list[1]){
        data1.push({
        	label: "Rate Limiting Threshold Exceeded | | Traffic exceeded defined rate limits | hovdt2",
            data: d1_2,
            bars: {
                show: true,
                barWidth: 12 * 24 * 60 * 60 * 300,
                fill: true,
                lineWidth: 1,
                order: 2,
                fillColor: "#006600"
            },
            color: "#006600"
        });
        }
    if(data_list[2]){
        data1.push({
            label: "HTTP_Request Integrity Check Failed",
            data: d1_3,
            bars: {
                show: true,
                barWidth: 12 * 24 * 60 * 60 * 300,
                fill: true,
                lineWidth: 1,
                order: 3,
                fillColor: "#44c2B9"
            },
            color: "#44c2B9"
        });
        }
    if(data_list[3]){
        data1.push({
        	label: "Behavioral Integrity Check Failed",
            data: d1_4,
            bars: {
                show: true,
                barWidth: 12 * 24 * 60 * 60 * 300,
                fill: true,
                lineWidth: 1,
                order: 3,
                fillColor: "#a646a3"
            },
            color: "#a646a3"
        });
        }

    $.plot($(div_id), data1, {
        xaxis: {
            min: (new Date(2011, 11, 15)).getTime(),
            max: (new Date(2012, 04, 18)).getTime(),
            mode: "time",
            timeformat: "%b",
            tickSize: [1, "month"],
            monthNames: [ number_conversion(data_list[0], 0) , number_conversion(data_list[1], 0), number_conversion(data_list[2], 0), number_conversion(data_list[3], 0), number_conversion(data_list[4], 0)],
            tickLength: 0, // hide gridlines
            axisLabel: '',
            axisLabelUseCanvas: true,
            axisLabelFontSizePixels: 12,
            axisLabelFontFamily: 'Verdana, Arial, Helvetica, Tahoma, sans-serif',
            axisLabelPadding: 5
        },
        yaxis: {
            tickFormatter: function (val, axis) {
            return "";
            },
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
            container: $(".legendContainer"),
            labelFormatter: function(label, series) {
                var label_split = label.split('|');
                var label_new = "";
                if (label_split[2]) {
                    label_new = label_split[0] + '<a id="' + label_split[3].trim() + '"  data-toggle="popover" style="cursor: pointer; cursor: hand;" title="" data-content="' + label_split[2] + '"  data-placement="left" data-trigger="hover">?</a>';
                } else {
                    label_new = label_split[0];
                }
                return (label_new);
            }
        },
        series: {
            shadowSize: 1
        }
    });

}


function action_on_bad_bot_bar_chart(div_id, data_list, data_total) {
    var d1_1 = [
        [1325376000000, data_list[0]],
        [1328054400000, 0],
        [1330560000000, 0],
        [1333238400000, 0]

    ];

    var d1_2 = [
        [1325376000000, 0],
        [1328054400000, data_list[1]],
        [1330560000000, 0],
        [1333238400000, 0]
    ];

    var d1_3 = [
        [1325376000000, 0],
        [1328054400000, 0],
        [1330560000000, data_list[2]],
        [1333238400000, 0]
    ];

    var d1_4 = [
        [1325376000000, 0],
        [1328054400000, 0],
        [1330560000000, 0],
        [1333238400000, data_list[3]]
    ];

    var data1 = [];
    if(data_list[0]){
    data1.push({
        label: "Allow",
        data: d1_1,
        bars: {
            show: true,
            barWidth: 12 * 24 * 60 * 60 * 300,
            fill: true,
            lineWidth: 1,
            order: 1,
            fillColor: "#aad42f"
        },
        color: "#aad42f "
    });
    }
    if(data_list[1]){
    data1.push({
    	label: "Show Captcha",
        data: d1_2,
        bars: {
            show: true,
            barWidth: 12 * 24 * 60 * 60 * 300,
            fill: true,
            lineWidth: 1,
            order: 2,
            fillColor: "#FFFF33"
        },
        color: "#FFFF33"
    });
    }
    if(data_list[2]){
    data1.push({
        label: "Block",
        data: d1_3,
        bars: {
            show: true,
            barWidth: 12 * 24 * 60 * 60 * 300,
            fill: true,
            lineWidth: 1,
            order: 3,
            fillColor: "#ff6600"
        },
        color: "#ff6600"
    });
    }
    if(data_list[3]){
    data1.push({
        label: "Feed Fake Data",
        data: d1_4,
        bars: {
            show: true,
            barWidth: 12 * 24 * 60 * 60 * 300,
            fill: true,
            lineWidth: 1,
            order: 2,
            fillColor: "#660000"
        },
        color: "#660000"
    });
    }

    $.plot($(div_id), data1, {
        xaxis: {
            min: (new Date(2011, 11, 15)).getTime(),
            max: (new Date(2012, 04, 18)).getTime(),
            mode: "time",
            timeformat: "%b",
            tickSize: [1, "month"],
            monthNames: [ number_conversion(data_list[0], 0) , number_conversion(data_list[1], 0), number_conversion(data_list[2], 0), number_conversion(data_list[3], 0), ''],
            tickLength: 0, // hide gridlines
            axisLabel: '',
            axisLabelUseCanvas: true,
            axisLabelFontSizePixels: 12,
            axisLabelFontFamily: 'Verdana, Arial, Helvetica, Tahoma, sans-serif',
            axisLabelPadding: 5
        },
        yaxis: {
            tickFormatter: function (val, axis) {
            return "";
            },
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
            container: $(".legendContainer_bar")
        },

        series: {
            shadowSize: 1
        }
    });

}

function number_conversion(numeric_value,digit)
{
    if (numeric_value)
    {
        return abbrNum(numeric_value,digit);
    }
    else
    {
        return '';
    }
}
