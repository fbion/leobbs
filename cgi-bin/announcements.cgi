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
require "code.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "announcements.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

for ('membername','password','announcementtitle','announcementpost','action','checked','number', 'forum') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput($tp);
    ${$_} = $tp;
}
$inmembername           = $membername;
$inpassword             = $password;
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}
$inannouncementtitle    = $announcementtitle;
$inannouncementpost     = $announcementpost;
$inforum		= $forum;
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum) && ($inforum !~ /^[0-9]+$/));
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ((!$inmembername) or ($inmembername eq "����")) { $inmembername = "����"; }
  else {
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

if ($inforum ne "") { &getoneforum("$inforum"); } else { $inmembmod = "no"; }
#    &moderator("$inforum");

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&title;

if ($inforum ne "") {
    if ($category=~/childforum-[0-9]+/) {
	$tempforumno=$category;
	$tempforumno=~s/childforum-//;
	open(FILE, "${lbdir}forum$tempforumno/foruminfo.cgi");
	$forums = <FILE>;
	close(FILE);
	(undef, undef, undef, $tempforumname, undef) = split(/\t/,$forums);
	$addlink  = qq~ �� <a href=forums.cgi?forum=$tempforumno>$tempforumname</a>~;
    }
    $forumdescription = &HTML("$forumdescription");
    $forumdescription =~ s/<BR>//isg;
    $forumdescription =~ s/<P>//isg;
        $output .= qq~
<table width=$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> $forumdescription</td></tr></table>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3><tr height=25><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=12> <font color=$navfontcolor><a href=leobbs.cgi>$boardname</a>$addlink �� <a href=forums.cgi?forum=$inforum>$forumname</a> �� �����̳����</td><td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td>
<table cellpadding=3 cellspacing=1 width=100% style="TABLE-LAYOUT: fixed">
~;
} else {
        $output .= qq~
<table width=$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> �����������Բ鿴����վ���й���</td></tr></table>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3 height=25><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=11> <font face="$font" color=$navfontcolor> <a href="leobbs.cgi">$boardname</a> �� <a href="announcements.cgi">��̳����</a> �� �鿴��̳����<td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td>
<table cellpadding=3 cellspacing=1 width=100% style="TABLE-LAYOUT: fixed">
~;
}

if ($action eq "delete") {
    if ($checked eq "yes") {
	if (($membercode ne "ad") && ($membercode ne 'smo') && ($inmembmod ne "yes")) { &error("ʹ�ù���&�����ǹ���Ա��"); }

	$filetoopen = "$lbdir" . "data/news$inforum.cgi";
        open(FILE, "$filetoopen");
        @announcements = <FILE>;
        close(FILE);
        $count = 0;

        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE, ">$filetoopen");
        flock (FILE, 2) if ($OS_USED eq "Unix");
        foreach (@announcements) {
	    chomp $_;
	    if ($count ne $number) {
                print FILE "$_\n";
            }
	    $count++;
	}
        close(FILE);
	&winunlock($filetoopen) if ($OS_USED eq "Nt");
        &doend("��̳�����Ѿ���ɾ��");
	exit;
    }
    else {
	&login("$thisprog?action=delete&number=$number&checked=yes&forum=$inforum");
    }
}
elsif ($action eq "add") {
    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
	&whosonline("$inmembername\t������\tnone\t��ӹ���\t");
    }
    if (($membercode ne "ad")&&($membercode ne 'smo') && ($inmembmod ne "yes")) { &error("ʹ�ù���&�����ǹ���Ա��"); }
    $output .= qq~<tr><td bgcolor=$titlecolor colspan=2 align=center $catbackpic>
