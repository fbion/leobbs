#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

$namecookie	   = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
$passcookie 	   = cookie(-name => "apasswordcookie"  , -value => "", -path => "$cookiepath/");
$onlineviewcookie  = cookie(-name => "onlineview"       , -value => "", -path => "$cookiepath/");
$threadcookie 	   = cookie(-name => "threadages"       , -value => "", -path => "$cookiepath/");
$viewcookie 	   = cookie(-name => "viewMode"         , -value => "", -path => "$cookiepath/");
$nodisp    	   = cookie(-name => "nodisp"           , -value => "", -path => "$cookiepath/");
$freshtimecookie   = cookie(-name => "freshtime"        , -value => "", -path => "$cookiepath/");
$selectstylecookie = cookie(-name => "selectstyle"      , -value => "", -path => "$cookiepath/");
$tanchumsgcookie   = cookie(-name => "tanchumsg"        , -value => "", -path => "$cookiepath/");
$lastvisitcookie   = cookie(-name => "lastvisit"        , -value => "", -path => "$cookiepath/");
$templastcookie    = cookie(-name => "templastvisit"    , -value => "", -path => "$cookiepath/");
$catlogcookie      = cookie(-name => "catlog"           , -value => "", -path => "$cookiepath/");
$unioncookie       = cookie(-name => "union"            , -value => "", -path => "$cookiepath/");
$banfreshcookie    = cookie(-name => "banfresh"         , -value => "", -path => "$cookiepath/");
$tecookie	   = cookie(-name => "catlog"           , -value => "", -path => "$cookiepath/");
print header(-cookie=>[$tecookie, $lastvisitcookie, $templastcookie, $catlogcookie, $unioncookie, $banfreshcookie, $onlineviewcookie, $threadcookie, $viewcookie, $nodisp, $freshtimecookie, $selectstylecookie, $tanchumsgcookie, $namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
print qq ~<script>location.href="leobbs.cgi";</script>~;
exit;
1;
