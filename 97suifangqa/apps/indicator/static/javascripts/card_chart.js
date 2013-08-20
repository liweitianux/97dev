// set global options for hightcharts {{{
$(function() {
    Highcharts.setOptions ({
        //chart: {
        //    type: 'areaspline'
        //    //marginLeft: 25,
        //    //height: 223,
        //    //spacingTop: 10,
        //    //spacingBottom: 4
        //    //overflow: false,
        //    //zIndex: 5
        //},
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
        title: {
            text: null
        },
        tooltip: {
            useHTML: true,
            style: {
                padding: '7px'
            },
            borderColor: '#EAEAEA'
        },
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: {
                day: '%m-%e',
                month: '%Y-%m'
            },
            lineColor: '#CECECE',
            gridLineColor: '#EFECEF',
            gridLineWidth: 1,
            tickWidth: 0,
            labels: {
                step: 2,
                maxStaggerLines: 1
            },
            startOnTick: false,
            endOnTick: false,
            //tickInterval: (7 * 24 * 3600 * 1000),       // 7 days
            tickInterval: null,
            tickPixelInterval: 50,
            tickColor: '#FFFFFF'
        },
        yAxis: {
            title: {
                text: null
            },
            min: null,
            max: null,
            //allowDecimals: false,
            startOnTick: false,
            endOnTick: false,
            tickInterval: null,
            tickPixelInterval: 40,
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
    //详细历史记录
    $(".detail_history").bind("click", function(){
        // update 'detail_card_id'
        detail_card_id = $(this).closest(".index_card").attr("id").replace('index_card_', '');
        // check if this card has data
        // if has no data, then exists div class="edit_icon_container"
        if ($("#index_card_"+detail_card_id + " .edit_icon_container").length) {
            $(".detail_card_info").hide();
            return false;
        }
        // get the index title and set for the 'detail card'
        var index_title = $("#index_card_"+detail_card_id + " .card_title").html();
        $(".detail_card_info .card_title .title").html(index_title);
        // set date for the 'shift_date' buttons
        var date_fmt = 'YYYY-MM-DD';
        var today_mm = moment();
        var today_str = today_mm.format(date_fmt);
        var three_month_ago_str = today_mm.clone().subtract('months', 3).format(date_fmt);
        var six_month_ago_str = today_mm.clone().subtract('months', 6).format(date_fmt);
        $(".recent_three_month").attr('end_date', today_str);
        $(".recent_three_month").attr('begin_date', three_month_ago_str);
        $(".recent_six_month").attr('end_date', today_str);
        $(".recent_six_month").attr('begin_date', six_month_ago_str);
        // draw chart
        // pass default global var 'begin_date_str' and 'end_date_str'
        // detail_chart global var: 'detail_chart'
        // options for chart global var: 'options_chart_<id>'
        // update global var 'detail_chart_options'
        detail_chart_options = 'options_chart_' + detail_card_id;
        redraw_chart(detail_chart_str, detail_chart_options,
            begin_date_str, end_date_str
        );
        $(".act_card_container").addClass("move_div_2_left");
        return false;
    });

    //切换日期
    $(".shift_date").bind("click", function(){
        $(".shift_date").addClass("unselected");
        $(this).removeClass("unselected");
        var begin_str = $(this).attr("begin_date");
        var end_str = $(this).attr("end_date");
        redraw_chart(detail_chart_str, detail_chart_options,
            begin_str, end_str
        );
        return false;
    });

    //根据日期搜索
    $("#search_begin_date, #search_end_date").bind("change", function(){
        $(".shift_date").addClass("unselected");
        var begin_str = $("#search_begin_date").val();
        var end_str = $("#search_end_date").val();
        redraw_chart(detail_chart_str, detail_chart_options,
            begin_str, end_str
        );
        return false;
    });

    //浏览更多
    $(".see_more_btn").bind("click", function(){
        var btn = $(".see_more_btn");
        var end_str = end_date_str;
        get_card_data_table(null, end_str, false);
        return false;
    });

    //收起历史记录
    $(".collapse_btn").bind("click", function(){
        // //删除图表数据
        // var serieses = detail_chart.series;
        // for (series_key in serieses){
        //     serieses[series_key].remove();
        // }
        //删除图表
        if (window[detail_chart_str] != null) {
            window[detail_chart_str].destroy();
            window[detail_chart_str] = null;
        }
        //删除表格数据
        $("tr").not(".first_line").remove();
        //隐藏div
        $(".detail_card_info").hide();
        //初始化详细卡片id
        detail_card_id = "-1";
        //添加删除div位置初始化
        $(".act_card_container").removeClass("move_div_2_left");
        return false;
    });
});

// 重画历史记录图表
// destroy the original chart and new.
// chart_str: (string),
//   name of global var of chart to draw;
//   and the div id to contain the chart.
// options_str: (string),
//   name of global var of the chart options for drawing,
//   used to draw the detail chart by updating its data.
// begin, end: (string), 'YYYY-MM-DD'
function redraw_chart(chart_str, options_str, begin, end){
    var time = moment().valueOf();
    $.ajax({
        type: 'get',
        url: indicator_url + 'ajax/get_card_data_chart',
        data: 'card_id='+detail_card_id + '&begin='+begin + '&end='+end + '&time='+time,
        dataType: 'json',
        success: function(dataJson) {
            // 设置默认起始结束时间
            //console.log(begin);
            //console.log(end);
            var begin_date_js = $.datepicker.parseDate('yy-mm-dd', begin);
            var end_date_js = $.datepicker.parseDate('yy-mm-dd', end);
            $("#search_begin_date").datepicker("setDate", begin_date_js);
            $("#search_end_date").datepicker("setDate", end_date_js);

            //显示
            $(".detail_card_info").show();

            //删除chart已有数据
            //var serieses = detail_chart.series;
            //for (series_key in serieses){
            //    serieses[series_key].remove();
            //}
            //更新chart数据
            //detail_chart.addSeries({
            //    data: dataJson,
            //    pointStart: begin_date_log_UTC_time,
            //    pointInterval: pointInterval
            //});

            // destroy original chart and
            // redraw with new options and data
            var begin_dt = moment(begin);
            var end_dt = moment(end);
            window[options_str].chart.renderTo = chart_str;
            window[options_str].xAxis.min = begin_dt.valueOf();
            window[options_str].xAxis.max = end_dt.valueOf();
            window[options_str].series[0].data = dataJson;
            // clickable data point
            window[options_str].plotOptions = {
                series: {
                    cursor: 'pointer',
                    point: {
                        events: {
                            click: function(event) {
                                //console.log(event);
                                //console.log(this);
                                var date = moment(this.x).utc().format('YYYY-MM-DD');
                                TB_show(false, indicator_url+'popup/edithistorydata?card_id='+detail_card_id+'&date='+date+'&TB_iframe=true&transfer_params&height=351&width=630', false);
                            }
                        }
                    }
                }
            }
            if (window[chart_str] != null) {
                window[chart_str].destroy();
                window[chart_str] = null;
            }
            window[chart_str] = new Highcharts.Chart(window[options_str]);

            //更新table数据
            //TODO
            get_card_data_table(begin, end, true);
        }
    });
}

function get_card_data_table(begin, end, redraw){
    var time = moment().valueOf();
    $.ajax({
        type: 'get',
        url: indicator_url + 'ajax/get_card_data_table',
        data: 'card_id='+detail_card_id + '&begin='+begin + '&end='+end + '&time='+time,
        success: function(data) {
            if(redraw){
                $("tr").not(".first_line").remove();
            }
            $("table").append(data);
        }
    });
}

// vim: set ts=8 sw=4 tw=0 fenc=utf-8 ft=javascript: //
