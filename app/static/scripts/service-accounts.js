/**
 * Created by arozar on 10/27/15.
 */
var ServiceAccount = function(){

  var handleAddSvcAccount = function(){
    jQuery('.svc-acc-form').hide();

    /*
    $('.add-svc-account').validate({
      errorElement: 'span', //default input error message container
      errorClass: 'help-block', // default input error message class
      focusInvalid: false, // do not focus the last invalid input
      ignore: "",
      rules: {

        username: {
          required: true
        },

        password:{
          required: true
        }
      },

      invalidHandler: function(event, validator) { //display error alert on form submit
      },

      highlight: function(element) { // hightlight error inputs
        $(element)
          .closest('.form-group').addClass('has-error'); // set error class to the control group
      },

      success: function(label) {
        label.closest('.form-group').removeClass('has-error');
        label.remove();
      },

      errorPlacement: function(error, element) {
        if (element.closest('.input-icon').size() === 1) {
          error.insertAfter(element.closest('.input-icon'));
        } else {
          error.insertAfter(element);
        }
      },

      submitHandler: function(form) {
        form.submit();
      }
    });

    $('.svc-acc-form input').keypress(function(e) {
      if (e.which == 13) {
        if ($('.svc-acc-form').validate().form()) {
          $('.svc-acc-form').submit();
        }
        return false;
      }
    });

    */

    jQuery('#add-svc-acc-btn').click(function() {
              jQuery('.portlet-body').hide();
              jQuery('.svc-acc-form').show();
    });

    jQuery('#add-svc-acc-back-btn').click(function() {
            jQuery('.portlet-body').show();
            jQuery('.svc-acc-form').hide();
        });
  };
  return{
    init: function(){
      handleAddSvcAccount()
    }
  };
}();