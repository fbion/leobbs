#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

    $ingetpassq        = &cleaninput($query -> param("getpassq"));
    $ingetpassa        = &cleaninput($query -> param("getpassa"));

    $inmembernamefile = $inmembername;
    $inmembernamefile =~ s/ /\_/g;
    $inmembernamefile =~ tr/A-Z/a-z/;

    opendir (DIRS, "${lbdir}$msgdir");
    my @files = readdir(DIRS);
    closedir (DIRS);
    @files = grep(/\.cgi$/i, @files);
    foreach (@files) {unlink ("${lbdir}$msgdir/$_") if ((-M "${lbdir}$msgdir/$_") > 1);}

    if (-e "${lbdir}$msgdir/$inmembernamefile.cgi") {
    	&error("������ʧ��&�벻Ҫ�ظ���ȡ���룬��̳�涨�û�ÿ�������Ӳ���ȡ������һ�Σ�") if((-M "${lbdir}$msgdir/$inmembernamefile.cgi") *86400 < 900);
    }

    if ($password ne "") {
    	if (-e "${lbdir}$msgdir/$inmembernamefile.cgi") {
    	    open(FILE, "${lbdir}$msgdir/$inmembernamefile.cgi");
    	    $x = <FILE>;
    	    close(FILE);
    	    chomp $x;
	} else {
	    $x = &myrand(1000000000);
	    $x = crypt($x, aun);
	    $x =~ s/%([a-fA-F0-9]{2})/pack("C", hex($1))/eg;
	    $x =~ s/[^\w\d]//g;
	    $x = substr($x, 2, 6);
	}
    	open(FILE, ">${lbdir}$msgdir/$inmembernamefile.cgi");
    	print FILE "$x";
    	close(FILE);
    	$password = "$x$password";
        eval {$password = md5_hex($password);};
        if ($@) {eval('use Digest::MD5 qw(md5_hex);$password = md5_hex($password);');}
    }
    else { &error("������ʧ��&������������Ѿ���ʧ������ϵ����Ա�޸���"); }

    if (($membercode eq "ad")||($membercode eq "smo")) { require "doblocked.pl"; }
    elsif (($ingetpassq ne "")&&($ingetpassa ne "")) {
	my ($getpassq, $getpassa) =split(/\|/,$userquestion); 
	if(($ingetpassq eq $getpassq)&&($ingetpassa eq $getpassa)&&($membercode ne "mo")&&($membercode ne "amo")&&($membercode ne "cmo")){
	    $inmembername1 = uri_escape($inmembername);
	    $output .= qq~ 
<tr><td bgcolor=$titlecolor $catbackpic valign=middle align=center><font color=$fontcolormisc><b>��ã�$inmembername</b></font></td></tr> 
<tr><td bgcolor=$miscbackone align=center><font color=$fontcolormisc>Ӧ����Ҫ���ֽ�������̳�����ȡ��ʽ������</td></tr> 
<tr><td bgcolor=$miscbackone align=center><font color=$fontcolormisc> 
�����û����ƣ�$inmembername<br><br><B><a href="$boardurl/getmypass.cgi?username=$inmembername1&password=$password">�밴�˻��������̳����</a></B><br><br>
ע�⣺��������һ���ʧЧ���뾡����ʲ����������޸ġ�<BR><BR>
</td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT><BR><BR>
~;
	} else { 
	    $output .= qq~
<tr><td bgcolor=$titlecolor $catbackpic valign=middle align=center><font color=$fontcolormisc><b>�ǳ���Ǹ��$inmembername</b></font></td></tr>
<tr><td bgcolor=$miscbackone align=center><font color=$fontcolormisc>
�����������̳������ʾ����ʹ𰸲���ȷ��������û���ڸ�����������д�������޷�ȡ�أ� (ע��������ǰ��񣬳��ڰ�ȫ���ǣ������ʼ�ȡ����̳���룡)
</td></tr></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
	    unlink ("${lbdir}$msgdir/$inmembernamefile.cgi");
	    }
	}
	elsif ($emailfunctions eq "off") {
	    $output .= qq~
<tr><td bgcolor=$titlecolor $catbackpic valign=middle align=center><font color=$fontcolormisc><b>�ǳ���Ǹ��$inmembername</b></font></td></tr>
<tr><td bgcolor=$miscbackone align=center><font color=$fontcolormisc>
���������̳�ķ����ʼ������Ѿ��رգ���ͨ�������;������ϵ̳������ȡ������̳���룡
</td></tr></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
	}
	elsif ($userregistered ne "no") {
	    $inmembername1 = uri_escape($inmembername);
	    eval("use MAILPROG qw(sendmail);");
	    $message .= "\n";
	    $message .= "$boardname <br>\n";
	    $message .= "$boardurl/leobbs.cgi \n<br><br>\n";
	    $message .= "------------------------------------------------<br>\n";
	    $message .= "Ӧ����Ҫ���ֽ�������̳�����ȡ��ʽ�ĸ�����\n <br><br>\n";
	    $message .= "�����û�����$inmembername <br>\n";
	    $message .= "������̳���밴�˻�ã� $boardurl/getmypass.cgi?username=$inmembername1&password=$password \n <br><br>\n";
	    $message .= "ע�⣺��������һ���ʧЧ���뾡����ʲ����������޸ġ�<br><br>\n";
	    $message .= "------------------------------------------------<br>\n";
	    $to = $emailaddress;
	    $from = $adminemail_out;
	    $subject = "������̳����[$boardname]";
	    if (&sendmail($from, $from, $to, $subject, $message)) {
                $output =~ s/�û�����/��̳�����Ѿ��ĳ�/g;
                $output .= qq~
<tr><td bgcolor=$titlecolor $catbackpic valign=middle align=center><font color=$fontcolormisc><b>��ã�$inmembername</b></font></td></tr>
<tr><td bgcolor=$miscbackone align=center><font color=$fontcolormisc>������̳�����ȡ��ʽ�Ѿ��ɹ���ͨ��ָ�����ʼ���ַ���͸����ˡ�</td></tr></table></td></tr></table>
~;
	    } else {
		&error("�����ʵ�ʧ��&�ƺ������������ʼ������г���һЩ���⣬���Ժ����ԡ�");
	    }
	} else {
	    &error("������̳����&����������ע���û���");
	}
1;
