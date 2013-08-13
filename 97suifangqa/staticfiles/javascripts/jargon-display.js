//Jargon display
function jargon_display(annotations) {
	var make_jargon_entry = function(j) {
		var li = $('<li><a href="#jargon-' + j.id + '">'+j.name+'</a></li>');
        $('a', li).data('jargon', j);
        return li;
	  };

	$.each(annotations, function(id, pn) {
        if (pn.type == 0 ) {
            /* 段落注释 */
            $("#paracomments-list").append(make_jargon_entry(pn));
        } else {
            $("#propernouns-list").append(make_jargon_entry(pn));
            $("p").each(function (i, elm) {
              p = $(elm);
              p.html(p.html().
                replace(pn.name, '<a class="jargon" href="#jargon-'+id+'">'+pn.name+'</a>'));
            });
        }
    });

	var jargonRoot = $(".jargons");
	var jargonDisplayBox = $('#content .jargon-explanation-box');
	if (jargonRoot.size() == 0 || jargonDisplayBox.size() == 0 )
		return;

    jargonDisplayBox.bind("setdata", function(evt, jargon) {
        var text = jargon.is_collected ? "点击取消收藏" : "收藏该注释";
        text += '(已有' + jargon.collected_times + '人收藏)';
        jargonDisplayBox.data('jargon', jargon);
        $(".name", $(this)).text(jargon.name);
        $(".jargon-details", $(this)).html(jargon.content);
        if (jargon.type == 0){$("a.collect", $(this)).hide()}
        	else {$("a.collect", $(this)).text(text).show()}
        		/* Maxwell modified */
    })

    $('a.collect', jargonDisplayBox).click(function() {
      var jargon = jargonDisplayBox.data('jargon');
      if (jargon.type == 0) {
          /* 段落注释不添加收藏功能 */
          return ;
      }
      var button = $(this);
      var url = '/blog/annotation/'+jargon.id+'/collect';
      $.ajax({
          url:url,
          dataType:'json',
          success: function(data) {
              var origjargon = jargonDisplayBox.data('jargon');
              origjargon.is_collected = data.added;
              origjargon.collected_times = data.times;
              jargonDisplayBox.trigger('setdata', origjargon);
          }
      });
    });

	function setJargonBoxPosition(position) {
		if (position) {
			jargonDisplayBox.css('margin-top', '');
			jargonDisplayBox.css('top', position['top']);
			jargonDisplayBox.find('.text-pointer').css('left', position['left']);
			jargonDisplayBox.removeClass('modal');
		}else{
			jargonDisplayBox.css('margin-top', - jargonDisplayBox.outerHeight() / 2);
			jargonDisplayBox.addClass('modal');
			$("#modal-page-overlay").removeClass('hidden');
			$('body').addClass('modal-active');
		}
	}

	function closeJargonBox() {
		jargonDisplayBox.removeClass('open');
		$("#modal-page-overlay").addClass('hidden');
		$('body').removeClass('modal-active');
		jargonDisplayBox.removeClass('loaded');
		currentJargonKey = null;
	}

	function showJargonExplanation(jargon, position) {
        jargonDisplayBox.addClass('open');
        setJargonBoxPosition(position);
        
        jargonDisplayBox.trigger('setdata', jargon)
        jargonDisplayBox.addClass('loaded');
	}

	jargonDisplayBox.click(function(e) {
		e.stopPropagation();
	})
	$('body').click(closeJargonBox);
	jargonDisplayBox.find('.close-box').click(closeJargonBox);

	function inlinePos(elem) {
	    var el = $('<i/>').css('display','inline').insertBefore(elem);
	    var pos = el.position();
	    var outerHeight = el.outerHeight()
	    el.remove();
	    return [pos, outerHeight];
	};
	var maxWidth = jargonRoot.innerWidth();

	$('a.jargon').each(function() {
        var id = $(this).attr('href').substr($(this).attr('href').search('-')+1);
		$(this).data('jargon', annotations[id]);
    }).click(function(e) {
		e.stopPropagation();
		e.preventDefault();
		var link = $(this);
		var info = inlinePos(link);
		var pos = info[0];
		var outerHeight = info[1];
		pos['top'] += outerHeight;
		var trueWidth = link.outerWidth();
		if (trueWidth > (maxWidth - pos['left']))
			trueWidth = maxWidth - pos['left'];
		
		pos['left'] = pos['left'] + trueWidth / 2;
		if (pos['left'] < 10) pos['left'] = 10;
		showJargonExplanation(link.data('jargon'), pos);
	})

	$(".jargon-links a").filter(function() {
		return $(this).attr('href') && $(this).attr('href').indexOf('#') == 0;
	}).click(function(e) {
		e.stopPropagation();
		e.preventDefault();
		showJargonExplanation($(this).data('jargon'));
	})
}

