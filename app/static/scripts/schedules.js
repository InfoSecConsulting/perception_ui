/**
 * Created by arozar on 07/28/16
 * */

var AddSchedule = function(){

  var handleAddSchedule = function(){
    jQuery('.schedules-form').hide();

    jQuery('#add-schedule-btn').click(function() {
      jQuery('.portlet-body').hide();
      jQuery('.schedules-form').show();
    });
    
    //jQuery('#delete-schedule-btn').live('click', function() {
    //  $.ajax({
    //    url: '/delete_service_accounts?data_id='+$(this).data("id")+'&data_set='+$(this).data("set"),
    //    type: 'POST',
    //    //data: {data_id: },
    //    success: function(result) {
    //      location.reload();
    //    }});
    //});
    
    jQuery('#add-schedule-back-btn').click(function() {
      jQuery('.portlet-body').show();
      jQuery('.schedules-form').hide();
    });
  };
  return{
    init: function(){
      handleAddSchedule()
    }
  };
}();
