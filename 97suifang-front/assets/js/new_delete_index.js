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
	
	/************************ 登录控件交互 Start ********************************/
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
	/************************ 登录控件交互 Start ********************************/
	
	
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
	$(".add>.icon").live("click", function(){
		var add_icon = $(this);
		var index_id = add_icon.closest(".index_line").attr("index_id");
		var date = new Date();
		var time = date.getTime();
		$.ajax({
			type: 'get',
			url: '../ajax/act_index',
			data: 'index_id='+index_id+'&act=add'+'&time='+time,
			success: function(data){
				if(data == 'success'){
					var obj = add_icon.parent();
					var objClone = obj.clone();
					objClone.removeClass("add")
					objClone.children(".index_category").remove();
					$(".right").append(objClone);
					classHover(objClone, "minus");
				}
			}
		});
		
		return false;
	});
	$(".minus>.icon").live("click", function(){
		var minus_icon = $(this);
		var index_id = minus_icon.closest(".index_line").attr("index_id");
		var date = new Date();
		var time = date.getTime();
		$.ajax({
			type: 'get',
			url: '../ajax/act_index',
			data: 'index_id='+index_id+'&act=minus'+'&time='+time,
			success: function(data){
				var obj = minus_icon.parent();
				obj.remove();
			}
		});
		
		return false;
	});
	$(".all_condition>.index_all_letter>div").bind("click", function(){
		$(".letter_selected").removeClass("letter_selected");
		$(this).addClass("letter_selected");
		var container = $(".index_letter_container");
		var letterClass = $(this).text();
		var scrollTo = $("."+letterClass);
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