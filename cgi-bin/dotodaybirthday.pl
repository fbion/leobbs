#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

my $lockfile = "$lbdir" . "lock/birthday.lck";
if (!(-e $lockfile)) {
    open (LOCKBIRTH, ">$lockfile");
    close (LOCKBIRTH);

    undef @birthdaytoday;
    open (MEMFILE, "${lbdir}data/lbmember3.cgi");
    my @memberdata = <MEMFILE>;
    close (MEMFILE);

    foreach (@memberdata) {
    	chomp $_;
    	(my $users, my $borns) = split(/\t/,$_);
    	(my $unowy, my $unowm, my $unowd) = split(/\//, $borns);
    	if (($nowm eq $unowm)&&($nowd eq $unowd)) {
            my $usersfilename = $users;
            $usersfilename =~ s/ /\_/g;
            $usersfilename =~ tr/A-Z/a-z/;
            $usersfilename =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
            $unowy = $nowy - $unowy;
            $unowy = $unowy - 1900 if ($unowy > 1900);
            push(@birthdaytoday, "$users\t$usersfilename\t$unowy\t\n");
            if ($sendtobirthday eq "yes") {
               	open (FILE, "${lbdir}$msgdir/in/${usersfilename}_msg.cgi");
		sysread(FILE, my $inboxmessages,(stat(FILE))[7]);
               	close (FILE);
	        $inboxmessages =~ s/\r//isg;
               	open (FILE, ">${lbdir}$msgdir/in/${usersfilename}_msg.cgi");
               	print FILE "����������ȫ�������Ա\tno\t$currenttime\t��$boardname��ף�����տ��֣�\t�������� $unowy ������,��$boardname��ף�����տ��֣�\n$inboxmessages";
                close (FILE);
            }
    	}
    }
    
    chomp @birthdaytoday;
    foreach (@birthdaytoday) {
      	next if ($_ eq "");
	(my $users,my $usersfilename,my $unowy) = split(/\t/,$_);
	next if ($users eq "");
	$birthdayuser .= qq~<span style=cursor:hand onClick=javascript:O9('~ . uri_escape($usersfilename) . qq~') title=ף$unowy�����տ��֣�>$users</span>, ~;
    }
    chop $birthdayuser;
    chop $birthdayuser;
    $borncount = @birthdaytoday;
            
    open (BDILE, ">${lbdir}data/birthdaytoday.cgi");
    print BDILE "#$nowtime\n";
    print BDILE qq~$birthdayuser\n~;
    print BDILE qq~$borncount\n~;
    close (BDILE);
    unlink($lockfile);
} else {
    (my $sec,my $no) = localtime($currenttime);
    $sec = int($sec/15);
    unlink($lockfile) if ($sec == 2);
    $birthdayuser="";
    $borncount=0;
}
1;
