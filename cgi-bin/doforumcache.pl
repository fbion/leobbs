#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

$docache = "yes";
open(LOCKFILE, ">${lbdir}cache/forumcache-$skin.pl.lock");
print LOCKFILE "die;";
close(LOCKFILE);
if (open(FILE, "${lbdir}data/allforums.cgi")) {
    sysread(FILE, $forums,(stat(FILE))[7]);
    close(FILE);
    $forums =~ s/\r//isg;
}
else { unlink("${lbdir}cache/forumcache-$skin.pl.lock"); &error("��̳��û����&�����ڹ�������������̳�����߷�����Ϣ��ȫ��ʧ����̳�����������ؽ���̳�����棡"); }
@forums=split(/\n/,$forums);

my $a = 0;
foreach $forum (@forums) {
    $a  = sprintf("%09d",$a);
    chomp $forum;
    next if (length("$forum") < 30);
    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threadsno, $postsno, $forumgraphic,$tmp,$tmp,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpostno, $miscad5) = split(/\t/,$forum);
    next if (($forumid !~ /^[0-9]+$/)||($forumname eq ""));
    $forumdescription  = &HTML("$forumdescription");

    if (open(FILEFORUM,"${lbdir}boarddata/foruminfo$forumid.cgi")) {
        ($lastposttime, $threads, $posts, $todayforumpost, $lastposter) = split(/\t/,<FILEFORUM>);
        close(FILEFORUM);
    } else {
    	$lastposttime=$todayforumpost=$lastposter="";
    	$threads=$posts="0";
    }

    ($lastposttime,$threadnumber,$topictitle)=split(/\%\%\%/,$lastposttime);
    if ($topictitle) {
	$topictitle =~ s/^����������//;
	my $topictitletemp = $topictitle;
	$topictitletemp =~ s/\&lt;/</g;
	$topictitletemp =~ s/\&gt;/>/g;
	$topictitletemp =~ s/\&amp;/\&/g;
	$topictitletemp =~ s/\&nbsp;/ /g;
	$topictitletemp =~ s/  /��/g;
	$topictitletemp =~ s/\&quot;/\\\"/g;
	$topictitletemp = &lbhz($topictitle,18);
#	$topictitletemp =~ s/\&/\&amp;/g;
	$topictitletemp =~ s/</\&lt;/g;
	$topictitletemp =~ s/>/\&gt;/g;
	$topictitle = qq~&nbsp;���⣺ <a href=topic.cgi?forum=$forumid&topic=$threadnumber&replynum=last TITLE="$topictitle">$topictitletemp</a><BR>~;
	$lastposttime  = $lastposttime + $timeadd;
	$lastposterfilename = $lastposter;
	$lastposterfilename =~ y/ /_/;
	$lastposterfilename =~ tr/A-Z/a-z/;
	if ($lastposter=~/\(��\)/) {
	    $lastposter=~s/\(��\)//isg;
	    $lastposter  = qq~<font title="��Ϊδע���û�">&nbsp;��󷢱� $lastposter</font>��<img src="$imagesurl/images/lastpost.gif" width=11>~;
	}
	else { $lastposter  = qq~&nbsp;��󷢱� <span style="cursor:hand" onClick="javascript:O9('~ . uri_escape($lastposterfilename) . qq~')">$lastposter</span>��<img src="$imagesurl/images/lastpost.gif" width=11>~; }
    }
    $lastposttime="$lastposttime%%%$threadnumber%%%$topictitle";

    if ($teamlogo =~ m/\.swf$/i) { my ($fgwidth,$fgheight) = split(/\|/,$fgheight); $teamlogo= qq~<PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><embed src=$imagesurl/myimages/$teamlogo width=$fgwidth height=$fgheight quality=high pluginspage="http:\/\/www.macromedia.com\/shockwave\/download\/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application\/x-shockwave-flash"><\/embed>~; } elsif ($teamlogo ne "") { $teamlogo= qq~<img src=$imagesurl/myimages/$teamlogo border=0>~; }
    if ($teamlogo eq "") { $team = ""; } elsif (($teamurl eq "")||($teamurl eq "http://")) { $team=qq~<a href=forums.cgi?forum=$forumid>$teamlogo</a>~; } else { $team=qq~<a href=$teamurl>$teamlogo</a>~; }

    if ($category =~ /^childforum-[0-9]+/) {
    	$cforums[$forumid] = "$forumid\t$category\t$hiddenforum\t$forumname\t";
	$topforumno=$category;
	$topforumno=~s/^childforum-//;
	$threadadds[$topforumno]+=$threads;
	$postadds[$topforumno]+=$posts;
	($todayforumpost, $todayforumposttime) = split(/\|/,$todayforumpost);
	$todayforumpost = 0 if (($nowtime ne $todayforumposttime)||($todayforumpost eq ""));
	$todayforumpostadds[$topforumno]+=$todayforumpost;
	($olastposttime,undef)=split(/\%\%\%/,$lastposttime[$topforumno]);
	($clastposttime,undef)=split(/\%\%\%/,$lastposttime);
	if (($clastposttime > $olastposttime || ($lastposttime[$topforumno] eq "" && $lastposter[$topforumno] eq ""))&&($privateforum ne "yes")) {
	    $lastposttime[$topforumno]=$lastposttime."%%%$forumid";
	    $lastposter[$topforumno]=$lastposter;
	}
	$lvisit .= "$forumid-$currenttime--";
    } else {
	$lastposttime[$forumid]=$lastposttime;
	$lastposter[$forumid]=$lastposter;
	$categoryplace  = sprintf("%09d",$categoryplace);
	$rearrange = ("$categoryplace\t$a\t$category\t$forumname\t$forumdescription\t$privateforum\t$startnewthreads\t$lastposter\t$lastposttime\t$threads\t$posts\t$hiddenforum\t$forumid\t$team\t$miscad4\t$todayforumpost\t");
	push (@rearrangedforums, $rearrange);
	$lvisit .= "$forumid-$currenttime--";
	$a++;
    }

    $modnumber = 0;
    $modout="";
    $adminstyle = 2 if ($adminstyle eq "");
    if ($forummoderator) {
	$forummoderator =~ s/\, /\,/gi;
	$forummoderator =~ s/ \,/\,/gi;
	$forummoderator =~ s/\,\,/\,/gi;
	$forummoderator =~ s/\,$//gi;
	$forummoderator =~ s/^\,//gi;
	my @mods = split(/\,/,$forummoderator);
	$modnumber = @mods;
	my $modprintnum = 1;
	foreach (@mods) {
	    my $modname = $_;
            $modname =~ y/ /_/;
            $modname =~ tr/A-Z/a-z/;

	    if (($adminstyle eq 1)||($modnumber <= 3 && $adminstyle eq 3)) {
  	        last if ($modprintnum > 3 );
                if ($modprintnum != $modnumber) {
                    if(($_ =~m/����Ա/isg)||($_ =~m/��Ƹ��/isg)||($_ =~m/��ʱ��ȱ/isg)||($_ =~m/����/isg)||($_ =~m/����/isg)||($_ =~m/̳��/isg)){ $modout .= qq~<font color=$fontcolormisc2>$_</font><BR>~; } else { $modout .= qq~<span style=cursor:hand onClick="javascript:O9('~ . uri_escape($modname) . qq~')">$_</span><BR>~; }
                } else {
		    if(($_ =~m/����Ա/isg)||($_ =~m/��Ƹ��/isg)||($_ =~m/��ʱ��ȱ/isg)||($_ =~m/����/isg)||($_ =~m/����/isg)||($_ =~m/̳��/isg)){ $modout .= qq~<font color=$fontcolormisc2>$_</font>~; } else { $modout .= qq~<span style=cursor:hand onClick="javascript:O9('~ . uri_escape($modname) . qq~')">$_</span>~; }
	        }
	        $modprintnum++;
	    } else {
	        if(($_ =~m/����Ա/isg)||($_ =~m/��Ƹ��/isg)||($_ =~m/��ʱ��ȱ/isg)||($_ =~m/����/isg)||($_ =~m/����/isg)||($_ =~m/̳��/isg)){ $modout .= qq~<option>~ . &lbhz($_, 10) . qq~</option>~; } else { $modout .= qq~<option value="~ . &uri_escape($_) . qq~">~ . &lbhz($_, 10) . "</option>"; }
	    }
	}
    }
    if (($adminstyle eq 1)||($modnumber <= 3 && $adminstyle eq 3)) {
    	$modout .= qq~<font color=$fontcolormisc2>More...~ if ($modnumber > 3 );
        $modout  = "<font color=$fontcolormisc>��ʱ��ȱ<BR>��Ƹ��" if ($modout eq "");
    } else {
    	$modout  = "<option>��ʱ��ȱ</option><option>��Ƹ��</option>" if ($modout eq "");
        $modout = qq~<select onChange="surfto(this)"><option style="background-color: $forumcolorone">�����б�</option><option>----------</option>$modout</select>~;
    }
    $modout[$forumid] = $modout;
}
@rearrangedforums = sort(@rearrangedforums);
@forums = @cforums;

