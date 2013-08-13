$(document).ready(function(){
	////伸缩式导航，兼容ff、ie
	$("#nav_container").hover(
		function(){
			$(".default_nav").animate({left: "194px"}, {queue:false, duration:300}); //�������(20px)+�������(86+1=87px)*2=194px
		},
		function(){
			$(".default_nav").animate({left: "20px"}, {queue:false, duration:300});  //�������
		}
	);
});