<form action="$thisprog" method=post>
<input type=hidden name="action" value="addannouncement">
<input type=hidden name="forum" value="$inforum">
<font face="$font" color=$fontcolormisc><b>������̳����</b></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> �����Ҫ�������û���ݷ����������������û��������롣�������ı��û���ݣ������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>��̳�������</b></font></td>
<td bgcolor=$miscbackone valign=middle><input type=text name="announcementtitle" size=60 maxlength=100></td></tr>
<tr>
<td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>��̳��������</b><br>������������̳�������ݡ�<p>���ʹ���˱����ַ�ת����LeoBBS ���Զ��ڹ�����ת�������ַ���</font></td>
<td bgcolor=$miscbackone valign=middle><textarea cols=60 rows=10 name="announcementpost"></textarea></td></tr>
<tr><td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
<input type=Submit  value="�� ��" name=Submit onClick="return clckcntr();"> &nbsp; <input type="reset" name="Clear">
</td></form></tr>
~;
}
elsif ($action eq "addannouncement") {
    $currenttime = time;
    if (($membercode ne "ad")&&($membercode ne 'smo') && ($inmembmod ne "yes")) { &error("ʹ�ù���&�����ǹ���Ա��"); }
    if ($inannouncementpost eq "")  { &error("ʹ�ù���&��������̳�������ݣ�"); }
    if ($inannouncementtitle eq "") { &error("ʹ�ù���&��������̳������⣡"); }

    $filetoopen = "$lbdir" . "data/news$inforum.cgi";
    open(FILE, "$filetoopen");
    @announcements = <FILE>;
    close(FILE);
    $newline = "$inannouncementtitle\t$currenttime\t$inannouncementpost\t$inmembername\t";

    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, ">$filetoopen");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    print FILE "$newline\n";
    foreach $line (@announcements) {
        chomp $line;
	print FILE "$line\n";
    }
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    &doend("��̳�����Ѿ�����");
    exit;
}
elsif ($action eq "edit") {
    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
        &whosonline("$inmembername\t������\tnone\t�༭����\t");
    }
    if (($membercode ne "ad")&&($membercode ne 'smo') && ($inmembmod ne "yes")) { &error("ʹ�ù���&�����ǹ���Ա��"); }

    $filetoopen = "$lbdir" . "data/news$inforum.cgi";
    open(FILE, "$filetoopen");
    @announcements = <FILE>;
    close(FILE);
    $count = 0;

    foreach (@announcements) {
        if ($count eq $number) {
            ($announcementtitle, $notneeded, $announcementpost,$notneeded) = split(/\t/,$_);
            last;
        }
        $count++;
    }
    &error("ʹ�ù���&�ù��治���ڣ�") if ($announcementtitle eq "");
    $announcementpost =~ s/\<p\>/\n\n/g;
    $announcementpost =~ s/\<br\>/\n/g;
    $output .= qq~<tr><td bgcolor=$titlecolor colspan=2 align=center $catbackpic>
