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
$LBCGI::POST_MAX=200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
use MAILPROG qw(sendmail);
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "lbfriend.cgi";
$query = new LBCGI;
&ipbanned; #��ɱһЩ ip
$inforum         = $query -> param('forum');
$intopic         = $query -> param('topic');
$action          = $query -> param('action');
$inrealname      = $query -> param('realname');
$intoname        = $query -> param('toname');
$infromemail     = $query -> param('fromemail');
$intoemail       = $query -> param('toemail');
$insubject       = $query -> param('subject');
$inemailmessage  = $query -> param('emailmessage');
$emailtopictitle = $query -> param('emailtopictitle');
$inrealname          = &cleaninput($inrealname);
$insubject           = &cleaninput($insubject);
$inemailmessage      = &cleaninput($inemailmessage);
$emailtopictitle     = &cleaninput($emailtopictitle);
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum) && ($inforum !~ /^[0-9]+$/));
$inmembername = $query->cookie("amembernamecookie");
$inpassword   = $query->cookie("apasswordcookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($inmembername eq "" || $inmembername eq "����" ) {
    $inmembername = "����";
	    if ($regaccess eq "on" && &checksearchbot) {
	    	print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
	    	print "<script language='javascript'>document.location = 'loginout.cgi?forum=$inforum'</script>";
	    	exit;
	    }
}
else {
#    &getmember("$inmembername");
    &getmember("$inmembername","no");
    $mymembercode=$membercode;
    $myrating=$rating;
     if ($inpassword ne $password) {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("��ͨ����&�������û���������������µ�¼��");
     }
    &error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
    }
if ($emailfunctions ne "on") { &error("���ʼ�������&�Բ�����̳����Աû�н��ʼ����ܴ򿪣�"); }
$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) { require "${lbdir}data/skin/${inselectstyle}.cgi"; }
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&title;
$output .= qq~
<br>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> ���������������ʼ����ܷ��ͱ�ҳ�������</td></tr></table>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3 height=25><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=11> <font face="$font" color=$navfontcolor> <a href="leobbs.cgi">$boardname</a> �� �����ʼ�������<td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>
<SCRIPT>valigntop()</SCRIPT>
  <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
    <tr>
      <td>
      <table cellpadding=6 cellspacing=1 width=100%>
