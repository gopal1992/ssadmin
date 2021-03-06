var ArkAdmin = new
function ($) {
	"use strict";

	function updateContentHeight() {
		var windowHeight = $(window).height(),
			navHeight = $(".navbar-main").height();
		$(".content").css("min-height", windowHeight - navHeight - 1 + "px")
	}
	function initMenus() {
		function toggleMenu($menu) {
			$menu.toggleClass("open")
		}
		$(document).on("click", ".menu .menu-toggle", function (event) {
			event.preventDefault(), toggleMenu($(this).parents(".menu").first())
		})
	}
	function initControls() {
			$("textarea").autosize(), $('[data-toggle="tooltip"]').tooltip(), $("input:checkbox, input:radio").uniform(), $(".select2").select2(), $(".pie-chart").length && $(".pie-chart").easyPieChart({
			barColor: "#44ab89",
			lineWidth: 4,
			animate: 1e3,
			onStart: function () {
				if (!this.options.isInit) {
					this.options.isInit = !0;
					var color = $(this.el).data("barColor");
					color && (this.options.barColor = color)
				}
			},
			onStep: function (oldVal, newVal, crtVal) {
				$(this.el).find("span").text(Math.floor(crtVal) + "%")
			}
		})
	}
	function initDatePickers() {
		$(".datepicker").datepicker({
			autoclose: !0
		}), $("#reportrange").daterangepicker({
			ranges: {
				"Last Day": [moment().subtract("days", 2), moment().subtract("days", 2)],
// 				Yesterday: [moment().subtract("days", 1), moment().subtract("days", 1)],
				"Last 7 Days": [moment().subtract("days", 8), moment().subtract("days", 2)],
				"Last 30 Days": [moment().subtract("days", 31), moment().subtract("days", 2)],
				"This Month": [moment().startOf("month"), moment().endOf("month")],
				"Last Month": [moment().subtract("month", 1).startOf("month"), moment().subtract("month", 1).endOf("month")]
			},
			startDate: moment().startOf("month"),
			endDate: moment().endOf("month")
		}, function (start, end) {
			$("#reportrange span").html(start.format("MMMM D, YYYY") + " - " + end.format("MMMM D, YYYY"))
		})
	}
	function initCharts(charts) {
		function labelFormatter(label, series) {
			return "<div style='font-size:8pt; text-align:center; padding:2px; color:white;'>" + label + "<br/>" + Math.round(series.percent) + "%</div>"
		}
		function showTooltip(x, y, contents) {
			$('<div id="tooltip">' + contents + "</div>").css({
				position: "absolute",
				display: "none",
				top: y - 30,
				left: x - 50,
				color: "#fff",
				padding: "2px 5px",
				"border-radius": "6px",
				"background-color": "#000",
				opacity: .8
			}).appendTo("body").fadeIn(200)
		}
		var chartLines = {
			series: {
				lines: {
					show: !0,
					lineWidth: 1,
					fill: !0,
					fillColor: {
						colors: [{
							opacity: .1
						},
						{
							opacity: .13
						}]
					}
				},
				points: {
					show: !0,
					lineWidth: 2,
					radius: 3
				},
				shadowSize: 0,
				stack: !0
			},
			grid: {
				hoverable: !0,
				clickable: !0,
				tickColor: "#f9f9f9",
				borderWidth: 0
			},
			legend: {
				show: !0,
				labelBoxBorderColor: "#fff"
			},
			colors: ["#a7b5c5", "#30a0eb" , "#3ffffb"],
			xaxis: {
				ticks: [
					[1, "1Apr"],
					[2, "3Apr"],
					[3, "5Apr"],
					[4, "7Apr"],
					[5, "9Apr"],
					[6, "11Apr"],
					[7, "13Apr"],
					[8, "15Apr"],
					[9, "17Apr"],
					[10, "19Apr"],
					[11, "21Apr"],
					[12, "23Apr"],
					[13, "25Apr"]
				],
				font: {
					size: 12,
					family: "Open Sans, Arial",
					color: "#697695"
				}
			},
			yaxis: {
				ticks:[
					[1, "1"],
					[10, "10"],
					[100, "100"],
					[1000, "1K"],
					[10000, "10K"],
					[100000, "100K"],
					[1000000, "1M"],
					[10000000, "10M"]
				],
				transform:  function(v) { return Math.log(v+1); },
				tickFormatter:  function(v) { return Math.log(v+1); },
				font: {
					size: 12,
					color: "#9da3a9"
				}
			}
//  		grid: { hoverable: true, clickable: true }
		},
			pieOpts = {
				series: {
					pie: {
						show: !0,
						radius: 1,
						label: {
							show: !0,
							radius: .75,
							formatter: labelFormatter,
							background: {
								opacity: .8
							}
						}
					}
				},
				legend: {
					show: !1
				}
			},
			chartBars = {
				series: {
					bars: {
						show: !0,
						lineWidth: 1,
						fill: !0,
						fillColor: {
							colors: [{
								opacity: .1
							},
							{
								opacity: .13
							}]
						}
					}
				},
				legend: {
					show: !0,
					labelBoxBorderColor: "#fff"
				},
				colors: ["#30a0eb"],
				bars: {
					horizontal: !1,
					barWidth: .7
				},
				grid: {
					hoverable: !0,
					clickable: !0,
					tickColor: "#f9f9f9",
					borderWidth: 0
				},
				xaxis: {
					ticks: [
						[1, "Jan"],
						[2, "Feb"],
						[3, "Mar"],
						[4, "Apr"],
						[5, "May"],
						[6, "Jun"],
						[7, "Jul"],
						[8, "Aug"],
						[9, "Sep"],
						[10, "Oct"],
						[11, "Nov"],
						[12, "Dec"]
					],
					font: {
						size: 12,
						family: "Open Sans, Arial",
						color: "#697695"
					}
				},
				yaxis: {
					ticks: 5,
					tickDecimals: 0,
					font: {
						size: 13,
						color: "#9da3a9"
					}
				}
			};
		$.each(charts, function (id, value) {
			if ($(id).length) {
				var opts = null;
				switch (value.type) {
				case "bars":
					opts = chartBars;
					break;
				case "pie":
					opts = pieOpts;
					break;
				default:
 					opts = chartLines
				}
				var previousPoint = ($.plot($(id), value.data, opts), null);
				$(id).bind("plothover", function (event, pos, item) {
					if (item) {
						if (previousPoint != item.dataIndex) {
							previousPoint = item.dataIndex, $("#tooltip").remove();
							var y = (item.datapoint[0].toFixed(0), item.datapoint[1].toFixed(0)),
								month = item.series.xaxis.ticks[item.dataIndex].label;
							showTooltip(item.pageX, item.pageY, item.series.label + " of " + month + ": " + y)
						}
					} else $("#tooltip").remove(), previousPoint = null
				})
			}
		})
	}
	this.init = function (charts) {
		initControls(), initDatePickers(), initMenus(), "function" == typeof prettyPrint && prettyPrint(), initCharts(charts), updateContentHeight(), $("body").resize(function () {
			updateContentHeight()
		})
	}, this.initExamples = function () {
		if ($("#nestable").length) {
			var updateOutput = function (e) {
				var list = e.length ? e : $(e.target),
					output = list.data("output");
				window.JSON ? output.val(window.JSON.stringify(list.nestable("serialize"))) : output.val("JSON browser support required for this demo.")
			};
			$("#nestable").nestable({
				group: 1
			}).on("change", updateOutput), $("#nestable2").nestable({
				group: 1
			}).on("change", updateOutput), updateOutput($("#nestable").data("output", $("#nestable-output"))), updateOutput($("#nestable2").data("output", $("#nestable2-output"))), $("#nestable-menu").on("click", function (e) {
				var target = $(e.target),
					action = target.data("action");
				"expand-all" === action && $(".dd").nestable("expandAll"), "collapse-all" === action && $(".dd").nestable("collapseAll")
			})
		}
		$("#layout_options .options-handle").on("click", function (event) {
			event.preventDefault();
			var open = $("#layout_options").hasClass("open");
			open ? $("#layout_options").animate({
				right: "-180px"
			}).removeClass("open") : $("#layout_options").animate({
				right: "0px"
			}).addClass("open")
		}), $("#layout_options #fixed_container").on("click", function (event) {
			$(event.target).prop("checked") ? $(".wrapper").addClass("container") : $(".wrapper").removeClass("container")
		}), $("#layout_options #fixed_header").on("click", function (event) {
			$(event.target).prop("checked") ? $("body").addClass("fixed_header") : $("body").removeClass("fixed_header")
		}), $(":checkbox").on("click", function () {
			$(this).parent().nextAll("select").select2("enable", this.checked)
		}), setInterval(function () {
		//	$(".pie-chart").length && $(".pie-chart").last().data("easyPieChart").update(Math.floor(100 * Math.random()))
		}, 5e3), $("[data-toggle=popover]").popover({
			container: "body"
		}), $(".ark-ex-loading").click(function () {
			var btn = $(this);
			btn.button("loading"), setTimeout(function () {
				btn.button("reset")
			}, 3e3)
		});
		var date = new Date,
			d = date.getDate(),
			m = date.getMonth(),
			y = date.getFullYear();
		if ($("#calendar").length) var calendar = $("#calendar").fullCalendar({
			header: {
				left: "prev,next today",
				center: "title",
				right: "month,agendaWeek,agendaDay"
			},
			selectable: !0,
			editable: !0,
			select: function (start, end, allDay) {
				var title = prompt("Event Title:");
				title && calendar.fullCalendar("renderEvent", {
					title: title,
					start: start,
					end: end,
					allDay: allDay
				}, !0), calendar.fullCalendar("unselect")
			},
			events: [{
				title: "All Day Event",
				start: new Date(y, m, 1)
			},
			{
				title: "Long Event",
				start: new Date(y, m, d - 5),
				end: new Date(y, m, d - 2)
			},
			{
				id: 999,
				title: "Repeating Event",
				start: new Date(y, m, d - 3, 16, 0),
				allDay: !1
			},
			{
				id: 999,
				title: "Repeating Event",
				start: new Date(y, m, d + 4, 16, 0),
				allDay: !1
			},
			{
				title: "Meeting",
				start: new Date(y, m, d, 10, 30),
				allDay: !1
			},
			{
				title: "Lunch",
				start: new Date(y, m, d, 12, 0),
				end: new Date(y, m, d, 14, 0),
				allDay: !1
			},
			{
				title: "Birthday Party",
				start: new Date(y, m, d + 1, 19, 0),
				end: new Date(y, m, d + 1, 22, 30),
				allDay: !1
			},
			{
				title: "Click for Google",
				start: new Date(y, m, 28),
				end: new Date(y, m, 29),
				url: "http://google.com/"
			}]
		})
	}
}(jQuery);
jQuery(function () {
	"use strict";
	for (var data = [], i = 0; 5 > i; i++) data[i] = {
		label: "Series" + (i + 1),
		data: Math.floor(20 * Math.random()) + 15
	};
	var charts = {
//  		"#dashboardConversions": {
//  			data: [{
//  				label: "Genuine Users ",
//  				data: [
//  				[1, 30],
// 				[2, 70],
// 				[3, 92],
// 				[4, 321],
// 				[5, 682],
// 				[6, 1024],
// 				[7, 224],
// 				[8, 1003],
// 				[9, 331],
// 				[10, 893],
// 				[11, 903],
// 				[12, 733],
// 				[13, 331]
//  				]
//  			},
//
//  			{
//  			label: "Trusted Bots",
//  				data: [
//  				[1, 102120],
// 				[2, 1312423],
// 				[3, 1032342],
// 				[4, 1022131],
// 				[5, 1221442],
// 				[6, 224224],
// 				[7, 242424],
// 				[8, 131313],
// 				[9, 31631],
// 				[10, 131313],
// 				[11, 131313],
// 				[12, 131133],
// 				[13, 31311]
//  				]
//  			},
//
//  			{
//  				label: "Bad Bots",
//  				data: [
//  				[1, 120],
// 				[2, 12222233],
// 				[3, 1042],
// 				[4, 1131],
// 				[5, 1282],
// 				[6, 2224],
// 				[7, 2422],
// 				[8, 1313],
// 				[9, 3131],
// 				[10, 1313],
// 				[11, 13193],
// 				[12, 1318],
// 				[13, 1231]
//  				]
//  			}]
//  		},
		"#dashboardRevenues": {
			type: "bars",
			data: [{
				label: "Sales",
				data: [
					[1, 51231],
					[2, 44220],
					[3, 12455],
					[4, 24313],
					[5, 57523],
					[6, 98432],
					[7, 90934],
					[8, 78932],
					[9, 12367],
					[10, 67345],
					[11, 43672],
					[12, 74213]
				]
			}]
		},
		"#chartPie": {
			type: "pie",
			data: data
		}
	};
	ArkAdmin.init(charts), ArkAdmin.initExamples()
});