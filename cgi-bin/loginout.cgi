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
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
require "cleanolddata.pl";
$|++;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$thisprog = "loginout.cgi";
$query = new LBCGI;
&ipbanned; #��ɱһЩ ip

if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else {
    $boardurltemp =$boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
#    $cookiepath =~ tr/A-Z/a-z/;
}

$inforum  = $query -> param('forum');
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum) && ($inforum !~ /^[0-9]+$/));
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

for ('inmembername','inpassword','action','CookieDate','onlineview','viewMode','nodispavatar',
'nodispsign','nodispphoto','freshtime','hidden','selectstyle','tanchumsg') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &unHTML("$tp");
    ${$_} = $tp;
}
$hidden = 0 if ($canhidden eq "no");
$CookieDate = "+1d" if ($CookieDate eq "");

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie");   }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

if ($inmembername eq "" || $inmembername eq "����") {
    $inmembername = "����";
    $userregistered = "no";
}
else {
    &error("�û���½&�Բ�����������û��������⣬�벻Ҫ���û����а���\@\#\$\%\^\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]�����ַ���") if ($inmembername =~ /[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]]/);
    &getmember("$inmembername","no");
    &error("�û���¼&�Բ���,�û����������������") if (($inpassword ne $password)&&($action ne "logout"));
    $inmembername = $membername;
}
$memberfilename = $inmembername;
$memberfilename =~ s/ /\_/g;
$memberfilename =~ tr/A-Z/a-z/;
&getoneforum("$inforum");
#&moderator("$inforum");
#&title;
&mischeader("��¼/�˳�");

$output .= qq~<p><SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
~;

