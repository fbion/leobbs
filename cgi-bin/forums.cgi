#!/usr/bin/perl
#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

BEGIN {
    $startingtime=(times)[0]+(times)[1];
    foreach ($0,$ENV{'PATH_TRANSLATED'},$ENV{'SCRIPT_FILENAME'}){
    	my $LBPATH = $_;
    	next if ($LBPATH eq '');
    	$LBPATH =~ s/\\/\//g; $LBPATH =~ s/\/[^\/]+$//o;
        unshift(@INC,$LBPATH);
    }
}

use LBCGI;
$LBCGI::POST_MAX=500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
use VISITFORUM qw(getlastvisit setlastvisit);
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/mpic.cgi";
require "bbs.lib.pl";
$|++;
$thisprog = "forums.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else {
    $boardurltemp =$boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
#    $cookiepath =~ tr/A-Z/a-z/;
}
&ipbanned; #��ɱһЩ ip

$jumpto         = $query -> param('jumpto'); if ($jumpto) { print redirect(-location=>"$jumpto"); exit; }
$inforum        = $query -> param('forum');
&error("����̳&�ϴ󣬱��Һ��ҵĳ���ѽ��") if ($inforum !~ /^[0-9]+$/);
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

$action         = $query -> param('action');
$action         = &stripMETA("$action");
$inshow         = $query -> param('show');
$inshow 	= 0 if (($inshow !~ /^[0-9]+$/)||($inshow eq ""));
$deshow         = $query -> param('dshow');
$deshow 	= "" if ($deshow !~ /^[0-9]+$/);
$startarray     = $inshow;
$inthreadages 	= $query -> param('threadages');
$inthreadages   = $defaulttopicshow if ($inthreadages eq "" && $defaulttopicshow ne "");

$inselectstyle  = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
$currenttime = time;
&error("����̳&�Բ��������̳�����ڣ����ȷ������̳����û����ô�����������޸���̳һ�Σ�") if (!(-e "${lbdir}boarddata/listno$inforum.cgi"));

$inshow = int($inshow/$maxthreads+0.5)*$maxthreads;
$inshow = ($deshow-1) * $maxthreads if ($deshow ne "");

$inmembername  = $query -> param('membername');
$inpassword    = $query -> param('password');
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$forumpassword = $query -> param('forumpassword');
if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie");   }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
if ((!$inmembername) or ($inmembername eq "����")) { $inmembername = "����"; }
  else {
#    &getmember("$inmembername");
    &getmember("$inmembername","no");
    &error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
     if ($inpassword ne $password) {
	$namecookie  = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie  = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("��ͨ����&�������û���������������µ�¼��");
     }
    &getlastvisit;
    $forumlastvisit = $lastvisitinfo{$inforum};
    &setlastvisit("$inforum,$currenttime");
}
require "${lbdir}imagead.cgi" if (($forumimagead eq "1")||($useimageadforum eq "1")||($forumimagead1 eq "1")||($useimageadforum1 eq "1"));

$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");
$addtimes           = $timedifferencevalue*3600 + $timezone*3600;
$screenmode  = $query->cookie("screenmode");
$screenmode  = 8 if ($screenmode eq "");
my $onlineview1 = $query->cookie("onlineview");
$onlineview = $onlineview1 if ($onlineview1 ne "");
$onlineview = 0 if ($onlineview eq "");
$onlineview = $onlineview == 1 ? 0 : 1 if ($action eq "onlineview");
$onlineviewcookie = cookie(-name => "onlineview", -value => "$onlineview", -path => "$cookiepath/", -expires => "+30d");
if ($onlineview == 1) { $onlinetitle="[<a href=$thisprog?action=onlineview&forum=$inforum><font color=$titlefontcolor>�ر���ϸ�б�</font></a>]"; }
                 else { $onlinetitle="[<a href=$thisprog?action=onlineview&forum=$inforum><font color=$titlefontcolor>��ʾ��ϸ�б�</font></a>]"; }

&moderator("$inforum");

require "doaccessrequire.pl" if ($action eq "accessrequired");
require "resetposts.pl"      if ($action eq "resetposts");

if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }
$insidead = "" if (($forumimagead ne "1")&&($useimageadforum eq "0")); $insidead1   = "" if (($forumimagead1 ne "1")&&($useimageadforum1 eq "0"));