if (-e "$lbdir/data/todaypost.cgi") {
    open (FILE,"$lbdir/data/todaypost.cgi");
    $todaypost=<FILE>;
    close(FILE);
    chomp $todaypost;
    ($nowtoday,$todaypostno,$maxday,$maxdaypost,$yestdaypost)=split(/\t/,$todaypost);
    if ($nowtoday ne $nowtime) {
    	$yestdaypost = $todaypostno;
        $todaypostno = 0;
    }
} else {
    $maxday      = $nowtime;
    $yestdaypost = 0;
    $todaypostno = 0;
    $maxdaypost  = 0;
}
$yestdaypost = 0 if ($yestdaypost eq "");
$todaypostlist = qq~<font color=\$titlecolor>���� </font><font color=\$postfontcolortwo>��/��������: $yestdaypost/<font color=\$fonthighlight><b>$todaypostno</b></font> ƪ</font><BR><font color=\$titlecolor>���� </font><font color=\$postfontcolorone title="��������: $maxday">��ʷ���һ�췢����: <b>$maxdaypost</b> ƪ</font><BR>~;

eval { require "data/boardstats.cgi"; };
if ($@) { require "repireboardinfo.pl"; require "data/boardstats.cgi"; }

$cleanlastregistered = $lastregisteredmember;
$cleanlastregistered =~ y/ /_/;
$cleanlastregistered =~ tr/A-Z/a-z/;
$cleanlastregistered = qq~<span style="cursor:hand" onClick="javascript:O9('~ . uri_escape($cleanlastregistered) . qq~')">$lastregisteredmember</span>~;
$todaypostlist = qq~<td bgcolor=$forumcolortwo width=210><font color=$titlecolor>���� </font><font color=$postfontcolorone>���ע���Ա: $cleanlastregistered</font><BR><font color=$titlecolor>���� </font><font color=$postfontcolortwo>ע���Ա����:  <a href="memberlist.cgi?a=5" target=_blank><b><font color=#990000>$totalmembers</font></b></a> ��<br></font><font color=$titlecolor>���� </font><font color=$postfontcolorone>��̳��������: <b>$totalthreads</b> ƪ</font><br><font color=$titlecolor>���� </font><font color=$postfontcolortwo>��̳�ظ�����: <b>$totalposts</b> ƪ</font><br><font color=$titlecolor>���� </font><font color=$postfontcolorone>��ǰ��������: <a href=whosonline.cgi><B>totleonlineall</B></a> ��</font><br>$todaypostlist~;

