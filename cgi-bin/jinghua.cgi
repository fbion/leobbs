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
$LBCGI::POST_MAX=200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "code.cgi";
require "bbs.lib.pl";
require "rebuildlist.pl";
require "recooper.pl";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$|++;
$thisprog = "jinghua.cgi";
$query = new LBCGI;
&ipbanned; #��ɱһЩ ip

$inshow  = $query -> param('show');
for ('forum','topic','membername','password','action','checked','movetoid') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
$inforum       = $forum;
$intopic       = $topic;
$inmembername  = $membername;
$inpassword    = $password;
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

@intopic=split(/ /,$intopic);
$intopic=~ s/ //g;
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum) && ($inforum !~ /^[0-9]+$/));
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
require "sendmanageinfo.pl" if ($sendmanageinfo eq "yes");

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

if (($inforum)  && ($inforum  !~ /^[0-9]+$/)) { &error("��ͨ����&�벻Ҫ�޸����ɵ� URL��"); }
if (($intopic ) && ($intopic  !~ /^[0-9]+$/)) { &error("��ͨ����&�벻Ҫ�޸����ɵ� URL��"); }
if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

    if ($inmembername eq "") {
        $inmembername = "����";
    }
    else
    {
#    &getmember("$inmembername");
    &getmember("$inmembername","no");
     if ($inpassword ne $password) {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("��ͨ����&�������û���������������µ�¼��");
     }
    &error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
}
&getoneforum("$inforum");
#&moderator("$inforum");
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }
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

my %Mode = (
    'add'  =>   \&add,
    'del'  =>   \&del,
    );
if($Mode{$action}) {
        $Mode{$action}->();
        }
        elsif (($inforum ne "")&&($action eq "list")) { &list;   }
        else { &error("��ͨ����&������ȷ�ķ�ʽ���ʱ�����"); }
    &output($boardname,\$output);

