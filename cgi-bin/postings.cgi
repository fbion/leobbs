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
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
$LBCGI::POST_MAX=500000;
#require "code.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
#require "postjs.cgi";
require "cleanolddata.pl";
require "recooper.pl";

$|++;
$thisprog = "postings.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

for ('forum','topic','membername','password','action','inpost','checked') {
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

$inmembername  = $membername;
$inpassword    = $password;
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$currenttime   = time;

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
require "sendmanageinfo.pl" if ($sendmanageinfo eq "yes");
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

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

&error("��ͨ����&û���������̳��") if (!(-e "${lbdir}forum$inforum"));
#&getoneforum("$inforum");
&moderator("$inforum");
&cleanolddata;

my %Mode = (
    'lock'                 =>    \&lockthread,
    'unlock'               =>    \&unlockthread,
    'puttop'               =>    \&puttop,
    'putdown'              =>    \&putdown,
    'repireforum'          =>    \&repireforum,
    'locktop'		   =>	 \&locktop,
    'unlocktop'		   =>	 \&unlocktop,
    'catlocktop'           =>    \&catlocktop,
    'catunlocktop'         =>    \&catunlocktop,
    'abslocktop'	   =>	 \&abslocktop,
    'absunlocktop'	   =>	 \&absunlocktop,
    'highlight' 	   =>    \&highlight,
    'lowlight'  	   =>    \&lowlight,
);

if ($Mode{$action}) { $Mode{$action}->(); } else { &error("��ͨ����&������ȷ�ķ�ʽ���ʱ�����"); }

for(my $iii=0;$iii<=4;$iii++) {
    my $jjj = $iii * $maxthreads;
    unlink ("${lbdir}cache/plcache$inforum\_$jjj.pl");
}

&output($boardname,\$output);
exit;

sub lockthread {
	my $intopics = $intopic;
	my @intopic = split(/ +/, $intopics);
	my $lockcount = @intopic;
	&error("��������&����ѡ����Ҫ���������⣡") if ($lockcount <= 0);
    &mischeader("��������");

    $cleartoedit = "no";
    if (($membercode eq "ad")  && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($membercode eq 'smo') && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($inmembmod eq "yes")  && ($inpassword eq $password)) { $cleartoedit = "yes"; }

    if (($arrowuserdel eq "on")&&($cleartoedit ne "yes")) {
        open (ENT, "${lbdir}forum$inforum/$intopic.pl");
        $in = <ENT>;
        close (ENT);
        chomp $in;
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $inposticon, $inposttemp, $addmetemp) = split(/\t/,$in);
        if ((lc($inmembername) eq lc($startedby)) && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    if ($cleartoedit eq "no" && $checked eq "yes") { &error("��������&�����Ǳ���̳̳������������������������"); }

    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
	my $lockreason = $query->param("lockreason");
	$lockreason = &cleaninput($lockreason);
	$lockreason = &lbhz($lockreason, 60);
	$lockreason = "�������ǣ�$lockreason" if ($lockreason ne "");

      foreach $intopic (@intopic) {
	my $filetomake = "${lbdir}forum$inforum/$intopic.pl";
	unless (-e $filetomake) {
	    $lockcount--;
	    next;
	}

        open (ENT, "${lbdir}forum$inforum/$intopic.pl");
        $in = <ENT>;
        close (ENT);
        chomp $in;
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $inposticon, $inposttemp, $addmetemp) = split(/\t/,$in);
        if (($threadstate eq "poll")||($threadstate eq "pollclosed")) { $threadstate = "pollclosed"; } else { $threadstate = "closed"; }
        if (open(FILE, ">${lbdir}forum$inforum/$intopic.pl")) {
            print FILE "$intopic\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$inposticon\t$inposttemp\t$addmetemp\t";
            close(FILE);
        }
        $topictitle =~ s/^����������//;
        &sendtoposter("$inmembername","$startedby","","lock","$inforum","$intopic", "$topictitle","$lockreason") if (($sendmanageinfo eq "yes")&&(lc($inmembername) ne lc($startedby)));
      }

		if ($lockcount == 1)
		{
			&addadminlog("��������$lockreason", $intopic);
		}
		else
		{
			&addadminlog("������������ $lockcount ƪ$lockreason");
		}

        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>���������ɹ��������� <font color=$fonthighlight>$lockcount</font> ƪ���⡣</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
���������<ul><li><a href="forums.cgi?forum=$inforum">������̳</a><li><a href="leobbs.cgi">������̳��ҳ</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
    } else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="lock">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>�����������û���������������ģʽ [���� $lockcount ������]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=text name=lockreason size=60> ���ɲ��</td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="�� ¼"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}

