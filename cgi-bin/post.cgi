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
$LBCGI::POST_MAX=1024 * 10000;
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 1;
require "code.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "bbs.lib.pl";
require "dopost.pl";

$|++;
$thisprog = "post.cgi";
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

#$addme  = $query->param('addme');
$listmy = $query->param('listmy');

for ('forum','topic','membername','password','action','postno','inshowsignature',
     'notify','inshowemoticons','intopictitle','inshowchgfont',
     'inpost','posticon','inhiddentopic','postweiwang','moneyhidden','moneypost','uselbcode','inwater','floor') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
$intopictitle  =~ s/\\0//isg;
#$intopictitle  =~ s/\\/&#92;/isg;
$intopictitle  = "����������$intopictitle";

$inforum       = $forum;
$intopic       = $topic;
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ����") if ($inforum !~ /^[0-9]+$/);
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }
$maxupload = 300 if ($maxupload eq "");

&error("��ͨ����&������ȷ�ķ�ʽ���ʱ�����") if (($postweiwang > $maxweiwang)&&($inhiddentopic eq "yes"));
$moneymax = 99999 if ($moneymax <=0 || $moneymax >=99999);
$moneypost = int($moneypost) if (($moneypost ne "")&&($moneyhidden eq "yes"));
&error("��ͨ����&����ȷ���������ӵļ۸񣬲�Ҫ���� 1��Ҳ��Ҫ���� $moneymax ��") if ((($moneypost > $moneymax)||($moneypost < 1))&&($moneyhidden eq "yes"));
$inmembername  = $membername;
$inpassword    = $password;
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$inpostno      = $postno;
$innotify      = $notify;
$currenttime   = time;
$postipaddress = &myip();
$inpost        =~ s/LBHIDDEN/LBHIDD\&\#069\;N/sg;
$inpost        =~ s/LBSALE/LBSAL\&\#069\;/sg;
$inpost        =~ s/USECHGFONTE/USECHGFONT\&\#069\;/sg;
$inpost        =~ s/\[DISABLELBCODE\]/\[DISABLELBCOD\&\#069\;\]/sg;
$inpost        =~ s/\[POSTISDELETE=(.+?)\]/\[POSTISDELET\&\#069\;=$1\]/sg;
$inpost        =~ s/\[ADMINOPE=(.+?)\]/\[ADMINOP\&\#069\;=$1\]/sg;
$inpost        =~ s/\[ALIPAYE\]/\[ALIPAY\&\#069\;\]/sg;

$inpost        .=($uselbcode eq "yes")?"":"[DISABLELBCODE]" if ($action eq "addnew" || $action eq "addreply"|| $action eq "addnewpay");
$inpost        .=($inshowchgfont eq "yes")?"[USECHGFONTE]":"" if (($action eq "addnew" || $action eq "addreply"|| $action eq "addnewpay")&&($canchgfont ne "no"));

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie"); }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if($moneyhidden eq "yes" && $cansale ne "no"){ 
    if (open(FILE,"${lbdir}data/cansalelist.cgi")) {
        my $CANSALELIST=<FILE>;
        close(FILE);
        $CANSALELIST=~s/^\t//isg;
        $CANSALELIST=~s/\t$//isg;

	$CANSALELIST =~ s/^([01])\t//;
	if ($CANSALELIST ne "") {
	    my $type = $1;
	    $CANSALELIST="\t$CANSALELIST\t";
	    &error("��ͨ����&�����ܹ��������ӣ�") if (!$type && $CANSALELIST !~/\t$inmembername\t/ || $type && $CANSALELIST =~/\t$inmembername\t/);
	}
    }
}

$inposticon    = $posticon;

&ipbanned; #��ɱһЩ ip

if (($inpostno) && ($inpostno !~ /^[0-9]+$/)) { &error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ������"); }

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

if ($inshowemoticons ne "yes") { $inshowemoticons eq "no"; }
if ($innotify ne "yes")        { $innotify eq "no"; }

if (!(-e "${lbdir}boarddata/listno$inforum.cgi")) { &error ("����������&�Բ��������̳�����ڣ����ȷ������̳����û����ô�����������޸���̳һ�Σ�"); }

if ($inmembername eq "" || $inmembername eq "����" ) {
    $inmembername = "����";
    $userregistered = "no";
} else {
    
    &getmember("$inmembername");
    &error("��ͨ����&���û����������ڣ�") if ($inpassword ne "" && $userregistered eq "no");
     if ($inpassword ne $password && $userregistered ne "no") {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("��ͨ����&�������û���������������µ�¼��");
     }
}

&doonoff;  #��̳�������

$mymembercode=$membercode;
$myrating=$rating;
$myrating="-6" if !($myrating);
$maxpoststr = "" if ($maxpoststr eq 0);
$maxpoststr = 100 if (($maxpoststr < 100)&&($maxpoststr ne ""));

$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&moderator("$inforum");
$myinmembmod = $inmembmod;

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

require "postjs.cgi";

if ($wwjf ne "no") {
    for (my $i=0;$i<$maxweiwang;$i++) {
	$weiwangoption.=qq~<option value=$i>$i</option>~;
    }
    $weiwangoptionbutton=qq~<input type=checkbox name="inhiddentopic" value="yes">���ܴ�����ֻ�Բ����û��ɼ����û�����������Ҫ  <select name=postweiwang>$weiwangoption</select><br>~;
} else {
    undef $weiwangoptionbutton;
}

if ($cansale ne "no") {
    my $cessinfo = " (��ȡ˰��: $postcess%)" if ($postcess ne '' && $postcess >= 1 && $postcess <= 100);
    $salepost = qq~<input type=checkbox name="moneyhidden" value="yes">���۴�����ֻ�и�Ǯ�ſ��Բ鿴���ۼ� <input type="text" name="moneypost" size="5" maxlength="5" value="100"> $moneyname$cessinfo<br>~;
} else {
    undef $salepost;
}

if ($canchgfont ne "no") {
    $fontpost = qq~<input type=checkbox name="inshowchgfont" value="yes">ʹ������ת����<br>~;
} else {
    undef $fontpost;
}

if ($nowater eq "on") { 
    $gsnum = 0 if ($gsnum<=0);
    $nowaterpost =qq~<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>��ˮ����</b></font></td><td bgcolor=$miscbackone><input type="radio" class=1 name="inwater" value="no"> �����ˮ�� <input name="inwater" type="radio" class=1 value="yes" checked> �����ˮ��    [���ѡ�񡰲����ˮ������ظ��������� <B>$gsnum</B> �ֽ�]</td></tr>~;
}

if ($useemote eq "yes") {
    $filetoopen = "$lbdir" . "data/emote.cgi";
    open (FILE, "$filetoopen");
    $emote = <FILE>;
    close (FILE);
}
else { undef $emote; }


$helpurl = &helpfiles("�Ķ����");
$helpurl = qq~$helpurl<img src=$imagesurl/images/$skin/help_b.gif border=0></span>~;

my %Mode = (
    'new'        => \&newthread,
    'reply'      => \&reply,
    'replyquote' => \&replyquote,
    'pay'      => \&pay,
    'copy1'      => \&copy1
);

    if ($arrawpostpic eq "on")      { $postpicstates = "����";}      else { $postpicstates = "��ֹ";}
    if ($arrawpostflash eq "on")    { $postflashstates = "����";}    else { $postflashstates = "��ֹ";}
    if ($arrawpostfontsize eq "on") { $postfontsizestates = "����";} else { $postfontsizestates = "��ֹ";}
    if ($arrawpostsound eq "on")    { $postsoundstates = "����";}    else { $postsoundstates = "��ֹ";}

    if ($postjf eq "yes")    { $postjfstates = "����";}    else { $postjfstates = "��ֹ";}
    if ($jfmark eq "yes")    { $jfmarkstates = "����";}    else { $jfmarkstates = "��ֹ";}
    if ($hidejf eq "yes")    { $hidejfstates = "����";}    else { $hidejfstates = "��ֹ";}

    if ($Mode{$action}) { $Mode{$action}->(); }
    elsif ($action eq "addnew"  )  { &addnewthread; }
    elsif ($action eq "addreply")  { &addreply; }
    elsif ($action eq "addnewpay"  )  { &addnewpay; }
    else { &error("��ͨ����&������ȷ�ķ�ʽ���ʱ�����"); }

&output("$boardname - ��$forumname�ڷ���",\$output);
exit;

sub copy1 {
    require "gettopiccopy.pl";
}

sub pay {
    require "pay.pl";
}

sub addnewpay {
    require "addnewpay.pl";
}

sub addreply {
    if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
        &error("����&��Ļ���Ϊ $jifen��������ֻ̳�л��ִ��ڵ��� $replyminjf �Ĳ��ܻظ���") if ($replyminjf > 0 && $jifen < $replyminjf);
    }
    &error("����&�벻Ҫ���ⲿ���ӱ�����") if (($ENV{'HTTP_REFERER'} !~ /$ENV{'HTTP_HOST'}/i && $ENV{'HTTP_REFERER'} ne '' && $ENV{'HTTP_HOST'} ne '')&&($canotherlink ne "yes"));
    require "dotopicreplay.pl";
}

sub addnewthread {
    if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
        &error("����&��Ļ���Ϊ $jifen��������ֻ̳�л��ִ��ڵ��� $postminjf �Ĳ��ܷ��ԣ�") if ($postminjf > 0 && $jifen < $postminjf);
    }
    &error("����&�벻Ҫ���ⲿ���ӱ�����") if (($ENV{'HTTP_REFERER'} !~ /$ENV{'HTTP_HOST'}/i && $ENV{'HTTP_REFERER'} ne '' && $ENV{'HTTP_HOST'} ne '')&&($canotherlink ne "yes"));
    require "doaddnewtopic.pl";
}

sub replyquote {
    if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
        &error("����&��Ļ���Ϊ $jifen��������ֻ̳�л��ִ��ڵ��� $replyminjf �Ĳ��ܻظ���") if ($replyminjf > 0 && $jifen < $replyminjf);
    }
    require "doreplyquote.pl";
}

sub newthread {
#&getoneforum("$inforum");

if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
    &error("����&��Ļ���Ϊ $jifen��������ֻ̳�л��ִ��ڵ��� $postminjf �Ĳ��ܷ��ԣ�") if ($postminjf > 0 && $jifen < $postminjf);
}

    if ($startnewthreads eq "onlysub") {&error("����&�Բ��������Ǵ�����̳�����������ԣ�"); }
    $tempaccess = "forumsallowed". "$inforum";
    $testentry = $query->cookie("$tempaccess");

    if ((($testentry eq $forumpass)&&($testentry ne ""))||($allowedentry{$inforum} eq "yes")||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }
    if (($privateforum eq "yes") && ($allowed ne "yes")) { &error("����&�Բ�����û���ڴ���̳�з����Ȩ����"); }

    if ($postopen eq "no") { &error("��������&�Բ��𣬱���̳�����������⣡"); }

    if ($deletepercent > 0 && $numberofposts + $numberofreplys > 0 && $membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo" && $membercode ne "amo" && $inmembmod ne "yes") {
	&error("����������&�Բ������ɾ���ʳ�����<b>$deletepercent</b>%������Ա�������㷢�������⣡����ϵ̳�������") if ($postdel / ($numberofposts + $numberofreplys) >= $deletepercent / 100);
    }

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
	if ($privateforum ne "yes") { &whosonline("$inmembername\t$forumname\tnone\t����������\t"); }
	                       else { &whosonline("$inmembername\t$forumname(��)\tnone\t�����µı�������\t"); }
    }
    if ((($onlinetime + $onlinetimeadd) < $onlinepost)&&($onlinepost ne "")&&($membercode ne "ad")&&($membercode ne "smo")&&($membercode ne "cmo")&&($membercode ne "mo")&&($membercode ne "amo")&&($membercode !~ /^rz/))     {  $onlinetime = $onlinetime + $onlinetimeadd; &error("����������&�Բ��𣬱���̳����������ʱ������ $onlinepost ����û��������⣡��Ŀǰ�Ѿ����� $onlinetime �룡<BR>�������ʱ��ͳ�Ʋ���ȷ,�����µ�½��̳һ�μ��ɽ����"); }

    &mischeader("����������");

    if ($emailfunctions eq "on") {
	if ($innotify eq "yes") { $requestnotify = " checked"; } else { $requestnotify = ""; }
	$requestnotify = qq~<input type=checkbox name="notify" value="yes"$requestnotify>�лظ�ʱʹ���ʼ�֪ͨ����<br>~;
    }

    if ($startnewthreads eq "no")        { $startthreads = "�ڴ���̳���µ���������ӻظ�ֻ����̳������������"; }
    elsif ($startnewthreads eq "follow") { $startthreads = "�ڴ���̳���µ�����ֻ����̳��������������ͨ��Աֻ���Ը�����"; }
    elsif ($startnewthreads eq "all")    { $startthreads = "�κ��˾����Է���ͻظ����⣬δע���û��������������գ�"; }
    elsif ($startnewthreads eq "cert")   { $startthreads = "�ڴ���̳���µ�����ֻ����̳������������֤�Ļ�Ա����"; }
    else { $startthreads = "����ע���Ա�����Է���ͻظ����⣡"; }

    $startthreads .= " <B>(�����ڱ��������)</B>" if ($mastpostatt eq "yes");

    if ($emoticons eq "on") {
	$emoticonslink = qq~<li><a href="javascript:openScript('misc.cgi?action=showsmilies',300,350)">����<B>ʹ��</B>�����ַ�ת��</a>~;
	$emoticonsbutton =qq~<input type=checkbox name="inshowemoticons" value="yes" checked>���Ƿ�ϣ��<b>ʹ��</b>�����ַ�ת�������������У�<br>~;
    }

    if ($emoticons eq "on") {
	$output .= qq~<script language="javascript">function smilie(smilietext) {smilietext=' :'+smilietext+': ';if (document.FORM.inpost.createTextRange && document.FORM.inpost.caretPos) {var caretPos = document.FORM.inpost.caretPos;caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? smilietext + ' ' : smilietext;document.FORM.inpost.focus();} else {document.FORM.inpost.value+=smilietext;document.FORM.inpost.focus();}}</script>~;
    }
    if ($htmlstate eq "on")     { $htmlstates = "����"; }     else { $htmlstates = "������"; }
    if ($idmbcodestate eq "on") { $idmbcodestates = "����"; $canlbcode =qq~<input type=checkbox name="uselbcode" value="yes" checked>ʹ�� LeoBBS ��ǩ��<br>~; } else { $idmbcodestates = "������"; $canlbcode= "";}
    if ($useemote eq "no")      { $emotestates = "������"; }  else { $emotestates = "����"; }

    $intopictitle =~ s/^����������//;
    $output .= qq~<script>