if ($dispborn ne "no") {
    &birthday;
    unless (($dispborn eq "auto")&&($birthdayuser eq "")) {
        $birthdayuser = "����û���˹�����" if ($birthdayuser eq "");
        $birthdayoutput = qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=\$tablewidth bgcolor=\$tablebordercolor align=center><tr><td><table cellpadding=6 cellspacing=1 width=100%><tr><td bgcolor=\$titlecolor colspan=7 \$catbackpic><font color=\$titlefontcolor><B>-=> ��������յ�ע���û� ���� $borncount �ˣ�</b>     [<a href="calendar.cgi" target=_blank>��̳����</a>]</td></tr><tr><td bgcolor=\$forumcolorone align=center width=26><img src=$imagesurl/images/\$skin/born.gif alt="�����������Ա����" width=16></td><td bgcolor=\$forumcolortwo colspan=6 width=*><img src=$imagesurl/images/none.gif width=400 height=0><br>��<font color=\$forumfontcolor>$birthdayuser</td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT><img src=$imagesurl/images/none.gif height=5><br>~;
    }
}

require "${lbdir}data/forumcate.pl" if (($cancmodoutput ne "no")&&(-e "${lbdir}data/forumcate.pl"));

open (FILE, ">${lbdir}cache/forumcache-$skin.pl");
print FILE qq~\$lvisit="$lvisit";\n~;
for ($i=0;$i<=$#rearrangedforums;$i++) {
    $rearrangedforums[$i] =~ s/\\/\\\\/isg;
    $rearrangedforums[$i] =~ s/~/\\\~/isg;
    $rearrangedforums[$i] =~ s/\$/\\\$/isg;
    $rearrangedforums[$i] =~ s/\@/\\\@/isg;
    print FILE qq(\$rearrangedforums[$i] = qq~$rearrangedforums[$i]~;\n) if ($rearrangedforums[$i] ne "");
    $rearrangedforums[$i] =~ s/\\\~/~/isg;
    $rearrangedforums[$i] =~ s/\\\$/\$/isg;
    $rearrangedforums[$i] =~ s/\\\@/\@/isg;
    $rearrangedforums[$i] =~ s/\\\\/\\/isg;
}
for ($i=0;$i<=$#threadadds;$i++) {
    print FILE qq~\$threadadds[$i] = "$threadadds[$i]";\n~ if ($threadadds[$i] ne "");
}
for ($i=0;$i<=$#postadds;$i++) {
    print FILE qq~\$postadds[$i] = "$postadds[$i]";\n~ if ($postadds[$i] ne "");
}
for ($i=0;$i<=$#todayforumpostadds;$i++) {
    print FILE qq~\$todayforumpostadds[$i] = "$todayforumpostadds[$i]";\n~ if ($todayforumpostadds[$i] ne "");
}
for ($i=0;$i<=$#lastposttime;$i++) {
    $lastposttime[$i] =~ s/\\/\\\\/isg;
    $lastposttime[$i] =~ s/~/\\\~/isg;
    $lastposttime[$i] =~ s/\$/\\\$/isg;
    $lastposttime[$i] =~ s/\@/\\\@/isg;
    print FILE qq(\$lastposttime[$i] = qq~$lastposttime[$i]~;\n) if ($lastposttime[$i] ne "");
    $lastposttime[$i] =~ s/\\\~/~/isg;
    $lastposttime[$i] =~ s/\\\$/\$/isg;
    $lastposttime[$i] =~ s/\\\@/\@/isg;
    $lastposttime[$i] =~ s/\\\\/\\/isg;
}
for ($i=0;$i<=$#lastposter;$i++) {
    $lastposter[$i] =~ s/~/\\\~/isg;
    $lastposter[$i] =~ s/\$/\\\$/isg;
    $lastposter[$i] =~ s/\@/\\\@/isg;
    print FILE qq(\$lastposter[$i] = qq~$lastposter[$i]~;\n) if ($lastposter[$i] ne "");
    $lastposter[$i] =~ s/\\\~/~/isg;
    $lastposter[$i] =~ s/\\\$/\$/isg;
    $lastposter[$i] =~ s/\\\@/\@/isg;
}
for ($i=0;$i<=$#cforums;$i++) {
    $cforums[$i] =~ s/\\/\\\\/isg;
    $cforums[$i] =~ s/~/\\\~/isg;
    $cforums[$i] =~ s/\$/\\\$/isg;
    $cforums[$i] =~ s/\@/\\\@/isg;
    print FILE qq(\$forums[$i] = qq~$cforums[$i]~;\n) if ($cforums[$i] ne "");
    $cforums[$i] =~ s/\\\~/~/isg;
    $cforums[$i] =~ s/\\\$/\$/isg;
    $cforums[$i] =~ s/\\\@/\@/isg;
    $cforums[$i] =~ s/\\\\/\\/isg;
}
for ($i=0;$i<=$#modout;$i++) {
    $modout[$i] =~ s/~/\\\~/isg;
    $modout[$i] =~ s/\$/\\\$/isg;
    $modout[$i] =~ s/\@/\\\@/isg;
    print FILE qq(\$modout[$i] = qq~$modout[$i]~;\n) if ($modout[$i] ne "");
    $modout[$i] =~ s/\\\~/~/isg;
    $modout[$i] =~ s/\\\$/\$/isg;
    $modout[$i] =~ s/\\\@/\@/isg;
}
for ($i=0;$i<=$#cmodoutput;$i++) {
    $cmodoutput[$i] =~ s/~/\\\~/isg;
    $cmodoutput[$i] =~ s/\$/\\\$/isg;
    $cmodoutput[$i] =~ s/\@/\\\@/isg;
    print FILE qq(\$cmodoutput[$i] = qq~$cmodoutput[$i]~;\n) if ($cmodoutput[$i] ne "");
    $cmodoutput[$i] =~ s/\\\~/~/isg;
    $cmodoutput[$i] =~ s/\\\$/\$/isg;
    $cmodoutput[$i] =~ s/\\\@/\@/isg;
}
$todaypostlist =~ s/\\/\\\\/isg;
$todaypostlist =~ s/~/\\\~/isg;
$todaypostlist =~ s/\$/\\\$/isg;
$todaypostlist =~ s/\@/\\\@/isg;
$todaypostlist =~ s/\\\$/\$/isg;
print FILE qq(\$todaypostlist  = qq~$todaypostlist~;\n);
$todaypostlist =~ s/\$/\\\$/isg;
$todaypostlist =~ s/\\\~/~/isg;
$todaypostlist =~ s/\\\$/\$/isg;
$todaypostlist =~ s/\\\@/\@/isg;
$todaypostlist =~ s/\\\\/\\/isg;

