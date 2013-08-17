// global js var: card_2_delete_id (type: string)

$(document).ready(function(){
//	console.log(parent.card_2_delete_id); //要取消关注的 卡片id 的获取方法
	//点大叉、继续关注按钮，关闭弹层页面
	$(".delete_card_tip_close, .action_confirm_ignore").bind("click", function(){
		parent.TB_remove();
		return false;
	});
	
	//取消关注，关闭弹层页面
	$(".action_confirm_cancel").bind("click", function(){
		// ajax process to unfollow the indicator
		// indicator_id -> parseInt(parent.card_2_delete_id)
		// 底层数据层取消关注（ajax）
		var date = new Date();
		var time = date.getTime();
		$.ajax({
			type: 'get',
			url: parent.indicator_url + 'ajax/unfollow_indicator',
			data: 'indicator_id='+parent.card_2_delete_id+'&time='+time,
			success: function(data) {
				if (data == 'success') {
					parent.delete_card();
					parent.TB_remove();
				}
			},
		});
		
		return false;
	});
});
