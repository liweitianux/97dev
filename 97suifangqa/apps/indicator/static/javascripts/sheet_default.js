var now_js = new Date();
// require 'moment.js'
var curr_moment = moment();
var today_str = curr_moment.format('YYYY-MM-DD');
// global var to store the data of record
var record_data = {
    id: null,
    date: null,
    value: null,
    val_min: null,
    val_max: null,
};

$(document).ready(function(){
    // login control kit
    $(".drop-down-area").bind("click", function(){
        var drop_down_menu = $(".drop-down-menu");
        if(drop_down_menu.hasClass("open")){
            drop_down_menu.removeClass("open");
        }else{
            drop_down_menu.addClass("open");
        }
        return false;
    });
    $("body").bind("click", function(){
        $(".drop-down-menu").removeClass("open");
    });

    // recommended indicators
    $("#index_status_container .recommended").each(function() {
        var this_card = $(this);
        var id = this_card.attr("id").replace('index_card_', '');
        var qtip_title = '<strong>为您推荐的指标</strong>';
        var qtip_help = '若不需要，可以点击卡片右上角的 &times; 关闭';
        this_card.qtip({
            id: 'card_help'+id,
            prerender: false,
            content: {
                text: qtip_help,
                title: qtip_title,
                button: true
            },
            position: {
                my: 'bottom left',
                at: 'top center',
                target: this_card.find('.card_title')
            },
            show: {
                event: false
            },
            hide: {
                event: false
            },
            style: {
                classes: 'qtip-sf'
            }
        });
        this_card.qtip('api').show();
    });

    //不允许input框复制，减少验证粘帖的交互
    // $("input[type='text']").bind("paste", function(){
    //     return false;
    // });

    //副标题点大叉
    $("#index_title_closed_icon").bind("click", function(){
        var closeBtn = $(this);
        var date = new Date();
        var time = date.getTime();
        $.ajax({  //数据库还是cookie，都可以，建议使用cookie，html中是否显示sub_title也由后端读取的cookie决定
            type: 'get',
            url: indicator_url + 'ajax/close_sub_title',
            data: 'time='+time,
            success: function(data){
                if(data == 'success'){
                    closeBtn.parent().remove();
                }
            }
        });

        return false;
    });

    //卡片大叉删除交互
    $(".card_delete_icon").hover(
        function(){
            $(this).removeClass("card_delete");
            $(this).addClass("card_delete_hover");
        },
        function(){
            $(this).removeClass("card_delete_hover");
            $(this).addClass("card_delete");
        }
    );
    $(".card_delete_icon").bind("click", function(){
        card_2_delete_id = $(this).parent().attr("id").replace('index_card_', '');
    });

    //点击编辑icon(small) || click 'edit_icon'(big)
    $(".small_edit_icon, .edit_icon").bind("click", function(){
        var this_card = $(this).closest(".index_card");
        var this_edit_data_div = this_card.find(".edit_data");
        var this_editing_data_div = this_edit_data_div.siblings(".editing_data");
        var this_edit_icon_container_div = this_edit_data_div.siblings(".edit_icon_container");
        this_edit_data_div.hide();
        this_edit_icon_container_div.hide();
        this_editing_data_div.show();
        return false;
    });

    //点击取消icon
    $(".cancel_edit_icon").bind("click", function(){
        var id = $(this).closest(".index_card").attr("id").replace('index_card_', '');
        var this_editing_data_div = $(this).parent();
        var this_edit_data_div = this_editing_data_div.siblings(".edit_data");
        var this_edit_icon_container_div = this_editing_data_div.siblings(".edit_icon_container");
        this_editing_data_div.hide();
        this_edit_data_div.show();
        if (recordempty['id'+id]) {
            // record empty
            this_edit_icon_container_div.show();
        }
        return false;
    });

    // initialize
    // empty data input
    $(".data_input").val('');
    // unselect radio buttons
    if ($(".editing_data .radio_input").length) {
        $(".radio_input input:radio").prop("checked", false);
    }

    // validate data and qtip2 {{{
    $(".index_card").each(function() {
        var this_card = $(this);
        var id = this_card.attr("id").replace('index_card_', '');
        var data_type = datatypes['id'+id];
        //console.log("id: "+id+"; data_type: "+data_type);
        var confine = confines['id'+id];

        // data {{{
        if (data_type == DATA_TYPES_JS.INTEGER_TYPE) {
            // INTEGER_TYPE
            // TODO
        }
        else if (data_type == DATA_TYPES_JS.FLOAT_TYPE) {       // {{{
            // FLOAT_TYPE
            var datainput_help = '<p>定值型</p><p>数据格式示例：123.7; 1.23e4; 3.5e-2</p>';
            // tooltip
            $(this).find(".data_input").qtip({
                id: 'datainput_'+id,
                prerender: false,
                content: {
                    text: datainput_help
                },
                position: {
                    my: 'bottom left',
                    at: 'top right'
                },
                show: {
                    event: 'mouseenter'
                },
                hide: {
                    event: 'mouseleave unfocus'
                }
            });
            this_card.find(".data_input").focus(function() {
                $(this).removeClass("valid invalid");
            });
            // validate
            this_card.find(".data_input").on('validate', null, function() {
                var value_str = $(this).val();
                var value = is_float(value_str);
                if (value === false) {
                    // format invalid
                    $(this).removeClass("valid");
                    $(this).addClass("invalid");
                    var qtip_content = '<p>数据格式不符合要求，请检查后重新输入</p>';
                    $(this).qtip('api').set('content.text', qtip_content);
                    $(this).qtip('api').show();
                }
                else {
                    // format valid
                    // check confine
                    if (value >= confine.math_min &&
                            value <= confine.math_max) {
                        // confine valid
                        $(this).removeClass("invalid");
                        $(this).addClass("valid");
                        var qtip_content = datainput_help;
                        $(this).qtip('api').set('content.text', qtip_content);
                        $(this).qtip('api').hide();
                        // update data
                        record_data.value = value;
                    }
                    else {
                        // confine tooltip
                        $(this).removeClass("valid");
                        $(this).addClass("invalid");
                        var qtip_content = '<p>数值超出范围</p><p>允许数据范围：'+confine.math_range_html+' </p>';
                        $(this).qtip('api').set('content.text',
                                qtip_content);
                        $(this).qtip('api').show();
                    }
                }
            });
            this_card.find(".data_input").on('blur', null, function() {
                $(this).trigger('validate');
            });
        } // }}}
        else if (data_type == DATA_TYPES_JS.RANGE_TYPE) {       // {{{
            // RANGE_TYPE
            var datainput_help = '<p>范围型</p><p>数据格式示例：&bullet; <123.7; &bullet; >1.3e3; &bullet; 1.5e3 ~ 3.7e3</p>';
            // tooltip
            this_card.find(".data_input").qtip({
                id: 'datainput_'+id,
                prerender: false,
                content: {
                    text: datainput_help
                },
                position: {
                    my: 'bottom left',
                    at: 'top right'
                },
                show: {
                    event: 'mouseenter'
                },
                hide: {
                    event: 'mouseleave unfocus'
                }
            });
            this_card.find(".data_input").focus(function() {
                $(this).removeClass("valid invalid");
            });
            // validate
            this_card.find(".data_input").on('validate', null, function() {
                var value_str = $(this).val();
                var value = is_range(value_str);
                if (is_range(value_str) === false) {
                    // format invalid
                    $(this).removeClass("valid");
                    $(this).addClass("invalid");
                    var qtip_content = '<p>数据格式不符合要求，请检查后重新输入</p>';
                    $(this).qtip('api').set('content.text', qtip_content);
                    $(this).qtip('api').show();
                }
                else {
                    // range format valid
                    // check if within 'confine'
                    var confine_valid = false;
                    var val_min = null;
                    var val_max = null;

                    var operator = value.operator;
                    if (operator === '<') {
                        val_max = value.value;
                        if (val_max > confine.math_min &&
                                val_max <= confine.math_max) {
                            // valid
                            confine_valid = true;
                            val_min = confine.math_min;
                        }
                    }
                    else if (operator === '>') {
                        val_min = value.value;
                        if (val_min >= confine.math_min &&
                                val_min < confine.math_max) {
                            // valid
                            confine_valid = true;
                            val_max = confine.math_max;
                        }
                    }
                    else if (operator === '~') {
                        val_min = value.val_min;
                        val_max = value.val_max;
                        if (val_min >= confine.math_min &&
                                val_max < confine.math_max) {
                            // valid
                            confine_valid = true;
                        }
                    }
                    else {
                        confine_valid = false;
                    }

                    if (confine_valid === true) {
                        $(this).removeClass("invalid");
                        $(this).addClass("valid");
                        var qtip_content = datainput_help;
                        $(this).qtip('api').set('content.text',
                                qtip_content);
                        $(this).qtip('api').hide();
                        // update data
                        record_data.val_min = val_min;
                        record_data.val_max = val_max;
                    }
                    else {
                        // data not within range
                        $(this).removeClass("valid");
                        $(this).addClass("invalid");
                        var qtip_content = '<p>数值超出范围</p><p>允许数据范围：'+confine.math_range_html+' </p>';
                        $(this).qtip('api').set('content.text',
                                qtip_content);
                        $(this).qtip('api').show();
                    }
                }
            });
            this_card.find(".data_input").on('blur', null, function() {
                $(this).trigger('validate');
            });
        } // RANGE_TYPE }}}
        else if (data_type == DATA_TYPES_JS.FLOAT_RANGE_TYPE) {
            // TODO
        }
        else if (data_type == DATA_TYPES_JS.PM_TYPE) {          // {{{
            // TODO
            var radioinput_help = '<p>请直接点击选择</p>';
            // tooltip
            this_card.find(".radio_input").qtip({
                id: 'radioinput_'+id,
                prerender: false,
                content: {
                    text: radioinput_help
                },
                position: {
                    my: 'bottom left',
                    at: 'top right'
                },
                show: {
                    event: 'mouseenter'
                },
                hide: {
                    event: 'mouseleave unfocus'
                }
            });
            // validate
            this_card.find(".radio_input").on('validate', null, function() {
                if (this_card.find(".radio_input input:radio:checked").length != 1) {
                    var qtip_content = '<p>请选择化验结果</p>';
                    $(this).qtip('api').set('content.text',
                        qtip_content);
                    $(this).qtip('api').show();
                }
                else {
                    // valid
                    var qtip_content = radioinput_help;
                    $(this).qtip('api').set('content.text',
                        qtip_content);
                    $(this).qtip('api').hide();
                    // update data
                    record_data.value = this_card.find(".radio_input input:radio:checked").val();
                }
            });
        } // }}}
        else {
            // unknown
            return false;
        }
        // }}}

        // date {{{
        // date_input tooltip
        var dateinput_help = '<p>日期格式：YYYY-MM-DD; 如：2013-08-26</p><p>日期不能晚于<strong>今天</strong></p>';
        this_card.find(".date_input").qtip({
            id: 'dateinput_'+id,
            prerender: false,
            content: {
                text: dateinput_help
            },
            position: {
                my: 'left top',
                at: 'right bottom'
            },
            show: {
                event: 'mouseenter'
            },
            hide: {
                event: 'mouseleave unfocus'
            }
        });
        this_card.find(".date_input").focus(function() {
            $(this).removeClass("valid invalid");
            // show help tooltip
            //var qtip_content = dateinput_help;
            //$(this).qtip('api').set('content.text', qtip_content);
            //$(this).qtip('api').show();
        });
        // validate
        this_card.find(".date_input").on('validate', null, function() {
            var date_str = $(this).val();
            var date_mm = moment(date_str, 'YYYY-MM-DD');
            var today_mm = moment();
            //console.log('date_str: ', date_str);
            // date cannot beyond today
            if (date_mm.isValid() && !date_mm.isAfter(today_mm)) {
                $(this).removeClass("invalid");
                $(this).addClass("valid");
                var qtip_content = dateinput_help;
                $(this).qtip('api').set('content.text', qtip_content);
                $(this).qtip('api').hide();
                // update data
                record_data.date = date_str;
            }
            else {
                // date invalid
                $(this).removeClass("valid");
                $(this).addClass("invalid");
                var qtip_content = '<p>请检查输入日期的格式，并且日期不能晚于<strong>今天</strong></p>';
                $(this).qtip('api').set('content.text', qtip_content);
                $(this).qtip('api').show();
            }
        });
        this_card.find(".date_input").on('change blur', null, function() {
            $(this).trigger('validate');
        });
        // }}}
    });
    // }}}

    //点击提交icon
    $(".confirm_edit_icon").bind("click", function(){
        var this_editing_data_div = $(this).closest(".editing_data");
        var card = $(this).closest(".index_card");
        var id = card.attr("id").replace('index_card_', '');
        // validate data before submit
        this_editing_data_div.find(".to_validate").trigger('validate');
        if (this_editing_data_div.find(".invalid").length) {
            // XXX: tooltip/popup
            return false;
        }

        // submit data (AJAX) {{{
        var time = moment().valueOf();
        $.ajax({
            type: 'post',
            url: indicator_url + 'ajax/add_record/',
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                indicator_id: id,
                date: record_data.date,
                value: record_data.value,
                val_min: record_data.val_min,
                val_max: record_data.val_max,
                time: time
            },
            dataType: 'json',
            success: function(dataJson) {
                if (dataJson.failed == true) {
                    // failed: tooltip
                    if (dataJson.error_code === 20) {
                        // 'record_exist'; given date has record
                        var date_input = card.find(".date_input");
                        date_input.removeClass("valid");
                        date_input.addClass("invalid");
                        var qtip_content = '<p>该日期已存在记录，请检查</p>';
                        date_input.qtip('api').set('content.text', qtip_content);
                        date_input.qtip('api').show();
                    }
                    else {
                        // XXX: other error
                        var data_input = card.find(".data_input");
                        data_input.removeClass("valid");
                        data_input.addClass("invalid");
                        var qtip_content = '<p>输入记录不符合要求，请检查</p>';
                        data_input.qtip('api').set('content.text', qtip_content);
                        data_input.qtip('api').show();
                    }
                }
                else {
                    // successfully added record
                    // remove 'record_empty' class
                    card.removeClass("record_empty");
                    var this_edit_data_div = this_editing_data_div.siblings(".edit_data");
                    this_editing_data_div.hide();
                    this_edit_data_div.show();
                    // last_edit_data & last_edit_date (std_unit)
                    var this_last_edit_data_div = this_edit_data_div.find(".last_edit_data");
                    var this_last_edit_date_div = this_edit_data_div.find(".last_edit_date");
                    this_last_edit_data_div.children(".data_value").html(dataJson.value_html);
                    this_last_edit_date_div.children(".date_value").html(dataJson.date);
                    this_last_edit_data_div.show();
                    this_last_edit_date_div.show();
                    // explain_icon
                    this_edit_data_div.find(".nodata_icon").hide();
                    this_edit_data_div.find(".lastdata_icon").show();
                    // refresh_icon
                    this_edit_data_div.find(".refresh_icon").show();
                    // edit_icon_container & chart
                    this_editing_data_div.siblings(".edit_icon_container").hide();
                    this_editing_data_div.siblings(".chart").show();
                }
            }
        });
        // }}}

        return false;
    });

    //日期控件
    $(".datepicker_container>.datepicker").datepicker({
        showOn: "both",
        buttonImage: static_url + "images/calendar.png",
        buttonImageOnly: true,
        maxDate: now_js
    });
    $(".datepicker_container>.datepicker").datepicker("setDate", now_js);

    //时间范围控制（开始时间<结束时间）
    $("#search_begin_date").datepicker({
        showOn: "both",
        buttonImage: static_url + "images/calendar.png",
        buttonImageOnly: true,
        onClose: function( selectedDate ) {
            $("#search_end_date").datepicker("option", "minDate", selectedDate);
        }
    });
    $("#search_end_date").datepicker({
        showOn: "both",
        buttonImage: static_url + "images/calendar.png",
        buttonImageOnly: true,
        onClose: function( selectedDate ) {
            $("#search_begin_date").datepicker("option", "maxDate", selectedDate);
        }
    });
});

