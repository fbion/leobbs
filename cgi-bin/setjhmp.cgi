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
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 1;
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "setjhmp.cgi";
$query = new LBCGI;
#&ipbanned; #��ɱһЩ ip

$addme=$query->param('addme');

for('action','jhmpid','jhmpname','jhmpstatus','jhmporganiger'){
	my $theparam = $query->param($_);
    $theparam = &cleaninput("$theparam");
	${$_} = $theparam;
}
$checkaction    =  ($query->param('checkaction') eq "yes")?"yes":"no";

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

my %Mode = ('createform' => \&createform,
            'processnew' => \&createaction,
	    'edit'       => \&editform,
	    'processedit'=> \&editaction,
	    'delete'     => \&deleteaction
	  );

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;
&getmember("$inmembername","no");
if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
    print qq~
    <tr><td bgcolor="#2159C9" colspan=2><font color=#FFFFFF>
    <b>��ӭ������̳�������� / ���ɹ�����</b>
    </td></tr>~;
    if ($Mode{$action}) { 
        $Mode{$action}->();
    } else {
        &jhmplist;
    }
    print qq~</table></td></tr></table>~;
} else {
    &adminlogin;
}

sub jhmplist {
    print qq~
    <script language="javascript">
	function O9(id) {if(id!="")window.open("profile.cgi?action=show&member="+id);}
	</script>
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#990000><b>ע������</b>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF colspan=2 align=center>
    ���������棬��������Ŀǰ���е����ɡ�����������һ���µ����ɡ�Ҳ���Ա༭��ɾ��Ŀǰ�������ɡ�<p>
    </td>
    </tr>
    ~;

    $filetoopen = "$lbdir" . "data/jhmp.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @jhmp = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
	chomp @jhmp;
	@jhmp = grep(/^(.+?)\t[1|0]\t/,@jhmp);

	print qq~
    <tr>
    <td bgcolor=#FFFFFF align=center colspan=2><table width=90% cellspacing="0" cellpadding="2">
	<tr><td align="center" colspan="4" bgcolor="#EEEEEE">|| <a href="$thisprog?action=createform">����������</a> ||</td></tr>
	<tr><td align="center" bgcolor=$catback><b style="color:blue">��������</b></td><td align="center" width="20%" bgcolor=$catback><b style="color:blue">���ɴ�����</b></td><td align="center" width="10%" bgcolor=$catback><b style="color:blue">����״̬</b></td><td align="center" width="30%" bgcolor=$catback><b style="color:blue">��ز���</b></td></tr>
	~;
    $jhmpnum = 0;
    foreach $jhmp (@jhmp) {
    	chomp $jhmp;
    	next if($jhmp eq "");
		($jhmpname, $jhmpstatus, $jhmporganiger) = split(/\t/,$jhmp);
		$jhmpurl=~s/\\//g;
		$jhmpnum++;
		$jhmpstatus=($jhmpstatus)?"��������":"��������";
		print qq~
		<tr><td align="left">����<b>$jhmpname</b></td><td align="center"><span style="cursor:hand" onClick="javascript:O9('$jhmporganiger')"><font color="#333333"><u>$jhmporganiger</u></font></span></td><td align="center"><u>$jhmpstatus</u></td><td align="center"><a href="$thisprog?action=edit&jhmpid=$jhmpnum">[�༭]</a> <a href="$thisprog?action=delete&jhmpid=$jhmpnum">[ɾ��]</a></td></tr>
	    ~;
	}
    
    
	print qq~
	<tr><td align="center" colspan="4" bgcolor="#EEEEEE">�������� $jhmpnum �� </td></tr></table>
	~;
}
sub createform{
    print qq~
    <script language="javascript">
	function O9(id) {if(id!="")window.open("profile.cgi?action=show&member="+id);}
	</script>
    <form action="$thisprog" method="post">
    <input type=hidden name="action" value="processnew">    
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left width=40%>
    <font color=#333333><b>��������</b><br>�����������ɵ�����<BR></font></td>
    <td bgcolor=#FFFFFF valign=middle align=left>
    <input type=text size=20 name="jhmpname" value=""></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left width=40%>
    <font color=#333333><b>����״̬��</b><br>��ѡ�����ɵĿ���״̬</font></td>
    <td bgcolor=#FFFFFF valign=middle align=left>
    <select name="jhmpstatus"><option value="1">���ţ��������ɼ���</option><option value="0">���أ����������ɼ���</option></select>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left width=40%>
    <font  color=#333333><b>���ɴ�����</b><br>���������ɵĴ�����</font></td>
    <td bgcolor=#FFFFFF valign=middle align=left>
    <input type=text size=20 name="jhmporganiger" value="$inmembername"> <input type=button value="���" onClick="O9(this.form.jhmporganiger.value)"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
    <input type=submit value="�� ��"></form>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">����</a> --</td>
    </tr>
    ~;
}
sub editform {
    $filetoopen = "$lbdir" . "data/jhmp.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @jhmp = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
	chomp @jhmp;
	@jhmp = grep(/^(.+?)\t[1|0]\t/,@jhmp);
    unless (defined $jhmp[$jhmpid-1]){&errorout("�����ɲ����ڣ�"); return;}
    ($jhmpname,$jhmpstatus,$jhmporganiger) = split(/\t/,$jhmp[$jhmpid-1]);   
    $jhmpurl=~s/\\//g;
	$jhmpstatus_select=qq(<option value="1">���ţ��������ɼ���</option><option value="0">���أ����������ɼ���</option>);
	$jhmpstatus_select=~s/ value="$jhmpstatus">/ value="$jhmpstatus" selected>/;
    print qq~
    <script language="javascript">
	function O9(id) {if(id!="")window.open("profile.cgi?action=show&member="+id);}
	</script>
    <form action="$thisprog" method="post">
    <input type=hidden name="action" value="processedit">
    <input type=hidden name="jhmpid" value="$jhmpid">
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left width=40%>
    <font color=#333333><b>��������</b><br>�����������ɵ�����<BR></font></td>
    <td bgcolor=#FFFFFF valign=middle align=left>
    <input type=text size=20 name="jhmpname" value="$jhmpname"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left width=40%>
    <font color=#333333><b>����״̬��</b><br>��ѡ�����ɵĿ���״̬</font></td>
    <td bgcolor=#FFFFFF valign=middle align=left>
    <select name="jhmpstatus">$jhmpstatus_select</select>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left width=40%>
    <font  color=#333333><b>���ɴ�����</b><br>���������ɵĴ�����</font></td>
    <td bgcolor=#FFFFFF valign=middle align=left>
    <input type=text size=20 name="jhmporganiger" value="$jhmporganiger"> <input type=button value="���" onClick="O9(this.form.jhmporganiger.value)"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
    <input type=submit value="�� ��"></form>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">����</a> --</td>
    </tr>
    ~;
}
sub createaction {
    if ($jhmpname eq "" || $jhmporganiger eq ""){&errorout("�������Ƽ������˲���Ϊ�գ�"); return;}
    if(length($jhmpname)>21) {&errorout("�������ɹ������벻Ҫ����20���ַ���10�����֣���"); return;}
    $jhmpstatus=($jhmpstatus)?1:0;
    $filetoopen = "$lbdir" . "data/jhmp.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @jhmp = <FILE>;
    close(FILE);
	chomp @jhmp;
	@jhmp = grep(/^(.+?)\t[1|0]\t/,@jhmp);
	@exisjhmp = grep(/^$jhmpname\t[1|0]\t/,@jhmp);
    if (@exisjhmp){&errorout("�����������ѱ�ʹ�ã�"); return;}
	
    open(FILE, ">$filetoopen");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    print FILE "########################################\n";
    print FILE "# LeoBBS auto-generated config file    #\n";
    print FILE "# Do not change anything in this file! #\n";
    print FILE "########################################\n";
	foreach $jhmp (@jhmp) {
    next if ($jhmp eq "");
	chomp $jhmp;
    print FILE "$jhmp\n";
    }
    print FILE "$jhmpname\t$jhmpstatus\t$jhmporganiger\t\n";
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    
    print qq~
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
    <fon color=#2159C9><b>���ӽ��</b><p>
    <li>������ <B>$jhmpname</b> �Ѿ�������
    <br><BR><a href=$thisprog?action=createform>������������</a>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">����</a> --</td>
    </tr>
    ~;
}
sub editaction {
    if ($jhmpname eq "" || $jhmporganiger eq ""){&errorout("�������Ƽ������˲���Ϊ�գ�"); return;}
    if(length($jhmpname)>21) {&errorout("�������ɹ������벻Ҫ����20���ַ���10�����֣���"); return;}
    $jhmpstatus=($jhmpstatus)?1:0;
    $filetoopen = "$lbdir" . "data/jhmp.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @jhmp = <FILE>;
    close(FILE);
	chomp @jhmp;
	@jhmp = grep(/^(.+?)\t[1|0]\t/,@jhmp);
    unless (defined $jhmp[$jhmpid-1]){&errorout("�����ɲ����ڣ�"); return;}
	@exisjhmp = grep(/^$jhmpname\t[1|0]\t/,@jhmp);
#    if (@exisjhmp){&errorout("�����������ѱ�ʹ�ã�"); return;}
    
    open(FILE,">$filetoopen");
    flock(FILE,2) if ($OS_USED eq "Unix");
    print FILE "########################################\n";
    print FILE "# LeoBBS auto-generated config file    #\n";
    print FILE "# Do not change anything in this file! #\n";
    print FILE "########################################\n";
	$jhmpnum = 0;
	foreach $jhmp (@jhmp) {
    next if ($jhmp eq "");
	chomp $jhmp;
    $jhmpnum ++;
		if ($jhmpid eq $jhmpnum) {
	($oldjhmpname,undef,undef)=split(/\t/,$jhmp);
    print FILE "$jhmpname\t$jhmpstatus\t$jhmporganiger\t\n";
		} else {
	print FILE "$jhmp\n";
		}
	}
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    
    print qq~
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
    <fon color=#2159C9><b>�༭���</b><p>
    <li>���� <B>$oldjhmpname</b> �Ѿ����£�
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">����</a> --</td>
    </tr>
    ~;
}
sub deleteaction {
	if($checkaction ne "yes"){
    $filetoopen = "$lbdir" . "data/jhmp.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @jhmp = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
	chomp @jhmp;
	@jhmp = grep(/^(.+?)\t[1|0]\t/,@jhmp);
    unless (defined $jhmp[$jhmpid-1]){&errorout("�����ɲ����ڣ�"); return;}
    ($jhmpname,$jhmpstatus,$jhmporganiger) = split(/\t/,$jhmp[$jhmpid-1]);   
    print qq~
    <tr>
    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
    <font color=#990000><b>���棡��</b>
    </td></tr>
    
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
    <font color=#333333>�����ȷ��Ҫɾ������ <u>$jhmpname</u>����ô������������<p>
    >> <a href="$thisprog?action=delete&checkaction=yes&jhmpid=$jhmpid">ɾ������</a> <<
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">����</a> --</td>
    </tr>
    ~;
    return;
	}
    $filetoopen = "$lbdir" . "data/jhmp.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @jhmp = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
	chomp @jhmp;
	@jhmp = grep(/^(.+?)\t[1|0]\t/,@jhmp);
    unless (defined $jhmp[$jhmpid-1]){&errorout("�����ɲ����ڣ�"); return;}

    open(FILE,">$filetoopen");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    print FILE "########################################\n";
    print FILE "# LeoBBS auto-generated config file    #\n";
    print FILE "# Do not change anything in this file! #\n";
    print FILE "########################################\n";
	$jhmpnum = 0;
	foreach $jhmp (@jhmp) {
    next if ($jhmp eq "");
	chomp $jhmp;
    $jhmpnum ++;
		if ($jhmpid eq $jhmpnum) {
	($oldjhmpname,undef,undef)=split(/\t/,$jhmp);
		}else{
	print FILE "$jhmp\n";
		}
	}
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

    print qq~
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
    <fon color=#2159C9><b>ɾ�����</b><p>
    <li>���� <B>$oldjhmpname</B> �ѱ�ɾ����
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">����</a> --</td>
    </tr>
    ~;
}
sub errorout{
	#sub errorout v2.0
	my $errormsg=shift;
    print qq~
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#990000><b>�����ʽ���e</b>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF align="center" colspan=2><font color=red>$errormsg</font></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">����</a> --</td>
    </tr>
    ~;
}