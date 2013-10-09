//
// js for 'add_edit_blog_info' page
//
// 2013/10/08
//

// a list contains all the configs data objects
var research_configs_list = new Array();

$(document).ready(function() {
    // make a configs list from 'research_configs {{{
    var obj_keys = Object.keys(research_configs);
    for (var i=0; i<obj_keys.length; i++) {
        var key = obj_keys[i];
        var configs = research_configs[key].configs;
        research_configs_list = research_configs_list.concat(configs);
    }
    // }}}

    // categories buttons {{{
    var cate_btns_html = '';
    for (var i=1; i<=rind_num; i++) {
        var btn_id = 'btn_cate_'+i;
        var btn_value = i+'个指标';
        cate_btns_html += '<input type="button" class="unselected" id="'+btn_id + '" value="'+btn_value + '" /> &ensp; ';
    };
    $("#cate_btns").html(cate_btns_html);
    // button actions
    $('#cate_btns input[type="button"]').on("click", document, function() {
        // unselect all buttons
        //console.log(this);
        $('#cate_btns input[type="button"]').removeClass("selected");
        $('#cate_btns input[type="button"]').addClass("unselected");
        $(this).removeClass("unselected");
        $(this).addClass("selected");
        // unselect buttons of combinations
        $('#comb_divs input[type="button"]').removeClass("selected");
        $('#comb_divs input[type="button"]').addClass("unselected");
        // hide configs div's
        $('#conf_divs .conf_comb').hide();
        // display category of combinations
        var cate_id = $(this).attr('id').replace('btn_cate_', '');
        $('#comb_divs .comb').hide();
        $('#div_comb_'+cate_id).show();
    });
    // }}}

    // indicator combinations div's and buttons {{{
    var comb_divs_html = '';
    for (var i=1; i<=rind_num; i++) {
        var id = 'div_comb_'+i;
        comb_divs_html += '<div class="comb" id="'+id + '" style="display: none;">\n';
        // combinations buttons
        var btn_comb_html = '';
        var combs = rind_categories['N'+i];
        for (var j=0; j<combs.length; j++) {
            var btn_id = combs[j].tag;
            // get value for button
            var btn_value = get_comb_btn_value(combs[j].data);
            btn_comb_html += '<input type="button" class="unselected" id="'+btn_id + '" value="'+btn_value + '" /> &ensp; ';
        };
        comb_divs_html += btn_comb_html + '\n</div>\n';
    };
    $("#comb_divs").html(comb_divs_html);
    // button actions
    $('#comb_divs input[type="button"]').on("click", document, function() {
        // unselect all buttons
        $('#comb_divs input[type="button"]').removeClass("selected");
        $('#comb_divs input[type="button"]').addClass("unselected");
        $(this).removeClass("unselected");
        $(this).addClass("selected");
        // display configs of the combination
        var comb_id = $(this).attr('id');
        $('#conf_divs .conf_comb').hide();
        $('#div_conf_'+comb_id).show();
    });
    // }}}

    // config div's & info input {{{
    var conf_divs_html = '';
    for (var i=0; i<rind_combs.length; i++) {
        var comb = rind_combs[i];
        var id = 'div_conf_'+comb.tag;
        conf_divs_html += '<div class="conf_comb" id="'+id + '" style="display: none;">\n';
        // configs input
        var conf_input_html = '<table class="conf">\n';
        // table head
        conf_input_html += '<thead style="display: none;">\n<tr class="head">';
        conf_input_html += '<th class="name"></th> <th class="response"></th> <th class="weight"></th>';
        conf_input_html += '</tr></thead>\n';
        // table body
        conf_input_html += '<tbody>\n';
        var configs = research_configs[comb.tag].configs;
        //console.log(configs);
        for (var j=0; j<configs.length; j++) {
            // odd or even (for table tr style)
            if (j%2 == 0) {
                var odd_even = 'odd';
            }
            else {
                var odd_even = 'even';
            }
            var conf = configs[j];
            var conf_id = conf.tag;
            var conf_tr_html = '<tr class="conf '+odd_even + '" id="'+conf_id + '">';
            // display name column
            conf_tr_html += '<td class="name">' + conf.display + '</td>';
            // treat response column (prompt & select input)
            conf_tr_html += '<td class="response">' + treat_responses_objs.name + ': <select class="treat_response"></select></td>';
            // weight column
            conf_tr_html += '<td class="weight">权重: <input type="text" class="weight" value="" /></td>';
            //
            conf_tr_html += '</tr>\n';
            conf_input_html += conf_tr_html;
        };
        conf_input_html += '</tbody>\n</table>';
        //console.log(conf_input_html);
        conf_divs_html += conf_input_html + '\n</div>\n';
    };
    $("#conf_divs").html(conf_divs_html);
    // }}}

    // treat response select {{{
    $("select.treat_response").each(function() {
        // add options for 'select'
        var select_html = '';
        // add empty value
        select_html += '<option value="" selected="selected">----</option>\n';
        for (var i=0; i<treat_responses_list.length; i++) {
            var tr = treat_responses_list[i];
            select_html += '<option class="response tr'+tr.id+'" value="id'+tr.id + '">' + tr.name + '</option>\n';
        }
        $(this).html(select_html);
    });
    // }}}

    // validate weight {{{
    $("input.weight").on("validate", null, function(e) {
        e.stopPropagation();
        var value = $(this).val();
        var number = parseFloat(value);
        if (value == "") {
            $(this).removeClass("valid invalid");
        }
        else if (isNaN(number)) {
            $(this).removeClass("valid");
            $(this).addClass("invalid");
        }
        else if (number<0.0 || number>10.0) {
            $(this).removeClass("valid");
            $(this).addClass("invalid");
        }
        else {
            $(this).removeClass("invalid");
            $(this).addClass("valid");
        }
    });
    $("input.weight").on("change", null, function() {
        $(this).trigger("validate");
    });
    // }}}

    // validate tr conf {{{
    // if only one of the 'treat_response' or 'weight' has data
    // then 'invalid'
    $("tr.conf").on("validate", null, function(e) {
        e.stopPropagation();
        var weight_jq = $(this).find("input.weight");
        var response_jq = $(this).find("select.treat_response");
        //console.log(weight_jq);
        // NOTES:
        // only trigger 'validate' of '.weight' element, when
        // the event originated on any element apart from '.weight'
        // REF: http://stackoverflow.com/questions/5967923/jquery-trigger-click-gives-too-much-recursion
        if (! $(e.target).is(".weight")) {
            weight_jq.trigger("validate");
        }
        if (weight_jq.hasClass("invalid")) {
            $(this).addClass("invalid");
        }
        // only one of the 'treat_response' or 'weight' has data
        if (weight_jq.val() !== '' && response_jq.val() === '') {
            $(this).addClass("invalid");
        }
        else if (weight_jq.val() === '' && response_jq.val() !== '') {
            $(this).addClass("invalid");
        }
    });
    // }}}

    // fill provided configs data {{{
    $("tr.conf").each(function() {
        var conf_id = $(this).attr('id');
        var conf_obj = get_config_obj(conf_id);
        if (conf_obj.hasOwnProperty('id')) {
            // this config already in database
            var tr_id = conf_obj.treatResponse_id;
            $(this).find('select>option.tr'+tr_id).prop('selected', true);
            $(this).find('.weight').val(conf_obj.weight);
            // validate tr config
            $(this).trigger('validate');
        }
    });
    // }}}


    // back_to_list button {{{
    $("#back_to_list").bind("click", function() {
        var msg = '注意：当前页面未保存的信息将会丢失。是否继续？';
        var ans = confirm(msg);
        if (ans) {
            window.location.href = recommend_index_url;
        }
        else {
            return false;
        }
    });
    // }}}

    // submit info button {{{
    $("#submit_info").on("click", null, function() {
        // validate tr conf data
        $("tr.conf").trigger("validate");
        if ($("tr.conf.invalid").length) {
            alert('存在有错误数据的行，请更正后再提交');
            return false;
        }
        // collect conf data
        var configs_list = new Array();
        $("tr.conf").each(function() {
            var conf_id = $(this).attr('id');
            var conf_obj = get_config_obj(conf_id);
            // get config data
            var weight_jq = $(this).find("input.weight");
            var response_jq = $(this).find("select.treat_response");
            var weight = weight_jq.val();
            var tr_id = response_jq.val().replace('id', '');
            //
            if (conf_obj.hasOwnProperty('id')) {
                if (weight === '' && tr_id === '') {
                    // delete config
                    conf_obj['action'] = 'delete';
                    conf_obj['weight'] = null;
                    conf_obj['treatResponse_id'] = null;
                }
                else {
                    // edit config
                    conf_obj['action'] = 'edit';
                    conf_obj['weight'] = parseFloat(weight);
                    conf_obj['treatResponse_id'] = parseInt(tr_id);
                }
            }
            else {
                if (weight !== '' && tr_id !== '') {
                    // add config
                    conf_obj['action'] = 'add';
                    conf_obj['weight'] = parseFloat(weight);
                    conf_obj['treatResponse_id'] = parseInt(tr_id);
                }
                else {
                    // null config
                    conf_obj['action'] = null;
                    conf_obj['weight'] = null;
                    conf_obj['treatResponse_id'] = null;
                }
            }
            // push config data
            configs_list.push(conf_obj);
        });
        //console.log(configs_list);

        // ajax post configs data {{{
        var time = moment().valueOf();
        $.ajax({
            type: 'post',
            url: recommend_url + 'ajax/add_edit_configs/',
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                configs_list: JSON.stringify(configs_list),
                blog_id: blog_id,
                time: time
            },
            dataType: 'json',
            success: function(dataJson) {
                if (dataJson.failed == true) {
                    // submit failed
                    alert('Error: submit failed');
                    return false;
                }
                else {
                    alert('submit successful');
                    // reload page (do not use cache)
                    location.reload(true);
                }
            }
        });
        // }}}
    });
    // }}}
});


// generate value for combination button
// sort id list by magnitude
function get_comb_btn_value(rid_list) {
    // sort id list numerically (smallest first)
    rid_list.sort(function(a, b) { return a-b });
    var value = '';
    for (var i=0; i<rid_list.length; i++) {
        var key = 'id'+rid_list[i];
        value += rind_objs[key].indicator_name + ' | ';
    }
    value = value.replace(/\s*\|\s*$/, '');
    return value;
};

// return the config js obj (copy)
// by searching the given 'tag' in 'research_configs_list'
function get_config_obj(tag) {
    var result = $.grep(research_configs_list,
            function(e) { return e.tag == tag });
    if (result.length == 1) {
        return $.extend({}, result[0]);
    }
    else {
        return null;
    }
};

// vim: set ts=8 sw=4 tw=0 fenc= ft=javascript: //
