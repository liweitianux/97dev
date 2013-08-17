var detail_chart;

// set global options for hightcharts {{{
$(function() {
    Highcharts.setOptions ({
        chart: {
            type: 'area',
            marginLeft: 15,
            height: 223,
            spacingTop: 10,
            spacingBottom: 0
            //overflow: false,
            //zIndex: 5
        },
        colors: ['#31B6AD'],
        credits: {
            enabled: false
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            series: {
                fillOpacity: 0.12,
                lineWidth: 1,
                marker: {
                    enabled: true, //false false的时候就不会突出显示点
                    lineColor: '#31B6AD',
                    lineWidth: 1,
                    radius: 3,  // 点的大小
                    fillColor: '#FFFFFF' // 设置点中间填充的颜色
                },
                shadow: false
                //threshold: null
            }
        },
        //series: [{
        //    data: [6.0, 5.9, 5.5, 4.5, 6.2, 6.5, 5.2, 6.0,
        //           5.9, 5.5, 4.5, 6.2, 6.5, 5.2, 6.0, 5.9,
        //           5.5, 4.5, 6.2, 6.5],
        //    pointStart: start_date_UTC_time,
        //    pointInterval: 1 * 24 * 3600 * 1000         // one day
        //}],
        title: {
            text: null
        },
        tooltip: {
            //formatter: function() {
            //    return '<span style="color:#969696;font-weight:bold;">' + Highcharts.dateFormat('%b %e', this.x) + '</span>' +'<br />' + '<span style="color:#464646;font-weight:bold;">' + this.y + 'mmol/L' + '</span>' + '<br />' + 'click for more info';
            //},
            // positioner: function (boxWidth, boxHeight, point) {
            //     return { x: point.plotX+80, y: point.plotY-20 };
            // },
            style: {
                padding: '7px'
            },
            borderColor: '#EAEAEA'
        },
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: {
                day: '%e/%m'
            },
            lineColor: '#CECECE',
            gridLineColor: '#EFECEF',
            gridLineWidth: 1,
            tickWidth: 0,
            labels:{
                step: 2,
                maxStaggerLines: 1
            },
            tickInterval: (4 * 24 * 3600 * 1000),       // 4 days
            tickColor: '#FFFFFF'
        },
        yAxis: {
            //title: {
            //    text: ''
            //},
            allowDecimals: false,
            endOnTick: false,
            tickInterval: 1,
            lineColor: '#CECECE',
            lineWidth: 2,
            gridLineColor: '#EFECEF',
            gridLineWidth: 1,
            minPadding: 0.3,
            maxPadding: 1.2
        }
    });
});
// }}}

