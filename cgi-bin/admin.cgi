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

&testsystem;
use LBCGI;
$LBCGI::POST_MAX=200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "cleanolddata.pl";
eval { require "data/boardstats.cgi"; };
if ($@) { require "repireboardinfo.pl"; require "data/boardstats.cgi"; }
require "bbs.lib.pl";


eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;');
    unless (WebGzip::getStatus()) {
	$gzipfunc = qq~Gzip ģ���Ƿ����? == [ͨ��]~;
    }
    else {
    	$e = WebGzip::getStatus();
    	$gzipfunc = qq~<font color=#FF0000>Gzip ģ���Ƿ����? == [ʧ��]</font> $e~ 
    }

eval ('use GD;');
if ($@) {
    $gdfunc = qq~<font color=#FF0000>GD ģ���Ƿ����? == [ʧ��]</font>~;
}
else {
    $gdfunc = qq~GD ģ���Ƿ����? == [ͨ��]~;
}

$thisprog = "admin.cgi";
$query = new LBCGI;
#&ipbanned; #��ɱһЩ ip
$action       = $query -> param('action');
$loginprog    = $query -> param('loginprog');
$inmembername = $query -> param('membername');
$inpassword   = $query -> param('password');
$inpasswordtemp = $inpassword;
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$inmembername = &unHTML("$inmembername");
$inpassword   = &unHTML("$inpassword");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

unlink ("${lbdir}ilite.cgi");
unlink ("${lbdir}cat.cgi");
unlink ("${lbdir}record.cgi");

mkdir ("${lbdir}$memdir/old", 0777) if (!(-e "${lbdir}$memdir/old"));
mkdir ("${lbdir}cache", 0777) if (!(-e "${lbdir}cache"));
mkdir ("${lbdir}cache/online", 0777) if (!(-e "${lbdir}cache/online"));
mkdir ("${lbdir}cache/myinfo", 0777) if (!(-e "${lbdir}cache/myinfo"));
mkdir ("${lbdir}cache/mymsg", 0777) if (!(-e "${lbdir}cache/mymsg"));
mkdir ("${lbdir}cache/meminfo", 0777) if (!(-e "${lbdir}cache/meminfo"));
mkdir ("${lbdir}cache/id", 0777) if (!(-e "${lbdir}cache/id"));
mkdir ("${lbdir}FileCount", 0777) if (!(-e "${lbdir}FileCount"));
mkdir ("${lbdir}verifynum", 0777) if (!(-e "${lbdir}verifynum"));
mkdir ("${lbdir}verifynum/login", 0777) if (!(-e "${lbdir}verifynum/login"));
mkdir ("${lbdir}$saledir", 0777) if (!(-e "${lbdir}$saledir"));
chmod(0777,"${lbdir}verifynum");
chmod(0777,"${lbdir}verifynum/login");
chmod(0777,"${lbdir}$memdir/old");

if ((-e "${lbdir}install.cgi")&&(!(-e "${lbdir}data/install.lock"))) {
    print "Content-type: text/html\n\n";
    print qq(
    <HTML><HEAD><TITLE>��װ����</TITLE></HEAD>
    <BODY BGCOLOR=#ffffff TEXT=#000000>
    <H1>LeoBBS ����</H1><FONT COLOR=#ff0000><B>��ȫ����</B>��
    <br>install.cgi �ļ���Ȼ�����ķ������ϣ����������� FTP ������ɾ������<br> ����ɾ��֮��ˢ�±�ҳ�����½���������ġ�</FONT></body></html>);
    exit;
}