var autoSave = false;
function storeCaret(textEl) {if (textEl.createTextRange) textEl.caretPos = document.selection.createRange().duplicate();if (autoSave)savePost();}
function HighlightAll(theField) {
var tempval=eval("document."+theField)
tempval.focus()
tempval.select()
therange=tempval.createTextRange()
therange.execCommand("Copy")}
function DoTitle(addTitle) {
var revisedTitle;var currentTitle = document.FORM.intopictitle.value;revisedTitle = addTitle+currentTitle;document.FORM.intopictitle.value=revisedTitle;document.FORM.intopictitle.focus();
return;}
</script>
<form action=$thisprog method=post name="FORM" enctype="multipart/form-data">
<input type=hidden name=action value=addnew>
<input type=hidden name=forum value=$inforum>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor colspan=2 $catbackpic><font color=$titlefontcolor><b>˭���Է���</b> $startthreads</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>�������</b></font>��
<select name=font onchange=DoTitle(this.options[this.selectedIndex].value)>
<OPTION selected value="">ѡ����</OPTION> <OPTION value=[ԭ��]>[ԭ��]</OPTION><OPTION value=[ת��]>[ת��]</OPTION><OPTION value=[��ˮ]>[��ˮ]</OPTION><OPTION value=[����]>[����]</OPTION><OPTION value=[����]>[����]</OPTION><OPTION value=[�Ƽ�]>[�Ƽ�]</OPTION><OPTION value=[����]>[����]</OPTION><OPTION value=[ע��]>[ע��]</OPTION><OPTION value=[��ͼ]>[��ͼ]</OPTION><OPTION value=[����]>[����]</OPTION><OPTION value=[����]>[����]</OPTION><OPTION value=[����]>[����]</OPTION>
</SELECT></td><td bgcolor=$miscbackone><input type=text size=60 maxlength=80 name="intopictitle" value="$intopictitle">�����ó��� 40 ������</td></tr>$nowaterpost
    ~;
    &posttable(1);
}

