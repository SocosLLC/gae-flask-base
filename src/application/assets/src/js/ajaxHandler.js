/* ajaxHandler.js
 *
 * Pilfered from http://cam.st/ajax-block-rendering-in-flask/
 */

function ajaxGet(url, data) {

  var successFcn = function(data) {
    // If pushState is supported, use it for AJAXy response
    if (!!window.history && history.pushState) {
      history.pushState(data.page, data.title, data.url);
      $(data.view_container).html(data.page);
    } else {  // If no pushState support, just go to URL
      console.log("No pushState. Redirecting to " + data.url);
      location.href = data.url;
    }
  };

  var failureFcn = function(something, error) {
    console.log('GET failure: ' + error);
  };

  $.get(url, data)
    .done(successFcn)
    .fail(failureFcn)
}


function ajaxPost(url, data, handler /* = null */) {

  var successFcn = function(data) {
    // If pushState is supported, use it for AJAXy response
    if (!!window.history && history.pushState) {
      history.pushState(data.page, data.title, data.url);
      $(data.view_container).html(data.page);
    } else {  // If no pushState support, just go to URL
      console.log("No pushState. Redirecting to " + data.url);
      location.href = data.url;
    }
  };

  var failureFcn = function(_, error) {
    console.log('POST failure: ' + error);
  };

  if (handler) {
    if (data) {
      data += '&handler=' + handler;
    } else {
      data = 'handler=' + handler
    }
  }

  $.post(url, data)
    .done(successFcn)
    .fail(failureFcn)
}

