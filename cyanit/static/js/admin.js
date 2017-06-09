function ui_del(btn) {
  if (btn.text() == '恢复') {
    btn.parent().prev().text('正常');
    btn.text('删除');
    btn.removeClass('label-warning recover');
    btn.addClass('label-danger delete');
  } else {
    btn.parent().prev().text('已删除');
    btn.text('恢复');
    btn.removeClass('label-danger delete');
    btn.addClass('label-warning recover');
  }
}

function ajax_del(url, btn) {
  $.ajax({
    url: url,
    data: {'id': btn.attr('id')},
    type: 'POST',
    dataType: 'json',
    success: function(res) {
      if (res.success == undefined) {
        alert(res.error);
        }
      else {
        ui_del(btn);
      }
    },
    error: function(error) {
      alert('server error');
    }
  });
  }

function init_btn(url, word) {
  // 初始化刪除按钮
  $('#table tr').on('click', 'a.delete', function(e) {
    e.preventDefault();
    if (confirm('确定要删除该'+word+'?')) {
      ajax_del(url, $(this));
    }
  });
  $('#table tr').on('click', 'a.recover', function(e) {
    e.preventDefault();
    if (confirm('确定要恢复该'+word+'?')) {
      ajax_del(url, $(this));
    }
  });
}
