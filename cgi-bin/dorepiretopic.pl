#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

$threadposts = @threads; $threadposts --;
my $postfirst = $threads[0];
$postfirst =~ s/[\a\f\n\e\0\r]//isg;
my $postlast = $threads[-1];
$postlast =~ s/[\a\f\n\e\0\r]//isg;
($startedby, $topictitle, my $postipaddress1, my $showemoticons1, my $showsignature1, $startedpostdate, my $post1, $posticon) = split(/\t/,$postfirst);
($lastposter, my $topictitle2, my $postipaddress2, my $showemoticons2, my $showsignature2, $lastpostdate, $inposttemp, my $posticon2) = split(/\t/,$postlast);
$topictitle =~ s/^����������//;
if ($topictitle eq "") { $topictitle = $topictitle2; $topictitle =~ s/^����������//; }
$topictitle = "����������$topictitle";
$topicid = $intopic;

if ($post1 =~ /.*?\[UploadFile.{0,6}=(.+?)\].*?/i) {
    ($no , $addmetype) = split(/.*\./,$1);
} else {
    $addmetype = "";
}

$threadviews = ($threadposts+1) * 8 if ($threadviews eq "");
$lastposter  = "" if ($threadposts eq 0);
$inposttemp  = "(����)" if ($inposttemp=~/LBHIDDEN\[(.*?)\]LBHIDDEN/sg);
$inposttemp  = "(����)" if ($inposttemp=~/LBSALE\[(.*?)\]LBSALE/sg);
$inposttemp  = &temppost($inposttemp);
$inposttemp  = &lbhz($inposttemp, 50);

chomp $posticon;
$posticon =~ s/\s//isg;
if ($posticon =~/<br>/i) {
    $posticon =~ s/<br>/\t/ig;
    my @temppoll = split(/\t/, $posticon);
    if ($#temppoll >= 1) { $posticon = "<br>"; } else { $posticon = ""; }
}
if (($posticon =~ m/<br>/i)&&($threadstate ne "poll")&&($threadstate ne "pollclosed")) { $threadstate = "poll"; }
                                                                                  else { $threadstate="open" if ($threadstate eq ""); }
1;
