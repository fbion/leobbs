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
$LBCGI::POST_MAX = 200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "recopr.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

$inmembername = $query->cookie("amembernamecookie") if (!$inmembername);
$inpassword = $query->cookie("apasswordcookie") if (!$inpassword);
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($inmembername eq "" || $inmembername eq "����" )
{
	&error("��ͨ����&�����ڵ�����Ƿÿͣ������¼�Ժ���ܲ鿴�������⣡");
}
else
{
	&getmember($inmembername,"no");
     if ($inpassword ne $password) {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("��ͨ����&�������û���������������µ�¼��");
     }
	&error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
}

$inselectstyle  = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

    opendir (DIRS, "$lbdir");
    my @files = readdir(DIRS);
    closedir (DIRS);
    @files = grep(/^\w+?$/i, @files);
    my @recorddir = grep(/^record/i, @files);
    my $recorddir = $recorddir[0];

$action = $query->param("action");
if ($action eq "post")
{
	$title = "�ұ��ظ�������";
	&getmytopic("post");
}
elsif ($action eq "reply")
{
	$title = "�Ҳ��������";
	&getmytopic("reply");
}
else
{
	$title = "��̳������";
	&getmytopic("all");
}

$output = qq~<p>
<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellpadding=3 cellspacing=1 width=100%>
<tr><td bgcolor=$miscbacktwo $catbackpic align=center height=26><font color=$fontcolormisc><b>$title</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>$mytopics</font></td></tr>
</table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&output("$boardname - �����ע",\$output,"msg");
exit;

sub getmytopic
{
	my $mode = shift;
	if ($mode eq "all")
	{
		$filetoopen = $lbdir . "data/recentpost.cgi";
	}
	else
	{
		my $cleanmembername = $inmembername;
		$cleanmembername =~ s/ /\_/isg;
		$cleanmembername =~ tr/A-Z/a-z/;
		$filetoopen = $lbdir . "$recorddir/" . $mode . "/" . $cleanmembername . ".cgi";
	}
	my @temptopics;
	if (-e $filetoopen)
	{
		open(FILE, $filetoopen);
		@temptopics = <FILE>;
		close(FILE);
	}
	$mytopics = "";
	if (@temptopics)
	{
		foreach (@temptopics)
		{
			chomp($_);
			my ($tempinforum, $tempintopic, $temptopictitle, $tempcurrenttime, $tempposticon, $tempmembername) = split(/\t/, $_);
	                $temptopictitle =~ s/^����������//;
            		next if (($tempinforum !~ /^[0-9]+$/)||($tempintopic !~ /^[0-9]+$/));
			if (($tempposticon eq "") || ($tempposticon !~ /^[0-9]+\.gif$/i)) {
				$tempposticon = int(myrand(23));
				if ($tempposticon <10 ) {
				    $tempposticon = "0$tempposticon.gif";
				} else {
				    $tempposticon = "$tempposticon.gif";
				}
			}

	    $temptopictitle = &cleanarea("$temptopictitle");
	    $temptopictitle =~ s/\'/\`/g;
            $temptopictitle =~ s/\&amp;/\&/g;
	    $temptopictitle =~ s/\&quot;/\"/g;
#	    $topictitle =~ s/\&lt;/</g;
#	    $topictitle =~ s/\&gt;/>/g;
	    $temptopictitle =~ s/ \&nbsp;/��/g;

				$addmspace ="";
			if (length($temptopictitle) > 45)
			{
				$temptopictitle = &lbhz($temptopictitle, 45);
			}
			else
			{
				my $addspace = 45 - length($temptopictitle);
				for (my $i = 0; $i < $addspace; $i++) {$addmspace .= "&nbsp;";}
			}
			$temptopictitle =~ s/\&/\&amp;/g;
			$temptopictitle =~ s/\&amp;\#/\&\#/isg;
			$temptopictitle =~ s/\&amp\;(.{1,6})\&\#59\;/\&$1\;/isg;
			$temptopictitle =~ s/\&\#([0-9]{1,6})\&\#59\;/\&\#$1\;/isg;
			$temptopictitle =~ s/\"/\&quot;/g;
			$temptopictitle =~ s/</\&lt;/g;
			$temptopictitle =~ s/>/\&gt;/g;
			$temptopictitle =~ s/ /\&nbsp;/g;
			$tempcurrenttime = &dateformatshort($tempcurrenttime + $timezone * 3600 + $timedifferencevalue * 3600);
			if ($mode eq "all")
			{
				$mytopics .= qq~<img src=$imagesurl/posticons/$tempposticon border=0> <a href=$boardurl/topic.cgi?forum=$tempinforum&topic=$tempintopic target=_blank title="���ӷ���ʱ��: $tempcurrenttime">$temptopictitle</a>$addmspace [<a href=profile.cgi?action=show&member=~ . uri_escape($tempmembername) . qq~ title="����鿴$tempmembername������" target=_blank>$tempmembername</a>]<br>~;
			}
			elsif ($mode eq "post")
			{
				$mytopics .= qq~<img src=$imagesurl/posticons/$tempposticon border=0> <a href=$boardurl/topic.cgi?forum=$tempinforum&topic=$tempintopic target=_blank title="���ظ�ʱ��: $tempcurrenttime">$temptopictitle</a>$addmspace<br>~;
			}
			else
			{
				$mytopics .= qq~<img src=$imagesurl/posticons/$tempposticon border=0> <a href=$boardurl/topic.cgi?forum=$tempinforum&topic=$tempintopic target=_blank title="������ʱ��: $tempcurrenttime">$temptopictitle</a>$addmspace<br>~;
			}
		}
	}
	else
	{
		$mytopics = "����ʱû�м�¼";
	}
	return;
}