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
$LBCGI::POST_MAX = 1000000;
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 1;
require "code.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "bbs.lib.pl";

$|++;
$thisprog = "messanger.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;
#&ipbanned;

&error("����Ϣ��ֹʹ��&�ܱ�Ǹ��̳������ĳ��ԭ���ѽ�ֹ�����û�ʹ�ö���Ϣ����&msg") if ($allowusemsg eq "off");

$action = $query->param("action");

$actionto = $query->param("actionto");

$inwhere = $query->param("where");
$inmsg = $query->param("msg");
$inmembername = $query->cookie("amembernamecookie");
$inpassword = $query->cookie("apasswordcookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

$inselectstyle  = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

if ($action eq "send" || $action eq "new")
{
	$intouser = $query->param("touser");
	$intouser =~ s/\; /\;/ig;
	$intouser =~ s/ \;/\;/ig;
	$intouser =~ s/\;$//ig;
	$intouser =~ s/^\;//ig;
	$intouser =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\'\:\"\,\.\/\<\>\?]//isg;
	$inmsgtitle = $query->param("msgtitle");
	$inmessage = $query->param("message");
	$inmessage = &cleaninput($inmessage);
	$inmsgtitle = &cleaninput($inmsgtitle);
}
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if ($inmembername =~  m/\// || $inmembername =~ m/\\/ || $inmembername =~ m/\.\./);
&error("��ͨ����&�벻Ҫ�޸����ɵ� URL��") if ($inmsg =~ /[^0-9]/);

if ($inmembername eq "" || $inmembername eq "����")
{
	&error("��ͨ����&�㻹û��¼�أ����ȵ�¼��̳��&msg");
}
else
{
	&getmember($inmembername,"no");
	&error("��ͨ����&���û����������ڣ�&msg") if ($userregistered eq "no");
	&error("��ͨ����&�������û���������������µ�¼��&msg") if ($inpassword ne $password);
}
&doonoff;  #��̳�������

$msgmm = 0 if (($msgmm <= 0)||($msgmm eq ""));
$msgmneedmm = "off" if (($msgmm <= 0)||($msgmm eq ""));
$msgmneedmm = "off" if (($membercode eq "ad")||($membercode eq 'smo')||($membercode eq 'cmo')||($membercode eq "mo"));

$action = "inbox" if ($action eq "");
$memberfilename = $inmembername;
$memberfilename =~ s/ /\_/g;
$memberfilename =~ tr/A-Z/a-z/;

$output .= qq~<script language="JavaScript">
function bbimg(o){var zoom=parseInt(o.style.zoom,10)||100;zoom+=event.wheelDelta/12;if (zoom>0) o.style.zoom=zoom+'%';return false;}
function openscript(url, width, height)
{
	var Win = window.open(url, "openwindow", "width=" + width + ",height=" + height + ",resizable=1,scrollbars=yes,menubar=yes,status=yes");
}
function enable(btn)
{
	btn.filters.gray.enabled = 0;
}
function disable(btn)
{
	btn.filters.gray.enabled = 1;
}
</script>
<style>
.gray	{cursor: hand; filter:gray}
</style>~;

$inboxpm = qq~<img src=$imagesurl/images/inboxpm.gif border=0 alt="�ռ���" width=40 height=40>~;
$outboxpm = qq~<img src=$imagesurl/images/outboxpm.gif border=0 alt="������" width=40 height=40>~;
$newpm = qq~<img src=$imagesurl/images/newpm.gif border=0 alt="������Ϣ" width=40 height=40>~;
$replypm = qq~<img src=$imagesurl/images/replypm.gif border=0 alt="�ظ���Ϣ" width=40 height=40>~;
$fwpm = qq~<img src=$imagesurl/images/fwpm.gif border=0 alt="ת����Ϣ" width=40 height=40>~;
$deletepm = qq~<img src=$imagesurl/images/deletepm.gif border=0 alt="ɾ����Ϣ" width=40 height=40>~;
$friendpm = qq~<img src=$imagesurl/images/friendpm.gif border=0 alt="�򿪺���¼" width=40 height=40>~;
$blockpm = qq~<img src=$imagesurl/images/blockpm.gif border=0 alt="�򿪺�����" width=40 height=40>~;

$output .= qq~
<p>
<SCRIPT>valigntop()</SCRIPT><table cellPadding=0 cellSpacing=0 border=0 width=$tablewidth bgColor=$tablebordercolor align=center><tr><td><table cellPadding=3 cellSpacing=1 border=0 width=100%>~;

if ($action eq "attach") {
	my $box = $query->param('box');
	my $filetoopen = $box eq 'out' ? "${lbdir}${msgdir}/out/${memberfilename}_out.cgi" : "${lbdir}${msgdir}/in/${memberfilename}_msg.cgi";
	my $mestemp;
	&winlock($filetoopen) if ($OS_USED eq "Nt");
	if (open(FILE, $filetoopen))
	{
        	flock (FILE, 1) if ($OS_USED eq "Unix");
		sysread(FILE, $mestemp, (stat(FILE))[7]);
		close(FILE);
		$mestemp =~ s/\r//isg;
	}
	&winunlock($filetoopen) if ($OS_USED eq "Nt");
	my @boxmessages = split($/, $mestemp);
	my $msgtograb = $boxmessages[$inmsg];
	chomp($msgtograb);
	my ($from, $readstate, $date, $messagetitle, $post, $attach) = split(/\t/, $msgtograb);
	&error("��ȡ����&��Ϣû�и����������Ϣ�ѱ�ɾ����&msg") if ($attach eq '');

	my ($filename, $content) = split('����������', $attach);
	my $fileext = lc((split(/\./, $filename))[-1]);
	$content = &Base64decode($content);
	my $filesize = length($content);

	$fileext = 'jpeg' if ($fileext eq 'jpg');
	$fileext = 'html' if ($fileext eq 'htm');
	$fileext = 'plain' if ($fileext eq 'txt');
	print $fileext eq 'gif' || $fileext eq 'jpeg' || $fileext eq 'png' || $fileext eq 'bmp' ? header(-type=>"image/$fileext", -attachment=>$filename, -expires=>'0', -content_length=>$filesize) : $fileext eq 'swf' ? header(-type=>"application/x-shockwave-flash", -attachment=>$filename, -expires=>'0', -content_length=>$filesize) : $fileext eq 'plain' || $fileext eq 'html' ? header(-type=>"text/$fileext", -attachment=>$filename, -expires=>'0', -content_length=>$filesize) : header(-type=>"attachment/$fileext", -attachment=>$filename, -expires=>'0', -content_length=>$filesize);
	binmode(STDOUT);
	print $content;
	exit;
}

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

if ($action eq "new")
{
	my $messfilename = "${lbdir}${msgdir}/main/${memberfilename}_mian.cgi";
	&error("�������Ͷ���Ϣ&�������˶���Ϣ����ţ����������޷����ܶ���Ϣ�ģ�������Ҳ�޷����Ͷ���Ϣ��<br><font color=$fonthighlight>��ȡ������Ϣ����ţ�Ȼ�������·��Ͷ���Ϣ��</font><br><br>&msg") if (-e $messfilename && $membercode ne "ad");
        $mymoney2 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
	if (($msgmneedmm ne "off")&&($actionto eq "msg")) {
	    &error("$moneyname����&���Ͷ���Ϣ��Ҫ����:$msgmm $moneyname������ֻ�� $mymoney2 $moneyname��<BR><BR>&msg") if ($mymoney2 < $msgmm);
	}
	my $cleanname = $intouser;
	$cleanname =~ tr/A-Z/a-z/;
	$cleanname =~ s/\_/ /g;
	$inmessage =~ s/<p>/\n\n/ig;
	$inmessage =~ s/<br>/\n/ig;

	my $friendlist = "";
	if (open(FILE, "${lbdir}memfriend/${memberfilename}.cgi")) {
        	sysread(FILE, my $currentlist,(stat(FILE))[7]);
		close(FILE);
		$currentlist =~ s/\r//isg;
		@currentlist = split (/\n/, $currentlist);
	}
	my $friendlist = "";
	foreach (@currentlist) {
		chomp;
		s/^����������//isg;
		$friendlist .= qq~<option value="$_">$_</option>~;
	}

	if ($msgmneedmm ne "off") {
	$addout=qq~
	<tr>
            <td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>�����ֽ�</b></td>
            <td bgcolor=$miscbackone align="left">&nbsp;<B>$mymoney2</B> $moneyname</td>
            </tr>
	<tr>
            <td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>���ã�</b></td>
            <td bgcolor=$miscbackone align="left">&nbsp;<b>$msgmm</B> $moneyname/��</td>
            </tr>
	~;
	}

	$output .= qq~
<script language="Javascript">
function friendls1() {
    var myfriend = document.FORM.friend.options[document.FORM.friend.selectedIndex].value;
    if (myfriend != "") document.FORM.touser.value = document.FORM.touser.value = myfriend;
}
</script>
<tr><td bgColor=$miscbacktwo align=center colSpan=2 $catbackpic height=26><font color=$fontcolormisc><b>���Ͷ���Ϣ</b></td></tr>
<tr><td bgColor=$miscbackone align=center colSpan=2><a href=$thisprog?action=inbox>$inboxpm</a>��<a href=$thisprog?action=outbox>$outboxpm</a>��<a href=$thisprog?action=new>$newpm</a>��<a href="javascript:openscript('friendlist.cgi', 420, 320)">$friendpm</a>��<a href="javascript:openscript('blocklist.cgi', 420, 320)">$blockpm</a></td></tr>
<tr><td bgColor=$miscbacktwo colSpan=2 align=center><form action=messanger.cgi method=POST name=FORM enctype="multipart/form-data"><input type=hidden name=action value="send"><input type=hidden name=check value="yes"><font color=$fontcolormisc><b>����������������Ϣ</b></td></tr>
<tr>
<td bgColor=$miscbackone><font color=$fontcolormisc><b>�ռ��ˣ�</b></font></td>
<td bgColor=$miscbackone><input type=text name=touser value="$cleanname" size=16> ��<select name=friend OnChange="friendls1()"><option>��������</option>$friendlist</select></td>
</tr>
<tr>
<td bgColor=$miscbackone valign=top><font color=$fontcolormisc><b>���⣺</b></font></td>
<td bgColor=$miscbackone><input type=text name=msgtitle size=36 maxlength=80 value=$inmsgtitle></td>
</tr>~;
	if ($allowmsgattachment ne 'no')
	{
		my $addtypedisp = $addtype;
		$addtypedisp =~ s/\, /\,/ig;
		$addtypedisp =~ s/ \,/\,/ig;
		$addtypedisp =~ tr/A-Z/a-z/;
		my @addtypedisp = split(/\,/, $addtypedisp);
		$addtypedisp = "<select><option value=#>֧�����ͣ�</option><option value=#>----------</option>";
		foreach (@addtypedisp)
		{
			chomp;
			next if ($_ eq "");
			$addtypedisp .= "<option>$_</option>";
		}
		$addtypedisp .= qq~</select>~;
		$output .= qq~
<tr>
<td bgColor=$miscbackone valign=top width=30%><font color=$fontcolormisc><b>������</b><br>(��� <b>60</b> KB)</font></td>
<td bgColor=$miscbackone><input type=file size=30 name=addme><br>$addtypedisp</td>
</tr>
~;
	}

$output .= qq~
<tr>
<td bgColor=$miscbackone valign=top><font color=$fontcolormisc><b>���ݣ�</b></td>
<td bgColor=$miscbackone><textarea cols=35 rows=6 name=message OnKeyDown="ctlent()">$inmessage</textarea><br><input type=checkbox name=backup value="yes" class=1><font color=$fontcolormisc>�Ƿ���һ����Ϣ�������䣿</font></td>
</tr>$addout
<tr><td  colSpan=2 bgColor=$miscbacktwo align=center><input type=submit value="�� ��" name=Submit> ��<input type=reset name=Clear value="�� ��"></td></form></tr>
~;
}

elsif ($action eq "exportall")
{
	my $filetotrash = $inwhere eq "inbox" ? "${lbdir}${msgdir}/in/${memberfilename}_msg.cgi" : "${lbdir}${msgdir}/out/${memberfilename}_out.cgi";

	if (-e $filetotrash)
	{
		open(FILE, $filetotrash);
        	sysread(FILE, my $messanges,(stat(FILE))[7]);
		close(FILE);
		$messanges =~ s/\r//isg;
		my @messanges = split (/\n/, $messanges);
		
		$output .= qq~
<script language="JavaScript">
function HighlightAll(theField)
{
	var tempval = eval("document." + theField);
	tempval.focus();
	tempval.select();
	therange = tempval.createTextRange();
	therange.execCommand("Copy");
}
</script>
<tr><td bgColor=$miscbacktwo align=center><font color=$fontcolormisc><b>��������Ϣ</b></td></tr>
<tr><td bgColor=$miscbackone align=center><a href=$thisprog?action=inbox>$inboxpm</a>��<a href=$thisprog?action=outbox>$outboxpm</a>��<a href=$thisprog?action=new>$newpm</a>��<a href="javascript:openscript('friendlist.cgi', 420, 320)">$friendpm</a>��<a href="javascript:openscript('blocklist.cgi', 420, 320)">$blockpm</a></td></tr>
<tr><td bgColor=$miscbackone align=center><form name=FORM2><textarea name=inpost rows=12 style="width=90%">~;
	my $boxname = $inwhere eq "inbox" ? "�ռ���" : "������";
	$current_time = localtime;
	$output .= qq~
$boardname��$inmembername�Ķ���Ϣ$boxname��������
(����ʱ�䣺$current_time)
----------------------------------------
~;
	my $addtime = ($timedifferencevalue + $timezone) * 3600;
	foreach (@messanges)
	{
		($usrname, $msgread, $msgtime, $msgtitle, $msgwords) = split(/\t/, $_);
		$usrname =~ s/^����������//isg;
		$msgwords =~ s/\r//ig;
		$msgwords =~ s/&nbsp;/ /g;
		$msgwords =~ s/"/\&quot;/g;
		$msgwords =~ s/\s+/ /g;
		$msgwords =~ s/<br>/\n/g;
		$msgwords =~ s/<p>/\n/g;
		$msgtime = &dateformat($msgtime + $addtime);
		$output .= "\n[�շ�����]��$usrname\n[�շ�ʱ��]��$msgtime\n[���ű���]��$msgtitle\n[��������]��$msgwords\n";
	}
	$output .= qq~</textarea><br>>> <a href="javascript:HighlightAll('FORM2.inpost')">���Ƶ������� <<</a></form>
<font color=red>����$boxname�еĶ���Ϣ��ȫ����������Щ����Ϣ��δ������ɾ����<br>Ϊ���ٷ�����ѹ�����뾡��<a href=$thisprog?action=deleteall&where=$inwhere>[���]</a>����$boxname�еĶ���Ϣ��<br><br></td></tr>~;
	}
	else
	{
		&error("����Ϣ&�ļ�û���ҵ������ظ��ղŲ��裡&msg");
	}
}

elsif ($action eq "markall")
{	    
	$filetoopen = "${lbdir}${msgdir}/in/${memberfilename}_msg.cgi";
	if (-e $filetoopen)
	{
		&winlock($filetoopen) if ($OS_USED eq "Nt");
		open(FILE, $filetoopen);
		flock(FILE, 1) if ($OS_USED eq "Unix");
        	sysread(FILE, my $inboxmessages,(stat(FILE))[7]);
		close(FILE);
		$inboxmessages =~ s/\r//isg;
		my @inboxmessages = split (/\n/, $inboxmessages);
		
		open(FILE, ">$filetoopen");
		flock(FILE, 2) if ($OS_USED eq "Unix");
		foreach (@inboxmessages)
		{
			chomp;
			next if ($_ eq "");
			($from, $readstate, $date, $messagetitle, $post, $attach) = split(/\t/, $_);
			print FILE "$from\tyes\t$date\t$messagetitle\t$post\t$attach\n";
		}
		close(FILE);
		&winunlock($filetoopen) if ($OS_USED eq "Nt");
	}
	my $boxname = $inwhere eq "inbox" ? "�ռ���" : "������";
	$output .= qq~
<tr><td bgColor=$miscbacktwo align=center><font color=$fontcolormisc><b>���еĶ���Ϣ�ѱ����Ϊ�Ѷ�</b></td></tr>
<tr><td bgColor=$miscbackone align=center><a href=$thisprog?action=inbox>$inboxpm</a>��<a href=$thisprog?action=outbox>$outboxpm</a>��<a href=$thisprog?action=new>$newpm</a>��<a href="javascript:openscript('friendlist.cgi', 420, 320)">$friendpm</a>��<a href="javascript:openscript('blocklist.cgi', 420, 320)">$blockpm</a></td></tr>
<tr><td bgColor=$miscbackone align=center><font color=$fontcolormisc><b>����$boxname�еĶ���Ϣ�Ѿ�ȫ�����Ϊ�Ѷ�</b><br><br></td></tr>~;
}

elsif ($action eq "send")
{
	&error("����&�벻Ҫ���ⲿ���ӱ�����") if (($ENV{'HTTP_REFERER'} !~ /$ENV{'HTTP_HOST'}/i && $ENV{'HTTP_REFERER'} ne '' && $ENV{'HTTP_HOST'} ne '')&&($canotherlink ne "yes"));
	&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��&msg") if ($intouser =~  m/\// || $intouser =~ m/\\/ || $intouser =~ m/\.\./);
	&error("����Ϣ&������ֹ���ԣ�&msg") if ($membercode eq "banned" || $membercode eq "masked");
	if (($onlinetime + $onlinetimeadd) < $onlinemessage && $onlinemessage ne "" && $membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo" && $membercode ne "amo" && $membercode !~ /^rz/) { $onlinetime = $onlinetime + $onlinetimeadd; &error("����Ϣ&����̳����������ʱ������ $onlinemessage ����û����Ͷ���Ϣ����Ŀǰ�Ѿ����� $onlinetime �룡<BR>�������ʱ��ͳ�Ʋ���ȷ,�����µ�½��̳һ�μ��ɽ����&msg"); }
	my @sendtouserlist = split(/\;/, $intouser);
	&error("����Ϣ��ֹ����&�ܱ�Ǹ��һ��Ⱥ��ѶϢ��������� $maxsend ����&msg") if (@sendtouserlist > $maxsend && $maxsend =~ /^[0-9]+$/ && $membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo" && $membercode ne "amo");
	$inbackup = $query->param("backup");
	&error("����Ϣ&û��ָ���ռ��ˣ�&msg") if (@sendtouserlist == 0);
	
	$mymoney2 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
	$msgmm = 0 if (($msgmm < 0)||($msgmm eq "")||($membercode eq "ad")||($membercode eq 'smo')||($membercode eq 'amo')||($membercode eq 'cmo')||($membercode eq "mo"));
	if ($msgmneedmm ne "off") {
		if ($mymoney2 < $msgmm) { &error("$moneyname����&���Ͷ���Ϣ��Ҫ����:$msgmm $moneyname������ֻ��$mymoney2 $moneyname��<BR><BR>&msg"); }
		else {
		    $cleanmembername = $inmembername;
           	    $cleanmembername =~ s/ /\_/g;
		    $cleanmembername =~ tr/A-Z/a-z/;
		    my $namenumber = &getnamenumber($cleanmembername);
		    &checkmemfile($cleanmembername,$namenumber);

		    $filetomake = "$lbdir" . "$memdir/$namenumber/$cleanmembername.cgi";
        	    &winlock($filetomake) if ($OS_USED eq "Nt");
        	    if (open(FILE, ">$filetomake")) {
        		flock(FILE, 2) if ($OS_USED eq "Unix");
			$mymoney=$mymoney-$msgmm;
        		print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
        		close(FILE);
        	    }
        	    &winunlock($filetomake) if ($OS_USED eq "Nt");
        	}
	}

    # $addme=$query->upload('addme'); #���CGI.pm�汾>2.47���Ƽ�ʹ��
    $addme=$query->param('addme'); #���CGI.pm�汾<2.47�������滻�Ͼ�

        my $attach = '';
        if ($addme && $allowmsgattachment ne 'no')
        {

               my ($up_filename) = $addme =~ m|([^/:\\]+)$|; #ע��,��ȡ�ļ����ֵ���ʽ�仯
               my @up_names = split(/\./,$up_filename); #ע��
               my $up_name = $up_names[0];
               my $up_ext = $up_names[-1];
               $up_ext = lc($up_ext);


                my $checkadd = 0;
                foreach (split(/\,\s*/, $addtype))
                {
                        $checkadd = 1, last if ($up_ext eq lc($_));
                }
                &error("�ϴ�����&��֧�������ϴ��ĸ�������($up_ext)��������ѡ��&msg") if ($checkadd == 0);
                my $filesize = 0;
                my $bufferall = '';


                 binmode ($addme); #ע��

                 while (read($addme,$buffer,4096) )
                 {#2
                   if ($up_ext eq "txt" || $up_ext eq "htm" || $up_ext eq "html" || $up_ext eq "shtml")
                   {
                       $buffer =~ s/\.cookie/\&\#46\;cookie/isg;
                       $buffer =~ s/on(mouse|exit|error|click|key)/\&\#111\;n$1/isg;
                       $buffer =~ s/script/scri\&\#112\;t/isg;
                       $buffer =~ s/style/\&\#115\;tyle/isg;
                   }
                  $bufferall .= $buffer;
                  $filesize += 4;
                  } #2

                 close ($addme); #ע��

                &error("�ϴ�����&�ϴ�������С���� 60 KB��������ѡ��&msg") if (length($bufferall) > 60 * 1024);

                if ($up_ext eq "gif" || $up_ext eq "jpg" || $up_ext eq "bmp" || $up_ext eq "jpeg" || $up_ext eq "png" || $up_ext eq "ppm" || $up_ext eq "svg" || $up_ext eq "xbm" || $up_ext eq "xpm")
                {
                        eval("use Image::Info qw(image_info);");
                        if ($@ eq "")
                        {
                                my $info = image_info(\$bufferall);
                                &error("�ϴ�����&�ϴ���������ͼƬ�ļ������ϴ���׼��ͼƬ�ļ���&msg") if ($info->{error} eq "Unrecognized file format");
                        }
                }
                $attach = "$up_filename����������" . &Base64encode($bufferall);
        }

	undef @NoRegUser; undef @Max; undef @NoPM;
	my $noadmin = $membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "amo" && $membercode ne "mo" ? 1 : 0;
	my $currenttime = time;
	foreach (@sendtouserlist)
	{
		undef @inboxmessages; undef @allmessages; undef @blacklist;

		chomp;
		next if ($_ eq "");
		$cleanintouser = $_;
		$cleanintouser =~ s/ /\_/g;
		$cleanintouser =~ tr/A-Z/a-z/;
		$cleanintouser = &stripMETA($cleanintouser);

		&getmember($_,"no");
		if ($userregistered eq "no")
		{
			push(@NoRegUser, "���Ͷ���Ϣ����-û���ҵ��û���$_��");
			next;
		}

		if ($noadmin)
		{
			if ($membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "amo" && $membercode ne "mo" && $maxmsgno =~ /^[0-9]+$/ && $maxmsgno != 0)
			{
				my $filetoopen = "${lbdir}${msgdir}/in/${cleanintouser}_msg.cgi";
				if (open(FILE, $filetoopen)) {
        				sysread(FILE, my $allmessages,(stat(FILE))[7]);
					close(FILE);
					$allmessages =~ s/\r//isg;
					@allmessages = split (/\n/, $allmessages);
				}
				if (@allmessages >= $maxmsgno) {
					push(@Max, "�޷����Ͷ���Ϣ���Է�-$_�Ķ���Ϣ�ռ��������� $maxmsgno ����Ϣ���ռ�����");
					next;
				}
			}

			my $filetoopen = "${lbdir}memblock/${cleanintouser}.cgi";
			if (open(FILE, $filetoopen)) {
        			sysread(FILE, my $blacklist,(stat(FILE))[7]);
				close(FILE);
				$blacklist =~ s/\r//isg;
				@blacklist = split (/\n/, $blacklist);
				chomp(@blacklist);
				if (grep(/^����������$inmembername$/i, @blacklist))
				{
					push(@Max, "�޷����Ͷ���Ϣ���Է�-$_�ѽ���������������ڣ�����������κζ���Ϣ��");
					next;
				}
			}

			my $messfilename = "${lbdir}${msgdir}/main/${cleanintouser}_mian.cgi";
			if (open(FILE, $messfilename))
			{
				$mess = <FILE>;
				close(FILE);	
				push(@NoPM, "�޷����Ͷ���Ϣ-$_�����˶���Ϣ����Ź��ܡ�<br><br>�Զ�����Żظ� <font color=$fonthighlight>$mess</font><br><br>");
				next;
			}
		}

		my $tmp = &dofilter("$inmsgtitle\t$inmessage");
		($inmsgtitle, $inmessage) = split (/\t/, $tmp);
		
		$inmsgtitle =~ s/()+//isg;
		my $tempinmsgtitle = $inmsgtitle;
		$tempinmsgtitle =~ s/ //g;
		$tempinmsgtitle =~ s/\&nbsp\;//g;
		$tempinmsgtitle =~ s/��//isg;
		$tempinmsgtitle =~ s/��//isg;
		$tempinmsgtitle =~ s/^����������//;
		&error("��������&���������⣡&msg") if ($tempinmsgtitle eq "");
		&error("��������&�뽫��Ϣ��д������&msg") if ($inmessage eq "");

		my $filetoopen = "${lbdir}${msgdir}/in/${cleanintouser}_msg.cgi";
		&winlock($filetoopen) if ($OS_USED eq "Nt");
		if (open(FILE, $filetoopen)) {
			flock(FILE, 1) if ($OS_USED eq "Unix");
       			sysread(FILE, $inboxmessages,(stat(FILE))[7]);
			close(FILE);
			$inboxmessages =~ s/\r//isg;
		}
		open(FILE, ">$filetoopen");
		flock(FILE, 2) if ($OS_USED eq "Unix");
		print FILE "����������$inmembername\tno\t$currenttime\t$inmsgtitle\t$inmessage\t$attach\n$inboxmessages";
		close(FILE);
		&winunlock($filetoopen) if ($OS_USED eq "Nt");
		unlink ("${lbdir}cache/mymsg/${cleanintouser}.pl");
	}

	if ($inbackup eq "yes")
	{
		undef @outboxmessages;

		$filetoopen = "${lbdir}${msgdir}/out/${memberfilename}_out.cgi";
		&winlock($filetoopen) if ($OS_USED eq "Nt");
		if (open (FILE, $filetoopen)) {
			flock(FILE, 1) if ($OS_USED eq "Unix");
       			sysread(FILE, $outboxmessages,(stat(FILE))[7]);
			close(FILE);
			$outboxmessages =~ s/\r//isg;
		}
		open(FILE, ">$filetoopen");
		flock(FILE, 2) if ($OS_USED eq "Unix");
		$intouser =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
		print FILE "����������$intouser\tyes\t$currenttime\t$inmsgtitle\t$inmessage\t$attach\n$outboxmessages";
		close(FILE);
		&winunlock($filetoopen) if ($OS_USED eq "Nt");
		$backupmsg = "����ϢͬʱҲ���Ƶ����ķ��������ˣ�<br>";
	}

	$output .= qq~
<tr><td bgColor=$miscbacktwo align=center><font color=$fontcolormisc><b>�շ�����Ϣ</b></td></tr>
<tr><td bgColor=$miscbackone align=center><a href=$thisprog?action=inbox>$inboxpm</a>��<a href=$thisprog?action=outbox>$outboxpm</a>��<a href=$thisprog?action=new>$newpm</a>��<a href="javascript:openscript('friendlist.cgi',420,320)">$friendpm</a>��<a href="javascript:openscript('blocklist.cgi',420,320)">$blockpm</a></td></tr>~;

	unless (@NoRegUser > 0 || @Max > 0 || @NoPM > 0)
	{
		$output .= qq~
<tr><td bgColor=$miscbackone align=center><font color=$fontcolormisc><b>��$intouser�Ķ���Ϣ�Ѿ�������</b>$backupmsg<br>�Զ������ռ��䡣<br><br></td></tr>
<meta http-equiv="refresh" Content="2; url=$thisprog?action=inbox">~;
	}
	else
	{
		$output .= qq~
<tr><td bgColor=$miscbackone align=center><font color=$fontcolormisc><b>����Ϣ�����д���</b>$backupmsg<br><br><br></td></tr>~;

		foreach (@NoRegUser, @Max, @NoPM)
		{
			$output .= qq~
<tr><td bgColor=$miscbackone align=center>$_</td></tr>~;
		}
	}
}

elsif ($action eq "outbox")
{
	$filetoopen = "${lbdir}${msgdir}/out/${memberfilename}_out.cgi";
	if (open(FILE, $filetoopen)) {
		sysread(FILE, my $outboxmessages,(stat(FILE))[7]);
		close(FILE);
		$outboxmessages =~ s/\r//isg;
		@outboxmessages = split (/\n/, $outboxmessages);
	}
	$totalinboxmessages = @outboxmessages;

	$output .= qq~
<style>
input	{border-top-width: 1px; padding-right: 1px; padding-left: 1px; border-left-width: 1px; font-size: 9pt; border-left-color: #cccccc; border-bottom-width: 1px; border-bottom-color: #cccccc; padding-bottom: 1px; border-top-color: #cccccc; padding-top: 1px; height: 18px; border-right-width: 1px; border-right-color: #cccccc}
</style>
<script language="JavaScript">
function CheckAll(form)
{
	for (var i = 0; i < form.elements.length; i++) form.elements[i].checked = true;
}
function FanAll(form)
{
	for (var i = 0; i < form.elements.length; i++) form.elements[i].checked = !(form.elements[i].checked);
}
</script>
<form action=$thisprog method=POST>
<input type=hidden name=where value="outbox">
<input type=hidden name=action value="delete">
<tr><td bgColor=$miscbacktwo align=center colSpan=3 $catbackpic height=26><font color=$fontcolormisc><b>��ӭʹ�ö���Ϣ���ͣ�$inmembername</b></td></tr>
<tr><td bgColor=$miscbackone align=center colSpan=3><a href=$thisprog?action=inbox>$inboxpm</a>��<a href=$thisprog?action=outbox>$outboxpm</a>��<a href=$thisprog?action=new>$newpm</a>��<a href="javascript:openscript('friendlist.cgi', 420, 320)">$friendpm</a>��<a href="javascript:openscript('blocklist.cgi', 420, 320)">$blockpm</a></td></tr>
<tr>
<td bgColor=$miscbackone align=center width=20%><font color=$fontcolormisc><b>�ռ���</b></td>
<td bgColor=$miscbackone align=center><font color=$fontcolormisc><b>����</b></td>
<td bgColor=$miscbackone align=center width=10%><font color=$fontcolormisc><b>ɾ�����</b></td>
</tr>~;
	&splitpage("outbox");

	foreach (@outboxmessages [$startarray .. $endarray])
	{
		chomp;
		my ($from, $readstate, $date, $messagetitle, $message, $attach) = split(/\t/, $_);
		$from =~ s/^����������//isg;
		$messagetitle = &dofilter($messagetitle);
		$messagetitle = "<a href=$thisprog?action=outread&msg=$count>$messagetitle</a>";
		$messagetitle .= qq~ <img src=$imagesurl/icon/replyattachment.gif width=15 align=absmiddle alt="����Ϣ�к��и���">~ if($attach ne '');
		my $tempform = my $tempname = $from;
		$from = &lbhz($from, 12);
		$tempname =~ s/ /\_/g;
		$tempname = uri_escape($tempname);
		$output .= qq~
<tr>
<td bgColor=$miscbackone align=center><font color=$fontcolormisc><a href=profile.cgi?action=show&member=$tempname target=_blank title="$tempform">$from</a></td>
<td bgColor=$miscbackone><font color=$fontcolormisc>&nbsp;$messagetitle</td>
<td bgColor=$miscbackone align=center><font color=$fontcolormisc><b><input type=checkbox name="msg" value="$count" class=1></b></td>
</tr>~;
		$count++;
 	}
	$output .= qq~
<tr><td bgColor=$miscbacktwo align=center colSpan=3>$pages<font color=$fontcolormisc><a href=$thisprog?action=deleteall&where=outbox>[ɾ������]</a>  <a href=$thisprog?action=exportall&where=outbox>[��������]</a>  <input type=button name=chkall value="ȫѡ" OnClick="CheckAll(this.form)"> <input type=button name=clear2 value="��ѡ" OnClick="FanAll(this.form)"> <input type=reset name=Reset value="����"> <input type=submit name=delete value="ɾ��"></td></tr></form>~;
}

elsif ($action eq "inbox")
{
	my $filetoopen = "${lbdir}${msgdir}/in/${memberfilename}_msg.cgi";
	if (open (FILE, $filetoopen)) {
		sysread(FILE, my $inboxmessages,(stat(FILE))[7]);
		close(FILE);
		$inboxmessages =~ s/\r//isg;
		@inboxmessages = split (/\n/, $inboxmessages);
	}
	$totalinboxmessages = @inboxmessages;

	$output .= qq~
<style>
input	{border-top-width: 1px; padding-right: 1px; padding-left: 1px; border-left-width: 1px; font-size: 9pt; border-left-color: #cccccc; border-bottom-width: 1px; border-bottom-color: #cccccc; padding-bottom: 1px; border-top-color: #cccccc; padding-top: 1px; height: 18px; border-right-width: 1px; border-right-color: #cccccc}
</style>
<script language="JavaScript">
function CheckAll(form)
{
	for (var i = 0; i < form.elements.length; i++) form.elements[i].checked = true;
}
function FanAll(form)
{
	for (var i = 0; i < form.elements.length; i++) form.elements[i].checked = !(form.elements[i].checked);
}
</script>
<form action=$thisprog method=POST>
<input type=hidden name=where value="inbox">
<input type=hidden name=action value="delete">
<tr><td bgColor=$miscbacktwo align=center colSpan=4 $catbackpic height=26><font color=$fontcolormisc>$dxxboom<b>��ӭʹ�������ռ��䣬$membername</b></td>
</tr>
<tr><td bgColor=$miscbackone align=center colSpan=4><a href=$thisprog?action=inbox>$inboxpm</a>��<a href=$thisprog?action=outbox>$outboxpm</a>��<a href=$thisprog?action=new>$newpm</a>��<a href="javascript:openscript('friendlist.cgi', 420, 320)">$friendpm</a>��<a href="javascript:openscript('blocklist.cgi', 420, 320)">$blockpm</a></td></tr>
<tr>
<td bgColor=$miscbackone align=center width=20%><font color=$fontcolormisc><b>������</b></td>
<td bgColor=$miscbackone align=center><font color=$fontcolormisc><b>����</b></td>
<td bgColor=$miscbackone align=center width=10%><font color=$fontcolormisc><b>�Ƿ��Ѷ�</b></td>
<td bgColor=$miscbackone align=center width=10%><font color=$fontcolormisc><b>ɾ�����</b></td>
</tr>~;
	&splitpage("inbox");

	foreach (@inboxmessages[$startarray .. $endarray])
	{
		my ($from, $readstate, $date, $messagetitle, $message, $attach) = split(/\t/, $_);
		$from =~ s/^����������//isg;
		$callstate = 1 if($readstate eq "no");
		my $readstate = $readstate eq "no" ? qq~<img src=$imagesurl/images/unread.gif border=0 alt="δ��" width=16 height=12>~ : qq~<img src=$imagesurl/images/read.gif border=0 alt="�Ѷ�" width=16 height=14>~;
		$messagetitle = &dofilter($messagetitle);
		$messagetitle = "<a href=$thisprog?action=read&msg=$count>$messagetitle</a>";
		$messagetitle .= qq~ <img src=$imagesurl/icon/replyattachment.gif width=15 height=15 align=absmiddle alt="����Ϣ�к��и���">~ if($attach ne '');
		my $tempform = my $tempname = $from;
		$from = &lbhz($from, 12);
		$tempname =~ s/ /\_/g;
		$tempname = uri_escape($tempname);
		$output .= qq~
<tr>
<td bgColor=$miscbackone align=center><font color=$fontcolormisc><a href=profile.cgi?action=show&member=$tempname target=_blank title="$tempform">$from</a></td>
<td bgColor=$miscbackone><font color=$fontcolormisc>&nbsp;$messagetitle</td>
<td bgColor=$miscbackone align=center>$readstate</td>
<td bgColor=$miscbackone align=center><font color=$fontcolormisc><b><input type=checkbox name=msg value="$count" class=1></b></td>
</tr>~;
		$count++;
	}
	if ($membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "amo" && $membercode ne "mo" && $maxmsgno != 0)
	{
		$pmpercent = int(($totalinboxmessages / $maxmsgno) * 100);
		if ($pmpercent < 100)
		{
			$output .= qq~
<tr><td bgColor=$miscbacktwo colSpan=4 align=center>�����ڵĶ���Ϣ�洢��: $pmpercent%</td></tr>
<tr><td bgColor=$miscbackone colSpan=4><img src=$imagesurl/images/pm_gauge.gif width=$pmpercent% height=9><table cellSpacing=1 width=100%><tr><td width=45% align=left>0%</td><td width=* align=center>50%</td><td width=45% align=right>100%</td></tr></table></td></tr>~;
		}
		else
		{
			$output .= qq~<tr><td bgColor=$miscbacktwo colSpan=4 align=center><font color=red>�����ڵĶ���Ϣ�洢���������粻����ɾ�������ܽ��ն���Ϣ</font></td></tr>~;
		}
	}
	$output .= qq~<bgsound src=$imagesurl/images/mail.wav border=0>~ if(($callstate eq '1')&&($infofreshtime ne ''));
	$output .= qq~<meta http-equiv="refresh" content="$infofreshtime; url=$thisprog?action=inbox">~ if($infofreshtime ne '');
	$output .= qq~
<tr><td bgColor=$miscbacktwo align=center colSpan=4>$pages<font color=$fontcolormisc><a href=$thisprog?action=deleteall&where=inbox>[ɾ������]</a> <a href=$thisprog?action=exportall&where=inbox>[��������]</a> <a href=$thisprog?action=markall&where=inbox>[�����Ѷ�]</a> <input type=button name=chkall value="ȫѡ" OnClick="CheckAll(this.form)"> <input type=button name=clear2 value="��ѡ" OnClick="FanAll(this.form)"> <input type=reset name=Reset value="����"> <input type=submit name=delete value="ɾ��"></td></tr></form>~;
}

elsif ($action eq "outread")
{
	$filetoopen = "${lbdir}${msgdir}/out/${memberfilename}_out.cgi";
	my @outboxmessages;
	if (open(FILE, $filetoopen)) {
		sysread(FILE, my $outboxmessages,(stat(FILE))[7]);
		close(FILE);
		$outboxmessages =~ s/\r//isg;
		@outboxmessages = split (/\n/, $outboxmessages);
	}
	my $msgtograb = $outboxmessages[$inmsg];
	&error("�����Ϣ&û�д���Ϣ�������Ϣ�ѱ�ɾ����&msg") if ($msgtograb eq "");

	$wwjf = "no";
	$hidejf = "no";
	$postjf = "no";
	$membercode = "no";
        
	my ($to, $readstate, $date, $messagetitle, $post, $attach) = split(/\t/, $msgtograb);
	$to =~ s/^����������//isg;
	$date = $date + ($timedifferencevalue + $timezone) * 3600;
	$date = &dateformat($date);
	
	$post1 = $post;
	&lbcode(\$post);
	if ($emoticons eq "on")
	{
		&doemoticons(\$post);
		&smilecode(\$post);
	}
	$remsg = "Re:$messagetitle";
	$fwmsg = "Fw:$messagetitle";
	$remodel = "$to�����ã��ϴ���д����\n\n------------------------------\n$post1\n------------------------------";
	$fwmodel = "$to�����ã�������ת������Ϣ��\n\n------------------------------\n$post1\n------------------------------";

	%readstatus = ("yes"=>"�Ѷ�", "no"=>"δ��");
        if ($inmsg < @outboxmessages - 1)
	{
		my $outboxdown = $inmsg + 1;
		(undef, $nreadstate, undef, $nmessagetitle, undef) = split(/\t/, $outboxmessages[$outboxdown]);
		$outboxmsgdown = qq~<a href=$thisprog?action=outread&msg=$outboxdown title="��һ����Ϣ: ($readstatus{$nreadstate})\n��Ϣ����: $nmessagetitle">��һ��</a>~;
	}
	if ($inmsg > 0)
	{
		my $outboxup = $inmsg - 1;
		(undef, $preadstate, undef, $pmessagetitle, undef) = split(/\t/, $outboxmessages[$outboxup]);
		$outboxmsgup = qq~<a href=$thisprog?action=outread&msg=$outboxup title="��һ����Ϣ: ($readstatus{$preadstate})\n��Ϣ����: $pmessagetitle">��һ��</a>~;
	}
	$outboxsplitline = " | " if ($outboxmsgdown ne "" && $outboxmsgup ne "");
	if ($outboxmsgdown ne "" || $outboxmsgup ne "")
	{
		$outboxtempone = "[ ";
		$outboxtemptwo = " ]";
	}
	my $attachfile = '';
	if ($attach ne '')
	{
		$attachfile = (split('����������', $attach), 1)[0];
		my $up_ext = lc((split(/\./, $attachfile))[-1]);
		my $filetype = "unknow";
		$filetype = $up_ext if (-e "${imagesdir}icon/$up_ext.gif");
		$attachfile = "<br><b>��Ϣ������</b><img src=$imagesurl/icon/$filetype.gif width=16 height=16> <a href=$thisprog?action=attach&box=out&msg=$inmsg target=_blank>$attachfile</a>";
		if (($filetype eq "gif")||($filetype eq "jpg")||($filetype eq "jpe")||($filetype eq "jpeg")||($filetype eq "tif")||($filetype eq "png")||($filetype eq "bmp")) {
			$post = qq~<a href=$thisprog?action=attach&box=out&msg=$inmsg target=_blank><img src=$thisprog?action=attach&box=out&msg=$inmsg border=0 alt=�������´������ͼƬ onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333" onmousewheel="return bbimg(this)"></a><p>$post~;
		}
	}

	$output .= qq~
<form name=re action=$thisprog method=POST><input type=hidden name=action value="new"><input type=hidden name=touser value="$to"><input type=hidden name=msgtitle value="$remsg"><input type=hidden name=message value="$remodel"></form>
<form name=fw action=$thisprog method=POST><input type=hidden name=action value="new"><input type=hidden name=touser value="$to"><input type=hidden name=msgtitle value="$fwmsg"><input type=hidden name=message value="$fwmodel"></form>
<tr><td bgColor=$miscbacktwo align=center colSpan=3 $catbackpic height=26><font color=$fontcolormisc><b>��ӭʹ�ö���Ϣ���գ�$inmembername</b></td></tr>
<tr><td bgColor=$miscbackone align=center colSpan=3><a href=$thisprog?action=delete&where=outbox&msg=$inmsg>$deletepm</a>��<a href=$thisprog?action=inbox>$inboxpm</a>��<a href=$thisprog?action=outbox>$outboxpm</a>��<a href=$thisprog?action=new>$newpm</a>��<a href="javascript:document.re.submit()">$replypm</a>��<a href="javascript:document.fw.submit()">$fwpm</a>��<a href="javascript:openscript('friendlist.cgi', 420, 320)">$friendpm</a>��<a href="javascript:openscript('blocklist.cgi', 420, 320)">$blockpm</a></td></tr>
<tr><td bgColor=$miscbacktwo align=center><font color=$fontcolormisc>��<b>$date</b>�������ʹ���Ϣ��<b>$to</b>��</td></tr>
<tr><td bgColor=$miscbackone valign=top><font color=$fontcolormisc>
<b>��Ϣ���⣺$messagetitle</b>$attachfile<p>$post
<p align=right>$outboxtempone$outboxmsgup$outboxsplitline$outboxmsgdown$outboxtemptwo</p>
</td></tr>~;
}

elsif ($action eq "read")
{
	my $filetoopen = "${lbdir}${msgdir}/in/${memberfilename}_msg.cgi";
	&winlock($filetoopen) if ($OS_USED eq "Nt");
	my @inboxmessages;
	if (open(FILE, $filetoopen)) {
        	flock (FILE, 1) if ($OS_USED eq "Unix");
		sysread(FILE, my $inboxmessages,(stat(FILE))[7]);
		close(FILE);
		$inboxmessages =~ s/\r//isg;
		@inboxmessages = split (/\n/, $inboxmessages);
	}
	$msgtograb = $inboxmessages[$inmsg];
	chomp $msgtograb;
	if ($msgtograb eq "")
	{
		&winunlock($filetoopen) if ($OS_USED eq "Nt");
		&error("�����Ϣ&û�д���Ϣ�������Ϣ�ѱ�ɾ����&msg");
	}
	my ($from, $readstate, $date, $messagetitle, $post, $attach) = split(/\t/, $msgtograb);
	if ($readstate eq "no")
	{
		$count = 0;
		open(FILE, ">$filetoopen");
		flock(FILE, 2) if ($OS_USED eq "Unix");
		foreach (@inboxmessages)
		{
			chomp;
			if ($count eq $inmsg) {
				print FILE "$from\tyes\t$date\t$messagetitle\t$post\t$attach\n";
			}
			else {
				print FILE "$_\n";
			}
			$count++;
		}
		close (FILE);
	}
	&winunlock($filetoopen) if ($OS_USED eq "Nt");

	$wwjf = "no";
	$hidejf = "no";
	$postjf = "no";
	$membercode = "no";

	$from =~ s/^����������//isg;
	$date = $date + ($timedifferencevalue + $timezone) * 3600;
	$date = &dateformat($date);

	$post1 = $post;
	&lbcode(\$post);
	if ($emoticons eq "on")
	{
		&doemoticons(\$post);
		&smilecode(\$post);
	}

       if($messagetitle =~m/^Re:(.+?)$/){ 
       $omessagetitle=$messagetitle; 
       $replynum=1; 
       while($omessagetitle =~ m/^Re:/){ 
       $replynum++;$omessagetitle=~s/^Re://s; 
       } 
       $remsg="Re($replynum):$omessagetitle"; 
       }elsif($messagetitle =~m/^Re(.+?):(.+?)$/){ 
       $omessagetitle=$messagetitle; 
       $replynum=$1; 
       $replynum=~s/^\(//; 
       $replynum=~s/\)$//; 
       $replynum=int($replynum)+1; 
       $omessagetitle=~s/^Re(.+?)://; 
       $remsg="Re($replynum):$omessagetitle"; 
       }else{ 
       $remsg="Re:$messagetitle"; 
       } 
       if($messagetitle =~m/^Fw:(.+?)$/){ 
       $omessagetitle=$messagetitle; 
       $fornum=1; 
       while($omessagetitle =~ m/^Fw:/){ 
       $fornum++;$omessagetitle=~s/^Fw://s; 
       } 
       $fwmsg="Fw($fornum):$omessagetitle"; 
       }elsif($messagetitle =~m/^Fw(.+?):(.+?)$/){ 
       $omessagetitle=$messagetitle; 
       $fornum=$1; 
       $fornum=~s/^\(//; 
       $fornum=~s/\)$//; 
       $fornum=int($fornum)+1; 
       $omessagetitle=~s/^Fw(.+?)://; 
       $fwmsg="Fw($fornum):$omessagetitle"; 
       }else{ 
       $fwmsg="Fw:$messagetitle"; 
       } 

	$post1 =~ s/<p>/\n\n/ig;
	$post1 =~ s/<br>/\n/ig;
	$post1 =~ s/[\"|\<|\>]//ig;
	$remodel = "$from�����ã��ϴ���д����\n\n------------------------------\n$post1------------------------------";
	$fwmodel = "$from�����ã�������ת������Ϣ��\n\n------------------------------\n$post1------------------------------";

	%readstatus = ("yes"=>"�Ѷ�", "no"=>"δ��");
        if ($inmsg < @inboxmessages - 1)
	{
		my $inboxdown = $inmsg + 1;
		(undef, $nreadstate, undef, $nmessagetitle, undef) = split(/\t/, $inboxmessages[$inboxdown]);
		$inboxmsgdown = qq~<a href=$thisprog?action=read&msg=$inboxdown title="��һ����Ϣ: ($readstatus{$nreadstate})\n��Ϣ����: $nmessagetitle">��һ��</a>~;
	}
	if ($inmsg > 0)
	{
		my $inboxup = $inmsg - 1;
		(undef, $preadstate, undef, $pmessagetitle, undef) = split(/\t/, $inboxmessages[$inboxup]);
		$inboxmsgup = qq~<a href=$thisprog?action=read&msg=$inboxup title="��һ����Ϣ: ($readstatus{$preadstate})\n��Ϣ����: $pmessagetitle">��һ��</a>~;
	}
	$inboxsplitline = " | " if ($inboxmsgdown ne "" && $inboxmsgup ne "");
	if ($inboxmsgdown ne "" || $inboxmsgup ne "")
	{
		$inboxtempone = "[ ";
		$inboxtemptwo = " ]";
	}

	my $attachfile = '';
	if ($attach ne '')
	{
		$attachfile = (split('����������', $attach), 1)[0];
		my $up_ext = lc((split(/\./, $attachfile))[-1]);
		my $filetype = "unknow";
		$filetype = $up_ext if (-e "${imagesdir}icon/$up_ext.gif");
		$attachfile = "<br><b>��Ϣ������</b><img src=$imagesurl/icon/$filetype.gif width=16 height=16> <a href=$thisprog?action=attach&box=in&msg=$inmsg target=_blank>$attachfile</a>";
		if (($filetype eq "gif")||($filetype eq "jpg")||($filetype eq "jpe")||($filetype eq "jpeg")||($filetype eq "tif")||($filetype eq "png")||($filetype eq "bmp")) {
			$post = qq~<a href=$thisprog?action=attach&box=in&msg=$inmsg target=_blank><img src=$thisprog?action=attach&box=in&msg=$inmsg border=0 alt=�������´������ͼƬ onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333" onmousewheel="return bbimg(this)"></a><p>$post~;
		}
	}

	$output .= qq~
<form name=re action=$thisprog method=POST><input type=hidden name=action value="new"><input type=hidden name=touser value="$from"><input type=hidden name=msgtitle value="$remsg"><input type=hidden name=message value="$remodel"></form>
<form name=fw action=$thisprog method=POST><input type=hidden name=action value="new"><input type=hidden name=touser value="$from"><input type=hidden name=msgtitle value="$fwmsg"><input type=hidden name=message value="$fwmodel"></form>
<tr><td bgColor=$miscbacktwo align=center colSpan=2 $catbackpic height=26><font color=$fontcolormisc><b>��ӭʹ�������ռ��䣬$inmembername</b></td></tr>
<tr><td bgColor=$miscbackone align=center colSpan=2><a href=$thisprog?action=delete&where=inbox&msg=$inmsg>$deletepm</a>��<a href=$thisprog?action=inbox>$inboxpm</a>��<a href=$thisprog?action=outbox>$outboxpm</a>��<a href=$thisprog?action=new>$newpm</a>��<a href="javascript:document.re.submit()">$replypm</a>��<a href="javascript:document.fw.submit()">$fwpm</a>��<a href="javascript:openscript('friendlist.cgi', 420, 320)">$friendpm</a>��<a href="javascript:openscript('blocklist.cgi', 420, 320)">$blockpm</a></td></tr>
<tr><td bgColor=$miscbacktwo align=center colSpan=2><font color=$fontcolormisc>��Ϣ����<b>$from</b>�����͸�����ʱ�䣺<b>$date</b></font></td></tr>
<tr><td bgColor=$miscbackone valign=top colSpan=2><font color=$fontcolormisc>
<b>��Ϣ���⣺$messagetitle</b>$attachfile<p>$post
<p align=right>$inboxtempone$inboxmsgup$inboxsplitline$inboxmsgdown$inboxtemptwo</p>
</td></tr>
<tr>
<td bgColor=$miscbacktwo valign=top width=20%><font color=$fontcolormisc><b>���ٻظ���</b></td> 
<td bgColor=$miscbacktwo>$remsg</td> 
</tr>
<tr> 
<form action=$thisprog method=POST name=FORM enctype="multipart/form-data"><input type=hidden name=action value="send"><input type=hidden name=touser value="$from"><input type=hidden name=msgtitle value="$remsg">
<td bgColor=$miscbackone valign=top width=20%><font color=$fontcolormisc><b>���ݣ�</b></td> 
<td bgColor=$miscbackone><textarea cols=35 rows=4 name=message OnKeyDown="ctlent()"></textarea><br><input type=checkbox name=backup value=yes class=1><font color=$fontcolormisc>�Ƿ���һ����Ϣ�������䣿</font></td>
</tr>
~;
	if ($allowmsgattachment ne 'no')
	{
		my $addtypedisp = $addtype;
		$addtypedisp =~ s/\, /\,/ig;
		$addtypedisp =~ s/ \,/\,/ig;
		$addtypedisp =~ tr/A-Z/a-z/;
		my @addtypedisp = split(/\,/, $addtypedisp);
		$addtypedisp = "<select><option value=#>֧�����ͣ�</option><option value=#>----------</option>";
		foreach (@addtypedisp)
		{
			chomp;
			next if ($_ eq "");
			$addtypedisp .= "<option>$_</option>";
		}
		$addtypedisp .= qq~</select>~;
		$output .= qq~
<tr>
<td bgColor=$miscbackone valign=top width=30%><font color=$fontcolormisc><b>������</b><br>(��� <b>60</b> KB)</font></td>
<td bgColor=$miscbackone><input type=file size=30 name=addme><br>$addtypedisp</td>
</tr>
~;
	}
$output .= qq~
<tr><td bgColor=$miscbacktwo colSpan=2 align=center><input type=submit value="�� ��" name=Submit>   <input type=reset name=Clear value="�� ��"></td></form></tr>~;
}

elsif ($action eq "deleteall")
{
	my $filetotrash = $inwhere eq "inbox" ? "${lbdir}${msgdir}/in/${memberfilename}_msg.cgi" : "${lbdir}${msgdir}/out/${memberfilename}_out.cgi";
	unlink($filetotrash);
	my $wherename = $inwhere eq "inbox" ? "�ռ���" : "������";
	$output .= qq~
<tr><td bgColor=$miscbacktwo align=center><font color=$fontcolormisc><b>���еĶ���Ϣ�ѱ�ɾ��</b></td></tr>
<tr><td bgColor=$miscbackone align=center><a href=$thisprog?action=inbox>$inboxpm</a>��<a href=$thisprog?action=outbox>$outboxpm</a>��<a href=$thisprog?action=new>$newpm</a>��<a href="javascript:openscript('friendlist.cgi', 420, 320)">$friendpm</a>��<a href="javascript:openscript('blocklist.cgi', 420, 320)">$blockpm</a></td></tr>
<tr><td bgColor=$miscbackone align=center><font color=$fontcolormisc><b>����$wherename�еĶ���Ϣ�Ѿ�ȫ��ɾ��</b><br><br></td></tr>~;
}

elsif ($action eq "delete")
{
	@inmsg= $query->param("msg");
	my $filetoopen = $inwhere eq "inbox" ? "${lbdir}${msgdir}/in/${memberfilename}_msg.cgi" : "${lbdir}${msgdir}/out/${memberfilename}_out.cgi";
	my @boxmessages;

	&winlock($filetoopen) if ($OS_USED eq "Nt");
	if (open(FILE, $filetoopen)) {
		flock(FILE, 1) if ($OS_USED eq "Unix");
		sysread(FILE, my $boxmessages,(stat(FILE))[7]);
		close(FILE);
		$boxmessages =~ s/\r//isg;
		@boxmessages = split (/\n/, $boxmessages);
	}
	$count = 0;
	open (FILE, ">$filetoopen");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	foreach $line (@boxmessages) {
		chomp($line);
		my $checkmsg = 0;
		foreach (@inmsg)
		{
			if ($count eq $_)
			{
				$checkmsg = 1;
				last;
			}
		}
		print FILE "$line\n" if ($checkmsg == 0 && $line ne "");
		$count++;
	}
	close(FILE);
	&winunlock($filetoopen) if ($OS_USED eq "Nt");
	my $wherename = $inwhere eq "inbox" ? "�ռ���" : "������";
	$output .= qq~
<tr><td bgColor=$miscbacktwo align=center><font color=$fontcolormisc><b>��Ϣɾ��</b></td></tr>
<tr><td bgColor=$miscbackone align=center><a href=$thisprog?action=inbox>$inboxpm</a>��<a href=$thisprog?action=outbox>$outboxpm</a>��<a href=$thisprog?action=new>$newpm</a>��<a href="javascript:openscript('friendlist.cgi', 420, 320)">$friendpm</a>��<a href="javascript:openscript('blocklist.cgi',420,320)">$blockpm</a></td></tr>
<tr><td bgColor=$miscbackone align=center><font color=$fontcolormisc><b>����$wherename�еĶ���Ϣ�Ѿ�ɾ����<br><br>�Զ�����$wherename<br><br></b></td></tr>
<meta http-equiv="refresh" Content="2; url=$thisprog?action=$inwhere">~;
}
elsif($action eq "disable_pm"){
	my $disable_pm_status = ($query->param('disable_pm_status') eq "����")?"����":"�ر�";
	my $disable_pm_mess = &lbhz(&unHTML($query->param('mess')),40);
	my $memberfilename = $inmembername;
	$memberfilename =~ s/ /\_/g;
	$memberfilename =~ tr/A-Z/a-z/;
	my $messfilename = "${lbdir}${msgdir}/main/${memberfilename}_mian.cgi";
	if($disable_pm_status eq "����"){
		if (length($disable_pm_mess) == 0) {
			$disable_pm_mess = "�Բ��������ں�æ�������Ժ�����ϵ�ҡ�";
		}else {
			$disable_pm_mess =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\=\+\\\'\:\"\/\<\>\?\[\]]//isg;
		}
		if (open(FILE,">$messfilename")) {
			print FILE "$disable_pm_mess";
			close(FILE);
		}
	}else{
	    chomp $messfilename;
	    unlink ($messfilename) if (-e $messfilename);
	}
	$output .= qq~
<tr><td bgColor=$miscbacktwo align=center><font color=$fontcolormisc><b>����Ϣ�����</b></td></tr>
<tr><td bgColor=$miscbackone align=center><a href=$thisprog?action=inbox>$inboxpm</a>��<a href=$thisprog?action=outbox>$outboxpm</a>��<a href=$thisprog?action=new>$newpm</a>��<a href="javascript:openscript('friendlist.cgi', 420, 320)">$friendpm</a>��<a href="javascript:openscript('blocklist.cgi',420,320)">$blockpm</a></td></tr>
<tr><td bgColor=$miscbackone align=center><font color=$fontcolormisc><b>����$disable_pm_status�����ģʽ��<br><br>�Զ������ռ���<br><br></b></td></tr>
<meta http-equiv="refresh" Content="2; url=$thisprog?action=inbox">~;
}
$memberfilename = $inmembername;
$memberfilename =~ s/ /\_/g;
$memberfilename =~ tr/A-Z/a-z/;
my $messfilename = "${lbdir}${msgdir}/main/${memberfilename}_mian.cgi";
my $disable_pm_mess ="";
if (open(FILE, $messfilename)){
	$disable_pm_mess = <FILE>;
	close(FILE);
}
$now_status=($disable_pm_mess ne "")?"����":"�ر�";
$disable_pm_mess = "�Բ��������ں�æ�������Ժ�����ϵ�ҡ�" if (length($disable_pm_mess) == 0);

	my $cleanname = $intouser;
	$cleanname =~ tr/A-Z/a-z/;
	$cleanname =~ s/\_/ /g;
	$inmessage =~ s/<p>/\n\n/ig;
	$inmessage =~ s/<br>/\n/ig;

	if (open(FILE, "${lbdir}memfriend/${memberfilename}.cgi")) {
		my $currentlist = <FILE>;
		close(FILE);
		@currentlist = split (/\n/, $currentlist);
	}
	my $friendlist = "";
	foreach (@currentlist) {
		chomp;
		s/^����������//isg;
		$friendlist .= qq~<option value="$_">$_</option>~;
	}

$output.=qq~</table></td></tr></table><SCRIPT>valignend()</SCRIPT><br>

<form action=$thisprog method=POST><input type=hidden name=action value="disable_pm">
<p>
<SCRIPT>valigntop()</SCRIPT><table cellPadding=0 cellSpacing=0 width=$tablewidth bgColor=$tablebordercolor align=center><tr><td>
<table cellPadding=3 cellSpacing=1 width=100%><tr>
<td bgColor=$miscbacktwo align=center width="30%"><b>����Ϣ�����״̬��</b> <u style="color:$fonthighlight">$now_status</u></td>
<td bgColor=$miscbackone align=center><input type="text" name="mess" size=20 maxlength=40 value="$disable_pm_mess"></td>
<td bgColor=$miscbacktwo align=center width="25%"><input type="submit" value="����" name="disable_pm_status"> <input type="submit" value="�ر�" name="disable_pm_status"></td>
</tr>
</form>~;

$output .= "</table></td></tr></table><SCRIPT>valignend()</SCRIPT>";
&output("$boardname - ����Ϣ",\$output,"msg");

sub splitpage
{
	$maxthread = 9 if ($maxthread !~ /^[0-9]+$/);
	my $tmp = shift;
	my $instart = $query->param("start");
	$instart = 0 if ($instart !~ /^[0-9]+$/);
	$count = $instart;
	my $tempnumberofpages = $totalinboxmessages / $maxthread;
	my $numberofpages = int($tempnumberofpages);
	$numberofpages++ if ($numberofpages != $tempnumberofpages);

	if ($numberofpages > 1)
	{
		$startarray = $instart;
		$endarray = $instart + $maxthread - 1;
		$endarray = $totalinboxmessages - 1 if ($endarray >= $totalinboxmessages);

		my $currentpage = int($instart / $maxthread) + 1;
		my $endstart = ($numberofpages - 1) * $maxthread;
		my $beginpage = $currentpage == 1 ? "<font color=$fonthighlight face=webdings>9</font>" : qq~<a href=$thisprog?action=$tmp&start=0 title="�� ҳ" ><font face=webdings>9</font></a>~;
		my $endpage = $currentpage == $numberofpages ? "<font color=$fonthighlight face=webdings>:</font>" : qq~<a href=$thisprog?action=$tmp&start=$endstart title="β ҳ" ><font face=webdings>:</font></a>~;

		my $uppage = $currentpage - 1;
		my $nextpage = $currentpage + 1;
		my $upstart = $instart - $maxthread;
		my $nextstart = $instart + $maxthread;
		my $showup = $uppage < 1 ? "<font color=$fonthighlight face=webdings>7</font>" : qq~<a href=$thisprog?action=$tmp&start=$upstart title="��$uppageҳ"><font face=webdings>7</font></a>~;
		my $shownext = $nextpage > $numberofpages ? "<font color=$fonthighlight face=webdings>8</font>" : qq~<a href=$thisprog?action=$tmp&start=$nextstart title="��$nextpageҳ"><font face=webdings>8</font></a>~;

		my $tempstep = $currentpage / 7;
		my $currentstep = int($tempstep);
		$currentstep++ if ($currentstep != $tempstep);
		my $upsteppage = ($currentstep - 1) * 7;
		my $nextsteppage = $currentstep * 7 + 1;
		my $upstepstart = ($upsteppage - 1) * $maxthread;
		my $nextstepstart = ($nextsteppage - 1) * $maxthread;
		my $showupstep = $upsteppage < 1 ? "" : qq~<a href=$thisprog?action=$tmp&start=$upstepstart class=hb title="��$upsteppageҳ">��</a> ~;
		my $shownextstep = $nextsteppage > $numberofpages ? "" : qq~<a href=$thisprog?action=$tmp&start=$nextstepstart class=hb title="��$nextsteppageҳ">��</a> ~;

		$pages = "";
		for (my $i = $upsteppage + 1; $i < $nextsteppage; $i++)
		{
			last if ($i > $numberofpages);
			my $currentstart = ($i - 1) * $maxthread;
			$pages .= $i == $currentpage ? "<font color=$fonthighlight><b>$i</b></font> " : qq~<a href=$thisprog?action=$tmp&start=$currentstart class=hb>$i</a> ~;
		}
		$pages = "<font color=$menufontcolor><b>�� <font color=$fonthighlight>$numberofpages</font> ҳ</b> $beginpage $showup \[ $showupstep$pages$shownextstep\] $shownext $endpage</font><br>";
	}
	else
	{
		$startarray = 0;
		$endarray = $totalinboxmessages - 1;
		$pages = "<font color=$menufontcolor>ֻ��һҳ</font><br>";
	}
	return;
}

sub Base64encode
#Base64���뺯��
{
	my $res = pack("u", $_[0]);
	$res =~ s/^.//mg;
	$res =~ s/\n//g;
	$res =~ tr|` -_|AA-Za-z0-9+/|;
	my $padding = (3 - length($_[0]) % 3) % 3;
	$res =~ s/.{$padding}$/'=' x $padding/e if $padding;
	return $res;
}

sub Base64decode
#Base64���뺯��
{
	local($^W) = 0;
	my $str = shift;
	my $res = '';
   
	$str =~ tr|A-Za-z0-9+/||cd;
	$str =~ tr|A-Za-z0-9+/| -_|;
	while ($str =~ /(.{1,60})/gs)
	{
		my $len = chr(32 + length($1)*3/4);
		$res .= unpack("u", $len . $1 );
	}
	return $res;
}
