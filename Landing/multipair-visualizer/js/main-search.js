
  
$( function() {
	$.widget( "custom.catcomplete", $.ui.autocomplete, {
		_create: function() {
			this._super();
			this.widget().menu( "option", "items", "> :not(.ui-autocomplete-category)" );
		},
		_renderMenu: function( ul, items ) {
			var that = this,
			currentCategory = "";
			console.log("in rendermenu");
			$.each( items, function( index, item ) {
				//console.log("prvi dio item label: "+item.label+" prvi dio item value: "+item.value);
				var li;
				if ( item.category != currentCategory ) {
					ul.append( "<li class='ui-autocomplete-category'>" + item.category + "</li>" );
					currentCategory = item.category;
				}
				li = that._renderItemData( ul, item );
				
				if ( item.category ) {
					li.attr( "aria-label", item.category + " : " + item.label );
				}
			});
		}
	});
	
	$('#searchbox').catcomplete({
		minLength: 3,
		source: function(request, response) {
			$.ajax({
				url: '/fast/2fh_search.php',
				delay: 1000,
				data: {
					q: request.term
				},
				dataType: "json",
				success: function(data) {
					//console.log("success, got something back...");
					//data.data.sort(function(item1, item2){
						//						return item1.category > item2.category ? 1 : -1;
						//console.log("data sorting: "+item.category+" "+item.name);
					//});
					response($.map(data, function(item) {
						return {
							value: item.value,
							label: item.label,
							category: item.category,
							slug: item.slug
						}
					}));
				}
			});
		},
		select: function( event, ui ) {
			console.log( "Selected: " + ui.item.value + " aka " + ui.item.label + " cat: "+ui.item.category );
			if(ui.item.category=='crypto')
			{
				window.location.href = 'https://cryptocoincharts.info/coins/show/'+ui.item.value;
			}
			if(ui.item.category=='exchange')
			{
				window.location.href = 'https://cryptocoincharts.info/markets/show/'+ui.item.value;
			}
			if(ui.item.category=='market')
			{
				window.location.href = 'https://cryptocoincharts.info/pair/'+ui.item.value;
			}
			if(ui.item.category=='ico')
			{
				window.location.href = 'https://cryptocoincharts.info/ico/'+ui.item.slug;
			}
			//console.log( "Selected: " + ui.item.value + " aka " + ui.item.label + " cat: "+ui.item.category );
		}
	});
});