~;
    &getoneforum("$inforum");
    if (($allowedentry{$inforum} eq "yes")||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; } else { $allowed = "no"; }
    if (($startnewthreads eq "cert")&&(($membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "amo" && $membercode ne "mo" && $membercode !~ /^rz/)||($inmembername eq "����"))&&($userincert eq "no")) { &error("������̳&��һ���Ա������������̳��"); }

    if (($privateforum eq "yes") && ($allowed ne "yes")) { &error("����˽����̳&�Բ�������Ȩ���������̳��");}
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
    
  if ($action eq "send") {
    $blankfields = "";
    if(!$inrealname)        { $blankfields = "yes"; }
    elsif(!$intoname)       { $blankfields = "yes"; }
    elsif(!$intoemail)      { $blankfields = "yes"; }
    elsif(!$infromemail)    { $blankfields = "yes"; }
    elsif(!$insubject)      { $blankfields = "yes"; }
    elsif(!$inemailmessage) { $blankfields = "yes"; }
    
    if ($blankfields) {
        &error("���ʼ�������&��������������Ȼ���ͣ�");
    }
    
    if ($infromemail !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/) { &error("���ʼ�������&������ʼ���ַ��"); }
    if ($intoemail !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/) { &error("���ʼ�������&������ʼ���ַ��"); }

    my $temp = &dofilter("$insubject\t$inemailmessage\t$emailtopictitle");
    ($insubject,$inemailmessage,$emailtopictitle) = split(/\t/,$temp);

    $to = $intoemail;
    $from = $infromemail;
    $subject = "$insubject";
    $message .= "\n";
    $message .= "$boardname <br>\n";
    $message .= "$boardurl/leobbs.cgi <br>\n";
    $message .= "���� LeoBBS ��̳�����ѵ���Ϣ\n";
    $message .= "---------------------------------------------------------------------\n<br><br>\n";
    $message .= "$inrealname �� $homename �����ʼ�������<br>\n";
    $message .= "---------------------------------------------------------------------\n<br><br>\n";
    $message .= "$inemailmessage\n <br><br>\n";
    $message .= "���⣺ $emailtopictitle\n <br><br>\n<br>\n";
    $message .= "��ַ�� $boardurl/topic.cgi?forum=$inforum&topic=$intopic <br>\n";
    $message .= "---------------------------------------------------------------------\n<br><br>\n";
    $message .= "��ʾ����û�б�Ҫ�ظ�����ʼ�����ֻ����̳������֪ͨ��\n<br><br>\n";
    $message .= "---------------------------------------------------------------------<br>\n";
                
    &sendmail($from, $from, $to, $subject, $message);
    $output .= qq~
        <tr>
         <td bgcolor=$titlecolor $catbackpic valign=middle align=center><font face="$font" color=$fontcolormisc><b>Email ������ɣ�</b></font></td></tr>
         <tr>
         <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
         �����������
         <ul>
         <li><a href="topic.cgi?forum=$inforum&topic=$intopic">��������</a>
         <li><a href="forums.cgi?forum=$inforum">������̳</a>
         <li><a href="leobbs.cgi">������̳��ҳ</a>
         </ul>
         </tr>
         </td>
         </table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
    ~;
}
else {

    $filetoopen = "${lbdir}forum$inforum/$intopic.pl";
    open(FILE, "$filetoopen");
    $allthreads = <FILE>;
    close(FILE);
    
    ($topicid, $topictitle, $no, $no, $no ,$no, $startedby, $startedpostdate, $no) = split(/\t/,$allthreads);

    $topictitle = &cleanarea("$topictitle");
    $topictitle =~ s/^����������//;

	if ($addtopictime eq "yes") {
	    my $topictime = &dispdate($startedpostdate + ($timedifferencevalue*3600) + ($timezone*3600));
	    $topictitle = "[$topictime] $topictitle";
	}

    $output .= qq~
    <form action="$thisprog" method=post>
    <input type=hidden name="action" value="send">
    <input type=hidden name="forum" value="$inforum">
    <input type=hidden name="topic" value="$intopic">
    <tr>
    <td bgcolor=$titlecolor $catbackpic valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc><b>�����ʼ�������</b></font></td></tr>
    <tr>
    <td bgcolor=$miscbackone valign=middle colspan=2><font face="$font" color=$fontcolormisc>
    <b>ͨ���ʼ��������� <a href="topic.cgi?forum=$inforum&topic=$intopic">$topictitle</a> ���������ѡ�</b>������������������������ȷ���ʼ���ַ��<br>��������һЩ�Լ�����Ϣ����������ݿ��ڡ�����������ӵ������ URL ����Բ���д����Ϊ��������ڷ��͵� Email ���Զ���ӵģ�
    </td>
    <tr>
    <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc><b>����������</b></td>
    <td bgcolor=$miscbackone><input type=text size=40 name="realname"></td>
    </tr><tr>
    <td bgcolor=$miscbacktwo><font face="$font" color=$fontcolormisc><b>���� Email ��ַ��</b></td>
    <td bgcolor=$miscbacktwo><input type=text size=40 name="fromemail"></td>
    </tr><tr>
    <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc><b>�����ѵ����֣�</b></td>
    <td bgcolor=$miscbackone><input type=text size=40 name="toname"></td>
    </tr><tr>
    <td bgcolor=$miscbacktwo><font face="$font" color=$fontcolormisc><b>�����ѵ� Email��</b></td>
    <td bgcolor=$miscbacktwo><input type=text size=40 name="toemail"></td>
    </tr><tr>
    <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc><b>Email ���⣺</b></td>
    <td bgcolor=$miscbackone><input type=text size=40 name="subject" value="$topictitle"></td>
    </tr><tr>
    <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc><b>��Ϣ���ݣ�</b></td>
    <td bgcolor=$miscbackone><textarea name="emailmessage" cols="55" rows="6">������� '$homename' �� '$topictitle' ����������ݻ����Ȥ�ģ���ȥ������</textarea></td>
    </tr><tr>
    <td colspan=2 bgcolor=$miscbacktwo align=center><input type=hidden name="emailtopictitle" value="$topictitle"><input type=submit value="�� ��" name="Submit"></table></td></form></tr></table>
<SCRIPT>valignend()</SCRIPT>
    ~;
}
&output($boardname,\$output);
