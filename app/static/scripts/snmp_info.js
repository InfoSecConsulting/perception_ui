/**
 * Created by arozar on 4/2/16.
 */


var SnmpInfo = function(){

  var handleSnmpInfo = function(){
    jQuery('.snmp-info-form').hide();
    jQuery('.edit-snmp-info-form').hide();
    
    jQuery('#add-snmp-info-btn').click(function() {
      jQuery('.portlet-body').hide();
      jQuery('.snmp-info-form').show();
    });

    jQuery('#add-snmp-info-back-btn').click(function() {
      jQuery('.portlet-body').show();
      jQuery('.snmp-info-form').hide();
    });

    jQuery('#delete-snmp-info-btn').live('click', function() {
      $.ajax({
        url: '/delete_snmp_info?data_id='+$(this).data("id"),
        type: 'POST',
        //data: {data_id: },
        success: function(result) {
          location.reload();
        }});
    });
  
    jQuery('#edit-snmp-info-btn').live('click', function() {
      jQuery('.portlet-body').hide();
      jQuery('.edit-snmp-info-form').show();
    });

    jQuery('#submit-snmp-info-btn').live('click', function () {
      alert('submit!');
      
      $.ajax({
        url: '/edit_snmp_info?data_id='+$(this).data("id"),
        type: 'POST',
        data: {
          community_sting: $(this).data("cs"),
          snmp_user: $(this).data("v3user"),
          snmp_group: $(this).data("v3group")
        },
        success: function(result) {
         location.reload();
        }});
      });

    jQuery('#edit-snmp-info-back-btn').click(function() {
      jQuery('.portlet-body').show();
      jQuery('.edit-snmp-info-form').hide();
    });
    
  };
  return{
    init: function(){
      handleSnmpInfo()
    }
  };
}();