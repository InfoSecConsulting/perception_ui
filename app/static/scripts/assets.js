/**
 * Created by arozar on 10/20/15.
 */
var Assets = function(){

  var handleAssets= function(){
    jQuery('.individual-asset-table-scrollable').hide();

    jQuery('#show-individual-asset').live('click', function() {
      $.ajax({
        url: '/individual_asset?data_id='+$(this).data("id"),
        type: 'GET',
        success: function(response) {
          jQuery('.portlet-body').hide()
          $("#individual-asset-table-scrollable").html(response);
          jQuery('.individual-asset-table-scrollable').show();
        }
      });
    });

    jQuery('#hide-individual-asset').click(function(){
      jQuery('.portlet-body').show()
      jQuery('.individual-asset-table-scrollable').hide();
    });
  };

return{
    init: function(){
      handleAssets()
    }};
}();