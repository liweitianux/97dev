// global var to store the data of record
var record_data = {
    date: null,
    value: null,
    val_min: null,
    val_max: null,
    reason: null
};

$(document).ready(function(){
    //点大叉，关闭弹层页面
    $(".edit_history_data_close").bind("click", function(){
        parent.TB_remove();
        return false;
    });
    // jquery-ui: datepicker
    $("#editing_date_picker").datepicker({
        showOn: "both",
        buttonImage: static_url + "images/calendar.png",
        buttonImageOnly: true,
        maxDate: 0      // 0->today, 1->tomorrow
    });

    // edit button
    $("#edit_btn").bind("click", function(){
        var this_edit_data_div = $(this).closest(".edit_data");
        var this_editing_data_div = this_edit_data_div.siblings(".editing_data");
        this_editing_data_div.show();
        this_edit_data_div.hide();
        return false;
    });

    // save botton {{{
    $("#save_btn").bind("click", function(){
        // force to trigger 'validate' before save
        $(".editing_data .to_validate").trigger('validate');
        if ($(".editing_data .invalid").length) {
            // TODO: tooltip/popup
            return false;
        }

        // modified data validated
        var cur_mm = moment();
        var created_at_str = cur_mm.toISOString();
        var time = cur_mm.valueOf();
        $.ajax({
            type: 'post',
            url: indicator_url + 'ajax/modify_record/',
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                record_id: record_id,
                date: record_data.date,
                value: record_data.value,
                val_min: record_data.val_min,
                val_max: record_data.val_max,
                reason: record_data.reason,
                created_at: created_at_str,
                time: time
            },
            dataType: 'json',
            success: function(dataJson) {
                if (dataJson.failed == true) {
                    // tooltip
                }
                else {
                    // successfully modified
                    parent.TB_remove();
                    // update the detail chart
                    //parent.redraw_chart(parent.detail_chart, "2013-08-04", "2013-08-10"); //这边需要穿过来起始，结束时间，以便刷新图表和表格
                }
            }
        });
        return false;
    });
    // }}}

    // initalize
    // set datepicker 'date_input' value
    var date_init = $.datepicker.parseDate('yy-mm-dd',
            $(".date_input").attr('value'));
    $(".date_input").datepicker("setDate", date_init);
    // select radio button according to the original value
    if ($(".editing_data .radio_input").length) {
        $(".radio_input input:radio").prop("checked", false);
    }
    if (record.value === '-') {
        $(".radio_input #minus_r").prop("checked", true);
    }
    else {
        $(".radio_input #plus_r").prop("checked", true);
    }

    // record data validate {{{
    // date {{{
    // date_input tooltip
    var dateinput_help = '<p>日期格式：YYYY-MM-DD; 如：2013-08-26</p><p>日期不能晚于<strong>今天</strong></p>';
    $(".date_input").qtip({
        id: 'dateinput',        // -> '#qtip-dateinput'
        prerender: false,
        content: {
            text: dateinput_help
        },
        position: {
            my: 'bottom left',
            at: 'top right'
        },
        show: {
            event: false
        },
        hide: {
            //event: 'click'
            event: false
        }
    });
    $(".date_input").focus(function() {
        $(this).removeClass("valid invalid");
        // show help tooltip
        var qtip_content = dateinput_help;
        $(this).qtip('api').set('content.text', qtip_content);
        $(this).qtip('api').show();
    });
    $(".date_input").on('validate', null, function() {
        var date_str = $(this).val();
        var date_mm = moment(date_str, 'YYYY-MM-DD');
        var today_mm = moment();
        //console.log('date_str: ', date_str);
        // date cannot beyond today
        if (date_mm.isValid() && !date_mm.isAfter(today_mm)) {
            $(this).removeClass("invalid");
            $(this).addClass("valid");
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
    $(".date_input").on('change blur', null, function() {
        $(this).trigger('validate');
    });
    // }}}

    // validate data
    if (data_type == DATA_TYPES.INTEGER_TYPE) {
        // INTEGER_TYPE
        // TODO
    }
    else if (data_type == DATA_TYPES.FLOAT_TYPE) {          // {{{
        // FLOAT_TYPE
        var datainput_help = '<p>定值型</p><p>数据格式示例：123.7; 1.23e4; 3.5e-2</p>';
        // tooltip
        $(".data_input").qtip({
            id: 'datainput',
            prerender: false,
            content: {
                text: datainput_help
            },
            position: {
                my: 'bottom left',
                at: 'top right'
            },
            show: {
                event: false
            },
            hide: {
                //event: 'click'
                event: false
            }
        });
        $(".data_input").focus(function() {
            $(this).removeClass("valid invalid");
            // show help tooltip
            var qtip_content = datainput_help;
            $(this).qtip('api').set('content.text', qtip_content);
            $(this).qtip('api').show();
        });
        // validate
        $(".data_input").on('validate', null, function() {
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
        $(".data_input").on('blur', null, function() {
            $(this).trigger('validate');
        });
    } // }}}
    else if (data_type == DATA_TYPES.RANGE_TYPE) {          // {{{
        // RANGE_TYPE
        var datainput_help = '<p>范围型</p><p>数据格式示例：&bullet; <123.7; &bullet; >1.3e3; &bullet; 1.5e3 ~ 3.7e3</p>';
        // tooltip
        $(".data_input").qtip({
            id: 'datainput',
            prerender: false,
            content: {
                text: datainput_help
            },
            position: {
                my: 'bottom left',
                at: 'top right'
            },
            show: {
                event: false
            },
            hide: {
                //event: 'click'
                event: false
            }
        });
        $(".data_input").focus(function() {
            $(this).removeClass("valid invalid");
            // show help tooltip
            var qtip_content = datainput_help;
            $(this).qtip('api').set('content.text', qtip_content);
            $(this).qtip('api').show();
        });
        // validate
        $(".data_input").on('validate', null, function() {
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
        $(".data_input").on('blur', null, function() {
            $(this).trigger('validate');
        });
    } // RANGE_TYPE }}}
    else if (data_type == DATA_TYPES.FLOAT_RANGE_TYPE) {
        // TODO
    }
    else if (data_type == DATA_TYPES.PM_TYPE) {             // {{{
        // TODO
        var radioinput_help = '<p>请直接点击选择</p>';
        // tooltip
        $(".radio_input").qtip({
            id: 'radioinput',
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
        $(".radio_input").on('validate', null, function() {
            if ($(".radio_input input:radio:checked").length != 1) {
                var qtip_content = '<p>请选择化验结果</p>';
                $(this).qtip('api').set('content.text',
                    qtip_content);
                $(this).qtip('api').show();
            }
            else {
                // valid
                record_data.value = $(".radio_input input:radio:checked").val();
            }
        });
    } // }}}
    else {
        // unknown
        return false;
    }

    // validate reason
    var reasoninput_help = '<p><strong>必填</strong></p>';
    $(".reason_input").qtip({
        id: 'reasoninput',
        prerender: false,
        content: {
            text: reasoninput_help
        },
        position: {
            my: 'bottom left',
            at: 'top right'
        },
        show: {
            event: false
        },
        hide: {
            //event: 'click'
            event: false
        }
    });
    $(".reason_input").focus(function() {
        $(this).removeClass("valid invalid");
        // show help tooltip
        var qtip_content = dateinput_help;
        $(this).qtip('api').set('content.text', qtip_content);
        $(this).qtip('api').show();
    });
    $(".reason_input").on('validate', null, function() {
        var reason_str = $(this).val();
        if (is_str_blank(reason_str)) {
            // reason not given or blank
            $(this).removeClass("valid");
            $(this).addClass("invalid");
            var qtip_content = '<p>未输入内容，或为空白内容</p><p>请重新输入</p>';
            $(this).qtip('api').set('content.text', qtip_content);
            $(this).qtip('api').show();
        }
        else {
            // valid
            $(this).removeClass("invalid");
            $(this).addClass("valid");
            $(this).qtip('api').hide();
            // update data
            record_data.reason = reason_str;
        }
    });
    $(".reason_input").on('blur', null, function() {
        $(this).trigger('validate');
    });
    // }}}
});

// help functions
// check if a string is empty, null or undefined
function is_str_empty(str) {
    return (!str || 0 === str.length);
}

// check if a string is blank, null or undefined
function is_str_blank(str) {
    return (!str || /^\s*$/.test(str));
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