$inforumcookies = $query->cookie("forumscookies");
if(",$inforumcookies,"!~/,$inforum,/){
$inforumcookies .=",$inforum";}
my $forumscookie= cookie(-name => "forumscookies" , -value => $inforumcookies, -path => "$cookiepath/" ,  -expires => "+30d");
print header(-cookie=>[$allowforumcookie, $onlineviewcookie, $tempvisitcookie, $permvisitcookie ,$forumscookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");


&error("������̳&һ���Ա������������̳��") if (($startnewthreads eq "cert")&&(($membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo" && $membercode ne "amo" && $membercode !~ /^rz/)||($inmembername eq "����"))&&($userincert eq "no"));
&error("������̳&�����̳��û��Ȩ�޽�����̳��") if ($yxz ne '' && $yxz!~/,$membercode,/);
if ($allowusers ne ''){
    &error('������̳&�㲻����������̳��') if (",$allowusers," !~ /,$inmembername,/i && $membercode ne 'ad');
}
if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
    &error("������̳&�㲻����������̳���������Ϊ $rating��������ֻ̳���������ڵ��� $enterminweiwang �Ĳ��ܽ��룡") if ($enterminweiwang > 0 && $rating < $enterminweiwang);
    if ($enterminmony > 0 || $enterminjf > 0 ) {
	require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
	$mymoney1 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
	&error("������̳&�㲻����������̳����Ľ�ǮΪ $mymoney1��������ֻ̳�н�Ǯ���ڵ��� $enterminmony �Ĳ��ܽ��룡") if ($enterminmony > 0 && $mymoney1 < $enterminmony);
	&error("������̳&�㲻����������̳����Ļ���Ϊ $jifen��������ֻ̳�л��ִ��ڵ��� $enterminjf �Ĳ��ܽ��룡") if ($enterminjf > 0 && $jifen < $enterminjf);
    }
}

if ($adlinks ne "") {
    require "doadlinks.pl";
}

$rsshtml = qq~  <a href="rss.cgi/leo.xml?forum=$inforum" target="_blank"><img src="$imagesurl/images/xml.gif" border="0" height=15 align="absmiddle" alt="RSS ���ı���̳"></a>&nbsp;<a href="wap.cgi" target="_blank"><img src="$imagesurl/images/wap.gif" height=15 border="0" align="absmiddle" alt="ͨ���ֻ�������̳����ַ��$boardurl/wap.cgi"></a>~;
if ($enterminmony > 0 || $enterminjf > 0 || $enterminweiwang > 0 || $allowusers ne '') {
    $rsshtml = "";
}
if ($regaccess eq "on") {
    $rsshtml = "";
}
if (($startnewthreads eq "cert")&&($userincert eq "no")) {
    $rsshtml = "";
}
if ($rssinfo eq "no") {
    $rsshtml = "";
}

&title;
if (-e "${lbdir}cache/forumshead$inforum.pl") {
    eval{ require "${lbdir}cache/forumshead$inforum.pl";};
    if ($@) { unlink ("${lbdir}cache/forumshead$inforum.pl");  require "doforumhead.pl"; }
} else { require "doforumhead.pl"; }
$output .= qq~$adlinks<br>$titleoutput<br>~;

$output .= qq~<BGSOUND SRC=$imagesurl/midi/$midiaddr LOOP=-1>~ if ((-e "${imagesdir}midi/$midiaddr")&&($midiaddr ne ""));

if ($canusetreeview ne "no") {
    $output .= qq~<script>
function loadThreadFollows(f_id,t_id){ document.frames["hiddenframe"].location.replace("reply_tree.cgi?forum="+f_id+"&topic="+t_id);}
function loadThreadFollow(f_id,t_id,id_of_topic){
var targetImg =eval("document.images.followImg" + id_of_topic);
var targetDiv =eval("follow" + id_of_topic);
if (targetImg.nofollow <= 0){return false;}
if (typeof(targetImg) == "object"){
if (targetDiv.style.display!='block'){
targetDiv.style.display="block";targetImg.src="$imagesurl/images/cat1.gif";
if (targetImg.loaded=="no"){ document.frames["hiddenframe"].location.replace("reply_tree.cgi?forum="+f_id+"&topic="+t_id); }
}else{ targetDiv.style.display="none";targetImg.src="$imagesurl/images/cat.gif"; }
}}
</script>
<iframe width=0 height=0 align=center src="" id=hiddenframe></iframe>
~;
}

$output .= qq~<style>
.ha {color: $fonthighlight; font: bold;}
.hb {color: $menufontcolor; font: bold;}
.dp {padding: 4px 0px;}
.jc {position:relative;}
.ts {BORDER-RIGHT:black 1px solid;PADDING-RIGHT:2px;BORDER-TOP:black 1px solid;PADDING-LEFT:2px;PADDING-BOTTOM:2px;MARGIN-LEFT:18px;BORDER-LEFT:black 1px solid;WIDTH:170px;COLOR:black;PADDING-TOP:2px;BORDER-BOTTOM:black 1px solid;BACKGROUND-COLOR:lightyellow;cursor:hand;}
TABLE {BORDER-TOP: 0px; BORDER-LEFT: 0px; BORDER-BOTTOM: 1px; }
TD {BORDER-RIGHT: 0px; BORDER-TOP: 0px; color: $fontcolormisc; }
</style>
<script>
~;

if ($usefake eq "yes") {
    $output .= qq~
function O1(id) {window.open("topic-$inforum-"+id+"-0-0-.htm");}
function O2(id) {window.open("view-$inforum-"+id+".htm");}
function O5(id1,id2) {window.open("topic-"+id1+"-"+id2+"-.htm");}
function O6(id1,id2) {window.open("view-"+id1+"-"+id2+".htm");}
function O3(id1,id2,id3) {window.open("topic-" + id1 + "-" + id2 + "-" + id3 + "-0-last.htm#bottom", "_self");}
function O4(id) {window.open("forums-"+id+"-0.htm");} 
function O9(id) {if(id!="")window.open("profile-"+id+".htm");}
~;
} else {
    $output .= qq~
function O1(id) {window.open("topic.cgi?forum=$inforum&topic="+id);}
function O2(id) {window.open("view.cgi?forum=$inforum&topic="+id);}
function O5(id1,id2) {window.open("topic.cgi?forum="+id1+"&topic="+id2);}
function O6(id1,id2) {window.open("view.cgi?forum="+id1+"&topic="+id2);}
function O3(id1,id2,id3) {window.open("topic.cgi?forum=" + id1 + "&topic=" + id2 + "&start=" + id3 + "&replynum=last#bottom", "_self");}
function O4(id) {window.open("forums.cgi?forum="+id);} 
function O9(id) {if(id!="")window.open("profile.cgi?action=show&member="+id);}
~;
}

$output .= qq~
var exp = new Date();exp.setTime(exp.getTime() + 30*86400*1000);
if (screen.width <= 800 ){SetCookie('screenmode','5',exp,"$cookiepath/");}
if ((screen.width >800 )&&(screen.width<=1024)){SetCookie('screenmode','8',exp,"$cookiepath/");}
if (screen.width >1024 ){SetCookie('screenmode','10',exp,"$cookiepath/");}
function SetCookie (name, value) { var argv = SetCookie.arguments;var argc = SetCookie.arguments.length;var expires = (argc > 2) ? argv[2] : null;var path = (argc > 3) ? argv[3] : null;var domain = (argc > 4) ? argv[4] : null;var secure = (argc > 5) ? argv[5] : false; document.cookie = name + "=" + escape (value) + ((expires == null) ? "" : ("; expires=" + expires.toGMTString())) + ((path == null) ? "" : ("; path=" + path)) + ((domain == null) ? "" : ("; domain=" + domain)) + ((secure == true) ? "; secure" : ""); } 
</script>
$insidead$insidead1
~;

if ($privateforum eq "yes") {
    $rsshtml = "";
    if ($inmembername eq "����") {
	print "<script language='javascript'>document.location = 'loginout.cgi?forum=$inforum'</script>";
	exit;
    }
    $testentry = cookie("forumsallowed$inforum");
    if ((($testentry eq $forumpass)&&($testentry ne ""))||(($userregistered ne "no")&&($allowedentry{$inforum} eq "yes"))||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) {
	if ($inpassword ne $password) { &error("������̳&��������㲻����������̳��"); }
    } else { require "accessform.pl"; }
}

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
    if ($privateforum ne "yes") {
       &whosonline("$inmembername\t$forumname\t$forumname\t�鿴��̳�ϵ�����");
    } else {
       &whosonline("$inmembername\t$forumname(��)\t$forumname\t�鿴������̳�ϵ�����");
    }
    undef $memberoutput if ($onlineview != 1);
} else {
    unlink ("$filetoopens.lck") if ((-M "$filetoopens.lck") *86400 > 30);
    $memberoutput = "";
    $membertongji = " <B>���ڷ�������æ�����Ա�����̳������������ʱ���ṩ��ʾ��</B>";
    $onlinetitle = "";
}

$nowtime = &shortdate($currenttime + $timeadd);
if ($startnewthreads ne "onlysub") {
    my ($todayforumpost, $todayforumposttime) = split(/\|/,$todayforumpost);
    $todayforumpost = 0 if (($nowtime ne $todayforumposttime)||($todayforumpost eq ""));
    $membertongji .= " ���������� <font color=$fonthighlight><b>$todayforumpost</b></font> ƪ";
    $modoutput = "<B>����̳������ʱ��ȱ&nbsp;</B>" if (!$modoutput);
}

if ($announcements eq 'yes') {
    if (-e "${lbdir}data/announce$inforum.pl") {
        require "${lbdir}data/announce$inforum.pl";
        $announcedisp =~ s/\$forumfontcolor/$forumfontcolor/isg;
	$announcedisp =~ s/\$fonthighlight/$fonthighlight/isg;
    } else {
        $announcedisp=qq~&nbsp;<a href=announcements.cgi?forum=$inforum target=_blank title="��ǰû�й���"><b>��ǰû�й���</b></a>~;
	$announcetemp1 = qq~<img src=$imagesurl/images/announce.gif border=0 alt=����̳��ʱ�޹��棡 width=18>~;
    }
}

$output .= qq~
<SCRIPT FOR=forum EVENT=onclick>a();</SCRIPT>
<table cellpadding=1 cellspacing=0 width=$tablewidth align=center>
<tr><td width=2></td><td align=center width=34>$announcetemp1</td><td width=*>$announcedisp</td><td align=right width=500><p>
<SCRIPT>
function threadmenu(){var URL = document.jump1.threadages.options[document.jump1.threadages.selectedIndex].value;top.location.href = "forums.cgi?forum=$inforum&threadages=" + URL; target = '_self';}
</SCRIPT>
<form action=forums.cgi method=post name=jump1><A href=javascript:JM_setTarget() value='' id=globalTarget><img src=$imagesurl/images/$skin/$wlogo border=0 alt=�鿴����ʹ�õ�ģʽ�� align=absmiddle></a>��
~;

eval{require "data/fname.pl";};
my @inforumcookies=split(/\,/,$inforumcookies);
foreach (@inforumcookies) {
    chomp ; 
    next if ($_ eq '');
    next if ($_ eq $inforum);
    my $a='fname'.$_;
    next if (${$a} eq '');
    $vist_f.="<option value=$_>��-${$a}";
}

if ($usefake eq "yes") {
$output.=qq~ <select onchange="if(this.options[this.selectedIndex].value != '')
window.location=('forums-'+this.options[this.selectedIndex].value+'-0.htm')"><option value=1 style=background-color:\$titlecolor>������ʵİ��...$vist_f</select>
~;
} else {
$output.=qq~ <select onchange="if(this.options[this.selectedIndex].value != '')
window.location=('forums.cgi?forum='+this.options[this.selectedIndex].value)"><option value=1 style=background-color:\$titlecolor>������ʵİ��...$vist_f</select>
~;
}
$output.=qq~
<select name="threadages" onchange="threadmenu()"><option value="all">�鿴���е�����</option><option value="1">�鿴һ���ڵ�����</option><option value="2">�鿴�����ڵ�����</option><option value="7">�鿴һ�����ڵ�����</option><option value="15">�鿴������ڵ�����</option><option value="30">�鿴һ�����ڵ�����</option><option value="61">�鿴�������ڵ�����</option><option value="182">�鿴�����ڵ�����</option><option value="365">�鿴һ���ڵ�����</option>
</select></form></p></td><td align=center width=4></td></tr></table>
<SCRIPT>
function a(){el=event.srcElement;if (el.tagName=='A' && el.target!="_blank") el.target=(globalTarget.value);}
function setVMcookie(vtype){var exp = new Date();exp.setTime(exp.getTime() + (30*86400*1000));SetCookie('viewMode',vtype,exp,"$cookiepath/");}
function JM_setTarget(){globalTarget.value=(globalTarget.value=='_blank')?'':'_blank';globalTarget.children[0].src=(globalTarget.value=='')?'$imagesurl/images/$skin/$wlogo':'$imagesurl/images/$skin/$nwlogo';setVMcookie(globalTarget.value);}
function initViewMode(){viewMode=GetCookie('viewMode');globalTarget.value=(!viewMode)?'':'_blank';globalTarget.children[0].src=(!viewMode)?'$imagesurl/images/$skin/$wlogo':'$imagesurl/images/$skin/$nwlogo';}
initViewMode()
function Jumptopage(form){Jumppage.dshow.value = document.Action.dshow.value; Jumppage.submit();}
</script><center>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor><tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor width=92% $catbackpic><font color=$titlefontcolor>$membertongji�� $onlinetitle</td>
<td bgcolor=$titlecolor width=8% align=center $catbackpic><a href="javascript:this.location.reload()"><img src=$imagesurl/images/refresh.gif border=0 height=12></a></td>
</tr>
~;
$output =~ s/option value=\"$inthreadages\"/option value=\"$inthreadages\" selected/;

if ($onlineview == 1) { $output .= qq~<tr><td colspan=2 bgcolor=$forumcolorone><table cellpadding=1 cellspacing=0>$memberoutput</table></td></tr>~; }

$output .= qq~</table></td></tr></table><SCRIPT>valignend()</SCRIPT><br>~;

my ($forumrule, $editrule);
if (-e "${lbdir}boarddata/forumrule$inforum.cgi") {
   open FILE, "${lbdir}boarddata/forumrule$inforum.cgi";
   $forumrule = <FILE>;
   close FILE;
   require "code.cgi";
   &lbcode(\$forumrule);
   my @testforumrule = split(/\<br\>/i,$forumrule);
   $forumrulelines = @testforumrule;
   $forumrule = qq~<span style="height:64;overflow:auto;padding:2px;color:#000000;width:100%;text-align:left">$forumrule</span>~ if ($forumrulelines > 5);
}

if (($membercode eq "ad")||($membercode eq 'smo')||(",$catemods," =~ /\Q\,$inmembername\,\E/i)||($inmembmod eq "yes")) {
   $editrule = "<a href='forumrule.cgi?forum=$inforum'><img src='$imagesurl/images/a_edit.gif' border=0></a>";
   $forumrule = "Ŀǰû����̳������Ҫ��Ϣ����<a href='forumrule.cgi?forum=$inforum'>����</a>������" unless $forumrule;
}

$output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor><tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor width=92% $catbackpic><font color=$titlefontcolor><B> ��̳������Ҫ��Ϣ</B></td>
<td bgcolor=$titlecolor width=8% align=center $catbackpic>$editrule</td></tr>
<tr><td colspan=2 bgcolor=$forumcolorone>$forumrule</td></tr>
</table></td></tr></table><SCRIPT>valignend()</SCRIPT><br>
~ if ($forumrule);

if (($inshow eq 0)&&($#childforum >= 0)) { require "getcforms.pl"; }

if ($startnewthreads ne "onlysub") {  #�Ǵ�����̳���Ͳ�����ʾ

if (($xzbopen ne "no")&&($startnewthreads ne "no")&&($privateforum ne "yes")) { require "forumxzb.pl";}

if (($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) {
    $admindisp = $query->cookie('admindisp');
    $admini = $admindisp eq '' ? '����' : '��ʾ';
    $admini = qq~<img src=$imagesurl/images/icon.gif width=14> <b><span style=cursor:hand onClick=javascript:showadmini()><font color=$fonthighlight id=admini0 title=�����Ƿ���ʾ�������ٲ�����>$admini��������</font></span><span id=admini style="display:$admindisp"></span></b>��~;
    $multimanage  = qq~<td bgcolor=$titlecolor width=25 align=center $catbackpic><font color=$titlefontcolor><b>ѡ</b></td>~;
    $multimanageitem = qq~<td align=center><input type="button" name="chkall" value="ȫѡ" onclick="CheckAll(this.form)"><input type="button" name="clear2" value="��ѡ" onclick="FanAll(this.form)"><input type="reset" name="Reset" value="����"><BR><input type=button name=lock value="��" OnClick="LockThreads(this.form)"><input type="submit" name="delete" value="ɾ" onClick="SetAction('delete')"><input type="submit" name="move" value="��" onClick="SetAction('movetopic')"><input type="button" name="jinghua" value="��" onClick="AddToJingHua(this.form)"></td>~;
    $output .= qq~<script language="JavaScript">
function CheckAll(form){for (var i=0;i<form.elements.length;i++){var e = form.elements[i];e.checked = true;}}
function FanAll(form){for (var i=0;i<form.elements.length;i++){var e = form.elements[i];if (e.checked == true){ e.checked = false; }else { e.checked = true;}}}
function SetAction(A){Action.action.value=A;}
function AddToJingHua(form){JingHua.topic.value='';for (var i=0;i<form.elements.length;i++){var e = form.elements[i];if (e.checked == true && e.name == 'topic'){JingHua.topic.value+=e.value+" "; }}JingHua.submit();}
function LockThreads(form){Lock.topic.value = "";for (var i = 0; i < form.topic.length; i++){var e = form.topic[i];if (e.checked == true) Lock.topic.value += e.value + " ";}Lock.submit();}
function showadmini(){
var exp = new Date();
exp.setTime(exp.getTime() + (24 * 3600 * 1000));
for (var i = 0; i < admini.length; i++){
var e = admini[i];
if (e.style.display == ""){
if (i == 0) if (confirm('�Ƿ�Ҫһֱ���ذ���������')) SetCookie('admindisp', 'none', exp, "$cookiepath/");
e.style.display = "none";admini0.innerText = "��ʾ��������";
}else{
if (i == 0) if (confirm('�Ƿ�Ҫһֱ��ʾ����������')) SetCookie('admindisp', '', exp, "$cookiepath/");
e.style.display = "";admini0.innerText = "���ذ�������";
}}}
</script>
~;
}

my $freshtime= $query->cookie("freshtime");
if ($freshtime ne "") {
    $autofreshtime = $freshtime*60-1;
    $autofreshtime = 300 if ($autofreshtime < 59);
    $output .= qq~\n<meta http-equiv="refresh" content="$autofreshtime;">~;
}
elsif ($refreshforum eq "on") {
    $autofreshtime = 300 if ($autofreshtime < 59);
    $output .= qq~\n<meta http-equiv="refresh" content="$autofreshtime;">~;
}

if (($privateforum eq "yes")||($xzbopen eq "no")||($startnewthreads eq "no")||($startnewthreads eq "cert")) { $newthreadbutton3 = ""; }
  else { $newthreadbutton3 = qq~<a href=xzb.cgi?action=new&forum=$inforum><img src=$imagesurl/images/$skin/$newxzblogo border=0 alt=����һ��С�ֱ�></a>��~; }
if ($pollopen eq "no") { $newthreadbutton2 = ""; }
  else { $newthreadbutton2 = qq~<a href=poll.cgi?action=new&forum=$inforum><img src=$imagesurl/images/$skin/$newpolllogo border=0 alt=����һ����ͶƱ></a>��~; }
if ($postopen eq "no") { $newthreadbutton1 = ""; }
  else { $newthreadbutton1 = qq~<a href=post.cgi?action=new&forum=$inforum><img src=$imagesurl/images/$skin/$newthreadlogo border=0 alt=����һ��������></a>��~; }
if ($payopen eq "no") { $newthreadbutton4 = ""; }
  else { $newthreadbutton4 = qq~<a href=post.cgi?action=pay&forum=$inforum><img src=$imagesurl/images/$skin/newpay.gif border=0 alt="����һ���½��ף�����֧�����ľ���˵������� http://www.alipay.com/"></a>��~; }
$newthreadbutton = "$newthreadbutton1$newthreadbutton2$newthreadbutton3$newthreadbutton4";

if ($startnewthreads ne "no") { $jinghua    =qq~<img src=$imagesurl/images/icon.gif width=14> <a href=jinghua.cgi?action=list&forum=$inforum><font color=$fonthighlight><B>���澫��</B></font></a>&nbsp;~; }
unless ($look eq "off")       { $lookstyles =qq~<img src=$imagesurl/images/icon.gif width=14> <a href=lookstyles.cgi?forum=$inforum>������ɫ</a>&nbsp;~; }
$forumlog = qq~<img src=$imagesurl/images/icon.gif width=14> <a href=forumlogs.cgi?forum=$inforum><font color=$fonthighlight><B>������־</B></font></a>&nbsp;~;

$output.=qq~
<script language="JavaScript" type="text/javascript">
function Download(ForumNo,TopicNo,ReplyNo){
document.Download.forum.value=ForumNo;
document.Download.topic.value=TopicNo;
document.Download.reply.value=ReplyNo;
document.Download.submit();
}
~;

if ($usefake eq "yes") {
$output.=qq~
function makepage(numberofpages,topicid,forumid){
var j=0;
if (numberofpages <= 11) {
for (var i=1; i <= numberofpages; i++){
j = (i-1) * $maxtopics;
document.write("<a href=topic-"+forumid+"-"+topicid+"-"+j+"-$inshow-.htm class=ha>"+ i +"</a> ");
}}
else{
for (var i=1; i <= 4; i++){
j = (i-1) * $maxtopics;
document.write("<a href=topic-"+forumid+"-"+topicid+"-"+j+"-$inshow-.htm class=ha>"+ i +"</a> ");
}
document.write(" . . . ");
for (var i=numberofpages-1; i <= numberofpages; i++){
j = (i-1) * $maxtopics;
document.write("<a href=topic-"+forumid+"-"+topicid+"-"+j+"-$inshow-.htm class=ha>"+ i +"</a> ");
}}}
~;
} else {
$output.=qq~
function makepage(numberofpages,topicid,forumid){
var j=0;
if (numberofpages <= 11) {
for (var i=1; i <= numberofpages; i++){
j = (i-1) * $maxtopics;
document.write("<a href=topic.cgi?forum="+forumid+"&topic="+topicid+"&start="+j+"&show=$inshow class=ha>"+ i +"</a> ");
}}
else{
for (var i=1; i <= 4; i++){
j = (i-1) * $maxtopics;
document.write("<a href=topic.cgi?forum="+forumid+"&topic="+topicid+"&start="+j+"&show=$inshow class=ha>"+ i +"</a> ");
}
document.write(" . . . ");
for (var i=numberofpages-1; i <= numberofpages; i++){
j = (i-1) * $maxtopics;
document.write("<a href=topic.cgi?forum="+forumid+"&topic="+topicid+"&start="+j+"&show=$inshow class=ha>"+ i +"</a> ");
}}}
~;
}

$output.=qq~
</script>
<table cellpadding=0 cellspacing=0 width=$tablewidth>
<tr><td align=center width=2></td><td>$newthreadbutton</td><td align=right colspan=2>$modoutput&nbsp;</td>
<form action=download.cgi name=Download method=POST target=_blank><input type=hidden name=forum><input type=hidden name=topic><input type=hidden name=reply></form>
<form action=jinghua.cgi method=post name=JingHua><input type=hidden name=action value=add><input type=hidden name=forum value="$inforum"><input type=hidden name=topic></form>
<form action=postings.cgi method=post name=Lock><input type=hidden name=action value="lock"><input type=hidden name=forum value="$inforum"><input type=hidden name=topic></form>
<form action=forums.cgi method=get name=Jumppage><input type=hidden name=forum value="$inforum"><input type=hidden name=dshow><input type=hidden name=threadages value=$inthreadages></form>
</tr></table>
<table cellpadding=0 cellspacing=0 width=$tablewidth><tr><td>$admini$xzb</td><td align=right width=*>$jinghua$forumlog$lookstyles$rsshtml</td><td width=4></td></tr></table>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor>
<form action=delpost.cgi name=Action method=post onsubmit="if ((Action.action.value != 'delete')&&(Action.action.value != 'movetopic')) return false;"><input type=hidden name=forum value="$inforum"><input type=hidden name=action value="">
<tr><td height=1></td></tr></table>
<table cellpadding=0 cellspacing=0 width=$tablewidth height=27 bordercolor=$tablebordercolor border=1 align=center>
<tr><td bgcolor=$titlecolor $catbackpic width=30 align=center><font color=$titlefontcolor><b>״̬</b></td>
<td bgcolor=$titlecolor $catbackpic width=* align=center><font color=$titlefontcolor><b>������</b> (�������Ϊ���ŷ�ʽ�Ķ�)</td>
<td bgcolor=$titlecolor $catbackpic align=center width=78><font color=$titlefontcolor><b>�� ��</b></td>
<td bgcolor=$titlecolor $catbackpic align=center width=60><font color=$titlefontcolor><b>�ظ�/���</b></td>
<td bgcolor=$titlecolor $catbackpic width=193 align=center><font color=$titlefontcolor><b>�� ������ �� | ���ظ���</b></td>
$multimanage</tr></table>
~;

if (-e "${lbdir}cache/forumstop$inforum.pl") {
  eval{ require "${lbdir}cache/forumstop$inforum.pl";};
  if ($@) { unlink ("${lbdir}cache/forumstop$inforum.pl"); unlink ("${lbdir}cache/plcache$inforum\_0.pl"); require "dotop.pl"; unlink ("${lbdir}cache/forumstoptopic$inforum.pl"); }
  $jhdata = "" if ($usejhpoint ne "yes");
} else { require "dotop.pl"; unlink ("${lbdir}cache/forumstoptopic$inforum.pl"); unlink ("${lbdir}cache/plcache$inforum\_0.pl"); }

if ($dispabstop ne "0") {
    @absontop = split(/\_/,$absontopdata);
    $abstopcount = @absontop;
    $absontopdata = "\_$absontopdata\_";
} else {
    $abstopcount = 0;
    $absontopdata = "";
}

if ($dispcattop ne "0") {
    @catontop = split(/\_/,$catontopdata);
    $cattopcount = @catontop;
    $catontopdata = "\_$catontopdata\_";
} else {
    $cattopcount = 0;
    $catontopdata = "";
}

if ($ontopdata ne "") {
    @ontop = split(/\_/,$ontopdata);
    $topcount = @ontop;
    $ontopdata = "\_$ontopdata\_";
}

if (($inthreadages)&&($inthreadages ne "all"))  { $threadagesstart = "&threadages=$inthreadages"; } else { undef $threadagesstart; }

if ((-e "${lbdir}cache/plcache$inforum\_$inshow.pl")&&((-M "${lbdir}cache/plcache$inforum\_$inshow.pl") *86400 < 300)&&($threadagesstart eq "")) {
    open (FILE, "${lbdir}cache/plcache$inforum\_$inshow.pl");
    $topicpages = <FILE>;
    chomp $topicpages;
    ($abstopcount,$cattopcount,$topcount) = split(/\t/,<FILE>);
    @toptopic = <FILE>;
    close(FILE);
    my $topicnum = @toptopic;
    if ($topicnum < 7) { undef @toptopic; undef $topicpages; unlink ("${lbdir}cache/plcache$inforum\_$inshow.pl"); require "doplcache.pl"; }
} else {
    require "doplcache.pl";
}

$output .= qq~<script>
var ns6=document.getElementById&&!document.all
var ie=document.all
var customcollect=new Array()
var i=0
function jiggleit(num){
if ((!document.all&&!document.getElementById)) return;
customcollect[num].style.left=(parseInt(customcollect[num].style.left)==-1)? customcollect[num].style.left=1 : customcollect[num].style.left=-1
}
function init(){
i=0;j=0;
if (ie){
while (i <= ($topcount+$abstopcount+$cattopcount)){
if (eval("document.all.jiggle"+i)!=null) {customcollect[j]= eval("document.all.jiggle"+i);j++;}
i++
}}
else if (ns6){
while (i <= ($topcount+$abstopcount+$cattopcount)){
if (document.getElementById("jiggle"+i)!=null) {customcollect[j]= document.getElementById("jiggle"+i);j++;}
i++
}}
if (customcollect.length==1)
setInterval("jiggleit(0)",120)
else if (customcollect.length>1)
for (y=0;y<customcollect.length;y++){
var tempvariable='setInterval("jiggleit('+y+')",'+'140)'
eval(tempvariable)
}}
window.onload=addSenToEventHandle(window.onload,"init();")
</script>
~;

opendir (DIR, "${imagesdir}$usrdir/$inforum");
@usruploadfile = readdir(DIR);
closedir (DIR);

$topiccount = 0;
$jnum = 0;
$fnum = 0;

if ($tablewidth > 100) {
    if ($tablewidth > 1000) { $topictitlemax = 84; } elsif ($tablewidth > 770) { $topictitlemax = 71; } else { $topictitlemax = 40; }
} else {
    if ($screenmode >=10) { $topictitlemax = 84; } elsif ($screenmode >=8) { $topictitlemax = 71; } else { $topictitlemax = 40; }
}

$threadagelimit = $currenttime - $inthreadages * 86400;
foreach $topic (@toptopic) {
    $addonlength = $canusetreeview ne "no" ? 3 : 0;
    chomp $topic;
    ($topicid, $forumid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $posticon, $posttemp, $addmetype) = split(/\t/,$topic);

    if ($multimanage eq "") { $multimanagebutton = ""; }
	              else  { $multimanagebutton = qq~<td bgcolor=$forumcolortwo align=center width=25><input type=checkbox name=topic value=$topicid></td>~; $addonlength += 2.5; }

    if ($forumid eq $inforum) {
        if ($jhdata =~ /\_$topicid\_/) {
	    $jhimage  = qq~ <img src=$imagesurl/images/$skin/$new_JH align=absmiddle alt=��������>~;
	    $jhbuttom = qq~<a href=jinghua.cgi?action=del&forum=$inforum&topic=$topicid><font color=$titlecolor>ȡ������</font></a>|~;
        } else { $jhimage=""; $jhbuttom = qq~<a href=jinghua.cgi?action=add&forum=$inforum&topic=$topicid><font color=$titlecolor>��</font></a>|~; }
    }
    else { $jhimage=""; $jhbuttom=""; }

    $abslockbuttom = $membercode eq "ad" ? "<a href=postings.cgi?action=abslocktop&forum=$forumid&topic=$topicid><font color=$titlecolor>�ܹ�</font></a>|" : "";
    $catlockbuttom = $membercode eq "ad" || $membercode eq "smo" || ",$catemods," =~ /\Q\,$inmembername\,\E/i ? "<a href=postings.cgi?action=catlocktop&forum=$inforum&topic=$topicid><font color=$titlecolor>����</font></a>|" : "";

    $hllink=($highlight=~m/\_$forumid-$topicid\_/i)?"<a href=postings.cgi?action=lowlight&forum=$forumid&topic=$topicid><font color=$titlecolor>ȡ������</font></a>":"<a href=postings.cgi?action=highlight&forum=$forumid&topic=$topicid><font color=$titlecolor>����</font></a>";

    if (($posticon eq "")||($posticon =~/<br>/i)) {
        $posticon = int(myrand(23));
    	$posticon = "0$posticon" if ($posticon<10);
	$posticon = qq~<img src=$imagesurl/posticons/$posticon.gif border=0 align=absmiddle>~;
    } else{
        $posticon = qq~<img src=$imagesurl/posticons/$posticon border=0 align=absmiddle>~;
    }

    $numberofitems = $threadposts + 1;
    $numberofpages = $numberofitems / $maxtopics;

    $threadpages = "";
    if ($numberofitems > $maxtopics) {
        if ($numberofpages>int($numberofpages)){ $numberofpages = int($numberofpages)+1 ;}
        $gotoendpost = ($numberofpages-1)*$maxtopics;
        $pagestoshow = qq~<font color=$forumfontcolor>����[�� <script>makepage($numberofpages,$topicid,$forumid)</script> ҳ]</font>~;
    } else {
        $gotoendpost = "0";
        $pagestoshow = "";
    }

    if ($inthreadages && ($inthreadages ne "all")&&(($topiccount >= $topcount + $abstopcount + $cattopcount)||($startarray ne 0))) {
	if ($lastpostdate < $threadagelimit) { last; }
    }
    if (!$forumlastvisit) { $forumlastvisit = "0"; }

    if ($startedpostdate > $currenttime - 3600 * $newmarktime) { $topnew = " <img src=$imagesurl/images/$skin/$new_blogo absmiddle>";$addonlength +=2; } else { $topnew = ""; }

    if ((lc($inmembername) eq lc($startedby))&&($nodispown eq "yes")){ $mypost="<img src=$imagesurl/images/$skin/$mypost_blogo title=�ҷ��������> "; $addonlength +=2; } else { $mypost=""; }

    $topicicon = "<img src=$imagesurl/images/$skin/topicnonew.gif border=0>";

    if ($inmembername ne "����") {
        if (($threadposts >= $hottopicmark) && ($forumlastvisit < $lastpostdate))    { $topicicon = "<img src=$imagesurl/images/$skin/topichot3.gif border=0>"; }
        elsif (($threadposts >= $hottopicmark) && ($forumlastvisit > $lastpostdate)) { $topicicon = "<img src=$imagesurl/images/$skin/topichotnonew.gif border=0>"; }
        elsif (($threadposts <  $hottopicmark) && ($forumlastvisit < $lastpostdate)) { $topicicon = "<img src=$imagesurl/images/$skin/topicnew3.gif border=0>"; }
        elsif (($threadposts <  $hottopicmark) && ($forumlastvisit > $lastpostdate)) { $topicicon = "<img src=$imagesurl/images/$skin/topicnonew.gif border=0>"; }
    }

    $threadstate = "poll" if (($posticon =~/<br>/i)&&($threadstate eq ""));
    if (($threadstate eq "poll")||($threadstate eq "pollclosed")) {
	if (open(FILE, "${lbdir}forum$forumid/$topicid.poll.cgi")) {
	    my @allpoll = <FILE>;
            close(FILE);
	    $size = @allpoll;
        } else {
       	    $size = 0;
	}
    }
    if ($threadstate eq "closed") { $topicicon = "<img src=$imagesurl/images/$skin/topiclocked3.gif border=0>"; }
    elsif ($threadstate eq "poll") {
        if ($size >= $hotpollmark) { $topicicon = "<img src=$imagesurl/images/$skin/closedbhot.gif border=0>"; }
	                      else { $topicicon = "<img src=$imagesurl/images/$skin/closedb.gif border=0>"; }
    }
    elsif ($threadstate eq "pollclosed") { $topicicon = "<img src=$imagesurl/images/$skin/closedb1.gif border=0>"; }

    if ($lastpostdate ne "") {
	$lastpostdate = $lastpostdate + $addtimes;
	$lastpostdate = &dateformatshort("$lastpostdate");
    }
    else { $lastpostdate = qq~û��~; }
    
	if ($addtopictime eq "yes") {
	    my $topictime = &dispdate($startedpostdate + $addtimes);
	    $topictitle = "[$topictime] $topictitle";
	}

    $startedpostdate  = $startedpostdate + $addtimes;
    $startedlongdate  = &dateformat("$startedpostdate");
    $startedpostdate  = qq~$startedlongdate~;

    $posttemp         = "(������)" if ($posttemp eq "");

    $topictitletemp   = &lbhz($topictitle,$topictitlemax-6);

    $highlightstyle = $topiccount < $abstopcount && $startarray == 0 ? qq~style="color:$color_of_absontop; font-weight:900"~ : $topiccount < $abstopcount + $cattopcount && $startarray == 0 ? qq~style="color:$color_of_quontop; font-weight:900"~ : $topiccount < $abstopcount + $cattopcount + $topcount && $startarray == 0 ? qq~style="color:$color_of_ontop; font-weight:900"~ : $highlight =~ m/\_$forumid-$topicid\_/ ? qq~style="color:$color_of_hightopic; font-weight:600"~ : "";

    $topictitle = qq~<a href=topic.cgi?forum=$forumid&topic=$topicid&show=$inshow title="$topictitle \n����ʱ�䣺 $startedpostdate \n���ظ��� $posttemp "$highlightstyle t>$topictitletemp</a>~;

    if ($lastposter) {
	if ($lastposter=~/\(��\)/) {
       	    $lastposter=~s/\(��\)//isg;
	    $lastposter = qq~<font color=$postfontcolorone title=��Ϊδע���û�>$lastposter</font>~;
	}
	else {
	    my $lastposterfilename = $lastposter;
	    $lastposterfilename =~ s/ /\_/isg;
	    $lastposterfilename =~ tr/A-Z/a-z/;
	    $lastposter = qq~<span style=cursor:hand onClick="javascript:O9('~ . uri_escape($lastposterfilename) . qq~')">$lastposter</span>~;
	}
    }
    else {$lastposter = qq~--------~;}

    if ($topicdescription) {
	my $topicdescriptiontemp = $topicdescription;
	$topicdescriptiontemp =~s/\s*(.*?)\s*\<a \s*(.*?)\s*\>\s*(.*?)\s*\<\/a\>/$3/isg;
	$topicdescriptiontemp =~s/\<\/a\>//isg;
	if (length($topicdescriptiontemp) > ($topictitlemax-4)) {
	    $topicdescriptiontemp=&lbhz("$topicdescriptiontemp",$topictitlemax);
	    $topicdescription =~s/\<a \s*(.*?)\s*\>\s*(.*?)\s*\<\/a\>/\<a $1\>$topicdescriptiontemp\<\/a\>/isg;
        }
    	$topicdescription = qq~<br>����-=> $topicdescription~;
    }
    
    if (($topiccount >= $abstopcount + $cattopcount)||($startarray ne 0)||($forumid eq $inforum)) {
      my @usruploadfile = grep(/^$inforum\_$topicid(\.|\_)/,@usruploadfile);
      if ($#usruploadfile >= 0 || $addmetype ne "") {
        my @files = grep(/^$inforum\_$topicid\./,@usruploadfile);
        if ($#files >= 0 || $addmetype ne "") {
            if ($addmetype eq "") {
	        my $usrfilename = $files[0]; chomp $usrfilename;
	        ($up_name, $up_ext) = split(/\./,$usrfilename);
	    } else {
	    	$up_ext = $addmetype;
	    }
	    $up_ext =~ tr/A-Z/a-z/;
            $filetype = "unknow";
            $filetype = $up_ext if (-e "${imagesdir}icon/$up_ext.gif");
             
            if (($up_ext eq 'jpg')||($up_ext eq 'gif')||($up_ext eq 'bmp')||($up_ext eq 'png')) { $topictitle ="<img src=$imagesurl/icon/$filetype.gif width=16 alt=\"�����⺬�� $filetype ��ʽ��ͼƬ\" border=0 align=absmiddle></a> ".$topictitle; }
	        elsif ($up_ext eq "swf") { $topictitle ="<img src=$imagesurl/icon/$filetype.gif width=16 alt=\"�����⺬�� $filetype ��ʽ�Ķ���\" border=0 align=absmiddle></a> ".$topictitle; }
	    else {
	        $topictitle ="<img src=$imagesurl/icon/$filetype.gif width=16 align=absmiddle alt=\"�����⺬�С�$filetype�����͵ĸ���\" border=0></a> ".$topictitle;
	    }
            $addonlength += 4;
        }
      }
    }
    if ($numberofpages == 0) { $pagestoshowtemp1 = 0; } elsif ($numberofpages > 11) { $pagestoshowtemp1 = 41; } else { $pagestoshowtemp1 = int($numberofpages)*3.3+7; }
    $totlelength = $pagestoshowtemp1 + length($topictitletemp) + 3 + $addonlength; #���������ܳ���

    if (($membercode eq "ad") || ($membercode eq 'smo') || ($inmembmod eq "yes")) {
    	if ($membercode ne "amo") {
	    $admini = qq~<DIV id=admini style="display:$admindisp" ALIGN=Right><font color=$titlecolor>|$hllink|$jhbuttom$abslockbuttom$catlockbuttom<a href=postings.cgi?action=locktop&forum=$inforum&topic=$topicid><font color=$titlecolor>��</font></a>|<a href=postings.cgi?action=puttop&forum=$inforum&topic=$topicid&checked=yes><font color=$titlecolor>��</font></a>|<a href=postings.cgi?action=putdown&forum=$inforum&topic=$topicid><font color=$titlecolor>��</font></a>|<a href=postings.cgi?action=lock&forum=$inforum&topic=$topicid><font color=$titlecolor>��</font></a>|<a href=postings.cgi?action=unlock&forum=$inforum&topic=$topicid&checked=yes><font color=$titlecolor>��</font></a>|<a href=delpost.cgi?action=delete&forum=$inforum&topic=$topicid><font color=$titlecolor>ɾ</font></a>|<a href=delpost.cgi?action=movetopic&forum=$inforum&topic=$topicid&checked=yes><font color=$titlecolor>��</font></a>|</font>&nbsp;</DIV>~;
	} else {
	    $admini = qq~<DIV id=admini style="display:$admindisp" ALIGN=Right><font color=$titlecolor>|$hllink|<a href=postings.cgi?action=puttop&forum=$inforum&topic=$topicid&checked=yes><font color=$titlecolor>��</font></a>|<a href=postings.cgi?action=putdown&forum=$inforum&topic=$topicid><font color=$titlecolor>��</font></a>|<a href=postings.cgi?action=lock&forum=$inforum&topic=$topicid><font color=$titlecolor>��</font></a>|<a href=postings.cgi?action=unlock&forum=$inforum&topic=$topicid&checked=yes><font color=$titlecolor>��</font></a>|</font>&nbsp;</DIV>~;
	}
    }
    elsif ((lc($inmembername) eq lc($startedby)) && ($inmembername !~ /^����/)) {
	if ($arrowuserdel eq "on") {
           $admini = qq~<DIV id=admini style="display:$admindisp" ALIGN=Right><font color=$titlecolor>���ٲ����� ~;
           $admini .= qq~| <a href=postings.cgi?action=lock&forum=$inforum&topic=$topicid><font color=$titlecolor>������������������˻ظ�</font></a> ~ unless ($threadstate eq "closed");
           $admini .= qq~| <a href=delpost.cgi?action=delete&forum=$inforum&topic=$topicid><font color=$titlecolor>ɾ������</font></a> |</font>&nbsp;</DIV>~;
	}
	else { undef $admini; }
    }
    else { undef $admini; }
    if (($startarray eq 0)&&($topiccount < $topcount + $abstopcount + $cattopcount)) {
        if ($topiccount < $abstopcount) {
    	    if ($membercode eq "ad") {
	        $admini = qq~<DIV id=admini style="display:$admindisp" ALIGN=Right><font color=$titlecolor>|<a href=postings.cgi?action=absunlocktop&forum=$forumid&topic=$topicid&checked=yes><font color=$titlecolor>ȡ���̶ܹ�</font></a>|<a href=postings.cgi?action=abslocktop&forum=$forumid&topic=$topicid><font color=$titlecolor>��</font></a>|$jhbuttom<a href=postings.cgi?action=lock&forum=$forumid&topic=$topicid><font color=$titlecolor>��</font></a>|<a href=postings.cgi?action=unlock&forum=$forumid&topic=$topicid&checked=yes><font color=$titlecolor>��</font></a>|</font>&nbsp;</DIV>~;
            } else { undef $admini; }
            $topicicon = "<img src=$imagesurl/images/$skin/abstop.gif border=0>";
            $topictitle =~ s/\&nbsp\;\"\>/\&nbsp\;\" target=\_blank\>/isg;
            $pagestoshow =~ s/ class=ha\>/ target=\_blank class=ha\>/isg;
            $topictitle = "<font color=$color_of_absontop><B>[����]</B></font> $topictitle";
            if ($abstopshake eq "1") { $topictitle = "<span id=jiggle$jnum class=jc>$topictitle</span>";$jnum++;}
	    elsif ($abstopshake eq "2") { $topictitle =~ s/\ t\>/ id=flashlink$fnum flashtype=0 flashcolor=$color_of_absontop>/s;$fnum++;}
	    elsif ($abstopshake eq "3") { $topictitle =~ s/\ t\>/ id=flashlink$fnum flashtype=1 flashcolor=#cccccc>/s;$fnum++;}
            $totlelength = $totlelength + 5;
            $multimanagebutton = "<td bgcolor=$forumcolortwo width=25>&nbsp;</td>" if ($multimanagebutton ne "");
        }
        elsif ($topiccount < $cattopcount + $abstopcount) {
            if ($membercode eq "ad" || $membercode eq "smo" || ",$catemods," =~ /\Q\,$inmembername\,\E/i) {
                $admini = qq~<div id=admini style="display:$admindisp" align=right><font color=$titlecolor>|<a href=postings.cgi?action=catunlocktop&forum=$forumid&topic=$topicid&checked=yes><font color=$titlecolor>ȡ�����̶�</font></a>|$abslockbuttom<a href=postings.cgi?action=catlocktop&forum=$forumid&topic=$topicid><font color=$titlecolor>��</font></a>|$jhbuttom<a href=postings.cgi?action=lock&forum=$forumid&topic=$topicid><font color=$titlecolor>��</font></a>|<a href=postings.cgi?action=unlock&forum=$forumid&topic=$topicid&checked=yes><font color=$titlecolor>��</font></a>|</font>&nbsp;</div>~;
            } else { $admini = ""; }
            $topicicon = "<img src=$imagesurl/images/$skin/lockcattop.gif border=0>";
            $topictitle =~ s/\ \;\"\>/\ \;\" target=\_blank\>/isg;
            if ($cattopshake eq "1") { $topictitle = "<span id=jiggle$jnum class=jc>$topictitle</span>";$jnum++;}
	    elsif ($cattopshake eq "2") { $topictitle =~ s/\ t\>/ id=flashlink$fnum flashtype=0 flashcolor=$color_of_quontop>/s;$fnum++;}
	    elsif ($cattopshake eq "3") { $topictitle =~ s/\ t\>/ id=flashlink$fnum flashtype=1 flashcolor=#cccccc>/s;$fnum++;}
            $pagestoshow =~ s/ class=ha\>/ target=\_blank class=ha\>/isg;
            $multimanagebutton = "<td bgColor=$forumcolortwo width=25>&nbsp;</td>" if ($multimanagebutton ne "");
        }
        elsif ($topiccount < $topcount + $abstopcount + $cattopcount) {
    	    if (($membercode eq "ad") || ($inmembmod eq "yes") || ($membercode eq 'smo')) {
	        $admini = qq~<DIV id=admini style="display:$admindisp" ALIGN=Right><font color=$titlecolor>|<a href=postings.cgi?action=unlocktop&forum=$inforum&topic=$topicid&checked=yes><font color=$titlecolor>ȡ���̶�</font></a>|$abslockbuttom$catlockbuttom<a href=postings.cgi?action=locktop&forum=$inforum&topic=$topicid><font color=$titlecolor>��</font></a>|$jhbuttom<a href=postings.cgi?action=lock&forum=$inforum&topic=$topicid><font color=$titlecolor>��</font></a>|<a href=postings.cgi?action=unlock&forum=$inforum&topic=$topicid&checked=yes><font color=$titlecolor>��</font></a>|</font>&nbsp;</DIV>~;
      	    } else { undef $admini; }
            $topicicon = "<img src=$imagesurl/images/$skin/locktop.gif border=0>";
            $multimanagebutton = "<td bgcolor=$forumcolortwo width=25>&nbsp;</td>" if ($multimanagebutton ne "");
            if ($topshake eq "1") { $topictitle = "<span id=jiggle$jnum class=jc>$topictitle</span>";$jnum++;}
	    elsif ($topshake eq "2") { $topictitle =~ s/\ t\>/ id=flashlink$fnum flashtype=0 flashcolor=$color_of_ontop>/s;$fnum++;}
	    elsif ($topshake eq "3") { $topictitle =~ s/\ t\>/ id=flashlink$fnum flashtype=1 flashcolor=#cccccc>/s;$fnum++;}
        }
    }
    $topictitle = "$mypost$topictitle";
    $topictitle .= $topnew;
    $topictitle .= $jhimage;
    $topictitle=$topictitle."<BR>" if ($totlelength > $topictitlemax+7);

#    if ($threadviews > 9999) { $threadviewstemp = "<font color=$forumfontcolor title=�����$threadviews>>Max</font>"; } else { $threadviewstemp = "<font color=$forumfontcolor>$threadviews</font>"; }
#    if ($threadposts > 9999) { $threadpoststemp = "<font color=$forumfontcolor title=�ظ���$threadposts>>Max</font>"; } else { $threadpoststemp = "<font color=$forumfontcolor>$threadposts</font>"; }

if ($threadposts < 1000 && $threadviews < 1000) { $threadposts = "$threadposts "; $threadviews = " $threadviews"; }

    $startedbyfilename = $startedby;
    $startedbyfilename =~ s/ /\_/isg;
    $startedbyfilename =~ tr/A-Z/a-z/;

    if (($threadstate eq "poll")||($threadstate eq "pollclosed")) { $outputtemp = qq~<td bgcolor=$forumcolortwo align=center width=60 TITLE="�ظ���$threadposts ƪ\n�����$threadviews ��"><font color=$forumfontcolor>�� $size Ʊ</font></td>~; } else { $outputtemp = qq~<td bgcolor=$forumcolortwo align=center width=60><font color=$forumfontcolor>$threadposts<font color=$fonthighlight>/</font>$threadviews</td>~; }
    if ($startedby=~/\(��\)/) { $startedby=~s/\(��\)//isg; $startedby=qq~<font color=$postfontcolorone title=��Ϊδע���û�>$startedby</font>~; } else { $startedby=qq~<span style=cursor:hand onClick=javascript:O9('~ . uri_escape($startedbyfilename) . qq~')>$startedby</span>~; }
    if (($startarray eq 0)&&($topiccount < $abstopcount + $cattopcount)) {
	$topicicontemp = qq~<span style=cursor:hand onClick=javascript:O5($forumid,$topicid)>$topicicon</span>~;
	$posticontemp  = qq~<span style=cursor:hand onClick=javascript:O6($forumid,$topicid)>$posticon</span>~;
    }
    else {
	$topicicontemp = qq~<span style=cursor:hand onClick=javascript:O1($topicid)>$topicicon</span>~;
	$posticontemp  = qq~<span style=cursor:hand onClick=javascript:O2($topicid)>$posticon</span>~;
    }
    #������
    if ($canusetreeview ne "no") {
        if ($threadposts > 0) { $nofollow = "cat.gif"; } else { $nofollow = "cat1.gif"; }
        $id_of_this_topid = sprintf("%04d%05d",$forumid,$topicid);
        $followImg=qq(<img id=followImg$id_of_this_topid title=չ�������� style=CURSOR:hand onclick=loadThreadFollow($forumid,$topicid,'$id_of_this_topid') src=$imagesurl/images/$nofollow width=9 loaded=no nofollow=$threadposts> );
    }
    else { undef $followImg; }

    $output .=qq~<table cellspacing=0 cellpadding=0 width=$tablewidth bordercolor=$tablebordercolor border=1 height=35><tr><td align=center width=30 bgcolor=$forumcolorone>$topicicontemp</td>
<td width=* class=dp bgColor=$forumcolortwo onmouseover=this.bgColor='$forumcolorone'; onmouseout=this.bgColor='$forumcolortwo';>&nbsp;$posticontemp $followImg<span id=forum>$topictitle$pagestoshow$topicdescription$admini</span></td>
<td align=center width=78 bgcolor=$forumcolorone>$startedby</td>$outputtemp<td width=193 bgcolor=$forumcolorone>&nbsp;<span style=cursor:hand onClick=javascript:O3($forumid,$topicid,$gotoendpost)>$lastpostdate</span><font color=$fonthighlight> | </font>$lastposter</td>$multimanagebutton</tr></table>
~;

    $output .=qq~<table cellspacing=0 width=$tablewidth bordercolor=$tablebordercolor border=1 id=follow$id_of_this_topid style=DISPLAY:none><tr><td id=followTd$id_of_this_topid><DIV class=ts onclick=loadThreadFollow($forumid,$topicid,'$id_of_this_topid')>���ڶ�ȡ�����Ժ� ...</DIV></td></tr></table>~ if ($canusetreeview ne "no");
    $topiccount++;
}
$pn = ($inshow/$maxthreads)+1;
$output .= qq~</tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT><table cellpadding=0 cellspacing=2 width=$tablewidth><tr height=4></tr><tr><td>$topicpages��<b>ת��</b>��<input type=text name="dshow" size=2 value="$pn"> <input type=button value=Go onClick="Jumptopage(this.form)"><BR> [���湲������ <B>$threads</B> ƪ���ظ� <b>$posts</b> ƪ]</td>$multimanageitem</form>~;

if (($indexforum ne "no")&&($dispjump ne "no")) {
    require "${lbdir}data/forumjump.pl" if (-e "${lbdir}data/forumjump.pl");
    $jumphtml =~ s/\<\!\-\-h (.+?) \-\-\>/$1/isg if (($disphideboard eq "yes")||($membercode eq "ad")||($membercode eq "smo")||($membercode eq "cmo")||($membercode eq "mo")||($membercode eq "amo"));
    $jumphtml =~ s/\<\!\-\-c (.+?) \-\-\>/$1/isg if ($dispchildjump ne "no");
    $jumphtml = "<tr><td align=right>$jumphtml</td></form>";
} else { $jumphtml = ""; }

$output .= qq~<td align=right><table cellpadding=0 cellspacing=2>~;
$output .= qq~<tr><td align=right><form action=search.cgi method=post><input type=hidden name=action value=startsearch><input type=hidden name=POST_SEARCH value=topictitle_search><input type=hidden name=NAME_SEARCH value=topictitle_search><input name=SEARCH_STRING value=����ؼ��� onfocus="this.value ='';" size=14><select name=TYPE_OF_SEARCH><option value="keyword_search">����<option value="username_search">����</select><input type=hidden name=FORUMS_TO_SEARCH value=$inforum> <input type=submit value=����></td></form></tr>~ if ($searchopen ne "99");
$output .= qq~$jumphtml</table></td></tr></table></tr></table><br>~;

if ($usefastpost ne "no") { require "forumfastpost.pl"; }
}
else {

if (($indexforum ne "no")&&($dispjump ne "no")) {
    require "${lbdir}data/forumjump.pl" if (-e "${lbdir}data/forumjump.pl");
    $jumphtml =~ s/\<\!\-\-h (.+?) \-\-\>/$1/isg if (($disphideboard eq "yes")||($membercode eq "ad")||($membercode eq "smo")||($membercode eq "cmo")||($membercode eq "mo")||($membercode eq "amo"));
    $jumphtml =~ s/\<\!\-\-c (.+?) \-\-\>/$1/isg if ($dispchildjump ne "no");
    $jumphtml = "<tr><td align=right>$jumphtml</td></form>";
} else { $jumphtml = ""; }

$output .= qq~<table cellpadding=1 cellspacing=0 width=$tablewidth><tr><td align=right>$jumphtml</td></tr></table>~;
$output .= "<BR><center><font color=$fonthighlight><B>�����Ǵ�����̳��飬��ѡ�������Ӧ����̳</B></font><BR><BR><BR>";
}
if (($dispview eq "yes")||(($membercode eq "ad" || $inmembmod eq "yes" || $membercode eq 'smo')&&($membercode ne 'amo'))) { require "dodispviewforum.pl"; }

&output("$forumname",\$output);
exit;