sub unlockthread {
    &mischeader("�������");

    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if(($membercode eq 'smo') && ($inpassword eq $password)) {$cleartoedit  = "yes"; }
    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    if ($cleartoedit eq "no" && $checked eq "yes") { &error("�������&�����Ǳ���̳̳������������������������"); }
    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        my $file = "${lbdir}forum$inforum/$intopic.pl";
        open (ENT, $file);
        $in = <ENT>;
        close (ENT);
        chomp $in;
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate,$inposticon, $inposttemp,$addmetemp) = split(/\t/,$in);
 	$topictitle =~ s/^����������//;

        if (($threadstate eq "pollclosed")||($threadstate eq "poll")) { $threadstate = "poll"; } else { $threadstate = "open"; }
        if (open(FILE, ">$file")) {
            print FILE "$intopic\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$inposticon\t$inposttemp\t$addmetemp\t";
            close(FILE);
        }

	&addadminlog("���ӽ���", $intopic);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>��������ɹ�</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
���������<ul><li><a href="forums.cgi?forum=$inforum">������̳</a><li><a href="leobbs.cgi">������̳��ҳ</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
    } else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="unlock">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>�����������û���������������ģʽ [�������]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="�� ¼"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}

sub repireforum {
    &mischeader("��̳�޸�");

    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if(($membercode eq 'smo') && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($inmembmod eq "yes") && ($membercode ne 'amo') && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    if ($cleartoedit eq "no" && $checked eq "yes") { &error("��̳�޸�&�����Ǳ���̳̳���������������������������"); }

    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
    	require "rebuildlist.pl";
        my $truenumber = rebuildLIST(-Forum=>"$inforum");
        ($tpost,$treply) = split (/\|/,$truenumber);
        
            open(FILE, "${lbdir}boarddata/listno$inforum.cgi");
            $topicid = <FILE>;
            close(FILE);
            chomp $topicid;
	    my $rr = &readthreadpl($forumid,$topicid);
	    (my $lastpostdate, my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $posticon, my $posttemp) = split (/\t/,$rr);

            open(FILE, "+<${lbdir}boarddata/foruminfo$inforum.cgi");
            ($no, $no, $no, $todayforumpost, $no) = split(/\t/,<FILE>);
            $lastforumpostdate = "$lastpostdate\%\%\%$topicid\%\%\%$topictitle";
	    $lastposter = $startedby if ($lastposter eq "");
	    seek(FILE,0,0);
            print FILE "$lastforumpostdate\t$tpost\t$treply\t$todayforumpost\t$lastposter\t\n";
            close(FILE);
	    $posts = 0 if ($posts eq "");$threads = 0 if ($threads eq "");
	    open(FILE, ">${lbdir}boarddata/forumposts$inforum.pl");
	    print FILE "\$threads = $tpost;\n\$posts = $treply;\n\$todayforumpost = \"$todayforumpost\";\n1;\n";
            close(FILE);

	&addadminlog("�޸���̳");
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>��̳�޸��ɹ�</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
���������<ul><li><a href="forums.cgi?forum=$inforum">������̳</a><li><a href="leobbs.cgi">������̳��ҳ</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
    } else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="repireforum">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>�����������û���������������ģʽ [��̳�޸�]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="�� ¼"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}

