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
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
$LBCGI::POST_MAX=500000;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
require "data/cityinfo.cgi";
require "cleanolddata.pl";
require "recooper.pl";
require "dopost.pl";

$|++;
$thisprog = "delpost.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

$addme=$query->param('addme');
if ($arrowavaupload ne "on") { undef $addme; }
for ('forum','topic','membername','password','action','postno',
     'notify','deletepost','inpost','checked','movetoid','leavemessage','posticon') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
$inpost = " " if ($inpost eq "");
$inforum       = $forum;
$intopic       = $topic;
$movetoid =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
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

$inpostno      = $postno;
@inpostno      = split(/ /,$inpostno); 
$inpostno      = ~ s/ //g; 
$indeletepost  = $deletepost;
$inleavemessage= $leavemessage;
$currenttime   = time;
$inposticon	= $posticon;

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
require "sendmanageinfo.pl" if ($sendmanageinfo eq "yes");
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

if (($inpostno) && ($inpostno !~ /^[0-9]+$/)) { &error("��ͨ����&�벻Ҫ�޸����ɵ� URL��"); }

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($inmembername eq "" || $inmembername eq "����" ) {
    $inmembername = "����";
} else {
    &getmember("$inmembername");
#    &getmember("$inmembername","no");
    &error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
     if ($inpassword ne $password) {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("��ͨ����&�������û���������������µ�¼��");
     }
}
&moderator("$inforum");
$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");
    &cleanolddata;
my %Mode = (
    'delete'      =>    \&deletethread,
    'movetopic'   =>    \&movetopic,
);
if ($Mode{$action}) { $Mode{$action}->(); }
elsif ($action eq "processedit" && $indeletepost eq "yes") { &deletepost;   }
elsif ($action eq "directdel") {&deletepost}
elsif ($action eq "postdeleteonce") {&postdeleteonce}
elsif ($action eq "unpostdeleteonce") {&unpostdeleteonce}
else { &error("��ͨ����&������ȷ�ķ�ʽ���ʱ�����"); }

&output("$boardname - ���⴦��",\$output);
exit;
    
