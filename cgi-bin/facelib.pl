#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

$mansex = "0-0-0-0-0-0-0-init-init-init-0-init-0-init-init-0-0-0-init-0-0-0-0-0-0-0";
$fairsex = "0-0-0-0-0-0-0-initf-initf-initf-0-initf-0-initf-initf-0-0-0-initf-0-0-0-0-0-0-0";

sub readface {
    my ($nametocheck,$read_type) = @_;
    &getmember("$nametocheck","no") if($read_type eq '1');

    if($userface eq '')
    {
	$currequip = $sex eq 'f' ? $fairsex : $mansex;
	@currequip = split(/-/,$currequip);
	@buy_sp = (B,,,,,,,,,,,,,,,,,,,,,,,,,);
	$loadface = 'n';
    }
    else
    {
	@FaceInfo = split(/\|/,$userface);	# ������������
	$currequip = @FaceInfo[0];	# ��ǰװ��
	$allequip = @FaceInfo[1];	# ����װ�����
	$loadface  = @FaceInfo[2];	# �Ƿ�ʹ����������

	@currequip = split(/\-/,$currequip);
	@buy_sp = split(/\-/,$allequip);
	unshift(@buy_sp,"B");
    }
}

sub upplugdata	# ����ָ���ֶ�����
{
    my ($nametocheck,$facedata,$moneydata) = @_;    # �û����������������ݡ��ֽ�

    $nametocheck =~ s/ /\_/g;
    $nametocheck =~ tr/A-Z/a-z/;
    $nametocheck =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
    my $namenumber = &getnamenumber($nametocheck);
    &checkmemfile($nametocheck,$namenumber);
    my $filetoopen = "${lbdir}$memdir/$namenumber/$nametocheck.cgi";
    if (-e $filetoopen)
    {
	&winlock($filetoopen) if ($OS_USED eq "Nt");
	open(FILE,"+<$filetoopen");
	flock(FILE, 2) if ($OS_USED eq "Unix");
        my $filedata = <FILE>;
	chomp($filedata);
	(my $membername, my $password, my $membertitle, my $membercode, my $numberofposts, my $emailaddress, my $showemail, my $ipaddress, my $homepage, my $oicqnumber, my $icqnumber ,my $location ,my $interests, my $joineddate, my $lastpostdate, my $signature, my $timedifference, my $privateforums, my $useravatar, my $userflag,my  $userxz, my $usersx, my $personalavatar, my $personalwidth, my $personalheight, my $rating, my $lastgone, my $visitno,my  $useradd04,my  $useradd02, my $mymoney, my $postdel, my $sex, my $education, my $marry, my $work, my $born, my $chatlevel,my  $chattime, my $jhmp,my $jhcount,my $ebankdata,my $onlinetime,my $userquestion,my $awards,my $jifen,my $userface, my $soccerdata, my $useradd5) = split(/\t/,$filedata);

	if (($membername ne "")&&($password ne ""))
	{
		if ($facedata ne '')		# $facedata = clear : ɾ��ԭ���� ��:����ԭ���� ����������������
		{
		    $userface = ($facedata ne 'clear') ? $facedata : "";
		}

		$mymoney += $moneydata if($moneydata ne '');	# �����Ϊ�գ����ֽ����������

		seek(FILE,0,0);
		print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t\n";
		close(FILE);
	      if (open(FILE,">${lbdir}$memdir/old/$nametocheck.cgi")) {
		print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t\n";
	        close(FILE);
	      }
            unlink ("${lbdir}cache/myinfo/$nametocheck.pl");
            unlink ("${lbdir}cache/meminfo/$nametocheck.pl");
	} else {
            close(FILE);
	}
	&winunlock($filetoopen) if ($OS_USED eq "Nt");
    }
}

sub errorout
{
    my $errormsg = shift;
    ($errortitle,$errorcon,$errortype) = split(/\&/, $errormsg);	# ������⡢������ʾ����ʾ����
    if($errortype eq 1)
    {
	print qq~<title>$errortitle</title><script>alert("����$errortitle\\n\\nԭ��$errorcon");self.close();</script>~;
    }
    else
    {
	print qq~<title>$errortitle</title><script>alert("����$errortitle\\n\\nԭ��$errorcon");history.back();</script>~;
    }
    exit;
}

sub write_messages
{
    my ($sendcorp,$rename, $temptopic, $tempcontent) = @_;	# ���������ơ����������ơ����⡢����
    my $filetoopen = "$lbdir". "$msgdir/in/$rename" . "_msg.cgi";
    $filetoopen = &stripMETA($filetoopen);
    open (FILE, "$filetoopen");
    sysread(FILE, my $messanges,(stat(FILE))[7]);
    close(FILE);
    $messanges =~ s/\r//isg;

    open (FILE, ">$filetoopen");
    print FILE "����������$sendcorp\tno\t$currenttime\t$temptopic\t$tempcontent\n$messanges";
    close (FILE);
    return;
}