sub puttop {
    &mischeader("��������");

    $cleartoedit = "no";
    if (($membercode eq "ad")  && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($membercode eq 'smo') && ($inpassword eq $password)) { $cleartoedit  = "yes"; }
    if (($inmembmod eq "yes")  && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    if ($cleartoedit eq "no" && $checked eq "yes") { &error("��������&�����Ǳ���̳̳������������������������"); }

    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        my $file = "${lbdir}forum$inforum/$intopic.pl";
        open (ENT, $file);
        $in = <ENT>;
        close (ENT);
        chomp $in;
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate,$inposticon,$inposttemp,$addmetemp) = split(/\t/,$in);

        if (open(FILE, ">$file")) {
            print FILE "$intopic\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$currenttime\t$inposticon\t$inposttemp\t$addmetemp\t";
            close(FILE);
        }
 	$topictitle =~ s/^����������//;

        $file = "$lbdir" . "boarddata/listno$inforum.cgi";
        &winlock($file) if ($OS_USED eq "Nt");
        open (LIST, "$file");
	flock (LIST, 1) if ($OS_USED eq "Unix");
	sysread(LIST, $listall,(stat(LIST))[7]);
        close (LIST);
        $listall =~ s/\r//isg;

	$listall =~ s/(^|\n)$intopic\n/$1/isg;

        if (open (LIST, ">$file")) {
	    flock (LIST, 2) if ($OS_USED eq "Unix");
            print LIST "$intopic\n$listall";
            close (LIST);
        }
        &winunlock($file) if ($OS_USED eq "Nt");


            open(FILE, "+<${lbdir}boarddata/foruminfo$inforum.cgi");
            ($no, $posts, $replys, $todayforumpost, $no) = split(/\t/,<FILE>);
            $lastforumpostdate = "$lastpostdate\%\%\%$topicid\%\%\%$topictitle";
	    $lastposter = $startedby if ($lastposter eq "");
	    seek(FILE,0,0);
            print FILE "$lastforumpostdate\t$posts\t$replys\t$todayforumpost\t$lastposter\t\n";
	    close(FILE);
	    $posts = 0 if ($posts eq "");$threads = 0 if ($threads eq "");
	    open(FILE, ">${lbdir}boarddata/forumposts$inforum.pl");
	    print FILE "\$threads = $posts;\n\$posts = $replys;\n\$todayforumpost = \"$todayforumpost\";\n1;\n";
            close(FILE);


	&addadminlog("��������λ��", $intopic);
       $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>���������ɹ�</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
���������<ul><li><a href="forums.cgi?forum=$inforum">������̳</a><li><a href="leobbs.cgi">������̳��ҳ</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
    } else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="puttop">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>�����������û���������������ģʽ [��������]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="�� ¼"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}

sub putdown {
    &mischeader("�������");

    $cleartoedit = "no";
    if (($membercode eq "ad")  && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($membercode eq 'smo') && ($inpassword eq $password)) { $cleartoedit  = "yes"; }
    if (($inmembmod eq "yes")  && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    if ($cleartoedit eq "no" && $checked eq "yes") { &error("�������&�����Ǳ���̳̳������������������������"); }

    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        my $file = "${lbdir}forum$inforum/$intopic.pl";
        open (ENT, $file);
        $in = <ENT>;
        close (ENT);
        chomp $in;
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate,$inposticon,$inposttemp,$addmetemp) = split(/\t/,$in);
	$lastpostdate = $lastpostdate - 3600 * 24 * 365; # ʱ����ǰ 1 ��
        
        if (open(FILE, ">$file")) {
            print FILE "$intopic\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$inposticon\t$inposttemp\t$addmetemp\t";
            close(FILE);
        }
 	$topictitle =~ s/^����������//;

        $file = "$lbdir" . "boarddata/listno$inforum.cgi";
        &winlock($file) if ($OS_USED eq "Nt");
        open (LIST, "$file");
	flock (LIST, 1) if ($OS_USED eq "Unix");
	sysread(LIST, $listall,(stat(LIST))[7]);
        close (LIST);
        $listall =~ s/\r//isg;

	$listall =~ s/(^|\n)$intopic\n/$1/isg;

        if (open (LIST, ">$file")) {
	    flock (LIST, 2) if ($OS_USED eq "Unix");
            print LIST "$listall$intopic\n";
            close (LIST);
        }
        &winunlock($file) if ($OS_USED eq "Nt");

	&addadminlog("����λ�ó���", $intopic);
       $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>������׳ɹ�</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
���������<ul><li><a href="forums.cgi?forum=$inforum">������̳</a><li><a href="leobbs.cgi">������̳��ҳ</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
    } else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="putdown">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>�����������û���������������ģʽ [�������]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="�� ¼"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}

