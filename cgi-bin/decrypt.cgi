#!/usr/bin/perl
#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
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

use LBCGI;
$LBCGI::POST_MAX = 200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$query = new LBCGI;
&error("���ӳ���&�Բ��𣬲�����ʹ�� GET ���ᣡ") unless ($ENV{'REQUEST_METHOD'} =~ /^POST$/i);
&error("���ӳ���&�Բ��𣬲�����Ǳ���̳�������ᣡ") if ($ENV{'HTTP_REFERER'} !~ /$ENV{'HTTP_HOST'}/ && $ENV{'HTTP_HOST'} ne '' && $ENV{'HTTP_REFERER'} ne '');
$inforum        = $query -> param('forum');
$intopic        = $query -> param('topic');
$inpostno       = $query -> param('postno');
$decrypt        = $query -> param('clno');
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($intopic !~ /^[0-9]+$/)||($inforum !~ /^[0-9]+$/)||($inpostno !~ /^[0-9]+$/)||($decrypt !~ /^[0-9]+$/));
$inmembername = $query->cookie("amembernamecookie");
$inpassword   = $query->cookie("apasswordcookie");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ�ʽѽ����") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;
if ((!$inmembername) or ($inmembername eq "����")) {
    &error("��ͨ����&����Ϊ����̳�û����ɽ��룬�����µ�¼��");
}else {
    &getmember("$inmembername","no");
    &error("��ͨ����&�������û���������������µ�¼��") if ($inpassword ne $password);
    &error("��ͨ����&�û�û�е�¼��ע�ᣡ") if ($userregistered eq "no");
}
my $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
if (open(FILE, "$filetoopen")) {
    @threads = <FILE>;
    close(FILE);
    chomp @threads;
}
else {
    &error("���ӳ���&�Ҳ����ñ�ŵ����ᣬ��ȷ��������һ����Ч�����ӣ�");
}
$get_the_post=$threads[$inpostno];
@split_the_post=split(/\t/,$get_the_post);
$post_text=$split_the_post[6];
if($post_text=~/\[curl=\s*(http|https|ftp):\/\/(.*?)\s*\]/i){
$post_text="#$post_text";
$post_text=~s/\n//sg;
@clinklist=();$clinkcount=0;
$post_text =~ s/\[curl=\s*(http|https|ftp):\/\/(.*?)\s*\]/\n\$clinklist[\$clinkcount]="$1:\/\/$2";\n\$clinkcount++;\n\#/isg;
eval($post_text);
$get_the_link=$clinklist[$decrypt];
chomp $get_the_link;
}
$get_the_link=$clinklist[$decrypt];
chomp $get_the_link;
&error("���ӳ���&�Ҳ����ñ�ŵ����ᣬ��ȷ��������һ����Ч�����ӡ�") if($get_the_link eq "");
if($get_the_link=~m/^(http|https|ftp):\/\//i){
print header(-charset=>gb2312,-location=>$get_the_link,-expires=>now,-cache=>yes);
}else{
&error("���ӳ���&�ñ�ŵ����᲻��֧�ֵ�ͨѶЭ����������ֻ֧�� HTTP,HTTPS �� FTP ��");
}
exit;