if ($action eq "login") {
    &cleanolddata;
    if (($userregistered ne "no") && ($inpassword eq $password)) {
	&whosonline("$inmembername\t��̳��¼\tnone\t��¼��̳\t");
	if ($inforum eq "") { $refrashurl = "leobbs.cgi"; } else { $refrashurl = "forums.cgi?forum=$inforum"; }
	$output .= qq~<tr><td bgcolor=$titlecolor $catbackpic valign=middle align=center><font face="$font" color=$fontcolormisc><b>��л���¼ $inmembername</b></font></td></tr>
<tr><td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
���������<ul><li><a href="$refrashurl">������̳</a>
<meta http-equiv="refresh" content="3; url=$refrashurl">
</ul></tr></td></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;

	if ($boarddispsign eq "no") { $nodispsign="yes"; } else { $nodispsign="no" if !($nodispsign); } 
        	
	$namecookie        = cookie(-name => "amembernamecookie", -value => "$inmembername", -path => "$cookiepath/", -expires => "$CookieDate");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "$inpassword",   -path => "$cookiepath/", -expires => "$CookieDate");
	$onlineviewcookie  = cookie(-name => "onlineview",        -value => "$onlineview",   -path => "$cookiepath/", -expires => "$CookieDate");
	$viewcookie        = cookie(-name => "viewMode",          -value => "$viewMode",     -path => "$cookiepath/", -expires => "$CookieDate");
	$freshtimecookie   = cookie(-name => "freshtime",         -value => "$freshtime",    -path => "$cookiepath/", -expires => "$CookieDate");
	$selectstylecookie = cookie(-name => "selectstyle",       -value => "$selectstyle",  -path => "$cookiepath/", -expires => "$CookieDate");
	$tanchumsgcookie   = cookie(-name => "tanchumsg",         -value => "$tanchumsg",    -path => "$cookiepath/", -expires => "$CookieDate");
	$nodisp            = cookie(-name => "nodisp",            -value => "$nodispavatar|$nodispsign|$nodispphoto", -path => "$cookiepath/", -expires => "$CookieDate");


  	print header(-cookie=>[$onlineviewcookie,$threadcookie,$viewcookie, $nodisp, $freshtimecookie, $selectstylecookie, $tanchumsgcookie, $namecookie,$passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

    }
    else {

	print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

	$output .= qq~<tr><td bgcolor=$titlecolor $catbackpic valign=middle align=center><font face="$font" color=$fontcolormisc><b>��¼����</b></font></td></tr>
<tr><td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>��¼����Ŀ���ԭ��
<ul><li>�������<li>�û�������<li>������<a href=register.cgi?forum=$inforum>ע��</a>�û�</ul></tr></td></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
    }
}
elsif ($action eq "logout") {
   &cleanolddata1;
   if ($inmembername ne "" && $inmembername ne "����") {
    $filetoopen = "$lbdir" . "data/onlinedata.cgi";
    my $filetoopens = &lockfilename($filetoopen);
    if (!(-e "$filetoopens.lck")) {
	&winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	open(FILE,"$filetoopen");
	flock(FILE, 1) if ($OS_USED eq "Unix");
	sysread(FILE, my $onlinedata,(stat(FILE))[7]);
	close(FILE);
	$onlinedata =~ s/\r//isg;

	if (length($onlinedata) >= 80) {
	    my $inmembername1 = $inmembername;
   	    $inmembername1 =~ s/\|/\\\|/isg;
   	    $onlinedata =~ s/(.*)(^|\n)$inmembername1\t(.*?)(\n|$)(.*)/$1$2$5/i;
	    ($savedcometime, $savedtime, undef) = split(/\t/, $3);
	    open(ONLINEFILE,">$filetoopen");
            flock(ONLINEFILE, 2) if ($OS_USED eq "Unix");
            print ONLINEFILE "$onlinedata";
	    close(ONLINEFILE);
	}
	else { unlink("$filetoopen"); }
	&winunlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	require "douplogintime.pl";
        &uplogintime("$inmembername","")
    }
    else {
    	unlink ("$filetoopens.lck") if ((-M "$filetoopens.lck") *86400 > 30);
    }
   }
    $output .= qq~<tr><td bgcolor=$titlecolor $catbackpic valign=middle align=center><font face="$font" color=$fontcolormisc><b>�������Ѿ��˳���̳</b></font></td></tr>
<tr><td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
����ѡ�<ul><li><a href="leobbs.cgi">������̳</a><li><a href=javascript:close();>�ر����������</a></ul></tr></td></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;

	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        $trashcookie       = cookie(-name => "templastvisit",     -value => "", -path => "$cookiepath/");
        $onlineviewcookie  = cookie(-name => "onlineview",        -value => "", -path => "$cookiepath/");
        $viewcookie        = cookie(-name => "viewMode",          -value => "", -path => "$cookiepath/");
        $nodisp            = cookie(-name => "nodisp",            -value => "", -path => "$cookiepath/");
        $freshtimecookie   = cookie(-name => "freshtime",         -value => "", -path => "$cookiepath/");
        $selectstylecookie = cookie(-name => "$selectstyle",      -value => "", -path => "$cookiepath/");
        $tanchumsgcookie   = cookie(-name => "$tanchumsg",        -value => "", -path => "$cookiepath/");
       	$banfreshcookie    = cookie(-name => "banfresh"         , -value => "", -path => "$cookiepath/");
	$treeviewcookie    = cookie(-name => "treeview"         , -value => "", -path => "$cookiepath/");
	$tecookie	   = cookie(-name => "catlog"           , -value => "", -path => "$cookiepath/");


        print header(-cookie=>[$banfreshcookie, $treeviewcookie, $tecookie, $namecookie, $passcookie, $trashcookie,$onlineviewcookie,$viewcookie, $nodisp, $freshtimecookie, $selectstylecookie, $tanchumsgcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

}
else {
    if ($query->cookie("selectstyle")) { $inselectstyle = $query->cookie("selectstyle"); }
    $inselectstyle   = $skinselected if ($inselectstyle eq "");
    if ($query->cookie("viewMode") ne "")  { $checked ="checked"; $checked1 =""; } else { $checked1 ="checked"; $checked =""; }
    if ($query->cookie("tanchumsg") eq "") { $tcchecked ="checked"; $tcchecked1 =""; } else { $tcchecked1 ="checked"; $tcchecked =""; }
    if (($query->cookie("onlineview") == 1)||($query->cookie("onlineview") eq "")) { $online ="checked"; $online1 =""; } else { $online1 ="checked"; $online =""; }
    $nodisp = $query->cookie("nodisp");
    ($nodispavatar, $nodispsign, $nodispphoto)  = split(/\|/,$nodisp);
    if ($nodispavatar eq "yes"){ $checked2 ="checked" ; }

    if ($boarddispsign eq "no") { $checked3 ="checked disabled"; }
    elsif ($boarddispsign eq "noselect" && $nodispsign eq "")    { $checked3 ="checked"; }
    elsif ($boarddispsign eq "noselect" && $nodispsign eq "yes") { $checked3 ="checked"; }
    elsif ($boarddispsign eq "noselect" && $nodispsign eq "no")  { $checked3 ="" ;       }
    elsif ($boarddispsign eq "yes" && $nodispsign eq "")         { $checked3 ="";        }
    elsif ($boarddispsign eq "yes" && $nodispsign eq "yes")      { $checked3 ="checked"; }	
    elsif ($boarddispsign eq "yes" && $nodispsign eq "no")       { $checked3 ="";        }	

    if ($nodispphoto eq "yes") { $checked4 ="checked"; }


    print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
    if ($inmembername ne "����") {
      my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
      $filetoopens = &lockfilename($filetoopens);
      if (!(-e "$filetoopens.lck")) {
	&whosonline("$inmembername\t��̳��¼\tnone\t��¼��̳\t");
      }
    }
    opendir (DIR, "${lbdir}data/skin");
    @skindata = readdir(DIR);
    closedir (DIR);
    my $myskin="";
    @skindata = grep(/\.cgi$/,@skindata);
    $topiccount = @skindata;
    @skindata=sort @skindata;
    for (my $i=0;$i<$topiccount;$i++){
        $skindata[$i]=~s /\.cgi//isg;
        $myskin.=qq~<option value="$skindata[$i]">[ $skindata[$i] ]</option>~;
    }
    if ($canhidden ne "no") {
        $userhidden = qq~<tr><td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>��̳����</b><BR>��ѡ����ĵ�¼��ʾ��ʽ�������ʵ����������˽��</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="radio" name="hidden" value="0" checked id=1> <label for=1>������¼����ʾ�����߻�Ա�б���</label><br>
                <input type="radio" name="hidden" value="1" id=2> <label for=2>�����¼����Ҫ������ʾ�������б���</label><br>
                </font>
                </td></tr>
    ~;
    }
    else { $userhidden = ""; }
$helpurl = &helpnewfiles("���ٵ�¼");
$helpurl = qq~$helpurl<img src=$imagesurl/images/$skin/help_b.gif border=0></span>~;

    $output .= qq~
    <tr>
    <td bgcolor=$titlecolor $catbackpic valign=middle colspan=2 align=center>
    <form action="$thisprog" name="login" method="post" onSubmit="submitonce(this)">
    <input type=hidden name="action" value="login">
    <input type=hidden name="forum" value="$inforum">
    <font face="$font" color=$fontcolormisc><b>�����������û����������¼</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="inmembername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="inpassword"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
    <tr>
    <td bgcolor=$miscbacktwo colspan=2 valign=middle><font face="$font" color=$fontcolormisc><b>��̳��¼ѡ��</b></font></td></tr>
    $userhidden
    <tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>Cookie ѡ��</b><BR> ��ѡ����� Cookie ����ʱ�䣬�´η��ʿ��Է������롣</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="radio" name="CookieDate" value="0" checked id=3> <label for=3>�����棬�ر��������ʧЧ</label> <font color=$fonthighlight>(�����ɵȹ�����������ѡ�����)</font><br>
                <input type="radio" name="CookieDate" value="+1d" id=4> <label for=4>�� �� һ ��</label><br>
                <input type="radio" name="CookieDate" value="+30d" id=5> <label for=5>�� �� һ ��</label><br>
                <input type="radio" name="CookieDate" value="+20y" id=6> <label for=6>�� �� �� ��</label> <font color=$fonthighlight>(�ڼ����ʹ���Լ��ĵ���ʱ�ſ�ѡ�����)</font><br>
                </font>
                </td></tr>
</table></td></tr></table>
~; 
if ($advlogin == 1) { 
$advloginout = "true"; 
$advmode = qq~<td width=50%><INPUT id=advcheck name=advshow type=checkbox value=1 onclick=showadv() checked><span id="advance">�رո߼���¼ѡ��</a></span> </td><td width=50%><input type=submit value="�� ¼" name=submit></td>~;} 
else { 
$advloginout = "none"; 
$advmode = qq~<td width=50%><INPUT id=advcheck name=advshow type=checkbox value=1 onclick=showadv()><span id="advance">��ʾ�߼���¼ѡ��</a></span> </td><td width=50%><input type=submit value="�� ¼" name=submit></td>~;} 
$output .=qq~ 
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center id=adv style="DISPLAY: $advloginout">
 <tr><td>
    <table cellpadding=4 cellspacing=1 width=100%>

<tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>�����б�</b> ��ѡ���������������ʾ��ʽ�����Լӿ���̳��ʾ��</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="radio" name="onlineview" value="1" $online id=9> <label for=9>��ʾ��ϸ����</label><br>
                <input type="radio" name="onlineview" value="0" $online1 id=10> <label for=10>�ر���ϸ����</label><br>
                </font>
                </td></tr>
      <tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>�鿴����</b> ��ѡ����ϲ�õĲ鿴���ӷ�ʽ�����Է����Ķ���</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="radio" name="viewMode" value="" $checked1 id=11> <label for=11>��ԭ���������</label><br>
                <input type="radio" name="viewMode" value="_blank" $checked id=12> <label for=12>���´��������</label><br>
                </font>
                </td></tr>

      <tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>�鿴��������</b> ��ѡ��鿴��������ʱ���Ƿ���ʾ�û�ͷ��ǩ������ͼ��</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="checkbox" name="nodispavatar" value="yes" $checked2 id=13> <label for=13>����ʾ�û�ͷ��</label><br>
                <input type="checkbox" name="nodispsign"   value="yes" $checked3 id=14> <label for=14>����ʾ�û�ǩ��</label><br>
                <input type="checkbox" name="nodispphoto"  value="yes" $checked4 id=15> <label for=15>����ʾ�û���ͼ</label><br>
                </font>
                </td></tr>
		   <tr>
~;
if ($showskin ne "off") {$output.=qq~
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>����趨</b> ��ѡ�������̳���</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
		  <select name="selectstyle">
        <option value="">Ĭ�Ϸ��</option>
	$myskin
        </select>
        </font>
        </td></tr>
~;}
$output.=qq~
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>�ж���Ϣ�Ƿ񵯳���</b> <BR>���������Ա�����˲��������ѡ����Ч��</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="radio" class=1 name="tanchumsg" value="" $tcchecked id=16> <label for=16>��������Ϣ����</label><br>
                <input type="radio" class=1 name="tanchumsg" value="no" $tcchecked1 id=17> <label for=17>����������Ϣ����</label><br>
                </font></td></tr>

<tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>ҳ���Զ�ˢ��ʱ��</b> <BR>���������̳��ҳ�Զ�ˢ�µ�ʱ�䣨���������շ���̳��Ĭ�����ý���ˢ�»��߲�ˢ�£�</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
ÿ�� <input type=text name="freshtime" value="$freshtime" maxlength="2" size="2"> �����Զ�ˢ��һ��

</tr>
</table></td></tr>
<SCRIPT>valignend()</SCRIPT>
<script>
function showadv(){
if (document.login.advshow.checked == true) {
		adv.style.display = "";
		advance.innerText="�رո߼���¼ѡ��"
	}else{
		adv.style.display = "none";
		advance.innerText="��ʾ�߼���¼ѡ��"
	}
}		
function submitonce(theform){
if (document.all||document.getElementById){
for (i=0;i<theform.length;i++){
var tempobj=theform.elements[i]
if(tempobj.type.toLowerCase()=="submit"||tempobj.type.toLowerCase()=="reset")
tempobj.disabled=true
}}}
</script>
</tr></table><img src="" width=0 height=4><BR>
<table cellpadding=0 cellspacing=0 width=$tablewidth align=center>
<tr>
$advmode</form></tr></table></td></tr></table><BR><BR>

~;
}

$inselectstyle =~ s/\(/\\(/isg;
$inselectstyle =~ s/\)/\\)/isg;
$output =~ s/option value=\"$inselectstyle\"/option value=\"$inselectstyle\" selected/;
&output("$boardname - ��¼/�˳�",\$output);
exit;
