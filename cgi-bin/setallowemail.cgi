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
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "setallowemail.cgi";
$query = new LBCGI;


$action       = ($query -> param('action') ne "")?'process':'toppage';
$wordarray    = $query -> param('wordarray');
$select_type  = ($query -> param('select_type') eq "allow")?'allow':'ban';

$inmembername = $query->cookie('adminname');
$inpassword   = $query->cookie('adminpass');
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;


my %Mode = ('process' => \&process);

#################--- Main program ---###################
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;
&getmember("$inmembername","no");
	if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
		print qq~
		<tr><td bgcolor="#2159C9" colspan=2><font color=#FFFFFF>
		<b>��ӭ������̳�������� / ����(����)��ע������</b>
		</td></tr>~;
		if($Mode{$action}) { 
			$Mode{$action}->();
		} else {
			&toppage;
		}
		print qq~</td></tr></table></td></tr></table>~;
	} else {
		&adminlogin;
	}
sub toppage{
	$allowmail = "";
	$filetoopen = "$lbdir" . "data/allow_email.cgi";
	open (FILE, "$filetoopen");
	$allowtype = <FILE>;
	$allowmail = <FILE>;
	close (FILE);
	chomp $allowtype;
	chomp $allowmail;
	$allowmail =~s/\t/\n/g;
	$allowmail =~s/ //g;
	$allowtype = ($allowtype eq "allow")?'allow':'ban';
	$select_type{$allowtype} = ' checked';
	
	
	print qq~
	<form action="$thisprog" method="post">
	<tr>
	<td bgcolor="#EEEEEE" align="center" colspan="2">
	<font color="#333333"><b>���ƿ�ע������</b>
	</td>
	</tr>
	<tr>
	<td bgcolor="#FFFFFF" align="center" colspan="2">
	<table width=80% align=center>
	<tr><td><ol type="1">
	<li>�˹��ܿ����Ʊ�����ĳЩ����ע�ᡣ
	<li>Ҳ������ĳ�������䲻��ע�ᣬ��ֹ������������ע�ᡣ
	<li>�����ʱ��ÿ������һ�������������ɡ�<B><U>���ü����ʺ����ƺ� \@ ��</U></B>��
	<li>������������������ִ�Сд��
	<LI>���磬���� hotmail.com�����Ʒ�ʽΪ�����ϵ����䲻����ע�ᡱ��<BR>�����;ܾ�������ʹ�� hotmail.com �������ǰ��ע�ᡣ
	</ol></td></tr>
	</table>
	</td>
	</tr>
	
	<input type=hidden name="action" value="process">
	
	<tr>
	<td bgcolor="#FFFFFF" align="center" colspan="2">
	<textarea cols=60 rows=20 wrap="virtual" name="wordarray">$allowmail</textarea>
	</td>
	</tr>
	<tr>
	<td bgcolor="#FFFFFF" width="30%" align="right">���Ʒ�ʽ��
	</td>
	<td bgcolor="#FFFFFF"><input type="radio" name="select_type" value="allow"$select_type{'allow'}>����Ϊ�����������ע�� <input type="radio" name="select_type" value="ban"$select_type{'ban'}>���ϵ����䲻����ע��</td>
	</tr>
	
	<tr>
	<td bgcolor="#FFFFFF" align="center" colspan="2">
	<input type=submit name=submit value="�� ��">
	</td>
	</tr>
	</form>
	~;
}
sub process{
	$output_text = ($select_type eq "allow")?'ֻ��ʹ����Щ����ע��':'ʹ����Щ����ע�᲻��ע��';
	$select_type .= "\n";
	$wordarray .= "\n";
	$wordarray =~ s/[\a\f\e\0\r\t ]//isg;
	$wordarray =~ s/\r\n/\n/ig;
	$wordarray =~ s/\n+/\n/ig;
	$wordarray =~ s/\n/\t/isg;
	$filetoopen = "$lbdir" . "data/allow_email.cgi";
	open (FILE, ">$filetoopen");
	print FILE $select_type;
	print FILE $wordarray;
	close (FILE);
	
	print qq~
	<tr>
	<td bgcolor="#EEEEEE" align="center" colspan="2">
	<font color="#333333"><b>���������Ѿ�����</b>
	</td>
	</tr>
	<tr>
	<td bgcolor="#FFFFFF" align="center" colspan="2">
	<font color="#333333"><b>�����������䱻���棬$output_text��</b>
	</td>
	</tr>
	<tr>
	<td bgcolor="#FFFFFF" align="center" colspan="2">
	<table width=80% align=center>
	<tr><td>
	<ol>
	~;
	@savedwordarray = split(/\t/,$wordarray);
	foreach $word(@savedwordarray) {
		chomp $word;
		print qq~<li>$word~;
	}
	print qq~
	</ol></td></tr>
	</table>
	</td>
	</tr>
	<tr>
	<td bgcolor="#FFFFFF" align="center" colspan="2">
	<a href="$thisprog?"><font color="#333333">��������Ҫ���Ƶ�����</font></a>
	</td>
	</tr>
	~;
}