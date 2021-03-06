// Generated by CoffeeScript 1.6.3
var bootstrap_alert;

bootstrap_alert = Object;

bootstrap_alert.warning = function() {
  return $('#alert_placeholder').html('<div class="alert alert-error block-message"><span>' + message + '</span></div>');
};

bootstrap_alert.hide = function() {
  return $('#alert_placeholder').html('');
};

$(function() {
  $('#login-form').validate({
    rules: {
      email: {
        required: true,
        email: true
      },
      password: {
        minlength: 8,
        required: true
      }
    },
    highlight: function(label) {
      var group;
      group = $(label).closest('.control-group');
      group.removeClass('success');
      return group.addClass('error');
    },
    success: function(label) {
      var group;
      group = $(label).closest('.control-group');
      group.removeClass('error');
      return group.addClass('success');
    }
  });
  return true;
});
