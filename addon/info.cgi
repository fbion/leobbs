#!/usr/bin/perl
###################################################
# LeoBBS ��ҳ��ʾ��̳��Ϣ ver 2.0
###################################################
# ʹ�ð취�� info.cgi
# ���� ������ҳ���ʵ�λ�ü����������
#      <script src="info.cgi"></script>
#      �����Ϳ�������Ӧλ����ʾ������̳��һЩ��Ϣ
#
#   �������Ҫ��ʾ��ô��ϸ�����Լ��������������
#   ������֣�ɾ������Ҫ��ʾ���У��Ϳ����ˡ�
###################################################

#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
#  ����ɽӥ��������ȱ������ LB5000 XP 2.30 ��Ѱ�   #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBoard.com/          #
#      ��̳��ַ�� http://www.LeoBBS.com/            #
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

#unless ($ENV{'HTTP_REFERER'} =~ /$ENV{'HTTP_HOST'}/) {
#print "Content-Type:text/html\n\n";
#print "document.write('<font color=red>���Բ��𣬲�����Ǳ���̳�������ã�</font>');";
#exit;
#}
use LBCGI;
require "data/boardinfo.cgi";
require "data/boardstats.cgi";
require "bbs.lib.pl";

$|++;

$query = new LBCGI;
$thisprog = "info.cgi";
print "Content-type: text/html\n\n";

my $filetoopen = "$lbdir" . "data/onlinedata.cgi";
&winlock($filetoopen) if (($OS_USED eq "Unix")||($OS_USED eq "Nt"));
open(FILE,"$filetoopen");
flock (FILE, 1) if ($OS_USED eq "Unix");
my @onlinedata1 = <FILE>;
close(FILE);
&winunlock($filetoopen) if (($OS_USED eq "Unix")||($OS_USED eq "Nt"));
$total_users = @onlinedata1;

$filetomake = "$lbdir" . "data/counter.cgi";
&winlock($filetomake) if (($OS_USED eq "Unix")||($OS_USED eq "Nt"));
open(FILE,"$filetomake");
flock (FILE, 1) if ($OS_USED eq "Unix");
my $count = <FILE>;
close(FILE);
&winunlock($filetomake) if (($OS_USED eq "Unix")||($OS_USED eq "Nt"));
($count1,$count2,$onlinemax1,$onlinemaxtime1) = split(/\t/, $count);
	
$all= $totalthreads+$totalposts;
$cleanlastregistered = $lastregisteredmember;
$cleanlastregistered =~ y/ /_/;
$cleanlastregistered =~ tr/A-Z/a-z/;
$cleanlastregistered = qq~<a href=$boardurl/profile.cgi?action=show&member=~ . ($uri_escape eq "no" ? $cleanlastregistered : uri_escape($cleanlastregistered)) . qq~ target=_blank>$lastregisteredmember</a>~;
$onlinemaxtime1 =&dateformatshort($onlinemaxtime1 + ($timezone*3600) + ($timedifferencevalue*3600));

$str = "";
$str.= "��������: $total_users<br>";
$str.= "�ܷ�����: $count1<br>";
$str.= "�ܵ����: $count2<br>";
$str.= "���߷�ֵ: $onlinemax1<br>";
$str.= "��ֵʱ��: $onlinemaxtime1<br>";
$str.= "ע���Ա: $totalmembers<br>";
$str.= "��������: $totalthreads<br>";
$str.= "�ظ�����: $totalposts<br>";
$str.= "��������: $all<br>";
$str.= "������: $cleanlastregistered<br>";
print "document.write('$str')\n";
exit;
sub dateformatshort {
    my $time = shift;
    (my $sec,my $min,my $hour,my $mday,my $mon,my $year,my $wday,my $yday,my $isdst) = localtime($time);
    my @months = ('01','02','03','04','05','06','07','08','09','10','11','12');
    $mon = $months[$mon];
    if ($hour < 10) { $hour = "0$hour"; }
    if ($mday < 10) { $mday = "0$mday"; }
    if ($min < 10) { $min = "0$min"; }
    if ($sec < 10) { $sec = "0$sec"; }
    $year = $year + 1900;
    return "$year/$mon/$mday $hour:$min";
}

sub winlock{
    my ($lockfile) = shift;
    my $i = 0;
    $lockfile =~ s/\\/\//isg;
    $lockfile =~ s/\://isg;
    $lockfile =~ s/\//\_/isg;
    $lockfile = "$lbdir" . "lock/$lockfile";
    while (-e "$lockfile.lck") {
	last if ($i >= 177);
	select(undef,undef,undef,0.1);
	$i++;
    }
    open (LOCKFILE, ">$lockfile.lck");
    close (LOCKFILE);
}
sub winunlock{
    my ($lockfile) = shift;
    $lockfile =~ s/\\/\//isg;
    $lockfile =~ s/\://isg;
    $lockfile =~ s/\//\_/isg;
    $lockfile = "$lbdir" . "lock/$lockfile";
#    chmod(0777,"$lockfile.lck");
    unlink("$lockfile.lck");
}
