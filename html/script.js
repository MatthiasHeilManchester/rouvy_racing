
//===================================================================
// Function to display animated gif while loading specified php script
//===================================================================
function display_cyclist_while_loading_most_popular_route(url_of_most_popular_route_php_script){
    window.location.assign(url_of_most_popular_route_php_script);
    $("#most_popular_route_loader").attr('src', 'rvy_racing.png');
    //$("#most_popular_route_loader").attr('src', 'https://i.stack.imgur.com/SBv4T.gif');
    //)cyclist_displayed_while_finding_most_popular_rides.gif');
    $("#most_popular_route_loader").css('display','block');
    $("#most_popular_route_loader").css('visibility','visible');
    $(".race_blob").css('webkit-filter', 'blur(3px)');
    $(".blurrable_during_popular_race_load").css('webkit-filter', 'blur(3px)');
    //window.location.href=url_of_most_popular_route_php_script;
}


//===================================================================
// Function to navigate to rvy home page. Specify number dir levels
// we need to ascend to get above the rvy_racing home directory (in
// the published webpages)
//===================================================================
function back_to_rvy_racing_homepage(levels_up_to_rvy_racing_dir) {
    var dir="";
    for (i = 0; i < levels_up_to_rvy_racing_dir; i++) {
	dir+="../";
    }
    dir+="rvy_racing/rvy_racing.php";
    console.log(dir);
    window.location.href=dir;
}


//===================================================================
// Function to make full (1), wed-only (2) or sat-only (3) league
// table visible
//===================================================================
function show_league_table(i_table) {
    
    switch(i_table) {
    case 1:
	document.getElementById("full_league_table_div").style.display = "block";
	document.getElementById("wed_league_table_div").style.display = "none";
	document.getElementById("sat_league_table_div").style.display = "none";
	document.getElementById("full_league_table_button").style.background = "yellow";
	document.getElementById("wed_league_table_button").style.background = "lightyellow";
	document.getElementById("sat_league_table_button").style.background = "lightyellow";
	break;
    case 2:
	document.getElementById("full_league_table_div").style.display = "none";
	document.getElementById("wed_league_table_div").style.display = "block";
	document.getElementById("sat_league_table_div").style.display = "none";
	document.getElementById("full_league_table_button").style.background = "lightyellow";
	document.getElementById("wed_league_table_button").style.background = "yellow";
	document.getElementById("sat_league_table_button").style.background = "lightyellow";
	break;
    case 3:
	document.getElementById("full_league_table_div").style.display = "none";
	document.getElementById("wed_league_table_div").style.display = "none";
	document.getElementById("sat_league_table_div").style.display = "block";
	document.getElementById("full_league_table_button").style.background = "lightyellow";
	document.getElementById("wed_league_table_button").style.background = "lightyellow";
	document.getElementById("sat_league_table_button").style.background = "yellow";
	break;
    default:
    }
    
    
}




//=======================================================================
// Specify table column header that this is called from
// (clicking on "this" object calls this function; we retrieve the
// enclosing table by going up the dom hierarchy...
// Sort entries in the n-th column.
// Direction is specified by dir which can take values "asc" or "desc"
// Based on: https://www.w3schools.com/howto/howto_js_sort_table.asp
//=======================================================================
function sort_column_in_table(dir,th,n) {
    
    var table, rows, switching, i, x, y, shouldSwitch, switchcount = 0;
    
    // Check that direction is legal 
    if ((dir!="asc")&&(dir!="desc")){
	var err_messg="Error dir has to be \"asc\" or \"desc\"";
	console.error(err_messg);
	return;
    }
    
    // Get point to table itself
    table = th.parentNode.parentNode;
    
    // Row as array
    var header_row=table.getElementsByTagName("th");
    // Switch colours: to show activated one
    for (i = 0; i < (header_row.length); i++) {
	header_row[i].style.backgroundColor='yellow';
    }
    th.style.backgroundColor='gold';
    
    
    
    // Make a loop that will continue until
    // no switching has been done
    switching = true;
    while (switching) {
	switching = false;
	rows = table.rows;
	// Loop through all table rows (except the
	// first, which contains table headers):
	for (i = 1; i < (rows.length - 1); i++) {
	    shouldSwitch = false;
	    // Get the two elements you want to compare,
	    //one from current row and one from the next:
	    x = rows[i].getElementsByTagName("TD")[n];
	    y = rows[i + 1].getElementsByTagName("TD")[n];
	    // check if the two rows should switch place,
	    // based on the direction, asc or desc:
            var lhs=0;
            // strip out "=" signs from draws
            lhs=parseFloat(x.innerHTML.replace(/=/,''));
	    var rhs=0;
	    rhs=parseFloat(y.innerHTML.replace(/=/,''));
	    if (dir == "asc") {
		if (lhs > rhs) {
		    //if so, mark as a switch and break the loop:
		    shouldSwitch= true;
		    break;
		}
	    } else if (dir == "desc") {
		if (lhs < rhs) {		    
		    //if so, mark as a switch and break the loop:
		    shouldSwitch = true;
		    break;
		}
	    }
	}
	if (shouldSwitch) {
	    // If a switch has been marked, make the switch
	    // and mark that a switch has been done:
	    rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
	    switching = true;
	    //Each time a switch is done, increase this count by 1:
	    switchcount ++;      
	}  //hierher else {
	// /* If no switching has been done AND the direction is "asc",
	// then the column was already sorted in ascending order, so
	// set the direction to "desc" and run the while loop again.*/
	// if (switchcount == 0 && dir == "asc") {
	//   dir = "desc";
	//   switching = true;
	// } 
	// } 
    }
}