sub deletethread {
    &mischeader("ɾ������");
    $cleartoedit = "no";
    if (($membercode eq "ad")  && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($membercode eq 'smo') && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($inmembmod eq "yes")  && ($membercode ne 'amo') && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    $alldeltopic = 0;

    if ($membercode ne "ad") { 
	    $trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
	    $trueipaddress = "no" if ($trueipaddress eq "" || $trueipaddress =~ m/a-z/i || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);
	    my $trueipaddress1 = $ENV{'HTTP_CLIENT_IP'};
	    $trueipaddress = $trueipaddress1 if ($trueipaddress1 ne "" && $trueipaddress1 !~ m/a-z/i && $trueipaddress1 !~ m/^192\.168\./ && $trueipaddress1 !~ m/^10\./);
        $maxdeloneday = 9 if (($maxdeloneday eq "")||($maxdeloneday <= 0));
        open(FILE,"${lbdir}data/baddel.cgi"); 
        my @delfile = <FILE>; 
        close(FILE); 
        my $delcount=0; 
        my $delcou=0; 
        my $totime=time-24*3600;
        foreach (@delfile){ 
	    chomp $_; 
	    (my $delname, my $no, my $noip, $no, $no ,my $notime) = split(/\t/,$_); 
	    if (lc($delname) eq lc($inmembername)){ 
	        if ($notime > $totime){ 
	            $delcount++; 
	        } 
	    } 
	    if ($noip eq $trueipaddress){ 
	        if ($notime > $totime){ 
	            $delcou++; 
	        }
	    }
        }
        if ($delcount > $maxdeloneday){ &error("ɾ������&�����ɾ������̫�࣬�����������"); } 
        if ($delcou > $maxdeloneday)  { &error("ɾ������&�����ɾ������̫�࣬�����������"); } 
        undef $delcount; 
        undef $delcou; 
    }

    if ($checked eq "yes"){ #1
        @intopic=split(/ /,$intopic);
        $alldeltopic=@intopic;
        &error("ɾ������&����ѡ����Ҫɾ�������⣡") if ($alldeltopic <= 0);
        foreach $intopic (@intopic) {#2
            $filetoopen = "${lbdir}forum$inforum/$intopic.thd.cgi";
            if (!(-e $filetoopen)) { $alldeltopic -- ; }
    	    else { #3
		open(FILE, "$filetoopen");
		@threads = <FILE>;
		close(FILE);

	    	($startedby, $topictitle, my $no, $no, $no ,$no, $no, $no, $no, $no) = split(/\t/,$threads[0]);
        	if ($arrowuserdel eq "on") {
            	    if ((lc($inmembername) eq lc($startedby)) && ($inpassword eq $password)) { $cleartoedit = "yes"; }
        	}
		unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }

        	if ($cleartoedit eq "no") { &error("ɾ������&�����Ǳ���̳̳���������Ҳ���Ǳ�����ķ����ߣ����������������"); }
        	else {#4
                    &sendtoposter("$inmembername","$startedby","","deletethread","$inforum","$intopic", "$topictitle","$inpost") if (($sendmanageinfo eq "yes")&&(lc($inmembername) ne lc($startedby)));
	  	    $nametocheck = $startedby;
	  	    $nametocheck =~ s/ /\_/g;
	  	    $nametocheck =~ tr/A-Z/a-z/;
	  	    $nametocheck =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;

		    my $namenumber = &getnamenumber($nametocheck);
		    &checkmemfile($nametocheck,$namenumber);

	  	    my $filetoopen = "${lbdir}$memdir/$namenumber/$nametocheck.cgi";
	  	    if (-e $filetoopen) {#6
	    		&winlock($filetoopen) if ($OS_USED eq "Nt");
	    		open(FILE,"$filetoopen");
	    		flock (FILE, 1) if ($OS_USED eq "Unix");
            		my $filedata = <FILE>;
            		close(FILE);
	    		chomp $filedata;
	    		(my $membername, my $password, my $membertitle, my $membercode, my $numberofposts, my $emailaddress, my $showemail, my $ipaddress, my $homepage, my $oicqnumber, my $icqnumber ,my $location ,my $interests, my $joineddate, my $lastpostdate, my $signature, my $timedifference, my $privateforums, my $useravatar, my $userflag, my $userxz, my $usersx, my $personalavatar, my $personalwidth, my $personalheight, my $rating, my $lastgone, my $visitno,my  $useradd04,my  $useradd02, my $mymoney, my $postdel, my $sex, my $education, my $marry, my $work, my $born, my $chatlevel, my $chattime, my $jhmp,my $jhcount, my $ebankdata, my $onlinetime,my $userquestion, my $awards, my $jifen, my $userface, my $soccerdata, my $useradd5 ) = split(/\t/,$filedata);
	  		if (($membername ne "")&&($password ne "")) {#7

	      my ($post1, $post2) = split(/\|/,$numberofposts);
	      $post1 ||= "0";
	      $post2 ||= "0";
	if ($jifen eq "") {
		$jifen = $post1 * $ttojf + $post2 * $rtojf - $postdel * $deltojf;
  }

	    		    open(FILE,">$filetoopen");
	    		    flock (FILE, 2) if ($OS_USED eq "Unix");
	    		    $lastgone=time;
	    		    if ($inleavemessage eq "yes") {
				$postdel++;
				$mymoney -= $forumdelmoney - $delmoney if ($forumdelmoney ne "");
				if ($forumdeljf ne "") { $jifen -= $forumdeljf; } else { $jifen -= $deltojf; }
			    }
	    		    print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t\n";
	    		    close(FILE);
	  		}#7
	    		&winunlock($filetoopen) if ($OS_USED eq "Nt");
			unlink ("${lbdir}cache/meminfo/$nametocheck.pl");
			unlink ("${lbdir}cache/myinfo/$nametocheck.pl");
	  	    }#6
		    $postcount = @threads;
        	    $postcount--;
		    $alldelpost=$postcount+$alldelpost;

        	    unlink ("${lbdir}forum$inforum/$intopic.pl");
        	    unlink ("${lbdir}forum$inforum/$intopic.thd.cgi");
        	    unlink ("${lbdir}forum$inforum/$intopic.poll.cgi");
        	    unlink ("${lbdir}forum$inforum/$intopic.mal.pl");
        	    unlink ("${lbdir}forum$inforum/rate$intopic.file.pl");
        	    unlink ("${lbdir}forum$inforum/rateip$intopic.file.pl");
        	    unlink ("${lbdir}FileCount/$inforum/$inforum\_$intopic.txt");
        	    unlink ("${lbdir}FileCount/$inforum/$inforum\_$intopic.cgi");
        	    unlink ("${lbdir}forum$inforum/$intopic.clk.pl");

		    opendir (DIRS, "${lbdir}$saledir");
		    my @files = readdir(DIRS);
		    closedir (DIRS);

		    my @files = grep(/^$inforum\_$intopic\_/i, @files);
		    foreach (@files) {
		        chomp $_;
		        unlink ("${lbdir}$saledir/$_");
    		    }

		    opendir (DIRS, "${imagesdir}$usrdir/$inforum");
		    my @files = readdir(DIRS);
		    closedir (DIRS);
		    
		    @files = grep(/^$inforum\_$intopic(\.|\_)/i, @files); 
		    foreach (@files) { 
			chomp $_; 
			unlink ("${imagesdir}$usrdir/$inforum/$_"); 
		    }
		    &delallupfiles($inforum,$intopic); ##�µ����Ӹ���ɾ��(cache��ʽ)
	        }#4
	    }#3
	}#2

        if ($alldeltopic > 5){
	    $trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
	    $trueipaddress = "no" if ($trueipaddress eq "" || $trueipaddress =~ m/a-z/i || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);
	    my $trueipaddress1 = $ENV{'HTTP_CLIENT_IP'};
	    $trueipaddress = $trueipaddress1 if ($trueipaddress1 ne "" && $trueipaddress1 !~ m/a-z/i && $trueipaddress1 !~ m/^192\.168\./ && $trueipaddress1 !~ m/^10\./);
	    my $thistime=time;
            if (open(FILE, ">>${lbdir}data/baddel.cgi")) {
                print FILE "$inmembername\t���벻��ʾ\t$ENV{'REMOTE_ADDR'}\t$trueipaddress\tɾ��$forumname $alldeltopic ������\t$thistime\t\n";
                close(FILE);
            }
            undef $thistime;
        }
        if ($inpost ne "") { $inpost = "<BR>ɾ�����ɣ�$inpost"; }
		if ($alldeltopic == 1)
		{
			$topictitle =~ s/^����������//;
			&addadminlog("ɾ������ <i>$topictitle</i><BR>���ߣ�$startedby$inpost");
		}
		else
		{
			&addadminlog("����ɾ������ $alldeltopic ƪ$inpost") if ($alldeltopic > 1);
		}

    if ($cleartoedit eq "no")  { &error("ɾ������&�����Ǳ���̳̳���������Ҳ���Ǳ�����ķ����ߣ����������������"); }
    if ($cleartoedit eq "yes") {
	$file = "$lbdir" . "boarddata/listno$inforum.cgi";
        &winlock($file) if ($OS_USED eq "Nt");
        open (LIST, "$file");
	flock (LIST, 1) if ($OS_USED eq "Unix");
        sysread(LIST, $listall,(stat(LIST))[7]);
        close (LIST);
	$listall =~ s/\r//isg;
	
	foreach (@intopic) {
	    chomp $_;
	    $listall =~ s/(^|\n)$_\n/$1/;
	}

        if (open (LIST, ">$file")) {
	    flock (LIST, 2) if ($OS_USED eq "Unix");
	    print LIST "$listall";
	    close (LIST);
	}
        &winunlock($file) if ($OS_USED eq "Nt");

	$file = "$lbdir" . "boarddata/listall$inforum.cgi";
        &winlock($file) if ($OS_USED eq "Nt");
        open (LIST, "$file");
	flock (LIST, 1) if ($OS_USED eq "Unix");
        sysread(LIST, $listall,(stat(LIST))[7]);
        close (LIST);
	$listall =~ s/\r//isg;
	
	foreach (@intopic) {
	    chomp $_;
	    $listall =~ s/(^|\n)$_\t.*?\n/$1/;
	}

        if (open (LIST, ">$file")) {
	    flock (LIST, 2) if ($OS_USED eq "Unix");
	    print LIST "$listall";
	    close (LIST);
	}
        &winunlock($file) if ($OS_USED eq "Nt");

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
	    ($tempno1, $tempno2, $no) = split (/\t/,$_);
	    next if (($tempno1 !~ /^[0-9]+$/)||($tempno2 !~ /^[0-9]+$/));
	    my $checkme=0;
	    $checkme = 1 if ($intopic eq $tempno2);
	    foreach $intopic (@intopic){
		if ($tempno2 eq $intopic) {
		    $checkme=1;
		}
	    }
	    unless (($tempno1 eq $inforum)&&($checkme eq 1)) {
		print FILE "$_\n"
	    }
	}
	close(FILE);
	}
	&winunlock($filetomakeopen) if ($OS_USED eq "Nt");

	$filetoopen = "$lbdir" . "boarddata/ontop$inforum.cgi";
	if (-e $filetoopen) {
	    open(FILE, "$filetoopen");
            @ontop = <FILE>;
            close(FILE);

            if (open(FILE, ">$filetoopen")) {
            flock(FILE, 2) if ($OS_USED eq "Unix");
	    foreach (@ontop) {
		chomp $_;
		my $checkme=0;
	        $checkme = 1 if ($intopic eq $_);
          	foreach $intopic (@intopic){
	    	    if ($_ eq $intopic) {
	      	        $checkme=1;
	            }
	        }
	        print FILE "$_\n" if ($checkme ==0);
	    }
            close(FILE);
            }
	}

	$filetoopen = "$lbdir" . "boarddata/absontop.cgi";
	if (-e $filetoopen) {
	    open(FILE, "$filetoopen");
            @toptopic = <FILE>;
            close(FILE);

            if (open(FILE, ">$filetoopen")) {
	        foreach (@toptopic) {
	            chomp $_;
                    next if ($_ eq "");
	            ($tempinforum,$tempintopic) = split (/\|/,$_);
	            unless (($tempinforum eq $inforum)&&($tempintopic eq $intopic)) {
	    	        print FILE "$_\n";
	            }
	        }
                close(FILE);
            }
	}

	$filetoopen = "${lbdir}boarddata/foruminfo$inforum.cgi";
	my $filetoopens = &lockfilename($filetoopen);
	if (!(-e "$filetoopens.lck")) {
            &winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

            open(FILE, "${lbdir}boarddata/listno$inforum.cgi");
            $topicid = <FILE>;
            close(FILE);
            chomp $topicid;
  	    require "rebuildlist.pl";
	    my $rr = &readthreadpl($inforum,$topicid);
	    (my $lastpostdate, my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $posticon, my $posttemp, my $addmetemp) = split (/\t/,$rr);

            open(FILE, "$filetoopen");
            ($no, $threads, $posts, $todayforumpost, $no) = split(/\t/,<FILE>);
            close(FILE);
            $posts = $posts - $alldelpost;
            $threads=$threads-$alldeltopic;
            $lastforumpostdate = "$lastpostdate\%\%\%$topicid\%\%\%$topictitle";
	    $lastposter = $startedby if ($lastposter eq "");
	    if (open(FILE, ">$filetoopen")) {
                print FILE "$lastforumpostdate\t$threads\t$posts\t$todayforumpost\t$lastposter\t\n";
        	close(FILE);
	        $posts = 0 if ($posts eq "");$threads = 0 if ($threads eq "");
	        open(FILE, ">${lbdir}boarddata/forumposts$inforum.pl");
	        print FILE "\$threads = $threads;\n\$posts = $posts;\n\$todayforumpost = \"$todayforumpost\";\n1;\n";
                close(FILE);
            }

            &winunlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	}
        else {
    	    unlink ("$filetoopens.lck") if ((-M "$filetoopens.lck") *86400 > 30);
	}


	$filetoopen = "$lbdir" . "boarddata/catontop$categoryplace.cgi";
	if (-e $filetoopen) {
	    open(FILE, "$filetoopen");
            @toptopic = <FILE>;
            close(FILE);

            if (open(FILE, ">$filetoopen")) {
	        foreach (@toptopic) {
	            chomp $_;
                    next if ($_ eq "");
	            ($tempinforum,$tempintopic) = split (/\|/,$_);
	            unless (($tempinforum eq $inforum)&&($tempintopic eq $intopic)) {
	    	        print FILE "$_\n";
	            }
	        }
                close(FILE);
            }
	}

        require "$lbdir" . "data/boardstats.cgi";

      $filetomake = "$lbdir" . "data/boardstats.cgi";
      my $filetoopens = &lockfilename($filetomake);
      if (!(-e "$filetoopens.lck")) {
        $totalthreads=$totalthreads-$alldeltopic;
        $totalposts = $totalposts - $alldelpost;
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
    }#1

opendir (CATDIR, "${lbdir}cache");
@dirdata = readdir(CATDIR);
closedir (CATDIR);
@dirdata1 = grep(/^plcache$inforum\_/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }
@dirdata1 = grep(/^forumstoptopic$inforum/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }
@dirdata1 = grep(/^forumstop$inforum/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }

if ($category =~ /childforum-[0-9]+/) {
    my $tempforumno = $category;
    $tempforumno =~ s/childforum-//;
    @dirdata1 = grep(/^forums$tempforumno/,@dirdata);
    foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }
}

        $output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>ɾ���ɹ�</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>���������<ul>