sub add {
    $cleartoedit = "no";

    &mischeader("��Ǿ�������");
    if (($membercode eq "ad")  && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($membercode eq "smo") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($inmembmod eq "yes")  && ($membercode ne "amo") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    if ($cleartoedit eq "no") { &error("��Ǿ�������&�����Ǳ���̳̳������������������������"); }
    
    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
    	unlink("${lbdir}cache/forumstop$inforum.pl");
    	unlink("${lbdir}cache/forumstopic$inforum.pl");
        my $file = "$lbdir" . "boarddata/jinghua$inforum.cgi";
        if (open (ENT, $file)) {
            @toptopic = <ENT>;
            close (ENT);
		$jhdata = join("\_",@toptopic);
    		$jhdata = "\_$jhdata\_";
    		$jhdata =~ s/\W//isg;
            if (open (ENT, ">$file")) {
            	undef @intopictemp;
            	$jhdata1 = "\_";
                foreach (@intopic){
	            chomp $_;
		    if ((-e "${lbdir}forum$inforum/$_.thd.cgi")&&($_ ne "")) {
		    	print ENT "$_\n";
            		$jhdata1 = "\_$_$jhdata1";
            		push(@intopictemp, $_);
		    }
		}
            	undef $intopictemp1;
	        foreach $ttemp (@toptopic) {
	            chomp $ttemp;
	    	    if ((-e "${lbdir}forum$inforum/$ttemp.thd.cgi")&&($ttemp ne "")&&($jhdata1 !~ /\_$ttemp\_/)) {
	    	        print ENT "$ttemp\n";
	    	        $jhdata1 = "$jhdata1\_$ttemp";
	    	    } else {
            		$intopictemp1 = "$intopictemp1\_$ttemp";
	    	    }
	        }
                close (ENT);
            }
        }
        else {
            if (open (ENT, ">$file")) {
            	$jhdata = "\_";
            	undef @intopictemp;
                foreach (@intopic){
                    chomp $_;
		    if ((-e "${lbdir}forum$inforum/$_.thd.cgi")&&($_ ne "")&&($jhdata !~ /\_$_\_/)) {
                        print ENT "$_\n";
            		$jhdata = "\_$_$jhdata";
            		push(@intopictemp, $_);
		    }
	        }
                close (ENT);
            }
        }
        if ($intopictemp1 ne "") {
            undef @intopictemp1;
            $intopictemp1 = "$intopictemp1\_";
	    foreach (@intopictemp) {
	    	chomp $_;
            	push(@intopictemp1, $_) if ($intopictemp1 !~ /\_$_\_/);
	    }
	    @intopictemp = @intopictemp1;
	}
        @intopic = @intopictemp;
       	undef @intopictemp;
        $alloldposts = @intopic;
        if ($movetoid ne ""){
            if ($movetoid == $inforum) { &error("��������&��������ͬ����̳�Ͽ������⣡"); }
			if (open(FILE, "${lbdir}forum$movetoid/foruminfo.cgi"))
			{
				$readdisktimes++;
				$forums = <FILE>;
				close(FILE);
				(undef, undef, undef, $newforumname, undef) = split(/\t/, $forums);
			}
			else
			{
				&error("��������&Ŀ����̳�����ڣ�")
			}

	    my @inforumwrite;
	    $alloldthreadposts = 0;
            opendir (DIR, "${imagesdir}$usrdir/$inforum");
            @files = readdir(DIR);
            closedir (DIR);
	    @files = grep(/^$inforum\_$intopic(\.|\_)/,@files);
	    
	    foreach $intopic (@intopic) {
                $currenttime = time;
	        if ($newthreadnumber eq "") {
	            if (open(FILE, "${lbdir}boarddata/lastnum$movetoid.cgi")) {
	                $newthreadnumber = <FILE>;
                        close(FILE);
                        chomp $newthreadnumber;
	                $newthreadnumber ++;
	            }
	        }
	        else { $newthreadnumber ++; }
	        unless ((!(-e "${lbdir}forum$movetoid/$newthreadnumber.pl"))&&($newthreadnumber =~ /^[0-9]+$/)) {
                    opendir (DIR, "${lbdir}forum$movetoid");
                    @sorteddirdata = readdir(DIR);
                    closedir (DIR);
                    @sorteddirdata = grep(/.thd.cgi$/,@sorteddirdata);
                    @sorteddirdata = sort {$b <=> $a} (@sorteddirdata);
                    $highestno = $sorteddirdata[0];
                    undef @sorteddirdata;
                    $highestno =~ s/.thd.cgi$//;
                    $newthreadnumber = $highestno + 1;
	        }

    		$intopic =~ s/\W//isg;
	    	chomp $intopic;
        	open (ENT, "${lbdir}forum$inforum/$intopic.pl");
        	$in = <ENT>;
        	close (ENT);
        	chomp $in;
        	($topicid, $topictitle, $topicdescription1, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $lastinposticon, $inposttemp, $addmetemp) = split(/\t/,$in);

                $inforumwrite = "$newthreadnumber\t$topictitle\t\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$currenttime\t$lastinposticon\t$inposttemp\t$addmetemp\t";
                if (open(FILE, ">${lbdir}forum$movetoid/$newthreadnumber.pl")) {
                    print FILE "$inforumwrite";
                    close(FILE);
                }
                push (@inforumwrite, "$newthreadnumber");

                $filetoopen = "${lbdir}forum$inforum/$intopic.thd.cgi";
                open(FILE, "$filetoopen");
                my @oldforummessages = <FILE>;
                close(FILE);
                $oldthreadposts = @oldforummessages - 1;
                $alloldthreadposts = $alloldthreadposts + $oldthreadposts;

   	        copy("${lbdir}forum$inforum/$intopic.thd.cgi",      "${lbdir}forum$movetoid/$newthreadnumber.thd.cgi")       if (-e "${lbdir}forum$inforum/$intopic.thd.cgi");
   	        copy("${lbdir}forum$inforum/$intopic.mal.pl",       "${lbdir}forum$movetoid/$newthreadnumber.mal.pl")        if (-e "${lbdir}forum$inforum/$intopic.mal.pl");
   	        copy("${lbdir}forum$inforum/$intopic.poll.cgi",     "${lbdir}forum$movetoid/$newthreadnumber.poll.cgi")      if (-e "${lbdir}forum$inforum/$intopic.poll.cgi");
   	        copy("${lbdir}forum$inforum/rate$intopic.file.pl",  "${lbdir}forum$movetoid/rate$newthreadnumber.file.pl")   if (-e "${lbdir}forum$inforum/rate$intopic.file.pl");
   	        copy("${lbdir}forum$inforum/rateip$intopic.file.pl","${lbdir}forum$movetoid/rateip$newthreadnumber.file.pl") if (-e "${lbdir}forum$inforum/rateip$intopic.file.pl");


##########�ɵĸ���copy��Ϊ�˼��ݣ����� ·��
                @files1 = grep(/^$inforum\_$intopic\./,@files);
                $files1 = @files1;
	        if ($files1 > 0) {
	            foreach (@files1) {
	    	        (my $name,my $ext) = split(/\./,$_);
		        copy("${imagesdir}$usrdir/$inforum/$name.$ext","${imagesdir}$usrdir/$movetoid/$movetoid\_$newthreadnumber\.$ext");
	            }
	        }

                @files1 = grep(/^$inforum\_$intopic\_/,@files);
                $files1 = @files1;
	        if ($files1 > 0) {
	            foreach (@files1) {
	    	        (my $name,my $ext) = split(/\./,$_);
	    	        (my $name1,my $name2,my $name3) = split(/\_/,$name);
		        copy("${imagesdir}$usrdir/$inforum/$name.$ext","${imagesdir}$usrdir/$movetoid/$movetoid\_$newthreadnumber\_$name3\.$ext");
	            }
	        }
###########
            require "dopost.pl"; #·��
            &moveallupfiles($inforum,$intopic,$movetoid,$newthreadnumber,"yes"); #�µĸ���copy ·��
	    }

            $file = "$lbdir" . "boarddata/listno$movetoid.cgi";
            &winlock($file) if ($OS_USED eq "Nt");
            open (LIST, "$file");
            flock (LIST, 1) if ($OS_USED eq "Unix");
	    sysread(LIST, $listall,(stat(LIST))[7]);
            close (LIST);
	    $listall =~ s/\r//isg;
            open (LIST, ">$file");
            flock (LIST, 2) if ($OS_USED eq "Unix");
            foreach (@inforumwrite) {
              	chomp $_;
                print LIST "$_\n" if ($_ ne "");
            }
            print LIST $listall;
            close (LIST);
            &winunlock($file) if ($OS_USED eq "Nt");

            $newthreadnumber ++;
            if (open(FILE, ">${lbdir}boarddata/lastnum$movetoid.cgi")) {
                print FILE $newthreadnumber;
                close(FILE);
	    }

	$filetoopen = "${lbdir}boarddata/foruminfo$movetoid.cgi";
	my $filetoopens = &lockfilename($filetoopen);
	if (!(-e "$filetoopens.lck")) {
            &winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

            open(FILE, "+<$filetoopen");
            ($lastposttime, $threads, $posts, $todayforumpost, $lastposter) = split(/\t/,<FILE>);

            $threads = $alloldposts + $threads;
            $posts   = $posts + $alloldthreadposts;
            $lastposter = $startedby if ($lastposter eq "");
            $topictitle =~ s/^����������//;
            my $newthreadnumber = $newthreadnumber - 1;
            $lastposttime = "$currenttime\%\%\%$newthreadnumber\%\%\%$topictitle";
	    seek(FILE,0,0);
            print FILE "$lastposttime\t$threads\t$posts\t$todayforumpost\t$lastposter\t\n";
            close(FILE);
	    $posts = 0 if ($posts eq "");$threads = 0 if ($threads eq "");
	    open(FILE, ">${lbdir}boarddata/forumposts$movetoid.pl");
	    print FILE "\$threads = $threads;\n\$posts = $posts;\n\$todayforumpost = \"$todayforumpost\";\n1;\n";
            close(FILE);

            &winunlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	}
        else {
    	    unlink ("$filetoopens.lck") if ((-M "$filetoopens.lck") *86400 > 30);
	}

            $filetomake = "${lbdir}data/boardstats.cgi";
            require "$filetomake";

            $totalthreads = $totalthreads + $alloldposts;
            $totalposts   = $totalposts + $alloldthreadposts;
	    &winlock($filetomake) if ($OS_USED eq "Nt");
            if (open(FILE, ">$filetomake")) {
                flock(FILE, 2) if ($OS_USED eq "Unix");
                print FILE "\$lastregisteredmember = \'$lastregisteredmember\'\;\n";
                print FILE "\$totalmembers = \'$totalmembers\'\;\n";
                print FILE "\$totalthreads = \'$totalthreads\'\;\n";
                print FILE "\$totalposts = \'$totalposts\'\;\n";
                print FILE "\n1\;";
                close (FILE);
            }
            &winunlock($filetomake) if ($OS_USED eq "Nt");
	}

		$newforumname = "�����Ƶ� $newforumname" if ($newforumname ne "");
		if ($alloldposts == 1)
		{
			&addadminlog("��Ǿ�������$newforumname", $intopic);
		}
		else
		{
			&addadminlog("������Ǿ������� $alloldposts ƪ$newforumname");
		}
	&UpdateNo(\@intopic,$inforum,"+");
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td>
<table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>��Ǿ������ӳɹ�</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>���������<ul>
<li><a href="jinghua.cgi?action=list&forum=$inforum">���ؾ�����</a>
<li><a href="forums.cgi?forum=$inforum">������̳</a>
<li><a href="leobbs.cgi">������̳��ҳ</a>
</ul></tr></td></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
    }
    else {
        $inmembername =~ s/\_/ /g;
        open(FILE, "${lbdir}data/allforums.cgi");
        my @forums = <FILE>;
        close(FILE);
        $jumphtml .= "<option value=\"\">ѡ��һ����̳\n</option><option value=\"\">�����κο���\n</option>";
        $a = 0;
        foreach (@forums) {
            chomp $_;
      	    next if (length("$_") < 30);
	    $a  = sprintf("%09d",$a);
            ($movetoforumid, $category, $categoryplace, $forumname, $forumdescription, $noneed ,$noneed ,$noneed ,$noneed, $startnewthreads ,$noneed ,$noneed, $noneed, $noneed, $noneed, $miscad2, $noneed,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/,$_);
	    $categoryplace  = sprintf("%09d",$categoryplace);
            $rearrange = ("$categoryplace\t$a\t$category\t$forumname\t$forumdescription\t$movetoforumid\t$forumgraphic\t$startnewthreads\t$miscad2\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$fgwidth\t$fgheight\t$miscad4\t$todayforumpost\t$miscad5\t");
            push (@rearrangedforums, $rearrange);
	    $a++;
        }

        @finalsortedforums = sort (@rearrangedforums);
        foreach (@finalsortedforums) {
	    ($categoryplace,my $a, $category, $forumname, $forumdescription, $movetoforumid, $forumgraphic, $startnewthreads,$miscad2, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/,$_);

	    if ((($startnewthreads eq "no")||($startnewthreads eq "cert"))&&($movetoforumid ne $inforum)) {
	        $jumphtml .= "<option value=\"$movetoforumid\">$forumname\n</option>";
	    }
        }
        $intopic = @intopic;
        &error("��Ǿ�������&����ѡ�������ٽ��б�ǣ�") if ($intopic <= 0);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="add">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="@intopic">
<font color=$fontcolormisc><b>�����������û���������������ģʽ [��� $intopic ����������]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>����һ������������</b></font></td>
<td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><select name="movetoid">$jumphtml</select></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="�� ¼"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}

sub del {
    &mischeader("ȡ����������");
    $cleartoedit = "no";
    if (($membercode eq "ad")  && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($membercode eq "smo") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($inmembmod eq "yes")  && ($membercode ne "amo") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    if ($cleartoedit eq "no") { &error("ȡ����������&�����Ǳ���̳̳������������������������"); }

    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
    	unlink("${lbdir}cache/forumstop$inforum.pl");
    	unlink("${lbdir}cache/forumstopic$inforum.pl");
        my $file = "$lbdir" . "boarddata/jinghua$inforum.cgi";
        if (-e $file) {
            open (ENT, $file);
            @toptopic = <ENT>;
            close (ENT);

            if (open (ENT, ">$file")) {
                $jhdel = 0;
	        foreach (@toptopic) {
	            chomp $_;
	            if ($_ ne $intopic) {
	    	        print ENT "$_\n" if ((-e "${lbdir}forum$inforum/$_.thd.cgi")&&($_ ne ""));
	            } else {
	                $jhdel = 1;
	            }
	        }
                close (ENT);
            }
        }
	&addadminlog("ȡ���������ӱ��", $intopic);
	&UpdateNo($intopic,$inforum,"-") if ($jhdel eq 1);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td>
<table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>ȡ���������ӳɹ�</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>���������<ul>
<li><a href="jinghua.cgi?action=list&forum=$inforum">���ؾ�����</a>
<li><a href="forums.cgi?forum=$inforum">������̳</a>
<li><a href="leobbs.cgi">������̳��ҳ</a>
</ul></tr></td></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
    }
    else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td>
<table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="del">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>�����������û���������������ģʽ [ȡ����������]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="�� ¼"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}

sub list {
    &mischeader("���澫������");
    if ("$privateforum" eq "yes"){
        if ($inmembername eq "����") {
	    print "<script language='javascript'>document.location = 'loginout.cgi?forum=$inforum'</script>";
	    exit;
        }
        $testentry = cookie("forumsallowed$inforum");
        if ((($testentry eq $forumpass)&&($testentry ne ""))||(($userregistered ne "no")&&($allowedentry{$inforum} eq "yes"))||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) {
	    if ($inpassword ne $password) { &error("������̳&��������㲻����������̳��"); }
        } else { require "accessform.pl"; }
    }
    if (($startnewthreads eq "cert")&&(($membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo"&& $membercode ne "amo" && $membercode ne "mo" && $membercode !~ /^rz/)||($inmembername eq "����"))&&($userincert eq "no")) { &error("������̳&һ���Ա������������̳��"); }

    $defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
    $defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
        if ($privateforum ne "yes") {
    	    &whosonline("$inmembername\t$forumname\tboth\t�鿴��̳�ϵľ�������\t");
        }
        else {
	    &whosonline("$inmembername\t$forumname(��)\tboth\t�鿴������̳�ϵľ�������\t");
        }
    }

$output.=qq~
<style>
TABLE {BORDER-TOP: 0px; BORDER-LEFT: 0px; BORDER-BOTTOM: 1px; }
TD {BORDER-RIGHT: 0px; BORDER-TOP: 0px; color: $fontcolormisc; }
.ha {color: $fonthighlight; font: bold;}
.hb {color: $menufontcolor; font: bold;}
.dp {padding: 4px 0px;}
</style>
<span id=forum>
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
</tr></table>
	~;

    $icon_num = int(myrand(10));
    $topcount = 0;
    $filetoopen = "$lbdir" . "boarddata/jinghua$inforum.cgi";
    if (-e $filetoopen) {
    	&winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE, "$filetoopen");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        @ontop = <FILE>;
        close(FILE);
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
    }
    else { undef @ontop; }
    $topcount = @ontop;
    $numberofpages = $topcount / $maxthreads;


    if ($topcount > $maxthreads) {
        $showmore = "yes";
        if ($inshow eq "" || $inshow < 0) { $inshow = 0; }
        if ($inshow > 0) { $startarray = $inshow; }
        else { $startarray = 0; }
        $endarray = $inshow + $maxthreads - 1;
        if ($endarray < ($topcount - 1)) { $more = "yes"; }
        elsif (($endarray > ($maxthreads - 1)) && ($more ne "yes")) { $endarray = $topcount -1; }
    }
    else {
        $showmore = "no";
        $startarray = 0;
        $topicpages = qq~<font color=$menufontcolor>��������ֻ��һҳ</font>~;
        $endarray = $topcount -1;
    }

        if ($showmore eq "yes") {
	if ($maxthreads < $topcount) {
	    ($integer,$decimal) = split(/\./,$numberofpages);
	    if ($decimal > 0) { $numberofpages = $integer + 1; }
	    $mypages=$numberofpages;
	    #��ҳ
	    $intshow=$inshow/(12*$maxthreads);
	    ($intshow,$mydecimal) = split(/\./,$intshow);
	    $intshow = $intshow + 1;
	    $preshow=($intshow-1)*12*$maxthreads-$maxthreads;
	    $nextshow=$intshow*12*$maxthreads;
	    $pages=qq~<a href="$thisprog?action=list&forum=$inforum&show=$preshow"><font color=$menufontcolor><b>��</b></font></a> ~ if ($intshow > 1);
	    if ($numberofpages > ($intshow*12)){
		$numberofpages=($intshow*12);
		$isnext=qq~<a href="$thisprog?action=list&forum=$inforum&show=$nextshow"><font color=$menufontcolor><b>��</b></font></a> ~;
	    }
	    $pagestart = ($intshow-1)*12*$maxthreads;
            $counter = ($intshow-1)*12;
            while ($numberofpages > $counter) {
		$counter++;
		if ($inshow ne $pagestart) { $pages .= qq~<a href="$thisprog?action=list&forum=$inforum&show=$pagestart"><font color=$menufontcolor><b>$counter</b></font></a> ~; }
		else { $pages .= qq~<font color=$fonthighlight><b>$counter</b></font> ~; }
		$pagestart = $pagestart + $maxthreads;
	    }
	    $pages .=  $isnext;
	    #��ҳend
	}
	$topicpages = qq~<font color=$menufontcolor><b>������������ <font color=$fonthighlight>$mypages</font> ҳ</b> [ $pages ]~;
    }
    if ($topcount > 0) {

    for ($i=$startarray;$i<=$endarray;$i++) {
      	$id=$ontop[$i];
      	chomp $id;
      	$rr = &readthreadpl($inforum,$id);
	if ($rr ne "") {push (@toptopic, $rr);}
    }
  }
  else { undef @toptopic; }



$topiccount = 0;
        foreach $topic (@toptopic) {
	    chomp $topic;
            ($lastpostdate, $topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $posticon, $posttemp) = split(/\t/,$topic);
       	    next if ($topicid eq "");
            if ($posticon ne "") {
            	$poll=0;
            	if ($posticon =~/<br>/i){
                    $posticon = int(myrand(23));
    		    $posticon = "0$posticon" if ($posticon<10);
		    $posticon = qq~<img src=$imagesurl/posticons/$posticon.gif border=0 alt="���ŷ�ʽ���">~;
            	}
            	else{
            	    $posticon = qq~<img src=$imagesurl/posticons/$posticon border=0 alt="���ŷ�ʽ���">~;
            	}
            }
	    else {
    		$posticon = int(myrand(23));
    		$posticon = "0$posticon" if ($posticon<10);
		$posticon = qq~<img src=$imagesurl/posticons/$posticon.gif border=0 alt="���ŷ�ʽ���">~;
	    }
	   
    	    $topictitle =~ s/^����������//;
	    $lastpostdatetemp=$lastpostdate;

	    $lastpostdate=$lastpostdatetemp;
            $topcount = $threadposts + 1;
            $topcount = $topcount / $maxtopics;
	    $counter = 0;
            if ($topcount > $maxtopics) {
		if ($maxtopics < $topcount) {
		    ($integer,$decimal) = split(/\./,$topcount);
		    if ($decimal > 0) { $topcount = $integer + 1; }
		    $pagestart = 0;
		    while ($topcount > $counter) {
			$counter++;
			$threadpages .= qq~<a href=topic.cgi?forum=$inforum&topic=$topicid&start=$pagestart><font color=$fonthighlight><b>$counter</b></font></a> ~;
			$pagestart = $pagestart + $maxtopics;
		    }
		}
		$pagestoshow = qq~<font color=$forumfontcolor>����[�� $threadpages ҳ]</font>~;
	    }





	    if ($lastpostdate ne "") {
		$lastpostdate = $lastpostdate + ($timedifferencevalue*3600) + ($timezone*3600);
		$longdate = &dateformatshort("$lastpostdate");
		$lastpostdate = qq~<font color=$fontcolormisc>$longdate</font>~;
	    }
	    else {
		$lastpostdate = qq~<font color=$fontcolormisc>û��~;
		$lastpoststamp = "";
	    }
	    $startedpostdate = $startedpostdate + ($timedifferencevalue*3600) + ($timezone*3600);
	    $startedlongdate = &shortdate("$startedpostdate");
	    $startedshorttime = &shorttime("$startedpostdate");
	    $startedpostdate = qq~<font color=$fontcolormisc>$startedlongdate</font>~;
	    $screenmode   = $query->cookie("screenmode");
	    $topictitlemax = 54;

if ($tablewidth > 100) {
    if ($tablewidth > 1000) { $topictitlemax = 84; } elsif ($tablewidth > 770) { $topictitlemax = 71; } else { $topictitlemax = 40; }
} else {
    if ($screenmode >=10) { $topictitlemax = 84; } elsif ($screenmode >=8) { $topictitlemax = 71; } else { $topictitlemax = 40; }
}

	    $posttemp = "(������)" if ($posttemp eq "");
	    if (length($topictitle)>$topictitlemax) { $topictitletemp = substr($topictitle,0,$topictitlemax-4)." ..."; }
	    else { $topictitletemp = $topictitle; }
	    $topictitle = qq~<ACRONYM TITLE="���ظ�ժҪ��\n\n$posttemp"><a href=topic.cgi?forum=$inforum&topic=$topicid target=_blank>$topictitletemp</a></ACRONYM>~;
	    $startedbyfilename = $startedby;
	    $startedbyfilename =~ s/ /\_/isg;
	    $startedbyfilename =~ tr/A-Z/a-z/;
           if ($startedby=~/\(��\)/) { $startedby=~s/\(��\)//isg; $startedby=qq~<font color=$postfontcolorone title="��Ϊδע���û�">$startedby</font>~; } else { $startedby=qq~<a href=profile.cgi?action=show&member=~ . uri_escape($startedbyfilename) . qq~>$startedby</a>~; }
    if (($threadstate eq "poll")||($threadstate eq "pollclosed")) { $outputtemp = qq~<td bgcolor=$forumcolortwo align=center width=63 rowspan=2><ACRONYM TITLE="�ظ�����$threadposts�� �������$threadviews">�� $size Ʊ</ACRONYM></font></td>~; } else { $outputtemp = qq~<td bgcolor=$forumcolortwo align=center width=30><font color=$forumfontcolor>$threadposts</font></td><td bgcolor=$forumcolortwo align=center width=30><font color=$forumfontcolor>$threadviews</font></td>~; }

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
	    else {$lastposter = qq~<font color=$fontcolormisc>--------</a>~;}

	    $topicdescriptiontemp = $topicdescription;

	    $topicdescriptiontemp =~s/\s*(.*?)\s*\<a \s*(.*?)\s*\>\s*(.*?)\s*\<\/a\>/$3/isg;
	    $topicdescriptiontemp =~s/\<\/a\>//isg;

	    if (length($topicdescriptiontemp) > ($topictitlemax-4)) {
		$topicdescriptiontemp = substr($topicdescriptiontemp,0, $topictitlemax-8) . " ...";
		$topicdescription =~s/\<a \s*(.*?)\s*\>\s*(.*?)\s*\<\/a\>/\<a $1\>$topicdescriptiontemp\<\/a\>/isg;
	    }

	    if ($topicdescription) { $topicdescription = qq~<br>����-=> $topicdescription~; }

	    if ($counter == 0) { $pagestoshowtemp1 = 0; }
	    else { $pagestoshowtemp1 =7;}
	    $totlelength = $counter*3.3 + $pagestoshowtemp1 + length($topictitletemp) + 4; #���������ܳ���
	    undef $pagestoshowtemp1;



      	   if (($membercode eq "ad") ||($membercode eq "smo") || ($inmembmod eq "yes")) {
		    $admini = qq~<DIV ALIGN=Right><font color=$titlecolor>|<a href=jinghua.cgi?action=del&forum=$inforum&topic=$topicid&checked=yes><font color=$titlecolor>��</font></a>|<a href=jinghua.cgi?action=add&forum=$inforum&topic=$topicid><font color=$titlecolor>��</font></a>|<a href=postings.cgi?action=lock&forum=$inforum&topic=$topicid&checked=yes><font color=$titlecolor>��</font></a>|<a href=postings.cgi?action=unlock&forum=$inforum&topic=$topicid&checked=yes><font color=$titlecolor>��</font></a>|</font>&nbsp;</DIV>~;
      	   }else{
      	   $admini="";
      	   }
            $topicicon = "<img src=$imagesurl/images/jh.gif border=0>";

    if (($threadstate eq "poll")||($threadstate eq "pollclosed")) {
       	$size = 0;
	if (open(FILE, "${lbdir}forum$forumid/$topicid.poll.cgi")) {
	    my @allpoll = <FILE>;
            close(FILE);
	    $size = @allpoll;
        }
    }

    if (($threadstate eq "poll")||($threadstate eq "pollclosed")) { $outputtemp = qq~<td bgcolor=$forumcolortwo align=center width=63 rowspan=2><ACRONYM TITLE="�ظ�����$threadposts�� �������$threadviews">�� $size Ʊ</ACRONYM></font></td>~; } else { $outputtemp = qq~<td bgcolor=$forumcolortwo align=center width=30><font color=$forumfontcolor>$threadposts</font></td><td bgcolor=$forumcolortwo align=center width=30><font color=$forumfontcolor>$threadviews</font></td>~; }

	    $topictitle=$topictitle."<BR>" if ($totlelength > $topictitlemax+5);
	    $output .=qq~
		<table cellspacing=0 width=$tablewidth bordercolor=$tablebordercolor border=1><tr><td align=center width=30 bgcolor=$forumcolorone><a href=topic.cgi?forum=$inforum&topic=$topicid target=_blank>$topicicon</a></td>
<td width=* class=dp bgColor=$forumcolortwo onmouseover="this.bgColor='$forumcolorone';" onmouseout="this.bgColor='$forumcolortwo';">&nbsp;<a href=view.cgi?forum=$inforum&topic=$topicid target=_blank>$posticon</a>&nbsp;<span id=forum>$topictitle$pagestoshow$topicdescription$admini</span></td>
<td align=center width=78 bgcolor=$forumcolorone>$startedby</td>$outputtemp<td width=193 bgcolor=$forumcolorone>&nbsp;$lastpostdate<font color=$fonthighlight> | </font>$lastposter</td></tr></table>
	    ~;
	    $pagestoshow = undef;
	    $threadpages = undef;
	    $topiccount++;
	}
        $output .= qq~
        </tr></table></td>
        </tr></table><SCRIPT>valignend()</SCRIPT></span>
        <table cellpadding=0 cellspacing=2 width=$tablewidth align=center>
	<tr height=4></tr>
        <tr>
        <td>$topicpages</td>
                   </tr></table>
            </tr>
            </table>
	    <br>
        ~;
}

sub UpdateNo { #R2
	my ($tid,$fid,$act)=@_;
	my ($no, $mn);
	my (@member_list,@topic_list);
	if (ref($tid) eq "ARRAY") {
	    @topic_list=@{$tid};
	} else {
	    @topic_list=();
	    $topic_list[0]=$tid;
	}

	foreach $tid(@topic_list){
		my $file = "$lbdir" . "forum$fid/$tid.pl";
		open (ENT, $file);
		my $in = <ENT>;
		close (ENT);
		my ($no, $topictitle, $no, $no, $no ,$no, $mn, $no, $no, $no, $no) = split(/\t/,$in);
		my $nametocheck = $mn;
		$nametocheck =~ s/ /\_/g;
		$nametocheck =~ tr/A-Z/a-z/;
		push(@member_list,$nametocheck);
        	&sendtoposter("$inmembername","$mn","","jinghua","$fid","$tid", "$topictitle","") if (($sendmanageinfo eq "yes")&&(lc($inmembername) ne lc($mn))&&($act eq "+"));
	}
	if($act eq "+") {
		foreach $mn(@member_list){
                &getmember("$mn","no");
                next if ($userregistered eq "no");
                $jhcount = 0 if ($jhcount eq ""); 
                $jhcount= int($jhcount); 
                $jhcount=$jhcount+1;
                &upmember($mn,$jhcount);
		}
	} else {
		foreach $mn(@member_list){
                &getmember("$mn","no");
                next if ($userregistered eq "no");
                $jhcount = 0 if ($jhcount eq ""); 
                $jhcount= int($jhcount); 
                $jhcount=$jhcount-1;
                &upmember($mn,$jhcount);
		}
	}
}

sub upmember {
    my ($nametocheck,$jhcount) = @_;    # �û�����������

    $nametocheck =~ s/ /\_/g;
    $nametocheck =~ tr/A-Z/a-z/;
    $nametocheck =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
    unlink ("${lbdir}cache/meminfo/$nametocheck.pl");
    unlink ("${lbdir}cache/myinfo/$nametocheck.pl");

    if (($nametocheck ne "")&&($jhcount ne "")) {
	my $namenumber = &getnamenumber($nametocheck);
	&checkmemfile($nametocheck,$namenumber);
        my $filetoopen = "${lbdir}$memdir/$namenumber/$nametocheck.cgi";
        if ((-e $filetoopen)&&($nametocheck !~ /^����/)) {
           &winlock($filetoopen) if (($OS_USED eq "Unix")||($OS_USED eq "Nt"));
	   if (open(FILE,">$filetoopen")) {
	        print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t\n";
		close(FILE);
	   }
	   &winunlock($filetoopen) if (($OS_USED eq "Unix")||($OS_USED eq "Nt"));
        }
    }
}
