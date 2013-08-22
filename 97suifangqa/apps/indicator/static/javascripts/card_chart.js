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
                lineWidth: 2,
                marker: {
                    enabled: true, // false的时候就不会突出显示点
                    lineColor: '#31B6AD',
                    lineWidth: 2,
                    radius: 4,  // 点的大小
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
            lineWidth: 2,
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
        // update global var 'detail_chart_options_str'
        detail_chart_options_str = 'options_chart_' + detail_card_id;
        // clickable data point
        window[detail_chart_options_str].plotOptions = {
            series: {
                cursor: 'pointer',
                point: {
                    events: {
                        click: function(event) {
                            //console.log(event);
                            //console.log(this);
                            var date = moment(this.x).utc().format('YYYY-MM-DD');
                            TB_show(false, indicator_url+'popup/edithistorydata?card_id='+detail_card_id+'&date='+date+'&no_title=true&TB_iframe=true&height=351&width=630', false);
                        }
                    }
                }
            }
        };
        var getdata_type = "num";
        var getdata_num = 10;
        detail_chart_getdata_draw(detail_chart_str,
            detail_chart_options_str,
            getdata_type, getdata_num,
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
        var end_date = $(this).attr("end_date");
        // add 2 days to 'end_str'
        // otherwise xAxis maybe incomplete to show the last data point
        var end_mm = moment(end_date);
        end_mm.add('days', 2);
        var end_str = end_mm.format('YYYY-MM-DD');
        var getdata_type = "date";
        var getdata_num = null;
        detail_chart_getdata_draw(detail_chart_str,
            detail_chart_options_str,
            getdata_type, getdata_num,
            begin_str, end_str
        );
        return false;
    });

    //根据日期搜索
    $("#search_begin_date, #search_end_date").bind("change", function(){
        $(".shift_date").addClass("unselected");
        var begin_str = $("#search_begin_date").val();
        var end_date = $("#search_end_date").val();
        // add 2 days to 'end_str'
        // otherwise xAxis maybe incomplete to show the last data point
        var end_mm = moment(end_date);
        end_mm.add('days', 2);
        var end_str = end_mm.format('YYYY-MM-DD');
        var getdata_type = "date";
        var getdata_num = null;
        detail_chart_getdata_draw(detail_chart_str,
            detail_chart_options_str,
            getdata_type, getdata_num,
            begin_str, end_str
        );
        return false;
    });

    //浏览更多
    $(".see_more_btn").bind("click", function(){
        // get the 'begin_date' of existing data
        // used as the 'end_date' to request earlier data
        var begin_orig = $("#detail_card_table tr:last .date").text();
        var end_date = moment(begin_orig);
        end_date.subtract('days', 1);
        var end_str = end_date.format('YYYY-MM-DD');
        var getdata_type = "num";
        var getdata_num = 10;
        get_card_data_table(getdata_type, getdata_num,
                null, end_str, true);
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

// destroy the original chart and new.
// chart_str: (string),
//   name of global var of chart to draw;
//   and the div id to contain the chart.
// options_str: (string),
//   name of global var of the chart options for drawing,
//   used to draw the detail chart by updating its data.
// begin, end: (string), 'YYYY-MM-DD'
// type: "num" | "date"
function detail_chart_getdata_draw(chart_str, options_str, type, num, begin, end) {
    var type2 = type || "num";   // default get data by 'num'
    var num2 = num || "";
    var begin2 = begin || "";
    var end2 = end || "";
    var time = moment().valueOf();
    $.ajax({
        type: 'get',
        url: indicator_url + 'ajax/get_card_data_chart',
        data: 'card_id='+detail_card_id + '&type='+type2 + '&num='+num2 + '&begin='+begin2 + '&end='+end2 + '&time='+time,
        dataType: 'json',
        success: function(dataJson) {
            // show detail card
            $(".detail_card_info").show();

            // update detail table data
            get_card_data_table(type, num, begin, end, false);

            //console.log(dataJson);
            if (dataJson.failed || dataJson.number_rsp == 0) {
                // getdata failed or get no data
                return false;
            }
            else {
                var begin_dt = moment(dataJson.begin_rsp);
                var end_dt = moment(dataJson.end_rsp);
                if (dataJson.number_rsp == 1) {
                    // only one data point
                    // (3days) dp_date (4days)
                    begin_dt.subtract('days', 3);
                    end_dt.add('days', 4);
                }
                else {
                    var diff_days = end_dt.diff(begin_dt, 'days');
                    var days_toadd = Math.floor(diff_days*0.10) + 1;
                    end_dt.add('days', days_toadd);
                }
                // type == "date"
                if (type == "date") {
                    // use date of request instead
                    begin_dt = moment(dataJson.begin_req);
                    end_dt = moment(dataJson.end_req);
                }

                // update datepicker
                var begin_date_js = $.datepicker.parseDate('yy-mm-dd',
                        begin_dt.format('YYYY-MM-DD'));
                var end_date_js = $.datepicker.parseDate('yy-mm-dd',
                        end_dt.format('YYYY-MM-DD'));
                $("#search_begin_date").datepicker("setDate",
                        begin_date_js);
                $("#search_end_date").datepicker("setDate",
                        end_date_js);

                // set chart data
                window[options_str].chart.renderTo = chart_str;
                window[options_str].xAxis.min = begin_dt.valueOf();
                window[options_str].xAxis.max = end_dt.valueOf();
                window[options_str].series[0].data = dataJson.data;
                // destroy original chart and
                // redraw with new options and data
                if (window[chart_str] != null) {
                    window[chart_str].destroy();
                    window[chart_str] = null;
                }
                window[chart_str] = new Highcharts.Chart(window[options_str]);
            }
        }
    });
}

// get data for detail card table
// if append=true, then keep original data,
// otherwise, replace original data with new data
function get_card_data_table(type, num, begin, end, append){
    var type2 = type || "num";   // default get data by 'num'
    var num2 = num || "";
    var begin2 = begin || "";
    var end2 = end || "";
    var time = moment().valueOf();
    $.ajax({
        type: 'get',
        url: indicator_url + 'ajax/get_card_data_table',
        data: 'card_id='+detail_card_id + '&type='+type2 + '&num='+num2 + '&begin='+begin2 + '&end='+end2 + '&time='+time,
        dataType: 'json',
        success: function(dataJson) {
            if (dataJson.failed || dataJson.number_rsp == 0) {
                // getdata failed or get no data
                return false;
            }
            // process data
            // 'tr' format:
            //   <tr id="record_#">
            //     <td class="date">"date"</td>
            //     <td class="record">"record (unit)"</td>
            //     <td class="state">"state"</td>
            //   </tr>
            var data_html = "";
            for (var i=0; i<dataJson.data.length; i++) {
                var r = dataJson.data[i];
                if (r.std_unit_symbol) {
                    var unit_str = ' (' + r.std_unit_symbol + ')';
                }
                else {
                    var unit_str = "";
                }
                var record_html = r.value_html + unit_str;
                if (r.is_normal == true) {
                    var state = '正常';
                }
                else if (r.is_normal == false) {
                    var state = '不正常';
                }
                else {
                    var state = '未知';
                }
                // tr_html
                var tr_html = '<tr id="record_' + r.id + '">';
                tr_html += '<td class="date">' + r.date + '</td>';
                tr_html += '<td class="record">' + record_html + '</td>';
                tr_html += '<td class="state">' + state + '</td>';
                tr_html += '</tr>';
                //console.log('tr_html: ', tr_html);
                data_html += tr_html + '\n';
            }
            // update table
            if (! append) {
                $("#detail_card_table tr").not(".first_line").remove();
                // reset to enable button
                $(".see_more_btn").removeAttr('disabled');
            }
            //console.log('data_html: ', data_html);
            $("#detail_card_table").append(data_html);
            // disable button if has no more data
            if (! dataJson.has_earlier) {
                $(".see_more_btn").attr('disabled', 'disabled');
            }
        }
    });
}

// vim: set ts=8 sw=4 tw=0 fenc=utf-8 ft=javascript: //
