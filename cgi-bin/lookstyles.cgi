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
$LBCGI::POST_MAX=20000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$thisprog = "lookstyles.cgi";

    $query = new LBCGI;

	@params = $query->param;
	foreach $param(@params) {
		$theparam = $query->param($param);
        $theparam = &cleaninput("$theparam");
		$PARAM{$param} = $theparam;
	    }



$action      =  $PARAM{'action'};
$inforum     =  $PARAM{'forum'};
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum) && ($inforum !~ /^[0-9]+$/));
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

$inmembername        = $query -> param("membername");
$inpassword          = $query -> param("password");
$action              = &cleaninput("$action");
$inmembername        = &cleaninput("$inmembername");
$inpassword          = &cleaninput("$inpassword");
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie"); }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

    if ($inmembername eq "" || $inmembername eq "����" ) { $inmembername = "����"; }
    else {
#    &getmember("$inmembername");
    &getmember("$inmembername","no");
    &error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
        }   
&getoneforum("$inforum");

&mischeader("������ɫ�б�");

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum) && ($inforum !~ /^[0-9]+$/));

&error("������ɫ&�Բ��𣬱���鲻����鿴��ɫ��") if ($look eq "off");

if ($privateforum ne "yes") {
    	&whosonline("$inmembername\t$forumname\tboth\t�鿴��̳$forumname����ɫ\t");
    }
    else {
	&whosonline("$inmembername\t$forumname(��)\tboth\t�鿴������̳$forumname����ɫ\t");
    }

$output .= qq~
<BR><SCRIPT>valigntop()</SCRIPT>
        <table cellpadding="5" style="border-collapse: collapse" width=$tablewidth cellspacing="0" bordercolor=$tablebordercolor border=1 align=center>               
              
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>��̳BODY��ǩ</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333>����������̳���ı�����ɫ���߱���ͼƬ��</font></td>
                <td bgcolor=#FFFFFF>
                $lbbody</td>
                </tr>
                              
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>��̳ҳ�ײ˵�</b>
                </font></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>ҳ�ױ�����ɫ (�˵����Ϸ�)</font></td>
                <td bgcolor=$titleback  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $titleback</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>ҳ��������ɫ (�˵����Ϸ�)</font></td>
                <td bgcolor=$titlefont  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $titlefont</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>ҳ�ױ߽���ɫ (�˵����Ϸ�)</font></td>
                <td bgcolor=$titleborder  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $titleborder</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�˵���������ɫ</font></td>
                <td bgcolor=$menufontcolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $menufontcolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�˵���������ɫ</font></td>
                <td bgcolor=$menubackground  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $menubackground</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>������ۺ���ɫ</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>"�������"������ɫ</font></td>
                <td bgcolor=$lastpostfontcolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $lastpostfontcolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>"������"������ɫ</font></td>
                <td bgcolor=$fonthighlight  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $fonthighlight</td>
                </tr>
                
                                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>һ���û�����������ɫ</font></td>
                <td bgcolor=$posternamecolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $posternamecolor</td>
                </tr>

		<tr>
		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>һ���û������ϵĹ�����ɫ</font></td>
		<td bgcolor=$memglow  width=12>��</td>
		<td bgcolor=#FFFFFF>
		$memglow</td>
		</tr>
               
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>̳������������ɫ</font></td>
                <td bgcolor=$adminnamecolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $adminnamecolor</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>̳�������ϵĹ�����ɫ</font></td>
		<td bgcolor=$adminglow  width=12>��</td>
		<td bgcolor=#FFFFFF>
		$adminglow</td>
		</tr>
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�ܰ�������������ɫ</font></td>
                <td bgcolor=$smonamecolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $smonamecolor</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>�ܰ��������ϵĹ�����ɫ</font></td>
		<td bgcolor=$smoglow  width=12>��</td>
		<td bgcolor=#FFFFFF>
		$smoglow</td>
		</tr>                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>��������������������ɫ</font></td>
                <td bgcolor=$cmonamecolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $cmonamecolor</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>���������������ϵĹ�����ɫ</font></td>
		<td bgcolor=$cmoglow  width=12>��</td>
		<td bgcolor=#FFFFFF>
		$cmoglow</td>
		</tr>                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>��������������ɫ</font></td>
                <td bgcolor=$teamnamecolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $teamnamecolor</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>���������ϵĹ�����ɫ</font></td>
		<td bgcolor=$teamglow  width=12>��</td>
		<td bgcolor=#FFFFFF>
		$teamglow</td>
		</tr>
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>����������������ɫ</font></td>
                <td bgcolor=$teamnamecolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $amonamecolor</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>�����������ϵĹ�����ɫ</font></td>
		<td bgcolor=$teamglow  width=12>��</td>
		<td bgcolor=#FFFFFF>
		$amoglow</td>
		</tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>���˺ͽ����û������ϵĹ�����ɫ</font></td>
		<td bgcolor=$banglow  width=12>��</td>
		<td bgcolor=#FFFFFF>
		$banglow</td>
		</tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>����ҳ����ɫ</center></b><br>
                <font color=#333333>��Щ��ɫ���ý�����ÿ��ҳ�档����ע�ᡢ��¼�������Լ�����ҳ�档
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>��������ɫ</font></td>
                <td bgcolor=$fontcolormisc  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $fontcolormisc</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>����������ɫһ</font></td>
                <td bgcolor=$miscbackone  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $miscbackone</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>����������ɫ��</font></td>
                <td bgcolor=$miscbacktwo  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $miscbacktwo</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>�����ɫ</center></b><br>
                <font color=#333333>��Щ��ɫ�󲿷�����leobbs.cgi��forums.cgi��topic.cgi
                </td></tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�����������ɫ</font></td>
                <td bgcolor=$catback  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $catback</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�����������ɫ</font></td>
                <td bgcolor=$catfontcolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $catfontcolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>���б��߽���ɫ</font></td>
                <td bgcolor=$tablebordercolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $tablebordercolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>���б����</font></td>
                <td bgcolor=#FFFFFF>
                $tablewidth</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>������ɫ</center></b><br>
                <font color=#333333>������ɫ�������ڷ����һ������ı���
                </td></tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>��̳/����ı�����������ɫ</font></td>
                <td bgcolor=$titlecolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $titlecolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>��̳/����ı�����������ɫ</font></td>
                <td bgcolor=$titlefontcolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $titlefontcolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>��̳������ɫ</center></b><br>
                <font color=#333333>�鿴��̳����ʱ��ɫ (forums.cgi)
                </td></tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>������ɫһ</font></td>
                <td bgcolor=$forumcolorone  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $forumcolorone</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>������ɫ��</font></td>
                <td bgcolor=$forumcolortwo  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $forumcolortwo</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>����������ɫ</font></td>
                <td bgcolor=$forumfontcolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $forumfontcolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>�ظ���ɫ</center></b><br>
                <font color=#333333>�ظ�������ɫ(topic.cgi)
                </td></tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�ظ���ɫһ</font></td>
                <td bgcolor=$postcolorone  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $postcolorone</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�ظ���ɫ��</font></td>
                <td bgcolor=$postcolortwo  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $postcolortwo</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�ظ�������ɫһ</font></td>
                <td bgcolor=$postfontcolorone  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $postfontcolorone</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�ظ�������ɫ��</font></td>
                <td bgcolor=$postfontcolortwo  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $postfontcolortwo</td>
                </tr>
               
              
                ~;             


$output .= qq~</td></tr></table><SCRIPT>valignend()</SCRIPT><br><br></body></html>~;
&output("�鿴$forumname����ɫ",\$output);
exit;

