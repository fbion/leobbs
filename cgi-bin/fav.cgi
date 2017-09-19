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
use File::Copy;
$loadcopymo = 1;
$LBCGI::POST_MAX=500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
use VISITFORUM qw(getlastvisit setlastvisit);
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/mpic.cgi";
require "code.cgi";
require "bbs.lib.pl";
require "rebuildlist.pl";

$|++;
$thisprog = "fav.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

#&ipbanned; #��ɱһЩ ip

opendir (DIRS, "$lbdir");
my @files = readdir(DIRS);
closedir (DIRS);
@files = grep(/^\w+?$/i, @files);
my @memfavdir = grep(/^memfav/i, @files);
$memfavdir = $memfavdir[0];

$inshow         = $query -> param('show');
$inshow         = &stripMETA("$inshow");
for ('forum','topic','membername','password','action','checked','member','mainopen','selectcate','newcate','selecttopic') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
$newcate =~ s/\`/\\\`/isg;
$newcate =~ s/\;/\\\;/isg;
$newcate =~ s/\\/\\\\/isg;
$newcate =~ s/\>/\\\>/isg;
$newcate =~ s/\</\\\</isg;
$newcate =~ s/\@/\\\@/isg;
$newcate =~ s/\#/\\\#/isg;
$newcate =~ s/\'/\\\'/isg;
$newcate =~ s/\"/\\\"/isg;
$newcate =~ s/\./\\\./isg;
$newcate =~ s/\$/\\\$/isg;
$newcate =~ s/\=/\\\=/isg;
$newcate =~ s/\//\\\//isg;
$newcate =~ s/system//isg;

$inforum       = $forum;
$intopic       = $topic;
$inmembername  = $membername;
$inpassword    = $password;
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$currenttime=time;
$maxthreads = 25 if ($maxthreads <=0);
$numberofpages = 25 if ($numberofpages <=0);
$maxtopics = 25  if ($maxtopics <=0);
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum) && ($inforum !~ /^[0-9]+$/));
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "")  { $catbackpic  = "background=$imagesurl/images/$skin/$catbackpic";  }

$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

if (!$inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (!$inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
$member        = $inmembername if($member eq "");
if ($inmembername eq "" || $inmembername eq "����" ) {
		&error("��ͨ����&������Ȩ���ʸ����ղؼУ�");
}
else {
    &getmember("$inmembername");
     if ($inpassword ne $password) {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("��ͨ����&�������û���������������µ�¼��");
     }
    &error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
    &getlastvisit;
}
$addtimes           = $timedifferencevalue*3600 + $timezone*3600;
$screenmode  = $query->cookie("screenmode");
$screenmode  = 8 if ($screenmode eq "");
    $infilemembername = $inmembername;
    $infilemembername =~ s/ /_/g;
    $infilemembername =~ tr/A-Z/a-z/;
    if (-e"${lbdir}$memfavdir/$infilemembername.cgi") {
    	mkdir ("${lbdir}$memfavdir/open", 0777) if (!(-e "${lbdir}$memfavdir/open"));
    	mkdir ("${lbdir}$memfavdir/close", 0777) if (!(-e "${lbdir}$memfavdir/close"));
        open (FAV, "${lbdir}$memfavdir/$infilemembername.cgi");
        @favtopic = <FAV>;
        close (FAV);
	@favtopic = &cleanslashes (@favtopic);#anthony
        open (FAV, ">${lbdir}$memfavdir/open/$infilemembername.cgi");
        print FAV "Ĭ��o\n";
        foreach (@favtopic) {
            chomp $_;
            print FAV "$_\n";
        }
        close (FAV);
        unlink ("${lbdir}$memfavdir/$infilemembername.cgi");
    }
	my %Mode = (
    'add'                 =>    \&add,
    'del'                 =>    \&del,
    'mov'                =>    \&mov,
    'top'                =>    \&top,
    'setting'             =>    \&setting,
    'show'                =>    \&list
    );
	if($Mode{$action}) {$Mode{$action}->();}
    else { &error("��ͨ����&������ȷ�ķ�ʽ���ʱ�����"); }
    &output("$boardname - �����ղ�",\$output);

sub add {
        $taction=($mainopen eq "up")?"����":"����";
   if (($intopic eq "")&&($inforum eq "")){&error("$taction�����ղ�&û��ָ�������ź���̳��ţ�");}
#    &getmember("$inmembername");

$testentry = $query->cookie("forumsallowed$inforum");

&getoneforum("$inforum");
if (($allowedentry{$inforum} eq "yes")||(($testentry eq $forumpass)&&($testentry ne ""))||($membercode eq "ad")||($inmembmod eq "yes")||($membercode eq 'smo')) { $allowed = "yes"; } else { $allowed  = "no"; }

if (($privateforum eq "yes" && $allowed ne "yes")) { &error("$taction�����ղ�&�Բ�����û��Ȩ���ղ�������ӣ�"); }
if (($startnewthreads eq "cert")&&(($membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo" && $membercode ne "amo" && $membercode !~ /^rz/)||($inmembername eq "����"))&&($userincert eq "no")) { &error("$taction�����ղ�&�Բ�����û��Ȩ���ղ�������ӣ�"); }

    &favmischeader("$taction�����ղ�");
    if ($checked eq "yes") {
    $file=(-e"${lbdir}$memfavdir/close/$infilemembername.cgi")?"${lbdir}$memfavdir/close/$infilemembername.cgi":"${lbdir}$memfavdir/open/$infilemembername.cgi";
		if (-e $file) {
        open (FAV, $file);
        @favtopic = <FAV>;
        close (FAV);
	@favtopic = &cleanslashes (@favtopic);#anthony
        chomp @favtopic;
        $catelist=shift(@favtopic);
        chomp $catelist;
        if($mainopen eq "up"){
        $i=0;
        foreach $line (@favtopic) {
	    chomp $line;
	    ($ttopic,$tforum,undef)=split(/\t/,$line);
        	if (($ttopic eq $intopic)&&($tforum eq $inforum)) {
        	my$oldtopic=splice(@favtopic,$i,1);
        ($topic,$forum,$status,$cate,$ftime)=split(/\t/,$oldtopic);
        last;
        	}
        $i++;
        }
        unshift(@favtopic,"$topic\t$forum\tnormal\t$cate\t$ftime\t");
        open (FAV, ">$file");
        print FAV "$catelist\n";
        foreach $line (@favtopic) {
	    chomp $line;
	    ($topic,$forum,$status,$cate,$ftime)=split(/\t/,$line);
	    my $rr = &readthreadpl($forum,$topic);
	    next if($rr eq "");
        print FAV "$topic\t$forum\t$status\t$cate\t$ftime\t\n";
        }
        close (FAV);
        }else{
        @catelist=split(/\t/,$catelist);
	foreach(@catelist){s/^����������//o;}
        $favdescript=pop(@catelist) if($catelist[$#catelist] =~/^\>\>/);
        chomp @catelist;
        if ($newcate eq "" && $catelist[$selectcate] eq "") { &error("��������ղ�&����ѡ��һ������Ŀ¼���½�һ��Ŀ¼��");}
        	if($newcate ne ""){
    	&error("��������ղ�&��Ŀ¼���Ʋ��ܶ�� 30 ��������(15 ��������)��") if(length($newcate) > 30);
    	foreach(@catelist){
    	$name=$_;
    	$name=~s/[oc]$//;
    	&error("��������ղ�&��Ŀ¼�Ѵ��ڣ�") if($newcate eq $name);
    	}
        $incate=$newcate;
        push(@catelist,$newcate."o");
        $catelistno=@catelist;
        &error("��������ղ�&���ֻ�ܹ��� 10 ��Ŀ¼��") if($catelistno > 10);
	@catelist = map('����������'.$_, @catelist);
        $catelist=join("\t",@catelist);
        $selectcate=$#catelist;
        	}else{
        $catelist=join("\t",@catelist);
        $incate=$catelist[$selectcate];
    	$incate=~s/[oc]$//;
        	}
        open (FAV, ">$file");
        print FAV "$catelist\t$favdescript\n";
        print FAV "$intopic\t$inforum\tnormal\t$incate\t$currenttime\t\n";
        foreach $line (@favtopic) {
	    chomp $line;
	    ($topic,$forum,$status,$cate,$ftime)=split(/\t/,$line);
	    my $rr = &readthreadpl($forum,$topic);
	    next if($rr eq "");
        	unless (($topic eq $intopic)&&($forum eq $inforum)) {
        print FAV "$topic\t$forum\t$status\t$cate\t$ftime\t\n";
        	}
        }
        close (FAV);
        }
		}else {
			if ($newcate eq "") { &error("��������ղ�&�����½�һ��Ŀ¼��");}
			$selectcate=0;
	        open (ENT, ">$file");
	        print ENT "����������${newcate}o\t\n";
	        print ENT "$intopic\t$inforum\tnormal\t$newcate\t$currenttime\t\n";
	        close (ENT);
		}
		if($mainopen ne "up"){
			$returntoforum=qq(<li><a href="topic.cgi?forum=$inforum&topic=$intopic">���ظ�����</a><li><a href="forums.cgi?forum=$inforum">������̳</a>);
		}

            $output .= qq~
            <SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 width=100%>
            <tr>
            <td bgcolor=$catback $catbackpic align=center><font color=$fontcolormisc><b>$taction�����ղسɹ�</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            ���������
            <ul>
            <li><a href="fav.cgi?action=show&selectcate=$selectcate">���ظ����ղؼ�</a>$returntoforum
            <li><a href="leobbs.cgi">������̳��ҳ</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <SCRIPT>valignend()</SCRIPT>
            ~;

    } # end if clear to edit
    else {
    $file=(-e"${lbdir}$memfavdir/close/$infilemembername.cgi")?"${lbdir}$memfavdir/close/$infilemembername.cgi":"${lbdir}$memfavdir/open/$infilemembername.cgi";
		if (-e $file) {
        open (FAV, $file);
        @favtopic = <FAV>;
        close (FAV);
	@favtopic = &cleanslashes (@favtopic);#anthony
        $catelist=shift(@favtopic);
        foreach $line(@favtopic){
			($topic,$forum,$status,$cate,$ftime)=split(/\t/,$line);
			&error("�����ղؼ�&�������Ѽ����ղؼ��е�Ŀ¼ - $cate��") if($topic eq $intopic && $forum eq $inforum);
        }
        @catelist=split(/\t/,$catelist);
	foreach(@catelist){s/^����������//o;}
        $favdescript=pop(@catelist) if($catelist[$#catelist] =~/^\>\>/);
        $cateno=@catelist;
			if($cateno > 0){
			$cate="";$i=0;
				foreach(@catelist){
					$_=~s/[oc]$//;
					chomp $_;
					next if($_ eq "");
					$cate.=qq(<option value="$i">$_</option>);
					$i++;
				}
        $cateselect=qq(<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>ѡ����뵽��һ��Ŀ¼</font></td><td bgcolor=$miscbackone><select name="selectcate" style="width:30%">$cate</select></td></tr>);
			}
		}
            $inmembername =~ s/\_/ /g;
            $output .= qq~
            <SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 width=100%>
            <tr>
            <td bgcolor=$catback $catbackpic colspan=2 align=center>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="add">
            <input type=hidden name="checked" value="yes">
            <input type=hidden name="forum" value="$inforum">
            <input type=hidden name="topic" value="$intopic">
            <font color=$fontcolormisc><b>�����������û����������������ղ� </b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>$cateselect
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>����һ����Ŀ¼</font></td>
            <td bgcolor=$miscbackone><input type=text name="newcate" value="" maxlength="30"></td></tr>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="ȷ ��"></td></form></tr></table></td></tr></table>
            </table></td></tr></table>
            <SCRIPT>valignend()</SCRIPT>
            ~;

    }
} # end
sub mov {
	if($selecttopic ne ""){
		my $selecttopiccheck=$selecttopic;
		$selecttopiccheck=~s/[0-9\_\|]//g;
		if ($selecttopiccheck ne ""){&error("�ƶ������ղ�&û��ָ���κ����⣡");}
		@selecttopic=split(/\_/,$selecttopic);
		$topictomove=0;
	}else{
		if (($intopic eq "")&&($inforum eq "")){&error("�ƶ������ղ�&û��ָ�������ź���̳��ţ�");}
	}
#    &getmember("$inmembername");

    &favmischeader("�ƶ������ղ�");
    if ($checked eq "yes") {
    $file=(-e"${lbdir}$memfavdir/close/$infilemembername.cgi")?"${lbdir}$memfavdir/close/$infilemembername.cgi":"${lbdir}$memfavdir/open/$infilemembername.cgi";
		if (-e $file) {
        open (FAV, $file);
        @favtopic = <FAV>;
        close (FAV);
	@favtopic = &cleanslashes (@favtopic);#anthony
        chomp @favtopic;
        $catelist=shift(@favtopic);
        chomp $catelist;
        @catelist=split(/\t/,$catelist);
	foreach(@catelist){s/^����������//o;}
        $favdescript=pop(@catelist) if($catelist[$#catelist] =~/^\>\>/);
        chomp @catelist;
        if ($newcate eq "" && $catelist[$selectcate] eq "") { &error("�ƶ������ղ�&����ѡ��һ������Ŀ¼���½�һ��Ŀ¼��");}
        	if($newcate ne ""){
    	&error("�ƶ������ղ�&��Ŀ¼���Ʋ��ܶ��� 30 ����(�� 15 ��������)��") if(length($newcate) > 30);
    	foreach(@catelist){
    	$name=$_;
    	$name=~s/[oc]$//;
    	&error("�ƶ������ղ�&��Ŀ¼�Ѵ��ڣ�") if($newcate eq $name);
    	}
        $incate=$newcate;
        push(@catelist,$newcate."o");
	@catelist=map('����������'.$_, @catelist);
        $catelist=join("\t",@catelist);
        $catelistno=@catelist;
        &error("�ƶ������ղ�&���ֻ�ܹ��� 10 ��Ŀ¼��") if($catelistno > 10);
        $selectcate=$#catelist;
        	}else{
        $catelist=join("\t",@catelist);
        $incate=$catelist[$selectcate];
    	$incate=~s/[oc]$//;
        	}
        open (FAV, ">$file");
        print FAV "$catelist\t$favdescript\n";
        foreach $line (@favtopic) {
	    chomp $line;
	    ($topic,$forum,$status,$cate,$ftime)=split(/\t/,$line);
	    my $rr = &readthreadpl($forum,$topic);
	    next if($rr eq "");
	    	if($selecttopic ne ""){
	    		$check="no";
	    		foreach(@selecttopic){
	    			next if($_ eq "");
	    			my ($inforum,$intopic)=split(/\|/,$_);
	    			next if($inforum eq "" || $inforum =~/[^0-9]/ || $intopic eq "" || $intopic =~/[^0-9]/);
	    			if(($topic eq $intopic)&&($forum eq $inforum)){
	    		$check="yes";
	    		last;
	    			}
	    		}
        		if($check eq "yes") {
		$topictomove++;
        print FAV "$topic\t$forum\tnormal\t$incate\t$ftime\t\n";
        		}else{
        print FAV "$topic\t$forum\t$status\t$cate\t$ftime\t\n";
        		}
	    	}else{
        		if(($topic eq $intopic)&&($forum eq $inforum)) {
		$topictomove=1;
        print FAV "$topic\t$forum\tnormal\t$incate\t$ftime\t\n";
        		}else{
        print FAV "$topic\t$forum\t$status\t$cate\t$ftime\t\n";
        		}
	    	}
        }
        close (FAV);
		}else{
			&error("�ƶ��ղؼ�&�����ղؼ���û������ɹ��ƶ���")
		}

            $output .= qq~
            <SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 width=100%>
            <tr>
            <td bgcolor=$catback $catbackpic align=center><font color=$fontcolormisc><b>�ɹ��ƶ� <b><font color="$fonthighlight">$topictomove</font></b> ƪ�����ղ�</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            ���������
            <ul>
            <li><a href="fav.cgi?action=show&selectcate=$selectcate">���ظ����ղ� [��Ŀ¼]</a>
            <li><a href="fav.cgi?action=show&selectcate=$mainopen">���ظ����ղ� [��Ŀ¼]</a>
            <li><a href="leobbs.cgi">������̳��ҳ</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <SCRIPT>valignend()</SCRIPT>
            ~;

    } # end if clear to edit
    else {
    $file=(-e"${lbdir}$memfavdir/close/$infilemembername.cgi")?"${lbdir}$memfavdir/close/$infilemembername.cgi":"${lbdir}$memfavdir/open/$infilemembername.cgi";
		if (-e $file) {
        open (FAV, $file);
        @favtopic = <FAV>;
        close (FAV);
	@favtopic = &cleanslashes (@favtopic);#anthony
        $catelist=shift(@favtopic);
        @catelist=split(/\t/,$catelist);
	foreach(@catelist){s/^����������//o;}
        $favdescript=pop(@catelist) if($catelist[$#catelist] =~/^\>\>/);
        $cateno=@catelist;
			if($cateno > 0){
			$cate="";$i=0;
				foreach(@catelist){
					$_=~s/[oc]$//;
					chomp $_;
					next if($_ eq "");
					$cate.=qq(<option value="$i">$_</option>);
					$i++;
				}
        $cateselect=qq(<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>ѡ���ƶ�����һ��Ŀ¼</font></td><td bgcolor=$miscbackone><select name="selectcate" style="width:30%">$cate</select></td></tr>);
			}
		}
            $inmembername =~ s/\_/ /g;
            $output .= qq~
            <SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 width=100%>
            <tr>
            <td bgcolor=$catback $catbackpic colspan=2 align=center>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="mov">
            <input type=hidden name="checked" value="yes">
            <input type=hidden name="forum" value="$inforum">
            <input type=hidden name="topic" value="$intopic">
            <input type=hidden name="mainopen" value="$selectcate">
            <input type=hidden name="selecttopic" value="$selecttopic">
            <font color=$fontcolormisc><b>�����������û����������ƶ������ղ� </b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>$cateselect
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>�ƶ���һ����Ŀ¼</font></td>
            <td bgcolor=$miscbackone><input type=text name="newcate" value="" maxlength="30"></td></tr>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="ȷ ��"></td></form></tr></table></td></tr></table>
            </table></td></tr></table>
            <SCRIPT>valignend()</SCRIPT>
            ~;
    }
} # end
sub top {
   if (($intopic eq "")&&($inforum eq "")){&error("�����ղ��ö�&û��ָ�������ź���̳���");}
#    &getmember("$inmembername");

    &favmischeader("�����ղ��ö�");
    if ($checked eq "yes") {
    $file=(-e"${lbdir}$memfavdir/close/$infilemembername.cgi")?"${lbdir}$memfavdir/close/$infilemembername.cgi":"${lbdir}$memfavdir/open/$infilemembername.cgi";
		if (-e $file) {
        open (FAV, $file);
        @favtopic = <FAV>;
        close (FAV);
	@favtopic = &cleanslashes (@favtopic);#anthony
        chomp @favtopic;
        $catelist=shift(@favtopic);
        chomp $catelist;
        open (FAV, ">$file");
        print FAV "$catelist\n";
        foreach $line (@favtopic) {
	    chomp $line;
	    ($topic,$forum,$status,$cate,$ftime)=split(/\t/,$line);
	    my $rr = &readthreadpl($forum,$topic);
	    next if($rr eq "");
        	if(($topic eq $intopic)&&($forum eq $inforum)) {
        		if($status ne "top"){
        print FAV "$topic\t$forum\ttop\t$cate\t$ftime\t\n";
        $topaction="�ö�";
        		}else{
        print FAV "$topic\t$forum\tnormal\t$cate\t$ftime\t\n";
        $topaction="ȡ���ö�";
        		}
        	}else{
        print FAV "$topic\t$forum\t$status\t$cate\t$ftime\t\n";
        	}
        }
        close (FAV);
		}else{
			&error("�����ղ��ö�&�����ղؼ���û������ɹ��ö���")
		}

            $output .= qq~
            <SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 width=100%>
            <tr>
            <td bgcolor=$catback $catbackpic align=center><font color=$fontcolormisc><b>�����ղ�$topaction�ɹ�</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            ���������
            <ul>
            <li><a href="fav.cgi?action=show&selectcate=$mainopen">���ظ����ղ�</a>
            <li><a href="leobbs.cgi">������̳��ҳ</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <SCRIPT>valignend()</SCRIPT>
            ~;

    } # end if clear to edit
    else {
            $inmembername =~ s/\_/ /g;
            $output .= qq~
            <SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 width=100%>
            <tr>
            <td bgcolor=$catback $catbackpic colspan=2 align=center>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="top">
            <input type=hidden name="checked" value="yes">
            <input type=hidden name="forum" value="$inforum">
            <input type=hidden name="topic" value="$intopic">
            <input type=hidden name="mainopen" value="$selectcate">
            <font color=$fontcolormisc><b>�����������û����������ö������ղ� </b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="ȷ ��"></td></form></tr></table></td></tr></table>
            </table></td></tr></table>
            <SCRIPT>valignend()</SCRIPT>
            ~;
    }
} # end
sub del {
	if($selecttopic ne ""){
		my $selecttopiccheck=$selecttopic;
		$selecttopiccheck=~s/[0-9\_\|]//g;
		if ($selecttopiccheck ne ""){&error("ɾ�������ղ�&û��ָ���κ����⣡");}
		@selecttopic=split(/\_/,$selecttopic);
		$topictodel=0;
	}else{
		if (($intopic eq "")&&($inforum eq "")){&error("ɾ�������ղ�&û��ָ�������ź���̳��ţ�");}
	}
#        &getmember("$inmembername");

    &favmischeader("ɾ�������ղ�");

    if ($checked eq "yes") {
    $file=(-e"${lbdir}$memfavdir/close/$infilemembername.cgi")?"${lbdir}$memfavdir/close/$infilemembername.cgi":"${lbdir}$memfavdir/open/$infilemembername.cgi";
		if (-e $file) {
        open (FAV, $file);
        @favtopic = <FAV>;
        close (FAV);
	@favtopic = &cleanslashes (@favtopic);#anthony
        chomp @favtopic;
        $catelist=shift(@favtopic);
        chomp $catelist;
        open (FAV, ">$file");
        print FAV "$catelist\n";
        foreach $line (@favtopic) {
	    chomp $line;
	    ($topic,$forum,$status,$cate,$ftime)=split(/\t/,$line);
	    my $rr = &readthreadpl($forum,$topic);
	    next if($rr eq "");
	    	if($selecttopic ne ""){
	    		$check="no";
	    		foreach(@selecttopic){
	    			next if($_ eq "");
	    			my ($inforum,$intopic)=split(/\|/,$_);
	    			next if($inforum eq "" || $inforum =~/[^0-9]/ || $intopic eq "" || $intopic =~/[^0-9]/);
	    			if(($topic eq $intopic)&&($forum eq $inforum)){
	    		$check="yes";
	    		last;
	    			}
	    		}
        		if($check eq "yes") {
		$topictodel++;
        		}else{
        print FAV "$topic\t$forum\t$status\t$cate\t$ftime\t\n";
        		}
	    	}else{
        		if(($topic eq $intopic)&&($forum eq $inforum)) {
		$topictodel=1;
        		}else{
        print FAV "$topic\t$forum\t$status\t$cate\t$ftime\t\n";
        		}
	    	}
        }
        close (FAV);
		}else {
			&error("ɾ���ղؼ�&�����ղؼ���û������ɹ�ɾ����")
		}

            $output .= qq~
            <SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 width=100%>
            <tr>
            <td bgcolor=$catback $catbackpic align=center><font color=$fontcolormisc><b>�ɹ�ɾ�� <b><font color="$fonthighlight">$topictodel</font></b> ƪ�����ղ�</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            ���������
            <ul>
            <li><a href="fav.cgi?action=show&selectcate=$mainopen">���ظ����ղ�</a>
            <li><a href="leobbs.cgi">������̳��ҳ</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <SCRIPT>valignend()</SCRIPT>
            ~;

    } # end if clear to edit
    else {
            $inmembername =~ s/\_/ /g;
            $output .= qq~
            <SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 width=100%>
            <tr>
            <td bgcolor=$catback $catbackpic colspan=2 align=center>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="del">
            <input type=hidden name="checked" value="yes">
            <input type=hidden name="forum" value="$inforum">
            <input type=hidden name="topic" value="$intopic">
            <input type=hidden name="mainopen" value="$selectcate">
            <input type=hidden name="selecttopic" value="$selecttopic">
            <font color=$fontcolormisc><b>�����������û���������ɾ�������ղ�</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="ȷ ��"></td></form></tr></table></td></tr></table>
            </table></td></tr></table>
            <SCRIPT>valignend()</SCRIPT>
            ~;
    }
} # end
sub list{
	$filemembername =$member;
    $filemembername =~ s/ /_/g;
    $filemembername =~ tr/A-Z/a-z/;
    &error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($member =~  m/\//)||($member =~ m/\\/)||($member =~ m/\.\./));

    if ($member eq ""){&error("�鿴�����ղ�&û��ָ����Ա��");}
    my $namenumber = &getnamenumber($filemembername);
    &checkmemfile($filemembername,$namenumber);
    if ((!(-e "${lbdir}$memdir/$namenumber/$filemembername.cgi"))&&(!(-e "${lbdir}$memdir/old/$filemembername.cgi"))) {&error("�鿴�����ղ�&û�иû�Ա��");}
#    &getmember("$inmembername");

    $favfile=(-e"${lbdir}$memfavdir/close/$filemembername.cgi")?"${lbdir}$memfavdir/close/$filemembername.cgi":"${lbdir}$memfavdir/open/$filemembername.cgi";
    if($filemembername eq $infilemembername){
    $cleartoedit="yes";$indexname="�����ղؼ�";
    }else{
    	if ($favfile eq "${lbdir}$memfavdir/close/$filemembername.cgi"){&error("�鿴�����ղ�&�ø����ղ��趨�����У�ֻ�������˿��Կ���") if($membercode ne "ad");}
    	elsif (!(-e $favfile)){&error("�鿴�����ղ�&�û�Աû�и����ղأ�");}
    $indexname=" $member ���ղؼ�";$cleartoedit="no";
    }


my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
if (!(-e "$filetoopens.lck")) {
&whosonline("$inmembername\t�����ղ�\tnone\t�鿴$indexname\t");
}
    $topcount = 0;
    $selectcate=0 if(!$selectcate);
    if (-e $favfile) {
    	&winlock($favfile) if ($OS_USED eq "Nt");
        open(FILE, "$favfile");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        @allfavtopic = <FILE>;
        close(FILE);
	@allfavtopic = &cleanslashes (@allfavtopic);#anthony
        &winunlock($favfile) if ($OS_USED eq "Nt");
        chomp @allfavtopic;
        $catelist=shift(@allfavtopic);
        chomp $catelist;
        @catelist=split(/\t/,$catelist);
	foreach(@catelist){s/^����������//o;}
        $favdescript=pop(@catelist) if($catelist[$#catelist] =~/^\>\>/isg);
        @catelist=grep(/o$/,@catelist) if($cleartoedit eq "no" && $membercode ne "ad");
        chomp @catelist;
        %catetopicc=();$catelist[$selectcate]=~s/[oc]$//;
        @favtopic=();@ontop=();
        foreach(@allfavtopic){
        	(undef,undef,my $status,my $cate,undef)=split(/\t/,$_);
        $catetopicc{$cate}=0 if(!$catetopicc{$cate});
        $catetopicc{$cate}++;
        	if($status ne "top"){
        push(@favtopic,$_) if($cate eq $catelist[$selectcate]);
        	}else{
        push(@ontop,$_) if($cate eq $catelist[$selectcate]);
        	}
        }
    }else{ undef @allfavtopic; }
    $cateoption="";%cates=();
    $i=0;
    foreach $name(@catelist){
    	$name=~s/[oc]$//;
    	next if($name eq "");
    $catetopicc{$name}=0 if(!$catetopicc{$name});
    $cateoption.=qq(<option value="$i">$name ($catetopicc{$name} ƪ����)</option>);
    $i++;
    }
    $ontopcount = @ontop;
    $topcount = @favtopic;
    $topcount +=$ontopcount;
    if($cateoption eq ""){
    $cateoption=qq(<img src=$imagesurl/images/fav.gif width=16> <a href="$thisprog?action=setting"><b>������Ŀ¼</b></a>);
    }else{
    $cateoption=qq(<select name="selectcate" onchange="C1(this.value)" style="width:100%">$cateoption</select>)
    }
    $cateoption=~s/option value="$selectcate"/option value="$selectcate" selected>>/;
#&title;
	if($cleartoedit eq "yes"){
$multimanagejs   = qq~
function CheckAll(form){for (var i=0;i<form.elements.length;i++){var e = form.elements[i];if (e.name == 'selectt'){e.checked = true;}}}
function FanAll(form){for (var i=0;i<form.elements.length;i++){var e = form.elements[i];if (e.name == 'selectt'){if (e.checked == true){e.checked = false;}else{e.checked = true;}}}}
function SetAction(form,A){form.action.value=A;}
function Check(form){form.selecttopic.value="";j=0;for (var i=0;i<form.elements.length;i++){var e = form.elements[i];if (e.name == 'selectt'){if (e.checked == true){j++;form.selecttopic.value+=e.value+"_";}}}if(j > 0){return true;}else{return false;}}
~;
$multimanageform   = qq~<form action="$thisprog" name=Admin method=post onSubmit="return Check(this)"><input type=hidden name="selectcate" value="$selectcate"><input type=hidden name="selecttopic" value=""><input type=hidden name="action" value="del">~;
	}
&favmischeader("�鿴�����ղ�");
$output .= qq~
<style>
TABLE {BORDER-TOP: 0px; BORDER-LEFT: 0px; BORDER-BOTTOM: 1px; }
TD {BORDER-RIGHT: 0px; BORDER-TOP: 0px; color: $fontcolormisc; }
.ha {color: $fonthighlight; font: bold;}
.hb {color: $menufontcolor; font: bold;}
.dp {padding: 4px 0px;}
</style>
<script language="javascript">
function C1(id) {if(id!="")self.location.href="$thisprog?action=show&member=$member&selectcate="+id;}
$multimanagejs
</script>~;
$favdescript=~s/^>>//;
&lbcode(\$favdescript);
$output.=qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=6 cellspacing=0 width=$tablewidth height=24 align=center style="border:1 solid $tablebordercolor"><tr><td bgcolor=$catback $catbackpic height=24 align=left><img src=$imagesurl/images/cat.gif border=0 width=9 height=9> <font color=$catfontcolor><b>�ղؼн���</b></font></td></tr></table>
<table cellpadding=6 cellspacing=0 width=$tablewidth height=24 align=center style="border:1 solid $tablebordercolor;border-top-width:0px">
<tr><td align=center width=26 bgcolor=$forumcolorone style="border-right:1 solid $tablebordercolor;"><img src=$imagesurl/images/fav.gif width=16 border=0></td>
<td width=* bgColor=$forumcolortwo>$favdescript</td>
</table><br>
~ if($favdescript ne "");
$output.=qq~
$multimanageform
<SCRIPT>valigntop()</SCRIPT>
<table cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td height=1></td></tr></table><center>
<table cellpadding=0 cellspacing=0 width=$tablewidth height=24 bordercolor=$tablebordercolor border=1>
<tr><td bgcolor=$titlecolor width=32 align=center $catbackpic><font color=$titlefontcolor><b>״̬</b></td>
<td bgcolor=$titlecolor width=* align=center $catbackpic><font color=$titlefontcolor><b>������</b> (�������Ϊ���ŷ�ʽ�Ķ�)</td>
<td bgcolor=$titlecolor align=center width=80 $catbackpic><font color=$titlefontcolor><b>�� ��</b></td>
<td bgcolor=$titlecolor align=center width=32 $catbackpic><font color=$titlefontcolor><b>�ظ�</b></td>
<td bgcolor=$titlecolor align=center width=32 $catbackpic><font color=$titlefontcolor><b>���</b></td>
<td bgcolor=$titlecolor width=195 align=center $catbackpic><font color=$titlefontcolor><b>�� ������ �� | ���ظ���</b></td>
<td width=37 bgcolor=$titlecolor align=center $catbackpic><font color=$titlefontcolor><b>ѡ</b></font></td></tr></table>

~;
$numberofpages = $topcount / $maxthreads;

if ($topcount > $maxthreads) {
    $showmore = "yes";
    if ($inshow eq "" || $inshow < 0) { $inshow = 0; }
    if ($inshow > 0) { $startarray = $inshow; } else { $startarray = 0; }
    $endarray = $inshow + $maxthreads - 1;
    if ($endarray < ($topcount - 1)) { $more = "yes"; }
        elsif (($endarray > ($maxthreads - 1)) && ($more ne "yes")) { $endarray = $topcount -1; }
}
else {
    $showmore = "no";
    $startarray = 0;
    $topicpages = qq~���ղؼ�ֻ��һҳ~;
    $endarray = $topcount -1;
}

if ($showmore eq "yes") {
	($integer,$decimal) = split(/\./,$numberofpages);
	if ($decimal > 0) { $numberofpages = $integer + 1; }
	$mypages=$numberofpages;
	$count     = (($inshow/$maxthreads)+1);
	$countstart= $count-4;
	$countend  = $count+4;
    if($countstart <= 0){
    $addendcount=0-$countstart;
    $countstart=1;
    $countend+=$addendcount;
    $countend++;
    }
    if($countend >= $mypages){
    $addstartcount=$countend-$mypages;
    $countend=$mypages;
    $countstart-=$addstartcount;
    }
    $checkpage=1;
    for ($page=$countstart;$page<=$countend;$page++){
    last if($checkpage > 9);
    if ($page<=$mypages && $page > 0){
    $pagestart=($page-1)*$maxthreads;
    if ($page ne $count) {$pages .= qq~<a href=$thisprog?action=show&member=$member&show=$pagestart&selectcate=$selectcate class=hb>$page</a> ~; }
	else{$pages .= qq~<font color=$fonthighlight><B>$page</B></font> ~;}
    }
    $checkpage++;
    }
    if ($count > "0") { 
    $beginpage=qq~<a href="$thisprog?action=show&member=$member&show=0&selectcate=$selectcate" title="�� ҳ" ><font face=webdings >9</font></a>~; 
    $pageup=$count-1;
    $pageup1=($pageup-1)*$maxthreads;
	$showup = qq~<a href="$thisprog?action=show&member=$member&show=$pageup1&selectcate=$selectcate" title="��$pageupҳ" ><font face=webdings >7</font></a>~;
    } else {
    $beginpage=qq~<font color=$fonthighlight><font face=webdings >9</font></font>~;
	$showup = qq~<font color=$fonthighlight><font face=webdings >7</font></font>~;
    }
    $showend=($mypages-1)*$maxthreads;
    if ($count ne $mypages) { 
    $endpage=qq~<a href="$thisprog?action=show&member=$member&show=$showend&selectcate=$selectcate" title="β ҳ" ><font face=webdings >:</font></a>~; 
    $pagedown=$count+1;
    $pagedown1=($count+1)*$maxthreads;
    $showdown = qq~<a href="$thisprog?action=show&member=$member&show=$pagedown1&selectcate=$selectcate" title="��$pagedownҳ" ><font face=webdings >8</font></a> ~; 
    } else { 
    $endpage=qq~<font color=$fonthighlight><font face=webdings >:</font></font>~;
    $showdown = qq~<font color=$fonthighlight><font face=webdings >8</font></font>~;
    }
    $topicpages = qq~<font color=$menufontcolor><b>���ղؼй� <font color=$fonthighlight>$mypages</font> ҳ</b> $beginpage $showup [ $pages ] $showdown $endpage~;
}
$threads=0;
$posts=0;
$oldforumcolorone=$forumcolorone;
$oldforumcolortwo=$forumcolortwo;
$ontopcount=@ontop;
undef @toptopic;
    if ($topcount > 0) {
    	if($startarray eq 0 && $ontopcount > 0){
    	$ontopcount=0;
        foreach (@ontop) {
	    chomp $_;
      	next if ($_ eq "");
	    my ($tempintopic,$tempinforum,$tempstatus,$tempcate,$temptime) = split (/\t/,$_);
	    next if($tempstatus ne "top");
	    next if($catelist[$selectcate] ne $tempcate);
	    my $rr = &readthreadpl($tempinforum,$tempintopic);
	    if ($rr ne "") {
	        (my $lastpostdate, my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $posticon, my $posttemp) = split (/\t/,$rr);
	        $threads++;
	        $posts+=$threadposts;
	        push (@toptopic, "$topicid\t$tempinforum\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$posticon\t$posttemp\t$temptime");
	    $ontopcount++;
	    }
        }
    	}
    	$i=0;
        foreach (@favtopic[$startarray .. $endarray]) {
        last if($i > $maxthreads);
	    chomp $_;
      	next if ($_ eq "");
	    my ($tempintopic,$tempinforum,$tempstatus,$tempcate,$temptime) = split (/\t/,$_);
	    next if($tempstatus eq "top");
	    next if($catelist[$selectcate] ne $tempcate);
	    my $rr = &readthreadpl($tempinforum,$tempintopic);
	    if ($rr ne "") {
	        (my $lastpostdate, my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $posticon, my $posttemp) = split (/\t/,$rr);
	        $threads++;
	        $posts+=$threadposts;
	        push (@toptopic, "$topicid\t$tempinforum\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$posticon\t$posttemp\t$temptime");
	       $i++;
	    }
        }
    }
$topiccount = 0;
foreach $topic (@toptopic) {
    $pagestoshow = undef;
    $threadpages = undef;
    chomp $topic;
    ($topicid, $forumid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $posticon, $posttemp, $favtime) = split(/\t/,$topic);
    $forumlastvisit = $lastvisitinfo{$forumid};
    if (($posticon eq "")||($posticon =~/<br>/i)) {
        $posticon = int(myrand(23));
    	$posticon = "0$posticon" if ($posticon<10);
	$posticon = qq~<img src=$imagesurl/posticons/$posticon.gif $defaultsmilewidth $defaultsmileheight border=0 align=absmiddle>~;
    }
    else{
        $posticon = qq~<img src=$imagesurl/posticons/$posticon $defaultsmilewidth $defaultsmileheight border=0 align=absmiddle>~;
    }

    $topcount = $threadposts + 1;
    $numberofpages = $topcount / $maxtopics;
    $counter = 0;
    $hasshow=0;
    if ($topcount > $maxtopics) {
        if ($numberofpages>int($numberofpages)){ $numberofpages = int($numberofpages)+1 ;}
	$pagestart = 0;
	while ($numberofpages > $counter) {
	    $counter++;
#	    if (($numberofpages <= 11)||($counter<5)||($counter>$numberofpages-4)){
		if(($counter < 3)||($counter>$numberofpages-2)){
		$threadpages .= qq~<a href=topic.cgi?forum=$forumid&topic=$topicid&start=$pagestart&show=$inshow class=ha target="_self">$counter</a> ~;
		}elsif ($hasshow eq 0) {
		$threadpages .="\.\.\.";
		$hasshow = 1;
		}
#		$threadpages .= qq~<option value="$pagestart" class=ha >$counter</option> ~;
#	    }
#	    elsif ($hasshow eq 0) {
#		$threadpages .="\. \. \. ";
#		$hasshow = 1;
#	    }
	    $pagestart = $pagestart + $maxtopics;
	}
	$pagestart   = $pagestart - $maxtopics;
        $gotoendpost = "$pagestart";
        $pagestoshow = qq~<font color=$forumfontcolor>[�� $threadpages ҳ]</font>~;
    }
    else {
        $gotoendpost = "0";
    }
    $counter=0;

    if (!$forumlastvisit) { $forumlastvisit = "0"; }

    if ((lc($inmembername) eq lc($startedby))&&($nodispown eq "yes")){ $mypost="<img src=$imagesurl/images/$skin/$mypost_blogo title=�ҷ��������> "}else {$mypost=""};

    $topicicon = "<img src=$imagesurl/images/$skin/topicnonew.gif width=14 border=0>";

    if (($threadposts >= $hottopicmark) && ($forumlastvisit < $lastpostdate) && ($inmembername ne "����")) { $topicicon = "<img src=$imagesurl/images/$skin/topichot3.gif width=14 border=0>"; }
    elsif (($threadposts >= $hottopicmark) && ($forumlastvisit > $lastpostdate) && ($inmembername ne "����")) { $topicicon = "<img src=$imagesurl/images/$skin/topichotnonew.gif width=14 border=0>"; }
    elsif (($threadposts <  $hottopicmark) && ($forumlastvisit < $lastpostdate) && ($inmembername ne "����")) { $topicicon = "<img src=$imagesurl/images/$skin/topicnew3.gif width=14 border=0>"; }
    elsif (($threadposts <  $hottopicmark) && ($forumlastvisit > $lastpostdate) && ($inmembername ne "����")) { $topicicon = "<img src=$imagesurl/images/$skin/topicnonew.gif width=14 border=0>"; }
		$forumcolorone=$forumcolortwo=$miscbacktwo if(($lastpostdate > $forumlastvisit) && ($inmembername ne "����"));

    $threadstate = "poll" if (($posticon =~/<br>/i)&&($threadstate eq ""));
    if (($threadstate eq "poll")||($threadstate eq "pollclosed")) {
       	$size = 0;
	if (open(FILE, "${lbdir}forum$forumid/$topicid.poll.cgi")) {
	    my @allpoll = <FILE>;
            close(FILE);
	    $size = @allpoll;
        }
    }
    if ($threadstate eq "closed") { $topicicon = "<img src=$imagesurl/images/$skin/topiclocked0.gif width=14 border=0>"; }
    elsif ($threadstate eq "poll") {
        if ($size >= $hotpollmark) { $topicicon = "<img src=$imagesurl/images/$skin/closedbhot.gif width=13 border=0>"; }
	                      else { $topicicon = "<img src=$imagesurl/images/$skin/closedb.gif width=13 border=0>"; }
    }
    elsif ($threadstate eq "pollclosed") { $topicicon = "<img src=$imagesurl/images/$skin/closedb1.gif width=13 border=0>"; }

	    if ($lastpostdate ne "") {
		$lastpostdate = $lastpostdate + $addtimes;
		$longdate = &dateformatshort("$lastpostdate");
		$lastpostdate = qq~<font color=$fontcolormisc>$longdate</font>~;
	    }
	    else {
		$lastpostdate = qq~<font color=$fontcolormisc>û��~;
		$lastpoststamp = "";
	    }
    
    $startedpostdate  = $startedpostdate + $addtimes;
    $startedlongdate  = &dateformat("$startedpostdate");
    $startedpostdate  = qq~$startedlongdate~;
    if(!$favtime){
    $favtime="Unknown";
    }else{
    $favtime  = $favtime + $addtimes;
    $favlongtime  = &dateformat("$favtime");
    $favtime  = qq~$favlongtime~;
    }

if ($tablewidth > 100) {
    if ($tablewidth > 1000) { $topictitlemax = 84; } elsif ($tablewidth > 770) { $topictitlemax = 71; } else { $topictitlemax = 40; }
} else {
    if ($screenmode >=10) { $topictitlemax = 84; } elsif ($screenmode >=8) { $topictitlemax = 71; } else { $topictitlemax = 40; }
}

    $posttemp       = "(������)" if ($posttemp eq "");
    $topictitle1=$topictitle;
    $topictitletemp = &lbhz($topictitle,$topictitlemax-6);
	$topic_title=qq( TITLE="$topictitle&nbsp;\n����ʱ�䣺 $startedpostdate&nbsp;\n�ղ�ʱ�䣺 $favtime&nbsp;\n���ظ��� $posttemp&nbsp;");
    $topictitle     = qq~<a href="topic.cgi?forum=$forumid&topic=$topicid" target="_blank" $topic_title>$topictitletemp</a>~;
    
    $startedbyfilename = $startedby;
    $startedbyfilename =~ s/ /\_/isg;
    $startedbyfilename =~ tr/A-Z/a-z/;

    if ($lastposter) {
	$lastposterfilename = $lastposter;
	$lastposterfilename =~ s/ /\_/isg;
	if ($lastposter=~/\(��\)/) {
       	    $lastposter=~s/\(��\)//isg;
	    $lastposter = qq~<font color=$postfontcolorone title="��Ϊδע���û�">$lastposter</font>~;
	}
	else {
	    $lastposter = qq~<a href=profile.cgi?action=show&member=~ . uri_escape($lastposterfilename) . qq~>$lastposter</a>~;
	}
    }
    else {$lastposter = qq~--------~;}
    undef $topicdescription;

    if ($counter == 0) { $pagestoshowtemp1 = 0; } elsif ($counter > 11) { $counter = 11; } else { $pagestoshowtemp1 = 7; }
    $totlelength = $counter*3.3 + $pagestoshowtemp1 + length($topictitletemp) + 3 + $addonlength; #���������ܳ���
    undef $pagestoshowtemp1;

    if($topicdescription=~m/<br>����-=> >>(.+?)<</){
    	$topicdescription="<br>����>>".$1;
    }
    if($cleartoedit eq "yes"){
    	if($topiccount < $ontopcount){
	    $admini = qq~<DIV ALIGN=Right><font color=$postfontcolortwo>|<a href=forums.cgi?forum=$forumid target=_blank><font color=$titlecolor>���ʸ������ڷ���̳</font></a>|<a href=fav.cgi?action=del&forum=$forumid&topic=$topicid&selectcate=$selectcate><font color=$titlecolor>ɾ��</font></a>|<a href=fav.cgi?action=top&forum=$forumid&topic=$topicid&checked=yes&selectcate=$selectcate><font color=$titlecolor>ȡ���ö�</font></a>|<a href=fav.cgi?action=mov&forum=$forumid&topic=$topicid&selectcate=$selectcate><font color=$titlecolor>�ƶ�</font></a>|</font>&nbsp;~ ;
	    $topicicon = "<img src=$imagesurl/images/$skin/locktop.gif width=15 border=0>";
	    }else{
	    $admini = qq~<DIV ALIGN=Right><font color=$postfontcolortwo>|<a href=forums.cgi?forum=$forumid target=_blank><font color=$titlecolor>���ʸ������ڷ���̳</font></a>|<a href=fav.cgi?action=del&forum=$forumid&topic=$topicid&selectcate=$selectcate><font color=$titlecolor>ɾ��</font></a>|<a href=fav.cgi?action=add&forum=$forumid&topic=$topicid&checked=yes&selectcate=$selectcate&mainopen=up><font color=$titlecolor>����</font></a>|<a href=fav.cgi?action=top&forum=$forumid&topic=$topicid&selectcate=$selectcate><font color=$titlecolor>�ö�</font></a>|<a href=fav.cgi?action=mov&forum=$forumid&topic=$topicid&selectcate=$selectcate><font color=$titlecolor>�ƶ�</font></a>|</font>&nbsp;~ ;
	    }
	 $multimanagebutton = qq~<td bgcolor=$forumcolortwo align=center width=35><input type=checkbox name=selectt value="$forumid|$topicid"></td>~; $addonlength += 2.5;
	}else{
	$multimanagebutton = qq(<td bgcolor=$forumcolortwo align=center width=35><span style="CURSOR: hand" onClick="window.external.AddFavorite('$boardurl/topic.cgi?forum=$forumid&topic=$topicid', '$boardname - $topictitle1')"><IMG SRC=$imagesurl/images/fav_add.gif BORDER=0 width=15 height=15 ALT="��������ӵ��ղؼ�"></span></td>);
	}
    $topictitle = "$mypost$topictitle";
    $topictitle=$topictitle."<BR>" if ($totlelength > $topictitlemax+7);
    if ($threadviews > 9999) { $threadviewstemp = "<font color=$forumfontcolor title=�������$threadviews>>Max</font>"; } else { $threadviewstemp = "<font color=$forumfontcolor>$threadviews</font>"; }
    if ($threadposts > 9999) { $threadpoststemp = "<font color=$forumfontcolor title=�ظ�����$threadposts>>Max</font>"; } else { $threadpoststemp = "<font color=$forumfontcolor>$threadposts</font>"; }
    if ($startedby=~/\(��\)/) { $startedby=~s/\(��\)//isg; $startedby=qq~<font color=$postfontcolorone title="��Ϊδע���û�">$startedby</font>~; } else { $startedby=qq~<a href=profile.cgi?action=show&member=~ . uri_escape($startedbyfilename) . qq~>$startedby</a>~; }
    if (($threadstate eq "poll")||($threadstate eq "pollclosed")) { 
$outputtemp=qq(<td bgcolor=$forumcolortwo align=center width=63 rowspan=2><ACRONYM TITLE="�ظ�����$threadposts�� �������$threadviews">�� $size Ʊ</ACRONYM></font></td>);
    } else { 
$outputtemp=qq(<td bgcolor=$forumcolortwo align=center width=30><font color=$forumfontcolor>$threadpoststemp</font></td><td bgcolor=$forumcolortwo align=center width=30><font color=$forumfontcolor>$threadviewstemp</font></td>);
    }
	$posticontemp  = qq~<a href=view.cgi?forum=$forumid&topic=$topicid>$posticon</a>~;

    $pagestoshow=qq(<span style="width:22%;text-align:right">$pagestoshow</span>) if($pagestoshow ne "");

    $output .=qq~<table cellspacing=0 width=$tablewidth bordercolor=$tablebordercolor border=1 align=center>
<tr><td align=center width=30 bgcolor=$forumcolorone><a href=topic.cgi?forum=$forumid&topic=$topicid target=_blank>$topicicon</a></td>
<td width=* class=dp bgColor=$forumcolortwo onmouseover="this.bgColor='$forumcolorone';" onmouseout="this.bgColor='$forumcolortwo';">&nbsp;<a href=view.cgi?forum=$inforum&topic=$topicid target=_blank>$posticon</a>&nbsp;<span id=forum>$topictitle$pagestoshow$topicdescription$admini</span></td>
<td bgcolor=$forumcolortwo align=center width=78>$startedby</td>
$outputtemp
<td width=193 bgcolor=$forumcolorone>&nbsp;$lastpostdate<font color=$fonthighlight> | </font>$lastposter</td>$multimanagebutton</tr>
</table>
~;
    $topiccount++;
    if($oldforumcolorone ne "" && $oldforumcolortwo ne ""){
    $forumcolorone=$oldforumcolorone;
    $forumcolortwo=$oldforumcolortwo;
    }
}
$output .= qq~<SCRIPT>valignend()</SCRIPT>~;
$output .= qq~<table cellpadding=0 cellspacing=2 width=$tablewidth align=center><tr height=4></tr><tr><td>$topicpages��&nbsp;[���� <B>$threads</B> ƪ���ظ� <b>$posts</b> ƪ]</td>~;
$output .= qq~<td align=center width="220"><input type="button" name="chkall" value="ȫѡ" onclick="CheckAll(this.form)"> <input type="button" name="clear2" value="��ѡ" onclick="FanAll(this.form)"> <input type="reset" name="Reset" value="����"> <input type="submit" name="submit" value="ɾ��" onClick="SetAction(this.form,'del')"> <input type="submit" name="submit" value="�ƶ�" onClick="SetAction(this.form,'mov')"></td>~ if($cleartoedit eq "yes");
$output .= qq~<td align=right width=30%>$cateoption</td></tr></form></table><br><br>~;
}
sub setting {
#        &getmember("$inmembername");

    &favmischeader("�����ղؼ��趨");

    $file=(-e"${lbdir}$memfavdir/close/$infilemembername.cgi")?"${lbdir}$memfavdir/close/$infilemembername.cgi":"${lbdir}$memfavdir/open/$infilemembername.cgi";
    if (-e $file) {
        open(FILE, "$file");
        @favtopic = <FILE>;
        close(FILE);
	@favtopic = &cleanslashes (@favtopic);#anthony
        chomp @favtopic;
        $catelist=shift(@favtopic);
        chomp $catelist;
        @catelist=split(/\t/,$catelist);
	foreach(@catelist){s/^����������//o;}
        chomp @catelist;
        $favdescript=pop(@catelist) if($catelist[$#catelist] =~/^\>\>/);
        $catelistno=@catelist;
    }else{ undef @favtopic; }
    if($checked eq "rename" && $newcate ne ""){
    	foreach(@catelist){
    	$name=$_;
    	$name=~s/[oc]$//;;
    	&error("���ø����ղ�&��Ŀ¼�Ѵ��ڣ�") if($newcate eq $name);
    	}
    	$oldcate=$catelist[$selectcate];
    	$cates=($oldcate =~ /o$/)?"o":"c";
    	$oldcate=~s/[oc]$//;
    	$catelist[$selectcate]=$newcate.$cates;
    	@catelist=grep(/(.+?)/,@catelist);
        open(FILE, ">$file");
        print FILE (join("\t",map('����������'.$_, @catelist)))."\t$favdescript\n";
        foreach $line(@favtopic){
        	my($topic,$forum,$status,$cate,$ftime)=split(/\t/,$line);
        	if($cate eq $oldcate){
        print FILE "$topic\t$forum\t$status\t$newcate\t$ftime\t\n";
        	}else{
        print FILE "$topic\t$forum\t$status\t$cate\t$ftime\t\n";
        	}
        }
        close(FILE);
    }elsif($checked eq "delete"){
    	$oldcate=$catelist[$selectcate];
    	$oldcate=~s/[oc]$//;
    	$catelist[$selectcate]="";
    	@catelist=grep(/(.+?)/,@catelist);
        open(FILE, ">$file");
        print FILE (join("\t",map('����������'.$_, @catelist)))."\t$favdescript\n";
        foreach $line(@favtopic){
        	my($topic,$forum,$status,$cate,$ftime)=split(/\t/,$line);
        	unless($cate eq $oldcate){
        print FILE "$topic\t$forum\t$status\t$cate\t$ftime\t\n";
        	}
        }
        close(FILE);
    }elsif($checked eq "up"){
    	unless($selectcate == 0){
    	$upcate=$selectcate-1;
    	($oldcate1,$oldcate2)=($catelist[$selectcate],$catelist[$upcate]);
    	$catelist[$upcate]=$oldcate1;
    	$catelist[$selectcate]=$oldcate2;
    	}
    	@catelist=grep(/(.+?)/,@catelist);
        open(FILE, ">$file");
        print FILE (join("\t",map('����������'.$_ ,@catelist)))."\t$favdescript\n";
        foreach $line(@favtopic){
        	my($topic,$forum,$status,$cate,$ftime)=split(/\t/,$line);
        print FILE "$topic\t$forum\t$status\t$cate\t$ftime\t\n";
        }
        close(FILE);
    }elsif($checked eq "down"){
    	unless($selectcate == $#catelist){
    	$downcate=$selectcate+1;
    	($oldcate1,$oldcate2)=($catelist[$selectcate],$catelist[$downcate]);
    	$catelist[$downcate]=$oldcate1;
    	$catelist[$selectcate]=$oldcate2;
    	}
    	@catelist=grep(/(.+?)/,@catelist);
        open(FILE, ">$file");
        print FILE (join("\t",map('����������'.$_, @catelist)))."\t$favdescript\n";
        foreach $line(@favtopic){
        	my($topic,$forum,$status,$cate,$ftime)=split(/\t/,$line);
        	unless($cate eq $oldcate){
        print FILE "$topic\t$forum\t$status\t$cate\t$ftime\t\n";
        	}
        }
        close(FILE);
    }elsif($checked eq "top"){
    	$oldcate1=splice(@catelist,$selectcate,1);
    	unshift(@catelist,$oldcate1);
    	@catelist=grep(/(.+?)/,@catelist);
        open(FILE, ">$file");
        print FILE (join("\t",map('����������'.$_, @catelist)))."\t$favdescript\n";
        foreach $line(@favtopic){
        	my($topic,$forum,$status,$cate,$ftime)=split(/\t/,$line);
        print FILE "$topic\t$forum\t$status\t$cate\t$ftime\t\n";
        }
        close(FILE);
    }elsif($checked eq "bottom"){
    	$oldcate1=splice(@catelist,$selectcate,1);
    	push(@catelist,$oldcate1);
    	@catelist=grep(/(.+?)/,@catelist);
        open(FILE, ">$file");
        print FILE (join("\t",map('����������'.$_, @catelist)))."\t$favdescript\n";
        foreach $line(@favtopic){
        	my($topic,$forum,$status,$cate,$ftime)=split(/\t/,$line);
        	unless($cate eq $oldcate){
        print FILE "$topic\t$forum\t$status\t$cate\t$ftime\t\n";
        	}
        }
        close(FILE);
    }elsif($checked eq "mainopen"){
		if($mainopen eq "off"){
		move("${lbdir}$memfavdir/open/$infilemembername.cgi","${lbdir}$memfavdir/close/$infilemembername.cgi") if(-e "${lbdir}$memfavdir/open/$infilemembername.cgi");
		}else{
		move("${lbdir}$memfavdir/close/$infilemembername.cgi","${lbdir}$memfavdir/open/$infilemembername.cgi") if(-e "${lbdir}$memfavdir/close/$infilemembername.cgi");
		}
    }elsif($checked eq "newcate"){
    	&error("���ø����ղ�&��Ŀ¼���Ʋ���Ϊ�գ�") if($newcate eq "");
    	&error("���ø����ղ�&��Ŀ¼���Ʋ��ܶ��� 30 ��Ӣ����(15 ��������)��") if(length($newcate) > 30);
    	foreach(@catelist){
    	$name=$_;
    	$name=~s/[oc]$//;;
    	&error("���ø����ղ�&��Ŀ¼�Ѵ��ڣ�") if($newcate eq $name);
    	}
    	push(@catelist,$newcate."o");
        $catelistno=@catelist;
        &error("���ø����ղ�&���ֻ�ܹ��� 10 ��Ŀ¼��") if($catelistno > 10);
        open(FILE, ">$file");
        print FILE (join("\t",map('����������'.$_, @catelist)))."\t$favdescript\n";
        foreach $line(@favtopic){
        	my($topic,$forum,$status,$cate,$ftime)=split(/\t/,$line);
        print FILE "$topic\t$forum\t$status\t$cate\t$ftime\t\n";
        }
        close(FILE);
    }elsif($checked eq "cateopen"){
    	$oldcate=$catelist[$selectcate];
    	$ccates=($oldcate =~ /o$/)?"c":"o";
    	$oldcate=~s/[oc]$//;
    	$catelist[$selectcate]=$oldcate.$ccates;
    	@catelist=grep(/(.+?)/,@catelist);
        open(FILE, ">$file");
        print FILE (join("\t",map('����������'.$_, @catelist)))."\t$favdescript\n";
        foreach $line(@favtopic){
        	my($topic,$forum,$status,$cate,$ftime)=split(/\t/,$line);
        print FILE "$topic\t$forum\t$status\t$cate\t$ftime\t\n";
        }
        close(FILE);
    }elsif($checked eq "changedescript"){
    	&error("���ø����ղ�&��鲻�ܶ��� 300 ��Ӣ����(150 ��������)��") if(length($newcate) > 300);
    	@descriptline = split(/\<br\>/,$newcate);
    	$descriptline = @descriptline;
    	&error("���ø����ղ�&��鲻�ܶ��� 3 �У�") if($descriptline > 3);
        open(FILE, ">$file");
        print FILE (join("\t",map('����������'.$_, @catelist)))."\t>>$newcate\n";
        foreach $line(@favtopic){
        	my($topic,$forum,$status,$cate,$ftime)=split(/\t/,$line);
        print FILE "$topic\t$forum\t$status\t$cate\t$ftime\t\n";
        }
        close(FILE);
    }
	if($checked ne ""){
	print qq ~<script>location.href="$thisprog?action=setting";</script>~;
	exit;
	}
	$favdescript=~s/^>>//;
	$favdescript=~s/<br>/\n/isg;
	$favdescript=~s/<p>/\n\n/isg;

	if($file eq "${lbdir}$memfavdir/close/$infilemembername.cgi"){
		$mainopenselect=qq(<option value="on">��ȫ����</option><option value="off" selected>��ȫ����</option>);
	}else{
		$mainopenselect=qq(<option value="on" selected>��ȫ����</option><option value="off">��ȫ����</option>);
	}
            $inmembername =~ s/\_/ /g;
    $cattemplist=join('","',@catelist);
            $output .= qq~
<script language="JavaScript" type="text/javascript">
var catlist=new Array("$cattemplist");
function edit(no,action){
fav.selectcate.value=no;
fav.checked.value=action;
	if(action == 'rename'){
		newname=prompt("�������µ�Ŀ¼���ơ�",catlist[no].replace(\/[oc]\$\/,""));
		if(newname == ""){
			alert("��Ŀ¼���Ʋ���Ϊ�գ�");
		}else if(newname != null){
			if(newname.length>30){
			alert("��Ŀ¼���Ʋ��ܶ�� 30 ��������(15 ��������)��");
			}else{
			fav.newcate.value=newname;
			fav.submit();
			}
		}
	}else if(action == 'delete'){
		if(confirm("ȷ��ɾ����Ŀ¼��\\n��Ŀ¼����������ᱻɾ����")==true){
		fav.submit();
		}
	}else{
		fav.submit();
	}
}
</script>
            <SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 width=100%>
            <tr>
            <form action="$thisprog" method="post" name="fav">
            <input type=hidden name="action" value="setting">
            <input type=hidden name="checked" value="">
            <input type=hidden name="selectcate" value="">
            <input type=hidden name="newcate" value="">
            </form>
            <td bgcolor=$titlecolor colspan=3 align=center $catbackpic>
            <font color=$fontcolormisc><b>���ø����ղ�</b></font></td></tr>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="setting">
            <input type=hidden name="checked" value="mainopen">
            <tr><td bgcolor=$miscbacktwo colspan="3"><span style="width=200"><b>�趨���ŷ�ʽ��</b></span><select name="mainopen">$mainopenselect</select> <input type=submit name="submit" value="�� ��"></td></tr></form>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="setting">
            <input type=hidden name="checked" value="changedescript">
            <tr><td bgcolor=$miscbacktwo colspan="3"><span style="width:200"><b>�ղؼ����ݼ�飺</b><br><br><br><li>���5�У�300�ֽ�</li><li><a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LeoBBS ��ǩ</a>: <b>����</b></li></span><textarea name="newcate" rows="5" cols="50">$favdescript</textarea>��<input type=submit name="submit" value="�޸ļ��"></span></td></tr></form>
            <tr>
            <td bgcolor=$titlecolor colspan=3 align=center $catbackpic>
            <font color=$fontcolormisc><b>�����ղ�Ŀ¼</b></font></td></tr>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="setting">
            <input type=hidden name="checked" value="newcate">
            <tr><td bgcolor=$miscbackone align="center" colspan="3"><font color=$fontcolormisc>��Ŀ¼����</font>��<input type=text name="newcate" value="" style="width:200"> <input type=submit name="submit" value="������Ŀ¼">&nbsp;&nbsp;&nbsp;&nbsp;</td></tr></form>
            ~;
            $i=0;
            foreach(@catelist){
            $name=$_;
            $name=~s/[oc]$//;
            $ccates=($_ =~ /o$/)?"�ر�":"����";
            $ncates=($_ =~ /o$/)?"������":"�ر���";
            $output .= qq~
            <tr bgColor=$forumcolortwo onmouseover="this.bgColor='$forumcolorone';" onmouseout="this.bgColor='$forumcolortwo';">
            <td width="61%"><img src=$imagesurl/images/folder.gif width=13 height=16 align=absmiddle> <a href="$thisprog?action=show&selectcate=$i"><font color=$fontcolormisc>$name</a> <font color=$fonthighlight>($ncates)</font></font><div align=right>|<a href=javascript:edit($i,'rename')><font color=$titlecolor>����</a></font>|<a href=javascript:edit($i,'delete')><font color=$titlecolor>ɾ��</a></font>|<a href=javascript:edit($i,'up')><font color=$titlecolor>����</font></a>|<a href=javascript:edit($i,'down')><font color=$titlecolor>����</font></a>|<a href=javascript:edit($i,'top')><font color=$titlecolor>����</font></a>|<a href=javascript:edit($i,'bottom')><font color=$titlecolor>�ײ�</font></a>|</div></td>
            <td align="center" width="5%">
            <input type=button name="submit" value="$ccates" onClick="edit($i,'cateopen')">
            </td></tr>
            ~;
            undef @disable;
            $i++;
            }
            $output .= qq~
            </table></td></tr></table>
            <SCRIPT>valignend()</SCRIPT>
            ~;
#    }
} # end
sub favmischeader{
    local($misctype) = shift;
       &title;
    $output .= qq~
<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=12> <font color=$navfontcolor><a href=leobbs.cgi>$boardname</a> �� <a href=fav.cgi?action=show>�����ղ�</a> �� $misctype</td><td bgcolor=$navbackground align=right><a href="$thisprog?action=setting">�����ղؼ��趨</a></td></tr></table></td></tr></table><BR>
~;
}
#anthony
sub cleanslashes
{
	my (@ref);
	for (my $i=0;$i<=$#_;$i++)
	{
		$ref[$i] = $_[$i];
		$ref[$i] =~ s/\\\`/\`/isg;
		$ref[$i] =~ s/\\\;/\;/isg;
		$ref[$i] =~ s/\\\\/\\/isg;
		$ref[$i] =~ s/\\\>/\>/isg;
		$ref[$i] =~ s/\\\</\</isg;
		$ref[$i] =~ s/\\\@/\@/isg;
		$ref[$i] =~ s/\\\\/\\/isg;
		$ref[$i] =~ s/\\\'/\'/isg;
		$ref[$i] =~ s/\\\"/\"/isg;
		$ref[$i] =~ s/\\\./\./isg;
		$ref[$i] =~ s/\\\$/\$/isg;
		$ref[$i] =~ s/\\\=/\=/isg;
		$ref[$i] =~ s/\\\//\//isg;
	}
	return @ref;
}
#anthony_end