sub reply {
#&getoneforum("$inforum");
    &moderator("$inforum");
    $tempaccess = "forumsallowed". "$inforum";
    $testentry = $query->cookie("$tempaccess");
    if (($allowedentry{$inforum} eq "yes")||(($testentry eq $forumpass)&&($testentry ne ""))||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }
    if (($privateforum eq "yes") && ($allowed ne "yes")) { &error("����&�Բ������������ڴ���̳����");}
    if ($postopen eq "no") { &error("�����ظ�����&�Բ��𣬱���̳���������ظ����⣡"); }
    &error("��ͨ����&���˲��ܲ鿴�������ݣ���ע����¼������") if (($guestregistered eq "off")&&($inmembername eq "����"));

    open(FILE, "${lbdir}forum$inforum/$intopic.thd.cgi");
    @threads = <FILE>;
    close(FILE);
    $posttoget = $inpostno - 1;
    ($membername, $topictitle, $postipaddress, $showemoticons, $showsignature ,$postdate, $post) = split(/\t/, $threads[$posttoget]);
    $topictitle =~ s/^����������//;

    if ($emoticons eq "on") {
        $emoticonslink = qq~<li><a href="javascript:openScript('misc.cgi?action=showsmilies',300,350)">����<B>ʹ��</B>�����ַ�ת��</a>~;
        $emoticonsbutton =qq~<input type=checkbox name="inshowemoticons" value="yes" checked>���Ƿ�ϣ��<b>ʹ��</b>�����ַ�ת�������������У�<br>~;
    }
    if ($emailfunctions eq "on") {
	if ($innotify eq "yes") { $requestnotify = " checked"; } else { $requestnotify = ""; }
	$requestnotify = qq~<input type=checkbox name="notify" value="yes"$requestnotify>�лظ�ʱʹ���ʼ�֪ͨ����<br>~;
    }

    &mischeader("����ظ�");

    $output .= qq~<script language="javascript">function smilie(smilietext) {smilietext=' :'+smilietext+': ';if (document.FORM.inpost.createTextRange && document.FORM.inpost.caretPos) {var caretPos = document.FORM.inpost.caretPos;caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? smilietext + ' ' : smilietext;document.FORM.inpost.focus();} else {document.FORM.inpost.value+=smilietext;document.FORM.inpost.focus();}}</script>~;

    if ($htmlstate eq "on")     { $htmlstates = "����";     } else { $htmlstates = "������";     }
    if ($idmbcodestate eq "on") { $idmbcodestates = "����"; $canlbcode =qq~<input type=checkbox name="uselbcode" value="yes" checked>ʹ�� LeoBBS ��ǩ��<br>~; } else { $idmbcodestates = "������"; $canlbcode= "";}
    if ($useemote eq "no")      { $emotestates = "������";  } else { $emotestates = "����"; }

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
	if ($privateforum ne "yes") {
     	    &whosonline("$inmembername\t$forumname\tnone\t�ظ�<a href=\"topic.cgi?forum=$inforum&topic=$intopic\"><b>$topictitle</b></a>\t");
	}
	else {
            &whosonline("$inmembername\t$forumname(��)\tnone\t�ظ���������\t");
	}
    }
    if ((($onlinetime + $onlinetimeadd) < $onlinepost)&&($onlinepost ne "")&&($membercode ne "ad")&&($membercode ne "smo")&&($membercode ne "cmo")&&($membercode ne "mo")&&($membercode ne "amo")&&($membercode !~ /^rz/))     {  $onlinetime = $onlinetime + $onlinetimeadd; &error("�ظ�����&�Բ��𣬱���̳����������ʱ������ $onlinepost ����û��ظ����⣡��Ŀǰ�Ѿ����� $onlinetime �룡<BR>�������ʱ��ͳ�Ʋ���ȷ,�����µ�½��̳һ�μ��ɽ����"); }

    $output .= qq~<script>
