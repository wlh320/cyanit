function vote_ajax(vote_to, action, id) {
  $.ajax({
    url: '/' + vote_to + '/vote/' + id + '?action=' + action,
    type: 'POST',
    dataType: 'json',
    success: function(res) {
      // todo
    },
    error: function(error) {
      alert(error.statusText);
    }
  });
}

// 顶
$('.up').click(function() {
  var parent = $(this).parent();
  var id = parent.attr('id');
  var vote_to = parent.attr('class').split('-')[1];
  var count = $(this).next();
  var down = $(this).next().next();
  vote_ajax(vote_to, 'up', id);
  if ($(this).hasClass('select')) {  //取消赞成
    $(this).removeClass('select');
    count.text(Number(count.text()) - 1);
  } else if (down.hasClass('select')) {  //反对变赞成
    down.removeClass('select');
    $(this).addClass('select');
    count.text(Number(count.text()) + 2);
  } else {  //直接赞成
    $(this).addClass('select');
    count.text(Number(count.text()) + 1);
  }
});

// 踩
$('.down').click(function() {
  var parent = $(this).parent();
  var id = parent.attr('id');
  var vote_to = parent.attr('class').split('-')[1];
  var count = $(this).prev();
  var up = $(this).prev().prev();
  vote_ajax(vote_to, 'down', id);
  if ($(this).hasClass('select')) {  //取消反对
    $(this).removeClass('select');
    count.text(Number(count.text()) + 1);
  } else if (up.hasClass('select')) {  //赞成变反对
    up.removeClass('select');
    $(this).addClass('select');
    count.text(Number(count.text()) - 2);
  } else {  //直接反对
    $(this).addClass('select');
    count.text(Number(count.text()) - 1);
  }
});
