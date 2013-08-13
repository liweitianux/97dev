$(document).ready(function(){
	//点大叉、继续关注按钮，关闭弹层页面
	$(".delete_card_tip_close, .action_confirm_ignore").bind("click", function(){
		parent.TB_remove();
		return false;
	});
	
	//取消关注，关闭弹层页面
	$(".action_confirm_cancel").bind("click", function(){
		//TODO
		//底层数据层取消关注（ajax）
		//console.log(parent.card_2_delete_id); //要取消关注的 卡片id 的获取方法
		
		parent.delete_card();
		parent.TB_remove();
		return false;
	});
});