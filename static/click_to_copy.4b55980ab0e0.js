$(function() {
    $('.form-control').click(function() {
      $(this).focus();
      $(this).select();
      document.execCommand('copy');
    });
 });