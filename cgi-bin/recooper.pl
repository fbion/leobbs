#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

sub addadminlog {
	my ($message, $intopic) = @_;
	my $logtime = time;
	my $trueipaddress = $ENV{"HTTP_CLIENT_IP"};
	$trueipaddress = $ENV{"HTTP_X_FORWARDED_FOR"} if ($trueipaddress eq "" || $trueipaddress =~ m/a-z/i || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);
	$trueipaddress = "no" if ($trueipaddress eq "" || $trueipaddress =~ m/a-z/i || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);

	my $filetomake = "${lbdir}boarddata/adminlog$inforum.cgi";
	&winlock($filetomake) if ($OS_USED eq "Nt");
	open(FILE, ">>$filetomake");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	print FILE "$inmembername\t$logtime\t$intopic\t$ENV{'REMOTE_ADDR'}\t$trueipaddress\t$message\n";
	close(FILE);
	&winunlock($filetomake) if ($OS_USED eq "Nt");
	return;
}
1;
