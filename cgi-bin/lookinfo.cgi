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
require "data/membertitles.cgi";
require "data/cityinfo.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "lookinfo.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

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

$inmember            = $query -> param('member');
$inmembername        = $query -> param("membername");
$inpassword          = $query -> param("password");
$action              = &cleaninput("$action");
$inmember            = &cleaninput("$inmember");
$inmembername        = &cleaninput("$inmembername");
$inpassword          = &cleaninput("$inpassword");
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

    if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
    if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie"); }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($inmembername eq "" || $inmembername eq "����" ) { $inmembername = "����"; }
    else {
        &getmember("$inmembername","no");
    }   

&mischeader("��̳��Ϣ");

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

            my %Mode = (             
            'style'               =>    \&styleform,   
            );

            if($Mode{$action}) { 
               $Mode{$action}->();
               }
##################################################################################
sub styleform {
&mischeader("�鿴��̳��Ϣ");
$mgraphic0 = "none.gif" if ($mgraphic0 eq "");
$output .= qq~<SCRIPT>valigntop()</SCRIPT>
        <table width=$tablewidth border=1 bordercolor=$tablebordercolor align=center cellpadding=5 cellspacing=0 >
        <tr><td bgcolor=$forumcolorone $catbackpic colspan=4 align=center><B>�� �� �� ��</B></td><tr>
        <tr><td bgcolor=$forumcolorone><B>��������</td><td  bgcolor=$forumcolortwo><B>������</td><td bgcolor=$forumcolorone><B>����ͼƬ</td><tr>
	<tr><td bgcolor=$forumcolorone>$mtitle0</td><td  bgcolor=$forumcolortwo>0</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic0></td><tr>
	<tr><td bgcolor=$forumcolorone>$mtitle1</td><td  bgcolor=$forumcolortwo>$mpostmark1</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic1></td><tr>
	<tr><td bgcolor=$forumcolorone>$mtitle2</td><td  bgcolor=$forumcolortwo>$mpostmark2</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic2></td><tr>
	<tr><td bgcolor=$forumcolorone>$mtitle3</td><td  bgcolor=$forumcolortwo>$mpostmark3</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic3></td><tr>
	<tr><td bgcolor=$forumcolorone>$mtitle4</td><td  bgcolor=$forumcolortwo>$mpostmark4</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic4></td><tr>
	<tr><td bgcolor=$forumcolorone>$mtitle5</td><td  bgcolor=$forumcolortwo>$mpostmark5</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic5></td><tr>
	<tr><td bgcolor=$forumcolorone>$mtitle6</td><td  bgcolor=$forumcolortwo>$mpostmark6</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic6></td><tr>
	<tr><td bgcolor=$forumcolorone>$mtitle7</td><td  bgcolor=$forumcolortwo>$mpostmark7</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic7></td><tr>
	<tr><td bgcolor=$forumcolorone>$mtitle8</td><td  bgcolor=$forumcolortwo>$mpostmark8</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic8></td><tr>
	<tr><td bgcolor=$forumcolorone>$mtitle9</td><td  bgcolor=$forumcolortwo>$mpostmark9</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic9></td><tr>
	~;
if ($mtitle10 ne "") {
	$output .= qq~<tr><td bgcolor=$forumcolorone>$mtitle10</td><td  bgcolor=$forumcolortwo>$mpostmark10</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic10></td><tr>
	~;
}
if ($mtitle11 ne "") {
	$output .= qq~<tr><td bgcolor=$forumcolorone>$mtitle11</td><td  bgcolor=$forumcolortwo>$mpostmark11</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic11></td><tr>
	~;
}
if ($mtitle12 ne "") {
	$output .= qq~<tr><td bgcolor=$forumcolorone>$mtitle12</td><td  bgcolor=$forumcolortwo>$mpostmark12</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic12></td><tr>
	~;
}
if ($mtitle13 ne "") {
	$output .= qq~<tr><td bgcolor=$forumcolorone>$mtitle13</td><td  bgcolor=$forumcolortwo>$mpostmark13</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic13></td><tr>
	~;
}
if ($mtitle14 ne "") {
	$output .= qq~<tr><td bgcolor=$forumcolorone>$mtitle14</td><td  bgcolor=$forumcolortwo>$mpostmark14</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic14></td><tr>
	~;
}
if ($mtitle15 ne "") {
	$output .= qq~<tr><td bgcolor=$forumcolorone>$mtitle15</td><td  bgcolor=$forumcolortwo>$mpostmark15</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic15></td><tr>
	~;
}
if ($mtitle16 ne "") {
	$output .= qq~<tr><td bgcolor=$forumcolorone>$mtitle16</td><td  bgcolor=$forumcolortwo>$mpostmark16</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic16></td><tr>
	~;
}
if ($mtitle17 ne "") {
	$output .= qq~<tr><td bgcolor=$forumcolorone>$mtitle17</td><td  bgcolor=$forumcolortwo>$mpostmark17</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic17></td><tr>
	~;
}
if ($mtitle18 ne "") {
	$output .= qq~<tr><td bgcolor=$forumcolorone>$mtitle18</td><td  bgcolor=$forumcolortwo>$mpostmark18</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic18></td><tr>
	~;
}
if ($mtitle19 ne "") {
	$output .= qq~<tr><td bgcolor=$forumcolorone>$mtitle19</td><td  bgcolor=$forumcolortwo>$mpostmark19</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic19></td><tr>
	~;
}
if ($mtitlemax ne "") {
	$output .= qq~<tr><td bgcolor=$forumcolorone>$mtitlemax</td><td  bgcolor=$forumcolortwo>$mpostmarkmax</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphicmax></td><tr>
	~;
}
if ($motitle ne "") {
	$output .= qq~ <tr><td bgcolor=$forumcolorone>$motitle</td><td  bgcolor=$forumcolortwo>��������</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$modgraphic></td><tr>
~;
}
if ($cmotitle ne "") {
	$output .= qq~ <tr><td bgcolor=$forumcolorone>$cmotitle</td><td  bgcolor=$forumcolortwo>��������</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$cmodgraphic></td><tr>
~;
}
if ($smotitle ne "") {
	$output .= qq~ <tr><td bgcolor=$forumcolorone>$smotitle</td><td  bgcolor=$forumcolortwo>��������</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$smodgraphic></td><tr>
~;
}
$output .= qq~
	<tr><td bgcolor=$forumcolorone>$adtitle</td><td  bgcolor=$forumcolortwo>��������</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$admingraphic></td><tr>
</table><SCRIPT>valignend()</SCRIPT><br><br><SCRIPT>valigntop()</SCRIPT>
<table width=$tablewidth border=1 bordercolor=$tablebordercolor align=center cellpadding=5 cellspacing=0 >
        <tr><td bgcolor=$forumcolorone $catbackpic colspan=4 align=center><B>�� �� �� Ϣ</B></td><tr>
        <tr><td bgcolor=$forumcolorone>ÿ�Ƽ�һ�������ӵĻ��ң�</td><td  bgcolor=$forumcolortwo>$addtjhb</td><tr>
        <tr><td bgcolor=$forumcolorone>ÿ�������������ӵĻ��ң�</td><td  bgcolor=$forumcolortwo>$addjhhb</td><tr>
        <tr><td bgcolor=$forumcolorone width="50%">���û�ע�����Ļ��ң�</td><td  bgcolor=$forumcolortwo>$joinmoney</td><tr>
        <tr><td bgcolor=$forumcolorone>�������������ӵĻ��ң�</td><td  bgcolor=$forumcolortwo>$addmoney</td><tr>
        <tr><td bgcolor=$forumcolorone>�����»ظ����ӵĻ��ң�</td><td  bgcolor=$forumcolortwo>$replymoney</td><tr>
        <tr><td bgcolor=$forumcolorone>ÿ�ε�¼ʱ���ӵĻ��ң�</td><td  bgcolor=$forumcolortwo>$loginmoney</td><tr>
        <tr><td bgcolor=$forumcolorone>��ɾ�����Ӽ��ٵĻ��ң�</td><td  bgcolor=$forumcolortwo>$delmoney</td><tr>

        <tr><td bgcolor=$forumcolorone>ÿ�Ƽ�һ�������ӵĻ��֣�</td><td  bgcolor=$forumcolortwo>$addtjjf</td><tr>
        <tr><td bgcolor=$forumcolorone>���û�ע�����Ļ��֣�</td><td  bgcolor=$forumcolortwo>$joinjf</td><tr>
        <tr><td bgcolor=$forumcolorone>ÿ��һ����������Ļ��֣�</td><td  bgcolor=$forumcolortwo>$ttojf</td><tr>
        <tr><td bgcolor=$forumcolorone>ÿ��һ���ظ�����Ļ��֣�</td><td  bgcolor=$forumcolortwo>$rtojf</td><tr>
        <tr><td bgcolor=$forumcolorone>��ɾ��һ�����Ӽ�ȥ�Ļ��֣�</td><td  bgcolor=$forumcolortwo>$deltojf</td><tr>
</table><SCRIPT>valignend()</SCRIPT><BR><BR>
~;
}

$output .= qq~</body></html>~;
&output("$boardname - �鿴��̳��Ϣ",\$output);
exit;
