#! /bin/bash


#--------------------------------------------------------
# Script to stage races in a specified series.
#
# Assumptions:
#
# - script is run from home directory, i.e.
#   the directory master_race_data is available
#   as
#
#        ./master_race_data
#
# - single command line argument specifies name
#   of race series, $1. This identifies the
#   series directory as
#
#        ./master_race_data/$1
#
# - Race series contains file with rouvy usernames of
#   all participants in
#
#        ./master_race_data/$1/user_list.txt
#
# - Info about official races is encoded in
#
#        ./master_race_data/$1/race?????/official_race.dat
#
#   which contain the urls of the rouvy race pages, so e.g.
#
#        > cat master_race_data/test_series/race00001/official_race.dat 
#        https://my.rouvy.com/onlinerace/live/87048
#        https://my.rouvy.com/onlinerace/live/87049
#        https://my.rouvy.com/onlinerace/live/87050
#
#--------------------------------------------------------

# Just one command line argument
if [ $# -ne 1 ]; then
 echo "Please specify the race series"
 exit 1
fi

# Be verbose for debugging?
verbose_debug=1

# Name of race series
race_series=$1

# Script should be run from home directory
home_dir=`pwd`
if [ ! -e master_race_data ]; then
    echo -e "\033[0;31mERROR:\033[0m Script ought to be run from home directory, so that"
    echo "directory master_race_data is available as ./master_race_data."
    echo "You are in $home_dir"
    exit 1
fi

# Does race series even exist?
if [ ! -e master_race_data/$race_series ]; then
    echo -e "\033[0;31mERROR:\033[0m Race series master_race_data/$race_series doesn't exist!"
    exit 1
fi
echo " "
echo "==========================================================================="
echo " "
echo "Staging race series : "$race_series
rm -f generated_race_data/$race_series/all_races_in_series.html


# Do we have users?
if [ ! -e ./master_race_data/$race_series/user_list.txt ]; then
    echo -e "\033[0;31mERROR:\033[0m No users for series, i.e. master_race_data/$race_series/user_list.txt doesn't exist!"
    exit 1
fi


# Loop over all races in this series
race_number_in_series=0
cd master_race_data
dir_list=`ls -d $race_series/race?????`



# Loop over all races in series (as identified in master directory)
for dir in `echo $dir_list`; do
 
    # Bump
    let race_number_in_series=$race_number_in_series+1
    echo " "
    echo "Doing race "$race_number_in_series" in series"

    # Set up storage for user contributed race data
    #----------------------------------------------
    cd $home_dir/contributed_race_data

       
    # Go into race
    if [ ! -e $dir ]; then
        echo "Making directory: "`pwd`$dir
        mkdir -p $dir
    else
        echo "Directory: "`pwd`"/$dir already exists."
    fi
    cd $dir
    
    # Create/touch contributed race file (will contain urls)
    touch contributed_race.dat

    # Create/touch file with list items for contributed race file 
    touch contributed_race_list_items.html

    
    # Set up storage for generated race data
    #---------------------------------------
    cd $home_dir/generated_race_data

    # Go into race
    if [ ! -e $dir ]; then
        echo "Making directory: "`pwd`$dir
        mkdir -p $dir
    else
        echo "Directory: "`pwd`"/$dir already exists."
    fi
    
    cd $dir

    # Kill existing official races html list items
    rm -f official_race_list_items.html

    
    # Check download directories or create them
    if [ -e downloaded_official_race_pages ]; then
        if [ $verbose_debug == 1 ]; then echo `pwd`"/downloaded_official_race_pages already exists."; fi
    else
        mkdir downloaded_official_race_pages
        if [ $verbose_debug == 1 ]; then echo "made "`pwd`"/downloaded_official_race_pages directory"; fi
    fi
    if [ -e downloaded_contributed_race_pages ]; then
        if [ $verbose_debug == 1 ]; then echo `pwd`"/downloaded_contributed_race_pages already exists."; fi
    else
        mkdir downloaded_contributed_race_pages
        if [ $verbose_debug == 1 ]; then echo "made "`pwd`"/downloaded_contributed_race_pages directory"; fi
    fi

    # Create link to official race data
    if [ ! -e official_race.dat ]; then
        if [ ! -e ../../../master_race_data/$dir/official_race.dat ]; then
            echo -e "\033[0;31mERROR:\033[0m official_race.dat doesn't exist in master race directory"
            echo "../../../master_race_data/$dir/official_race.dat"
            echo "I'm here: "`pwd`
            exit 1
        else
            echo "official_race.dat doesn't exist in master race directory; making link"
            ln -s ../../../master_race_data/$dir/official_race.dat
        fi
    fi

    # Link to contributed races
    if [ ! -e contributed_race.dat ]; then
        ln -s $home_dir/contributed_race_data/$dir/contributed_race.dat .
    fi
    if [ ! -e contributed_race_list_items.html ]; then
        ln -s $home_dir/contributed_race_data/$dir/contributed_race_list_items.html .
    fi
    
    url_list=`cat official_race.dat`
    cd downloaded_official_race_pages
    race_number=1
    race_date_from_race1="dummy"
    race_time_from_race1="dummy"
    route_id_from_race1="dummy"
    route_title="dummy"
    day="dummy"
    month="dummy"
    year="dummy"
    
    # an array to look up th month-names
    month_names=(not_a_month Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec)
    
    # Loop over all races, download race html file from rouvy
    # and check that they're all
    # - on the same day
    # - on the same route
    for url in `echo $url_list`; do
        html_file="downloaded_race_file"$race_number".html"
        if [ -e $html_file ]; then
            if [ $verbose_debug == 1 ]; then echo "INFO: Have already downloaded "$html_file; fi
        else
            # Check validity of url
            regex='^(https?|ftp|file)://[-A-Za-z0-9\+&@#/%?=~_|!:,.;]*[-A-Za-z0-9\+&@#/%=~_|]\.[-A-Za-z0-9\+&@#/%?=~_|!:,.;]*[-A-Za-z0-9\+&@#/%=~_|]$'
            if [[ $url =~ $regex ]]
            then 
                echo "$url a valid url"
            else
                echo "$url not a valid race url; please check official_race.dat"
                exit 1
            fi
            echo "ABOUT TO DOWNLOAD "$url" into "$html_file 
            wget -q -O $html_file $url
        fi

        # Extract race date and time from downloaded html files

        # Do first race first (provides reference data that we can check the others against
        if [ $race_number -eq 1 ]; then
            
            html_file_name=`ls downloaded_race_file1.html`
            race_date_from_race1=`$home_dir/bin/extract_parameters_from_rouvy_race_page.bash $html_file_name --date`
            race_time=`$home_dir/bin/extract_parameters_from_rouvy_race_page.bash $html_file_name --time`
            route_id_from_race1=`$home_dir/bin/extract_parameters_from_rouvy_race_page.bash $html_file_name --route_id`
            route_title=`$home_dir/bin/extract_parameters_from_rouvy_race_page.bash $html_file_name --route_title`
            
            day=`echo $race_date_from_race1 | awk '{print substr($0,4,2)}'`
            month=`echo $race_date_from_race1 | awk '{print substr($0,1,2)}'`
            year=`echo $race_date_from_race1 | awk '{print substr($0,7)}'`
	    
	    # https://coderwall.com/p/cobcna/bash-removing-leading-zeroes-from-a-variable
	    # (but retain original day format for comparison)
            orig_day=$day
	    day=$(echo $day | sed 's/^0*//')
	    month=$(echo $month | sed 's/^0*//')
	    year=$(echo $year | sed 's/^0*//')
	    
	    #echo "bla: " $day " " ${month} " " $year
            #exit
	    
            echo "Date : " $day " " ${month_names[${month}]} " " $year
            echo "Route: " $route_title
            echo " "
            
            echo "<div class=\"race_blob\"><h2>Race "$race_number_in_series" : " $day " " ${month_names[${month}]} " " $year "</h2>" > .race.html
            echo "<b>Route:</b> <a href=\"https://my.rouvy.com/virtual-routes/detail/"$route_id_from_race1"\">"$route_title"</a>" >> .race.html
            echo "<ul>" >> .race.html

        # Subsequent races: Check their data for consistency
        else
            html_file_name=`ls downloaded_race_file$race_number.html`
            race_date=`$home_dir/bin/extract_parameters_from_rouvy_race_page.bash $html_file_name --date`
            race_time=`$home_dir/bin/extract_parameters_from_rouvy_race_page.bash $html_file_name --time`
            route_id=`$home_dir/bin/extract_parameters_from_rouvy_race_page.bash $html_file_name --route_id`
            
            if [ "$race_date" != "$race_date_from_race1" ]; then
                echo "WARNING: official races 1 and "$race_number" are on different dates: -"$race_date"- and -"$race_date_from_race1"-"
            else
                if [ $verbose_debug == 1 ]; then echo "OK: official races 1 and "$race_number" are on same date!"; fi 
            fi
            if [ "$route_id" != "$route_id_from_race1" ]; then
                echo "WARNING: official races 1 and "$race_number" are on different routes: -"$route_id"- and -"$route_id_from_race1"-"
            else
                if [ $verbose_debug == 1 ]; then echo "OK: official races 1 and "$race_number" are on same route!"; fi 
            fi
        fi

        echo "<li>  <a href="$url">Official race $race_number: $race_time (GMT)</a>" >> .race.html
        echo "<li>  <a href="$url">Official race $race_number: $race_time (GMT)</a>" >> ../official_race_list_items.html
        let race_number=$race_number+1
    done
    echo "</ul>" >> .race.html

    # contributed races
    ncontrib=`wc -l ../contributed_race_list_items.html | awk '{print $1}'`
    if [ $ncontrib != 0 ]; then
        echo "<ul>" >> .race.html
        cat ../contributed_race_list_items.html >> .race.html
        echo "</ul>" >> .race.html
    fi
    
    # Prepare link to rouvy race ranking (dummy page until race is over and has been processed)
    if [ ! -e ../results.html ]; then
        echo "<h2>Race "$race_number_in_series" : " $day " " ${month_names[${month}]} " " $year "</h2><br>" > ../results.html
        echo "<b>Route:</b> <a href=\"https://my.rouvy.com/virtual-routes/detail/"$route_id_from_race1"\">"$route_title"</a>" >> ../results.html
        echo "<br><br>" >> ../results.html
        echo "Contributing races:" >> ../results.html
        echo "<ul>"  >> ../results.html
        cat ../official_race_list_items.html >> ../results.html
        cat ../contributed_race_list_items.html >> ../results.html
        echo "</ul>"  >> ../results.html
        echo "Race hasn't been raced or processed yet!<br>" >> ../results.html
    fi

    # Provide link in summary file -- either to race results (if they've been processed)
    # or to option to add private race
    not_processed_yet_count=`grep -c "Race hasn't been raced or processed yet!" ../results.html`
    if [ $not_processed_yet_count != 0 ]; then
        # Undo increment from above
        let race_number=$race_number-1
	# https://rocketvalidator.com/html-validation/bad-value-x-for-attribute-href-on-element-a-illegal-character-in-query
	route_title_with_padded_space=`echo $route_title | sed 's/ /%20/g' | sed 's/|/%7C/g' | sed 's/\[/%5B/g' | sed 's/&gt;/__rvy_padding_gt_sign_rvy_padding__/g' `
	echo "hierher: old " $route_title
	echo "hierher: new " $route_title_with_padded_space
	# hierher echo $route_title_with_padded_space | sed 's/&gt;/__rvy_padding_gt_sign_rvy_padding__/g'

	find_most_popular_race_php_string="'../../html/find_most_popular_race.php?route_id="$route_id_from_race1"&route_title="$route_title_with_padded_space"&race_number="$race_number_in_series"&race_series="$race_series"&race_date_string="$orig_day"%20"${month_names[${month}]}"%20"$year"'"
	echo "find_most_popular_race_php_string : "$find_most_popular_race_php_string

	
	
        echo "Race not raced/processed yet!<br><br><div style=\"font-size:small;\"><a class=\"select_league_table_buttons\" href=\"../../html/input_user_contributed_race_form.php?route_id="$route_id_from_race1"&route_title="$route_title_with_padded_space"&race_number="$race_number_in_series"&race_series="$race_series"&race_date_string="$orig_day"%20"${month_names[${month}]}"%20"$year"\">Add your own?</a><a class=\"select_league_table_buttons\" href=\"javascript:javascript:void(0)\" onClick=\"javascript:display_cyclist_while_loading_most_popular_route($find_most_popular_race_php_string)\">Find the most popular race</a></div>" >> .race.html # Note: needs to be relative, so it's accesible from var/www etc. not absolute

	#echo "Race not raced/processed yet!<br><br><div style=\"font-size:small;\"><a class=\"select_league_table_buttons\" href=\"../../html/input_user_contributed_race_form.php?route_id="$route_id_from_race1"&route_title="$route_title_with_padded_space"&race_number="$race_number_in_series"&race_series="$race_series"&race_date_string="$orig_day"%20"${month_names[${month}]}"%20"$year"\">Add your own?</a><a class=\"select_league_table_buttons\" href=\"../../html/find_most_popular_race.php?route_id="$route_id_from_race1"&route_title="$route_title_with_padded_space"&race_number="$race_number_in_series"&race_series="$race_series"&race_date_string="$orig_day"%20"${month_names[${month}]}"%20"$year"\">Find the most popular race</a></div>" >> .race.html # Note: needs to be relative, so it's accesible from var/www etc. not absolute 
	
    else
        race_results_file=`basename $dir`/results.html
        echo "<div style=\"font-size:small;\"><a class=\"select_league_table_buttons\" href=\"$race_results_file\">Race results</a></div>" >> .race.html
    fi
    echo "</div>" >> .race.html
    
    # Add to race info for overall series (reverse order)
    touch $home_dir/generated_race_data/$race_series/all_races_in_series.html
    mv $home_dir/generated_race_data/$race_series/all_races_in_series.html .tmp
    cat .race.html .tmp >> $home_dir/generated_race_data/$race_series/all_races_in_series.html
    rm -f .tmp
    rm .race.html


    
done



# Tell us what we're doing (on top!)
echo "<div class=\"blurrable_during_popular_race_load\">" > .tmp.txt
echo "<h2>Overall race programme for race series <em>"$race_series"</em></h2>" >> .tmp.txt
echo "Race programme compiled: "`date --utc` >> .tmp.txt
echo "</div>" >> .tmp.txt
echo "<img id=\"most_popular_route_loader\" style=\"display:none;\" src=\"cyclist_displayed_while_finding_most_popular_rides.gif\" alt=\"loader\">" >> .tmp.txt
#echo "<img src=\"cyclist_displayed_while_finding_most_popular_rides.gif\" alt=\"bla\">" >> .tmp.txt
cat .tmp.txt $home_dir/generated_race_data/$race_series/all_races_in_series.html > .tmp2.txt
mv .tmp2.txt $home_dir/generated_race_data/$race_series/all_races_in_series.html


# Tell us what you've done
cd $home_dir
echo "Races staged." 
echo "======================================================================"
echo " "
