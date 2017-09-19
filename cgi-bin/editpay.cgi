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
$LBCGI::POST_MAX=1024 * 1000000;
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "bbs.lib.pl";
require "dopost.pl";

$|++;
$thisprog = "editpay.cgi";
$query = new LBCGI;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$addme=$query->param('addme');

for ('forum','topic','membername','password','action',
     'notify','deletepost','intopictitle','intopicdescription',
     'inpost','inshowemoticons','inshowsignature','checked','movetoid','posticon','inshowchgfont',
     'newtopictitle','inhiddentopic','postweiwang','moneyhidden','moneypost','uselbcode','inwater') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
$inforum       = $forum;
$intopic       = $topic;
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($intopic) && ($intopic !~ /^[0-9 ]+$/));
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if ($inforum !~ /^[0-9 ]+$/);
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

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

$inpostno      = 1;
$innotify      = $notify;
$indeletepost  = $deletepost;
$currenttime   = time;
$inposticon    = $posticon;
$inpost        =~ s/LBHIDDEN/LBHIDD\&\#069\;N/sg;
$inpost        =~ s/LBSALE/LBSAL\&\#069\;/sg;
$inpost        =~ s/\[DISABLELBCODE\]/\[DISABLELBCOD\&\#069\;\]/sg;
$inpost        .=($uselbcode eq "yes")?"":"[DISABLELBCODE]" if($action eq "processedit");
$inpost        =~ s/\[USECHGFONTE\]/\[USECHGFONT\&\#069\;\]/sg;
$inpost        .=($inshowchgfont eq "yes")?"[USECHGFONTE]":"" if (($action eq "processedit")&&($canchgfont ne "no"));
$inpost        =~ s/\[POSTISDELETE=(.+?)\]/\[POSTISDELET\&\#069\;=$1\]/sg;
$inpost        =~ s/\[ADMINOPE=(.+?)\]/\[ADMINOP\&\#069\;=$1\]/sg;
$inpost        =~ s/\[ALIPAYE\]/\[ALIPAY\&\#069\;\]/sg;

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
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

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }
$maxupload = 300 if ($maxupload eq "");

if ($inshowemoticons ne "yes") { $inshowemoticons eq "no"; }
if ($innotify ne "yes")        { $innotify eq "no"; }
if (($inpostno) && ($inpostno !~ /^[0-9]+$/)) { &error("��ͨ����&�벻Ҫ�޸����ɵ� URL��"); }
if (($movetoid) && ($movetoid !~ /^[0-9]+$/)) { &error("��ͨ����&�벻Ҫ�޸����ɵ� URL��"); }

if ($useemote eq "yes") {
    open (FILE, "${lbdir}data/emote.cgi");
    $emote = <FILE>;
    close (FILE);
}
else { undef $emote; }

$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");

if ($inmembername eq "" || $inmembername eq "����" ) {
    $inmembername = "����";
} else {
#    &getmember("$inmembername");
    &getmember("$inmembername","no");
    &error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
     if ($inpassword ne $password) {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("��ͨ����&�������û���������������µ�¼��");
     }
}
require "postjs.cgi";

$maxpoststr = "" if ($maxpoststr eq 0);
$maxpoststr = 100 if (($maxpoststr < 100)&&($maxpoststr ne ""));

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&moderator("$inforum");
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

if ($action eq "edit") { &editform;}
    elsif ($action eq "processedit")  { &processedit;  }
    else { &error("��ͨ����&������ȷ�ķ�ʽ���ʱ�����."); }
    
&output($boardname,\$output);
exit;

sub editform {
    $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    @threads = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

    $posttoget = $inpostno;
    $posttoget--;
    
    ($postermembername, $topictitle, $postipaddress, $showemoticons, $showsignature ,$postdate, $post, $posticon, $water) = split(/\t/, $threads[$posttoget]);
    $topictitle =~ s/^����������//;
    $post =~ s/\<p\>/\n\n/ig;
    $post =~ s/\<br\>/\n/ig;

    &error("����&�Բ��𣬲�����༭ͶƱ���ӣ�") if (($posticon =~ m/<BR>/i)&&($posttoget eq 0));

    &error("����&�Բ���������ǽ�������") unless ($post=~m/\[ALIPAYE\]/);

    if ($noedittime ne '') {
	if (($membercode ne "ad")&&($membercode ne "smo")&&($inmembmod ne "yes")) {
	    &error("�༭����&���� $noedittime Сʱ�������ٱ༭���ӣ�") if(($currenttime - $postdate) > ($noedittime * 3600));
	}
    }

    $inmembmod = "no" if (($membercode eq "amo")&&($allowamoedit ne "yes"));
    if (($membercode ne "ad")&&($membercode ne "smo")&&($inmembmod ne "yes")&&((lc($inmembername) ne lc($postermembername))||($usereditpost eq "no"))) {&error("�༭����&������ԭ���ߡ���̳����Ա������������`�����ߴ���������༭���ӣ�");} 

    $testentry  = $query->cookie("forumsallowed$inforum");
    if (($allowedentry{$inforum} eq "yes")||(($testentry eq $forumpass)&&($testentry ne ""))||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }
    else { $allowed  = "no"; }
    if (($privateforum eq "yes") && ($allowed ne "yes")) { &error("����&�Բ������������ڴ���̳����"); }
    
    $rawpost = $post;
    
    if ($emailfunctions eq "on") {
	if ($innotify eq "yes") { $requestnotify = " checked"; } else { $requestnotify = ""; }
	$requestnotify = qq~<input type=checkbox name="notify" value="yes"$requestnotify>�лظ�ʱʹ���ʼ�֪ͨ����<br>~;
    }
    if ($emoticons eq "on") {
        $emoticonslink   = qq~<a href="javascript:openScript('misc.cgi?action=showsmilies',300,350)">����<B>ʹ��</B>�����ַ�ת��</a>~;
        $emoticonsbutton = qq~<input type=checkbox name="inshowemoticons" value="yes" checked>���Ƿ�ϣ��<b>ʹ��</b>�����ַ�ת�������������У�<br>~;
    }

    if ($htmlstate eq "on")         { $htmlstates = "����";         } else { $htmlstates = "������";       }
    if ($useemote eq "no") { $emotestates = "������"; } else { $emotestates = "����"; }
    if ($arrawpostflash eq "on")    { $postflashstates = "����";    } else { $postflashstates = "��ֹ";    }
    if ($arrawpostpic eq "on")      { $postpicstates = "����";      } else { $postpicstates = "��ֹ";      }
    if ($arrawpostfontsize eq "on") { $postfontsizestates = "����"; } else { $postfontsizestates = "��ֹ"; }
    if ($arrawpostsound eq "on")    { $postsoundstates = "����";    } else { $postsoundstates = "��ֹ";    }
    if ($postjf eq "yes")           { $postjfstates = "����";       } else { $postjfstates = "��ֹ";       }
    if ($jfmark eq "yes")    { $jfmarkstates = "����";}    else { $jfmarkstates = "��ֹ";}
    if ($hidejf eq "yes")           { $hidejfstates = "����";       } else { $hidejfstates = "��ֹ";       }

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
      &whosonline("$inmembername\t$forumname\tnone\t�༭<a href=\"topic.cgi?forum=$inforum&topic=$intopic\"><b>$topictitle</b></a>\t") if ($privateforum ne "yes");
      &whosonline("$inmembername\t$forumname(��)\tnone\t�༭��������\t") if ($privateforum eq "yes");
    }

if (($nowater eq "on")&&($inpostno eq "1")) { 
    $gsnum = 0 if ($gsnum<=0);
    $nowaterpost =qq~<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>��ˮ����</b></font></td><td bgcolor=$miscbackone><input type="radio" name="inwater" value=no> �����ˮ�� <input name="inwater" type="radio" value=yes> �����ˮ��    [���ѡ�񡰲����ˮ������ظ��������� <B>$gsnum</B> �ֽ�]</td></tr>~;
    $nowaterpost =~ s/value=$water/value=$water checked/i if ($water ne "");
}

    $rawpost =~ s/\[���(.+?)�����(.+?)�༭\]\n//isg;
    if ($wwjf ne "no") {
	if ($rawpost=~/LBHIDDEN\[(.*?)\]LBHIDDEN/sg) {
	    $weiwangchecked=" checked";
	    $weiwangchoice=$1;
        } else {
	    undef $weiwangchecked;
	    undef $weiwangchoice;
        }
        for (my $i=0;$i<$maxweiwang;$i++) {
	    $weiwangoption.=qq~<option value=$i>$i</option>~;
        }
        $weiwangoptionbutton=qq~<input type=checkbox name="inhiddentopic" value="yes" $weiwangchecked>���ܴ�����ֻ�Բ����û��ɼ����û�����������Ҫ  <select name=postweiwang>$weiwangoption</select><br>~;
        $weiwangoptionbutton =~ s/option value=$weiwangchoice/option value=$weiwangchoice selected/i if ($weiwangchoice ne "");
    } else {
        undef $weiwangoptionbutton;
    }

    if (($rawpost =~ /\[POSTISDELETE=(.+?)\]/)&&($membercode ne "ad")&&($membercode ne "smo")&&($inmembmod ne "yes")) {
        &error("�༭����&������༭�Ѿ����������ε����ӣ�");
    }

    $rawpost=~s/LBSALE\[(.*?)\]LBSALE//sg;
    $rawpost=~s/LBHIDDEN\[(.*?)\]LBHIDDEN//sg;
    $uselbcodecheck=($rawpost =~/\[DISABLELBCODE\]/)?"":" checked";
    $rawpost =~ s/\[DISABLELBCODE\]//isg;
    $usecanchgfont=($rawpost =~/\[USECHGFONTE\]/)?" checked":"";
    $rawpost =~ s/\[USECHGFONTE\]//isg;
    $rawpost =~ s/\[POSTISDELETE=(.+?)\]//isg;
    $rawpost =~ s/\[ADMINOPE=(.+?)\]//isg;

    &mischeader("�༭������");

    $helpurl = &helpfiles("�Ķ����");
    $helpurl = qq~$helpurl<img src="$imagesurl/images/$skin/help_b.gif" border=0></a>~;

if ($canchgfont ne "no") {
    $fontpost = qq~<input type=checkbox name="inshowchgfont" value="yes"$usecanchgfont>ʹ������ת����<br>~;
} else {
    undef $fontpost;
}
    if ($idmbcodestate eq "on")     { $idmbcodestates = "����"; $canlbcode = qq~<input type=checkbox name="uselbcode" value="yes"$uselbcodecheck>ʹ�� LeoBBS ��ǩ��<br>~; } else { $idmbcodestates = "������"; $canlbcode=""; }

    if ($inpostno eq "1") {
    	$topictitle = $newtopictitle if ($newtopictitle ne "");
        $topictitle =~s/ \(������\)$//;
        $topictitlehtml = qq~<td bgcolor=$miscbackone><font color=$fontcolormisc><b>��������</b></font></td><td bgcolor=$miscbackone><input type=text size=60 maxlength=80 name="newtopictitle" value="$topictitle">�����ó��� 40 ������</td>~;
        $topictitlehtml1="&nbsp;";
    }
    else {
        undef $topictitlehtml;
        $topictitlehtml1 = "<b>* ��������</b>�� $topictitle";
    }
    $output .= qq~<script>
function smilie(smilietext) {smilietext=' :'+smilietext+': ';if (document.FORM.inpost.createTextRange && document.FORM.inpost.caretPos) {var caretPos = document.FORM.inpost.caretPos;caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? smilietext + ' ' : smilietext;document.FORM.inpost.focus();} else {document.FORM.inpost.value+=smilietext;document.FORM.inpost.focus();}}
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
<input type=hidden name="action" value="processedit">
<input type=hidden name="postno" value="$inpostno">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic"><SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td>
<table cellpadding=4 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor colspan=2 $catbackpic><font color=$titlefontcolor>$topictitlehtml1</td></tr>
$topictitlehtml$nowaterpost
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr>
<td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>��ǰ����</b><BR><li>���������ӵ�ǰ��<BR></font></td>
<td bgcolor=$miscbackone valign=top>
~;
    open (FILE, "${lbdir}data/lbpost.cgi");
    my @posticondata = <FILE>;
    close (FILE);
    chomp @posticondata;
    my $tempiconnum=1;
    foreach (@posticondata) {
        $_ =~ s/[\a\f\n\e\0\r\t]//isg;
	if ($tempiconnum > 12) {
	    $tempiconnum = 1;
	    $tempoutput .= qq~<BR>~;
	}
	if ($_ eq $posticon) { $tempselect = " checked"; } else { $tempselect = ""; }
	$tempoutput .= qq~<input type=radio value="$_" name="posticon"$tempselect><img src=$imagesurl/posticons/$_ $defaultsmilewidth $defaultsmileheight>&nbsp;~;
	$tempiconnum ++;
    }
  
    $output .= qq~$tempoutput</td></tr>~;

#######�ɷ�ʽ�ĸ�����Ϊ�˼��ݣ�����############################
    my $p1=$inpostno-1;
    $dirtoopen2 = "$imagesdir" . "$usrdir/$inforum";
    opendir (DIR, "$dirtoopen2");
    @files = readdir(DIR);
    closedir (DIR);
    @files = grep(/^$inforum\_$intopic/,@files);
    if ($p1>0) { @files = grep(/^$inforum\_$intopic\_$p1\./,@files); } else { @files = grep(/^$inforum\_$intopic\./,@files); }
    if ( $#files >= 0 ) { $delimg="<BR><input type=checkbox name='delimg' value='no'>ɾ�����е�ԭͼ��򸽼�</input>"; }
########################################################
if ( $rawpost =~ m/\[UploadFile.{0,6}=([^\\\]]+?)\]/is ) {$delimg="<BR><input type=checkbox name='delimg' value='no'>ɾ�����е�ԭͼ��򸽼�</input>" if ($delimg eq "");}

    if (((($inpostno eq "1")&&($arrowupload ne "off"))||(($inpostno ne "1")&&($allowattachment ne "no"))||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes"))) {
        $uploadreqire= "" if ($uploadreqire <= 0);
        $uploadreqire = "<BR>������Ҫ���� <B>$uploadreqire</B> ƪ(��֤�û�����)" if ($uploadreqire ne "");
#        $output .= qq~<tr><td bgcolor=$miscbacktwo><b>�ϴ�������ͼƬ</b>(��� $maxupload KB)$uploadreqire</td><td bgcolor=$miscbacktwo> <input type="file" size=30 name="addme">����$addtypedisp</td></tr>~;
        ###·��add start
	$output .= qq~<script language="javascript">function jsupfile(upname) {upname='[UploadFile$imgslt='+upname+']';if (document.FORM.inpost.createTextRange && document.FORM.inpost.caretPos) {var caretPos = document.FORM.inpost.caretPos;caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? upname + ' ' : upname;document.FORM.inpost.focus();} else {document.FORM.inpost.value+=upname;document.FORM.inpost.focus();}}</script>~;
        ###·��add end
        $output .= qq~<tr><td bgcolor=$miscbackone><b>�ϴ�������ͼƬ</b> (������� <B>$maxupload</B>KB)$uploadreqire</td><td bgcolor=$miscbackone> <iframe id="upframe" name="upframe" src="upfile.cgi?action=uppic&forum=$inforum&topic=$intopic" width=100% height=40 marginwidth=0 marginheight=0 hspace=0 vspace=0 frameborder=0 scrolling=NO></iframe><br><font color=$fonthighlight>Ŀǰ����:(�粻��Ҫĳ��������ֻ��ɾ�������е���Ӧ [UploadFile$imgslt ...] ��ǩ����)  [<a href=upfile.cgi?action=delup&forum=$inforum target=upframe title=ɾ������δ�������ĸ�����ʱ�ļ� OnClick="return confirm('ȷ��ɾ������δ�������ĸ�����ʱ�ļ�ô��');">ɾ��</a>] </font></font>$delimg<SPAN id=showupfile name=showupfile></SPAN></td></tr>~;

    }

($no,$alipayid,$warename,$oldpost,$wareprice,$wareurl,$postage_mail,$postage_express,$postage_ems) = split(/\[ALIPAYE\]/,$rawpost);

if ($postage_mail ne "" || $postage_express ne "" || $postage_ems ne "") {
    $pviewed = ""; $tcheck1 = ""; $tcheck2 = "CHECKED";
} else {
    $pviewed = "disabled"; $tcheck1 = "CHECKED"; $tcheck2 = "";
}

    $output.=qq~</tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>�ҵ�֧�����˺�</b> <font color=$fonthighlight>(*)</font></font></td><td bgcolor=$miscbackone><input type=text size=28 maxlength=80 name="alipayid" value="$alipayid">�����û�У�����д��ȷ���ʼ���ַ</td></tr>~;
$output.=qq~</tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>��Ʒ����</b> <font color=$fonthighlight>(*)</font></font></td><td bgcolor=$miscbackone><input type=text size=28 maxlength=80 name="warename" value="$warename">��û�����ƣ������ô����?</td></tr>~;
$output.=qq~</tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>��Ʒչʾ��ַ</b></font></td><td bgcolor=$miscbackone><input type=text size=28 maxlength=80 name="wareurl" value="$wareurl">�����ͻ�������ϸ�Ľ���</td></tr>~;
    $output.=qq~</tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>��Ʒ�۸�</b> <font color=$fonthighlight>(*)</font></font></td><td bgcolor=$miscbackone><input type=text size=28 maxlength=80 name="wareprice" value="$wareprice">������д��ȷ�ļ۸�</td></tr>~;
    $output.=qq~</tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>�ʷѳе���ѡ��</b> <font color=$fonthighlight>(*)</font></font></td><td bgcolor=$miscbackone>
<input onclick="document.FORM.postage_mail.disabled=true; document.FORM.postage_express.disabled=true; document.FORM.postage_ems.disabled=true" type="radio" $tcheck1 value="s" name="transport"> ���ҳе��ʷ�<br>
<input onclick="document.FORM.postage_mail.disabled=false; document.FORM.postage_express.disabled=false; document.FORM.postage_ems.disabled=false" type="radio" $tcheck2 value="b" name="transport"> ��ҳе��ʷ�<br>
ͨ����������ѡ��ע���ý������������ķ��е��˷ѡ�<br>
�������ҳе��˷ѣ���ѡ������ṩ��������ʽ�Լ���Ӧ���á�<br>
ƽ�� <input $pviewed size="3" name="postage_mail" value="$postage_mail"> Ԫ (�����������ṩƽ��)<br>
��� <input $pviewed size="3" name="postage_express" value="$postage_express"> Ԫ (�����������ṩ���)<br>
EMS&nbsp; <input $pviewed size="3" name="postage_ems" value="$postage_ems"> Ԫ (�����������ṩ EMS)<br>
</td></tr>
~;
    $maxpoststr = "(������������ <B>400</B> ���ַ�)" ;

    $output .= qq~<td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>��Ʒ����</b> <font color=$fonthighlight>(*)</font>��$maxpoststr<p>
�ڴ���̳�У�<li>HTML ��ǩ��: <b>$htmlstates</b><li><a href="javascript:openScript('lookemotes.cgi?action=style',300,350)">EMOTE����ǩ</a>: <b>$emotestates</b><li><a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LeoBBS ��ǩ</a>: <b>$idmbcodestates</b><li>��ͼ��ǩ�� : <b>$postpicstates</b><li>Flash ��ǩ : <b>$postflashstates</b><li>���ֱ�ǩ�� : <b>$postsoundstates</b><li>���ִ�С�� : <b>$postfontsizestates</b><li>������ǩ ��: <b>$postjfstates</b><li>���ֱ�ǩ ��: <b>$jfmarkstates</b><li>���ܱ�ǩ ��: <b>$hidejfstates</b><li>$emoticonslink</font></td>
<td bgcolor=$miscbackone>$insidejs
<TEXTAREA cols=80 name=inpost rows=12 wrap="soft" onkeydown=ctlent() onselect="storeCaret(this);" onclick="storeCaret(this);" onkeyup="storeCaret(this);">$oldpost</TEXTAREA><br>
&nbsp; ģʽ:<input type="radio" name="mode" value="help" onClick="thelp(1)">������<input type="radio" name="mode" value="prompt" CHECKED onClick="thelp(2)">��ȫ��<input type="radio" name="mode" value="basic"  onClick="thelp(0)">��������>> <a href=javascript:HighlightAll('FORM.inpost')>���Ƶ�������</a> | <a href=javascript:checklength(document.FORM);>�鿴����</a> | <span style=cursor:hand onclick="document.getElementById('inpost').value += trans()">ת�������峬�ı�</spn><SCRIPT>rtf.document.designMode="On";</SCRIPT> <<</td></tr>
<tr><td bgcolor=$miscbackone valign=top colspan=2>
~;
    if ($emoticons eq "on"){
	$output.=qq~<font color=$fontcolormisc><b>�������ͼ�����������м�����Ӧ�ı���</B></font><br>&nbsp;~;
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
    }
    if (($inpostno ne 1)&&(($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")||(($arrowuserdel eq "on")&&(lc($inmembername) eq lc($postermembername))))) {
        $managetable = qq~<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>����Աѡ��</b></td><td bgcolor=$miscbackone>&nbsp;<a href="delpost.cgi?action=processedit&postno=$inpostno&forum=$inforum&topic=$intopic&deletepost=yes" OnClick="return confirm('���Ҫɾ���˻ظ�ô��');">ɾ���˻ظ�(����ʹ�ã����ɻָ�)</a></td></tr>~;
    }
    $output .= qq~</td></tr>
<tr><td bgcolor=$miscbacktwo valign=top><font color=$fontcolormisc><b>ѡ��</b><p>$helpurl
</font></td>
<td bgcolor=$miscbacktwo><font color=$fontcolormisc>$canlbcode
<input type=checkbox name="inshowsignature" value="yes" checked>�Ƿ���ʾ����ǩ����<br>$requestnotify$emoticonsbutton$fontpost$weiwangoptionbutton
</font></td></tr>$managetable
<tr><td bgcolor=$miscbackone colspan=2 align=center>
<input type=Submit value="�� ��" name=Submit onClick="return clckcntr();">����<input type=button value='Ԥ ��' name=Button onclick=gopreview()>����<input type="reset" name="Clear" value="�� ��"></td></form></tr></table></tr></td></table><SCRIPT>valignend()</SCRIPT>
<form name=preview action=preview.cgi method=post target=preview_page><input type=hidden name=body value=""><input type=hidden name=forum value="$inforum"><input type=hidden name=topic value="$intopic"></form>
<script>
function gopreview(){
document.forms[1].body.value=document.forms[0].inpost.value;
var popupWin = window.open('', 'preview_page', 'scrollbars=yes,width=600,height=400');
document.forms[1].submit()
}
</script>
~;

}

sub processedit {
    $inpostno1=$inpostno;
    $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
    if (-e $filetoopen) {
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE, "$filetoopen") or &error("�༭&������ⲻ���ڣ�");
        flock(FILE, 1) if ($OS_USED eq "Unix");
	sysread(FILE, my $allthreads,(stat(FILE))[7]);
        close(FILE);
	$allthreads =~ s/\r//isg;
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
        @allthreads = split(/\n/, $allthreads);
    }
    else { unlink ("$lbdir" . "forum$inforum/$intopic.pl"); &error("�༭&������ⲻ���ڣ�"); }

    if (($inhiddentopic eq "yes") && ($moneyhidden eq "yes")) { &error("��������&�벻Ҫ��һ��������ͬʱʹ�������ͽ�Ǯ���ܣ�"); }
    if ((($inhiddentopic eq "yes")||($moneyhidden eq "yes")) && ($userregistered eq "no")) { &error("��������&δע���û���Ȩ���������ͽ�Ǯ���ܣ�"); }

    $delimg=$query->param('delimg');
    $posttoget = $inpostno;
    $posttoget--;
    $postcountcheck = 0;

    ($postermembername, $topictitle, $postipaddress, $showemoticons, $showsignature ,$postdate, $post, $posticon) = split(/\t/, $allthreads[$posttoget]);

    $addpost = "";
    while ($post =~ /\[ADMINOPE=(.+?)\]/s) {
	$addpost .= "[ADMINOPE=$1]";
	$post =~ s/\[ADMINOPE=(.+?)\]//s;
    }
    
    if (($post =~ /\[POSTISDELETE=(.+?)\]/)&&($membercode ne "ad")&&($membercode ne "smo")&&($inmembmod ne "yes")) {
        &error("�༭����&������༭�Ѿ����������ε����ӣ�");
    }

    if ($noedittime ne '') {
	if (($membercode ne "ad")&&($membercode ne "smo")&&($inmembmod ne "yes")) {
	    &error("�༭����&���� $noedittime Сʱ�������ٱ༭���ӣ�") if(($currenttime - $postdate) > ($noedittime * 3600));
	}
    }

    while ($post =~ /\[UploadFile.{0,6}=(.+?)\]/) {
    	my $filenametemp = $1;
    	$filenametemp =~ s/\.\.//isg;
    	$filenametemp =~ s/\/\\//isg;
    	$addmetotle = "$addmetotle$filenametemp\n";
    	$post =~ s/\[UploadFile.{0,6}=(.+?)\]//;
    }
    @addmetotle = split(/\n/,$addmetotle);

$post =~ s/\[���(.+?)���(.+?)�༭\]//isg;
($edittimes, $temp) = split(/ ��/, $2);
($temp, $edittimes) = split(/�� /, $edittimes);
$edittimes = 0 unless ($edittimes);

    $testentry = $query->cookie("forumsallowed$inforum");
    if (($allowedentry{$inforum} eq "yes")||(($testentry eq $forumpass)&&($testentry ne ""))||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }
    else { $allowed  = "no"; }
    if (($privateforum eq "yes") && ($allowed ne "yes")) { &error("�༭����&�Բ������������ڴ���̳����"); }

    &error("�༭����&�Բ��𣬱���̳���������� <B>$maxpoststr</B> ���ַ������£�") if ((length($inpost) > $maxpoststr)&&($maxpoststr ne "")&&($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne 'cmo')&&($membercode ne 'amo') && ($membercode ne "mo") && ($membercode !~ /^rz/) && ($inmembmod ne "yes"));
    &error("�༭����&�Բ��𣬲�����༭ͶƱ���ӣ�") if (($posticon =~ m/<BR>/i)&&($posttoget eq 0));
    &error("�༭����&�Բ���������ǽ�������") unless ($post=~m/\[ALIPAYE\]/);
    &error("�༭����&�Բ��𣬱���̳������������ <B>$minpoststr</B> ���ַ������£�") if ((length($inpost) < $minpoststr)&&($minpoststr ne "")&&($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne 'cmo') && ($membercode ne "mo") && ($membercode ne "amo") && ($membercode !~ /^rz/) && ($inmembmod ne "yes"));

    $inmembmod = "no" if (($membercode eq "amo")&&($allowamoedit ne "yes"));
    if (($membercode ne "ad")&&($membercode ne "smo")&&($inmembmod ne "yes")&&((lc($inmembername) ne lc($postermembername))||($usereditpost eq "no"))) {&error("�༭����&������ԭ���ߡ���̳����Ա������������`�����ߴ���������༭���ӣ�");} 
    if (($membercode eq "banned")||($membercode eq "masked"))      { &error("�༭����&������ֹ���Ի��߷����Ѿ������Σ�����ϵ����Ա�Ա�����"); }

    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if(($membercode eq 'smo') && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if ((lc($inmembername) eq lc($postermembername)) && ($inpassword eq $password) && ($usereditpost ne "no")) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit eq "no"; }

    if ($cleartoedit eq "yes") {
        $editpostdate = $currenttime;
        $editpostdate = $editpostdate + ($timezone + $timedifferencevalue)*3600;
        $editpostdate = &dateformat("$editpostdate");
        $inpost =~ s/[\a\f\n\e\0\r\t]//g;
        $inpost =~ s/  / /g;
        $inpost =~ s/\n\n/\<p\>/g;
        $inpost =~ s/\n/\<br\>/g;
        $inpost =~ s/\[���(.+?)�����(.+?)�༭\]//isg;

        if ($emote && $inpost =~ m/\/\/\//) {
	    study ($inpost);
 	    my @pairs1 = split(/\&/,$emote);
	    foreach (@pairs1) {
	        chomp $_;
		($toemote, $beemote) = split(/=/,$_);
		$beemote =~ s/����/��$inmembername��/isg;
		$inpost =~ s/$toemote/$beemote/isg;
		last unless ($inpost =~ m/\/\/\//);
	    }
	}

	$newtopictitle =~ s/\(������\)$//;
	my $temp = &dofilter("$newtopictitle\t$inpost");
	($newtopictitle,$inpost) = split(/\t/,$temp);
	
        if ($inpostno eq 1){ 
	$newtopictitle =~ s/(a|A)N(d|D)/$1&#78;$2/sg;
	$newtopictitle =~ s/(a|A)n(d|D)/$1&#110;$2/sg;
	$newtopictitle =~ s/(o|O)R/$1&#82;/sg;
	$newtopictitle =~ s/(o|O)r/$1&#114;/sg;
#	$newtopictitle =~ s/\\/&#92;/isg;

	    $newtopictitle =~ s/()+//isg;
	    my $tempintopictitle = $newtopictitle;
	    $tempintopictitle =~ s/ //g;
	    $tempintopictitle =~ s/\&nbsp\;//g;
	    $tempintopictitle =~ s/��//g;
	    $tempintopictitle =~ s/^����������//;
	    if ($tempintopictitle eq "") { &error("�༭����&������������⣡"); }
	    undef $tempintopictitle; 
        }   
        
        if (($newtopictitle eq "")&&($inpostno eq 1)) { &error("�༭����&�Բ����������ⲻ��Ϊ�գ�"); }
        if ((length($newtopictitle) > 110)&&($inpostno eq 1))  { &error("�༭����&�Բ���������������"); }
        $newtopictitle  = "����������$newtopictitle";

	if (($nowater eq "on")&&($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne 'cmo')&&($membercode ne 'amo')&&($membercode ne 'mo')&&($inmembmod ne "yes")) {
          ($trash, $trash, $trash, $trash, $trash, $trash, $post, $trash,my $water) = split(/\t/,$allthreads[0]);
	  if ($water eq "no") {
	    my $inposttemp = $inpost;
	    $inposttemp =~ s/\[���(.+?)�����(.+?)�༭\]\<BR\>\<BR\>//isg;
	    $inposttemp =~ s/\[���(.+?)�����(.+?)�༭\]\<BR\>//isg;
	    $inposttemp =~ s/\[���(.+?)�����(.+?)�༭\]//isg;
	    $inposttemp =~ s/\[quote\]\[b\]����������\[u\].+?\[\/u\]�� \[i\].+?\[\/i\] ��������ݣ�\[\/b\].+?\[\/quote\]\<br\>//isg;
	    $inposttemp =~ s/\[quote\]\[b\]����������\[u\].+?\[\/u\]�� \[i\].+?\[\/i\] ��������ݣ�\[\/b\].+?\[\/quote\]//isg;
	    if ((length($inposttemp) < $gsnum)&&($gsnum > 0)) {
	        &error("����ظ�&�벻Ҫ��ˮ���������ֹ $gsnum �ֽ����µĹ�ˮ��");
                unlink ("${imagesdir}$usrdir/$inforum/$inforum\_$intopic\_$replynumber.$up_ext") if ($addme);
	    }
	  }
	}

        if ($inpostno eq 1) {
	    $newtopictitle = "$newtopictitle (������)" if (($inpost eq "")&&($addme eq ""));
	    if ($topictitle eq $newtopictitle) {
		$topictitlecomp = 1;
	    }
	    else {
	        $topictitle = $newtopictitle;
		$topictitlecomp = 0;
	    }
        }
	$edittimes++;
	$noaddedittime = 60 if ($noaddedittime < 0);
	$inpost = qq~[������������$inmembername�� $editpostdate �� $edittimes �α༭]<br><br>$inpost~ if (($currenttime - $postdate) > $noaddedittime || $postermembername ne $inmembername);

        if ($moneyhidden eq "yes") { $inposttemp = "(����)"; $inpost="LBSALE[$moneypost]LBSALE".$inpost;}

	if ($inhiddentopic eq "yes") { $inposttemp = "(����)"; $inpost="LBHIDDEN[$postweiwang]LBHIDDEN".$inpost; }

	$inpost =~ s/(ev)a(l)/$1&#97;$2/isg;

	if ($inposttemp ne "(����)") {
	    $inposttemp = $inpost;
	    $inposttemp = &temppost($inposttemp);
	    chomp $inposttemp;
            $inposttemp = &lbhz($inposttemp,50);
        }

    $p1=$inpostno-1;

########ɾ���ɷ�ʽ�ĸ��������ݵĻ�����####
    $dirtoopen2 = "$imagesdir" . "$usrdir/$inforum";
    opendir (DIR, "$dirtoopen2");
    @files = readdir(DIR);
    closedir (DIR);
    @files = grep(/^$inforum\_$intopic/,@files);

    if ($p1>0) { @files = grep(/^$inforum\_$intopic\_$p1\./,@files);} else { @files = grep(/^$inforum\_$intopic\./,@files);}

    foreach (@files) {
        if (($addme ne "")||($delimg ne "")) {
            unlink ("$imagesdir/$usrdir/$inforum/$_");
        }
   }

#######ɾ��ȫ��ԭ���ĸ��� START###(BY ·��)
     if ($delimg ne "") {$showerr = &delupfiles(\$inpost,$inforum,$intopic);}; #�·�ʽ

#######ɾ��ȫ��ԭ���ĸ��� END

    $topic =$intopic%100;
    my $topath = "${imagesdir}$usrdir/$inforum/$topic"; #Ŀ��Ŀ¼
  foreach (@addmetotle) {
  	if ($inpost !~ /$_/i) { unlink("$topath\/$_"); }
  }


    my $filesize=0;

   $addme= &upfileonpost(\$inpost,$inforum,$intopic);#�����ϴ���������ֵ��BT�����ж�

    for ('alipayid','warename','wareurl','wareprice','transport','postage_mail','postage_express','postage_ems') {
    next unless defined $_;
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
if(length($inpost)>400){
&error("����&��Ʒ�������ܳ���400���ַ�");
}
&error("����&���Բ����Ϲ涨�ļ۸�")if($wareprice!~/^[0-9\.]+$/i);
&error("����&���Բ����Ϲ涨�ļ۸�")if($postage_mail!~/^[0-9\.]+$/i && $postage_mail ne '');
&error("����&���Բ����Ϲ涨�ļ۸�")if($postage_express!~/^[0-9\.]+$/i && $postage_express ne '');
&error("����&���Բ����Ϲ涨�ļ۸�")if($postage_ems!~/^[0-9\.]+$/i && $postage_ems ne '');

$transport = 's' if ($postage_mail eq "" && $postage_express eq "" && $postage_ems eq "");

if ($transport eq 's') {
    $postage_mail = "";
    $postage_express = "";
    $postage_ems = "";
}

    $alipayid  = lc($alipayid);
    $alipayid =~ s/[\ \a\f\n\e\0\r\t\`\~\!\$\%\^\&\*\(\)\=\+\\\{\}\;\'\:\"\,\/\<\>\?\|]//isg;
    if($alipayid !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,4}|[0-9]{1,4})(\]?)$/) { &error("����&֧�����˺Ŵ���"); }

    $wareurl =~ s/[\a\f\n\e\0\r\t]//isg;
    $wareurl =~ s/^http:\/\///isg;

    $k="\[ALIPAYE\]$alipayid\[ALIPAYE\]$warename\[ALIPAYE\]$inpost\[ALIPAYE\]$wareprice\[ALIPAYE\]$wareurl\[ALIPAYE\]$postage_mail\[ALIPAYE\]$postage_express\[ALIPAYE\]$postage_ems\[ALIPAYE\]";
    $inpost = $k;

        $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        if (open(FILE, ">$filetoopen")) {
            flock(FILE, 2) if ($OS_USED eq "Unix");
            foreach $postline (@allthreads) {
                chomp $postline;
                if ($postcountcheck eq 0) { $water = "$inwater\t"; } else { $water=""; }
                if ($postcountcheck eq $posttoget) {
                    print FILE "$postermembername\t$topictitle\t$postipaddress\t$inshowemoticons\t$inshowsignature\t$postdate\t$addpost$inpost\t$inposticon\t$water\n";
                }
                else {
                    (my $postermembertemp, my $topictitletemp, my @endall) = split(/\t/,$postline);
                    print FILE "$postermembertemp\t$topictitle\t";
                    foreach (@endall) {
                        print FILE "$_\t";
                    }
                    print FILE "\n";
                }
                $postcountcheck++;
            }
            close(FILE);
        }
        &winunlock($filetoopen) if ($OS_USED eq "Nt");

        $postcountcheck--;
        $topictitle =~ s/^����������//;
       	if (($inpostno eq 1)||($postcountcheck eq $posttoget)) {
            $filetoopen = "$lbdir" . "forum$inforum/$intopic.pl";
	    open(FILE, "$filetoopen");
	    my $topicall = <FILE>;
            close(FILE);
            chomp $topicall;
	    (my $topicidtemp, my $topictitletemp, my $topicdescription,my $threadstate,my $threadposts ,my $threadviews,my $startedby,my $startedpostdate,my $lastposter,my $lastpostdate,my $posticon,my $posttemp, my $addmetype) = split(/\t/,$topicall);
	    $posttemp = $inposttemp if ($postcountcheck eq $posttoget);
	    $posticon = $inposticon if ($inpostno eq 1);
            if ($inpost =~ /\[UploadFile.{0,6}=(.+?)\]/i) {
	         ($no,$addmetype1) = split(/.*\./,$1);
	    } else { $addmetype1 = ""; }
	    if ($inpostno eq 1) { $addmetype = $addmetype1; }
            if (open(FILE, ">$filetoopen")) {
                print FILE "$intopic\t����������$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$posticon\t$posttemp\t$addmetype\t\n";
                close(FILE);
            }

	    $filetoopen = "$lbdir" . "boarddata/listall$inforum.cgi";
            &winlock($filetoopen) if ($OS_USED eq "Nt");
            open(FILE, "$filetoopen");
            flock(FILE, 2) if ($OS_USED eq "Unix");
	    sysread(FILE, my $allthreads,(stat(FILE))[7]);
            close(FILE);
	    $allthreads =~ s/\r//isg;
	    $allthreads =~ s/(.*)(^|\n)$intopic\t(.*?)\t(.*?)\t(.*?)\t\n(.*)/$1$2$intopic\t$topictitle\t$4\t$5\t\n$6/isg;

            if (open(FILE, ">$filetoopen")) {
                flock(FILE, 2) if ($OS_USED eq "Unix");
                print FILE "$allthreads";
                close(FILE);
            }
            &winunlock($filetoopen) if ($OS_USED eq "Nt");
	}
       	if (($inpostno eq 1)&&($topictitlecomp eq 0)) {

	    my $newthreadnumber;
	    $filetoopen = "$lbdir" . "boarddata/lastnum$inforum.cgi";
	    if (open(FILE, "$filetoopen")) {
		$newthreadnumber = <FILE>;
                close(FILE);
                chomp $newthreadnumber;
	    }
	    if ($newthreadnumber = $intopic) {
		$filetoopen = "${lbdir}boarddata/foruminfo$inforum.cgi";
		my $filetoopens = &lockfilename($filetoopen);
		if (!(-e "$filetoopens.lck")) {
	            &winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
		    open(FILE, "+<$filetoopen");
		    my ($lastforumpostdate, $tpost, $treply, $todayforumpost, $lastposter) = split(/\t/,<FILE>);
		    my ($lastposttime,$threadnumber,$topictitle1)=split(/\%\%\%/,$lastforumpostdate);
		    seek(FILE,0,0);
		    $lastforumpostdate = "$lastposttime\%\%\%$threadnumber\%\%\%$topictitle";
		    print FILE "$lastforumpostdate\t$tpost\t$treply\t$todayforumpost\t$lastposter\t\n";
		    close(FILE);
		    &winunlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
		}
	    }

	    $filetomakeopen = "$lbdir" . "data/recentpost.cgi";
    	    &winlock($filetomakeopen) if ($OS_USED eq "Nt");
	    open(FILE, "$filetomakeopen");
    	    flock (FILE, 1) if ($OS_USED eq "Unix");
	    @recentposts=<FILE>;
	    close(FILE);

            if (open (FILE, ">$filetomakeopen")) {
    	        flock (FILE, 2) if ($OS_USED eq "Unix");
                foreach (@recentposts) {
	            chomp $_;
	            ($tempno1, $tempno2, $no, @endall) = split (/\t/,$_);
    	            next if (($tempno1 !~ /^[0-9]+$/)||($tempno2 !~ /^[0-9]+$/));

                    if (($tempno1 eq $inforum)&&($tempno2 eq $intopic)) {
                        print FILE "$inforum\t$intopic\t$topictitle\t";
                        foreach (@endall) { print FILE "$_\t"; }
                        print FILE "\n"
                    }
                    else {
                        print FILE "$_\n"
                    }
                }
	        close(FILE);
	    }
    	    &winunlock($filetomakeopen) if ($OS_USED eq "Nt");
	}

        &mischeader("�༭����");

for(my $iii=0;$iii<=4;$iii++) {
    my $jjj = $iii * $maxthreads;
    unlink ("${lbdir}cache/plcache$inforum\_$jjj.pl");
}

$gopage = int(($posttoget-1)/$maxtopics)*$maxtopics;
$posttoget ++;
        if ($refreshurl == 1) { $relocurl = "topic.cgi?forum=$inforum&topic=$intopic&start=$gopage#$posttoget"; }
                         else { $relocurl = "forums.cgi?forum=$inforum"; }
        $output .= qq~<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>�༭�ɹ�</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
���������<ul><li><a href="topic.cgi?forum=$inforum&topic=$intopic&start=$gopage#$posttoget">��������</a><li><a href="forums.cgi?forum=$inforum">������̳</a><li><a href="leobbs.cgi">������̳��ҳ</a></ul>
</tr></td></table></td></tr></table>
<meta http-equiv="refresh" content="3; url=$relocurl">
~;
    }
    else { &error("�༭����&������ԭ���ߣ������û������������"); }
}
