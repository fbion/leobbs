#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

open(FILE, "${lbdir}data/allforums.cgi");
@forums = <FILE>;
close(FILE);
$totle1 = 0; $totle2 = 0;
foreach $forum (@forums) {
    chomp $forum;
    next if (length("$forum") < 30);
    (my $tempno,my $no) = split(/\t/,$forum);
    next if ($tempno !~ /^[0-9]+$/);
    eval{ require "${lbdir}boarddata/forumposts$tempno.pl";};
    $totle1 += $threads; $totle2 += $posts;
}
opendir (DIRS, "$lbdir");
my @memdir = readdir(DIRS);
closedir (DIRS);
@memdir = grep(/^\w+?$/i, @memdir);
@memdir = grep(/^members/i, @memdir);
my $memdir = $memdir[0];

opendir (DIR, "${lbdir}$memdir/old"); 
my @filedata = readdir(DIR);
closedir (DIR);
my @countvar = grep(/\.cgi$/i,@filedata);
$newtotalmembers = @countvar;

open(FILE, ">${lbdir}data/boardstats.cgi");
print FILE "\$lastregisteredmember = \'nodisplay\'\;\n";
print FILE "\$totalmembers = \'$newtotalmembers\'\;\n";
print FILE "\$totalthreads = \'$totle1\'\;\n";
print FILE "\$totalposts = \'$totle2\'\;\n";
print FILE "\n1\;";
close (FILE);
1;
