#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

# ���� -1��û���û�
# ���� 0 ���û����������⣬д��ʧ��
# ���� 1 ���ɹ�

sub updateuserinfo {  #���ñ仯���������û���Ϣ
    my($nametocheck,$cposts, $creplys, $crating,$cjin1yan,$cmei1li,$cmoney,$cpostdel,$cjhcount,$conlinetime,$cjifen) = @_;
#     �û������������仯�����ظ����仯���������仯��������仯��(����)�������仯��(����)����Ǯ�仯�������ӱ�ɾ�����仯�����������仯��������ʱ��仯�������ֱ仯��

    $cposts     = 0 if ($cposts      eq "");
    $creplys    = 0 if ($creplys     eq "");
    $crating    = 0 if ($crating     eq "");
    $cmoney     = 0 if ($cmoney      eq "");
    $cpostdel   = 0 if ($cpostdel    eq "");
    $cjhcount   = 0 if ($cjhcount    eq "");
    $conlinetime= 0 if ($conlinetime eq "");
    $cjifen     = 0 if ($cjifen eq "");

    my $nametochecktemp = $nametocheck;
    $nametocheck =~ s/ /\_/g;
    $nametocheck =~ tr/A-Z/a-z/;
    $nametocheck =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
    $userregistered = "";
    my $namenumber = &getnamenumber($nametocheck);
    &checkmemfile($nametocheck,$namenumber);
    my $filetoopen = "${lbdir}$memdir/$namenumber/$nametocheck.cgi";
    if (-e $filetoopen) {
	&winlock($filetoopen) if ($OS_USED eq "Nt");
	open(FILE,"+<$filetoopen");
	flock (FILE, 2) if ($OS_USED eq "Unix");
        my $filedata = <FILE>;
	chomp($filedata);
	(my $membername, my $password, my $membertitle, my $membercode, my $numberofposts, my $emailaddress, my $showemail, my $ipaddress, my $homepage, my $oicqnumber, my $icqnumber ,my $location ,my $interests, my $joineddate, my $lastpostdate, my $signature, my $timedifference, my $privateforums, my $useravatar, my $userflag,my  $userxz, my $usersx, my $personalavatar, my $personalwidth, my $personalheight, my $rating, my $lastgone, my $visitno,my  $useradd04,my  $useradd02, my $mymoney, my $postdel, my $sex, my $education, my $marry, my $work, my $born, my $chatlevel,my  $chattime, my $jhmp,my $jhcount,my $ebankdata,my $onlinetime,my $userquestion, my $awards, my $jifen, my $userface, my $soccerdata, my $useradd5) = split(/\t/,$filedata);
	$membercode ||= "me";

	(my $totleposts, my $totlecreplys) = split(/\|/,$numberofposts);

	$totleposts   += $cposts;
	$totlecreplys += $creplys;
	$totleposts   = 0 if($totleposts   < 0);
	$totlecreplys = 0 if($totlecreplys < 0);
	$numberofposts = "$totleposts|$totlecreplys";

	$rating     += $crating;
	$mymoney    += $cmoney;
	$postdel    += $cpostdel;
	$jhcount    += $cjhcount;
	$onlinetime += $conlinetime;
	$jifen      += $cjifen;

	$onlinetime = 0 if ($onlinetime < 0);
	$jhcount    = 0 if ($jhcount < 0);
	$postdel    = 0 if ($postdel < 0 );
	$rating     = -5 if ($rating < -5);
	$rating     = $maxweiwang  if ($rating >  $maxweiwang);

	unlink ("${lbdir}cache/meminfo/$nametocheck.pl");
	unlink ("${lbdir}cache/myinfo/$nametocheck.pl");

	if (($membername ne "")&&($password ne "")) {
	    seek(FILE,0,0);
	    print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t\n";
	    close(FILE);
	    if (((-M "${lbdir}$memdir/old/$nametocheck.cgi") > 0.5)||(!(-e "${lbdir}$memdir/old/$nametocheck.cgi"))) {
	        open(FILE,">${lbdir}$memdir/old/$nametocheck.cgi");
	        print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t\n";
	        close(FILE);
	    }
	    &winunlock($filetoopen) if ($OS_USED eq "Nt");
	    return 1;
	} else {
	    close(FILE);
	    &winunlock($filetoopen) if ($OS_USED eq "Nt");
	    return 0;
	}
    }
    else {
        return -1;
    }
}

sub upinfodata {  #�����û��ļ�����κ��ֶ�(ɢ�з�ʽ,�û������ܸ��£�������º�������)
    my %infos = @_;                      #��ȡ���������ɢ��
    my $nametocheck = $infos{name};      #�û�����
    return -1 if ($nametocheck eq "");   #û�����֣����� -1

    $nametocheck =~ s/ /\_/g;
    $nametocheck =~ tr/A-Z/a-z/;
    $nametocheck =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
    my $namenumber = &getnamenumber($nametocheck);
    &checkmemfile($nametocheck,$namenumber);
    my $filetoopen = "${lbdir}$memdir/$namenumber/$nametocheck.cgi";
    if ((-e $filetoopen)&&($nametocheck !~ /^����/)&&($nametocheck ne "")) {
	&winlock($filetoopen) if ($OS_USED eq "Nt");
	open(FILE,"+<$filetoopen");
	flock (FILE, 2) if ($OS_USED eq "Unix");
        my $filedata = <FILE>;
	chomp($filedata);
	local ($membername, $password, $membertitle, $membercode, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber ,$location ,$interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp,$jhcount,$ebankdata,$onlinetime,$userquestion,$awards,$jifen,$userface, $soccerdata, $useradd5) = split(/\t/,$filedata);
	($numberofposts, local $numberofreplys) = split(/\|/,$numberofposts);
	$numberofposts ||= "0";
	$numberofreplys ||= "0";
	$membercode ||= "me";
	$jhcount = "0" if ($jhcount <= 0);
	$jhcount ||= "0";
	$onlinetime = "3000" if ($onlinetime < 0);
	for ('password','membertitle','membercode','numberofposts','numberofreplys','emailaddress','showemail','ipaddress','homepage','oicqnumber','icqnumber','location','interests','joineddate','lastpostdate','signature','timedifference','privateforums','useravatar','userflag','userxz','usersx','personalavatar','personalwidth','personalheight','rating','lastgone','visitno','useradd04','useradd02','mymoney','postdel','sex','education','marry','work','born','chatlevel','chattime','jhmp','jhcount','ebankdata','onlinetime','userquestion','awards','jifen','userface','soccerdata','useradd5') {
	    ${$_} = $infos{$_} if ($infos{$_} ne ""); #��ȡ������������������ı���������᣺��
	}
	if (($membername ne "")&&($password ne "")) {
	    seek(FILE,0,0);
	    print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t\n";
	    close(FILE);
	    &winunlock($filetoopen) if ($OS_USED eq "Nt");
	    if (((-M "${lbdir}$memdir/old/$nametocheck.cgi") > 0.5)||(!(-e "${lbdir}$memdir/old/$nametocheck.cgi"))) {
	        open(FILE,">${lbdir}$memdir/old/$nametocheck.cgi");
		print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t\n";
	        close(FILE);
	    }
   	    unlink ("${lbdir}cache/meminfo/$nametocheck.pl");
	    unlink ("${lbdir}cache/myinfo/$nametocheck.pl");
	    return 1;
	}
        else { close(FILE); &winunlock($filetoopen) if ($OS_USED eq "Nt"); return 0; }
    }
    else {
        return -1;
    }
}

1;
