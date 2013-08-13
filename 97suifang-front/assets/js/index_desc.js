$(document).ready(function(){
	//点大叉、继续关注按钮，关闭弹层页面
	$(".index_desc_close").bind("click", function(){
		parent.TB_remove();
		return false;
	});
	
	//前往医学知识库
	$(".go_library_btn").bind("click", function(){
		parent.delete_card();
		parent.TB_remove();
		
		parent.window.location.href = "http://demo.97suifang.com/blog/1/source";
		return false;
	});
});