<form action="$thisprog" method=post>
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="action" value="doedit">
<input type=hidden name="number" value="$number">
<font face="$font" color=$fontcolormisc><b>�༭��̳����</b></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> �����Ҫ�������û���ݷ����������������û��������롣�������ı��û���ݣ������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>��̳�������</b></font></td>
<td bgcolor=$miscbackone valign=middle><input type=text name="announcementtitle" value="$announcementtitle"size=60 maxlength=100></td></tr>
<tr><td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>��̳��������</b><br>������������̳�������ݡ�<p>���ʹ���˱����ַ�ת����LeoBBS ���Զ��ڹ�����ת�������ַ���</font></td>
<td bgcolor=$miscbackone valign=middle><textarea cols=60 rows=10 name="announcementpost">$announcementpost</textarea></td></tr>
<tr><td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
<input type=Submit  value="�� ��" name=Submit onClick="return clckcntr();"> &nbsp; <input type="reset" name="Clear">
</td></form></tr>
~;
}
elsif ($action eq "doedit") {
    $currenttime = time;
    if (($membercode ne "ad") &&($membercode ne 'smo')&& ($inmembmod ne "yes")) { &error("ʹ�ù���&�����ǹ���Ա��"); }
    if ($inannouncementpost eq "") { &error("ʹ�ù���&��������̳�������ݣ�"); }
    if ($inannouncementtitle eq "") { &error("ʹ�ù���&��������̳������⣡"); }
    $filetoopen = "$lbdir" . "data/news$inforum.cgi";
    open(FILE, "$filetoopen") ;
    @announcements = <FILE>;
    close(FILE);
    $count = 0;
    $newline = "$inannouncementtitle\t$currenttime\t$inannouncementpost\t$inmembername\t";

    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, ">$filetoopen");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    foreach (@announcements) {
        chomp $_;
        if ($count eq $number) {
            print FILE "$newline\n";
        } else {
            print FILE "$_\n";
        }
        $count++;
    }
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    &doend("��̳�����Ѿ����༭��������");
    exit;
}
else {
    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
	&whosonline("$inmembername\t������\tboth\t�鿴����\t");
    }
    $filetoopen = "$lbdir" . "data/news$inforum.cgi";
    open(FILE, "$filetoopen");
    @announcements = <FILE>;
    close(FILE);
    $postcountcheck = 0;
    $totals = @announcements;
    if ($totals eq "0") {
        $dateposted = time;
        @announcements[0] = "��ǰû���κι���\t$dateposted\t�������ͼ��������һ������(�����ǹ���Ա)��<br>���㷢��һ�ι���󣬱�����ͻ��Զ���ʧ���������ֶ�ɾ����";
    }
    foreach (@announcements) {
	($title, $dateposted, $post, $nameposted) = split(/\t/, $_);
	next if ($title eq "");
	$postedid++;
        $dateposted = $dateposted + ($timedifferencevalue*3600) + ($timezone*3600);
        $dateposted = &dateformat("$dateposted");
        &lbcode(\$post);
        &doemoticons(\$post);
	&smilecode(\$post);

        if ($post !~/<blockquote><font face=����>����/isg){
            $post =~ s/&quot\;/\"/g;
            $post =~ s/\&amp\;/\&/g;
        }

        if ($count eq "1") {
	    $postbackcolor = "$postcolorone";
	    $postfontcolor = "$postfontcolorone";
	    $count++;
	}
	else {
	    $postbackcolor = "$postcolortwo";
	    $postfontcolor = "$postfontcolortwo";
	    $count = 1;
	}
        $post = qq~<p><blockquote>$post</blockquote><p>~;
        $adminadd = qq~<a href="$thisprog?action=add&forum=$inforum"><img src="$imagesurl/images/a_add.gif" border=0"></a>~;
        $admindelete = qq~<a href="$thisprog?action=delete&number=$postcountcheck&forum=$inforum"><img src="$imagesurl/images/a_delete.gif" border=0"></a>~;
        $adminedit = qq~<a href="$thisprog?action=edit&number=$postcountcheck&forum=$inforum"><img src="$imagesurl/images/a_edit.gif" border=0"></a>~;

        $output .= qq~<tr><a name=title$postedid></a><td bgcolor=$titlecolor align=center valign=top $catbackpic><font face="$font" color=$titlefontcolor><b>>> $title <<</b></td></tr>~;
        if (($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) {
	    $output .= qq~<tr><td bgcolor=$postbackcolor align=left>$admindelete &nbsp; $adminedit &nbsp; $adminadd</td></tr>~;
        }
	$nameposted = "��վ��Ĭ�Ϲ���" if (!$nameposted);
	$output .= qq~<tr><td bgcolor="$postbackcolor" valign=top style="LEFT: 0px; WIDTH: 100%; WORD-WRAP: break-word"><font face="$font" color=$postfontcolor>
$post</td></tr><tr><td bgcolor="$postbackcolor" valign=middle>
<table width=100% border="0" cellpadding="0" cellspacing="0">
<tr><td align=left>&nbsp;&nbsp;&nbsp;<font face="$font" color=$postfontcolor><b>������</b>�� $nameposted</font>
</td><td align=right><font face="$font" color=$postfontcolor><b>����ʱ��</b>�� $dateposted</font>&nbsp;&nbsp;&nbsp;
</tr></table></td></font></tr>
~;
        $postcountcheck++;
    }
}
$output .= qq~</table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
&output("$boardname - ����",\$output);
exit;

