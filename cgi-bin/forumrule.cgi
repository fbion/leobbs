#!/usr/bin/perl
#####################################################
#           ��̳�������� Money ά������           #
#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��վλַ�� http://www.LeoBBS.com/            #
#      ��̳λַ�� http://bbs.LeoBBS.com/            #
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
$LBCGI::POST_MAX=500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";

$|++;
$thisprog = "forumrule.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

$action = $query->param('action');
$inforum = $query->param('forum');
&error("��������&�ϴ󣬱��Һ��ҵĳ���ѽ��") if ($inforum !~ /^[0-9 ]+$/);
require "${lbdir}data/style${inforum}.cgi" if (-e "${lbdir}data/style${inforum}.cgi");

#my $inmembername = $query->param('membername');
#my $inpassword = $query->param('password');
$inmembername = $query->param('membername');
$inpassword = $query->param('password');
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$inselectstyle = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
require "${lbdir}data/skin/${inselectstyle}.cgi" if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi"));
$catbackpic = "background=$imagesurl/images/$skin/$catbackpic" if $catbackpic;

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

$inmembername = $query->cookie("amembernamecookie") unless $inmembername;
$inpassword = $query->cookie("apasswordcookie") unless $inpassword;
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($inmembername eq "" || $inmembername eq "����" ) {
    $inmembername = "����";
} else {
    &getmember("$inmembername","no");
    &error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
    if ($inpassword ne $password) {
	    $namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
        $passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("��ͨ����&�������û����Ʋ�����������µ��룡");
    }
}

&error("��ͨ����&û���������̳��") unless -e "${lbdir}forum$inforum";

&moderator($inforum);

if ($action ne "edit") {
    &ShowForm();
}else {
    &Edit();
}

&output("�༭��̳������Ҫ��Ϣ", \$output);
exit;

sub ShowForm {

    &mischeader("�༭��̳������Ҫ��Ϣ");

    open FILE, "${lbdir}boarddata/forumrule$inforum.cgi";
    my $forumrule = <FILE>;
    close FILE;

    $forumrule =~ s/<br>/\n/isg;

    $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="edit">
<input type=hidden name="forum" value="$inforum">
<font color=$fontcolormisc><b>�����������û����ơ�����������ģʽ [�༭��̳������Ҫ��Ϣ]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><b><u>$inmembername</u></b></font> ��Ҫʹ�������û���ݣ��������û����ƺ����롣δע������������������������հס�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û�����</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������̳������Ҫ��Ϣ<br>(����ʹ�� LBCODE ����)<br><br><font color=$fonthighlight>Ϊ�����ۣ������������5���ڡ�</font></td><td bgcolor=$miscbackone><textarea cols=60 name=forumrule rows=10>$forumrule</textarea> �����ձ�ʾ����ʾ��̳������Ҫ��Ϣ��</td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="�� ��"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT><p>
~;

}

sub Edit {
    &mischeader("�༭��̳������Ҫ��Ϣ");

    &error("Ȩ�޲���&�����Ǳ���̳̳������������������������") unless ((($membercode eq "ad")||($membercode eq 'smo')||(",$catemods," =~ /\Q\,$inmembername\,\E/i)||($inmembmod eq "yes"))&&($inpassword eq $password));

    my $forumrule = $query->param('forumrule');
       $forumrule = &cleaninput("$forumrule");
       $forumrule =~ s/\n/<br>/isg;
       $forumrule =~ s/<p>/<br><br>/isg;
       $forumrule =~ s/<br><br><br>/<br>/isg;
       $forumrule =~ s/<br>$//ig;

    if ($forumrule) {
        open FILE, ">${lbdir}boarddata/forumrule$inforum.cgi";
        print FILE $forumrule;
        close FILE;
    }else {
        # ������û����̳������Ҫ��Ϣ����������������ɾ��������һ�ε�����ȡ��
    	unlink "${lbdir}boarddata/forumrule$inforum.cgi";
    }

    require "recooper.pl";
    &addadminlog("�༭��̳������Ҫ��Ϣ");

    $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>��̳������Ҫ��Ϣ�ѱ༭</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
���������<ul><li><a href="forums.cgi?forum=$inforum">������̳</a><li><a href="leobbs.cgi">������̳��ҳ</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">~;

}