<li><a href="forums.cgi?forum=$inforum">������̳</a>
<li><a href="leobbs.cgi">������̳��ҳ</a>
</ul></tr></td></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
    } else {
        @intopic = $query -> param('topic');
        $alldeltopic=@intopic;
        $alldeltopic = 0 if ($intopic[0] eq 'action');
        &error("ɾ������&����ѡ����Ҫɾ�������⣡") if ($alldeltopic <= 0);
        if ($alldeltopic eq 1) {
            $filetoopen = "${lbdir}forum$inforum/$intopic.pl";
		open(FILE, "$filetoopen");
		$threads = <FILE>;
		close(FILE);
	    	($startedby, $topictitle, my $no, $no, $no ,$no, $no, $no, $no, $no) = split(/\t/,$threads);
	    	$topictitle =~ s/^����������//;
	    	$topictitle = qq~ɾ������"<a href=topic.cgi?forum=$inforum&topic=$intopic target=_blank>$topictitle</a>"~;
	} else { $topictitle = qq~����ɾ�� $alldeltopic ������~; }
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post" enctype="multipart/form-data">
<input type=hidden name="action" value="delete">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="@intopic">
<font color=$fontcolormisc><b>�����������û���������������ģʽ [$topictitle]</b></font></td></tr>
<tr><td bgcolor=$miscbackone colspan=2><font color=$fontcolormisc><b>�ò����ǲ�����ģ�����ϸ���ǣ�</font></td>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>ɾ�����ɣ�</font></td><td bgcolor=$miscbackone><input name="inpost" type=text size=50></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�Ƿ��������±�ɾ����</font></td>
<td bgcolor=$miscbackone><font color=$fontcolormisc><input type="radio" name="leavemessage" value="yes" checked>���㡡<input type="radio" name="leavemessage" value="no">������ </font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="�� ¼"></td></tr></form></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
} # end deletethread
sub deletepost {
    &mischeader("ɾ���ظ�");
  if ($checked eq "yes"){ #1
    $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
    if (-e $filetoopen) {
       &winlock($filetoopen) if ($OS_USED eq "Nt");
       open(FILE, "$filetoopen") or &error("ɾ��&������ⲻ���ڣ�");
       flock(FILE, 1) if ($OS_USED eq "Unix");
       @allthreads = <FILE>;
       close(FILE);
       &winunlock($filetoopen) if ($OS_USED eq "Nt");
    }else { unlink ("$lbdir" . "forum$inforum/$intopic.pl"); &error("ɾ��&������ⲻ���ڣ�"); }
    @threads=@allthreads;
    $tt=@threads;
    $postcountcheck = 0;
    $totalposts = @allthreads;
    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password))  { $cleartoedit = "yes";$checkcandelm="YES";}
    if (($membercode eq 'smo') && ($inpassword eq $password)) { $cleartoedit = "yes";$checkcandelm="YES";}
    if (($inmembmod eq "yes") && ($membercode ne 'amo') && ($inpassword eq $password))  { $cleartoedit = "yes";$checkcandelm="YES";}
	@newallthread=@allthreads;
	$threadscount=@allthreads;
	@inpostno=grep(/[0-9]+/,@inpostno);
	@oldinpostno=@inpostno;
	$delcount=@inpostno;
	&error("ɾ���ظ�&����ѡ����Ҫɾ���Ļظ���") if($delcount <= 0);
	$checkcandel=0;
	foreach $posttodelete (@inpostno){
	$posttodelete--;
	if ($posttodelete eq "0") { &error("ɾ���ظ�&����������ɾ���ظ��ģ�����ɾ�����⣡"); }
    ($startedby[$posttodelete], $topictitle) = split(/\t/,$allthreads[$posttodelete]);
    if ($arrowuserdel eq "on" && $checkcandelm ne "YES") {
    	if ((lc($inmembername) eq lc($startedby[$posttodelete])) && ($inpassword eq $password)) { $cleartoedit = "yes";$checkcandel++;
    	}else{ &error("ɾ���ظ�&����ԭ���ߡ���̳����Ա�����������������"); }
    }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
	
	(undef, undef, undef, undef, undef ,undef, $delpostES, undef) = split(/\t/, $newallthread[$posttodelete]); #·��
	$newallthread[$posttodelete]="";
	$checkaddon[$posttodelete]="YES";
	}
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
        if (($cleartoedit eq "no"||($checkcandel != $delcount && $checkcandelm ne "YES")) && $checked eq "yes") { &error("ɾ���ظ�&����ԭ���ߡ���̳����Ա�����������������"); }
        if ($cleartoedit eq "yes" && ($checkcandel == $delcount || $checkcandelm eq "YES")) {
        	$postdelnum = 0;
	  	foreach $posttodelete (@inpostno){
		    $startedby=$startedby[$posttodelete];
		    &sendtoposter("$inmembername","$startedby","","deletepost","$inforum","$intopic", "$topictitle","$inpost") if (($sendmanageinfo eq "yes")&&(lc($inmembername) ne lc($startedby)));
		    if ($inleavemessage eq "yes") {
			$postdelnum++;
			$mymoney1 -= $forumdelmoney - $delmoney if ($forumdelmoney ne "");
			if ($forumdeljf ne "") { $jifen1 -= $forumdeljf; } else { $jifen1 -= $deltojf; }
 		    }
		}
			$nametocheck = $startedby;
			$nametocheck =~ s/ /\_/g;
			$nametocheck =~ tr/A-Z/a-z/;
	  	        $nametocheck = &stripMETA($nametocheck);

			my $namenumber = &getnamenumber($nametocheck);
			&checkmemfile($nametocheck,$namenumber);

	  	        my $filetoopen = "${lbdir}$memdir/$namenumber/$nametocheck.cgi";
			if (-e $filetoopen) {
			&winlock($filetoopen) if ($OS_USED eq "Nt");
			open(FILE,"$filetoopen");
			flock (FILE, 1) if ($OS_USED eq "Unix");
			$filedata = <FILE>;
            		close(FILE);
			chomp($filedata);
			($membername, $password, $membertitle, $membercode, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber ,$location ,$interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime,$jhmp ,$jhcount, $ebankdata, $onlinetime,$userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5 ) = split(/\t/,$filedata);
			if (($membername ne "")&&($password ne "")) {

	      my ($post1, $post2) = split(/\|/,$numberofposts);
	      $post1 ||= "0";
	      $post2 ||= "0";
	if ($jifen eq "") {
		$jifen = $post1 * $ttojf + $post2 * $rtojf - $postdel * $deltojf;
  }

			open(FILE,">$filetoopen");
			flock (FILE, 2) if ($OS_USED eq "Unix");
			$lastgone=time;
			$postdel = $postdel + $postdelnum;
			$mymoney = $mymoney + $mymoney1;
			$jifen   = $jifen + $jifen1;
			print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t\n";
			close(FILE);
			}
	  		&winunlock($filetoopen) if ($OS_USED eq "Nt");
			unlink ("${lbdir}cache/meminfo/$nametocheck.pl");
			unlink ("${lbdir}cache/myinfo/$nametocheck.pl");
			}
        chomp @newallthread;
        @newallthread=grep(/^(.+?)$/,@newallthread);
        $newallthread=join("\n",@newallthread);
        $newallthread=~s/\n\n/\n/isg;
        chomp $newallthread;
        $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        if (open(FILE, ">$filetoopen")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$newallthread\n";
        close(FILE);
        }
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
        ($postermembername2, $topictitle2, $postipaddress2, $showemoticons2, $showsignature2 ,$postdate2, $post2, $posticon2) = split(/\t/, $newallthread[$#newallthread]);
        $postermembername2 = "" if ($#newallthread eq "0");
	$inposttemp = $post2;
	$inposttemp="(��)" if ($inposttemp=~/LBHIDDEN\[(.*?)\]LBHIDDEN/sg);
	$inposttemp="(��)" if ($inposttemp=~/LBSALE\[(.*?)\]LBSALE/sg);
        $inposttemp=&temppost($inposttemp);
        $inposttemp = &lbhz($inposttemp,50);

        $filetoopen = "${lbdir}forum$inforum/$intopic.pl";
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        if (open(FILE, "$filetoopen")) {
            flock(FILE, 1) if ($OS_USED eq "Unix");
            $linedata = <FILE>;
            close(FILE);
        }
	($topicno1,$topictitle1,$topicdescription,$threadstate,$threadposts,$threadviews,$startedby,$startedpostdate,$postermembername1,$postdate1,$posticon,$inposttemp1,$addmetemp1) = split(/\t/,$linedata);
	$threadposts -= $delcount;
	$newline1="$topicno1\t$topictitle1\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$postermembername2\t$postdate2\t$posticon\t$inposttemp\t$addmetemp1\t";
        if (open(FILE, ">$filetoopen")) {
            flock(FILE, 2) if ($OS_USED eq "Unix");
            print FILE "$newline1\n";
            close(FILE);
        }
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
	
##########�ϵĸ���ɾ�� ������Ϊ�˼���
       # unlink ("${lbdir}FileCount/$inforum/$inforum\_$intopic.pl"); #���ڲ���ɾ����
       $filetoopen = "${lbdir}FileCount/$inforum/$inforum\_$intopic.cgi";

#########�ֵܹ�����������Ϊ�˼��ݣ�������·�
       my $dirtoopen2 = "$imagesdir" . "$usrdir/$inforum";
       opendir (DIR, "$dirtoopen2");
       @dirdata = readdir(DIR);
       closedir (DIR);
       @oldinpostno=reverse sort @oldinpostno;
       @oldinpostnobak = @oldinpostno;
       
       foreach $pno(@oldinpostno){
       	   $pno--;
       	   @files=grep(/^$inforum\_$intopic\_$pno/,@dirdata);
       	   chomp @files;
       	   if($#files >= 0){
       	   $DTHack=~s/$inforum\_$intopic\_$pno\=$inforum\_$intopic\_$pno.(.+?)\=[0-9]+\n//s if (-e $filetoopen && $dispshowcount eq "yes" && $DTHack=~m/$inforum\_$intopic\_$pno/);
       	   	foreach $file(@files){
       	   unlink ("$dirtoopen2/$file");
       	   	}
       	   }
       	for(my $i=$pno+1;$i<$tt;$i++){
       	   @filetorename=grep(/^$inforum\_$intopic\_$i/,@dirdata);
       	   if($#filetorename >= 0){
       	   ($filename,$fileext)=split(/\./,$filetorename[0]);
       	   $ii=$i-1;
       	   rename ("${imagesdir}$usrdir/$inforum/$inforum\_$intopic\_$i.$fileext","${imagesdir}$usrdir/$inforum/$inforum\_$intopic\_$ii.$fileext");
       	   $DTHack=~s/$inforum\_$intopic\_$i/$inforum\_$intopic\_$ii/isg if (-e $filetoopen && $dispshowcount eq "yes" && $DTHack=~m/$inforum\_$intopic\_$i/);
       	   }
       	}
       }
###############�ϵĸ���ɾ��END
       &delupfiles(\$delpostES,$inforum,$intopic);      ###�µķ���BY·��

       my $dirtoopen2 = "${lbdir}$saledir";
       opendir (DIR, "$dirtoopen2");
       @dirdata = readdir(DIR);
       closedir (DIR);
       @oldinpostno = @oldinpostnobak;

       foreach $pno (@oldinpostno) {
       	  $pno--;
       	  unlink ("$dirtoopen2/$inforum\_$intopic\_$pno\.cgi") if (-e "$dirtoopen2/$inforum\_$intopic\_$pno\.cgi");
       	  for(my $i=$pno+1;$i<$tt;$i++){
       	      $ii=$i-1;
       	      rename ("${lbdir}$saledir/$inforum\_$intopic\_$i.cgi","${lbdir}$saledir/$inforum\_$intopic\_$ii.cgi") if (-e "${lbdir}$saledir/$inforum\_$intopic\_$i.cgi");
       	  }
       }
       
	$filetoopen = "${lbdir}boarddata/foruminfo$inforum.cgi";
	my $filetoopens = &lockfilename($filetoopen);
	if (!(-e "$filetoopens.lck")) {
            &winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

            open(FILE, "${lbdir}boarddata/listno$inforum.cgi");
            $topicid = <FILE>;
            close(FILE);
            chomp $topicid;
  	    require "rebuildlist.pl";
	    my $rr = &readthreadpl($inforum,$topicid);
	    (my $lastpostdate, my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $posticon, my $posttemp) = split (/\t/,$rr);

            open(FILE, "+<$filetoopen");
            ($no, $threads, $posts, $todayforumpost, $no) = split(/\t/,<FILE>);
            $posts = $posts - $delcount;
            $lastforumpostdate = "$lastpostdate\%\%\%$topicid\%\%\%$topictitle";
	    $lastposter = $startedby if ($lastposter eq "");
            seek(FILE,0,0);
            print FILE "$lastforumpostdate\t$threads\t$posts\t$todayforumpost\t$lastposter\t\n";
            close(FILE);
	    $posts = 0 if ($posts eq "");$threads = 0 if ($threads eq "");
	    open(FILE, ">${lbdir}boarddata/forumposts$inforum.pl");
	    print FILE "\$threads = $threads;\n\$posts = $posts;\n\$todayforumpost = \"$todayforumpost\";\n1;\n";
            close(FILE);

            &winunlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	}
        else {
    	    unlink ("$filetoopens.lck") if ((-M "$filetoopens.lck") *86400 > 30);
	}

      require "$lbdir" . "data/boardstats.cgi";

      $filetomake = "$lbdir" . "data/boardstats.cgi";
      my $filetoopens = &lockfilename($filetomake);
      if (!(-e "$filetoopens.lck")) {
        $totalposts-=$delcount;
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

       &mischeader("ɾ���ظ�");
        if ($inpost ne "") { $inpost = "<BR>ɾ�����ɣ�$inpost"; }
	&addadminlog("ɾ���ظ� $delcount ƪ$inpost", $intopic);

        if ($refreshurl == 1) {
	        $relocurl = "topic.cgi?forum=$inforum&topic=$intopic";
	}
	else {
               	$relocurl = "forums.cgi?forum=$inforum";
        }

opendir (CATDIR, "${lbdir}cache");
@dirdata = readdir(CATDIR);
closedir (CATDIR);
@dirdata1 = grep(/^plcache$inforum\_/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }
@dirdata1 = grep(/^forumstoptopic$inforum/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }
@dirdata1 = grep(/^forumstop$inforum/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }

            $output .= qq~
            <SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 width=100%>
            <tr>
            <td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>��ɾ�� <font color=$fonthighlight>$delcount</font> ƪ�ظ��������ˢ������ҳ��</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            ���������
            <ul>
            <li><a href="topic.cgi?forum=$inforum&topic=$intopic">��������</a>
            <li><a href="forums.cgi?forum=$inforum">������̳</a>
            <li><a href="leobbs.cgi">������̳��ҳ</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <SCRIPT>valignend()</SCRIPT>
             <meta http-equiv="refresh" content="3; url=$relocurl">
            ~;
            } # end if clear to edit
            else { &error("ɾ���ظ�&����ԭ���ߡ���̳����Ա��"); }

      } else {
	$inpostno = $postno;
	@inpostno = split(/ /,$inpostno); 
	$inpostno = @inpostno;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post" enctype="multipart/form-data">
<input type=hidden name="action" value="directdel">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<input type=hidden name="postno" value="$postno">
<font color=$fontcolormisc><b>�����������û���������������ģʽ [ɾ�� $inpostno ���ظ�]</b></font></td></tr>
<tr><td bgcolor=$miscbackone colspan=2><font color=$fontcolormisc><b>�ò����ǲ�����ģ�����ϸ���ǣ�</font></td>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>ɾ�����ɣ�</font></td><td bgcolor=$miscbackone><input name="inpost" type=text size=50></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�Ƿ��������±�ɾ����</font></td> 
<td bgcolor=$miscbackone><font color=$fontcolormisc><input type="radio" name="leavemessage" value="yes" checked>���㡡<input type="radio" name="leavemessage" value="no">������ </font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="�� ¼"></td></tr></form></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }

} # end subdelete

sub movetopic {
    &mischeader("�ƶ�����");
    @intopic=split(/ /,$intopic);
    $thismovetopic=@intopic;

    $cleartomove = "no";
    if (($membercode eq "ad")  && ($inpassword eq $password)) { $cleartomove = "yes"; }
    if (($membercode eq 'smo') && ($inpassword eq $password)) { $cleartomove = 'yes'; }
    if (($inmembmod eq "yes")  && ($membercode ne 'amo') && ($inpassword eq $password)) { $cleartomove = "yes"; }
    unless ($cleartomove eq "yes") { $cleartomove = "no"; }
    if ($cleartomove eq "no") { &error("�ƶ�����&������̳������������������������"); }

    if (($cleartomove eq "yes") && ($checked eq "yes") && ($movetoid)) {
        if ($movetoid == $inforum) { &error("�ƶ�����&��������ͬ����̳���ƶ����⣡"); }
        my $filetoopen = "${lbdir}forum$inforum/foruminfo.cgi";
        open(FILE, "$filetoopen");
        my $forums = <FILE>;
        close(FILE);
        (my $trash, $trash, $trash, $oldforumname, $trash) = split(/\t/,$forums);

        my $filetoopen = "${lbdir}forum$movetoid/foruminfo.cgi";
        open(FILE, "$filetoopen");
        my $forums = <FILE>;
        close(FILE);
        (my $trash, $trash, $trash, $newforumname, $trash, $trash, $trash, $trash, $trash, $nowstartnewthreads, $trash) = split(/\t/,$forums);

        if ($nowstartnewthreads eq "onlysub") {&error("�ƶ�&�Բ���Ŀ�����Ǵ�����̳���������������ӣ�"); }

        opendir (DIR, "${imagesdir}$usrdir/$inforum");
        @files = readdir(DIR);
        closedir (DIR);

        $inpostaddon = "<p>" if ($inpost ne "");
        if ($indeletepost eq "yes") {
            $moveinfoold = qq~�����ѱ�����Ա$inmembernameת������ <a href=forums.cgi?forum=$movetoid target=_self>$newforumname</a>~;
            $moveinfonew = qq~����ת���ԣ� <a href=forums.cgi?forum=$inforum target=_self>$oldforumname</a>~;
        }
        else { $moveinfonew = ""; $moveinfoold = ""; }
        
        my @inforumwrite;
        my @moveforumwrite;
        undef $newthreadnumber;
	my $movetopicnums = 0;
	foreach $intopic (@intopic) {
	    $intopic =~ s/\W//isg;
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

            $myinpost  = qq~***** ����ģʽ *****<p>$inpost$inpostaddon�������ǹ���Ա��<a href=forums.cgi?forum=$inforum>$oldforumname</a>ת�ƹ����ģ�~;
            $newinpost = qq~***** ����ģʽ *****<p>$inpost$inpostaddon<a href=topic.cgi?forum=$movetoid&topic=$newthreadnumber>�������ѱ�����Աת�ƣ���������鿴</a>~;
    
            open (ENT, "${lbdir}forum$inforum/$intopic.pl");
            $in = <ENT>;
            close (ENT);
            ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $lastinposticon,$inposttemp,$addmetemp) = split(/\t/,$in);
            $topictitle =~ s/����������//;
            &sendtoposter("$inmembername","$startedby","$newforumname","move","$inforum","$intopic", "$topictitle","") if(($sendmanageinfo eq "yes")&&(lc($inmembername) ne lc($startedby)));
	    $threadposts ++ if ($indeletepost eq "yes");

            $myinpost="$inmembername\t$topictitle\t$ENV{'REMOTE_ADDR'}\tyes\tyes\t$currenttime\t$myinpost\t$inposticon\t\n";#$topictitle�������

	    if ($moveinfonew ne "") {
	        $topicdescription = $moveinfonew;
	    }

	    $lastinposticon = $inposticon if ($inposticon ne "");

	    if ($indeletepost eq "yes") {
                $moveforumwrite = "$newthreadnumber\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$inmembername\t$currenttime\t$lastinposticon\t***** ����ģʽ *****\t$addmetemp\t";
	    }
	    else {
                $moveforumwrite = "$newthreadnumber\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$currenttime\t$lastinposticon\t$inposttemp\t$addmetemp\t";
	    }
            if (open(FILE, ">${lbdir}forum$movetoid/$newthreadnumber.pl")) {
                print FILE $moveforumwrite;
                close(FILE);
            }
            push (@moveforumwrite, "$newthreadnumber");
            
            $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
            &winlock($filetoopen) if ($OS_USED eq "Nt");
            open(FILE, "$filetoopen");
            flock(FILE, 1) if ($OS_USED eq "Unix");
            @oldforummessages = <FILE>;
            close(FILE);
            &winunlock($filetoopen) if ($OS_USED eq "Nt");
	    $movetopicnums++;

            $filetomake = "$lbdir" . "forum$movetoid/$newthreadnumber.thd.cgi";
            if (open(FILE, ">$filetomake")) {
                foreach (@oldforummessages) {
                    chomp $_;
                    print FILE "$_\n" if ($_ ne "");
                }
                print FILE "$myinpost" if ($indeletepost eq "yes");
                close(FILE);
            }

            copy("${lbdir}forum$inforum/$intopic.mal.pl",       "${lbdir}forum$movetoid/$newthreadnumber.mal.pl")        if (-e "${lbdir}forum$inforum/$intopic.mal.pl");
   	    copy("${lbdir}forum$inforum/$intopic.poll.cgi",     "${lbdir}forum$movetoid/$newthreadnumber.poll.cgi")      if (-e "${lbdir}forum$inforum/$intopic.poll.cgi");
   	    copy("${lbdir}forum$inforum/rate$intopic.file.pl",  "${lbdir}forum$movetoid/rate$newthreadnumber.file.pl")   if (-e "${lbdir}forum$inforum/rate$intopic.file.pl");
   	    copy("${lbdir}forum$inforum/rateip$intopic.file.pl","${lbdir}forum$movetoid/rateip$newthreadnumber.file.pl") if (-e "${lbdir}forum$inforum/rateip$intopic.file.pl");

####�ɵķ�ʽ
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
#####�ɵķ�ʽ
            &moveallupfiles($inforum,$intopic,$movetoid,$newthreadnumber,$inleavemessage); #�µķ�ʽ

            if (open(FILE, ">${lbdir}boarddata/lastnum$movetoid.cgi")) {
                print FILE $newthreadnumber;
                close(FILE);
	    }

   $OldHackDetail="";
   $NewHackDetail="";

   if (open(HACK, "${lbdir}FileCount/$inforum/$inforum\_$intopic.cgi")) {
			@AllHackDetail = <HACK>;
			close(HACK);
			open(NHACK, ">${lbdir}FileCount/$movetoid/$movetoid\_$newthreadnumber.cgi");
			foreach $HackDetail(@AllHackDetail){
				chomp $HackDetail;
				($ThisHackName,$ThisFileName,$ThisHackDT)=split(/\=/,$HackDetail);
					($hackforumno,$hacktopicno,$hackreplyno)=split(/\_/,$ThisHackName);
					($filename,$fileext)=split(/\./,$ThisFileName);
					($fileforumno,$filetopicno,$filereplyno)=split(/\_/,$filename);
					if($filereplyno){$ReplyNo="\_$filereplyno";}else{$ReplyNo="";}
				$NewHackName="$movetoid\_$newthreadnumber\_$hackreplyno";
				$NewFileName="$movetoid\_$newthreadnumber$ReplyNo\.$fileext";
				print NHACK "$NewHackName\=$NewFileName\=$ThisHackDT\n";
				}
			close(NHACK);
   }

#### �����������ļ�

            if ($inleavemessage eq "yes") { # ����ԭ�������ӣ�����ԭ�������������һ������
                $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
		if (-e $filetoopen) {
                    &winlock($filetoopen) if ($OS_USED eq "Nt");
                    open(FILE, "$filetoopen");
                    flock(FILE, 1) if ($OS_USED eq "Unix");
                    @allmessages = <FILE>;
                    close(FILE);

                    if (open(FILE, ">$filetoopen")) {
                        flock(FILE, 2) if ($OS_USED eq "Unix");
                        foreach (@allmessages) {
                            chomp $_;
                            print FILE "$_\n";
                        }
                        print FILE "$inmembername\t$topictitle\t$ENV{'REMOTE_ADDR'}\tyes\tyes\t$currenttime\t$newinpost\t$inposticon\t\n" if ($indeletepost eq "yes");
                        close(FILE);
                    }
	            &winunlock($filetoopen) if ($OS_USED eq "Nt");

                    my $file = "$lbdir" . "forum$inforum/$intopic.pl";
                    open (ENT, $file);
                    $in = <ENT>;
                    close (ENT);
                    chomp $in;
                    ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $lastinposticon,$inposttemp,$addmetemp) = split(/\t/,$in);
                    $threadposts ++ if ($indeletepost eq "yes");
		    if (($threadstate eq "poll")||($threadstate eq "pollclosed")) { $threadstate = "pollclosed"; } else { $threadstate = "closed"; }
                    if (open(FILE, ">$file")) {
                        $inforumwrite = "$intopic\t$topictitle\t$moveinfoold\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$inmembername\t$currenttime\t$lastinposticon\t$inposttemp\t$addmetemp\t";
                        print FILE $inforumwrite;
                        close(FILE);
                    }
                }
            }
	    else {            

        	  unlink ("${lbdir}forum$inforum/$intopic.pl");
        	  unlink ("${lbdir}forum$inforum/$intopic.thd.cgi");
        	  unlink ("${lbdir}forum$inforum/$intopic.poll.cgi");
        	  unlink ("${lbdir}forum$inforum/$intopic.mal.pl");
        	  unlink ("${lbdir}forum$inforum/rate$intopic.file.pl");
        	  unlink ("${lbdir}forum$inforum/rateip$intopic.file.pl");
        	  unlink ("${lbdir}FileCount/$inforum/$inforum\_$intopic.txt");
        	  unlink ("${lbdir}FileCount/$inforum/$inforum\_$intopic.cgi");
        	  unlink ("${lbdir}FileCount/$inforum/$inforum\_$intopic.pl");
        	  unlink ("${lbdir}forum$inforum/$intopic.clk.pl");

		  opendir (DIRS, "${imagesdir}$usrdir/$inforum");
		  my @files = readdir(DIRS);
		  closedir (DIRS);
		  @files = grep(/^$inforum\_$intopic(\.|\_)/i, @files); 
		  foreach (@files) { 
			chomp $_; 
			unlink ("${imagesdir}$usrdir/$inforum/$_"); 
		  }
                    push (@inforumwrite, "$intopic");
	    }
        }

	if ($inleavemessage eq "no") {  #ɾ��ԭ����̳�����ӣ��������������е�����
	    $filetomakeopen = "$lbdir" . "data/recentpost.cgi";
	    open(FILE, "$filetomakeopen");
	    @recentposts=<FILE>;
	    close(FILE);
	    
	    if (open (FILE, ">$filetomakeopen")) {
	        foreach (@recentposts) {
	            chomp $_;
	            ($inforumtemp, $intopictemp, $tempno3, $tempno4, $tempno5, $tempno6) = split (/\t/,$_);
	            next if (($inforumtemp !~ /^[0-9]+$/)||($intopictemp !~ /^[0-9]+$/));
	            if ($inforumtemp eq $inforum) {
	                my $checkme=0;
	                foreach $intopic (@intopic){
		            if ($intopictemp eq $intopic) {
		                $checkme=1;
		                last;
		            }
	                }
	                if ($checkme eq 0) {
		            print FILE "$_\n";
		        }
	                else {
	    	            print FILE "$movetoid\t$newthreadnumber\t$tempno3\t$tempno4\t$tempno5\t$tempno6\t\n";
	                }
	            }
	            else {
	    	        print FILE "$_\n";
	            }
	        }
	        close(FILE);
	    }
	}

    if ($inleavemessage eq "no") {

	$file = "$lbdir" . "boarddata/listno$inforum.cgi";
        &winlock($file) if ($OS_USED eq "Nt");
        open (LIST, "$file");
	flock (LIST, 1) if ($OS_USED eq "Unix");
        sysread(LIST, $listall,(stat(LIST))[7]);
        close (LIST);
	$listall =~ s/\r//isg;
	
            foreach (@inforumwrite) {
                chomp $_;
	        $listall =~ s/(^|\n)$_\n/$1/;
	    }

        if (open (LIST, ">$file")) {
	    flock (LIST, 2) if ($OS_USED eq "Unix");
	    print LIST "$listall";
	    close (LIST);
	}
        &winunlock($file) if ($OS_USED eq "Nt");

	$file = "$lbdir" . "boarddata/listall$inforum.cgi";
        &winlock($file) if ($OS_USED eq "Nt");
        open (LIST, "$file");
	flock (LIST, 1) if ($OS_USED eq "Unix");
        sysread(LIST, $listall,(stat(LIST))[7]);
        close (LIST);
	$listall =~ s/\r//isg;

            foreach (@inforumwrite) {
                chomp $_;
	        $listall =~ s/(^|\n)$_\t.*?\n/$1/;
	    }

        if (open (LIST, ">$file")) {
	    flock (LIST, 2) if ($OS_USED eq "Unix");
	    print LIST "$listall";
	    close (LIST);
	}
        &winunlock($file) if ($OS_USED eq "Nt");
    }
	
	undef @inforumwrite;
	undef @listall;
	
        $file = "$lbdir" . "boarddata/listno$movetoid.cgi";
        &winlock($file) if (($OS_USED eq "Unix")||($OS_USED eq "Nt"));
        open (LIST, "$file");
	flock (LIST, 1) if ($OS_USED eq "Unix");
        sysread(LIST, $listall,(stat(LIST))[7]);
        close (LIST);
	$listall =~ s/\r//isg;

        if (open (LIST, ">$file")) {
            flock (LIST, 2) if ($OS_USED eq "Unix");
            foreach (@moveforumwrite) {
                chomp $_;
	        print LIST "$_\n" if ($_ ne "");
	    }
	    print LIST "$listall\n" if ($listall ne "");
            close (LIST);
        }
        &winunlock($file) if (($OS_USED eq "Unix")||($OS_USED eq "Nt"));

		if ($movetopicnums == 1)
		{
			$topictitle =~ s/^����������//;
			&addadminlog("�ƶ����� <i>$topictitle</i> <BR>�� $newforumname", $intopic);
		}
		else
		{
			&addadminlog("�����ƶ����� $movetopicnums ƪ�� $newforumname") if ($movetopicnums > 1);
		}

opendir (CATDIR, "${lbdir}cache");
@dirdata = readdir(CATDIR);
closedir (CATDIR);
@dirdata1 = grep(/^plcache$inforum\_/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }
unlink ("${lbdir}cache/forumstoptopic$inforum");
unlink ("${lbdir}cache/forumstop$inforum");

@dirdata1 = grep(/^plcache$movetoid\_/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }
unlink ("${lbdir}cache/forumstoptopic$movetoid");
unlink ("${lbdir}cache/forumstop$movetoid");

	undef @moveforumwrite;
	undef @listall;
        $relocurl = "forums.cgi?forum=$inforum";
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>�����Ѿ��ƶ������ƶ����� <font color=$fonthighlight>$movetopicnums</font> ƪ��</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>���������<ul>
<li><a href="forums.cgi?forum=$inforum">����ԭ��̳</a>
<li><a href="forums.cgi?forum=$movetoid">��������̳</a>
<li><a href="leobbs.cgi">������̳��ҳ</a>
</ul></tr></td></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=$relocurl">
~;
    $checked = "no";
    }
    else {

        $filetoopen = "$lbdir" . "data/allforums.cgi";
        open(FILE, "$filetoopen");
#        flock(FILE, 1) if ($OS_USED eq "Unix");
        @forums = <FILE>;
        close(FILE);

        $jumphtml .= "<option value=\"\">ѡ��һ����̳\n</option>";
        $a=0;
        foreach $forum (@forums) {
	    $a  = sprintf("%09d",$a);
            chomp $forum;
	    next if (length("$forum") < 30);
            ($movetoforumid, $category, $categoryplace, $forumname, $forumdescription, $noneed ,$noneed ,$noneed ,$noneed, $nowstartnewthreads ,$noneed ,$noneed, $noneed, $noneed, $noneed, $miscad2, $noneed,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/,$forum);
    	    next if ($movetoforumid !~ /^[0-9]+$/);
    	    next if ($categoryplace !~ /^[0-9]+$/);
    	    next if ($nowstartnewthreads eq "onlysub");

	    $categoryplace  = sprintf("%09d",$categoryplace);
            $rearrange = ("$categoryplace\t$a\t$category\t$forumname\t$forumdescription\t$movetoforumid\t$forumgraphic\t$miscad2\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$fgwidth\t$fgheight\t$miscad4\t$todayforumpost\t$miscad5\t");
            push (@rearrangedforums, $rearrange);
            $a++;
        }
        @finalsortedforums = sort (@rearrangedforums);
        foreach $sortedforums (@finalsortedforums) {
            ($categoryplace,my $a, $category, $forumname, $forumdescription, $movetoforumid, $forumgraphic, $miscad2, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/,$sortedforums);
	    $categoryplace  = sprintf("%01d",$categoryplace);

            $child=($category =~/^childforum-[0-9]+/)?"��|":"";
            if ($categoryplace ne $lastcategoryplace) {
                $jumphtml .= "<option value=\"\" style=background-color:$titlecolor>��$category\n</option>";
                $jumphtml .= "<option value=\"$movetoforumid\">$child��|- $forumname\n</option>";
            }
            else {
                $jumphtml .= "<option value=\"$movetoforumid\">$child��|- $forumname\n</option>";
            }
            $lastcategoryplace = $categoryplace;
        }
        undef @intopic;
        @intopic = $query -> param('topic');
	$intopic = @intopic;
        $intopic = 0 if ($intopic[0] eq 'action');
        &error("ɾ������&����ѡ����Ҫ�ƶ������⣡") if ($intopic <= 0);

        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center colspan=2>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="movetopic">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="@intopic">
<font color=$fontcolormisc><b>�����������û���������������ģʽ [�ƶ� $intopic ������]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
<b>�ƶ�ѡ��</td>
<td bgcolor=$miscbackone><font color=$fontcolormisc>
<input name="leavemessage" type="radio" value="yes"> �ƶ�������һ���Ѿ�������������ԭ��̳<br><input name="leavemessage" type="radio" value="no" checked> �ƶ������������ԭ��̳��ɾ��<br><input name="deletepost" type="checkbox" value="yes" checked> ����������ʾת��������</font>
</td></tr>
<tr><td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>��ǰ����</b><br><li>���������ӵ�ǰ��<BR></font></td>
<td bgcolor=$miscbackone valign=top>
~;

        open (FILE, "${lbdir}data/lbpost.cgi");
        my @posticondata = <FILE>;
        close (FILE);
        chomp @posticondata;

        $tempiconnum=1;
#       $tempselect = "checked";
        foreach $picture (@posticondata) {
            $posticonname = $picture;
            $posticonname =~ s/\.gif$//ig;
            if ($tempiconnum > 12) {
    	        $tempiconnum = 1;
    	        $output .= qq~<BR>~;
            }
            if ($picture eq $posticon) {$tempselect = "checked";} else {$tempselect = "";}
            $output .= qq~<input type=radio value="$picture" name="posticon" $tempselect><img src="$imagesurl/posticons/$picture" $defaultsmilewidth $defaultsmileheight border=0>&nbsp;~;
            $tempiconnum ++;
#           $tempselect = "";
        }
        $output .= qq~</td></tr><tr><td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>��Ϣ��</b><p>
����ǿ�ѡ�ģ���������һЩ˵����Ϣ��<p> �ƶ����Ŀ���ַ���Զ������������С�</font></td>
<td bgcolor=$miscbackone><textarea cols=80 rows=9 wrap="soft" name="inpost"></textarea></td></tr>
<tr><td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>ת������</b></font></td>
<td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><select name="movetoid">$jumphtml</select></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="�� ��"></td></tr></form></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}

sub postdeleteonce {
    &mischeader("��������");
  if ($checked eq "yes") { #1
    $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
    if (-e $filetoopen) {
       &winlock($filetoopen) if ($OS_USED eq "Nt");
       open(FILE, "$filetoopen") or &error("��������&������ⲻ���ڣ�");
       flock(FILE, 1) if ($OS_USED eq "Unix");
       @allthreads = <FILE>;
       close(FILE);
       &winunlock($filetoopen) if ($OS_USED eq "Nt");
    }else { unlink ("$lbdir" . "forum$inforum/$intopic.pl"); &error("��������&������ⲻ���ڣ�"); }
    chomp @allthreads;
    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password))  { $cleartoedit = "yes";}
    if (($membercode eq 'smo') && ($inpassword eq $password)) { $cleartoedit = "yes";}
    if (($inmembmod eq "yes") && ($membercode ne 'amo') && ($inpassword eq $password))  { $cleartoedit = "yes";}
	$allthreads=@allthreads;
	$allthreads ++;
	&error("��������&�����Ӳ����ڣ�") if($postno > $allthreads);
	$inpostnotemp = $postno;
	$inpostnotemp --;
        ($postermembername1,$topictitle1,$postipaddress1,$inshowemoticons1,$inshowsignature1,$postdate1,$inpost1,$inposticon1,$water1) = split(/\t/,$allthreads[$inpostnotemp]);

        unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
        if ($cleartoedit eq "yes") {

	    &sendtoposter("$inmembername","$postermembername1","","postdeleteonce","$inforum","$intopic", "$topictitle1","$inpost") if (($sendmanageinfo eq "yes")&&(lc($inmembername) ne lc($postermembername1)));
	$inpost1 =~ s/\[POSTISDELETE=(.+?)\]//;
	$inpost1 = qq~[POSTISDELETE=$inpost]$inpost1~;
        $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        if (open(FILE, ">$filetoopen")) {
            flock(FILE, 2) if ($OS_USED eq "Unix");
            $postcountcheck = 0;
            foreach $postline (@allthreads) {
                chomp $postline;
                if ($postcountcheck eq $inpostnotemp) {
                    print FILE "$postermembername1\t$topictitle1\t$postipaddress1\t$inshowemoticons1\t$inshowsignature1\t$postdate1\t$inpost1\t$inposticon1\t$water1\n";
                }
                else {
                    print FILE "$allthreads[$postcountcheck]\n";
                }
                $postcountcheck++;
            }
            close(FILE);
        }
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
$allthreads --;
$inpostnotemp ++;
if ($inpostnotemp eq $allthreads) {
   my $file = "$lbdir" . "forum$inforum/$intopic.pl";
   open (ENT, $file);
   $in = <ENT>;
   close (ENT);
   chomp $in;
   ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $lastinposticon,$inposttemp,$addmetemp) = split(/\t/,$in);
   
   
   open (ENT, ">$file");
   print ENT "$topicid\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$lastinposticon\t�˻ظ��Ѿ�������\t$addmetemp";
   close (ENT);

for(my $iii=0;$iii<=4;$iii++) {
    my $jjj = $iii * $maxthreads;
    unlink ("${lbdir}cache/plcache$inforum\_$jjj.pl");
}

}

        if ($inpost ne " ") { $inpost = "<BR>�������ɣ�$inpost"; }
	&addadminlog("������������$inpost", $intopic);

        if ($refreshurl == 1) {
	        $relocurl = "topic.cgi?forum=$inforum&topic=$intopic";
	}
	else {
               	$relocurl = "forums.cgi?forum=$inforum";
        }

            $output .= qq~
            <SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 width=100%>
            <tr>
            <td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>��ƪ���ӻظ��Ѿ�����������</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            ���������
            <ul>
            <li><a href="topic.cgi?forum=$inforum&topic=$intopic">��������</a>
            <li><a href="forums.cgi?forum=$inforum">������̳</a>
            <li><a href="leobbs.cgi">������̳��ҳ</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <SCRIPT>valignend()</SCRIPT>
             <meta http-equiv="refresh" content="3; url=$relocurl">
            ~;
            } # end if clear to edit
            else { &error("��������&��������̳����Ա�����������������"); }

      } else {
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post" enctype="multipart/form-data">
<input type=hidden name="action" value="postdeleteonce">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<input type=hidden name="postno" value="$postno">
<font color=$fontcolormisc><b>�����������û���������������ģʽ [��������]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�������ɣ�</font></td><td bgcolor=$miscbackone><input name="inpost" type=text size=50></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="�� ¼"></td></tr></form></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }

} # end subdelete

