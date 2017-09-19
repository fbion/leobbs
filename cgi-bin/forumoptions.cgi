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
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
require "rebuildlist.pl";
require "recooper.pl";
require "dopost.pl";

$|++;
$thisprog = "forumoptions.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

$checked        = $query -> param('checked');
$inforum        = $query -> param('forum');
$intopic        = $query -> param('topic');
$action         = $query -> param('action');
$admin          = $query -> param('admin');
$prunedays      = $query -> param('prunedays');
$inmembername   = $query -> param('membername');
$inpassword     = $query -> param('password');
$inaddline      = $query -> param('addline');
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$movetoid       = $query -> param('movetoid');
$action         = &stripMETA("$action");

&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum) && ($inforum !~ /^[0-9]+$/));
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($movetoid) && ($movetoid !~ /^[0-9]+$/));
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }
$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
if (($inforum  !~ m|([0-9\G]+$)|g) or (!$inforum))  { &error("��ͨ����&�벻Ҫ�޸����ɵ� URL��"); }
if (($prunedays) && ($prunedays !~ /^[0-9]+$/)) { &error("��ͨ����&�벻Ҫ�޸����ɵ� URL��"); }
if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie"); }
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

&getoneforum("$inforum");

if ($action eq "prune") {
    $cleartoedit = "no";
    &mischeader("��������");
	if ($inpassword eq $password) {
		$pwok = "���벻��ʾ";
	}
	else {
		$pwok = $inpassword;
	}
	$trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
	$trueipaddress = "no" if ($trueipaddress eq "" || $trueipaddress =~ m/a-z/i || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);
	my $trueipaddress1 = $ENV{'HTTP_CLIENT_IP'};
	$trueipaddress = $trueipaddress1 if ($trueipaddress1 ne "" && $trueipaddress1 !~ m/a-z/i && $trueipaddress1 !~ m/^192\.168\./ && $trueipaddress1 !~ m/^10\./);
	my $thistime=time;
   if($admin eq 'delete'){
	$filetomake = "$lbdir" . "data/baddel.cgi";

    $maxdeloneday = 9 if (($maxdeloneday eq "")||($maxdeloneday <= 0));
    if ($membercode ne "ad"){ 
      open(FILE,"$filetomake"); 
      my @delfile = <FILE>; 
      close(FILE); 
      my $delcount=0; 
      my $delcou=0; 
      my $totime=time-86400; 
      foreach (@delfile){ 
	chomp($_); 
	(my $delname, my $no, my $noip, $no, $no ,my $notime) = split(/\t/,$_); 
	if (lc($delname) eq lc($inmembername)){ 
	  if ($notime > $totime){ 
	    $delcount++; 
	  } 
	} 
	if ($noip eq "$ENV{'REMOTE_ADDR'}"){ 
	  if ($notime > $totime){ 
	    $delcou++; 
	  }
	}
      }
      if ($delcount > $maxdeloneday){&error("ɾ������&�����ɾ������̫�࣬�����������");} 
      if ($delcou > $maxdeloneday)  {&error("ɾ������&�����ɾ������̫�࣬�����������");} 
      undef $delcount; 
      undef $delcou; 
    }
    if (open(FILE, ">>$filetomake")) {
    print FILE "$inmembername\t$pwok\t$ENV{'REMOTE_ADDR'}\t$trueipaddress\t����ɾ��$forumname $prunedays��ǰ������\t$thistime\t\n";
    close(FILE);
    }
	} elsif ($admin eq 'move') {
	$filetomake = "$lbdir" . "data/badmove.cgi";
    $maxmoveoneday = 9 if (($maxmoveoneday eq "")||($maxmoveoneday <= 0));
    if ($membercode ne "ad"){ 
      open(FILE,"$filetomake"); 
      my @movefile = <FILE>; 
      close(FILE); 
      my $movecount=0; 
      my $movecou=0; 
      my $totime=time-86400; 
      foreach (@movefile){ 
	chomp $_; 
	(my $movename, my $no, my $noip, $no, $no ,my $notime) = split(/\t/,$_); 
	if (lc($movename) eq lc($inmembername)){ 
	  if ($notime > $totime){ 
	    $movecount++; 
	  } 
	} 
	if ($noip eq "$ENV{'REMOTE_ADDR'}"){ 
	  if ($notime > $totime){ 
	    $movecou++; 
	  }
	}
      }
      if ($movecount > $maxmoveoneday){&error("�ƶ�����&������ƶ�����̫�࣬�����������");} 
      if ($movecou > $maxmoveoneday)  {&error("�ƶ�����&������ƶ�����̫�࣬�����������");} 
      undef $movecount; 
      undef $movecou; 
    }
    if (open(FILE, ">>$filetomake")) {
    print FILE "$inmembername\t$pwok\t$ENV{'REMOTE_ADDR'}\t$trueipaddress\t�����ƶ�$forumname $prunedays��ǰ������\t$thistime\t\n";
    close(FILE);
    }
    }
	undef $thistime;

    if ((($membercode eq "ad") ||($membercode eq 'smo'))&& ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($inmembmod eq "yes") && ($membercode ne 'amo') && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
        if ($cleartoedit eq "no" && $checked eq "yes") {&error("ʹ����������&�����Ǳ���̳̳��������Ա�������������������");  }
        if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        if ($prunedays < 20) {  &error("ʹ����������&ָ�����������Ҫ���� 20 ��"); }

       if($admin eq 'delete'){

if (-e "${lbdir}boarddata/jinghua$inforum.cgi") {
    open(FILE, "${lbdir}boarddata/jinghua$inforum.cgi");
    my @jhdatas = <FILE>;
    close(FILE);
    $jhdata = join("\_",@jhdatas);
    $jhdata = "\_$jhdata\_";
    $jhdata =~ s/\W//isg;
} 

	$dirtoopen = "$lbdir" . "forum$inforum";
	opendir (DIR, "$dirtoopen");
	my @dirdata = readdir(DIR);
	closedir (DIR);
	@entry = grep(/\.thd\.cgi$/,@dirdata);
        @entry = sort numerically(@entry);

		$dirtoopen2 = "$imagesdir" . "$usrdir/$inforum";
        	opendir (DIR, "$dirtoopen2");
	        @dirdata1 = readdir(DIR);
        	closedir (DIR);
		@dirdata1 = grep(/^$inforum\_/i, @dirdata1);

		    opendir (DIRS, "${lbdir}$saledir");
		    @files2 = readdir(DIRS);
		    closedir (DIRS);
		    @files2 = grep(/^$inforum\_/i, @files2);

	foreach (@entry) {
	  (my $topicid, my $tr) = split(/\./,$_);
          next if ($jhdata =~ /\_$topicid\_/);

	  $file1 = "$lbdir" . "forum$inforum/$topicid.thd.cgi";
	  open (TMP1, "$file1");
          flock(TMP1, 1) if ($OS_USED eq "Unix");
	  my @tmp = <TMP1>;
	  close (TMP1);
	  $postcount = @tmp;
          $postcount--;
	  my $tmp1 = $tmp[-1];
	  (my $no, my $no, my $no, my $no, my $no, my $lastpostdate, my $no, $no) = split(/\t/,$tmp1);

            $currenttime = time;
            $threadagelimit = $currenttime - $prunedays * 86400;
            if ($lastpostdate < $threadagelimit) {
                $filetotrash = "$lbdir" . "forum$inforum/$topicid.thd.cgi";
                unlink $filetotrash;
                $filetotrash = "$lbdir" . "forum$inforum/$topicid.mal.pl";
                unlink $filetotrash;
                $filetotrash = "$lbdir" . "forum$inforum/$topicid.poll.pl";
                unlink $filetotrash;
                $filetotrash = "$lbdir" . "forum$inforum/$topicid.pl";
                unlink $filetotrash;
        	$filetounlink = "$lbdir" . "forum$inforum/rate$topicid.file.pl";
	        unlink $filetounlink;
        	$filetounlink = "$lbdir" . "forum$inforum/rateip$topicid.file.pl";
	        unlink $filetounlink;

		&delallupfiles($inforum,$topicid);

		    my @files2 = grep(/^$inforum\_$topicid\_/i, @files2);
		    foreach (@files2) {
		        chomp $_;
		        unlink ("${lbdir}$saledir/$_");
    		    }

	        @files = grep(/^$inforum\_$topicid(\.|\_)/,@dirdata1);
        	foreach (@files) {
        	    unlink ("$dirtoopen2/$_");
            	}
                $totaltopics_deleted++;
                $totalposts_deleted = $totalposts_deleted + $postcount;
	   }
	  }

	    my $info = rebuildLIST(-Forum=>"$inforum");
            ($threadcount,$topiccount) = split (/\|/,$info);
            $threadcount = 0 if ($threadcount<0);
            $topiccount  = 0 if ($topiccount <0);

            open(FILE, "${lbdir}boarddata/listno$inforum.cgi");
            $topicid = <FILE>;
            close(FILE);
            chomp $topicid;
	    my $rr = &readthreadpl($forumid,$topicid);
	    (my $lastpostdate, my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $posticon, my $posttemp, my $addmetemp) = split (/\t/,$rr);

            open(FILE, "+<${lbdir}boarddata/foruminfo$inforum.cgi");
            ($no, $no, $no, $todayforumpost, $no) = split(/\t/,<FILE>);

            $lastforumpostdate = "$lastpostdate\%\%\%$topicid\%\%\%$topictitle";
	    $lastposter = $startedby if ($lastposter eq "");
	    seek(FILE,0,0);
            print FILE "$lastforumpostdate\t$threadcount\t$topiccount\t$todayforumpost\t$lastposter\t\n";
            close(FILE);
	    $posts = 0 if ($posts eq "");$threads = 0 if ($threads eq "");
	    open(FILE, ">${lbdir}boarddata/forumposts$inforum.pl");
	    print FILE "\$threads = $threadcount;\n\$posts = $topiccount;\n\$todayforumpost = \"$todayforumpost\";\n1;\n";
            close(FILE);

        require "$lbdir" . "data/boardstats.cgi";
        $filetomake   = "$lbdir" . "data/boardstats.cgi";
        $totalthreads = $totalthreads - $totaltopics_deleted;
        $totalposts   = $totalposts - $totalposts_deleted;
        &winlock($filetomake) if ($OS_USED eq "Nt");
        if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \"$lastregisteredmember\"\;\n";
        print FILE "\$totalmembers = \"$totalmembers\"\;\n";
        print FILE "\$totalthreads = \"$totalthreads\"\;\n";
        print FILE "\$totalposts = \"$totalposts\"\;\n";
        print FILE "\n1\;";
        close (FILE);
        }
        &winunlock($filetomake) if ($OS_USED eq "Nt");
        if (! $totaltopics_deleted) { $totaltopics_deleted = "0"; }
        if (! $totalposts_deleted)  { $totalposts_deleted  = "0"; }
	&addadminlog("����ɾ�� $prunedays ����ǰ�����⹲ $totaltopics_deleted ƪ");
            $output .= qq~
            <SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 width=100%>
            <tr>
            <td bgcolor=$titlecolor $catbackpic valign=middle align=center><font face="$font" color=$fontcolormisc><b>��̳�����Ѿ���ɾ��</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
            ͳ�����ϣ�
            <ul>
            <li>��ɾ�����⣺$totaltopics_deleted ƪ
            <li>��ɾ���ظ���$totalposts_deleted ƪ
            <li><a href="forums.cgi?forum=$inforum">������̳$savetopicid</a>
            <li><a href="leobbs.cgi">������̳��ҳ</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <SCRIPT>valignend()</SCRIPT>
	    ~;
       } else {
         if ($movetoid == $inforum) { &error("�ƶ�����&��������ͬһ��̳���ƶ���"); }

if (-e "${lbdir}boarddata/jinghua$inforum.cgi") {
    open(FILE, "${lbdir}boarddata/jinghua$inforum.cgi");
    my @jhdatas = <FILE>;
    close(FILE);
    $jhdata = join("\_",@jhdatas);
    $jhdata = "\_$jhdata\_";
    $jhdata =~ s/\W//isg;
}
                $currenttime = time;

                $filetoopen = "$lbdir" . "data/allforums.cgi";
                &winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
                open(FILE, "$filetoopen");
                flock(FILE, 1) if ($OS_USED eq "Unix");
                @forums = <FILE>;
                close(FILE);
                &winunlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
                foreach $forumline (@forums) { #start foreach @forums
                    ($tempno, $trash) = split(/\t/,$forumline);
                        if ($inforum eq $tempno) {
                            ($trash, $trash, $trash, $oldforumname, $trash) = split(/\t/,$forumline);
                            last;
                        }
                    }

                foreach $forumline (@forums) { #start foreach @forums
                    ($tempno, $trash) = split(/\t/,$forumline);
                        if ($movetoid eq $tempno) {
                            ($trash, $trash, $trash, $newforumname, $trash) = split(/\t/,$forumline);
                            last;
                        }
                    }
        if ($inaddline eq "yes") {
             $moveinfo = qq~����ת���ԣ� <a href=forums.cgi?forum=$inforum target=_self>$oldforumname</a>~;
        }

     $filetoopen = "$lbdir" . "boarddata/lastnum$movetoid.cgi";
     if (-e $filetoopen) {
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        $newthreadnumber = <FILE>;
        close(FILE);
        chomp $newthreadnumber;
	$newthreadnumber ++;
     }
        $dirtoopen2 = "$imagesdir" . "$usrdir/$inforum";
        opendir (DIR, "$dirtoopen2");
        @dirdata2 = readdir(DIR);
        closedir (DIR);
        @files = grep(/^$inforum\_/,@dirdata2);


	$dirtoopen = "$lbdir" . "forum$inforum";
	opendir (DIR, "$dirtoopen");
	my @dirdata = readdir(DIR);
	closedir (DIR);
	@entry = grep(/\.thd\.cgi$/,@dirdata);
	foreach (@entry) {
	  (my $topicid, my $tr) = split(/\./,$_);
	  
          next if ($jhdata =~ /\_$topicid\_/);
          	
	  $file1 = "$lbdir" . "forum$inforum/$topicid.thd.cgi";
	  open (TMP1, "$file1");
          flock(TMP1, 1) if ($OS_USED eq "Unix");
	  my @tmp = <TMP1>;
	  close (TMP1);
	  my $tmp1 = $tmp[-1];
	  (my $no, my $no, my $no, my $no, my $no, my $lastpostdate, my $no, $no) = split(/\t/,$tmp1);

            $currenttime = time;
            $threadagelimit = $currenttime - $prunedays * 86400;
            if ($lastpostdate < $threadagelimit) {
                &MoveTopic("$topicid", $#tmps);
                $totaltopics_moved++;
	   }
	  }

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

            my $truenumber = rebuildLIST(-Forum=>"$movetoid");
            ($tpost,$treply) = split (/\|/,$truenumber);

            open(FILE, "${lbdir}boarddata/listno$movetoid.cgi");
            $topicid = <FILE>;
            close(FILE);
            chomp $topicid;
	    my $rr = &readthreadpl($forumid,$topicid);
	    (my $lastpostdate, my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $posticon, my $posttemp, my $addmetemp) = split (/\t/,$rr);

            open(FILE, "+<${lbdir}boarddata/foruminfo$movetoid.cgi");
            ($no, $no, $no, $todayforumpost, $no) = split(/\t/,<FILE>);
            $lastforumpostdate = "$lastpostdate\%\%\%$topicid\%\%\%$topictitle";
	    $lastposter = $startedby if ($lastposter eq "");
	    seek(FILE,0,0);
            print FILE "$lastforumpostdate\t$tpost\t$treply\t$todayforumpost\t$lastposter\t\n";
       	    close(FILE);
	    $posts = 0 if ($posts eq "");$threads = 0 if ($threads eq "");
	    open(FILE, ">${lbdir}boarddata/forumposts$movetoid.pl");
	    print FILE "\$threads = $tpost;\n\$posts = $treply;\n\$todayforumpost = \"$todayforumpost\";\n1;\n";
            close(FILE);

            if (! $totaltopics_moved) { $totaltopics_moved = "0"; }

	    &addadminlog("����ת�� $prunedays ����ǰ�����⹲ $totaltopics_moved ƪ�� $newforumname");
            
            $output .= qq~
            <SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 width=100%>
            <tr>
            <td bgcolor=$titlecolor $catbackpic valign=middle align=center><font face="$font" color=$fontcolormisc><b>��̳�����Ѿ����ƶ�</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
            ͳ�����ϣ�
            <ul>
            <li>���ƶ����⣺$totaltopics_moved ƪ
            <li><a href="forums.cgi?forum=$inforum">����ԭ��̳</a>
            <li><a href="forums.cgi?forum=$movetoid">��������̳</a>
            <li><a href="leobbs.cgi">������̳��ҳ</a>
			</ul>
            </tr>
            </td>
            </table></td></tr></table>
            <SCRIPT>valignend()</SCRIPT>
	    ~;
	    }

	}
	else {
            &mischeader("��������");
    if ((($membercode eq "ad") ||($membercode eq 'smo'))&& ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($inmembmod eq "yes") && ($membercode ne "amo") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
        if ($cleartoedit eq "no" && $checked eq "yes") {&error("ʹ����������&�����Ǳ���̳̳��������Ա�������������������");  }
            $filetoopen = "$lbdir" . "data/allforums.cgi";
            &winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
            open(FILE, "$filetoopen");
            flock(FILE, 1) if ($OS_USED eq "Unix");
            @forums = <FILE>;
            close(FILE);
            &winunlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
            $jumphtml .= "<option value=\"\">ѡ��һ����̳\n</option>";
    $a=0;
    foreach my $forum (@forums) { #start foreach @forums
	$a  = sprintf("%09d",$a);
	chomp $forum;
	next if (length("$forum") < 30);
	(my $forumid, my $category, my $categoryplace, my $forumname, my $forumdescription, my $tmp , $tmp , $tmp , $tmp,  $tmp , $tmp , $tmp,  $tmp,  $tmp,  $tmp, $tmp, $tmp, $tmp,my $hiddenforum,$tmp,$tmp,$tmp, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/,$forum);
	next if ($forumid !~ /^[0-9]+$/);
	next if ($categoryplace !~ /^[0-9]+$/);
	$categoryplace  = sprintf("%09d",$categoryplace);
	$rearrange = ("$categoryplace\t$a\t$category\t$forumname\t$forumdescription\t$forumid\t$forumgraphic\t$miscad2\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$fgwidth\t$fgheight\t$miscad4\t$todayforumpost\t$miscad5\t");
	push (@rearrangedforums, $rearrange);
	$a++;
    }

    @finalsortedforums = sort (@rearrangedforums);

foreach my $sortedforums (@finalsortedforums) {
    (my $categoryplace, my $a, my $category, my $forumname, my $forumdescription, my $forumid, my $forumgraphic, my $miscad2, my $misc, my $forumpass, my $hiddenforum, my $indexforum,my $teamlogo,my $teamurl,my $fgwidth,my $fgheight,my $miscad4,my $todayforumpost,my $miscad5) = split(/\t/,$sortedforums);
    $categoryplace  = sprintf("%01d",$categoryplace);
    if ($categoryplace ne $lastcategoryplace) {
        $jumphtml .= "<option value=\"\" style=background-color:$titlecolor>��$category\n</option>";
    }
    if ($hiddenforum eq "yes"){ $hidden="(����)" ; }else{ $hidden=""; } 
	 $child=($category =~/^childforum-[0-9]+/)?"��|":"";
    $jumphtml .= "<option value=\"$forumid\">$child��|-$forumname$hidden\n</option>" if (($disphideboard eq "yes")||($hidden eq "")||($membercode eq "ad")||($membercode eq "smo")||($membercode eq "cmo")||($membercode eq "mo")||($membercode eq "amo"));
    $lastcategoryplace = $categoryplace;
}
$jumphtml .= qq~</select>\n~;

            $output .= qq~
            <SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 width=100%>
            <tr>
            <td bgcolor=$titlecolor $catbackpic valign=middle colspan=2 align=center>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="prune">
            <input type=hidden name="checked" value="yes">
            <input type=hidden name="forum" value="$inforum">
            <font face="$font" color=$fontcolormisc><b>������������ϸ�����Ա�������ģʽ[��������]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
	<tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>ѡ������ģʽ</font></td>
            <td bgcolor=$miscbackone valign=middle><input type="radio" name="admin" value="delete">ɾ�� <input type="radio" name="admin" value="move">�ƶ�</td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>ת������</b>(ֻ�������ƶ���Ч)</font></td>
            <td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><select name="movetoid">$jumphtml</select><BR><input type="checkbox" name="addline" value="yes" checked>����������ʾת������</font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle colspan=2><font face="$font" color=$fontcolormisc><b>һ����ѡ��ɾ�����£������ܹ��ָ���</b><br>���潫ɾ������ʱ�䳬��һ����������������¡�<br>�����ȷ��������������ϸ������������Ϣ��</font></td></tr>
			<tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>������������������<br>���磺����'30'���������� 30 ����������¡�</font></td>
            <td bgcolor=$miscbackone valign=middle><input type=text name="prunedays"></td></tr>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name="submit" value="�� ��"></td></tr></form></table></td></tr></table>
            </table></td></tr></table>
            <SCRIPT>valignend()</SCRIPT>
	    ~;
	}
}
else { &error("��ͨ����&δָ����������"); }
&output("$boardname - ��������",\$output);
exit;

sub MoveTopic {
	my ($intopic, $nums) = shift;
	do {
		$newthreadnumber++;
	} while (-e "${lbdir}forum$movetoid/$newthreadnumber.thd.cgi");

	open(ENT, "${lbdir}forum$inforum/$intopic.pl");
	my $in = <ENT>;
	close (ENT);
	chomp($in);
	my ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $lastinposticon, $inposttemp, $addmetemp) = split(/\t/, $in);

	if (open(FILE, ">${lbdir}forum$movetoid/$newthreadnumber.pl"))
	{
		print FILE "$newthreadnumber\t$topictitle\t$moveinfo\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$lastinposticon\t$inposttemp\t$addmetemp\t";
		close(FILE);
	}

	rename("${lbdir}forum$inforum/$intopic.thd.cgi", "${lbdir}forum$movetoid/$newthreadnumber.thd.cgi");
	rename("${lbdir}forum$inforum/$intopic.mal.pl", "${lbdir}forum$movetoid/$newthreadnumber.mal.pl") if (-e "${lbdir}forum$inforum/$intopic.mal.pl");
	rename("${lbdir}forum$inforum/$intopic.poll.cgi", "${lbdir}forum$movetoid/$newthreadnumber.poll.cgi") if (-e "${lbdir}forum$inforum/$intopic.poll.cgi");
	rename("${lbdir}forum$inforum/rate$intopic.file.pl", "${lbdir}forum$movetoid/rate$newthreadnumber.file.pl") if (-e "${lbdir}forum$inforum/rate$intopic.file.pl");
	rename("${lbdir}forum$inforum/rateip$intopic.file.pl", "${lbdir}forum$movetoid/rateip$newthreadnumber.file.pl") if (-e "${lbdir}forum$inforum/rateip$intopic.file.pl");
	for (0 .. $nums) {rename("${lbdir}forum$inforum/$intopic\_$_.sale.cgi", "${lbdir}forum$movetoid/$newthreadnumber\_$_.sale.cgi");}
	unlink("${lbdir}forum$inforum/$intopic.pl");
	unlink("${lbdir}FileCount/$inforum/$inforum\_$intopic.pl");

   $OldHackDetail="${lbdir}FileCount/$inforum/$inforum\_$intopic.cgi";
   $NewHackDetail="${lbdir}FileCount/$movetoid/$movetoid\_$newthreadnumber.cgi";

   if(-e $OldHackDetail){
			open(HACK, "$OldHackDetail");
			@AllHackDetail = <HACK>;
			close(HACK);
			open(NHACK, ">$NewHackDetail");
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
	        unlink $OldHackDetail;
   }

&moveallupfiles($inforum,$intopic,$movetoid,$movetoid,"yes"); #�µķ�ʽ

	my @files1 = grep(/^$inforum\_$intopic(\.|\_)/, @dirdata1);
	foreach (@files1)
	{
		chomp;
		my (undef, $ext) = split(/\./, $_);
		rename("${imagesdir}$usrdir/$inforum/$_", "${imagesdir}$usrdir/$movetoid/$movetoid\_$newthreadnumber.$ext");
	}
}
