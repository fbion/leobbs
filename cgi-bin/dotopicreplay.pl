#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

    if ($startnewthreads eq "onlysub") {&error("����&�Բ��������Ǵ�����̳�����������ԣ�"); }
    if (($floodcontrol eq "on") && ($membercode ne "ad") && ($membercode ne 'smo') && ($membercode ne 'amo') && ($membercode ne 'cmo') && ($membercode ne "amo") && ($membercode ne "mo") && ($inmembmod ne "yes")) {
	($lastpost, $posturl, $posttopic) = split(/\%\%\%/,$lastpostdate);
	$lastpost = $lastpost + $floodcontrollimit;
	if ($lastpost > $currenttime)  {
	    my $lastpost1 = $lastpost - $currenttime;
	    &error("����ظ�&��ˮԤ�������Ѿ�ʹ�ã��������ٵȴ� $lastpost1 ���Ӳ����ٴη���");
	}
    }
    if (($inhiddentopic eq "yes") && ($moneyhidden eq "yes")) { &error("����ظ�&�벻Ҫ��һ��������ͬʱʹ�������ͽ�Ǯ���ܣ�"); }
    if ((($inhiddentopic eq "yes")||($moneyhidden eq "yes")) && ($userregistered eq "no")) { &error("����ظ�&δע���û���Ȩ���������ͽ�Ǯ���ܣ�"); }

    &error("�����ظ�����&�Բ��𣬱���̳���������ظ����� <B>$maxpoststr</B> ���ַ������£�") if ((length($inpost) > $maxpoststr)&&($maxpoststr ne "")&&($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne 'cmo') && ($membercode ne "mo") && ($membercode ne "amo") && ($membercode !~ /^rz/) && ($inmembmod ne "yes"));
    &error("�����ظ�����&�Բ��𣬱���̳���������ظ����� <B>$minpoststr</B> ���ַ������£�") if ((length($inpost) < $minpoststr)&&($minpoststr ne "")&&($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne 'cmo') && ($membercode ne "mo") && ($membercode ne "amo") && ($membercode !~ /^rz/) && ($inmembmod ne "yes"));

    if ($postopen eq "no") { &error("�����ظ�����&�Բ��𣬱���̳���������ظ����⣡"); }

    if ($deletepercent > 0 && $numberofposts + $numberofreplys > 0 && $membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo" && $membercode ne "amo" && $inmembmod ne "yes") {
	&error("����ظ�&�Բ������ɾ���ʳ�����<b>$deletepercent</b>%������Ա�������㷢��ظ�������ϵ̳�������") if ($postdel / ($numberofposts + $numberofreplys) >= $deletepercent / 100);
    }

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
	if ($privateforum ne "yes") {
     	    &whosonline("$inmembername\t$forumname\tnone\t�ظ�<a href=\"topic.cgi?forum=$inforum&topic=$intopic\"><b>$topictitle</b></a>\t") if ($topictitle ne "");
	}
	else {
            &whosonline("$inmembername\t$forumname(��)\tnone\t�ظ���������\t");
	}
    }

    if ((($onlinetime + $onlinetimeadd) < $onlinepost)&&($onlinepost ne "")&&($membercode ne "ad")&&($membercode ne "smo")&&($membercode ne "cmo")&&($membercode ne "mo")&&($membercode ne "amo")&&($membercode !~ /^rz/))     { $onlinetime = $onlinetime + $onlinetimeadd;  &error("�ظ�����&�Բ��𣬱���̳����������ʱ������ $onlinepost ����û��ظ����⣡��Ŀǰ�Ѿ����� $onlinetime �룡<BR>�������ʱ��ͳ�Ʋ���ȷ,�����µ�½��̳һ�μ��ɽ����"); }

    if (($userregistered eq "no")&&(length($inmembername) > 12)) { &error("�����»ظ�&��������û���̫�����������6�������ڣ�");   }
    if (($userregistered eq "no")&&($inmembername =~ /^����/)) { &error("�����»ظ�&�벻Ҫ���û����Ŀ�ͷ��ʹ�ÿ���������");   }
    if ($inmembername eq "����") { &error("�����»ظ�&�벻Ҫ���û����Ŀ�ͷ��ʹ�ÿ���������");   }
    if (($userregistered eq "no")&&($startnewthreads ne "all")) { &error("�����»ظ�&��û��ע�ᣡ");   }
    elsif ((($inpassword ne $password)&&($userregistered ne "no"))||(($inpassword ne "")&&($userregistered eq "no"))) { &error("�����»ظ�&�����������"); }
    elsif (($membercode eq "banned")||($membercode eq "masked"))  { &error("����&�ѱ���ֹ���Ի��߷��Ա����Σ�����ϵ����Ա�����"); }
    elsif ($inpost eq "")            { &error("�����»ظ�&�����������ݣ�"); }
    else {
#	@allforums = @forums;

	if ($startnewthreads eq "no") {
            unless ($membercode eq "ad" || $membercode eq 'smo' || $inmembmod eq "yes") {&error("�����»ظ�&�ڴ���̳��ֻ����̳�����߱�����������»ظ���");}
        }
        elsif ($startnewthreads eq "cert"){
	    unless ($membercode eq "ad" ||$membercode eq 'smo'|| $inmembmod eq "yes"||$membercode eq 'cmo'||$membercode eq 'amo'||$membercode eq 'mo'||$membercode =~ /^rz/) { &error("�����»ظ�&�ڴ���̳��ֻ����̳������������֤��Ա�����»ظ���"); }
	}
	$tempaccess = "forumsallowed". "$inforum";
	$testentry = $query->cookie("$tempaccess");

	if ((($testentry eq $forumpass)&&($testentry ne ""))||($allowedentry{$inforum} eq "yes")||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }
        if (($privateforum eq "yes") && ($allowed ne "yes")) { &error("����&�Բ������������ڴ���̳����"); }
 	if (($startnewthreads eq "all")&&($userregistered eq "no")) { $inmembername = "$inmembername(��)"; }

        $inpost =~ s/\[���(.+?)�����(.+?)�༭\]//isg;

        $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
        if (-e $filetoopen) {
           &winlock($filetoopen) if ($OS_USED eq "Nt");
           open(FILE, "$filetoopen");
           flock(FILE, 1) if ($OS_USED eq "Unix");
	   sysread(FILE, $allmessages,(stat(FILE))[7]);
           close(FILE);
	   $allmessages =~ s/\r//isg;
           &winunlock($filetoopen) if ($OS_USED eq "Nt");
           @allmessages=split(/\n/,$allmessages);
        }
	else { unlink ("$lbdir" . "forum$inforum/$intopic.pl"); &error("�ظ�&������ⲻ���ڣ������Ѿ���ɾ����"); }

if ($floor ne "") {
unless ($floor=~ /^[0-9]+$/) {&error("���ûظ�����&��������ûظ�¥�������к��зǷ��ַ���");} 
if ($floor <= 0){&error("���ûظ�����&��������ûظ�¥�����ֲ���Ϊ�������");}
if ($floor != int($floor)){&error("���ûظ�����&��������ûظ�¥�����ֲ�������");}
$kate=@allmessages;
if($floor>$kate){&error("���ûظ�����&����ԭ��û��$floor���¥�㣬����ϸ�����ǲ�������д�����ִ����أ���������㲻�����ûظ����벻Ҫ�ڱ�������д����");}
($membername2, undef, undef, undef, undef ,$postdate2, $post2, undef) = split(/\t/, $allmessages[$floor-1]);

   if  ($post2=~/LBHIDDEN\[(.*?)\]LBHIDDEN/sg){
	$post2="(��������)";
   }
   if  ($post2=~/LBSALE\[(.*?)\]LBSALE/sg){
	$post2="(��������)";
   }

    $post2 =~ s/\[post=(.+?)\](.+?)\[\/post\]//isg;
    $post2 =~ s/\[jf=(.+?)\](.+?)\[\/jf\]//isg;
    $post2 =~ s/\[hide\](.+?)\[\/hide\]//isg;
    $post2 =~ s/\[watermark\](.+?)\[\/watermark\]/\n\(ˮӡ���ֲ�������\)\n/isg;
    $post2 =~ s/(\&\#35\;|#)Moderation Mode//isg;
    $post2 =~ s/\<p\>/\n\n/ig;
    $post2 =~ s/\<br\>/\n/ig;
    $post2 =~ s/ \&nbsp;/  /ig;
    $post2 =~ s/\[curl=\s*(http|https|ftp):\/\/(.*?)\s*\]/\[��������\]/isg if ($usecurl ne "no");
    $post2 =~ s/\[DISABLELBCODE\]//isg;
    $post2 =~ s/\[ADMINOPE=(.+?)\]//isg;
    $post2 =~ s/ \n/\n/isg;
    $post2 =~ s/��\n/\n/isg;
    if ($post2 =~ /\[POSTISDELETE=(.+?)\]/) {
    	if ($1 ne " ") { $presult = "�������ɣ�$1"; } else { $presult = "<BR>"; }
        $post2 = "�����������Ѿ����������Σ�$presult";
    }

   $membernametemp2=$membername2;

   $postdate2 = $postdate2 + ($timedifferencevalue + $timezone)*3600;
   $postdate2 = &dateformat("$postdate2");
   $rawpost = $post2;

    $rawpost =~ s/\[���(.+?)�����(.+?)�༭\]\n//isg;
    $rawpost =~ s/LBHIDDEN\[(.*?)\]LBHIDDEN//sg;
    $rawpost =~ s/LBSALE\[(.*?)\]LBSALE//sg;
    $rawpost =~ s/\[quote\](.*)\[quote\](.*)\[\/quote](.*)\[\/quote\]//isg;
    $rawpost =~ s/\[quote\](.*)\[\/quote\]//isg;
    $rawpost =~ s/\[equote\](.*)\[\/equote\]//isg;
    $rawpost =~ s/\[fquote\](.*)\[\/fquote\]//isg;
    $rawpost =~ s/\[hide\](.*)\[hide\](.*)\[\/hide](.*)\[\/hide\]//isg; 
    $rawpost =~ s/\[hide\](.*)\[\/hide\]//isg; 
    $rawpost =~ s/\[jf=(.+?)\](.+?)\[\/jf\]//isg;
    $rawpost =~ s/\[jf=(.+?)\](.+?)\[\/jf\](.*)\[jf=(.+?)\](.+?)\[\/jf\]//isg; 
    $rawpost =~ s/\[post=(.+?)\](.+?)\[\/post\](.*)\[post=(.+?)\](.+?)\[\/post\]//isg; 
    $rawpost =~ s/\[post=(.+?)\](.+?)\[\/post\]//isg; 
    $rawpost =~ s/\[\s*(.*?)\s*\]\s*(.*?)\s*\[\s*(.*?)\s*\]/$2/isg;
    $rawpost =~ s/\:.{0,20}\://isg;
    $rawpost =~ s/\<img\s*(.*?)\s*\>//isg;
    $rawpost =~ s/(http|https|ftp):\/\/(.*?)\.(png|jpg|jpeg|bmp|gif|swf)/($2\.$3)/isg;
    $rawpost =~ s/\&nbsp;/ /ig;
    $rawpost =~ s/( )+$//isg;
    $rawpost =~ s/^( )+//isg;
    $rawpost =~ s/\[.+?\]//g;
    $rawpost =~ s/(\n)+/\n/isg;
    $rawpost =~ s/ \n/\n/isg;
    $rawpost =~ s/��\n/\n/isg;
    $rawpost =~ s/\n\n/\n/isg;
    $rawpost =~ s/^\n//isg;
    $rawpost =~ s/\n$//isg;
    $rawpost =~ s/\n/<BR>/isg;
    chomp $rawpost;

   my @postall = split(/\n/,$rawpost);
   my $postall = @postall;
   if ($postall > 4) { $rawpost = "$postall[0]\n$postall[1]\n$postall[2]\n$postall[3]\n..."; }
   $rawpost = &lbhz($rawpost,200);

   $inpost = qq~\[quote\]\[b\]����������\[u\]$membernametemp2\[\/u\]�� \[i\]$postdate2\[\/i\] ��������ݣ�\[\/b\]<br>$rawpost<br>\[\/quote\]<br>$inpost~;
}

        my $file = "$lbdir" . "forum$inforum/$intopic.pl";
        &winlock($file) if ($OS_USED eq "Nt");
        open (ENT, $file);
        flock(ENT, 2) if ($OS_USED eq "Unix");
        $in = <ENT>;
        close (ENT);
	&winunlock($file) if ($OS_USED eq "Nt");
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $posticon, my $no, $addmetype) = split(/\t/,$in);
        if (($threadstate eq "closed")||($threadstate eq "pollclosed")) { &error("����ظ�&�Բ�����������Ѿ���������"); }
        $numberofitems = $threadposts+ 1; 
	if (($rdays ne '')&&($membercode ne "ad")&&($membercode ne "smo")) { &error("����ظ�&���� $rdays ������Ӳ������ٻظ���") if ($currenttime - $lastpostdate > $rdays * 86400); }

        $inpost = &dofilter("$inpost");

        if ($emote && $inpost =~ m/\/\/\//) {
	    study ($inpost);
 	    my @pairs1 = split(/\&/,$emote);
	    foreach (@pairs1) {
		my ($toemote, $beemote) = split(/=/,$_);
		chomp $beemote;
		$beemote =~ s/����/��$inmembername��/isg;
		$inpost =~ s/$toemote/$beemote/isg;
		last unless ($inpost =~ m/\/\/\//);
	    }
	}

        ($trash, $topictitle, $trash, $trash, $trash, $trash, $post, $trash,my $water) = split(/\t/,$allmessages[0]);

	if (($nowater eq "on")&&($water eq "no")&&($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne 'amo')&&($membercode ne 'cmo')&&($membercode ne 'mo')&&($inmembmod ne "yes")) {
	    my $inposttemp = $inpost;
	    $inposttemp =~ s/\[���(.+?)�����(.+?)�༭\]\<BR\>\<BR\>//isg;
	    $inposttemp =~ s/\[���(.+?)�����(.+?)�༭\]\<BR\>//isg;
	    $inposttemp =~ s/\[���(.+?)�����(.+?)�༭\]//isg;
	    $inposttemp =~ s/\[quote\]\[b\]����������\[u\].+?\[\/u\]�� \[i\].+?\[\/i\] ��������ݣ�\[\/b\].+?\[\/quote\]\<br\>//isg;
	    $inposttemp =~ s/\[quote\]\[b\]����������\[u\].+?\[\/u\]�� \[i\].+?\[\/i\] ��������ݣ�\[\/b\].+?\[\/quote\]//isg;
	    if ((length($inposttemp) < $gsnum)&&($gsnum > 0)) {
	        &error("����ظ�&�벻Ҫ��ˮ���������ֹ $gsnum �ֽ����µĹ�ˮ��");
	    }
	}

	$inpost =~ s/\[UploadFile.{0,6}=(.+?)\]//isg unless (($allowattachment ne "no")||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes"));

        $addme= &upfileonpost(\$inpost,$inforum,$intopic);#�����ϴ���������ֵ��BT�����ж�
#	&error("����������&���������������������뷵�����ԣ�") if (($addme eq "0")&&($mastpostatt eq "yes")&&($membercode ne "ad")&&($membercode ne 'smo')&&($inmembmod ne "yes"));

        if ($moneyhidden eq "yes") { $inposttemp = "(����)"; $inpost="LBSALE[$moneypost]LBSALE".$inpost;}

	if ($inhiddentopic eq "yes") { $inposttemp = "(����)"; $inpost="LBHIDDEN[$postweiwang]LBHIDDEN".$inpost; }

	if ($inposttemp ne "(����)") {
	    $inposttemp = $inpost;
	    $inposttemp = &temppost($inposttemp);
            chomp $inposttemp;
            $inposttemp = &lbhz($inposttemp,50);
	}
	$lastreplymessgae = $allmessages[-1];
        (my $ainmembername,my $no,my $no,my $no,my $no,my $no,my $ainpost,my $no) = split(/\t/,$lastreplymessgae);
 	if (($inmembername eq $ainmembername)&&($inpost eq $ainpost)) {
    	    &error("����ظ�&�벻Ҫ�ظ��ظ����Ѿ�������˻ظ�������ͬ�Ķ������㷢�Ļظ��ˣ�");
	}

        &winlock($filetoopen) if ($OS_USED eq "Nt");
        if (open(FILE, ">>$filetoopen")) {
            flock(FILE, 2) if ($OS_USED eq "Unix");
            print FILE "$inmembername\t$topictitle\t$postipaddress\t$inshowemoticons\t$inshowsignature\t$currenttime\t$inpost\t$inposticon\t\n";
            close(FILE);
        }
        &winunlock($filetoopen) if ($OS_USED eq "Nt");

        $threadposts = @allmessages;
        $threadviews = $threadposts if ($threadviews < $threadposts);
#	$threadviews = 9999 if ($threadviews > 10000);

        my $topictitletemp = $topictitle;
        $topictitletemp =~ s/^����������//;
        &winlock($file) if ($OS_USED eq "Nt");
        if (open(FILE, ">$file")) {
            flock(FILE, 2) if ($OS_USED eq "Unix");
            print FILE "$intopic\t����������$topictitletemp\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$inmembername\t$currenttime\t$posticon\t$inposttemp\t$addmetype\t";
        close(FILE);
        }
        &winunlock($file) if ($OS_USED eq "Nt");
        
	$file = "$lbdir" . "boarddata/listno$inforum.cgi";
        &winlock($file) if ($OS_USED eq "Nt");
        open (LIST, "$file");
        flock (LIST, 2) if ($OS_USED eq "Unix");
	sysread(LIST, $listall,(stat(LIST))[7]);
        close (LIST);
	$listall =~ s/\r//isg;
        $listall =~ s/(.*)(^|\n)$intopic\n(.*)/$1$2$3/;
        
	if (length($listall) > 500) {
	    if (open (LIST, ">$file")) {
        	flock (LIST, 2) if ($OS_USED eq "Unix");
        	print LIST "$intopic\n$listall";
        	close (LIST);
            }
            &winunlock($file) if ($OS_USED eq "Nt");
    	} else {
            &winunlock($file) if ($OS_USED eq "Nt");
	    require "rebuildlist.pl";
            my $truenumber = rebuildLIST(-Forum=>"$inforum");
            ($tpost,$treply) = split (/\|/,$truenumber);
	}

        $cleanmembername = $inmembername;
        $cleanmembername =~ s/ /\_/isg;
	$cleanmembername =~ tr/A-Z/a-z/;

      $maxpersontopic = 25;
      if ($maxpersontopic && $userregistered ne "no") {
              $cleanstart = $startedby;
              $cleanstart =~ s/ /\_/isg;
              $cleanstart =~ tr/A-Z/a-z/;
              &addmytopic("reply", $cleanmembername, $inforum, $intopic, $topictitletemp, $currenttime, $posticon);
              &addmytopic("post", $cleanstart, $inforum, $intopic, $topictitletemp, $currenttime, $posticon) if ($cleanmembername ne $cleanstart);
      }

	if ($jifen eq "") {
		require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
		$jifen = $numberofposts * $ttojf + $numberofreplys * $rtojf - $postdel * $deltojf;
  }

      if ($forumallowcount ne "no") {
	  $numberofreplys++;
	  $mymoney += $forumreplymoney - $replymoney if ($forumreplymoney ne "");
          if ($forumreplyjf ne "") { $jifen += $forumreplyjf; } else { $jifen += $rtojf; }
      }
        $lastpostdate = "$currenttime\%\%\%topic.cgi?forum=$inforum&topic=$intopic\%\%\%$topictitletemp" if ($privateforum ne "yes");
        chomp $lastpostdate;

    if (($userregistered ne "no")&&($password ne "")) {
	my $namenumber = &getnamenumber($cleanmembername);
	&checkmemfile($cleanmembername,$namenumber);
        $filetomake = "$lbdir" . "$memdir/$namenumber/$cleanmembername.cgi";
        &winlock($filetomake) if ($OS_USED eq "Nt");
        if ((open(FILE, ">$filetomake"))&&($inmembername ne "")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
        close(FILE);
        }
        &winunlock($filetomake) if ($OS_USED eq "Nt");
        unlink ("${lbdir}cache/myinfo/$cleanmembername.pl");
        if (((-M "${lbdir}cache/meminfo/$cleanmembername.pl") *86400 > 60*2)||(!(-e "${lbdir}cache/meminfo/$cleanmembername.pl"))) {
            require "getnameinfo.pl" if ($onloadinfopl ne 1);
            &getmemberinfo($cleanmembername);
        }
    }
    
    my $nowtime = &shortdate($currenttime + $timezone*3600);

    my $filetoopens = "$lbdir/data/todaypost.cgi";
    $filetoopens = &lockfilename($filetoopens);

    if (($usetodaypostreply ne "no")&&(!(-e "$filetoopens.lck"))) {
    	&winlock("$lbdir/data/todaypost.cgi") if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
        if (-e "$lbdir/data/todaypost.cgi") {
            open (FILE,"+<$lbdir/data/todaypost.cgi");
            $todaypost=<FILE>;
            chomp $todaypost;
            my ($nowtoday,$todaypostno,$maxday,$maxdaypost,$yestdaypost)=split(/\t/,$todaypost);
            if ($nowtoday eq $nowtime) {
            	$todaypostno ++;
            	if ($todaypostno > $maxdaypost) {
            	    $maxday     = $nowtime;
            	    $maxdaypost = $todaypostno;
            	}
            }
            else {
    opendir (CATDIR, "${lbdir}cache");
    @dirdata = readdir(CATDIR);
    closedir (CATDIR);
    @dirdata = grep(/forumcache/,@dirdata);
    foreach (@dirdata) { unlink ("${lbdir}cache/$_"); }
            	$nowtoday = $nowtime;
            	$yestdaypost = $todaypostno;
            	$todaypostno = 1;
            }
            seek(FILE,0,0);
            print FILE "$nowtoday\t$todaypostno\t$maxday\t$maxdaypost\t$yestdaypost\t";
            close (FILE);
        }
        else {
            open (FILE,">$lbdir/data/todaypost.cgi");
            print FILE "$nowtime\t1\t$nowtime\t1\t0\t";
            close (FILE);
        }
    	&winunlock("$lbdir/data/todaypost.cgi") if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
    }

	$filetoopen = "${lbdir}boarddata/foruminfo$inforum.cgi";
	my $filetoopens = &lockfilename($filetoopen);
	if (!(-e "$filetoopens.lck")) {
            &winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
            open(FILE, "+<$filetoopen");
            ($no, $threads, $posts, $todayforumpost, $lastposter) = split(/\t/,<FILE>);
            $lastposter   = $inmembername;
            $lastposttime = $currenttime;
            if (($tpost ne "")&&($treply ne "")) {
                $threads = $tpost;
                $posts   = $treply;
            } else { $posts++; }
            if ($usetodayforumreply eq "yes") {
		($todayforumpost, $todayforumposttime) = split(/\|/,$todayforumpost);
		if (($nowtime ne $todayforumposttime)||($todayforumpost eq "")) { $todayforumpost = 1; } else { $todayforumpost++; }
                $todayforumpost = "$todayforumpost|$nowtime";
            }
            $lastposttime = "$lastposttime\%\%\%$intopic\%\%\%$topictitletemp";
	    
	    seek(FILE,0,0);
            print FILE "$lastposttime\t$threads\t$posts\t$todayforumpost\t$lastposter\t\n";
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
        $totalposts++;
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
    else {
    	unlink ("$filetoopens.lck") if ((-M "$filetoopens.lck") *86400 > 30);
    }

    if ($emailfunctions eq "on") {
	eval("use MAILPROG qw(sendmail);");
	$filetoopen = "$lbdir" . "forum$inforum/$intopic.mal.pl";
	open (FILE, "$filetoopen");
	my @maildata = <FILE>;
	close (FILE);

	$mailall = "$inmembername\t$emailaddress\t";
	if ($innotify eq "yes") {
	    if (open (FILE, ">$filetoopen")) {
                print FILE "$mailall\n";
                foreach (@maildata) {
                    chomp $_;
                    print FILE "$_\n" if ($mailall ne $line);
                }
                close (FILE);
	    }
	}
	$toemail = '';
	foreach (@maildata) {
	    chomp $_;
	    ($postersname,$posteremailaddress) = split(/\t/,$_);
            if ($lastemailsent ne $postersname) {
                if ($inmembername eq $postersname) { next; }
                next if ($posteremailaddress eq "");
        	$posteremailaddress =~ s/[\a\f\n\e\0\r\t\`\~\!\$\%\^\&\*\(\)\=\+\\\{\}\;\'\:\"\,\/\<\>\?\|]//isg;
        	next if ($posteremailaddress !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/);
            	if ($toemail eq "") {$toemail = $posteremailaddress;} else {$toemail .= ", $posteremailaddress";}
                $lastemailsent = $postersname;
	    }
	}

	$output .= "\n\n<!-- ���� Email ���� --> \n\n";
	chomp $toemail;
	$toemail =~ s/\\//g;
	$fromemail = $adminemail_out;
	chomp $fromemail;
	$fromemail =~ s/\\//g;
	$topictitle =~ s/&quot\;/\"/g;
        $topictitle =~ s/^����������//;

	$to = $toemail;
	$from = $fromemail;
	$subject = "[$forumname] �ظ�֪ͨ";
        $message .= "$boardname <br>\n";
	$message .= "$boardurl/leobbs.cgi <br>\n";
        $message .= "---------------------------------------------------------------------\n<br><br>\n";
        $message .= "���, �����������һ���»ظ���\n <br><br>\n";
        $message .= "�ظ��ˣ� $inmembername <br>\n";
        $message .= "���ࣺ $category <br>\n";
        $message .= "��̳�� $forumname <br>\n";
        $message .= "���⣺ $topictitle <br>\n";
        $message .= "������������ȥ�鿴��ϸ���ݣ�\n <br><br>\n";
        $message .= "$boardurl/topic.cgi?forum=$inforum&topic=$intopic\n <br><br>\n";
        $message .= "---------------------------------------------------------------------<br>\n";

        &sendmail($from, $emailaddress, $to, $subject, $message);
    }

    $numberofitems++;
    $postend = int($numberofitems / $maxtopics)*$maxtopics; 
    $pagestoshow = "";
    $numberofpages = $numberofitems / $maxtopics;
    if ($numberofitems > $maxtopics) {
        if ($maxtopics < $numberofitems) {
            ($integer,$decimal) = split(/\./,$numberofpages);
            if ($decimal > 0) { $numberofpages = $integer + 1; }
            $pagestart = 0;
            $counter = 0;
            while ($numberofpages > $counter) {
                $counter++;
                $threadpages .= qq~ <a href="topic.cgi?forum=$inforum&topic=$intopic&start=$pagestart">$counter</a> ~;
                $pagestart = $pagestart + $maxtopics;
            }
        }
	$pagestoshow = qq~<font color=$forumfontcolor> &nbsp;[ ��$threadpagesҳ ]~;
    }

    &mischeader("�ظ��ɹ�");

opendir (CATDIR, "${lbdir}cache");
@dirdata = readdir(CATDIR);
closedir (CATDIR);

unlink ("${lbdir}cache/plcache$inforum\_0.pl");

    if ($refreshurl == 1) { $relocurl = "topic.cgi?forum=$inforum&topic=$intopic&start=$postend#bottom"; }
                     else { $relocurl = "forums.cgi?forum=$inforum"; }
    $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>лл�����Ļظ��Ѿ��ɹ�����</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������û���Զ����أ�������������ӣ���
<ul><li><a href="topic.cgi?forum=$inforum&topic=$intopic">��������</a>  $pagestoshow
<li><a href="forums.cgi?forum=$inforum">������̳</a><li><a href="leobbs.cgi">������̳��ҳ</a>
<li><a href="postings.cgi?action=lock&forum=$inforum&topic=$intopic&checked=yes">��������</a>
</ul></tr></td></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=$relocurl">
	~;
    }
1;