sub unpostdeleteonce {
    &mischeader("ȡ����������");
  if ($checked eq "yes") { #1
    $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
    if (-e $filetoopen) {
       &winlock($filetoopen) if ($OS_USED eq "Nt");
       open(FILE, "$filetoopen") or &error("ȡ����������&������ⲻ���ڣ�");
       flock(FILE, 1) if ($OS_USED eq "Unix");
       @allthreads = <FILE>;
       close(FILE);
       &winunlock($filetoopen) if ($OS_USED eq "Nt");
    }else { unlink ("$lbdir" . "forum$inforum/$intopic.pl"); &error("ȡ����������&������ⲻ���ڣ�"); }
    chomp @allthreads;
    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password))  { $cleartoedit = "yes";}
    if (($membercode eq 'smo') && ($inpassword eq $password)) { $cleartoedit = "yes";}
    if (($inmembmod eq "yes") && ($membercode ne 'amo') && ($inpassword eq $password))  { $cleartoedit = "yes";}
	$allthreads=@allthreads;
	$allthreads ++;
	&error("��������&�����Ӳ����ڣ�") if($postno > $allthreads);
	$inpostnotemp = $postno;
	$inpostnotemp --;
        ($postermembername1,$topictitle1,$postipaddress1,$inshowemoticons1,$inshowsignature1,$postdate1,$inpost1,$inposticon1,$water1) = split(/\t/,$allthreads[$inpostnotemp]);

        unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
        if ($cleartoedit eq "yes") {

	    &sendtoposter("$inmembername","$postermembername1","","unpostdeleteonce","$inforum","$intopic", "$topictitle1","$inpost") if (($sendmanageinfo eq "yes")&&(lc($inmembername) ne lc($postermembername1)));
	$inpost1 =~ s/\[POSTISDELETE=(.+?)\]//;
        $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        if (open(FILE, ">$filetoopen")) {
            flock(FILE, 2) if ($OS_USED eq "Unix");
            $postcountcheck = 0;
            foreach $postline (@allthreads) {
                chomp $postline;
                if ($postcountcheck eq $inpostnotemp) {
                    print FILE "$postermembername1\t$topictitle1\t$postipaddress1\t$inshowemoticons1\t$inshowsignature1\t$postdate1\t$inpost1\t$inposticon1\t$water1\n";
                }
                else {
                    print FILE "$allthreads[$postcountcheck]\n";
                }
                $postcountcheck++;
            }
            close(FILE);
        }
        &winunlock($filetoopen) if ($OS_USED eq "Nt");

        if ($inpost ne " ") { $inpost = "<BR>ȡ�����ɣ�$inpost"; }
	&addadminlog("ȡ��������������$inpost", $intopic);

        if ($refreshurl == 1) {
	        $relocurl = "topic.cgi?forum=$inforum&topic=$intopic";
	}
	else {
               	$relocurl = "forums.cgi?forum=$inforum";
        }

            $output .= qq~
            <SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 width=100%>
            <tr>
            <td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>��ƪ���ӻظ����������Ѿ���ȡ��</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            ���������
            <ul>
            <li><a href="topic.cgi?forum=$inforum&topic=$intopic">��������</a>
            <li><a href="forums.cgi?forum=$inforum">������̳</a>
            <li><a href="leobbs.cgi">������̳��ҳ</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <SCRIPT>valignend()</SCRIPT>
             <meta http-equiv="refresh" content="3; url=$relocurl">
            ~;
            } # end if clear to edit
            else { &error("ȡ����������&��������̳����Ա�����������������"); }

      } else {
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post" enctype="multipart/form-data">
<input type=hidden name="action" value="unpostdeleteonce">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<input type=hidden name="postno" value="$postno">
<font color=$fontcolormisc><b>�����������û���������������ģʽ [ȡ����������]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>ȡ�����ɣ�</font></td><td bgcolor=$miscbackone><input name="inpost" type=text size=50></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="�� ¼"></td></tr></form></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }

} # end subdelete
