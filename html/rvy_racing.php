<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
    <title>Rvy_racing</title>
    <link rel="stylesheet" href="css/style.css">
    <script src="js/script.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
  </head>
  <body>

    <img class="tabImage" src="rvy_racing.png" alt="rvy_racing logo">
    <input type="radio" name="tabs" id="tab1" checked>
<label for="tab1">Welcome</label><input type="radio" name="tabs" id="tab2">
<label for="tab2">The rules</label><input type="radio" name="tabs" id="tab3">
<label for="tab3">Races</label><input type="radio" name="tabs" id="tab4">
<label for="tab4">League Table</label><input type="radio" name="tabs" id="tab5">
<label for="tab5">Contact/FAQ</label>

<!-- <input type="radio" name="tabs" id="tab6" /><label for="tab6">Contact</label> -->


<div class="tab content1">


  <center>
    <div style="border: 1px solid black; background-color:rgb(250,250,250); border-radius:10px;   box-shadow: 4px 4px lightgray; padding: 10px; width:60%;">
	  <h3>(Watt-)Monster of the Month</h3>
    Given that people may join this group at random points in the
    season it seems unfair to have them linger at the end of the league table forever, so here's
	  a new feature: the "(Watt-)Monster of the Month" competition, a mini-league table extracted from all the races in a given month. Now you can experience the end-of-season madness every month. Yay!  
	  <?php
           if (1==0)
           {
           echo "<p><center><b>[(Watt-)Monster of the Month results will appear here when the first race has been processed.]</b></center></p>";}
           else {
           $race_series="rvy_racing";
	   $month_list=["Oct","Nov","Dec","Jan","Feb","Mar"];
	   #$month_list=["May","Jun","Jul","Aug","Sep"];
	   echo "<ul>";
           foreach ($month_list as $my_month)
	  {
	  $glob_string="../".$race_series."_".$my_month."*/league_table.html";
	  $result_file_list = glob($glob_string);
	  if (count($result_file_list)>1)
	  {
	    echo "Error: Too many entries in result file list: ".$result_file_list;
	    //die();
	  }
	  if (count($result_file_list)<1)
	  {
	    //echo "ERROR: No league tables yet, so there are no monthly league tables either!\n";
	  }	  
	  foreach ($result_file_list as $result_file)
	  {
	  //echo "result file = ".$result_file."<br>";
	  $string_length=strlen($result_file);
	  $year_start=$string_length-22;
		   $year=substr($result_file,$year_start,4);
		   $month_start=$string_length-26;
		   $month=substr($result_file,$month_start,3);
		   echo "<li style=\"text-align:left;\"><a href=\"$result_file\">".$month." ".$year."</a> <br>";
		   }
		   }
		   echo "</ul>";
}?>
Related to this: Feel free to join our races any time to try it out. There's no password
protection, so just turn up. If you then decide to join us (see below for instructions)
your previous efforts will be incorporated retrospectively next time the league table is
updated. 
    </div>
    </center>
      
    <h1>Rvy Racing: Welcome</h1>
    This is the official homepage of Rvy Racing - short for, yes, you
    guessed it: "Rouvy Racing".
    <br><br>The abbreviation is a meek attempt
    to avoid trouble with
    <a href="https://www.rouvy.com">Rouvy</a>'s legal department, and we
    should stress that this site is not affiliated
    with or endorsed by them; we're simply using their great platform 
    to host our races. <br><br>
    The group emerged from
    <a href="https://www.robirini66.com">RBF</a>, originally
    set up by Robi Rini, but discontinued when he moved to
    <a href="https://www.kinomap.com">kinomap</a>.
    <br><br>
    We're currently doing the Winter Series 23-24 (from
    October-March) with two races a week.
    The final league tables from the previous seasons have now been archived:
    <ul>
      <li><a href="../../rvy_racing_archived_seasons/rvy_racing_winter_22-23/league_table.html">Winter 22-23</a> </li>
      <li><a href="../../rvy_racing_archived_seasons/rvy_racing_summer_23/league_table.html">Summer 23</a> </li>
    </ul>
    If you're interested in joining our race series, please register
    on our <a href="https://www.matthias-heil.co.uk/phpbb/">phpBB
    Discussion Board</a> (see below for detailed instructions). Once we have your rouvy username
    and a few other details (which do not include your credit card number!),
    you will automatically be included in the rankings for each race
    (as DNS if you don't turn up). There's nothing else to do, apart
    from doing the actual racing. Easy (and free!), so do join us.
    And then hammer it -- not so easy...<br><br>
    The schedule of upcoming races, the rankings, and the overall
    league table are available via the tabs above.
    <br>
    <br>
    <hr>
    <br>
    <h3>How to register</h3>
    Here's a step-by-step guide for how to register:
    <ol>
      <li> Go to the discussion board at
        <center><a href="https://www.matthias-heil.co.uk/phpbb/">https://www.matthias-heil.co.uk/phpbb/</a></center>
      <li> Click on "Register" in the top right corner:
        <br><br>
        <center><a href="registration1.jpg"><img class="myImage"
                                                 src="registration1.jpg" alt="registration"
                                                 ></a><br><small>[click on
          screenshot to enlarge]</small></center>
        <br>
        <br>
        [Note: Sometimes there seems to be a problem where upon clicking "submit" in the final step (see below), you're returned to the empty form all over again. Aaaargh! No idea what's 
going on 
there. My offer to register you as proxy still stands. The message board is third-party software and this seems to be an intermittent bug. Will explore. For now: Sorry!]
        <br><br>
      <li> Read the terms and conditions (or not...) and accept:
        <br><br>
        <center><a href="registration2.jpg"><img class="myImage"
                                                 src="registration2.jpg" alt="registration"
                                                 ></a><br><small>[click on
          screenshot to enlarge]</small></center>
        <br>
      <li> Fill in the required details.
        <br><br>      
        <b>Note:</b>
        <br><br>
        <ul>
          <li> Make sure that your chosen username (in the first box)
          doesn't contain any whitespace. So "<em>JoeCool</em>"
            or "<em>Joe_Cool</em>"
            are OK; "<em>Joe Cool</em>" isn't. Other than that you
          can choose what you want.     <br><br>
          <li> The rouvy username is case sensitive, so make sure you enter it
            exactly as specified on rouvy. (Example: If your rouvy
            username is "<em>JoeCool</em>" you won't be recognised (and thus
            won't get any points!) if you enter "<em>joecool</em>"
            here.)
            <br><br>
          <li> Make sure that your email
            address is correct otherwise you'll never find out that your
            registration has been processed.
        </ul>
        <br><br>
        <center><a href="registration3.jpg"><img class="myImage" src="registration3.jpg"
 alt="registration"                                                 ></a><br><small>[click on
          screenshot to enlarge]</small></center>
        <br>
      <li> When you're done it should look a bit like this:
        <br><br>
        <center><a href="registration4.jpg"><img class="myImage" src="registration4.jpg"
   alt="registration"                                               ></a><br><small>[click on
          screenshot to enlarge]</small></center>
        Now press "submit".
        <br><br>
        <li> Wait for your registration to be approved by the race
        organiser. He does sleep (sometimes) so this may not be
        instantaneous, but rest assured that it'll be dealt with as
        soon as possible. You'll receive an email to the email address
        that you specified during the registration.
        <br><br>
        <li> Still can't get it to work? Contact the race organiser
        directly; see the Contact tab for details.
    </ol>
    <br>
    <br>
    <hr>
    <br>
    <h3>Warning:</h3>
    Rouvy do not provide a formal API to their (our!) data, so the 
    information required to maintain our league table is extracted
    from their webpages. There is a good chance
    that the machinery developed to do this will break when they
    move their route and race pages
    from <a href="https://my.rouvy.com">
      https://my.rouvy.com</a> to <a href="https://www.rouvy.com">
      https://www.rouvy.com</a>, and it
    may, in fact, prove impossible to continue this approach. If this
    happens, we may have to suspend the races (or at least their
    transfer to the league table) for a bit. Various possible alternatives
    exist but they'd need to be implemented (quickly) and are not
    super-attractive. Anyway, let's not worry about this just yet... 
</div>



<div class="tab content2">
  
    <h1>Rvy Racing: The rules</h1>

    
<h2>Race rules:</h2>
<ul>
  <li> There will be two races a week, on Wednesday and Saturday
    during "the winter season" which runs from the beginning of October to the
    end of March. The midweek races will be shorter (under an hour); the
    Saturday ones will be a bit longer: between 1 and 2 hours with a bit of
    uphill thrown in... In summer (from the beginning of May to the end
    of September) we only do one race a week on a Wednesday. <br><br>
  <li> Each race will be repeated several times (to cater for different
    timezones). Once the route has been published (typically a week in
    advance) you can sign up for one (or more!) of these
    on <a href="https://my.rouvy.com/onlinerace">Rouvy</a> as usual. 
    Direct links to the races are also provided directly from the race
    tab on this page. This lists
    dates, times, routes, etc. <br><br>
  <li> If none of the official times suit you, you can also arrange
    your own race
    on <a href="https://my.rouvy.com/onlinerace">Rouvy</a>.
    The race must be on
    the same day (in GMT) as the first official race. This gives everybody
    24 hours to do the route. Make sure you follow the link <b>"Add your
      own?"</b> for the appropriate race in the race tab on this page
    <br><br>
    <center><a href="add_your_own.jpg"><img class="myImage" src="add_your_own.jpg"
 alt="add your own race"                                            ></a></center>
    <br>
    This allows our machinery to extract
    the finish time and insert it into the compound ranking. The
    registration page will check that the race is held on the right
    route and on the right day. Note that the link disappears and is
    replaced by the race results once the race has been
    processed. <br><br>Please do not delete races on rouvy once you've
    registered them here. It breaks the scripts! <br><br>Finally,
    there's a "feature" (bug?) which means that races
    can't be added while the race is deemed to be running (i.e. while
    the rouvy webpage displays the elapsed time since the race start). If
    this is the case, a suitable error message is displayed. You
    can upload races before and after the race. If you forget to
    do this while the "Add your own" button is active
    just send an email to the race organiser and he'll do it for you
    retrospectively. <br><br>
  <li> You cannot get credit for individual rides (i.e. rides done outside
    races). This is mainly a technical issue: Rouvy doesn't provide
    script-based access to the finish times for individual rides and maintaining
    spreadsheets by hand is not an option. Sorry. If you absolutely want to ride
    by yourself, create your own race (see above) and password protect it; keep
    the password to yourself and nobody will bother you.<br><br>
  <li> If you participate in multiple instances of a race, your best
    time will count.<br><br>
  <li> Points will be awarded according to the UCI cyclocross scheme:
    40 points for the winner; 30 for second; 25 for third; 20 for
    fourth; 19 for fifth; then decreasing by one for each subsequent
    position (but kindly stopping at zero!).<br><br>
  <li> Crashes of the virtual kind (e.g. rouvy going down during a race;
    connection problems; race results not uploading, or races being deleted
    (see above); etc) will all be treated like real crashes: we'll all be
    sorry, but <em>c'est la vie</em> (as the Germans don't say). <br><br>
  <li> The person with the most points at the end of the "season"
    shall be known as "The Winner". Their
    parents/partners/children/hamsters/...
    will be very very proud of them. Everybody else will have had a
    great time busting their guts twice a week (which is what it's all
    about!). And your parents/partners/children/hamsters/... may still
    be very very proud of you. So there then.
