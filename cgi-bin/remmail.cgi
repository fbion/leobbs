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
require "bbs.lib.pl";

$|++;

$thisprog = "remmail.cgi";

$query = new LBCGI;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

@params = $query->param;
foreach $param(@params) {
    $theparam = $query->param($param);
    $theparam = &unHTML("$theparam");
    ${$param} = $theparam;
}

$inmembername = $query->cookie("amembernamecookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$member =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$member = "" if (length($member)>16);

if (lc($inmembername) eq lc($member)) {
 $filetoopen = "$lbdir" . "data/remmem.cgi";
 open (FILE,"$filetoopen");
 flock (FILE,2);
  @members = <FILE>;
 close (FILE);

foreach $removed (@members) {
 chomp($removed);
 if ($removed eq $member) {
  $output = qq~
   <tr bgcolor="#FFFFFF">
   <td align="center">
   ��ã�$member�����Ѿ��˳� LeoBBS �ʼ��б��ˡ�
   </td>
   </tr>
  ~;
  &displayoutput;
 }
}


$filetoopen = "$lbdir" . "data/remmem.cgi";
open (FILE,">>$filetoopen");
 print FILE "$member\n";
close (FILE);

$adminemail_out = &encodeemail($adminemail_out);
$output = qq~
 <tr bgcolor="#FFFFFF">
 <td align="center">
 ��ã�$member�����Ѿ��˳� LeoBBS �ʼ��б��ˡ�
 <br>����������¼��룬����ϵ <a href="mailto:$adminemail_out">̳��</a> ��
 </td>
 </tr>
~;
&displayoutput;

} else {

$output = qq~
 <tr bgcolor="#FFFFFF">
 <td align="center">
 �Բ������ Cookie ��ƥ�䡣<br>��������˳����ʼ��б���ô�������ȵ�¼��̳��
 <br><a href="loginout.cgi">���˵�¼������</a>
 </td>
 </tr>
~;
&displayoutput;
}

sub displayoutput {

print qq~
 <html>
 <head>
 <title></title>
 </head>
 <body bgcolor="#FFFFFF">
 <table border="0" align="center" width="456">
 <tr>
 <br><br><td bgcolor=#EEEEEE align="center" colspan=2><font color=#333333 size=3><b>��ӭʹ�� LeoBBS �ʼ��б�</td>
 </tr>
 $output
 </table>
 </body>
 </html>~;
exit;
}
