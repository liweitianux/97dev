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
        buttonImageOnly: true
    });
    // edit button
    $("#edit_btn").bind("click", function(){
        var this_edit_data_div = $(this).closest(".edit_data");
        //var data_fir = $(this).siblings(".data_fir").text();
        //var data_sec = $(this).siblings(".data_sec").text();
        var data_fir = 0;
        var data_sec = 0;
        var this_editing_data_div = this_edit_data_div.siblings(".editing_data");
        var input_container = this_editing_data_div.children(".input_container");
        input_container.children(".edit_input_main").val(parseInt(data_fir));
        input_container.children(".edit_input_sub").val(parseInt(data_sec));
        this_editing_data_div.show();
        this_edit_data_div.hide();
        return false;
    });
    // save botton
    $("#save_btn").bind("click", function(){
        var data_input_fir = $(".edit_input_main");
        var data_input_sec = $(".edit_input_sub");
        var data_input_fir_val = data_input_fir.val();
        var data_input_sec_val = data_input_sec.val();

        if(data_input_fir_val == '' || data_input_fir_val == 0){
            data_input_fir.addClass("error");
        }else{
            data_input_fir.removeClass("error");
        }
        if(data_input_sec_val == ''){
            data_input_sec.addClass("error");
        }else{
            data_input_sec.removeClass("error");
        }
        if($(".error").length > 0){
            return false;
        }

        var time = moment().valueOf();
        $.ajax({
            type: 'get',
            url: indicator_url + 'ajax/edit_history_data',
            data: 'time='+time,
            success: function(data){
                if(data == 'success'){
                    parent.TB_remove();
                    //parent.redraw_chart(parent.detail_chart, "2013-08-04", "2013-08-10"); //这边需要穿过来起始，结束时间，以便刷新图表和表格
                }
            }
        });
        return false;
    });

    // set datepicker 'date_input' value
    var date_init = $.datepicker.parseDate('yy-mm-dd',
            $(".date_input").attr('value'));
    $(".date_input").datepicker("setDate", date_init);

    // data validate {{{
    // validate date
    $(".date_input").focus(function() {
        $(this).removeClass("valid invalid");
    });
    $(".date_input").change(function() {
        var date_str = $(this).val();
        var date_mm = moment(date_str, 'YYYY-MM-DD');
        var today_mm = moment();
        //console.log('date_str: ', date_str);
        // date cannot beyond today
        if (date_mm.isValid() && !date_mm.isAfter(today_mm)) {
            $(this).removeClass("invalid");
            $(this).addClass("valid");
        }
        else {
            // date invalid
            $(this).removeClass("valid");
            $(this).addClass("invalid");
        }
    });
    // validate data
    $(".data_input").focus(function() {
        $(this).removeClass("valid invalid");
    });
    $(".data_input").change(function() {
        //$(this).removeClass("valid invalid");
    });
    // validate reason
    $(".reason_input").focus(function() {
        $(this).removeClass("valid invalid");
    });
    $(".reason_input").blur(function() {
        var reason_str = $(this).val();
        if (is_str_blank(reason_str)) {
            // reason not given or blank
            $(this).removeClass("valid");
            $(this).addClass("invalid");
        }
        else {
            // reason given and not blank
            $(this).removeClass("invalid");
            $(this).addClass("valid");
        }
    });
    // }}}

    //编辑数据的底数验证：只允许两位小数，非空
    $(".edit_input_main").bind("keyup", function(){
        var val = $(this).val();
        val = val.replace(/[^\d.]/g,""); //清除"数字"和"."以外的字符
        val = val.replace(/^\./g,""); //验证第一个字符是数字而不是..
        val = val.replace(/\.{2,}/g,"."); //只保留第一个. 清除多余的
        val = val.replace(".","$#$").replace(/\./g,"").replace("$#$",".");
        val = val.replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3');
        $(this).val(val);
        return false;
    });
    //编辑数据的指数验证：只允许整数
    $(".edit_input_sub").bind("keyup", function(){
        var val = $(this).val().replace(/[^\d]/g, '');
        $(this).val(val);
        return false;
    });
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

// vim: set ts=4 sw=4 tw=0 fenc=utf-8 ft=javascript: //
