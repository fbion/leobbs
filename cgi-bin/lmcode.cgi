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
require "data/styles.cgi";
require "data/boardinfo.cgi";
require "bbs.lib.pl";
$|++;

$query = new LBCGI;

$inselectstyle  = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

$thisprog = "lmcode.cgi";
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
$output = qq~<p>
<SCRIPT>valigntop()</SCRIPT>
  <table cellpadding="5" style="border-collapse: collapse" width=$tablewidth cellspacing="0" bordercolor=$tablebordercolor border=1 align=center>
    <tr>
      <td width="100%" colspan="3" bgcolor=$titlecolor $catbackpic>
      <p align="center"><font color="#333333"><b>��ӭ���� <u>$boardname</u> ���˴���</b></font></td>
    </tr>
    <tr>
      <td width="28%" bgcolor=$forumcolorone><b>��̳���ƣ�</b></td>
      <td width="72%" colspan="2" bgcolor=$forumcolortwo>$boardname</td>
    </tr>
    <tr>
      <td width="28%" bgcolor=$forumcolorone><b>��̳��ַ��</b></td>
      <td width="72%" colspan="2" bgcolor=$forumcolortwo>
      <a href="$boardurl/leobbs.cgi" target=_blank>
      $boardurl/leobbs.cgi</a></td>
    </tr>
    <tr>
      <td width="28%" bgcolor=$forumcolorone><b>��̳ͼ�꣺</b></td>
      <td width="72%" colspan="2" bgcolor=$forumcolortwo>
~;
if ($boardlogos ne "http://" && $boardlogos ne "") {$output .=qq~<a href="$boardlogos" target=_blank>$boardlogos</a>~;}
else {$output .=qq~û��~;}
      $output.= qq~
      </td>
    </tr>
    <tr>
      <td width="28%" bgcolor=$forumcolorone><b>��̳˵����</b></td>
      <td width="72%" colspan="2" bgcolor=$forumcolortwo>$boarddescription</td>
    </tr>
    <tr>
      <td width="28%" bgcolor=$forumcolorone><b>������ʾ��</b></td>
      <td width="100" bgcolor=$forumcolortwo>
      <p align="center">
~;
if ($boardlogos ne "http://" && $boardlogos ne "") {$output .=qq~<a href="$boardurl/leobbs.cgi" target=_blank><img src="$boardlogos" align="left" width="88" height="31" border="0"></a>~;}
else {$output .=qq~��ȱͼ��~;}
      $output.= qq~
      </td>
      <td width="*" bgcolor=$forumcolortwo>
      <a target="_blank" href="$boardurl/leobbs.cgi">
      <b>$boardname</b></a><br>
      $boarddescription</td>
    </tr>
    <tr>
      <td width="100%" colspan="3" bgcolor=$catback $catbackpic>
      <p align="center">
<input type=submit name="winclose" value="�� ��" onclick=window.close();></td>
    </tr>
  </table><SCRIPT>valignend()</SCRIPT>
~;
    &output("$boardname - �鿴������̳����",\$output,"msg");
exit;