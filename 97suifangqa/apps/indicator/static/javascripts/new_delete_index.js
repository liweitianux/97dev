// track the indexes already added(/followed)
var added_indexes_id = new Array();

$(document).ready(function(){
	$("#search_btn").bind("click", function(){
		var kw = $("#search_kw").val();
		window.location.href = '?kw='+kw;
		return false;
	});
	$(".left>.index_line, .index_letter_container>.index_lines>.index_line").each(function(){
		classHover($(this), "add");
	});
	$(".right>.index_line").each(function(){
		classHover($(this), "minus");
	});
	// save the "index_id's of added (type: string)
	$(".right>.index_line").each(function(){
		var index_id = $(this).attr("index_id");
		added_indexes_id.push(index_id);
	});
	$(".index_lines").on("click", ".add>.icon", function(){
		var add_icon = $(this);
		var index_id = add_icon.closest(".index_line").attr("index_id");
		var date = new Date();
		var time = date.getTime();
		$.ajax({
			type: 'get',
			url: indicator_url + 'ajax/act_index',
			data: 'index_id='+index_id+'&act=add'+'&time='+time,
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
	$(".index_lines").on("click", ".minus>.icon", function(){
		var minus_icon = $(this);
		var index_id = minus_icon.closest(".index_line").attr("index_id");
		var date = new Date();
		var time = date.getTime();
		$.ajax({
			type: 'get',
			url: indicator_url + 'ajax/act_index',
			data: 'index_id='+index_id+'&act=minus'+'&time='+time,
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
		$(".index_letter_container>.index_lines").hide();
		var letterClass = $(this).text();
		$("."+letterClass).show();
		$("."+letterClass).nextAll().show();
		return false;
	});
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

// vim: set ts=4 sw=4 tw=0 fenc=utf-8 ft=javascript: //
