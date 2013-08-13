/**
 * @file 
 * Primary Scripts for the site
 *
 * @author 赵迤晨 (Zhao Yichen) <interarticle@gmail.com>
 */

"use strick";
//Remove html no-js class, and add has-js class. Ensures proper css js detection.
//DON NOT REMOVE THE FOLLOWING LINE!
$("html").removeClass("no-js").addClass("has-js");

//Expandable blocks
(function($, undefined) {
	$(".expandable .expand-heading").click(function() {
		var element = $(this);
		var parentElement = $(this).closest('.expandable');
		if (!parentElement.hasClass('expanded') && parentElement.data('expand-group-selector')) {
			$(parentElement.data('expand-group-selector')).removeClass('expanded');
		}
		parentElement.toggleClass('expanded');
	})
})(jQuery);


/**
 * Image Enlargment 
 */
(function($, undefined) {
	var imageEnlargmentBox = $("#image-enlargement-box");
	var imageEnlargmentBoxContainer = imageEnlargmentBox.find('.image-container');
	function showImage(url) {
		imageEnlargmentBoxContainer.empty();
		var img = $("<img>").attr('src', url);
		imageEnlargmentBoxContainer.append(img);
		imageEnlargmentBox.addClass('open');
		img.load(function(){
			//SetTimeout to prevent incorrect image size measurement
			setTimeout(function() {
				imageEnlargmentBox.css('margin-top', -img.height() / 2);
				imageEnlargmentBox.css('margin-left', -img.width() / 2);
				imageEnlargmentBox.addClass('loaded');
			}, 100);
		});

		$("#modal-page-overlay").removeClass('hidden');
		$('body').addClass('modal-active');
	}

	function hideImage() {
		imageEnlargmentBox.removeClass('open');
		imageEnlargmentBox.css('margin-top','');
		imageEnlargmentBox.css('margin-left', '');
		$("#modal-page-overlay").addClass('hidden');
		$('body').removeClass('modal-active');
		imageEnlargmentBox.removeClass('loaded');
	}
	$("body").click(hideImage);
	if (imageEnlargmentBox.size() > 0) {
		$(function() {
			$("#content a.enlarge-image").click(function(e) {
				e.preventDefault();
				e.stopPropagation();
				showImage($(this).attr('href'));
			})
		});
	}
})(jQuery);

/**
 * General purpose modal dialog
 */
(function($, undefined) {
	var modalOverlay = $("#modal-page-overlay");
	var modalDialogBox = $("#modal-dialog-box");

	function modalShow() {
		modalOverlay.removeClass('hidden');
		modalDialogBox.css('margin-top', - modalDialogBox.outerHeight() / 2);
		modalDialogBox.css('margin-left', - modalDialogBox.outerWidth() / 2);
		modalDialogBox.addClass('open');
		$("body").addClass('modal-active');
	}
	function modalHide() {
		modalDialogBox.removeClass('open');
		modalOverlay.addClass('hidden');
		$('body').removeClass('modal-active');
	}
	$("body").click(modalHide);
	modalDialogBox.find('.close-box').click(modalHide);
	modalDialogBox.click(function(e) {
		e.stopPropagation();
	})
	$.fn.extend({
		modalShow: function() {
			modalDialogBox.find('.content-wrap').empty().append($(this).clone(true));
			modalShow();
		},
		modalHide: modalHide
	});
	$.extend({
		modalHide: modalHide
	});
})(jQuery);

/**
 * Section Nav scrolling
 */

(function($, undefined){
	var triggerPositions = [];
	function getScrollPosition(e) {
		var scrollID = typeof(e) == "string" && e ? e : e.attr('href');
		if (scrollID == null) return;
		scrollID = scrollID.substr(1);
		var elem = document.getElementById(scrollID);
		if (elem && $(elem).prop('tagName') == 'A') {
			location.href="#" + scrollID + "-jas";
			elem = $(elem);
			pos = elem.offset();
			if ($(window).width() >= 1300 && $(window).height() >= 600) {
				pos['top'] -= $("#blog-top-nav").outerHeight();
			}
			return pos['top']
		}
	}
	function scrollLink(e) {
		var pos = getScrollPosition($(this));
		if (pos != null) {
			$(".section-nav a").removeClass('active');
			$(this).addClass('active');
			if (typeof(e) != "string") e.preventDefault();
			$("html,body").animate({scrollTop: pos});
		}
	}
	$(function(){
		$(".section-nav a").filter(function() {
			return ($(this).attr('href').indexOf('#') == 0);
		}).click(scrollLink);
		var hash = location.hash;
		if (hash && hash.indexOf('-jas') > 0) {
			var hashTag = hash.substr(0, hash.lastIndexOf('-jas'));
			scrollLink($(".section-nav a").filter(function(){ return $(this).attr("href") == hashTag; }));
		}
	});
	if ($("body").hasClass("blog-details")) {
		$("#content").css('margin-top', $("#blog-top-nav").outerHeight());
	}
})(jQuery);

/**
 * Back to top button
 */
(function($, undefined) {
	$(window).scroll(function() {
		if ($(window).scrollTop() > 10) {
			$("body").addClass('scrolled-down');
		} else {
			$("body").removeClass('scrolled-down');
		}
	})
})(jQuery);
$(function() {
	var btn = $("#back-to-top-button");
	if (btn.size() > 0) {
		btn.click(function() {
			$("html,body").animate({scrollTop: 0});
		})
	}
});

/**
 * Card handling
 */
(function($,undefined) {
	$('.blog #content .card').click(function() {
		if ($(this).attr('href') != null)
			location.href = $(this).attr('href');
	}).mouseleave(function() {
		$("#card-abstract").removeClass('show').empty();
	}).mouseenter(function() {
		$("#card-abstract").empty().append($(this).find('.abstract').clone()).addClass('show');
	})
})(jQuery);

(function($, undefined) {
	$("#login.logged-in .drop-down-area").click(function(e) {
		e.stopPropagation();
		$("#login.logged-in .drop-down-menu").toggleClass('open');
	})
	$("body").click(function() {
		$("#login.logged-in .drop-down-menu").removeClass('open');
	})
})(jQuery);