var autoSave = false;
function storeCaret(textEl) {if (textEl.createTextRange) textEl.caretPos = document.selection.createRange().duplicate();if (autoSave)savePost();}
function HighlightAll(theField) {
var tempval=eval("document."+theField)
tempval.focus()
tempval.select()
therange=tempval.createTextRange()
therange.execCommand("Copy")}
</script>
<form action="$thisprog" method=post name="FORM" enctype="multipart/form-data">
<input type=hidden name="action" value="addreply">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor colspan=2 $catbackpic><font color=$titlefontcolor><b>�������</b>�� $topictitle</td></tr>
    ~;
    &posttable(2);
    require "dothreadreview.pl";
}

sub posttable {
    my $page = shift;
    $output .= qq~<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>��ǰ����</b><br><li>���������ӵ�ǰ��<BR></font></td><td bgcolor=$miscbackone valign=top>
~;
    open (FILE, "${lbdir}data/lbpost.cgi");
    my @posticondata = <FILE>;
    close (FILE);
    chomp @posticondata;
    my $tempiconnum=1;
    foreach (@posticondata) {
	if ($tempiconnum > 12) {
	    $tempiconnum = 1;
	    $output .= qq~<BR>~;
	}
	$output .= qq~<input type=radio value="$_" name="posticon"><img src=$imagesurl/posticons/$_ $defaultsmilewidth $defaultsmileheight>&nbsp;~;
	$tempiconnum ++;
    }
    if ((($page eq 1)&&($arrowupload ne "off"))||(($page eq 2)&&($allowattachment ne "no"))||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) {
    $uploadreqire = "" if ($uploadreqire <= 0);
    $uploadreqire = "<BR>������Ҫ���� <B>$uploadreqire</B> ƪ(��֤�û�����)" if ($uploadreqire ne "");
	$output .= qq~<script language="javascript">function jsupfile(upname) {upname='[UploadFile$imgslt='+upname+']';if (document.FORM.inpost.createTextRange && document.FORM.inpost.caretPos) {var caretPos = document.FORM.inpost.caretPos;caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? upname + ' ' : upname;document.FORM.inpost.focus();} else {document.FORM.inpost.value+=upname;document.FORM.inpost.focus();}}</script>~;
        $output .= qq~<tr><td bgcolor=$miscbackone><b>�ϴ�������ͼƬ</b> (������� <B>$maxupload</B>KB)$uploadreqire</td><td bgcolor=$miscbackone> <iframe id="upframe" name="upframe" src="upfile.cgi?action=uppic&forum=$inforum&topic=$intopic" width=100% height=40 marginwidth=0 marginheight=0 hspace=0 vspace=0 frameborder=0 scrolling=NO></iframe><br><font color=$fonthighlight>Ŀǰ����:(�粻��Ҫĳ��������ֻ��ɾ�������е���Ӧ [UploadFile$imgslt ...] ��ǩ����)  [<a href=upfile.cgi?action=delup&forum=$inforum target=upframe title=ɾ������δ�������ĸ�����ʱ�ļ� OnClick="return confirm('ȷ��ɾ������δ�������ĸ�����ʱ�ļ�ô��');">ɾ��</a>] </font></font><SPAN id=showupfile name=showupfile></SPAN></td></tr>~;
    }
    $maxpoststr = "(������������ <B>$maxpoststr</B> ���ַ�)" if ($maxpoststr ne "");
    
    $output .= qq~</td></tr><td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>����</b>��$maxpoststr<p>�ڴ���̳�У�<li>HTML ����ǩ: <b>$htmlstates</b><li><a href="javascript:openScript('lookemotes.cgi?action=style',300,350)">EMOTE����ǩ</a>: <b>$emotestates</b><li><a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LeoBBS ��ǩ</a>: <b>$idmbcodestates</b><li>��ͼ��ǩ ��: <b>$postpicstates</b><li>Flash ��ǩ : <b>$postflashstates</b><li>���ֱ�ǩ ��: <b>$postsoundstates</b><li>���ִ�С ��: <b>$postfontsizestates</b><li>������ǩ ��: <b>$postjfstates</b><li>���ֱ�ǩ ��: <b>$jfmarkstates</b><li>���ܱ�ǩ ��: <b>$hidejfstates</b>$emoticonslink</font></td><td bgcolor=$miscbackone>$insidejs<TEXTAREA cols=80 name=inpost id=inpost rows=12 wrap="soft" onkeydown=ctlent() onselect="storeCaret(this);" onclick="storeCaret(this);" onkeyup="storeCaret(this);">$inpost</TEXTAREA><br>
&nbsp; ģʽ:<input type="radio" name="mode" value="help" onClick="thelp(1)">������<input type="radio" name="mode" value="prompt" CHECKED onClick="thelp(2)">��ȫ��<input type="radio" name="mode" value="basic"  onClick="thelp(0)">��������>> <a href=javascript:HighlightAll('FORM.inpost')>���Ƶ�������</a> | <a href=javascript:checklength(document.FORM);>�鿴����</a> | <span style=cursor:hand onclick="document.getElementById('inpost').value += trans()">ת�������峬�ı�</spn><SCRIPT>rtf.document.designMode="On";</SCRIPT> <<
</td></tr></tr>~;
    
    if ($emoticons eq "on") {
	$output .= qq~<tr><td bgcolor=$miscbackone valign=top colspan=2><font color=$fontcolormisc><b>�������ͼ�����������м�����Ӧ�ı���</B></font><br>&nbsp;~;
	if (open (FILE, "${lbdir}data/lbemot.cgi")) {
	    @emoticondata = <FILE>;
	    close (FILE);
	    chomp @emoticondata;
	    $emoticondata = @emoticondata;
	}
	$maxoneemot = 16 if ($maxoneemot <= 5);
	if ($maxoneemot > $emoticondata) {
       	    foreach (@emoticondata) {
		my $smileyname = $_;
		$smileyname =~ s/\.gif$//ig;
		$output .= qq~<img src=$imagesurl/emot/$_ border=0 onClick="smilie('$smileyname');FORM.inpost.focus()" style="cursor:hand"> ~;
	    }
	} else {
	    my $emoticondata = "'" . join ("', '", @emoticondata) . "'";
	    $output .= qq~
<table><tr><td id=emotbox></td></tr></table>
<script>
var emotarray=new Array ($emoticondata);
var limit=$maxoneemot;
var eofpage=ceil(emotarray.length/limit);
var page=0;
function ceil(x){return Math.ceil(x)}
function emotpage(topage){
var beginemot=(page+topage-1)*limit;
var endemot=(page+topage)*limit ;
var out='';
page=page+topage;
if (page != 1) { out += '<span style=cursor:hand onclick="emotpage(-1)" title=��һҳ><font face=webdings size=+1>7</font></span> '; }
for (var i=beginemot;i<emotarray.length && i < endemot ;i++){out += ' <img src=$imagesurl/emot/' + emotarray[i] + ' border=0 onClick="smilie(\\'' + emotarray[i].replace(".gif", "") + '\\');FORM.inpost.focus()" style=cursor:hand> ';}
if (page != eofpage){ out += ' <span style=cursor:hand onclick="emotpage(1)" title=��һҳ><font face=webdings size=+1>8</font></span>'; }
out += '  �� '+ page+' ҳ���ܹ� '+ eofpage+ ' ҳ���� '+emotarray.length+' ��';
out += '  <B><span style=cursor:hand onclick="showall()" title="��ʾ���б���ͼʾ">[��ʾ����]</span></B>';
emotbox.innerHTML=out;
}
emotpage (1);
function showall (){var out ='';for (var i=0;i<emotarray.length;i++){out += ' <img src=$imagesurl/emot/' + emotarray[i] + ' border=0 onClick="smilie(\\'' + emotarray[i].replace(".gif", "") + '\\');FORM.inpost.focus()" style=cursor:hand> ';}emotbox.innerHTML=out;}
</script>
~;
	}
    	$output .= qq~</td></tr>~;
    }
    $output .= qq~<tr><td bgcolor=$miscbacktwo valign=top><font color=$fontcolormisc><b>ѡ��</b><p>$helpurl</font></td>
<td bgcolor=$miscbacktwo><font color=$fontcolormisc>$canlbcode
<input type=checkbox name="inshowsignature" value="yes" checked>�Ƿ���ʾ����ǩ����<br>
$requestnotify$emoticonsbutton$fontpost$weiwangoptionbutton$salepost
</font><BR></td></tr><tr><td bgcolor=$miscbacktwo colspan=2 align=center>
<input type=Submit value="�� ��" name=Submit onClick="return clckcntr();">����<input type=button value='Ԥ ��' name=Button onclick=gopreview()>����<input type="reset" name="Clear" value="�� ��"></td></form></tr></table></tr></td></table>
<SCRIPT>valignend()</SCRIPT>
<form name=preview action=preview.cgi method=post target=preview_page><input type=hidden name=body value=""><input type=hidden name=forum value="$inforum"></form>
<script>
function gopreview(){
document.preview.body.value=document.FORM.inpost.value;
var popupWin = window.open('', 'preview_page', 'scrollbars=yes,width=600,height=400');
document.preview.submit()
}
</script>
    ~;
}