</ul>


<h2>Other rules: Behave yourselves!</h2>
There shouldn't be any need for rules. We're all here to have fun
racing and that's that.
<br><br>
Sadly, past experience shows that there are certain issues that
raise tempers, so to avoid endless (and pointless) discussions, here
are a few rules anyway.
<ol>
  <li> Don't be an idiot. <br><br>
  <li> All races must be for "smart trainers only". Rouvy is the sole judge
  of which trainers fall into that category. <br><br>
  <li> Calibrate your trainer when needed. Most modern trainers don't
    seem to require this any more anyway but if yours does, do it!
    Note that it may even make you faster... <br><br>
  <li> You may have noticed that Rouvy allows you to specify your
    weight. For the implications of this fact you are referred to rule
    1.<br><br>
  <li> Make sure that your average power (W/kg) is displayed on the
    rouvy route pages and that the link to the activity (magnifying
    glass) is accessible.
    The picture below (click on it to magnify) shows how to annoy
    people. Please don't! You may
    have privacy concerns (though I don't know what they would be...) but
    people simply want to be able to convince themselves that other
    racers' data looks plausible. Personally I don't think it's a huge
    deal and I get annoyed about endless "cheater" discussions (see below), but if
    you hide your data, you're raising questions. If you want to keep
    your data hidden, please race elsewhere.
    <br><br>
    <center><a href="nonono.png"><img class="myImage" src="nonono.png"
 alt="nonono"                                      ></a></center>
    <br>
    Similarly, it would be appreciated if you kept your strava profile
                                      public and used a HRM. However,
                                      this will not be
    enforced.<br><br>
  <li> If you sign up for a race on rouvy, please make sure you
  actually turn up (or unregister a.s.a.p., if at all possible). People generally
  like to race with other people, and turning up in the expectation to
  find a proper stampede only to find that half the people couldn't
    actually be bothered is annoying.<br><br>
    Related to this: It would be good if you could sign up
    for the races a.s.a.p. Well attended races tend to attract yet more racers and stampedes
    are more fun than TT-style solo races.<br><br>
  <li> Banter on
  the <a href="https://www.matthias-heil.co.uk/phpbb/">discussion
      board</a>
    is actively encouraged. Taking
    yourself (or this whole thing) too seriously is not. Launching
    debates about possible cheaters (or other rule 1 violators) is
    strictly <em>verboten</em>. If you have any
    concerns, please contact the race organiser (via a private (!) message
    on the <a href="https://www.matthias-heil.co.uk/phpbb/">discussion board</a>), so they
    can have a quiet word (and/or escalate things if necessary; see
    below).
    <br><br>
 <center><a href="private_message.jpg"><img class="myImage" src="private_message.jpg"
   alt="private message"                                   ></a></center>
    <br><br>
  <li> No overtly political etc. discussions because it's likely to create
    tension. This is not censorship -- there are plenty of other forums
    on the internet (or in your local pub!) where you can raise your
    views on such matters and get into lovely slanging matches with
    people you disagree with. But not here, please.  <br><br>
  <li> Regular rule breakers will be dealt with. Somehow. Haven't
    decided yet, but punishment could range from flogging (for minor
    offences) to ejection from the group (for major ones). 
    Let's not go there.<br><br>
  <li> And now go racing! Hard!<br><br>
</ol>

</div>



<div class="tab content3">
  
  <div class="blurrable_during_popular_race_load">
    <h1>Rvy Racing: The races</h1>
  </div>
  <?php readfile("all_races_in_series.html"); ?>

</div>



<div class="tab content4">
  
  <h1>Rvy Racing: The league table</h1>

<span class="row_of_league_table_buttons">
<button id="full_league_table_button" class="select_league_table_buttons" onclick="show_league_table(1)">Full league table</button>
<button id="wed_league_table_button"  class="select_league_table_buttons" style="background-color:lightyellow;" onclick="show_league_table(2)">League table from Wednesday races only</button>
<button id="sat_league_table_button"  class="select_league_table_buttons" style="background-color:lightyellow;" onclick="show_league_table(3)">League table from Saturday races only</button>
</span>

<hr>

<div id="full_league_table_div" style="display:block; font-size:smaller;"> <?php readfile("league_table.html"); ?></div>
<div id="wed_league_table_div" style="display:none; font-size:smaller;"> <?php readfile("league_table_wed.html"); ?></div>
<div id="sat_league_table_div" style="display:none; font-size:smaller;"> <?php readfile("league_table_sat.html"); ?></div>

</div>


<div class="tab content5">
<h1>Rvy Racing: Contact/FAQ</h1>

<h1>Contact</h1>


  <ul>
<li> Please use the <a href="https://www.matthias-heil.co.uk/phpbb/">discussion
      board</a> for, well, for discussions, I guess. Constructive suggestions for improvement, bug
  reports/fixes, are also welcome. <br><br>
  <li >The race organiser can be contacted directly via
  the "Contact us" link on the registration page:
  <br><br>
  <center><a href="contact.jpg"><img class="myImage" src="contact.jpg" alt="contact"
                                      ></a></center>
  <br>
  You don't have to have registered to do this, though you will have
                                      to register if you want to
                                      participate in the races (or
                                      rather: get credit for them!).<br><br> 
<li> Those interested in the coding aspect are welcome to contribute to the
      machinery via
the  <a href="https://github.com/MatthiasHeilManchester/rvy_racing">
    github repository</a>.
</ul>


  <hr>
  
<h1>FAQ</h1>
<ul>
  <li> <h2><b>How to change settings in the profile on the phpBB Discussion
  Forum (e.g. to add your strava url if you forgot to do so when you
  first registered):</b></h2>
  <ul>
  <li> Click on your username (here assumed to be joe_cool) in the top right corner:
    <br><br>
    <center><a href="profile1.jpg"><img class="myImage"
                                             src="profile1.jpg" alt="profile"
                                             ></a><br><small>[click on
        screenshot to enlarge]</small></center>
    <br>
    <br>
  <li> Click on "Profile" in the drop-down menu:
    <br><br>
    <center><a href="profile2.jpg"><img class="myImage"
                                             src="profile2.jpg" alt="profile"
                                             ></a><br><small>[click on
        screenshot to enlarge]</small></center>
    <br>
    <br>
  <li> Click on "Edit Profile" 
    <br><br>
    <center><a href="profile3.jpg"><img class="myImage"
                                             src="profile3.jpg" alt="profile"
                                             ></a><br><small>[click on
        screenshot to enlarge]</small></center>
    <br>
    <br>
  <li> Fill in/update whatever you want to add/change: 
    <br><br>
    <center><a href="profile4.jpg"><img class="myImage"
                                             src="profile4.jpg" alt="profile"
                                             ></a><br><small>[click on
        screenshot to enlarge]</small></center>
    <br>
    <br>
  <li> Don't forget to press the "Submit" button!
    <br>
    <br>
  </ul>
    <li> <h2><b>How to subscribe to a forum (so you get an email when a new
    response is posted):</b></h2>
      <ul>
        <li> Click on the appropriate forum (here the "Races" one):
          <br><br>
          <center><a href="subscribe_to_forum1.jpg"><img class="myImage"
                                              src="subscribe_to_forum1.jpg" alt="subscribe"
                                              ></a><br><small>[click on
              screenshot to enlarge]</small></center>
          <br>
          <br>
        <li> Click on "Subscribe forum" (which, strangely, is already
        ticked, even though you're not subscribed yet!):
          <br><br>
          <center><a href="subscribe_to_forum2.jpg"><img class="myImage"
                                              src="subscribe_to_forum2.jpg" alt="subscribe"
                                              ></a><br><small>[click on
              screenshot to enlarge]</small></center>
	  <br>
	  Now you'll get lots of lovely emails to distract you from your work.
          <br>
          <br>
        <li> Had enough of all these emails? Click on "Unsubscribe
        forum" and you'll be left alone again.
          <br><br>
          <center><a href="subscribe_to_forum3.jpg"><img class="myImage"
                                              src="subscribe_to_forum3.jpg" alt="subscribe"
                                              ></a><br><small>[click on
              screenshot to enlarge]</small></center>
          <br>
          <br>
      </ul>
  </ul>

<center>
  <a href="https://matthias-heil.co.uk/rvy_racing/html/admin.php">Admin menu</a>
</center>

</div>

    

  </body>
  

  
</html>
