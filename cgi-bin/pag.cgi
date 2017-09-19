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
$LBCGI::POST_MAX=500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
use VISITFORUM qw(getlastvisit setlastvisit);
use MAILPROG qw(sendmail);
require "code.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;
$thisprog = "pag.cgi";
$query = new LBCGI;

$inforum        = $query -> param('forum');
$intopic        = $query -> param('topic');
$email        = $query -> param('email');

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum) && ($inforum !~ /^[0-9]+$/));
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($inmembername eq "" || $inmembername eq "����" ) {
    $inmembername = "����";
	    if ($regaccess eq "on" && &checksearchbot) {
	    	print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
	    	print "<script language='javascript'>document.location = 'loginout.cgi?forum=$inforum'</script>";
	    	exit;
	    }
    &error("��ͨ����&���˲��ܲ鿴�������ݣ���ע����¼������") if ($guestregistered eq "off");
}
else {
#    &getmember("$inmembername");
    &getmember("$inmembername","no");
    &error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
    if (($allowedentry{$inforum} eq "yes")||($membercode eq "ad")||($membercode eq 'smo')) { $allowed = "yes"; } else { $allowed = "no"; }
#        &getmemberstime("$inmembername");
        &getlastvisit;
        $forumlastvisit = $lastvisitinfo{$inforum};
        $currenttime = time;
        &setlastvisit("$inforum,$currenttime");
    }

if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

    &getoneforum("$inforum");

    $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    @threads = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    ($trash, $topictitle, $trash) = split(/\t/, @threads[0]);
    $topictitle =~ s/^����������//;

	if ($addtopictime eq "yes") {
	    my $topictime = &dispdate($postdate + ($timedifferencevalue*3600) + ($timezone*3600));
	    $topictitle = "[$topictime] $topictitle";
	}

    $postdate = &dateformat($postdate + ($timedifferencevalue*3600) + ($timezone*3600));