sub addmytopic {
   my ($mode, $cleanmembername, $inforum, $intopic, $topictitle, $currenttime, $posticon) = @_;
   if ($recorddir eq "") {
     opendir (DIRS, "$lbdir");
     my @files = readdir(DIRS);
     closedir (DIRS);
     @files = grep(/^\w+?$/i, @files);
     my @recorddir = grep(/^record/i, @files);
     $recorddir = $recorddir[0];
   }
#   mkdir ("${lbdir}$recorddir", 0777) if (!(-e "${lbdir}$recorddir"));
   mkdir ("${lbdir}$recorddir/$mode", 0777) if (!(-e "${lbdir}$recorddir/$mode"));
   my $filetoopen = $lbdir . "$recorddir/" . $mode . "/" . $cleanmembername . ".cgi";
   my $lockfile = &lockfilename($filetoopen);
   if (!(-e "$lockfile.lck")) {
      &winlock($filetoopen) if ($OS_USED eq "Nt");

      my $oldnum = 0;
      if (-e $filetoopen)
      {
              open(FILE, $filetoopen);
              flock(FILE, 1) if ($OS_USED eq "Unix");
              @oldtopics = <FILE>;
              close(FILE);
              chomp(@oldtopics);
              $oldnum = @oldtopics;
      }
      open (FILE, ">$filetoopen");
      flock(FILE, 2) if ($OS_USED eq "Unix");
      print FILE "$inforum\t$intopic\t$topictitle\t$currenttime\t$posticon\n";
      my $i = 0;
      while ($i < $maxpersontopic - 1 && $i < $oldnum)
      {
              my $tempcontent = shift(@oldtopics);
              last unless ($tempcontent ne "");
              my ($tempinforum, $tempintopic, $temptopictitle, $tempcurrenttime, $tempposticon) = split(/\t/, $tempcontent);
              unless ($tempinforum == $inforum && $tempintopic == $intopic)
              {
                      if ($temptopictitle ne "")
                      {
                              print FILE "$tempinforum\t$tempintopic\t$temptopictitle\t$tempcurrenttime\t$tempposticon\n";
                              $i++;
                      }
              }
      }
      close(FILE);
      &winunlock($filetoopen) if ($OS_USED eq "Nt");
   }
    else {
    	unlink ("$lockfile.lck") if ((-M "$lockfile.lck") *86400 > 30);
    }
}
