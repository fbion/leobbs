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
$LBCGI::POST_MAX=800000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "code.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "bbs.lib.pl";
require "plugin.lib.pl";
$|++;       
$thisprog = "buypost.cgi";
$query = new LBCGI;

for ('postnumber','moneynumber','inforum','intopic','salemembername') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
$salemembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]]//isg;
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ1��") if ($postnumber !~ /^[0-9]+$/);
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if ($intopic !~ /^[0-9]+$/);
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if ($inforum !~ /^[0-9]+$/);
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($moneynumber < 0)||($moneynumber > 99999));
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if ($salemembername eq "");
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

&error("����&�벻Ҫ���ⲿ���ӱ�����") if (($ENV{'HTTP_REFERER'} !~ /$ENV{'HTTP_HOST'}/i && $ENV{'HTTP_REFERER'} ne '' && $ENV{'HTTP_HOST'} ne '')&&($canotherlink ne "yes"));

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

if ($inmembername eq "" || $inmembername eq "����" ) {
    &error("��ͨ����&�Բ�����Ŀǰ������Ƿÿͣ����ܽ��룬���ȵ�¼!");
    exit;
} else {
#    &getmember("$inmembername");
    &getmember("$inmembername","no");
    &error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
     if ($inpassword ne $password) {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("��ͨ����&�������û���������������µ�¼��");
     }
}
$mvmoney = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
if ($mvmoney < $moneynumber){ &error("��������ʧ��&�ϴ����Ǯ������������Ӱ���");exit;}
if (lc($salemembername) eq lc($inmembername)) { &error("��������ʧ��&�ϴ����Լ����Լ���������ʲô����");exit; }

open (FILE, "${lbdir}forum$inforum/$intopic.thd.cgi");
my @threads = <FILE>;
close (FILE);

(my $membername1, my $no, $no, $no, $no, $no, my $post1, $no) = split(/\t/,$threads[$postnumber]);
$post1 =~ s/LBSALE\[(.*?)\]LBSALE//sg;
$buym = int($1);
&error("��������ʧ��&�������������⣬���ܽ���������") if ((lc($membername1) ne lc($salemembername))||($buym eq "")||($buym ne $moneynumber));

open (FILE, "${lbdir}$saledir/$inforum\_$intopic\_$postnumber.cgi");
$allbuyer = <FILE>;
close (FILE);
chomp $allbuyer;
$allbuyer = "\t$allbuyer\t";
$allbuyer =~ s/\t\t/\t/;
&error("��������ʧ��&���Ѿ���������������ˣ���ˢ�����ӾͿ��Կ����ģ���") if ($allbuyer =~ /\t$inmembername\t/i);

open (FILE, ">>${lbdir}$saledir/$inforum\_$intopic\_$postnumber.cgi");
print FILE "$inmembername\t";
close (FILE);

&updateuserinfo("$inmembername",0,0,0,0,0,-$moneynumber,0);
$moneynumber1 = $moneynumber;
$moneynumber1 = int($moneynumber - $moneynumber * $postcess / 100) if ($postcess ne '' && $postcess >= 1 && $postcess <= 100);
&updateuserinfo("$salemembername",0,0,0,0,0,$moneynumber1,0);
$inmembername =~ s/ /\_/isg;
$inmembername =~ tr/A-Z/a-z/;
unlink ("${lbdir}cache/myinfo/$inmembername.pl");
unlink ("${lbdir}cache/meminfo/$inmembername.pl");
$salemembername =~ s/ /\_/isg;
$salemembername =~ tr/A-Z/a-z/;
unlink ("${lbdir}cache/myinfo/$salemembername.pl");
unlink ("${lbdir}cache/meminfo/$salemembername.pl");

$mvmoney = $mvmoney - $moneynumber;

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&mischeader("�������ӳɹ�");

$output .= qq~<SCRIPT>valignend()</SCRIPT><table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 border=0 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>�㸶�� $moneynumber $moneyname����ʣ�� $mvmoney $moneyname��</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������û���Զ����أ�������������ӣ�
<ul><li><a href="topic.cgi?forum=$inforum&topic=$intopic">���ظ�����</a>
</ul></tr></td></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=topic.cgi?forum=$inforum&topic=$intopic">
~;
&output("$boardname - ��$forumname�ڹ�������",\$output);
exit;