$(document).ready(function(){
    var startDate = '2013-07-13';
    startDate = new Date(startDate.replace(/-/g,"/"));
    var start_date_UTC_time = startDate.getTime() - startDate.getTimezoneOffset() * 60 * 1000;
    var chart3 = new Highcharts.Chart({
        chart: {
            renderTo: 'chart_3'
        },
        yAxis: {
            title: {
                text: ''
            }
        },
        tooltip: {
            formatter: function() {
                return '<span style="color:#969696;font-weight:bold;">' + Highcharts.dateFormat('%b %e', this.x) + '</span>' +'<br />' + '<span style="color:#464646;font-weight:bold;">' + this.y + 'mmol/L' + '</span>' + '<br />' + 'click for more info';
            }
            // positioner: function (boxWidth, boxHeight, point) {
            //     return { x: point.plotX+80, y: point.plotY-20 };
            // },
        },
        series: [{
            data: [6.0, 5.9, 5.5, 4.5, 6.2, 6.5, 5.2, 6.0, 5.9, 5.5, 4.5, 6.2, 6.5, 5.2, 6.0, 5.9, 5.5, 4.5, 6.2, 6.5],
            pointStart: start_date_UTC_time,
            pointInterval:1 * 24 * 3600 * 1000
        }]
    });

    detail_chart = new Highcharts.Chart({
        chart: {
            renderTo: 'detail_chart',
            type: 'area',
            marginLeft: 25,
            width: 562,
            height: 303,
            spacingTop: 10,
            spacingBottom: 0,
            overflow: false,
            zIndex: 5
        },
        credits: {
            enabled: false
        },
        title: {
            text: ' '
        },
        colors: ['#31B6AD'],
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: {
                day: '%e/%m'  
            },
            lineColor: '#CECECE',
            gridLineColor: '#EFECEF',
            gridLineWidth: 1,
            tickWidth: 0,
            labels:{
                step: 2
            },
            tickInterval: (2 * 24 * 3600 * 1000),
            tickColor: '#FFFFFF'
        },
        yAxis: {
            title: {
                text: ''
            },
            allowDecimals: true,
            endOnTick: false,
            tickInterval: 0.5,
            lineColor: '#CECECE',
            lineWidth: 2,
            gridLineColor: '#EFECEF',
            gridLineWidth: 1,
            minPadding: 0.3,
            maxPadding: 1.2,
            labels: {
                formatter: function() {
                    var originYValue = this.value+'';
                    if (originYValue.length == 1){
                        originYValue += '.0';
                    }
                    return originYValue;
                }
            }
        },
        legend: {
            enabled: false
        },
        tooltip: {
            formatter: function() {
                return '<span style="color:#969696;font-weight:bold;">' + Highcharts.dateFormat('%b %e', this.x) + '</span>' +'<br />' + '<span style="color:#464646;font-weight:bold;">' + this.y + 'mmol/L' + '</span>' + '<br />' + 'click for more info';
            },
            // positioner: function (boxWidth, boxHeight, point) {
            //     return { x: point.plotX+80, y: point.plotY-20 };
            // },
            style: {
                padding: '7px'
            },
            borderColor: '#EAEAEA'
        },
        plotOptions: {
            series: {
                marker: {
                    enabled: true, //false false的时候就不会突出显示点 
                    lineColor: '#31B6AD',  
                    lineWidth: 1,
                    radius: 3,  // 点的大小  
                    fillColor: '#FFFFFF', // 设置点中间填充的颜色
                    symbol: 'circle'
                },
                fillOpacity: 0.12,
                lineWidth: 1,
                threshold: null,
                shadow: false,
                point: {
                    events: {
                        click: function() {
                            alert(this.x);
                            alert(this.y);
                            TB_show(false, indicator_url + 'popup/edithistorydata?TB_iframe=true&no1_title&transfer_params&height=351&width=630&card_id=3', false);
                        }
                    }
                }
            }
        },
        series: []
    });

    //详细历史记录
    $(".detail_history").bind("click", function(){
        card_detail_id = $(this).closest(".index_card").attr("id").replace('index_card_', '');
        var startDateLog = '2013-08-04';
        var endDateLog = '2013-08-10';
        var date = new Date();
        var time = date.getTime();
        redraw_chart(detail_chart, startDateLog, endDateLog);
        $(".act_card_container").addClass("move_div_2_left");
        return false;
    });

    //切换日期
    $(".shift_week").bind("click", function(){
        $(".shift_week").addClass("unselected");
        $(this).removeClass("unselected");
        var startDateLog = $(this).attr("start_date");
        var endDateLog = $(this).attr("end_date");
        redraw_chart(detail_chart, startDateLog, endDateLog);
        return false;
    });

    //根据日期搜索
    $("#search_start_date, #search_end_date").bind("change", function(){
        var startDateLog = $("#search_start_date").val();
        var endDateLog = $("#search_end_date").val();
        redraw_chart(detail_chart, startDateLog, endDateLog);
        return false;
    });

    //浏览更多
    $(".see_more_btn").bind("click", function(){
        var btn = $(".see_more_btn");
        var end = "2013-08-10";
        get_card_data_table(null, end, false);
        return false;
    });

    //收起历史记录
    $(".collapse_btn").bind("click", function(){
        //删除图表数据
        var serieses = detail_chart.series;
        for (series_key in serieses){
            serieses[series_key].remove();
        }
        //删除表格数据
        $("tr").not(".first_line").remove();
        //隐藏div
        $(".detail_card_info").hide();
        //初始化详细卡片id
        card_detail_id = 0;
        //添加删除div位置初始化
        $(".act_card_container").removeClass("move_div_2_left");
        return false;
    });
});

//重画历史记录图表
function redraw_chart(detail_chart, start, end){
    var date = new Date();
    var time = date.getTime();
    $.ajax({
        type: 'get',
        url: indicator_url + 'ajax/get_card_data_chart',
        data: 'card_detail_id='+card_detail_id+'&start='+start+'&end='+end+'&time='+time,
        dataType: 'json',
        success: function(dataJson) {
            //每一天都要有数据，否则x轴刻度时间对不上
            var startDateLogFormat = new Date(start.replace(/-/g,"/"));
            var start_date_log_UTC_time = startDateLogFormat.getTime() - startDateLogFormat.getTimezoneOffset() * 60 * 1000;
            var pointStart = start_date_log_UTC_time;
            var pointInterval = 1 * 24 * 3600 * 1000;

            //设置默认起始结束时间
            $("#search_start_date").datepicker( "setDate", start);
            $("#search_end_date").datepicker( "setDate", end);

            //删除chart已有数据
            var serieses = detail_chart.series;
            for (series_key in serieses){
                serieses[series_key].remove();
            }
            //更新chart数据
            detail_chart.addSeries({
                data: dataJson,
                pointStart: start_date_log_UTC_time,
                pointInterval: pointInterval
            });
            //更新table数据
            get_card_data_table(start, end, true);
            //显示
            $(".detail_card_info").show();
        }
    });
}

function get_card_data_table(start, end, redraw){
    var date = new Date();
    var time = date.getTime();
    $.ajax({
        type: 'get',
        url: indicator_url + 'ajax/get_card_data_table',
        data: 'card_detail_id='+card_detail_id+'&start='+start+'&end='+end+'&time='+time,
        success: function(data){
            if(redraw){
                $("tr").not(".first_line").remove();
            }
            $("table").append(data);
        }
    });
}

// vim: set ts=8 sw=4 tw=0 fenc=utf-8 ft=javascript: //
