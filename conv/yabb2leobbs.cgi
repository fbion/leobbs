#!/usr/bin/perl

##########################################
# YaBB �û����� --> LeoBBS �û�����ת����#
##########################################

$yabbdir   = "/path/to/YaBB members dir/";	#YaBB �û�Ŀ¼�����Ҫ��© / 
$leobbsdir = "/path/to/LeoBBS members dir/"; 	#LeoBBS �û�Ŀ¼�����Ҫ��© / ��ע������ 777 ����

print "Content-type: text/html\n\n";
print "YaBB --> LeoBBS �û�����ת����<BR><BR>\n";

opendir (DIR, "$yabbdir");
@dirdata = readdir(DIR);
closedir (DIR);

@yabbers = grep(/dat/,@dirdata);
$time = time;

foreach (@yabbers) {
    open (YABB, "$yabbdir/$_");
    @member = <YABB>;
    close (YABB);

    $username = $_;
    $username =~ s/\.dat//g;

    foreach (@member) {
        chomp $_;
        }
    $membercode = "me";
    $password = $member[0];
    $name     = $member[1];
    $email    = $member[2];
    $www      = $member[4];
    $sig      = $member[5];
    $posts    = $member[6];
    $title    = $member[7];
    $icq      = $member[8];

    $sig =~ s/\&\&/<br>/g;

    if ($title ne "Administrator") { $title = "Member"; $membercode = "me"; }
    else { $membercode = "ad"; }

    $name = y/ /_/;

    my $filename = "$leobbsdir" . "$name" . ".cgi";
    open (IKON, ">$filename");
    print IKON "$name\t$password\t$title\t$membercode\t$posts\t$email\tyes\txxx.xx.xxx.xx\t$www\t\t$icq\t\t\t$time\t\%\%\%$time\%\%\%\t$sig\t0\t\t\t\t\t\t\t\t\t\n";
    close (IKON);
    $membercount ++;
    $lastmember = "$username";
    print "�û� $username �Ѿ��ɹ�ת���� LeoBBS �û��ˣ�<BR><BR>";
    $www = ""; $sig = ""; $icq = "";
    }
    
    print "�ܹ�ת���� $newtotal ���û���<BR><BR>\n";
    exit;