sub locktop {
    &mischeader("����̶�");

    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if(($membercode eq 'smo') && ($inpassword eq $password)) { $cleartoedit = "yes";}
    if (($inmembmod eq "yes") && ($membercode ne 'amo') && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }

    if ($cleartoedit eq "no" && $checked eq "yes") { &error("����̶�����&�����Ǳ���̳̳���������������������������"); }
    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
    	unlink("${lbdir}cache/forumstop$inforum.pl");
        my $file = "$lbdir" . "boarddata/ontop$inforum.cgi";
        if (open (TOPFILE, $file)) {
            @toptopic = <TOPFILE>;
            close (TOPFILE);
            if (open (TOPFILE, ">$file")) {
                print TOPFILE "$intopic\n";
	        $putno = 1;
	        foreach (@toptopic) {
	            chomp $_;
	            if (($_ ne $intopic)&&(-e "${lbdir}forum$inforum/$_.thd.cgi")) {
	    	        print TOPFILE "$_\n";
	    	        $putno ++;
	            }
	            last if ($putno eq $maxtoptopic);
	        }
                close (TOPFILE);
            }
        } else {
            if (open (TOPFILE, ">$file")) {
                print TOPFILE "$intopic\n";
                close (TOPFILE);
            }
        }
	&addadminlog("�̶�����", $intopic);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>����̶����гɹ�</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
���������<ul><li><a href="forums.cgi?forum=$inforum">������̳</a><li><a href="leobbs.cgi">������̳��ҳ</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
    } else {
        if (open (TOPFILE, "${lbdir}boarddata/ontop$inforum.cgi")) {
            @toptopic = <TOPFILE>;
            close (TOPFILE);
	}
	$toptopic = 0;
	        foreach (@toptopic) {
	            chomp $_;
	            if (-e "${lbdir}forum$inforum/$_.thd.cgi") {
	    	        $toptopic ++;
	            }
	        }
	if ($toptopic >= $maxtoptopic) { $topnum = "<BR><B><font color=$fonthighlight>�Ѿ��̶��� $toptopic �������ˣ��������������һ�����̶������ӽ����Զ�ȡ���̶���</B></font>" } else { $topnum = "<BR><B><font color=$fonthighlight>�Ѿ��̶��� $toptopic �������ˣ��������Թ̶� $maxtoptopic �����ӡ�</B></font>"; }
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="locktop">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>�����������û���������������ģʽ [����̶�����]</b></font>$topnum</td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="�� ¼"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;

    }
}

sub unlocktop {
    &mischeader("����ȡ���̶�");

    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if(($membercode eq 'smo') && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if (($inmembmod eq "yes") && ($membercode ne 'amo') && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    if ($cleartoedit eq "no" && $checked eq "yes") { &error("����ȡ���̶�&�����Ǳ���̳̳���������������������������"); }

    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
    	unlink("${lbdir}cache/forumstop$inforum.pl");
        my $file = "${lbdir}boarddata/ontop$inforum.cgi";
        if (open (TOPFILE, $file)) {
            @toptopic = <TOPFILE>;
            close (TOPFILE);

            if (open (TOPFILE, ">$file")) {
                foreach (@toptopic) {
                    chomp $_;
                    if (($_ ne $intopic)&&(-e "${lbdir}forum$inforum/$_.thd.cgi")) {
	    	        print TOPFILE "$_\n";
	            }
	        }
                close (TOPFILE);
            }
        }
	&addadminlog("ȡ�����ӹ̶�", $intopic);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>����ȡ���̶��ɹ�</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
���������<ul><li><a href="forums.cgi?forum=$inforum">������̳</a><li><a href="leobbs.cgi">������̳��ҳ</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
    } else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="unlocktop">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>�����������û���������������ģʽ [����ȡ���̶�]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="�� ¼"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}

sub abslocktop {
    &mischeader("�����̶ܹ�����");
    if (($startnewthreads eq "no")||($startnewthreads eq "cert")||($privateforum eq "yes")) { &error("�����̶ܹ�����&�Բ����������̳�����Ƕ������û����ŵģ����Բ����̶ܹ����ӣ�"); }
    $absmaxtoptopic = 3 if ($absmaxtoptopic <=0);
    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    if ($cleartoedit eq "no" && $checked eq "yes") { &error("�����̶ܹ�����&�����Ǳ���̳̳�������������������"); }
    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
    	opendir (CATDIR, "${lbdir}cache");
	my @dirdata = readdir(CATDIR);
	closedir (CATDIR);
	@dirdata = grep(/^forumstop/,@dirdata);
	foreach (@dirdata) { unlink ("${lbdir}cache/$_"); }
        my $file = "$lbdir" . "boarddata/absontop.cgi";
        if (open (TOPFILE, $file)) {
            @toptopic = <TOPFILE>;
            close (TOPFILE);
            if (open (TOPFILE, ">$file")) {
                print TOPFILE "$inforum\|$intopic\n";
	        $putno = 1;
	        foreach (@toptopic) {
	            chomp $_;
                    next if ($_ eq "");
	            ($tempinforum,$tempintopic) = split (/\|/,$_);
	            unless (($tempinforum eq $inforum)&&($tempintopic eq $intopic)) {
	            	if (-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi") {
	    	            print TOPFILE "$_\n";
	    	            $putno ++;
	    	        }
	            }
	            last if ($putno eq $absmaxtoptopic);
	        }
                close (TOPFILE);
            }
        } else {
            if (open (TOPFILE, ">$file")) {
                print TOPFILE "$inforum\|$intopic\n";
                close (TOPFILE);
            }
        }
	&addadminlog("�̶ܹ�����", $intopic);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>�����̶ܹ����гɹ�</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
���������<ul><li><a href="forums.cgi?forum=$inforum">������̳</a><li><a href="leobbs.cgi">������̳��ҳ</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
    } else {
        if (open (TOPFILE, "${lbdir}boarddata/absontop.cgi")) {
            @toptopic = <TOPFILE>;
            close (TOPFILE);
        }
        $toptopic = 0;
	        foreach (@toptopic) {
	            chomp $_;
                    next if ($_ eq "");
	            ($tempinforum,$tempintopic) = split (/\|/,$_);
	            	if (-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi") {
	    	            $toptopic ++;
	    	        }
	        }
	if ($toptopic >= $absmaxtoptopic) { $topnum = "<BR><B><font color=$fonthighlight>�Ѿ��̶ܹ��� $toptopic �������ˣ��������������һ�����̶������ӽ����Զ�ȡ���̶���</B></font>" } else { $topnum = "<BR><B><font color=$fonthighlight>�Ѿ��̶ܹ��� $toptopic �������ˣ����������̶ܹ� $absmaxtoptopic �����ӡ�</B></font>"; }
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="abslocktop">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>�����������û���������������ģʽ [�����̶ܹ�����]</b></font>$topnum</td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="�� ¼"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;

    }
}

