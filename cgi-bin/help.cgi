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
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "help.cgi";
$query = new LBCGI;

$inadmin                = $query -> param('admin');
$innew                = $query -> param('helpnew');
$action                 = $query -> param('action');
$inhelpon               = $query -> param('helpon');
$inadminmodpass         = $query -> param("adminmodpass");
$inadminmodname         = $query -> param("adminmodname");
$inadminmodpass         = &cleaninput($inadminmodpass);
$inadminmodname         = &cleaninput($inadminmodname);
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inadminmodname =~ m/\//)||($inadminmodname =~ m/\\/)||($inadminmodname =~ m/\.\./));
$inadminmodname =~ s/\///g;
$inadminmodname =~ s/\.\.//g;
$inadminmodname =~ s/\\//g;
if ($inadminmodpass ne "") {
    eval {$inadminmodpass = md5_hex($inadminmodpass);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inadminmodpass = md5_hex($inadminmodpass);');}
    unless ($@) {$inadminmodpass = "lEO$inadminmodpass";}
}

$inselectstyle  = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

$inhelpon = &cleaninput($inhelpon);
$inhelpon =~ s/\///g;
$inhelpon =~ s/\.cgi//ig;
$inhelpon =~ s/\.\.//g;
$inhelpon =~ s/\\//g;
$inadmin =~ s/\///g;
$inadmin =~ s/\.\.//g;
$inadmin =~ s/\\//g;
$innew =~ s/\///g;
$innew =~ s/\.\.//g;
$innew =~ s/\\//g;
$cleanhelpname = $inhelpon;
$cleanhelpname =~ s/\_/ /g;
$cleanadminname = $inadmin;
$cleanadminname =~ s/\_/ /g;
$cleannewname = $innew;
$cleannewname =~ s/\_/ /g;
if (($number) && ($number !~ /^[0-9]+$/)) { &error("��ͨ����&�벻Ҫ�޸����ɵ� URL��"); }
if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
if (! $inadminmodname) { $inadminmodname = $inmembername; }
if (! $inadminmodpass) { $inadminmodpass = $inpassword; }

if ($inmembername eq "" || $inmembername eq "����" ) {
    $inmembername = "����";
}
else {
	&getmember("$inmembername","no");
     if ($inpassword ne $password) {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("��ͨ����&�������û���������������µ�¼��");
     }
	&error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
}
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
    if ($inhelpon) {
        $output .= qq~<p>
<SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
              <tr>
                <td>
                  <table cellpadding=3 cellspacing=1 width=100%>
                    <tr>
                      <td bgcolor=$miscbacktwo align=center $catbackpic height=26><font face="$font" color=$fontcolormisc><b>$boardname�İ����ļ�</b></td>
                    </tr>
                    <tr>
                      <td bgcolor=$miscbackone valign=middle align=cleft><font face="$font" color=$fontcolormisc>
                       <br><center>$inmembername��ϣ������İ�����������</center><br><br>
                       <font face="$font" color=$fontcolormisc>
                       <b>����$cleanhelpname�İ�����</b><p>
	~;
        $filetoopen = "$lbdir" . "help/$inhelpon.dat";
        $filetoopen =~ s/[<>\^\(\)\{\}\a\f\n\e\0\r\"\`\&\;\*\?]//g;
        open (FILE, "$filetoopen");
        sysread(FILE, $helpdata,(stat(FILE))[7]);
        close (FILE);
	$helpdata =~ s/\r//isg;

            $output .= $helpdata;
    }
    elsif ($innew) {
        $output .= qq~<p>
<SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
              <tr>
                <td>
                  <table cellpadding=3 cellspacing=1 width=100%>
                    <tr>
                      <td bgcolor=$miscbacktwo align=center $catbackpic height=26><font face="$font" color=$fontcolormisc><b>$boardname�İ����ļ�</b></td>
                    </tr>
                    <tr>
                      <td bgcolor=$miscbackone valign=middle align=cleft><font face="$font" color=$fontcolormisc>
                       <br>
                       <font face="$font" color=$fontcolormisc>
                       <b>����$cleannewname�İ�����</b><p>
	~;
        $filetoopen = "$lbdir" . "help/$cleannewname.pl";
        $filetoopen =~ s/[<>\^\(\)\{\}\a\f\n\e\0\r\"\`\&\;\*\?]//g;
        open (FILE, "$filetoopen");
        sysread(FILE, $helpdata,(stat(FILE))[7]);
        close (FILE);
	$helpdata =~ s/\r//isg;

            $output .= $helpdata;
    }
    elsif ($action eq "login") {

            &getmember("$inadminmodname","no");

            unless ($membercode eq "ad" ||($membercode eq 'smo')|| $membercode eq "cmo" || $membercode eq "amo" || $membercode eq "mo") { &messangererror("�鿴����&��û��Ȩ�޲鿴���ļ���"); }
            if ($inadminmodpass ne $password) { &messangererror("�鿴����&�����������"); }

            $output .= qq~<p>
<SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
               <tr>
                <td>
                  <table cellpadding=3 cellspacing=1 width=100%>
                    <tr>
                      <td bgcolor=$miscbacktwo align=center $catbackpic height=26><font face="$font" color=$fontcolormisc><b>$boardname�İ����ļ�</b></td>
                    </tr>
                    <tr>
                      <td bgcolor=$miscbackone valign=middle align=cleft><font face="$font" color=$fontcolormisc>
                      <br><center>$inadminmodname��ϣ������İ�����������</center><br><br>
                      <font face="$font" color=$fontcolormisc>
                      <b>����̳��/���������ļ�</b><p>
             ~;
            $dirtoopen = "$lbdir" . "help";
            opendir (DIR, "$dirtoopen");
            @dirdata = readdir(DIR);
            closedir (DIR);
            @sorteddirdata = grep(/cgi$/,@dirdata);
            @newdirdata = sort alphabetically(@sorteddirdata);

            foreach (@newdirdata) {
                chomp $_;
                $filename = $_;
                $filename =~ s/\.cgi$//g;
                $cleanname = $filename;
                $cleanname =~ s/\_/ /g;
                $cleannamefile = uri_escape($cleanname);
                $output .= qq~&nbsp;&nbsp;&nbsp;&nbsp;����<a href="$thisprog?admin=$cleannamefile" target="_self"><b>$cleanname</b></a>�İ���<p>~;
            }
	}
        elsif ($inadmin) {
	    &getmember("$inmembername","no");
            unless ($membercode eq "ad" || $membercode eq 'smo'|| $membercode eq 'cmo'|| $membercode eq 'amo'|| $membercode eq "mo") { &messangererror("�鿴����&��û��Ȩ�޲鿴���ļ���"); }
            if ($inpassword ne $password) { &messangererror("�鿴����&�����������"); }
	    $output .= qq~<p>
<SCRIPT>valigntop()</SCRIPT>
		<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
                 <tr>
                  <td>
                  <table cellpadding=3 cellspacing=1 width=100%>
                    <tr>
                      <td bgcolor=$miscbacktwo align=center $catbackpic height=26><font face="$font" color=$fontcolormisc><b>$boardname�İ����ļ�</b></td>
                    </tr>
                    <tr>
                      <td bgcolor=$miscbackone valign=middle align=cleft><font face="$font" color=$fontcolormisc>
                      <br><center>$inmembername��ϣ������İ�����������</center><br><br>
                      <font face="$font" color=$fontcolormisc>
                      <b>����$cleanadminname�İ���</b><p>
            ~;

	    $filetoopen = "$lbdir" . "help/$inadmin.cgi";
            $filetoopen =~ s/[<>\^\(\)\{\}\a\f\n\e\0\r\"\`\&\;\*\?]//g;
            open (FILE, "$filetoopen");
            @helpdata = <FILE>;
            close (FILE);

	    foreach (@helpdata) {
                $output .= $_;
            }
        }
        else {
	    $output .= qq~<p>
<SCRIPT>valigntop()</SCRIPT>
              <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
                <tr>
                <td>
                    <table cellpadding=3 cellspacing=1 width=100%>
                        <tr>
                            <td bgcolor=$miscbacktwo align=center colspan=2 $catbackpic height=26><font face="$font" color=$fontcolormisc><b>$boardname�İ����ļ�</b></td>
                        </tr>
                        <tr>
                            <td bgcolor=$miscbackone align=center><br><center><font face="$font" color=$fontcolormisc>
                            <b>&nbsp;&nbsp;&nbsp;&nbsp;��������ļ�</b></td>
                        </tr>
                        <tr>
                            <td bgcolor=$miscbackone valign=top align=left><font face="$font" color=$fontcolormisc>
                            
                            
            ~;

            $dirtoopen = "$lbdir" . "help";
            opendir (DIR, "$dirtoopen");
            @dirdata = readdir(DIR);
            closedir (DIR);
            @sorteddirdata = grep(/dat$/,@dirdata);
            @newdirdata = sort alphabetically(@sorteddirdata);

            foreach (@newdirdata) {
                chomp $_;
                $filename = $_;
                $filename =~ s/\.dat$//g;
                $cleanname = $filename;
                $cleanname =~ s/\_/ /g;
                $cleannamefile = uri_escape($cleanname);
                $output .= qq~&nbsp;&nbsp;&nbsp;&nbsp;����<a href="$thisprog?helpon=$cleannamefile" target="_self"><b>$cleanname</b></a>�İ���<p>~;
            }
	    $output .= qq~</td>~;
	}

$output .= qq~</tr><tr><td bgcolor=$miscbackone valign=middle align=center colspan=2><font face="$font" color=$fontcolormisc>~;
    if ($passwordverification eq "yes") { $passwordverification = "�Ǳ����"; }
    else { $passwordverification = "���Ǳ����"; }

    if ($emailfunctions ne "on") { $emailfunctions = "�ر�"; }

    if ($emoticons eq "on") {
	$emoticons = "ʹ��";
        $emoticonslink = qq~| �鿴<a href=javascript:openScript('misc.cgi?action=showsmilies',300,350)>����ת��</a>~;
    }
    else { $emoticons = "û��ʹ��"; }
    $output .= qq~<p><br><br>�鿴<a href=\"$thisprog\" target=\"_self\">���еİ����ļ�</a> $emoticonslink | �鿴 <a href=\"javascript:openScript('misc.cgi?action=lbcode',300,350)\">LeoBBS ��ǩ</a> | �鿴 <a href=\"javascript:openScript('lookemotes.cgi?action=style',300,350)\">EMOTE ��ǩ</a><BR><BR>~;

    $output .= qq~
    </td></tr>
    <tr>
    <td bgcolor=$miscbacktwo align=center colspan=2><font face="$font" color=$fontcolormisc><b>��̳������Ϣ</b><br><br>
    �����Զ�ת����<b>$emoticons</b><br>�ʼ���ַȷ�ϣ�<b>$passwordverification</b><br>��̳�ʼ����ܣ�<b>$emailfunctions</b><br><br>
    </td>
    </tr>
    <tr>
    <td bgcolor=$miscbackone align=center colspan=2><font face="$font" color=$fontcolormisc><b>��¼����̳��/�����İ���</b><br>

    <form action="$thisprog" method="post">
    <input type=hidden name="action" value="login">
    <font face="$font" color=$fontcolormisc>
    ��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�<BR>
    �û�����&nbsp; <input type=text name="adminmodname"> &nbsp;
    �ܡ��룺&nbsp; <input type=password name="adminmodpass"> &nbsp; <input type=submit value="�� ¼"></td></tr></form>
    </table></td></tr></table><SCRIPT>valignend()</SCRIPT>
    ~;

    &output("$boardname - ����",\$output,"msg");

sub messangererror {
    my $errorinfo = shift;
    (my $where,my $errormsg) = split(/\&/, $errorinfo);
    $output = qq~<p><SCRIPT>valigntop()</SCRIPT>
      <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
	<tr>
        <td>
        <table cellpadding=6 cellspacing=1 width=100%>
        <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center $catbackpic height=26><font face="$font" color=$fontcolormisc><b>����$where</b></font></td></tr>
            <tr>
                <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
                <b>����$where�������ϸԭ��</b>
                <ul>
                <li><b>$errormsg</b>
                </ul>
                <b>����$where����Ŀ���ԭ�򣺣�</b>
                <ul>
                <li>�������<li>�û�������
                </ul>
                </tr>
                </td></tr>
                <tr>
                <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc> <a href="javascript:history.go(-1)"> << ������һҳ</a>
                </td></tr>
                </table></td></tr></table><SCRIPT>valignend()</SCRIPT>
    ~;
    &output("$boardname - ����",\$output,"msg");
}