if (($startnewthreads eq "cert")&&(($membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo" && $membercode ne "amo" && $membercode !~ /^rz/)||($inmembername eq "����"))&&($userincert eq "no")) { &error("������̳&��һ���Ա������������̳��"); }
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

    if (($privateforum eq "yes") && ($allowed ne "yes")) {
        &error("����˽����̳&�Բ�������Ȩ���������̳��");
    }
    else {
      my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
      $filetoopens = &lockfilename($filetoopens);
      if (!(-e "$filetoopens.lck")) {
        if ($privateforum ne "yes") {
            &whosonline("$inmembername\t$forumname\tboth\t����ʵ�����<a href=\"topic.cgi?forum=$inforum&topic=$intopic\"><b>$topictitle</b></a>\t");
        }
        else {
            &whosonline("$inmembername\t$forumname(��)\tboth\t����ʵ����ӱ�������\t");
        }
      }
    }
if ($emailfunctions eq "off") { &error("����ʵ�&�ǳ���Ǹ����̳�ķ����ʼ������Ѿ��رգ�");  }

    if ($email){
        if ($email !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/) { &error("����ʵ�&������ʼ���ַ��"); }
        $email =~ s/[\a\f\n\e\0\r\t\`\~\!\$\%\^\&\*\(\)\=\+\\\{\}\;\'\:\"\,\/\<\>\?\|]//isg;
        $output .= qq~
        <html><head><title>$boardname</title>
	<style>
		A:visited {	TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	TEXT-DECORATION: underline overline	}
		A:link 	  {	text-decoration: none;}

	        A:visited {	text-decoration: none;}
	        A:active  {	TEXT-DECORATION: none;}
	        A:hover   {	TEXT-DECORATION: underline overline}

		.t     {	LINE-HEIGHT: 1.4					}
		BODY   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		SELECT {	FONT-FAMILY: ����; FONT-SIZE: 9pt;	}
		INPUT  {	FONT-FAMILY: ����; FONT-SIZE: 9pt; height:22px;	}
		TEXTAREA{	FONT-FAMILY: ����; FONT-SIZE: 9pt;	}
		DIV    {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		FORM   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		OPTION {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		P	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		BR	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
	</style>
    </head>
    <body topmargin=10 leftmargin=0>
    <table cellpadding=0 cellspacing=0 width=90% align=center>
        <tr>
            <td>
            <p><b>��$boardname���������</b><p>
            <b>�� ̳ ��- $boardname</b> ($boardurl/leobbs.cgi)<br>
            <b>��������-- $forumname</b> ($boardurl/forums.cgi?forum=$inforum)<br>
            <b>���ӱ���--- $topictitle</b> ($boardurl/topic.cgi?forum=$inforum&topic=$intopic)
        </tr>
    </table>
    <p><p><p>
    <table cellpadding=0 cellspacing=0 width=90% align=center>
        <tr>
            <td>

    ~;
    foreach $line (@threads) {
        ($postermembername, $topictitle, $postipaddress, $showemoticons, $showsignature, $postdate, $post) = split(/\t/,$line);
        $post = "<font color=red>�������Ӳ��ܴ��<\/font>" if ($post =~ /\[POSTISDELETE=(.+?)\]/isg);
        $post =~ s/\[hide\](.*)\[\/hide\]/<font color=red>�������ݲ��ܴ��<\/font>/isg; 
		$post="<font color=red>�������Ӳ��ܴ��<\/font>" if ($post=~/LBHIDDEN\[(.*?)\]LBHIDDEN/isg || $post=~/LBSALE\[(.*?)\]LBSALE/isg);
		$post =~ s/\[post=(.+?)\](.+?)\[\/post\]/<font color=red>�������Ӳ��ܴ��<\/font>/isg;
		$post =~ s/\[jf=(.+?)\](.+?)\[\/jf\]/<font color=red>�������Ӳ��ܴ��<\/font>/isg;
	$post =~ s/\[watermark\](.+?)\[\/watermark\]/<font color=red>��ˮӡ���ݲ��ܴ��<\/font>/isg;
	$post =~ s/\[curl=\s*(http|https|ftp):\/\/(.*?)\s*\]/\[��������\]/isg if ($usecurl ne "no");
        $post  =~ s/\[ALIPAYE\](.*)\[ALIPAYE\]//isg; 

	&lbcode(\$post);

        $post =~ s/&lt\;/\</g;
        $post =~ s/&gt\;/\>/g;
        $post =~ s/&quot\;/\"/g;
        $postdate = &dateformat($postdate + ($timedifferencevalue*3600) + ($timezone*3600));

        $output .= qq~ 
        <hr><br>
        -- �����ˣ� $postermembername<BR>
        -- ����ʱ�䣺 $postdate<br>
        $post      
        ~;
    }
    $output .= qq~
        </td></tr></table><center><hr><b>$boardname<br>&copy; 2000 LeoBBS.com</b></center>
        </body></html>
    ~;
    $subject = "��$boardname����ʵݹ���������";
    &sendmail($adminemail_out, $adminemail_in, $email, $subject, $output);
    print "<center><br><b>�ʵ��������!</b><br><br><a href=javascript:top.window.close()>�رմ���</a><script>top.window.close()</script></center>";
    exit;
}else {
    $output .= qq~
    <br><p>
<SCRIPT>valigntop()</SCRIPT>
    <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
    <tr><td>
    <table cellpadding=6 cellspacing=1 width=100%>
    <form action="$thisprog" method=post>
    <tr>
    <td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
    <input type=hidden name="forum" value="$inforum">
    <input type=hidden name="topic" value="$intopic">
    <font color=$fontcolormisc><b>����ʵ�</b></font></td></tr>
    <tr>
    <td bgcolor=$miscbackone colspan=2><font color=$fontcolormisc>
    <b>�ѱ��� <a href=topic.cgi?forum=$inforum&topic=$intopic>$topictitle</a> ����ʵݡ�</b><br>����ȷ������Ҫ�ʵݵ��ʼ���ַ��
    </td></tr><tr>
    <td bgcolor=$miscbacktwo><font color=$fontcolormisc><b>�ʵݵ� Email ��ַ��</b></td>
    <td bgcolor=$miscbacktwo><input type=text size=40 name="email"></td>
    </tr><tr>
    <td colspan=2 bgcolor=$miscbacktwo align=center><input type=submit value="�� ��" name="Submit"></table></td></form></tr></table><SCRIPT>valignend()</SCRIPT>
    ~;
    &output("$boardname - ���Ӵ��",\$output,"msg");
}
