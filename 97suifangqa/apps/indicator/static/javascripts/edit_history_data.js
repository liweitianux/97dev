$(document).ready(function(){
	//点大叉，关闭弹层页面
	$(".edit_history_data_close").bind("click", function(){
		parent.TB_remove();
		return false;
	});
	$("#edit_btn").bind("click", function(){
		var this_edit_data_div = $(this).parent();
		var data_fir = $(this).siblings(".data_fir").text();
		var data_sec = $(this).siblings(".data_sec").text();
		var this_editing_data_div = this_edit_data_div.siblings(".editing_data");
		var input_container = this_editing_data_div.children(".input_container");
		input_container.children(".edit_input_main").val(parseInt(data_fir));
		input_container.children(".edit_input_sub").val(parseInt(data_sec));
		this_editing_data_div.show();
		this_edit_data_div.hide();
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
		
		var date = new Date();
		var time = date.getTime();
		$.ajax({
			type: 'get',
			url: indicator_url + 'ajax/edit_history_data',
			data: 'time='+time,
			success: function(data){
				if(data == 'success'){
					parent.TB_remove();
					parent.redraw_chart(parent.detail_chart, "2013-08-04", "2013-08-10"); //这边需要穿过来起始，结束时间，以便刷新图表和表格
				}
			}
		});
		
		return false;
	});
});

// vim: set ts=4 sw=4 tw=0 fenc=utf-8 ft=javascript: //