sub login {
    local($url) = @_;
    ($postto, $therest) = split(/\?/,$url);
    @pairs = split(/\&/,$therest);

     if (($membercode ne "ad")&&($membercode ne 'smo') && ($inmembmod ne "yes")) { &error("ʹ�ù���&�����ǹ���Ա��"); }
   foreach (@pairs) {
        ($name, $value)=split(/\=/,$_);
        $hiddenvars .= qq~<input type=hidden name="$name" value="$value">\n~;
    }

    $output .= qq~<form action="$postto" method="post">
<tr><td bgcolor=$titlecolor valign=middle colspan=2 align=center $catbackpic>
$hiddenvars
<font face="$font" color=$fontcolormisc><b>��¼ǰ���������Ա����ϸ��Ϣ</b><br>��ע�⣬ֻ�й���Ա�ſ������ӡ�ɾ�����޸���̳���棡</font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> �����Ҫ�������û���ݷ����������������û��������롣�������ı��û���ݣ������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name="submit" value="ȷ��ɾ��"></td></form></tr></table></td></tr></table>
~;
}

sub doend {
    my $action_taken = shift;
    $relocurl = "$thisprog?forum=$inforum";
    $output .= qq~<tr>
<td bgcolor=$titlecolor $catbackpic valign=middle align=center><font face="$font" color=$fontcolormisc><b>��̳����</b></font></td></tr>
<tr><td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
�����������û���Զ�������̳���������������ֱ�ӷ��ء�
<ul><li><b>$action_taken</b><li><a href="$relocurl">������̳����</a><li><a href="leobbs.cgi">������̳��ҳ</a>
</ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=$relocurl">
~;
&writeannounce;
    &output("$boardname - ����",\$output);
    exit;
}

