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
require "admin.lib.pl";
require "bbs.lib.pl";
$|++;

$thisprog = "usermanager.cgi";
$query = new LBCGI;

$action          = $query -> param('action');
$usertype        = $query -> param('usertype');
$action          = &unHTML("$action");

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");       
&admintitle;
        
&getmember("$inmembername","no");
        
        
        if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
            
            print qq~
            <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
            <b>��ӭ������̳�������� / �û��������</b>
            </td></tr>
            ~;
            
            my %Mode = ( 
            'search' =>    \&searchusers,
            );


            if($Mode{$action}) { 
               $Mode{$action}->();
            }
            else { &searchoptions; }
            
            print qq~</table></td></tr></table>~;
        }
        else {
            &adminlogin;
        }
        
sub searchoptions {
       my $memteam1 = qq~<option value="rz1">$defrz1(��֤�û�)</option>~ if ($defrz1 ne "");
       my $memteam2 = qq~<option value="rz2">$defrz2(��֤�û�)</option>~ if ($defrz2 ne "");
       my $memteam3 = qq~<option value="rz3">$defrz3(��֤�û�)</option>~ if ($defrz3 ne "");
       my $memteam4 = qq~<option value="rz4">$defrz4(��֤�û�)</option>~ if ($defrz4 ne "");
       my $memteam5 = qq~<option value="rz5">$defrz5(��֤�û�)</option>~ if ($defrz5 ne "");

    print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
	���� <font color=red>һ���û�</font> ��Ŀ�϶࣬�뵽 <a href="setmembers.cgi">�û�����/����(*)</a> ������<br><br>
        <form method=get action="usermanager.cgi">
        <input type=hidden name="action" value="search">
        <div align=center>��ѡ����Ҫ��ѯ���û�����
	<select name="usertype">$memteam1$memteam2$memteam3$memteam4$memteam5
	<option value="rz">��֤�û�</option>
	<option value="amo">��̳������</option>
	<option value="mo">��̳����</option>
        <option value="cmo">�������ܰ���</option>
        <option value="smo">��̳�ܰ���</option>
	<option value="ad">̳��</option>
        <option value="banned">��ֹ�û�����</option>
        <option value="masked">���δ��û�����</option>
	</select> 
        <p><input type="submit" value='ȷ��'></p></div></form>
	</td></tr>
        ~;
        }

sub searchusers {
	unless ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>����</b><p>
                    
        <font color=#333333>��û��Ȩ��ʹ��������ܣ�</font>
                    
        </td></tr>
         ~;
        }

        if ($usertype eq ""){
	print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>����</b><p>
                    
        <font color=#333333>û��ѡ����Ҫ�������û����</font>
                    
        </td></tr>
         ~;
         }
         else {
	print qq~
        <tr>
        <td bgcolor=#FFFFFF colspan=2><br>
         ~;

	$filetoopen = "$lbdir" . "data/lbmember.cgi";
        open(FILE,"$filetoopen");
        flock (FILE, 1) if ($OS_USED eq "Unix");
        @memberfiles = <FILE>;
        close(FILE);
	$i=0;
        foreach $memtypedata (@memberfiles) {
	chomp $memtypedata;
        ($username, $membertype) = split(/\t/,$memtypedata);

       if ($membertype eq $usertype) {
       print qq~
       <a href="setmembers.cgi?action=edit&member=$username">$username</a><br><br>~;
       $i++;
       }
    }
       print qq~
       <br><br>
       <b>���ҵ� $i λ�û�</b><br>
       </td></tr>
       ~;
       }
     }

print qq~</td></tr></table></body></html>~;
exit;
