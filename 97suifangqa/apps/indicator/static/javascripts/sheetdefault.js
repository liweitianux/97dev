var card_2_delete_id;
var card_detail_id;
$(document).ready(function(){
	//不允许input框复制，减少验证粘帖的交互
	$("input[type='text']").bind("paste", function(){
		return false;
	});
	
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
	
	//点击编辑icon
	$(".small_edit_icon").bind("click", function(){
		var this_edit_data_div = $(this).parent();
		var this_select_date_div = this_edit_data_div.siblings(".select_date");
		var this_refresh_data_div = this_edit_data_div.siblings(".refresh_data");
		var this_last_edit_data_div = $(this).siblings(".last_edit_data");
		var this_editing_data_div = this_edit_data_div.siblings(".editing_data");
		var input_container = this_editing_data_div.children(".input_container");
		var data_fir = this_last_edit_data_div.children(".data_fir").text();
		var data_sec = this_last_edit_data_div.children(".data_sec").text();
		input_container.children(".edit_input_main").val(parseInt(data_fir));
		input_container.children(".edit_input_sub").val(parseInt(data_sec));
		this_editing_data_div.show();
		this_select_date_div.show();
		this_edit_data_div.hide();
		this_refresh_data_div.hide();
		return false;
	});
	//点击指数+1 icon
	$(".add_icon").bind("click", function(){
		var this_edit_input_sub = $(this).closest(".editing_data").children(".input_container").children(".edit_input_sub");
		var origin_value = parseInt(this_edit_input_sub.val());
		this_edit_input_sub.val(origin_value+1);
		return false;
	});
	//点击 指数-1 icon
	$(".minus_icon").bind("click", function(){
		var this_edit_input_sub = $(this).closest(".editing_data").children(".input_container").children(".edit_input_sub");
		var origin_value = parseInt(this_edit_input_sub.val());
		var after_value = origin_value-1;
		if(after_value >= 0){
			this_edit_input_sub.val(origin_value-1);
		}
		return false;
	});
	//编辑数据的底数验证：只允许两位小数，非空
	$(".edit_input_main").bind("keyup", function(){
		var val = $(this).val();
		val = val.replace(/[^\d.]/g,"");//清除"数字"和"."以外的字符
		val = val.replace(/^\./g,"");//验证第一个字符是数字而不是..
		val = val.replace(/\.{2,}/g,".");//只保留第一个. 清除多余的
		val = val.replace(".","$#$").replace(/\./g,"").replace("$#$",".");
		val = val.replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3');
		$(this).val(val);
		return false;
	});
	//编辑数据的指数验证：只允许整数
	$(".edit_input_sub").bind("keyup", function(){
		$(this).val($(this).val().replace(/[^\d]/g, ''));
		return false;
	});
	//点击取消icon
	$(".cancel_edit_icon").bind("click", function(){
		var input_container = $(this).siblings(".input_container");
		input_container.children(".edit_input_main").val('');
		input_container.children(".edit_input_sub").val('');
		var this_editing_data_div = $(this).parent();
		this_editing_data_div.siblings(".edit_data").show();
		this_editing_data_div.siblings(".refresh_data").show();
		this_editing_data_div.hide();
		this_editing_data_div.siblings(".select_date").hide();
		return false;
	});
	//点击提交icon
	$(".confirm_edit_icon").bind("click", function(){
		var input_container = $(this).siblings(".input_container");
		var data_input_fir = input_container.children(".edit_input_main");
		var data_input_sec = input_container.children(".edit_input_sub");
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
		
		//TODO ajax
		data_input_fir.val('');
		data_input_sec.val('');
		var this_editing_data_div = $(this).parent();
		var this_select_date_div = this_editing_data_div.siblings(".select_date");
		var this_refresh_data_div = this_editing_data_div.siblings(".refresh_data");
		var this_edit_data_div = this_editing_data_div.siblings(".edit_data");
		var this_last_edit_div = this_edit_data_div.children(".last_edit_data");
		this_last_edit_div.show();
		this_last_edit_div.children(".data_fir").html(data_input_fir_val);
		this_last_edit_div.children(".data_sec").html(data_input_sec_val);
		this_editing_data_div.hide();
		this_select_date_div.hide();
		this_edit_data_div.show();
		this_refresh_data_div.show();
		
		return false;
	});
	
	//日期控件
	$(".select_date>.datepicker").datepicker({
		 showOn: "both",
		 buttonImage: static_url + "plugins/datepicker/images/calendar.png",
		 buttonImageOnly: true
	});
	
	//时间范围控制（开始时间<结束时间）
	$("#search_start_date").datepicker({
		showOn: "both",
		buttonImage: static_url + "plugins/datepicker/images/calendar.png",
		buttonImageOnly: true,
		onClose: function( selectedDate ) {
			$("#search_end_date").datepicker("option", "minDate", selectedDate);
		}
	});
	$("#search_end_date").datepicker({
		onClose: function( selectedDate ) {
			$("#search_start_date").datepicker("option", "maxDate", selectedDate);
		}
	});
});

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

// vim: set ts=4 sw=4 tw=0 fenc=utf-8 ft=javascript: //
