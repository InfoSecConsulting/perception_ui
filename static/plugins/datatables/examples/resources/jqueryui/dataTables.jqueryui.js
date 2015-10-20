
(function(){

var DataTable = $.fn.dataTable;
var sort_prefix = 'css_right templates-icon templates-icon-';
var toolbar_prefix = 'fg-toolbar templates-toolbar templates-widget-header templates-helper-clearfix templates-corner-';

/* Set the defaults for DataTables initialisation */
$.extend( true, DataTable.defaults, {
	dom:
		'<"'+toolbar_prefix+'tl templates-corner-tr"lfr>'+
		't'+
		'<"'+toolbar_prefix+'bl templates-corner-br"ip>',
	renderer: 'jqueryui'
} );


$.extend( DataTable.ext.classes, {
	/* Full numbers paging buttons */
	"sPageButton":         "fg-button templates-button templates-state-default",
	"sPageButtonActive":   "templates-state-disabled",
	"sPageButtonDisabled": "templates-state-disabled",

	/* Features */
	"sPaging": "dataTables_paginate fg-buttonset templates-buttonset fg-buttonset-multi "+
		"templates-buttonset-multi paging_", /* Note that the type is postfixed */

	/* Sorting */
	"sSortAsc":            "templates-state-default sorting_asc",
	"sSortDesc":           "templates-state-default sorting_desc",
	"sSortable":           "templates-state-default sorting",
	"sSortableAsc":        "templates-state-default sorting_asc_disabled",
	"sSortableDesc":       "templates-state-default sorting_desc_disabled",
	"sSortableNone":       "templates-state-default sorting_disabled",
	"sSortIcon":           "DataTables_sort_icon",

	/* Scrolling */
	"sScrollHead": "dataTables_scrollHead "+"templates-state-default",
	"sScrollFoot": "dataTables_scrollFoot "+"templates-state-default",

	/* Misc */
	"sHeaderTH":  "templates-state-default",
	"sFooterTH":  "templates-state-default",
} );


DataTable.ext.renderer.header.jqueryui = function ( settings, cell, column, idx, classes ) {
	$('<div/>')
		.addClass( 'DataTables_sort_wrapper' )
		.append( cell.contents() )
		.append( $('<span/>')
			.addClass( classes.sSortIcon+' '+column.sSortingClassJUI )
		)
		.appendTo( cell );

	// Attach a sort listener to update on sort
	$(settings.nTable).on( 'order.dt', function ( e, settings, sorting, columns ) {
		cell
			.removeClass( classes.sSortAsc +" "+classes.sSortDesc )
			.addClass( columns[ idx ] == 'asc' ?
				classes.sSortAsc : columns[ idx ] == 'desc' ?
					classes.sSortDesc :
					column.sSortingClass
			);

		cell
			.find( 'span' )
			.removeClass(
				sort_prefix+'triangle-1-n' +" "+
				sort_prefix+'triangle-1-s' +" "+
				sort_prefix+'carat-2-n-s' +" "+
				sort_prefix+'carat-1-n' +" "+
				sort_prefix+'carat-1-s'
			)
			.addClass( columns[ idx ] == 'asc' ?
				sort_prefix+'triangle-1-n' : columns[ idx ] == 'desc' ?
					sort_prefix+'triangle-1-s' :
					column.sSortingClassJUI
			);
	} );
}


/*
 * TableTools jQuery UI compatibility
 * Required TableTools 2.1+
 */
if ( DataTable.TableTools ) {
	$.extend( true, DataTable.TableTools.classes, {
		"container": "DTTT_container templates-buttonset templates-buttonset-multi",
		"buttons": {
			"normal": "DTTT_button templates-button templates-state-default"
		},
		"collection": {
			"container": "DTTT_collection templates-buttonset templates-buttonset-multi"
		}
	} );
}


}());