if ($action eq "logout") {
    &cleanolddata1;
    print "Set-Cookie: adminname=\"\"\n";
    print "Set-Cookie: adminpass=\"\"\n";

    print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

    &admintitle;
    print qq(
    <tr><td bgcolor=#2159C9><font color=#FFFFFF>
    <b>��ӭ������̳��������</b>
    </td></tr>
    <tr><td bgcolor=#EEEEEE valign=middle align=center>
    <font color=#333333><b>���Ѿ���ȫ�˳���������</b></font>
    </td></tr>
    <tr><td bgcolor=#FFFFFF></td></tr>
    </td></tr></table></td></tr></table>
    );
}
else {
    if  ($action eq "login") {
	unlink("${lbdir}install.cgi") if (!(-e "${lbdir}data/install.lock"));
	&cleanolddata2;
	&checkverify;
	$tempmembername = uri_escape($inmembername);
	print "Set-Cookie: adminname=$tempmembername\n";
	print "Set-Cookie: adminpass=$inpassword\n";
    } else {
	&cleanolddata3;
	$inmembername = $query->cookie('adminname');
	$inpassword   = $query->cookie('adminpass');
    }
    $inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
    $inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
    &getadmincheck;

    print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

    &getmember("$inmembername","no");
    &admintitle;
    
    $trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
    $trueipaddress = "no" if ($trueipaddress eq "" || $trueipaddress =~ m/a-z/i || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);
    my $trueipaddress1 = $ENV{'HTTP_CLIENT_IP'};
    $trueipaddress = $trueipaddress1 if ($trueipaddress1 ne "" && $trueipaddress1 !~ m/a-z/i && $trueipaddress1 !~ m/^192\.168\./ && $trueipaddress1 !~ m/^10\./);
    
    if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
	if ($action eq "login") {
	    my $thistime=time;
	    $filetomake = "$lbdir" . "data/adminlogin.cgi";
            open(FILE, ">>$filetomake");
            print FILE "$inmembername\t���벻��ʾ\t$ENV{'REMOTE_ADDR'}\t$trueipaddress\t��¼�ɹ�\t$thistime\t\n";
            close(FILE);
	}

	if ($loginprog ne "") { print "<script language='javascript'>document.location = '$loginprog'</script>"; }

        $warning = qq~<br><font color=#000000>������⣺<b>ͨ��</b></font>~;

        $current_time = localtime;
        $inmembername =~ s/\_/ /g;
        $start_topic_ratio = $totalthreads / $totalmembers if ($totalthreads && $totalmembers);
        $start_topic_ratio = substr($start_topic_ratio, 0, 5) if ($totalthreads && $totalmembers);
        $posting_ratio     = $totalposts / $totalmembers if ($totalposts && $totalmembers);
        $posting_ratio     = substr($posting_ratio, 0, 5) if ($totalposts && $totalmembers);
	$start_topic_ratio = 0 if ($start_topic_ratio eq "");
	$posting_ratio     = 0 if ($posting_ratio eq "");
		
        $testcookie = $ENV{HTTP_COOKIE};
        if ($testcookie) {
            $cookie_result = qq(Cookies �Ƿ����? == [ͨ��]);
        } else {
            $cookie_result = qq(<font color=#FF0000>Cookies �Ƿ����? == [ʧ��]</font>);
        }

	$cgipath = &mypath();

	    eval {$aa = md5_hex("112");};
	    if ($@) {eval('use Digest::MD5 qw(md5_hex);$aa = md5_hex("112");');}
	    unless ($@) {$md5mode = qq(MD5 ģ���Ƿ����? == [ͨ��]);} else {$md5mode = qq(<font color=#FF0000>MD5 ģ���Ƿ����? == [ʧ��]</font>);}

        print qq~
<tr><td bgcolor=#2159C9><font color=#FFFFFF><b>��ӭ������̳��������</b></td></tr>
<tr><td bgcolor=#EEEEEE valign=middle align=center><font color=#333333><b>��ӭ $inmembername</b></font></td></tr>
<tr><td bgcolor=#FFFFFF></td></tr>
<tr><td bgcolor=#FFFFFF valign=middle align=left>
<font color=#000000><center><br>
������ʱ�䣺<b>$current_time</b><br>
</center>
$warning
<hr>
<font color=#000000><p>
<b>��̳����ժҪ</b><br><br><br>
ע���û�����$totalmembers ��
<br>�ܷ������⣺$totalthreads ƪ
<br>�ܷ���ظ���$totalposts ƪ<br><br>
<br>ע���û�ƽ��������������$start_topic_ratio ƪ
<br>ע���û�ƽ���ظ���������$posting_ratio ƪ
<br><br>
<br>Ŀ¼·������<font color=#FF0000>$cgipath</font> == [��ȷ]
<br>Perl  �汾��<font color=#FF0000>$]</font> == [ͨ��]
<br>LBCGI �汾��<font color=#FF0000>$version_needed</font> == [ͨ��]
<br>MD5�� ���ԣ�$md5mode
<br>Gzip�����ԣ�$gzipfunc
<br>GD�������ԣ�$gdfunc
<br>Cookie���ԣ�$cookie_result
<br><br>
<form action=setmembers.cgi method=POST>
<font color=#333333><b>�鿴���༭��ɾ������ֹ�û�</b><BR>
<input type=hidden name=action value=edit>
<input type=text name=member size=10 maxlength=16>
<input type=submit value=���ٶ�λ>
</form>
<br><br><hr>
��Ȩ���У�ɽӥ(��)������ȱ</font>
</font></td></tr></table></td></tr></table>
~;
    } else {
	&cleanolddata;
	&cleanolddata4;
	&adminlogin;
        
        if (($inmembername ne "")&&($inpassword ne "")) {
	    my $thistime=time;
	    $filetomake = "$lbdir" . "data/adminlogin.cgi";
            open(FILE, ">>$filetomake");
            print FILE "$inmembername\t��$inpasswordtemp\t$ENV{'REMOTE_ADDR'}\t$trueipaddress\t\<B\>��¼ʧ��\<\/B\>\t$thistime\t\n";
            close(FILE);
            undef $thistime;
	}
    }
}
print qq~</td></tr></table></body></html>~;
exit;

sub testsystem {
    if (1 == 0) {
	print "Content-type: text/html\n\n";
	print qq(
	    <HTML><HEAD><TITLE>��ʼ������</TITLE></HEAD>
	    <BODY BGCOLOR=#ffffff TEXT=#000000>
	    <H1>LeoBBS ����</H1>������������������Ϣ����ô˵��������û����ȷִ�У�����������Ϊ��ͨ�� HTML �����ʾ��������Ҫѯ�����ķ���������Ա�����Ŀ¼�Ƿ���ִ�� CGI �����Ȩ�ޡ�<p></body></html>
	);
    	exit;
    }
    my $prog = $0;
    open (PROG, $prog);
    my @prog = <PROG>;
    close (PROG);
    my $perl = $prog[0];
    $perl =~ s/^#!//;
    $perl =~ s/\s+$//;
    if ($] < 5.004) {
	print "Content-type: text/html\n\n";
	print qq(
	    <HTML><HEAD><TITLE>��ʼ������</TITLE></HEAD>
	    <BODY BGCOLOR=#ffffff TEXT=#000000>
	    <H1>LeoBBS ����</H1><FONT COLOR=#ff0000><B>Perl �汾����</B>����ѡ��� Perl ·�� - <B>$perl</B>�������⵽���İ汾Ϊ $]���� LeoBBS ���������� Perl 5.004 ���ϰ汾�� <U>ǿ��</U> �Ƽ�����ϵ����������Ա���� Perl �� Perl 5.004 ���ϰ汾��</FONT></body></html>
	);
	exit;
    }
    $version_needed = $LBCGI::VERSION;
}

sub checkverify {
	my $verifynum = $query -> param('verifynum');
	my $sessionid = $query->param('sessionid');
	$sessionid =~ s/[^0-9a-f]//isg;
	if (length($sessionid) != 32 && $useverify eq "yes")
	{
		$inpassword = "";
		return;
	}

	###��ȡ��ʵ�� IP ��ַ
	my $ipaddress = $ENV{'REMOTE_ADDR'};
	my $trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
	$ipaddress = $trueipaddress if ($trueipaddress ne "" && $trueipaddress ne "unknown" && $trueipaddress !~ m/^192\.168\./ && $trueipaddress !~ m/^10\./);
	$trueipaddress = $ENV{'HTTP_CLIENT_IP'};
	$ipaddress = $trueipaddress if ($trueipaddress ne "" && $trueipaddress ne "unknown" && $trueipaddress !~ m/^192\.168\./ && $trueipaddress !~ m/^10\./);

	###��ȡ��ǰ���̵���֤�����֤�����ʱ�䡢�û�����
	my $filetoopen = "${lbdir}verifynum/$sessionid.cgi";
	open(FILE, $filetoopen);
	$readdisktimes++;
	my $content = <FILE>;
	close(FILE);
	unlink($filetoopen);
	chomp($content);
	my ($trueverifynum, $verifytime, $savedipaddress) = split(/\t/, $content);
	my $currenttime = time;

	if (($verifynum ne $trueverifynum || $currenttime > $verifytime + 120 || $ipaddress ne $savedipaddress)&&($useverify eq "yes")) { #��֤����Чʱ���Ϊ2����
	    $inpassword = "";
	} else {
	    unlink("${lbdir}verifynum/$sessionid.cgi");
	    unlink("${imagesdir}verifynum/$sessionid.cgi");
	    mkdir ("${lbdir}verifynum/login", 0777) unless (-d "${lbdir}verifynum/login");
	    $memberfilename = $inmembername;
	    $memberfilename =~ y/ /_/;
	    $memberfilename =~ tr/A-Z/a-z/;
            $memberfilename = "${lbdir}verifynum/login/$memberfilename.cgi";
            
	    open (FILE, ">$memberfilename");
	    print FILE "$currenttime\n";
	    close(FILE);

        }
	return;
}

# ���Ծ���·��
sub mypath {
    local $temp;
    if ($ENV{'SERVER_SOFTWARE'} =~ /apache/i) {
        if ($ENV{'SCRIPT_FILENAME'}=~ /cgiwrap/i) {
            $temp=$ENV{'PATH_TRANSLATED'};
        }
        else {
            $temp=$ENV{'SCRIPT_FILENAME'};
        }
        $temp=~ s/\\/\//g if ($temp=~/\\/);
        $mypath=$temp;
#        $mypath=substr($temp,0,rindex($temp,"/"));
    }
    else {
        $mypath=substr($ENV{'PATH_TRANSLATED'},0,rindex($ENV{'PATH_TRANSLATED'},"\\"));
        $mypath=~ s/\\/\//g;
    }
    return $mypath;
}