$birthdayoutput =~ s/\\/\\\\/isg;
$birthdayoutput =~ s/~/\\\~/isg;
$birthdayoutput =~ s/\$/\\\$/isg;
$birthdayoutput =~ s/\@/\\\@/isg;
$birthdayoutput =~ s/\\\$/\$/isg;
print FILE qq(\$birthdayoutput = qq~$birthdayoutput~;\n);
$birthdayoutput =~ s/\$/\\\$/isg;
$birthdayoutput =~ s/\\\~/~/isg;
$birthdayoutput =~ s/\\\$/\$/isg;
$birthdayoutput =~ s/\\\@/\@/isg;
$birthdayoutput =~ s/\\\\/\\/isg;
print FILE "1;\n";
close(FILE);
$birthdayoutput =~ s/\$skin/$skin/isg;
$birthdayoutput =~ s/\$tablewidth/$tablewidth/isg;
$birthdayoutput =~ s/\$tablebordercolor/$tablebordercolor/isg;
$birthdayoutput =~ s/\$titlecolor/$titlecolor/isg;
$birthdayoutput =~ s/\$catbackpic/$catbackpic/isg;
$birthdayoutput =~ s/\$titlefontcolor/$titlefontcolor/isg;
$birthdayoutput =~ s/\$forumcolorone/$forumcolorone/isg;
$birthdayoutput =~ s/\$forumcolortwo/$forumcolortwo/isg;
$birthdayoutput =~ s/\$forumfontcolor/$forumfontcolor/isg;

