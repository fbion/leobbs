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
$LBCGI::POST_MAX=1024 * 10000;
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;
$thisprog = "addpost.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");
$query = new LBCGI;
if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else {
    $boardurltemp =$boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
}
for ('forum','topic','membername','password','inpost','id') {
    next unless defined $_;
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
$num = $id;
$inforum       = $forum;
$intopic       = $topic;
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ����") if ($inforum !~ /^[0-9]+$/);
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

$inmembername  = $membername;
$inpassword    = $password;
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}
$currenttime   = time;
$inpost        =~ s/LBHIDDEN/LBHIDD\&\#069\;N/sg;
$inpost        =~ s/LBSALE/LBSAL\&\#069\;/sg;
$inpost        =~ s/\[DISABLELBCODE\]/\[DISABLELBCOD\&\#069\;\]/sg;
$inpost        =~ s/\[USECHGFONTE\]/\[USECHGFONT\&\#069\;\]/sg;
$inpost        =~ s/\[POSTISDELETE=(.+?)\]/\[POSTISDELET\&\#069\;=$1\]/sg;
$inpost        =~ s/\[ADMINOPE=(.+?)\]/\[ADMINOP\&\#069\;=$1\]/sg;
$inpost        =~ s/\[ALIPAYE\]/\[ALIPAY\&\#069\;\]/sg;
$inpost = &dofilter("$inpost");
$inpost =~ s/(ev)a(l)/$1&#97;$2/isg;

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie"); }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
&ipbanned; #��ɱһЩ ip
if (($num) && ($num !~ /^[0-9]+$/)) { &error("��ͨ&�ϴ󣬱��Һ��ҵĳ���ѽ������"); }
if (!(-e "${lbdir}boarddata/listno$inforum.cgi")) { &error ("����������&�Բ��������̳�����ڣ����ȷ������̳����û����ô�����������޸���̳һ�Σ�"); }
if ($inmembername eq "" || $inmembername eq "����" ) {
    $inmembername = "����";
    $userregistered = "no";
} else {
    &getmember("$inmembername");
    &error("��ͨ����&���û����������ڣ�") if ($inpassword ne "" && $userregistered eq "no");
     if ($inpassword ne $password && $userregistered ne "no") {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("��ͨ����&�������û���������������µ�¼��");
     }
}
&doonoff;
$mymembercode=$membercode;
if ($inpost eq"")  { &error("��ӻظ�&������Ҫ��д�����ݣ�"); }
if (($membercode eq "banned")||($membercode eq "masked"))      { &error("��ӻظ�&������ֹ���Ի��߷��Ա����Σ�����ϵ����Ա�����"); }
$myrating=$rating;
$myrating="-6" if !($myrating);
$maxpoststr = "" if ($maxpoststr eq 0);
$maxpoststr = 100 if (($maxpoststr < 100)&&($maxpoststr ne ""));
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&moderator("$inforum");
&error("������̳&�����̳��û��Ȩ�޽�����̳��") if ($yxz ne '' && $yxz!~/,$membercode,/);
if ($allowusers ne ''){
    &error('������̳&�㲻����������̳��') if (",$allowusers," !~ /,$inmembername,/i && $membercode ne 'ad');
}
if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
    &error("������̳&�㲻����������̳���������Ϊ $rating��������ֻ̳���������ڵ��� $enterminweiwang �Ĳ��ܽ��룡") if ($enterminweiwang > 0 && $rating < $enterminweiwang);
    if ($enterminmony > 0 || $enterminjf > 0 ) {
	require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
	$mymoney1 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
	&error("������̳&�㲻����������̳����Ľ�ǮΪ $mymoney1��������ֻ̳�н�Ǯ���ڵ��� $enterminmony �Ĳ��ܽ��룡") if ($enterminmony > 0 && $mymoney1 < $enterminmony);
	&error("������̳&�㲻����������̳����Ļ���Ϊ $jifen��������ֻ̳�л��ִ��ڵ��� $enterminjf �Ĳ��ܽ��룡") if ($enterminjf > 0 && $jifen < $enterminjf);
    }
}
	my $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
	&winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @threads = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    my ($postermembername, $topictitle, $postipaddress, $showemoticons, $showsignature ,$postdate, $post, $posticon, $water) = split(/\t/, $threads[$num-1]);
    if(lc($postermembername) ne lc($inmembername)){&error("��������&�������߲����㣬�㲻���ڴ˻�������д");}
    
    &error("��������&�Բ��𣬱���̳���������ظ����� <B>$maxpoststr</B> ���ַ������£�") if (((length($inpost) + length($post)) > $maxpoststr)&&($maxpoststr ne "")&&($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne 'cmo') && ($membercode ne "mo") && ($membercode ne "amo") && ($membercode !~ /^rz/) && ($inmembmod ne "yes"));
    
    my $time1=time;
    $time1 = &longdateandtime($time1);

    $addnewpost ="[br][br]\[color=$fonthighlight\]\[b\]-=-=-=- ���������� \[i\]$postermembername\[\/i\] �� \[i\]$time1\[\/i\] ʱ��� -=-=-=-\[\/b\]\[\/color\]<br>".$inpost;

    if ($post=~m/\[ALIPAYE\]/) {
        my ($no,$alipayid,$warename,$oldpost,$wareprice,$wareurl,$postage_mail,$postage_express,$postage_ems) = split(/\[ALIPAYE\]/,$post);

        $newpost="\[ALIPAYE\]$alipayid\[ALIPAYE\]$warename\[ALIPAYE\]$oldpost$addnewpost\[ALIPAYE\]$wareprice\[ALIPAYE\]$wareurl\[ALIPAYE\]$postage_mail\[ALIPAYE\]$postage_express\[ALIPAYE\]$postage_ems\[ALIPAYE\]";

    } else {
        $newpost ="$post$addnewpost";
    }

    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, ">$filetoopen");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    my $j;
    foreach $postline (@threads) {
    chomp $postline;
    $j++;
    if($num eq $j){
    my ($postermembername, $topictitle, $postipaddress, $showemoticons, $showsignature ,$postdate, $post, $posticon, $water) = split(/\t/, $postline);
    print FILE "$postermembername\t$topictitle\t$postipaddress\t$showemoticons\t$showsignature\t$postdate\t$newpost\t$posticon\t$water\n";}
    else{
    print FILE "$postline\n";
    }
    }
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    &mischeader("��д����");
    $gopage = int(($num-1)/$maxtopics)*$maxtopics;
    if ($refreshurl == 1) { 
    	$relocurl = "topic.cgi?forum=$inforum&topic=$intopic&start=$gopage#$num"; 
    }else { 
    	$relocurl = "forums.cgi?forum=$inforum"; 
    }
    $output .= qq~<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>��д�ɹ�</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
���������<ul><li><a href="topic.cgi?forum=$inforum&topic=$intopic&start=$gopage#$num">��������</a><li><a href="forums.cgi?forum=$inforum">������̳</a><li><a href="leobbs.cgi">������̳��ҳ</a></ul>
</tr></td></table></td></tr></table>
<meta http-equiv="refresh" content="3; url=$relocurl">
	~;
&output("$boardname - ��$forumname����д����",\$output);