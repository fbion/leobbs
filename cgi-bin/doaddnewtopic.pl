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
    if (($floodcontrol eq "on") && ($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne 'amo') && ($membercode ne 'cmo') && ($membercode ne "mo") && ($inmembmod ne "yes")) {
	($lastpost, $posturl, $posttopic) = split(/\%\%\%/,$lastpostdate);
	$lastpost = $lastpost + $floodcontrollimit;
	if ($lastpost > $currenttime)  {
	    my $lastpost1 = $lastpost - $currenttime;
	    &error("����������&��ˮԤ�������Ѿ�ʹ�ã��������ٵȴ� $lastpost1 ���Ӳ����ٴη���");
	}
    }
    if (($inhiddentopic eq "yes") && ($moneyhidden eq "yes")) { &error("��������&�벻Ҫ��һ��������ͬʱʹ�������ͽ�Ǯ���ܣ�"); }
    if ((($inhiddentopic eq "yes")||($moneyhidden eq "yes")) && ($userregistered eq "no")) { &error("��������&δע���û���Ȩ���������ͽ�Ǯ���ܣ�"); }

    &error("�����ظ�����&�Բ��𣬱���̳���������ظ����� <B>$maxpoststr</B> ���ַ������£�") if ((length($inpost) > $maxpoststr)&&($maxpoststr ne "")&&($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne 'cmo') && ($membercode ne "mo") && ($membercode ne "amo") && ($membercode !~ /^rz/) && ($inmembmod ne "yes"));
    &error("�����ظ�����&�Բ��𣬱���̳���������ظ����� <B>$minpoststr</B> ���ַ������£�") if ((length($inpost) < $minpoststr)&&($minpoststr ne "")&&($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne 'cmo') && ($membercode ne "mo") && ($membercode ne "amo") && ($membercode !~ /^rz/) && ($inmembmod ne "yes"));

    if ($postopen eq "no") { &error("�����ظ�����&�Բ��𣬱���̳���������ظ����⣡"); }

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
	if ($privateforum ne "yes") { &whosonline("$inmembername\t$forumname\tnone\t����������\t"); }
	                       else { &whosonline("$inmembername\t$forumname(��)\tnone\t�����µı�������\t"); }
    }

    if ((($onlinetime + $onlinetimeadd) < $onlinepost)&&($onlinepost ne "")&&($membercode ne "ad")&&($membercode ne "smo")&&($membercode ne "cmo")&&($membercode ne "mo")&&($membercode ne "amo")&&($membercode !~ /^rz/))     { $onlinetime = $onlinetime + $onlinetimeadd; &error("����������&�Բ��𣬱���̳����������ʱ������ $onlinepost ����û��������⣡��Ŀǰ�Ѿ����� $onlinetime �룡<BR>�������ʱ��ͳ�Ʋ���ȷ,�����µ�½��̳һ�μ��ɽ����"); }

    if (($userregistered eq "no")&&(length($inmembername) > 12)) { &error("����������&��������û���̫�����������6�������ڣ�");   }
    if (($userregistered eq "no")&&($inmembername =~ /^����/)) { &error("����������&�벻Ҫ���û����Ŀ�ͷ��ʹ�ÿ���������");   }
    if ($inmembername eq "����") { &error("����������&�벻Ҫ���û����Ŀ�ͷ��ʹ�ÿ���������");   }
    if (($userregistered eq "no")&&($startnewthreads ne "all")) { &error("����������&��û��ע�ᣡ");   }
    elsif ((($inpassword ne $password)&&($userregistered ne "no"))||(($inpassword ne "")&&($userregistered eq "no"))) { &error("����������&�����������"); }
    elsif (($membercode eq "banned")||($membercode eq "masked"))      { &error("��ӻظ�&������ֹ���Ի��߷��Ա����Σ�����ϵ����Ա�����"); }
    elsif ($intopictitle eq "����������") { &error("����������&��������������⣡"); }
    elsif (length($intopictitle) > 92)   { &error("����������&������������"); }
    else  {
#	&error("����������&���������������������뷵�����ԣ�") if (($addme eq "")&&($mastpostatt eq "yes")&&($membercode ne "ad")&&($membercode ne 'smo')&&($inmembmod ne "yes"));
#	@allforums = @forums;
	$intopictitle =~ s/\(������\)$//;
	if (($inpost eq "")&&($addme eq "")) { $intopictitle.=" (������)"; }
        $intopictitle =~ s/()+//isg;
	my $tempintopictitle = $intopictitle;
	$tempintopictitle =~ s/ //g;
	$tempintopictitle =~ s/\&nbsp\;//g;
        $tempintopictitle =~ s/��//isg;
        $tempintopictitle =~ s/��//isg;
        $tempintopictitle =~ s/^����������//;
	if ($tempintopictitle eq "") { &error("����������&������������⣡"); }

        $tempaccess = "forumsallowed". "$inforum";
        $testentry = $query->cookie("$tempaccess");
        if (($allowedentry{$inforum} eq "yes")||(($testentry eq $forumpass)&&($testentry ne ""))||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }
        if (($privateforum eq "yes") && ($allowed ne "yes")) { &error("����&�Բ������������ڴ���̳����"); }

	if ($startnewthreads eq "no") {
            unless ($membercode eq "ad" ||$membercode eq 'smo'|| $inmembmod eq "yes") { &error("����������&�ڴ���̳��ֻ����̳�����߱���������������⣡"); }
	}
	elsif ($startnewthreads eq "cert") {
            unless ($membercode eq "ad" ||$membercode eq 'smo'|| $inmembmod eq "yes"||$membercode eq 'cmo'||$membercode eq 'mo'||$membercode eq 'amo'||$membercode =~ /^rz/) { &error("����������&�ڴ���̳��ֻ����̳������������֤��Ա���������⣡"); }
	}
	elsif (($startnewthreads eq "follow") &&($action eq "addnew")) {
            unless ($membercode eq "ad" ||$membercode eq 'smo'||$membercode eq 'cmo' ||$membercode eq 'mo'||$membercode eq 'amo'|| $inmembmod eq "yes") { &error("����������&�ڴ���̳��ֻ����̳�����߰������������⣡"); }
	}
	elsif (($startnewthreads eq "all")&&($userregistered eq "no")) { $inmembername = "$inmembername(��)"; }

	if ($deletepercent > 0 && $numberofposts + $numberofreplys > 0 && $membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo" && $membercode ne "amo" && $inmembmod ne "yes") {
	    &error("����������&�Բ������ɾ���ʳ�����<b>$deletepercent</b>%������Ա�������㷢�������⣡����ϵ̳�������") if ($postdel / ($numberofposts + $numberofreplys) >= $deletepercent / 100);
	}

        $inpost =~ s/\[���(.+?)�����(.+?)�༭\]//isg;
	$inpost = "\[watermark\]$inpost\[\/watermark\]" if (($intopictitle =~ /\[ԭ��\]/)&&($usewm ne "no"));

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

	undef $newthreadnumber;
	$filetoopen = "$lbdir" . "boarddata/lastnum$inforum.cgi";
	if (open(FILE, "$filetoopen")) {
	    $newthreadnumber = <FILE>;
            close(FILE);
            chomp $newthreadnumber;
	    $newthreadnumber ++;
	}
	
	if ((!(-e "${lbdir}forum$inforum/$newthreadnumber.pl"))&&($newthreadnumber =~ /^[0-9]+$/)) {
	    if (open(FILE, ">$filetoopen")) {
		flock(FILE, 2) if ($OS_USED eq "Unix");
		print FILE $newthreadnumber;
		close(FILE);
            }
	}
	else {
            opendir (DIR, "${lbdir}forum$inforum");
            my @dirdata = readdir(DIR);
            closedir (DIR);
            @dirdata = grep(/.thd.cgi$/,@dirdata);
            @dirdata = sort { $b <=> $a } (@dirdata);
            $highest = $dirdata[0];
            $highest =~ s/.thd.cgi$//;
            $newthreadnumber = $highest + 1;
            if (open(FILE, ">$filetoopen")) {
		flock(FILE, 2) if ($OS_USED eq "Unix");
		print FILE $newthreadnumber;
		close(FILE);
	    }
	}

	my $oldthreadnumber = $newthreadnumber - 1;
        if (open(FILE, "${lbdir}forum$inforum/$oldthreadnumber.thd.cgi")) {
            flock(FILE, 1) if ($OS_USED eq "Unix");
            my $threaddata =<FILE>;
            close(FILE);
            (my $amembername,my $atopictitle,my $no,my $no,my $no,my $no,my $apost,my $no) = split(/\t/, $threaddata);
	    if (($amembername eq $inmembername)&&((($apost eq $inpost)&&($apost ne "")&&($inpost ne ""))||($atopictitle eq $intopictitle))) {
	        if (open(FILE, ">${lbdir}boarddata/lastnum$inforum.cgi")) {
        	    flock(FILE, 2) if ($OS_USED eq "Unix");
        	    print FILE $oldthreadnumber;
        	    close(FILE);
        	}
	    	&error("����������&�벻Ҫ�ظ������ӣ��Ѿ������������������ͬ����������ͬ�Ķ������㷢�������ˣ�");
	    }
	}

	my $temp = &dofilter("$intopictitle\t$inpost");
	($intopictitle,$inpost) = split(/\t/,$temp);
	$intopictitle =~ s/(a|A)N(d|D)/$1&#78;$2/sg;
	$intopictitle =~ s/(a|A)n(d|D)/$1&#110;$2/sg;
	$intopictitle =~ s/(o|O)R/$1&#82;/sg;
	$intopictitle =~ s/(o|O)r/$1&#114;/sg;
#	$intopictitle  =~ s/\\/&#92;/isg;
	
	$inpost =~ s/\[UploadFile.{0,6}=(.+?)\]//isg unless (($arrowupload ne "no")||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes"));
	
	$inpost =~ s/(ev)a(l)/$1&#97;$2/isg;

        $addme= &upfileonpost(\$inpost,$inforum,$newthreadnumber);#�����ϴ���������ֵ��BT�����ж�
	&error("����������&���������������������뷵�����ԣ�") if (($addme eq "0")&&($mastpostatt eq "yes")&&($membercode ne "ad")&&($membercode ne 'smo')&&($inmembmod ne "yes"));
	$addme = "" if ($addme eq "0");
	$intopictitletemp = $intopictitle ;
	$intopictitletemp =~ s/^����������//;

        if ($moneyhidden eq "yes") { $inposttemp = "(����)"; $inpost="LBSALE[$moneypost]LBSALE".$inpost;}

	if ($inhiddentopic eq "yes") { $inposttemp = "(����)"; $inpost="LBHIDDEN[$postweiwang]LBHIDDEN".$inpost; }
	
	if ($inposttemp ne "(����)") {
	    $inposttemp = $inpost;
	    $inposttemp = &temppost($inposttemp);
	    chomp $inposttemp;
            $inposttemp = &lbhz($inposttemp,50);
        }

        if (open(FILE, ">${lbdir}forum$inforum/$newthreadnumber.pl")) {
            print FILE "$newthreadnumber\t$intopictitle\t\topen\t0\t0\t$inmembername\t$currenttime\t\t$currenttime\t$inposticon\t$inposttemp\t$addme\t";
            close(FILE);
        }

        if (open(FILE, ">${lbdir}forum$inforum/$newthreadnumber.thd.cgi")) {
            print FILE "$inmembername\t$intopictitle\t$postipaddress\t$inshowemoticons\t$inshowsignature\t$currenttime\t$inpost\t$inposticon\t$inwater\t\n";
            close(FILE);
        }

	if ($privateforum ne "yes") {
	    $filetomakeopen = "$lbdir" . "data/recentpost.cgi";
	    my $filetoopens = &lockfilename($filetomakeopen);
	    if (!(-e "$filetoopens.lck")) {
		if (-e $filetomakeopen) {
		    &winlock($filetomakeopen) if ($OS_USED eq "Nt");
		    open(FILE, "$filetomakeopen");
		    flock (FILE, 1) if ($OS_USED eq "Unix");
		    my @recentposts=<FILE>;
		    close(FILE);
		    my $checknumber = 0;
		    $maxadpost = 3 if ($maxadpost < 3);
		    if (($membercode ne "ad")&&($membercode ne "smo")&&($membercode ne "cmo")&&($membercode ne "mo")&&($membercode ne "amo")&&($membercode !~ /^rz/)) {
		        foreach (@recentposts) {
			    (my $no,$no,my $temptopic,$no,$no,my $tempmembername) = split(/\t/,$_);
			    $temptopic =~ s/^����������//;
			    $checknumber ++ if (($intopictitletemp eq $temptopic)&&(lc($tempmembername) eq lc($inmembername)));
		        }

		        if ($checknumber >= $maxadpost) {
			    &winunlock($filetomakeopen) if ($OS_USED eq "Nt");
			    unlink ("${lbdir}forum$inforum/$newthreadnumber.pl");
			    unlink ("${lbdir}forum$inforum/$newthreadnumber.thd.cgi");
	                    unlink ("${imagesdir}$usrdir/$inforum/$inforum\_${newthreadnumber}.$up_ext");

			    if (($inmembername ne "")&&($userregistered ne "no")&&($password ne "")) {
			        $memberfiletitle = $inmembername;
			        $memberfiletitle =~ s/ /\_/isg;
			        $memberfiletitle =~ tr/A-Z/a-z/;
			        my $namenumber = &getnamenumber($memberfiletitle);
			        &checkmemfile($memberfiletitle,$namenumber);
			        if (open(MEMFILE, ">${lbdir}$memdir/$namenumber/$memberfiletitle.cgi")) {
			            print MEMFILE "$inmembername\t$password\t$membertitle\tmasked\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
			            close(MEMFILE);
			        }
		                unlink ("${lbdir}cache/myinfo/$memberfiletitle.pl");
		                unlink ("${lbdir}cache/meminfo/$memberfiletitle.pl");
			    }
		            $filetomake = "$lbdir" . "data/idbans.cgi";
		            open (FILE, ">>$filetomake");
        		    print FILE "$inmembername\t";
		            close (FILE);
			    &error("����&�������ڶ������͹�棬�������Ѿ�����ֹ���ԣ�");
			}
		    }

		    $recentposts=@recentposts;
		    $maxpostreport = 31;
		    if ($recentposts<$maxpostreport) { $maxpostreport=$recentposts;} else { $maxpostreport--; }
		    
		    if (open (FILE, ">$filetomakeopen")) {
			flock (FILE, 2) if ($OS_USED eq "Unix");
			print FILE "$inforum\t$newthreadnumber\t$intopictitletemp\t$currenttime\t$inposticon\t$inmembername\t\n";
			for ($i=0;$i<$maxpostreport;$i++) { print FILE $recentposts[$i]; }
			close(FILE);
		    }
		    &winunlock($filetomakeopen) if ($OS_USED eq "Nt");
		} else {
      		    if (open (FILE, ">$filetomakeopen")) {
      			print FILE "$inforum\t$newthreadnumber\t$intopictitletemp\t$currenttime\t$inposticon\t$inmembername\t\n";
      			close(FILE);
      		    }
   		}
 	    }
	    else {
    		unlink ("$filetoopens.lck") if ((-M "$filetoopens.lck") *86400 > 30);
	    }
	}
    my $nowtime = &shortdate($currenttime + $timezone*3600);

    my $filetoopens = "$lbdir/data/todaypost.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
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
            	$nowtoday = $nowtime;
            	$yestdaypost = $todaypostno;
            	$todaypostno = 1;
    opendir (CATDIR, "${lbdir}cache");
    @dirdata = readdir(CATDIR);
    closedir (CATDIR);
    @dirdata = grep(/forumcache/,@dirdata);
    foreach (@dirdata) { unlink ("${lbdir}cache/$_"); }
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
    
        $file = "$lbdir" . "boarddata/listno$inforum.cgi";
        &winlock($file) if ($OS_USED eq "Nt");
        open (LIST, "$file");
        flock (LIST, 2) if ($OS_USED eq "Unix");
 	sysread(LIST, $listall,(stat(LIST))[7]);
        close (LIST);
	$listall =~ s/\r//isg;

    	if (length($listall) > 500) {
	    if (open (LIST, ">$file")) {
        	flock (LIST, 2) if ($OS_USED eq "Unix");
		print LIST "$newthreadnumber\n$listall";
		close (LIST);
	    }
            &winunlock($file) if ($OS_USED eq "Nt");
            if (open (LIST, ">>${lbdir}boarddata/listall$inforum.cgi")) {
                print LIST "$newthreadnumber\t$intopictitletemp\t$inmembername\t$currenttime\t\n";
            	close (LIST);
            }
	}
	else {
            &winunlock($file) if ($OS_USED eq "Nt");
	    require "rebuildlist.pl";
            my $truenumber = rebuildLIST(-Forum=>"$inforum");
            ($tpost,$treply) = split (/\|/,$truenumber);
	}

        $cleanmembername = $inmembername;
        $cleanmembername =~ s/ /\_/isg;
	$cleanmembername =~ tr/A-Z/a-z/;

	if ($jifen eq "") {
		require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
		$jifen = $numberofposts * $ttojf + $numberofreplys * $rtojf - $postdel * $deltojf;
  }
        
        if ($forumallowcount ne "no") {
	    $numberofposts++;
	    $mymoney += $forumpostmoney - $addmoney if ($forumpostmoney ne "");
	    if ($forumpostjf ne "") { $jifen += $forumpostjf; } else { $jifen += $ttojf; }
	}
        $lastpostdate = "$currenttime\%\%\%topic.cgi?forum=$inforum&topic=$newthreadnumber\%\%\%$intopictitletemp" if ($privateforum ne "yes");
        chomp $lastpostdate;

    	if (($userregistered ne "no")&&($password ne "")) {
	    $filetomake = "$lbdir" . "$memdir/$cleanmembername.cgi";
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
            } else { $threads++; }
	    my ($todayforumpost, $todayforumposttime) = split(/\|/,$todayforumpost);
	    if (($nowtime ne $todayforumposttime)||($todayforumpost eq "")) { $todayforumpost = 1; } else { $todayforumpost++; }
            $todayforumpost = "$todayforumpost|$nowtime";
            $lastposttime = "$lastposttime\%\%\%$newthreadnumber\%\%\%$intopictitletemp";
	    seek(FILE,0,0);
            print FILE "$lastposttime\t$threads\t$posts\t$todayforumpost\t$lastposter\t\n";
            close(FILE);

	    $posts = 0 if ($posts eq "");$threads = 0 if ($threads eq "");
	    open(FILE, ">${lbdir}boarddata/forumposts$inforum.pl");
	    print FILE "\$threads = $threads;\n\$posts = $posts;\n\$todayforumpost = \"$todayforumpost\";\n1;\n";
            close(FILE);
            &winunlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
            if ($threads < 10) {
    opendir (CATDIR, "${lbdir}cache");
    @dirdata = readdir(CATDIR);
    closedir (CATDIR);
    @dirdata = grep(/forumcache/,@dirdata);
    foreach (@dirdata) { unlink ("${lbdir}cache/$_"); }
            }
	}
        else {
    	    unlink ("$filetoopens.lck") if ((-M "$filetoopens.lck") *86400 > 30);
	}
	
        require "$lbdir" . "data/boardstats.cgi";
        $filetomake = "$lbdir" . "data/boardstats.cgi";
        my $filetoopens = &lockfilename($filetomake);
	if (!(-e "$filetoopens.lck")) {
	    $totalthreads++;
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

        if (($emailfunctions eq "on") && ($innotify eq "yes")) {
            if (open (FILE, ">${lbdir}forum$inforum/$newthreadnumber.mal.pl")) {
                print FILE "$inmembername\t$emailaddress\t\n";
                close (FILE);
            }
        }

        &mischeader("�����ⷢ��ɹ�");

opendir (CATDIR, "${lbdir}cache");
@dirdata = readdir(CATDIR);
closedir (CATDIR);

unlink ("${lbdir}cache/plcache$inforum\_0.pl");

        if ($refreshurl == 1) { $relocurl = "topic.cgi?forum=$inforum&topic=$newthreadnumber"; }
	                 else { $relocurl = "forums.cgi?forum=$inforum"; }
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>лл��$inmembername�������������Ѿ�����ɹ���</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������û���Զ����أ�������������ӣ�
<ul><li><a href="topic.cgi?forum=$inforum&topic=$newthreadnumber">����������</a>
<li><a href="forums.cgi?forum=$inforum">������̳</a>
<li><a href="leobbs.cgi">������̳��ҳ</a>
<li><a href="postings.cgi?action=locktop&forum=$inforum&topic=$newthreadnumber">������̶�</a>
<li><a href="postings.cgi?action=catlocktop&forum=$inforum&topic=$newthreadnumber">���������̶�</a>
<li><a href="postings.cgi?action=abslocktop&forum=$inforum&topic=$newthreadnumber">�������̶ܹ�</a>
</ul></tr></td></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=$relocurl">
	~;
    }
1;