$todaypostlist =~ s/\$titlecolor/$titlecolor/isg;
$todaypostlist =~ s/\$postfontcolortwo/$postfontcolortwo/isg;
$todaypostlist =~ s/\$fonthighlight/$fonthighlight/isg;
$todaypostlist =~ s/\$titlecolor/$titlecolor/isg;
$todaypostlist =~ s/\$postfontcolorone/$postfontcolorone/isg;

unlink("${lbdir}cache/forumcache-$skin.pl.lock");

sub birthday {
    $birthdayuser = "";
    $borncount = 0;
    my $filedate = "";
    my $nowtime = &shortdate($currenttime + $timeadd);
    ($nowy, $nowm, $nowd) = split(/\//, $nowtime);
    my $filetoopen = "${lbdir}data/birthdaytoday.cgi";
    if (-e $filetoopen) {
        open (BDILE, "$filetoopen");
        @birthdaytoday = <BDILE>;
        close (BDILE);
        chomp @birthdaytoday;
        $filedate=$birthdaytoday[0];
        chomp $filedate;
        $filedate =~ s/^#//isg;
    }
    if ($filedate ne $nowtime) {
    	require "dotodaybirthday.pl";
    }
    else {
    	$birthdayuser = $birthdaytoday[1];
    	$borncount = $birthdaytoday[2];
    }

}
1;
