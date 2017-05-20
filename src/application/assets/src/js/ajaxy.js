$( document ).ready(function() {

  $('#a-btn').click(function() { ajaxGet('ajaxy?state=a') });
  $('#b-btn').click(function() { ajaxGet('ajaxy?state=b') });

});
