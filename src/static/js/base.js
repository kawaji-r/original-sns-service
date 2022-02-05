// ==================================
// ナビゲーションバー
// ==================================
$(document).ready(() => {
    $('.top-menu-bar .btn').on('click', () => {
        $('.side-menu-bar').toggleClass('active');
    })
})

// ==================================
// プロフィール画面
// ==================================

// disabled切り替えトグル（Name,Description）
$(document).on("click", ".jz-profile-edit", function () {
  var el = $(this).parent().parent().find(".form-control");
  if ($(this).parent().parent().find(".form-control").prop("disabled")) {
    $(this).parent().parent().find(".form-control").prop("disabled", false);
  } else {
    $(this).parent().parent().find(".form-control").prop("disabled", true);
  }
});

// disabledになっているものはsubmitする前にenableにしておく必要がある
$("#profile-edit").submit(function () {
    $(this)
      .find(".form-control")
      .each(function (index, element) {
          $(element).prop("disabled", false);
      });
});

// ==================================
// ajax setup
// ==================================

$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          if (cookie.substring(0, name.length + 1) == name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    }
  },
});

// ==================================
// いいね機能 ajax
// ==================================

$(document).on("click", ".btn-like", function () {
  var child = $(this).children();
  var id = child.data("id");
  if (child.hasClass("post-like")) {
    $.ajax({
      type: "post",
      url: "/like/",
      data: {
        id: id,
        csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val(),
      },
      success: function (data) {
        $(".post-like-" + id)
          .removeClass("post-like")
          .addClass("post-liked");
        var like_count = data["like_count"];
        $(".like-count-" + id).html(like_count);
      },
    });
  } else {
    $.ajax({
      type: "post",
      url: "/unlike/",
      data: {
        id: id,
        csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val(),
      },
      success: function (data) {
        $(".post-like-" + id)
          .removeClass("post-liked")
          .addClass("post-like");
        var like_count = data["like_count"];
        $(".like-count-" + id).html(like_count);
      },
    });
  }
});

// ==================================
// リポスト機能 ajax
// ==================================

$(document).on("click", ".btn-repost", function () {
  var child = $(this).children();
  var id = child.data("id");
  if (child.hasClass("post-repost")) {
    $.ajax({
      type: "post",
      url: "/repost/",
      data: {
        id: id,
        csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val(),
      },
      success: function (data) {
        $(".post-repost-" + id)
          .removeClass("post-repost")
          .addClass("post-reposted");
      },
    });
  } else {
    $.ajax({
      type: "post",
      url: "/unrepost/",
      data: {
        id: id,
        csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val(),
      },
      success: function (data) {
        $(".post-repost-" + id)
          .removeClass("post-reposted")
          .addClass("post-repost");
      }
    })
  }
});

// ==================================
// ブックマーク機能 ajax
// ==================================
$(document).on("click", ".jz-btn-bookmark", function() {
    const id = $(this).data('id');
    const url = ($(this).hasClass('jz-bookmarked')) ? '/unbookmarking/' : '/bookmarking/';
    $.ajax({
        type: "post",
        url: url,
        data: {
            id: id,
            csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val()
        },
        success: function (data) {
            if (url === '/bookmarking/') {
                $(".jz-btn-bookmark[data-id="+id+"]").addClass("jz-bookmarked");
                $(".jz-btn-bookmark[data-id="+id+"]").text("ブックマークから外す");
            } else {
                $(".jz-btn-bookmark[data-id="+id+"]").removeClass("jz-bookmarked");
                $(".jz-btn-bookmark[data-id="+id+"]").text("このポストをブックマークする");
            }
            // $(".jz-btn-follow[data-id="+id+"]")[0].innerHTML = data.innerHtml;
        }
    });
});

// ==================================
// フォロー機能 ajax
// ==================================
$(document).on("click", ".jz-btn-follow", function () {
    // data-id属性からフォローするユーザーを取得（フォローボタンを設置する際はdata-id属性が必須）
    const id = $(this).data('id');
    const url = ($(this).hasClass('btn-main')) ? '/accounts/follow/' : '/accounts/unfollow/';
    $.ajax({
        type: "post",
        url: url,
        data: {
            id: id,
            csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val()
        },
        success: function (data) {
            if (url === '/accounts/follow/') {
                $(".jz-btn-follow[data-id="+id+"]").removeClass("btn-main").addClass("btn-sub");
            } else {
                $(".jz-btn-follow[data-id="+id+"]").removeClass("btn-sub").addClass("btn-main");
            }
            $(".jz-btn-follow[data-id="+id+"]")[0].innerHTML = data.innerHtml;
        }
    });
});

// ==================================
// リプライ表示 ajax
// ==================================

function showReply(pk, replies) {
  var trigger = "#posts-trigger-" + pk;
  var output = "#posts-reply-" + pk;
  var txt = $(trigger).html();
  txt = $.trim(txt);
  if (txt.endsWith("件の返信を表示")) {
    $.ajax({
      url: "/reply/",
      method: "GET",
      data: { pk: pk },
      dataType: "text",
      timeout: 5000,
    })
      .done(function (data) {
        $(trigger).html("返信を閉じる");
        $(output).html(data);
      })
      .fail(function () {
        $(output).text("リプライを取得できませんでした");
      });
  } else {
    $(trigger).html(replies + "件の返信を表示");
    $(output).html("");
  }
}

// ==================================
// プロフィール画像
// ==================================
$(() => {
    if (location.href.indexOf('/accounts/') === -1) return;

    // トリミング窓の大きさ設定
    viewportWidth = 300
    viewportHeight = 300
    boundaryWidth = 500
    boundaryHeight = 350

    // croppieの初期設定
    $image_crop = $('#profileImage_croppie').croppie({
        enableExif: true,
        viewport: {
            width: viewportWidth,
            height: viewportHeight,
            type:'circle'
        },
        boundary: {
            width: boundaryWidth,
            height: boundaryHeight
        }
    })

    $('#upload_image').on('change', function(){
        const reader = new FileReader()
        reader.onload = event => {
            $image_crop.croppie('bind', {
                url: event.target.result
            })
        }
        $('#profileImage_croppie').css('display','block')
        reader.readAsDataURL(this.files[0])
        $('#post_image').css('display', 'block')
    })

    // croppie窓非表示
    $('#profileImage_croppie').css('display', 'none')
    /// 登録ボタン非表示
    $('#post_image').css('display', 'none')

    // モーダルが非表示になった時に動く
    $('#uploadimageModal').on('hidden.bs.modal', function () {
        // croppie窓非表示
        $('#profileImage_croppie').css('display', 'none')
        /// 登録ボタン非表示
        $('#post_image').css('display', 'none')
    });

    // デフォルトアイコンの場合は「画像を削除」ボタン非表示
    if ($('.jz-img').attr('src') === '/static/images/no_photo.png') $('#delete_image').css('display', 'none')
})

// 登録ボタン押下
$('#post_image').on('click', () => {
    $image_crop.croppie('result', 'base64').then(response => {
        $('<input>').attr({
            type: 'hidden',
            name: 'image_base64',
            value: response
        }).appendTo('#profile-edit')
        $(this).parents('form').on('submit')
    })
})

// 削除ボタン押下
$('#delete_image').on('click', () => {
    $('<input>').attr({
        type: 'hidden',
        name: 'image_delete',
        value: true
    }).appendTo('#profile-edit')
    $(this).parents('form').on('submit')
})