sub absunlocktop {
    &mischeader("����ȡ���̶ܹ�");

    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    if ($cleartoedit eq "no" && $checked eq "yes") { &error("����ȡ���̶ܹ�&�����Ǳ���̳̳�������������������"); }

    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
    	opendir (CATDIR, "${lbdir}cache");
	my @dirdata = readdir(CATDIR);
	closedir (CATDIR);
	@dirdata = grep(/^forumstop/,@dirdata);
	foreach (@dirdata) { unlink ("${lbdir}cache/$_"); }
        my $file = "${lbdir}boarddata/absontop.cgi";
        if (open (TOPFILE, $file)) {
            @toptopic = <TOPFILE>;
            close (TOPFILE);

            if (open (TOPFILE, ">$file")) {
                foreach (@toptopic) {
                    chomp $_;
                    next if ($_ eq "");
	            my ($tempinforum,$tempintopic) = split (/\|/,$_);
	            unless (($tempinforum eq $inforum)&&($tempintopic eq $intopic)) {
	            	if (-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi") {
	    	            print TOPFILE "$_\n";
	    	        }
	            }
	        }
                close (TOPFILE);
            }
        }
	&addadminlog("ȡ�������̶ܹ�", $intopic);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>����ȡ���̶ܹ��ɹ�</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
���������<ul><li><a href="forums.cgi?forum=$inforum">������̳</a><li><a href="leobbs.cgi">������̳��ҳ</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
    } else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="absunlocktop">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>�����������û���������������ģʽ [����ȡ���̶ܹ�]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="�� ¼"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}
