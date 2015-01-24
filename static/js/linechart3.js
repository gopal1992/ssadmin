function ip_analysis_line_graph(div_id, dt1, dt4, ct, hourly_message) {
    var data1 = [],
        data2 = [],
        data3 = [],
        data4 = [],
        xax = [],
        yax = [],
        yax_main = [];
    var data_allowed = dt1.length;
    if (dt4.length <= 10) {
        var dl = dt4.length;
        var datalen = Math.round(dt1.length / dl);
        var xlen = 0;
        for (var i = 0; i < (dl); i++) {

            var new_element = [xlen, dt4[i]];
            xlen = xlen + datalen;
            xax.push(new_element);
        }


    } else {

        var datalen = Math.round((dt1.length) / 10);
        var dl = dt1.length / datalen;

        if (dl <= 10) {

            var xlen = 0;

            for (var i = 0; i < (dl); i++) {

                var new_element = [xlen, dt4[xlen]];
                xlen = xlen + datalen;
                xax.push(new_element);


            }

        } else {

            datalen = datalen + 1;
            dl = dt1.length / datalen;

            var xlen = 0;

            for (var i = 0; i < (dl); i++) {
                var new_element = [xlen, dt4[xlen]];
                xlen = xlen + datalen;
                xax.push(new_element);
            }
        }
    }

    for (var i = 0; i < data_allowed; i++) {
    	var str= dt4[i];
//    	str.replace(",", "");
        var new_date = str.split(" ");
        var date_update = "";
        if(new_date[2]){
        date_update = new_date[0] + " " + new_date[1]+ " "+ new_date[2];
        }
        else{
        date_update = new_date[0] + " " + new_date[1];
        }
        var new_element = [i, dt4[i]];
        data4.push(new_element);

    }




    for (var i = 0; i < data_allowed; i++) {
        var new_element = [i, dt1[i]];
        data1.push(new_element);
    }

    var tot_max = 0

    var tot_min;

    var dt1_max = dt1.reduce(function(previous, current) {
        return previous > current ? previous : current
    });
    var dt1_min = dt1.reduce(function(previous, current) {
        return previous < current ? previous : current
    });
    tot_max = tot_max > dt1_max ? tot_max : dt1_max;
    tot_min = dt1_min;

//
//     yax_main = [
//         [1, "1"],
//         [10, "10"],
//         [100, "100"],
//         [1000, "1K"],
//         [10000, "10K"],
//         [100000, "100K"],
//         [1000000, "1M"],
//         [10000000, "10M"],
//         [100000000, "100M"],
//         [1000000000, "1B"],
//         [10000000000, "10B"]
//     ];
//     var i = 0;
//     var bottom_value = 0;
//     for (; i < 10; i++) {
//         if ((yax_main[i])[0] < tot_max) {
//                 yax.push(yax_main[i]);
//         }
//         else {
//             break;
//         }
//     }
//     yax.push(yax_main[i]);


    var options1 = {

        grid: {
            hoverable: true,
            clickable: true,
            borderWidth: {
                top: 0,
                right: 0,
                bottom: 1,
                left: 1
            }
        },

        xaxis: {
            ticks: xax

        },
        yaxis: {
            tickFormatter: function(val, axis) { return abbrNum(Math.round(val),2);},
            minTickSize: 1
        },
        labelWidth: null,
        legend: {
            noColumns: 0,
            container: $(".legend_line_chart_Container")
        }
    };

    var plot1 = $.plot($(div_id), [{
        label: "No of bot hits",
        data: data1,
        color: '#ff0000'
    }], options1);

    if(hourly_message){
    	$('#hourly_message_'+ct).html(hourly_message);
    }

    $("<div id='tooltip'></div>").css({
        position: "absolute",
        display: "none",
        border: "1px solid #fdd",
        padding: "4px",
        "border-radius": "6px",
        "background-color": "#6b7002",
        "color": "#ffffff",
        "font-weight": "bold",
        opacity: 0.80
    }).appendTo("body");

     $(div_id).bind("plothover", function(event, pos, item) {
         if (1) {
             if (item) {
                 var x = item.datapoint[0],
                     y = item.datapoint[1].toFixed(2);
                 var hover_title = " bot hits"
                 $("#tooltip").html(data4[x][1] + " - " + abbrNum(Math.round(y), 2) + hover_title)
                     .css({
                         top: item.pageY + 5,
                         left: item.pageX + 5
                     })
                     .fadeIn(200);
             } else {
                 $("#tooltip").hide();
             }
         }
     });

     $("#placeholder").bind("plotclick", function(event, pos, item) {
         if (item) {
             //              $("#clickdata").text(" - click point " + item.dataIndex + " in " + item.series.label);
             plot.highlight(item.series, item.datapoint);
         }
     });



}




function abbrNum(number, decPlaces) {
    // 2 decimal places => 100, 3 => 1000, etc
    decPlaces = Math.pow(10, decPlaces);

    // Enumerate number abbreviations
    var abbrev = ["k", "m", "b", "t"];

    // Go through the array backwards, so we do the largest first
    for (var i = abbrev.length - 1; i >= 0; i--) {

        // Convert array index to "1000", "1000000", etc
        var size = Math.pow(10, (i + 1) * 3);

        // If the number is bigger or equal do the abbreviation
        if (size <= number) {
            // Here, we multiply by decPlaces, round, and then divide by decPlaces.
            // This gives us nice rounding to a particular decimal place.
            number = Math.round(number * decPlaces / size) / decPlaces;

            // Handle special case where we round up to the next abbreviation
            if ((number == 1000) && (i < abbrev.length - 1)) {
                number = 1;
                i++;
            }

            // Add the letter for the abbreviation
            number += abbrev[i];

            // We are done... stop
            break;
        }
    }

    return number;
}


