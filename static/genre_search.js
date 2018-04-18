
$(document).ready(function() {

	//$("#search-results").hide();

	var genres = [
	'adult standards',
	 'afrobeat',
	 'album rock',
	 'art rock',
	 'blues',
	 'blues-rock',
	 'brill building pop',
	 'chicago soul',
	 'christmas',
	 'classic funk rock',
	 'classic rock',
	 'country rock',
	 'dance pop',
	 'dance rock',
	 'deep funk',
	 'delta blues',
	 'disco',
	 'electric blues',
	 'folk rock',
	 'folk',
	 'funk',
	 'glam rock',
	 'hard rock',
	 'heavy christmas',
	 'hip pop',
	 'jazz blues',
	 'jazz christmas',
	 'jazz funk',
	 'lounge',
	 'melancholia',
	 'mellow gold',
	 'memphis blues',
	 'memphis soul',
	 'modern blues',
	 'motown',
	 'neo soul',
	 'new jack swing',
	 'new orleans blues',
	 'new romantic',
	 'new wave pop',
	 'new wave',
	 'northern soul',
	 'p funk',
	 'pop',
	 'post-disco',
	 'post-punk',
	 'protopunk',
	 'psychedelic rock',
	 'quiet storm',
	 'r&b',
	 'rock',
	 'rock-and-roll',
	 'rockabilly',
	 'roots rock',
	 'singer-songwriter',
	 'smooth jazz',
	 'soft rock',
	 'soul blues',
	 'soul christmas',
	 'soul jazz',
	 'soul',
	 'southern rock',
	 'southern soul',
	 'symphonic rock',
	 'synthpop',
	 'uk post-punk',
	 'urban contemporary',
	 'vocal jazz'
	 ];
	$( "#genre-search-bar" ).autocomplete({
	    source: genres
	});



	$("#search-form-master").submit(function(event) {
		//console.log("Button clicked");
		//var genre = $("#genre-search-bar").val();
		var tempo = $("#tempo-search-bar").val();
		var key = $("#key-list").val();
		var time_signature = $("#time-sig-list").val();
		//console.log(genre);

		//console.log(key);

		// Create empty array
		var array = [];

		// Create JSON object with property "genre_label"
		var json_object = {
			//genre: genre,   
			tempo: tempo,
			key: key,
			time_signature: time_signature
		}

		// console.log("JSON object");
		// console.log(json_object);

		// Add object to array
		array.push(json_object);

		// console.log("Array");
		// console.log(array);

		// Encode JSON string
		var json_string = JSON.stringify(array);

		// console.log("JSON string");
		// console.log(json_string);


		//$("#search-results").show();
		//$("#search-results").hide();

		var json = $.get("/song_search_test_temp", json_object, function(json) {parse(json);});

		// specify the columns
		var columnDefs = [
		{headerName: "Artist Name", field: "artist_name"}
	    ];

	    // let the grid know which columns and what data to use
    	var gridOptions = {
    		columnDefs: columnDefs,
    		enableSorting: true,
    		enableFilter: true
    	};

		// lookup the container we want the Grid to use
		var eGridDiv = document.querySelector('#myGrid');

		// create the grid passing in the div to use together with the columns & data we want to use
		new agGrid.Grid(eGridDiv, gridOptions);

		console.log("AAAA");
		gridOptions.api.setRowData(json.data);
		console.log("BBBB");
	});

	function parse(json)
	{
		// //console.log(json["data"]);
		// var results = json["data"];
		// results.forEach(function(element) {
		// 	var row = $("<div class='row'>");

		// 	// Allocate space for album art; insert image
		// 	var album_col = $("<div class='col-xs-2'>");
		// 	var album_art = $("<img src='https://images-na.ssl-images-amazon.com/images/I/510cBiPgbIL.jpg' class='img-responsive album_art'>");

		// 	// Allocate space for song information; insert information
		// 	var song_info_col = $("<div class='col-xs-10'>");
		// 	var song_info_row = $("<div class='row song-info-row'><div id='info1'>");
  //           var song_artist = $("<b>Superfly</b> • Curtis Mayfield"); 

  //           $(album_col).append(album_art);
  //           $(row).append(album_col);
		// 	$("#search-results").append(row);
		// });
	}


	// var artists = [];


});