//
function delete_card(){
    var card = $("#index_card_"+card_2_delete_id);
    card.nextAll().each(function(){
        if($(this).hasClass("index_card_fir")){
            $(this).removeClass("index_card_fir");
            $(this).addClass("index_card_sec");
        }else if($(this).hasClass("index_card_sec")){
            $(this).removeClass("index_card_sec");
            $(this).addClass("index_card_fir");
        }
    });
    card.remove();
}

// check if a string is float number                        // {{{
function is_float(str) {
    // regex for fixed notation float number
    var fix_regex = /^([+-]?)(\d+|\d+(\.\d*)?|\d*\.\d+)$/;
    // regex for exponential notation float number
    var exp_regex = /^([+-]?)(\d+|\d+(\.\d*)?|\d*\.\d+)[eE]([+-]?)\d+$/;;

    str = str || "";
    var str_orig = str;
    //console.log('str_orig: "'+str_orig+'"');
    // remove the blank on the head and tail
    str = str.replace(/(^\s*|\s*$)/g, '');
    // remove blank between sign and number
    str = str.replace(/^([+-]?)\s*/, '$1');
    //console.log('str: "'+str+'"');
    // valid str can only contains '[\d.]', '[+-]?', and '[eE]?'
    if (fix_regex.test(str) || exp_regex.test(str)) {
        // true
        return parseFloat(str);
    }
    else {
        return false;
    }
}
// }}}

// check if a string is valid range
// a) '< num'; b) '> num'; c) 'low ~ high' (range_symbol)   // {{{
function is_range(str) {
    if (typeof range_symbol === 'undefined') {
        range_symbol = '~';
    }
    str = str || "";
    var str_orig = str;

    str = str.replace(/(^\s*|\s*$)/g, '');
    var operator = str.charAt(0);
    if (operator === '<' || operator === '>') {
        // strip the first char
        str = str.replace(/^./, '');
        var value = is_float(str);
        if (value === false) {
            return false;
        }
        else {
            return {'operator': operator, 'value': value};
        }
    }
    else {
        // not case 'a)' & 'b)'
        var str_splited = str.split(range_symbol);
        if (str_splited.length == 2) {
            var val_min = is_float(str_splited[0]);
            var val_max = is_float(str_splited[1]);
            if (val_min !== false && val_max !== false
                    && val_min < val_max) {
                // valid
                operator = range_symbol;
                return {'operator': operator,
                        'val_min': val_min,
                        'val_max': val_max };
            }
            else {
                return false;
            }
        }
        else {
            // invalid
            return false
        }
    }
}
// }}}

// vim: set ts=4 sw=4 tw=0 fenc=utf-8 ft=javascript: //
