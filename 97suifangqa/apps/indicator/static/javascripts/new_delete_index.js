// track the indexes already added(/followed)
var added_indexes_id = new Array();

var select_letter = '';
var select_index_obj = null;

$(document).ready(function(){
    $(".index_type").each(function(){
        if($(this).hasClass("selected")){
            select_index_obj = $(this);
            return false;
        }
    });
    $(".index_type").hover(
        function(){
            $(this).addClass("selected");
        },
        function(){
            if(!$(this).is(select_index_obj)){
                $(this).removeClass("selected");
            }
        }
    );

    // 'all_condition' letter selectors {{{
    // disable all letter selectors
    $(".index_all_letter .letter").addClass("disabled");
    $(".index_letter_container .letter_section").each(function() {
        var l = $(this).attr('id').replace('sec_', '');
        //console.log(l);
        $(".index_all_letter #"+l).removeClass("disabled");
    });
    // }}}

    // login control kit {{{
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
    // login }}}

    // search -> ajax
    // bind enter key
    $(".search #search_kw").on('keypress', null, function(e) {
        var keycode = (e.keyCode ? e.keyCode : e.which);
        //console.log('keycode: "'+keycode+'"');
        if (keycode == 13) {
            //alert('"Enter" key pressed');
            var kw = $(this).val();
            //console.log('kw: "'+kw+'"');
            search_indicators(kw);
            return false;
        }
    });
    $(".search #search_btn").bind("click", function(){
        var kw = $("#search_kw").val();
        //console.log('kw: "'+kw+'"');
        //window.location.href = '?kw='+kw;
        search_indicators(kw);
        return false;
    });

    // XXX: cannot deal with the dynamically added div's by ajax
    /*
    $(".left>.index_line, .index_letter_container>.index_lines>.index_line").each(function(){
        classHover($(this), "add");
    });
    $(".right>.index_line").each(function(){
        classHover($(this), "minus");
    });
    */
    // updated to work with ajax
    $(".show_indexes").on('mouseenter mouseleave', '.index_lines>.index_line', function(e) {
        //console.log("event_type: "+e.type);
        var line = $(this);
        var lines_div = line.parent();
        if (lines_div.hasClass("to_add")) {
            // left container (unfollowed)
            var cls_name = "add";
        }
        else {
            // right container (followed)
            var cls_name = "minus";
        }
        // event type
        if (e.type === 'mouseenter') {
            $(this).addClass(cls_name);
        }
        else {
            $(this).removeClass(cls_name);
        }
    });

    // save the "index_id's of added (type: string)
    $(".right>.index_line").each(function(){
        var index_id = $(this).attr("index_id");
        added_indexes_id.push(index_id);
    });
    $(".show_indexes").on("click", ".add>.icon", function(){
        var add_icon = $(this);
        var index_id = add_icon.closest(".index_line").attr("index_id");
        var date = new Date();
        var time = date.getTime();
        $.ajax({
            type: 'get',
            url: indicator_url + 'ajax/act_index/',
            data: 'index_id='+index_id + '&act=add' + '&time='+time,
            success: function(data){
                if(data == 'success'){
                    // check if the index exists?
                    if (added_indexes_id.indexOf(index_id) == -1) {
                        var obj = add_icon.parent();
                        var objClone = obj.clone();
                        objClone.removeClass("add")
                        objClone.children(".index_category").remove();
                        $(".right").append(objClone);
                        classHover(objClone, "minus");
                        added_indexes_id.push(index_id);
                    }
                }
            }
        });

        return false;
    });
    $(".show_indexes").on("click", ".minus>.icon", function(){
        var minus_icon = $(this);
        var index_id = minus_icon.closest(".index_line").attr("index_id");
        var date = new Date();
        var time = date.getTime();
        $.ajax({
            type: 'get',
            url: indicator_url + 'ajax/act_index/',
            data: 'index_id='+index_id + '&act=minus' + '&time='+time,
            success: function(data){
                var obj = minus_icon.parent();
                obj.remove();
                rm_index = added_indexes_id.indexOf(index_id);
                added_indexes_id.splice(rm_index, 1);
            }
        });

        return false;
    });
    $(".all_condition>.index_all_letter>div").bind("click", function(){
        $(".letter_selected").removeClass("letter_selected");
        $(this).addClass("letter_selected");
        var container = $(".index_letter_container");
        var letterClass = $(this).attr('id');
        //console.log(letterClass);
        var scrollTo = $("#sec_"+letterClass);
        container.scrollTop(scrollTo.offset().top - container.offset().top + container.scrollTop());
        select_letter = letterClass;
        return false;
    });
    $(".all_condition>.index_all_letter>div").hover(
        function(){
            $(this).addClass("letter_selected");
        },
        function(){
            if(select_letter != $(this).text()){
                $(this).removeClass("letter_selected");
            }
        }
    );
    $("#submitIndexBtn").bind("click", function(){
        var commit_index = '';
        $(".right>.index_line").each(function(){
            commit_index += $(this).attr("index_id")+',';
        });
        $("#commit_index").val(commit_index);
        $("#index_form").submit();
        return false;
    });
});


// helper functions
function classHover(obj, c){
    obj.hover(
        function(){
            $(this).addClass(c);
        },
        function(){
            $(this).removeClass(c);
        }
    );
}

// search
function search_indicators(kw) {
    if (is_str_blank(kw)) {
        // 'kw' blank
        return false;
    }
    var time = moment().valueOf();
    $.ajax({
        type: 'get',
        url: indicator_url + 'ajax/search_indicators/',
        data: 'kw='+kw + '&time='+time,
        dataType: 'json',
        success: function(dataJson) {
            // unselect index_type
            $(".index_navigation .selected").removeClass("selected");
            select_index_obj = null;
            // hide & show
            $(".all_condition").hide();
            $(".category_condition").hide();
            $(".search_condition").show();
            // clear existing search div's or create
            if ($(".search_condition > .index_lines").length) {
                $(".search_condition > .index_lines").html('');
            }
            else {
                // add 'index_lines' div
                $(".search_condition").append('<div class="index_lines left to_add"></div>');
            }
            if (dataJson.failed === true) {
                if (dataJson.error_code === 10) {
                    // search keyword blank
                    $(".search_condition > .index_lines").append('<div class="index_search_error"> <div class="index_error">您未输入搜索关键词</div> <div class="icon"></div> <div style="clear:both"></div> </div>');
                }
                if (dataJson.error_code === 20) {
                    // search result empty
                    $(".search_condition > .index_lines").append('<div class="index_search_error"> <div class="index_error">未搜索到符合的结果</div> <div class="icon"></div> <div style="clear:both"></div> </div>');
                }
            }
            else {
                // append search results to page
                var results_html = '';
                for (var i=0; i<dataJson.indicators.length; i++) {
                    var ind = dataJson.indicators[i];
                    results_html += '<div class="index_line" index_id="'+ind.id + '"> <div class="index_name">'+ind.name + '</div> <div class="index_category"><a href="?tab='+ind.categories_id[0] + '">'+ind.categories_name[0] + '</a></div> <div class="icon"></div> <div style="clear:both"></div> </div> \n';
                }
                $(".search_condition > .index_lines").append(results_html);
            }
        }
    });
    return false;
}

// check if a string is blank, null or undefined
function is_str_blank(str) {
    return (!str || /^\s*$/.test(str));
}


// vim: set ts=4 sw=4 tw=0 fenc=utf-8 ft=javascript: //
