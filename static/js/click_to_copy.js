$(function() {
  $('.allowCopy').click(function() {
    $(this).focus();
    $(this).select();
    document.execCommand('copy');
  });
});