sub writeannounce {
  mkdir ("${lbdir}cache", 0777) if (!(-e "${lbdir}cache"));
  $currenttime = time;
  $timeadd  = $timedifferencevalue*3600;
  if ($inforum eq "") {
    if (open(FILE, "${lbdir}data/news.cgi")) {
        @announcementdata = <FILE>;
        close(FILE);
    }
    $totalannouncements = @announcementdata;
    if ($totalannouncements eq 0) { $dateposted = $currenttime; $title = "��ǰû�й���"; $announcetemp1 = qq~<img src=$imagesurl/images/announce.gif border=0 alt=����̳��ʱ�޹��棡 width=18>~; }
                             else { ($title, $dateposted, my $trash) = split(/\t/, $announcementdata[0]); $announcetemp1 = qq~<img src=$imagesurl/images/announce.gif border=0 alt="����̳���棡�� $totalannouncements ����" width=18>~; }
    $dateposted = $dateposted + $timeadd;
    $dateposted = &longdate("$dateposted");
    if ($announcemove eq "on") {
        if ($title ne "��ǰû�й���") {
            $title = "";
            $newstitleid = "";
            foreach (@announcementdata) {
                chomp  $_;
                (my $newstitle,my $dateposted) = split(/\t/,$_);
	        next if ($newstitle eq "");
                $dateposted = $dateposted + $timeadd;
                $dateposted = &longdate("$dateposted");
                $newstitleid++;
                $title .= qq~��<font color=\$forumfontcolor><B>$newstitleid. <a href=announcements.cgi#title$newstitleid target=_blank><font color=\$fonthighlight>$newstitle</font></a></B>��[$dateposted]</font> ����~;
            }
        }
        else { $title = "<a href=announcements.cgi target=_blank><B>$title</B></a>��[$dateposted]"; }
        $announcedisp=qq~<marquee scrollamount=3 onmouseover=this.stop(); onmouseout=this.start();>$title</marquee>~;
    }
    else {
        $titletemp = &lbhz($title,25); 
        $announcedisp=qq~&nbsp;<a href=announcements.cgi target=_blank title="$title"><b><font color=\$fonthighlight>$titletemp</font></b></a>��[$dateposted]~;
    }
    undef $titletemp; undef $title; undef $newstitleid;
    open (FILE, ">${lbdir}data/announce.pl");
    $announcedisp  =~ s/\\/\\\\/isg;
    $announcetemp1 =~ s/\\/\\\\/isg;
    $announcedisp  =~ s/~/\\\~/isg;
    $announcetemp1 =~ s/~/\\\~/isg;
    $announcedisp  =~ s/\$/\\\$/isg;
    $announcetemp1 =~ s/\$/\\\$/isg;
    $announcedisp  =~ s/\@/\\\@/isg;
    $announcetemp1 =~ s/\@/\\\@/isg;
    print FILE qq(\$announcedisp = qq~$announcedisp~;\n\$announcetemp1 = qq~$announcetemp1~;\n1;);
    close (FILE);
  } else {
    if (open(FILE, "${lbdir}data/news$inforum.cgi")) {
        @announcementdata = <FILE>;
        close(FILE);
    }
    $totalannouncements = @announcementdata;
    if ($totalannouncements eq 0) { $dateposted = $currenttime; $title = "��ǰû�й���"; $announcetemp1 = qq~<img src=$imagesurl/images/announce.gif border=0 alt=����̳��ʱ�޹��棡 width=18>~; }
                             else { ($title, $dateposted, my $trash) = split(/\t/, $announcementdata[0]); $announcetemp1 = qq~<img src=$imagesurl/images/announce.gif border=0 alt="����̳���棡�� $totalannouncements ����" width=18>~; }
    $dateposted = $dateposted + $timeadd;
    $dateposted = &longdate("$dateposted");
    if ($announcemove eq "on") {
        if ($title ne "��ǰû�й���") {
            $title = "";
            $newstitleid = "";
            foreach (@announcementdata) {
                chomp  $_;
                (my $newstitle,my $dateposted) = split(/\t/,$_);
	        next if ($newstitle eq "");
                $dateposted = $dateposted + $timeadd;
                $dateposted = &longdate("$dateposted");
                $newstitleid++;
                $title .= qq~��<font color=\$forumfontcolor><B>$newstitleid. <a href=announcements.cgi?forum=$inforum#title$newstitleid target=_blank><font color=\$fonthighlight>$newstitle</font></a></B>��[$dateposted]</font> ����~;
            }
        }
        else { $title = "<a href=announcements.cgi?forum=$inforum target=_blank><B>$title</B></a>��[$dateposted]"; }
        $announcedisp=qq~<marquee scrollamount=3 onmouseover=this.stop(); onmouseout=this.start();>$title</marquee>~;
    }
    else {
        $titletemp = &lbhz($title,38); 
        $announcedisp=qq~&nbsp;<a href=announcements.cgi?forum=$inforum target=_blank title="$title"><b>$titletemp</b></a>��[$dateposted]~;
    }
    undef $titletemp; undef $title; undef $newstitleid;
    open (FILE, ">${lbdir}data/announce$inforum.pl");
    $announcedisp  =~ s/\\/\\\\/isg;
    $announcetemp1 =~ s/\\/\\\\/isg;
    $announcedisp  =~ s/~/\\\~/isg;
    $announcetemp1 =~ s/~/\\\~/isg;
    $announcedisp  =~ s/\$/\\\$/isg;
    $announcetemp1 =~ s/\$/\\\$/isg;
    $announcedisp  =~ s/\@/\\\@/isg;
    $announcetemp1 =~ s/\@/\\\@/isg;
    print FILE qq(\$announcedisp = qq~$announcedisp~;\n\$announcetemp1 = qq~$announcetemp1~;\n1;);
    close (FILE);

  }
}