sub highlight {
  &mischeader("�������ӱ���");
  $maxhightopic = 8 if ($maxhightopic <=0);

  $cleartoedit = "no";
  if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
  if(($membercode eq 'smo') && ($inpassword eq $password)) {$cleartoedit = "yes";}
  if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
  unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
  if ($cleartoedit eq "no" && $checked eq "yes") { &error("�������ӱ���&�����Ǳ���̳̳������������������������"); }
  if (($cleartoedit eq "yes") && ($checked eq "yes")) {
      unlink("${lbdir}cache/forumstop$inforum.pl");
      my $file = "$lbdir" . "boarddata/highlight$inforum.cgi";
      if (open (HIGHFILE, $file)) {
          @hightopic = <HIGHFILE>;
          close (HIGHFILE);
          if (open (HIGHFILE, ">$file")) {
              print HIGHFILE "$inforum\-$intopic\n";
              $putno = 1;
      foreach (@hightopic) {
          chomp $_;
          next if ($_ eq "");
          ($tempinforum,$tempintopic) = split (/\-/,$_);
          chomp $tempintopic;chomp $tempinforum;
          unless (($tempinforum eq $inforum)&&($tempintopic eq $intopic)) {
              if (-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi") {
          	  print HIGHFILE "$_\n";
          	  $putno ++;
              }
          }
          last if ($putno eq $maxhightopic);
      }
              close (HIGHFILE);
          }
      } else {
          if (open (HIGHFILE, ">$file")) {
              print HIGHFILE "$inforum\-$intopic\n";
              close (HIGHFILE);
          }
      }
      &addadminlog("�������ӱ���", $intopic);
      $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>�������ӱ���ɹ�</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
���������<ul><li><a href="forums.cgi?forum=$inforum">������̳</a><li><a href="leobbs.cgi">������̳��ҳ</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
  } else {
        if (open (TOPFILE, "${lbdir}boarddata/highlight$inforum.cgi")) {
            @hightopic = <TOPFILE>;
            close (TOPFILE);
        }
        $toptopic = 0;
	        foreach (@hightopic) {
	            chomp $_;
                    next if ($_ eq "");
	            ($tempinforum,$tempintopic) = split (/\-/,$_);
	            	if (-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi") {
	    	            $toptopic ++;
	    	        }
	        }
	if ($toptopic >= $maxhightopic) { $topnum = "<BR><B><font color=$fonthighlight>�Ѿ������� $toptopic �����ӱ����ˣ��������������һ�������ر��⽫���Զ�ȡ�����ر��⡣</B></font>" } else { $topnum = "<BR><B><font color=$fonthighlight>�Ѿ������� $toptopic �����ӱ����ˣ��������Լ��� $maxhightopic �����ӱ��⡣</B></font>"; }
      $inmembername =~ s/\_/ /g;
      $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="highlight">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>�����������û���������������ģʽ [�������ӱ���]</b></font>$topnum</td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="�� ¼"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;

  }
}

sub lowlight {
  &mischeader("���ӱ���ȡ������");

  $cleartoedit = "no";
  if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
  if(($membercode eq 'smo') && ($inpassword eq $password)) {$cleartoedit = "yes";}
  if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
  unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
  if ($cleartoedit eq "no" && $checked eq "yes") { &error("���ӱ���ȡ������&�����Ǳ���̳̳������������������������"); }

  if (($cleartoedit eq "yes") && ($checked eq "yes")) {
      unlink("${lbdir}cache/forumstop$inforum.pl");
      my $file = "${lbdir}boarddata/highlight$inforum.cgi";
      if (open (HIGHPFILE, $file)) {
          @hightopic = <HIGHPFILE>;
          close (HIGHPFILE);

          if (open (HIGHPFILE, ">$file")) {
              foreach (@hightopic) {
                  chomp $_;
                  next if ($_ eq "");
          my ($tempinforum,$tempintopic) = split (/\-/,$_);
          unless (($tempinforum eq $inforum)&&($tempintopic eq $intopic)) {
              if (-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi") {
          	  print HIGHPFILE "$_\n";
              }
          }
      }
              close (HIGHPFILE);
          }
      }
      &addadminlog("���ӱ���ȡ������", $intopic);
      $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>���ӱ���ȡ�����سɹ�</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
���������<ul><li><a href="forums.cgi?forum=$inforum">������̳</a><li><a href="leobbs.cgi">������̳��ҳ</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
  } else {
      $inmembername =~ s/\_/ /g;
      $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="lowlight">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>�����������û���������������ģʽ [���ӱ���ȡ������]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="�� ¼"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
  }
} 

sub catlocktop {
    &mischeader("�������̶�����");
    if (($startnewthreads eq "no")||($startnewthreads eq "cert")||($privateforum eq "yes")) { &error("�������̶�����&�Բ����������̳�����Ƕ������û����ŵģ����Բ������̶����ӣ�"); }
    $absmaxcantopic = 3 if ($absmaxcantopic <= 0);
    $cleartoedit = "no";
    if (($membercode eq "ad" || $membercode eq "smo" || ",$catemods," =~ /\Q\,$inmembername\,\E/i) && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    if ($cleartoedit eq "no" && $checked eq "yes") { &error("�������̶�����&�����Ǳ���������Ա�����������������"); }
    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
    	opendir (CATDIR, "${lbdir}cache");
	my @dirdata = readdir(CATDIR);
	closedir (CATDIR);
	@dirdata = grep(/^forumstop/,@dirdata);
	foreach (@dirdata) { unlink ("${lbdir}cache/$_"); }

        my $file = "${lbdir}boarddata/catontop$categoryplace.cgi";
        if (open (TOPFILE, $file)) {
            @toptopic = <TOPFILE>;
            close (TOPFILE);
            if (open (TOPFILE, ">$file")) {
                print TOPFILE "$inforum\|$intopic\n";
                $putno = 1;
                foreach (@toptopic) {
                    chomp $_;
                    next if ($_ eq "");
                    ($tempinforum,$tempintopic) = split (/\|/,$_);
                    unless (($tempinforum eq $inforum && $tempintopic eq $intopic) || !(-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi")) {
                            print TOPFILE "$_\n";
                            $putno ++;
                    }
                    last if ($putno eq $absmaxcantopic);
                }
                close (TOPFILE);
            }
        } else {
            if (open (TOPFILE, ">$file")) {
                print TOPFILE "$inforum\|$intopic\n";
                close (TOPFILE);
            }
        }
	&addadminlog("���̶�����", $intopic);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>�������̶����гɹ�</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
���������<ul><li><a href="forums.cgi?forum=$inforum">������̳</a><li><a href="leobbs.cgi">������̳��ҳ</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
    } else {
        if (open (TOPFILE, "${lbdir}boarddata/catontop$categoryplace.cgi")) {
            @toptopic = <TOPFILE>;
            close (TOPFILE);
        }
        $toptopic = 0;
                foreach (@toptopic) {
                    chomp $_;
                    next if ($_ eq "");
                    ($tempinforum,$tempintopic) = split (/\|/,$_);
                    if (-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi") {
                            $toptopic ++;
                    }
                }
        if ($toptopic >= $absmaxcantopic) { $topnum = "<BR><B><font color=$fonthighlight>�Ѿ����̶��� $toptopic �������ˣ��������������һ�����̶������ӽ����Զ�ȡ���̶���</B></font>" } else { $topnum = "<BR><B><font color=$fonthighlight>�Ѿ����̶��� $toptopic �������ˣ������������̶� $absmaxcantopic �����ӡ�</B></font>"; }
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="catlocktop">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>�����������û���������������ģʽ [�������̶�����]</b></font>$topnum</td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="�� ¼"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;

    }
}

sub catunlocktop {
    &mischeader("����ȡ�����̶�");

    $cleartoedit = "no";
    if (($membercode eq "ad" || $membercode eq "smo" || ",$catemods," =~ /\Q\,$inmembername\,\E/i) && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    if ($cleartoedit eq "no" && $checked eq "yes") { &error("����ȡ�����̶�&�����Ǳ���������Ա�����������������"); }

    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
    	opendir (CATDIR, "${lbdir}cache");
	my @dirdata = readdir(CATDIR);
	closedir (CATDIR);
	@dirdata = grep(/^forumstop/,@dirdata);
	foreach (@dirdata) { unlink ("${lbdir}cache/$_"); }
        my $file = "${lbdir}boarddata/catontop$categoryplace.cgi";
        if (open (TOPFILE, $file)) {
            @toptopic = <TOPFILE>;
            close (TOPFILE);

            if (open (TOPFILE, ">$file")) {
                foreach (@toptopic) {
                    chomp;
                    next if ($_ eq "");
                    my ($tempinforum,$tempintopic) = split (/\|/,$_);
                    unless (($tempinforum eq $inforum && $tempintopic eq $intopic) || !(-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi")) {
                            print TOPFILE "$_\n";
                    }
                }
                close (TOPFILE);
            }
        }
	&addadminlog("ȡ���������̶�", $intopic);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>����ȡ�����̶��ɹ�</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
���������<ul><li><a href="forums.cgi?forum=$inforum">������̳</a><li><a href="leobbs.cgi">������̳��ҳ</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
    } else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="catunlocktop">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>�����������û���������������ģʽ [����ȡ�����̶�]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="�� ¼"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}
