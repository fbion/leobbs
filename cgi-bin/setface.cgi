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
#use URI::Escape;
$LBCGI::POST_MAX=500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
require "data/cityinfo.cgi";
require "face/config.pl";
require "facelib.pl";
$|++;
$thisprog = "setface.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;
if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else {
    $boardurltemp =$boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
}

#&ipbanned; #��ɱһЩ ip
$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) { require "${lbdir}data/skin/${inselectstyle}.cgi"; }

$inmembername = $query->cookie("amembernamecookie");
$inpassword   = $query->cookie("apasswordcookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));

if ($inmembername eq "" || $inmembername eq "����" ) {
    &error("���ܽ��� $plugname &��Ŀǰ������Ƿÿͣ����ȵ�½!");
    exit;
} else {
#    &getmember("$inmembername");
    &getmember("$inmembername","no");
    &error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
     if ($inpassword ne $password) {
	$namecookie  = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie  = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("��ͨ����&�������û���������������µ�¼��");
     }
}

&title;

$tempmembername = $membername;
$tempmembername =~ s/ /\_/g;
$tempmembername =~ tr/A-Z/a-z/;

$admin_user =~ s/ /\_/g;
$admin_user =~ tr/A-Z/a-z/;

if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

&error("$plugname ��̨����&ֻ����̳̳����������Ա���ܽ��������") if (($membercode ne "ad")&&($admin_user ne "$tempmembername"));

print $query->header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
$output .= qq~
<BODY>
<br>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> �����������Թ���װ�������͡����ú͹��������������</td></tr></table>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3 height=25><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=11> <font face="$font" color=$navfontcolor> <a href="leobbs.cgi">$boardname</a> �� <a href=face.cgi>$plugname</a> <img src=$imagesurl/images/fg.gif width=1 height=10> [<a href=setface.cgi>��̨����</a>]<td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td>
<table cellpadding=2 cellspacing=1 border=0 width=100%>
<tr><td height=30 bgcolor=$titlecolor $catbackpic><font color=$titlefontcolor>
&nbsp;<B><a href=$thisprog?action=set>��������</a> | <a href=$thisprog?action=sortm>������</a> | <a href=$thisprog?action=add_sp>���ӵ�һ��Ʒ</a> | <a href=$thisprog?action=edit>��Ʒ����</a> | <a href=$thisprog?action=view>�鿴�û���Ϣ</a></b></td></table>~;


$action = $query -> param('action');

my %Mode = (
	'set'=> \&bset,			# ��������
	'sortm'=> \&sort_manage,
	'edit_sort'=> \&edit_sort,	# �༭�����Ϣ
	'putjs'=> \&putjs,		# ������JS�ļ�
	'edit_cate'=> \&edit_cate,	# �༭����
	'del_cate'=> \&del_cate,	# ɾ������
	'add_cate'=> \&add_cate,	# ���ӷ���
	'upmenujs'=> \&upmenujs,	# �������˵���ʽ
	'add_sp'=> \&add_sp,		# ���ӵ�һ��Ʒ
	'view'=> \&view_user,		# �鿴�û���Ϣ
	'edit'=> \&edit_sp,		# �༭��ɾ����Ʒ��Ϣ
);

if ($Mode{$action})
{$Mode{$action} -> () ;}
else
{&main();}


sub main
{
    $output .= qq~<table cellpadding=6 cellspacing=1 width=100%>
    <tr align=middle bgcolor=$miscbacktwo><td>�� �� �� ̨ �� �� ˵ ��</td></tr>
    <tr align=middle bgcolor=$forumcolortwo><td align="left" valign="top">
����<B>��ӭ��ʹ���װ�������̳���������̨����ϵͳ�� </B><P>
�����������á�����- ���ò���Ļ���������ֻ��̳�����ܽ��������<P>
��������������- ���ӡ��༭��ɾ���������װ������JavaScript����ȣ�<P>
�������ӵ�һ��Ʒ��- ������ͨ��Ʒ��Ϣ��<P>
������Ʒ��������- �༭��ɾ����Ʒ��Ϣ��<P>
�����鿴�û���Ϣ��- �鿴�û���ǰ��װ�������<P>
���������Ȩ���У� <a href=http://www.lzeweb.com/ target=_blank>��Ԫ����</a>����������ƣ���ǿ(CPower)
    </td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
}


sub bset	# ��������
{
    &error("��������&��ѡ��ֻ�б���̳̳������ʹ�ã�") if ($membercode ne "ad");
    my $checked	= $query -> param('checked');
    if ($checked eq "yes")
    {
	my $new1 = $query -> param('plugname');	# �������
	my $new2 = $query -> param('close_plug');	# ���״̬
	my $newau = $query -> param('admin_user');	# �������Ա
	my $new3 = $query -> param('samnum');	# ��ͬװ�����������
	my $new4 = $query -> param('lognum');	# ϵͳ��¼����
	my $new6 = $query -> param('show_pagen');	# ÿҳ��ʾ��Ʒ��
	my $new7 = $query -> param('row_num');	# ÿ����ʾ��Ʒ��
	my $new8 = $query -> param('c_width');	# ÿ����Ʒ�ı����

	my $filetomake = $lbdir . "face/config.pl";
	&winlock($filetomake) if ($OS_USED eq "Nt");
	open(FILE, ">$filetomake");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	print FILE qq~\$admin_user = '$newau';
\$plugname = '$new1';
\$close_plug = '$new2';
\$samnum = '$new3';
\$lognum = '$new4';
\$show_pagen = '$new6';
\$row_num = '$new7';
\$c_width = '$new8';
\$td = 'td align=center';
1;~;
	close(FILE);
	&winunlock($filetomake) if ($OS_USED eq "Nt");

	$output .= qq~

<table cellPadding=6 cellSpacing=1 border=0 width=100%>
<tr><td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>�޸ĳɹ�</b></font></td></tr>
</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog?action=set">~;
    }
    else
    {
	$tempoutput = "<select name=\"close_plug\">\n<option value=\"open\">��������\n<option value=\"close\">��ʱ�ر�\n</select>\n";
	$tempoutput =~ s/value=\"$close_plug\"/value=\"$close_plug\" selected/;

	$output .= qq~

<table cellPadding=6 cellSpacing=1 width=100%>
<form action=$thisprog method=POST>
<input type=hidden name=action value="set">
<input type=hidden name=checked value="yes">
<tr bgcolor=$miscbacktwo>
<td colspan=4 align=center><font color=$fontcolormisc><b>[ �� �� �� �� ]</b></font></td>
</tr>
<tr bgcolor=$miscbackone>
<td><font color=$fontcolormisc>�������</font></td><td><input type=text size=15 name="plugname" value=$plugname></td>
<td><font color=$fontcolormisc>���״̬</font></td><td>$tempoutput</td>
</tr>
<tr bgcolor=$miscbackone>
<td><font color=$fontcolormisc>�������Ա</font></td><td><input type=text size=15 name="admin_user" value=$admin_user></td>
<td><font color=$fontcolormisc>��ͬװ�����������</font></td><td><input type=text size=10 name="samnum" value=$samnum></td>
</tr>
<tr bgcolor=$miscbacktwo>
<td><font color=$fontcolormisc>ϵͳ��¼����</font></td><td><input type=text size=10 name="lognum" value=$lognum></td>
<td><font color=$fontcolormisc>ÿҳ��ʾ��Ʒ��</font></td><td><input type=text size=3 name="show_pagen" value=$show_pagen></td>
</tr>
<tr bgcolor=$miscbacktwo>
<td><font color=$fontcolormisc>ÿ����ʾ��Ʒ��</font></td><td><input type=text size=2 name="row_num" value=$row_num></td>
<td><font color=$fontcolormisc>ÿ����Ʒ�ı����</font></td><td><input type=text size=5 name="c_width" value=$c_width></td>
</tr>

<tr bgcolor=$miscbacktwo><td colspan=4 align=center><input type=submit name=submit value="ȷ ��">����<input type=reset value=�ء���></td></form></tr>
</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
    }
}

sub sort_manage
{
    my $filetoopen = "$lbdir" . "face/category.pl";	# �����
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @cate = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

    $filetoopen = "$lbdir" . "face/class.cgi";		# С����
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @sort = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

    $output .= qq~
<script>
function OUTJS()
{if(!confirm("�Ƿ�ȷ����� JS �˵��ļ���"))return false;}
function DEL()
{if(!confirm("$membername�����������ɻָ������Ƿ�ȷ��ɾ����"))return false;}
</script>
<table cellPadding=6 cellSpacing=1 width=100%>
<form action=$thisprog method=POST>
<input type=hidden name=action value="set">
<input type=hidden name=checked value="yes">
<tr bgcolor=$miscbacktwo>
<td colspan=5 align=center><font color=$fontcolormisc><b>[ �� �� �� �� ]</b></font></td>
</tr>

<tr bgcolor=$miscbackone>
<td colspan=5>[<a href="$thisprog?action=add_cate">�����µķ���</a>] - [<a href="$thisprog?action=upmenujs" onclick="return OUTJS();">�������˵���ʽ</a>]</td>
</tr>~;

    foreach (@cate)
    {
	chop($_);
	($cate_id,$cate_state,$cate_name,$cate_info) = split(/\t/,$_);
	$cate_state = $cate_state eq 1 ? '<font color=blue>����</font>' : '<font color=red>�ر�</font>';
        $output .=qq~
	<tr bgcolor=#EEEEEE><td colspan=5 height=30>�������ƣ�$cate_name��$cate_state [<a href="$thisprog?action=edit_cate&id=$cate_id">�༭�˷���</a>]  [<a href="$thisprog?action=del_cate&id=$cate_id" onclick="return DEL();">ɾ���˷���</a>]</td></tr>
	<tr bgcolor=$miscbacktwo align=center><td width=120>�������</td><td width=80></td><td width=80></td><td width=50>���״̬</td><td width=320>�������</td></tr>~;
	
	foreach (@sort)
	{
            chomp $_;
	    ($cateid,$sort_id,$sort_status,$sortname,$sortinfo) = split(/\t/,$_);

	    if($cate_id eq $cateid)
	    {
		$status = $sort_status eq 1 ? '<font color=blue>����</font>' : '<font color=red>�ر�</font>';
		$jsinfo = $sort_status eq 1 ? "<a href=$thisprog?action=putjs&id=$sort_id>���JS�ļ�</a>" : "";

	        $output .=qq~<tr bgcolor=$miscbackone><td>$sortname</td><td align=center>$jsinfo</td><td align=center><a href="$thisprog?action=edit_sort&id=$sort_id">�༭</a>$msort</td><td width=50 align=center>$status</td><td>$sortinfo</td></tr>~;
	    }
        }
   }

   $output .=qq~<tr bgcolor=#EEEEEE><td colspan=5 height=30>�������ƣ�����</td></tr><tr bgcolor=$miscbacktwo align=center><td width=120>�������</td><td width=80></td><td width=80></td><td width=50>���״̬</td><td width=320>�������</td></tr>~;

    foreach (@sort)
    {
        chomp $_;
	($cateid,$sort_id,$sort_status,$sortname,$sortinfo) = split(/\t/,$_);

        if($cateid eq '')
	{
            $output .=qq~<tr bgcolor=$miscbackone><td>$sortname</td><td align=center></td><td align=center><a href="$thisprog?action=edit_sort&id=$sort_id">�༭</a>$msort</td><td width=50 align=center><font color=red>�ر�</font></td><td>$sortinfo</td></tr>~;
	}
    }
    $output .=qq~</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
}

sub edit_sort
{
    my $id = $query -> param('id');
    my $edit = $query -> param('edit');
    if($edit eq 'y')
    {
	$new_cname	= $query -> param('catename');
	$new_name	= $query -> param('sort_name');
	$new_status	= $query -> param('sort_status');
	$new_explain	= $query -> param('sort_explain');
	&error("�༭���&��Ʒ������ֲ��ܿգ���") if($new_name eq '');
	&error("�༭���&��Ʒ����������ܿգ���") if($new_explain eq '');

        my $filetoopen = "$lbdir" . "face/class.cgi";
	open(FILE,"$filetoopen");
        my @sort = <FILE>;
        close(FILE);

	open(FILE,">$filetoopen");
	for($i=0;$i<@sort;$i++)
	{
	    ($cateid,$old_id,$old_status,$old_name,$old_info)=split(/\t/,@sort[$i]);

	    if($old_id eq $id)	# ����ҵ����ϵ���������д���µ�����
	    {
		print FILE "$new_cname\t$old_id\t$new_status\t$new_name\t$new_explain\n";
	    }
	    else
	    {print FILE "$cateid\t$old_id\t$old_status\t$old_name\t$old_info";}
        }
	close(FILE);
	$output .= qq~
<table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>�� �� �� ��</b></font></td></tr>
</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="1; url=$thisprog?action=sortm">~;
    }
    else
    {
	my $filetoopen = "$lbdir" . "face/class.cgi";
	&winlock($filetoopen) if ($OS_USED eq "Nt");
	open(FILE,"$filetoopen");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	@sort = <FILE>;
	close(FILE);
	&winunlock($filetoopen) if ($OS_USED eq "Nt");
	for($i=0;$i<@sort;$i++)
	{
	    ($cateid,$sort_id,$sort_status,$sort_name,$sort_info) = split(/\t/,@sort[$i]);
	    last if($sort_id eq $id);
	}

	$filetoopen = "$lbdir" . "face/category.pl";	# �����
	&winlock($filetoopen) if ($OS_USED eq "Nt");
	open(FILE, "$filetoopen");
	flock(FILE, 1) if ($OS_USED eq "Unix");
	my @cate = <FILE>;
	close(FILE);
	&winunlock($filetoopen) if ($OS_USED eq "Nt");
	foreach (@cate)
	{
	    chop($_);
	    ($cate_id,$cate_state,$cate_name,$cate_info) = split(/\t/,$_);
	    $temps .= qq~<option value="$cate_id">$cate_name</option>~;
	}

	$temps =~ s/value=\"$cateid\"/value=\"$cateid\" selected/;
	$tempoutput = "<input type=radio name=sort_status value=\"1\"> ���á�<input type=radio name=sort_status value=\"0\"> �ر�";
	$tempoutput =~ s/value=\"$sort_status\"/value=\"$sort_status\" checked/;

	$output .= qq~
	<table cellPadding=6 cellSpacing=1 width=100%>
	<form action="$thisprog" method="post">
	<input type=hidden name="action" value="edit_sort">
	<input type=hidden name="edit" value="y">
	<input type=hidden name="id" value="$id">
	<tr bgcolor=$miscbacktwo>
	<td colspan=2 align=center><font color=$fontcolormisc><b>[ �� �� �� �� ]</b></font></td>
	</tr>
	<tr bgcolor=$miscbackone>
	<td>��������</td><td><select name=catename size=1">$temps</select></td>
	</tr>
	<tr bgcolor=$miscbacktwo>
	<td>�������</td><td><input type=text size=15 name="sort_name" maxlength=15 value="$sort_name"></td>
	</tr>
	<tr bgcolor=$miscbackone>
	<td>���״̬</td><td>$tempoutput</td>
	</tr>
	<tr bgcolor=$miscbacktwo>
	<td>�������</td><td><input type=text size=40 name="sort_explain" value="$sort_info"></td>
	</tr>
	<tr bgcolor=$miscbackone><td align=center colspan=2><input type=submit value="�� ��"></td></tr></form>
	</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
    }
}

sub putjs
{
    my $id = $query -> param('id');
    my $filetoopen = "$lbdir" . "face/wpdata/$id.pl";	# �����
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @spdata = <FILE>;
    my $spdata = @spdata;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

    foreach (@spdata)
    {
	chop($_);
	($x1,$x2,$x3,$x,$x,$x5,$x6,$x7,$x,$x8) = split(/\t/,$_);
	($x6,$x) = split(/\./,$x6);
	($x7,$x) = split(/\./,$x7);
	$outinfo .= qq~'$x1|$x2|$x3|$x5|$x6|$x7',~;
	#��ƷID,��Ʒ����,��Ʒ�۸�,������Ⱥ,��Ʒ��ͼ,��ƷСͼ
    }
    chop($outinfo);

    open(FILE, ">${imagesdir}/face/js/$id.js");
    print FILE qq~//�װ�������̳�������� ��Ʒ��Ϣ ID:$id
var SPNUM = $spdata;
var SPINFO = new Array($outinfo);~;
    close(FILE);

    $output .= qq~
<table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>JavaScript �ļ�����ɹ���</b></font></td></tr>
</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog?action=sortm">~;
}

sub edit_cate
{
    my $id = $query -> param('id');
    my $edit = $query -> param('edit');
    if($edit eq 'y')
    {
	$new_name	= $query -> param('cate_name');
	$new_state	= $query -> param('cate_status');
	$new_explain	= $query -> param('cate_explain');
	&error("�༭����&�������ֲ��ܿգ���") if($new_name eq '');
	&error("�༭����&�����������ܿգ���") if($new_explain eq '');

	$/="";
	my $filetoopen = "$lbdir" . "face/category.pl";
	open(FILE,"$filetoopen");
	my $cate=<FILE>;
	close(FILE);
	$/="\n";

	$cate =~ s/$id\t(.*)/$id\t$new_state\t$new_name\t$new_explain/;
	open(FILE,">$filetoopen");
	print FILE $cate;
	close(FILE);

	$output .= qq~
<table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>�� �� �� �� �� ��</b></font></td></tr>
</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="1; url=$thisprog?action=sortm">~;
    }
    else
    {
	my $filetoopen = "$lbdir" . "face/category.pl";
	&winlock($filetoopen) if ($OS_USED eq "Nt");
	open(FILE,"$filetoopen");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	@cate = <FILE>;
	close(FILE);
	&winunlock($filetoopen) if ($OS_USED eq "Nt");
	foreach (@cate)
	{
	    chop($_);
	    ($cate_id,$cate_state,$cate_name,$cate_info) = split(/\t/,$_);
	    last if($cate_id eq $id);
	}
	&error("�༭����&�༭�����ID�����ڣ���") if ($cate_id ne $id);

	$tempoutput = "<input type=radio name=cate_status value=\"1\"> ���á�<input type=radio name=cate_status value=\"0\"> �ر�";
	$tempoutput =~ s/value=\"$cate_state\"/value=\"$cate_state\" checked/;

	$output .= qq~
	<table cellPadding=6 cellSpacing=1 width=100%>
	<form action="$thisprog" method="post">
	<input type=hidden name="action" value="edit_cate">
	<input type=hidden name="edit" value="y">
	<input type=hidden name="id" value="$id">
	<tr bgcolor=$miscbacktwo>
	<td colspan=2 align=center><font color=$fontcolormisc><b>[ �� �� �� �� ]</b></font></td>
	</tr>
	<tr bgcolor=$miscbackone>
	<td>��������</td><td><input type=text size=15 name="cate_name" maxlength=15 value="$cate_name"></td>
	</tr>
	<tr bgcolor=$miscbackone>
	<td>����״̬</td><td>$tempoutput</td>
	</tr>
	<tr bgcolor=$miscbacktwo>
	<td>��������</td><td><input type=text size=40 name="cate_explain" value="$cate_info"></td>
	</tr>
	<tr bgcolor=$miscbackone><td align=center colspan=2><input type=submit value="�� ��"></td></tr></form>
	</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
    }
}

sub del_cate
{
    my $id = $query -> param('id');

    $/="";
    my $filetoopen = "$lbdir" . "face/category.pl";
    open(FILE,"$filetoopen");
    my $cate=<FILE>;
    close(FILE);
    $/="\n";

    if($cate =~ s/$id\t(.*)\n//)	# �ҵ�ָ����ID
    {
	open(FILE,">$filetoopen");
	print FILE $cate;
	close(FILE);
    }

    $filetoopen = "$lbdir" . "face/class.cgi";
    open(FILE,"$filetoopen");
    my @sort = <FILE>;
    close(FILE);

    open(FILE,">$filetoopen");
    foreach(@sort)
    {
	($cateid,$sort_id,$sort_status,$sort_name,$sort_info)=split(/\t/,$_);
	if($cateid ne $id)
	{
		print FILE $_;
	}
	else
	{
		print FILE "\t$sort_id\t0\t$sort_name\t$sort_info";
	}
    }
    close(FILE);

    $output .= qq~
<table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>ɾ �� �� �� �� ��</b></font></td></tr>
</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="1; url=$thisprog?action=sortm">~;
}

sub add_cate
{
    my $add		= $query -> param('add');

    if($add ne 'y')
    {
	$output .= qq~
	<table cellPadding=6 cellSpacing=1 width=100%>
	<form action="$thisprog" method="post">
	<input type=hidden name="action" value="add_cate">
	<input type=hidden name="add" value="y">
	<tr bgcolor=$miscbacktwo>
	<td colspan=2 align=center><font color=$fontcolormisc><b>[ �� �� �� �� �� ]</b></font></td>
	</tr>
	<tr bgcolor=$miscbackone>
	<td>��������</td><td><input type=text size=15 name="cate_name" maxlength=15></td>
	</tr>
	<tr bgcolor=$miscbacktwo>
	<td>��������</td><td><input type=text size=40 name="cate_explain"></td>
	</tr>
	<tr bgcolor=$miscbackone><td align=center colspan=2><input type=submit value="�� ��"></td></tr></form>
	</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
    }
    else
    {
	$cate_name	= $query -> param('cate_name');
	$cate_explain	= $query -> param('cate_explain');
	&error("���ӷ���&�������ֲ��ܿգ���") if($cate_name eq '');
	&error("���ӷ���&�����������ܿգ���") if($cate_explain eq '');

	my $filetoopen = "$lbdir" . "face/category.pl";
	if (( -e "$filetoopen"))
	{
	    open(FILE,"$filetoopen");
	    my @cate=<FILE>;
	    close(FILE);

	    foreach(@cate)
	    {
		($cate_num,$x,$old_name,$x)=split(/\t/,$_);
		&error("���������ظ�&�Ѿ�������ͬ�ķ������ƣ�") if($cate_name eq $old_name);
	    }
	}
	else
	{
	    $cate_num = 0;
	}
	$cate_num++;

	open(FILE,">>$filetoopen");
	print FILE "$cate_num\t0\t$cate_name\t$cate_explain\n";
	close(FILE);

	$output .= qq~
<table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>�� �� �� ��</b></font></td></tr>
</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT><meta http-equiv="refresh" content="1; url=$thisprog?action=sortm">~;
    }
}

sub upmenujs
{
    my $filetoopen = "$lbdir" . "face/category.pl";	# �����
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @cate = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

    $filetoopen = "$lbdir" . "face/class.cgi";		# С����
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @sort = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

    foreach (@cate)
    {
	chop($_);
	($cate_id,$cate_state,$cate_name,$cate_info) = split(/\t/,$_);
if($cate_state eq '1')
{
	my $menucon = "";
	foreach (@sort)
	{
            chomp($_);
	    ($cateid,$sort_id,$sort_status,$sortname,$sortinfo) = split(/\t/,$_);
	    if($sort_status eq '1')
	    {
		$menucon .= qq~<tr onMouseOut=\\"mOutNav(this, '')\\" onMouseOver=\\"mOverNav(this, '1')\\" bgcolor='$miscbackone'><td> <span onClick=DispSubMenu('$sort_id'); onMouseOver=DispSubMenu1('$sort_id'); style=cursor:hand; title='$sortinfo'>$sortname</span></td></tr>~ if($cate_id eq $cateid);
	    }
	}

	$outjs .= qq~//$cate_name\nvar MENU$cate_id = "$menucon"\n\n~;	# �����˵�ѡ��
	$smenun .= qq~<td><span style='width=80;cursor: hand;' onMouseOver='ShowMenu(MENU$cate_id,80)' title='$cate_info'>$cate_name</span></td>~;	# �Ӳ˵���
}
    }

    open(FILE, ">${imagesdir}/face/js/catemenu.js");
    print FILE qq~//3FACE ��Ʒ���������˵�����
 var h;
 var w;
 var l;
 var t;
 var topMar = 1;
 var leftMar = 0;
 var space = 1;
 var isvisible;

function mOverNav(navTD, caption)
{
	if (!navTD.contains(event.fromElement))
	{navTD.style.backgroundColor='$miscbacktwo';}
}
function mOutNav(navTD, caption)
{
	if (!navTD.contains(event.toElement))
	{navTD.style.backgroundColor='$miscbackone';}
}

function _HideMenu() 
{
 var mX;
 var mY;
 var vDiv;
 var mDiv;
 if (isvisible == true)
 {
	vDiv = document.all("_menuDiv");
	mX = window.event.clientX + document.body.scrollLeft;
	mY = window.event.clientY + document.body.scrollTop;
	if ((mX < parseInt(vDiv.style.left)) || (mX > parseInt(vDiv.style.left)+vDiv.offsetWidth) || (mY < parseInt(vDiv.style.top)-h) || (mY > parseInt(vDiv.style.top)+vDiv.offsetHeight)){
		vDiv.style.visibility = "hidden";
		_Search.style.visibility = "visible";
		isvisible = false;
	}
 }
}

function ShowMenu(vMnuCode,tWidth) {
	vSrc = window.event.srcElement;
	vMnuCode = "<table id='submenu' cellspacing=1 cellpadding=3 style='width:"+tWidth+"' bgcolor=$tablebordercolor border=0 onmouseout='_HideMenu()'>" + vMnuCode + "</table>";

	h = vSrc.offsetHeight;
	w = vSrc.offsetWidth;
	l = vSrc.offsetLeft + leftMar;
	t = vSrc.offsetTop + topMar + h + space;
	vParent = vSrc.offsetParent;
	while (vParent.tagName.toUpperCase() != "BODY")
	{
		l += vParent.offsetLeft;
		t += vParent.offsetTop;
		vParent = vParent.offsetParent;
	}
	_Search.style.visibility = "hidden";
	_menuDiv.innerHTML = vMnuCode;
	_menuDiv.style.top = t;
	_menuDiv.style.left = l;
	_menuDiv.style.visibility = "visible";
	isvisible = true;
}

$outjs

function displayMenu()
{
    s = "<table cellspacing=0 cellpadding=0 border=0><tr align=center>$smenun</tr></table>";
    document.write(s);
}
~;
close(FILE);
    $output .= qq~
<table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>����˵� JavaScript �ļ����³ɹ���</b></font></td></tr>
</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog?action=sortm">~;
}


sub add_sp
{
    my $add		= $query -> param('add');
    if($add ne 'y')
    {
	$filetoopen = "$lbdir" . "face/class.cgi";	# ��Ʒ���
	open(FILE,"$filetoopen");
	my @sort=<FILE>;
	close(FILE);
	my $id = $query -> param('id');
	foreach (@sort) 
	{
	    ($cateid,$sort_id,$x,$sort_name,$x)=split(/\t/,$_);
	    $temps = qq~$temps<option value="$sort_id">$sort_name</option>~ if($sort_id =~ /^[0-9]/);
	    $temps =~ s/value=\"$id\"/value=\"$id\" selected/;
	}

	if($id ne '')
        {
	     &error("����ֻ�����ӵ�һ����Ʒ&��һ��Ʒ����װ��Ʒ�������ǲ�һ���ģ�") if($id eq 't');
	     opendir (DIR, "${imagesdir}face/$id");
	     @thd = readdir(DIR);
	     closedir (DIR);
             $myimages="";
             $topiccount = @thd;
             @thd=sort @thd;
             for (my $i=0;$i<$topiccount;$i++){
		next if (($thd[$i] eq ".")||($thd[$i] eq ".."));
		$myimages.=qq~<option value="$thd[$i]">$thd[$i]~;
	     }
             $myimages =~ s/value=\"$action\"/value=\"$action\" selected/;
	}

	$output .= qq~
	<table cellPadding=6 cellSpacing=1 width=100%>
	<form action="$thisprog" method="post" name=FORM>
	<input type=hidden name="action" value="add_sp">
	<input type=hidden name="add" value="y">
	<tr bgcolor=$miscbacktwo>
	<td colspan=4 align=center><font color=$fontcolormisc><b>[ �� �� �� һ �� Ʒ ]</b></font></td>
	</tr>
	<tr bgcolor=$miscbackone>
	<td>��Ʒ����</td><td><SCRIPT language=javascript>
function select_class(){
window.open("$thisprog?action=add_sp&id="+document.FORM.file_name.options[document.FORM.file_name.selectedIndex].value,"_self");
}
function select(){
document.FORM.m_graphic.value=FORM.image.value;
document.bbsimg.src = "$imagesurl/face/$id/"+FORM.image.value;}
function select1(){
document.FORM.sx_graphic.value=FORM.sximage.value;
document.sxdemo.src = "$imagesurl/face/$id/"+FORM.sximage.value;}
</SCRIPT>
  <select name=file_name size=1" onchange=select_class()>
  <option value=blank>== ѡ����� ==</option>
  $temps
  </select></td><td rowspan="5" height=226 width=240><IMG border=1 name=bbsimg src="$imagesurl/face/blank.gif" align="absmiddle"> <IMG name=sxdemo src="$imagesurl/face/blank.gif" border=1 width=84 hegiht=84></td>
	</tr>
	<tr bgcolor=$miscbacktwo>
	<td>��Ʒ����</td><td><input type=text size=20 name="m_name" maxlength=20></td>
	</tr>
	<tr bgcolor=$miscbackone>
	<td>��Ʒ�۸�</td><td><input type=text size=10 name="m_money"> $moneyname</td>
	</tr>
	<tr bgcolor=$miscbacktwo>
	<td>��Ʒ����</td><td><input type=text size=40 name="m_description"></td>
	</tr>
	<tr bgcolor=$miscbacktwo>
	<td>�ʺ���Ⱥ</td><td><input type="radio" name="fit_herd" value="m">�� <input type="radio" name="fit_herd" value="f">Ů <input type="radio" name="fit_herd" value="t"> ͨ��</td>
	</tr>
	<tr bgcolor=$miscbackone>
	<td>��ƷͼƬ��ַ</td><td><input type=text size=40 name="m_graphic"></td><td><select name="image" onChange=select()><option value="blank.gif">ѡ��ͼƬ$myimages</select></td>
	</tr>
	<tr bgcolor=$miscbacktwo>
	<td>��Ʒ��СͼƬ��ַ</td><td><input type=text size=40 name="sx_graphic"></td><td><select name="sximage" onChange=select1()><option value="blank.gif">ѡ��ͼƬ$myimages</select></td>
	</tr>

	<tr bgcolor=$miscbackone><td align=center colspan=3><input type=submit value="�� ��"></td></tr></form>
	</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;

#	<tr bgcolor=$miscbackone>
#	<td>��Ʒ�;ö�</td><td><input type=text size=5 name="m_wear"> ��</td>
#	</tr>
    }
    else
    {
	$sp_name	= $query -> param('m_name');
	$file_name	= $query -> param('file_name');
	$sp_money	= $query -> param('m_money');
	$sp_description	= $query -> param('m_description');
	$sp_wear	= $query -> param('m_wear');
	$sp_fitherd	= $query -> param('fit_herd');
	$sp_graphic	= $query -> param('m_graphic');
	$sp_sxgraphic	= $query -> param('sx_graphic');

	&error("���ӵ�һ��Ʒ&��Ʒ���ֲ��ܿգ���") if ($sp_name eq "");
	&error("���ӵ�һ��Ʒ&��ѡ����Ʒ����𣡣�") if ($file_name eq "blank");
	&error("���ӵ�һ��Ʒ&��Ʒ�۸��ܿգ���") if ($sp_money eq "");
	&error("���ӵ�һ��Ʒ&��Ʒ�������ܿգ���") if ($sp_description eq "");
#	&error("���ӵ�һ��Ʒ&��Ʒ�;öȲ��ܿգ���") if ($sp_wear eq "");
	&error("���ӵ�һ��Ʒ&��ƷͼƬ���ܿգ���") if ($sp_graphic eq "");
	&error("���ӵ�һ��Ʒ&��Ʒ��СͼƬ���ܿգ���") if ($sp_sxgraphic eq "");
	&error("���ӵ�һ��Ʒ&��ѡ����Ʒ���ʺ���Ⱥ����") if ($sp_fitherd eq "");

	$currenttime = time();

	my $filetoopen = "$lbdir" . "face/wpdata/$file_name.pl";
	open(FILE, ">>$filetoopen");
	print FILE "$currenttime\t$sp_name\t$sp_money\t$sp_description\t$sp_wear\t$sp_fitherd\t$sp_graphic\t$sp_sxgraphic\t\t\n";
	close(FILE);
	$output .= qq~
<table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>�� Ʒ �� �� �� ����</b></font></td></tr>
</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog?action=add_sp">~;
    }
}

sub view_user
{
    my $id = $query -> param('id');

    my $filetoopen = "$lbdir" . "face/totaluser.cgi";
    open(FILE,"$filetoopen");
    my $totaluser=<FILE>;
    close(FILE);
    my @membernum = split(/\t/,$totaluser);
    $membernum = @membernum;
    foreach (@membernum)
    {
	$userinfo = qq~$userinfo<option value="$_">$_</option>~;
	$userinfo =~ s/value=\"$id\"/value=\"$_\" selected/;
    }
    if($id ne "")
    {
	&readface("$id",1);
	$loadface = "û����" if($loadface eq "");
	$loadface = "����������Ϊ��̳ͷ��" if($loadface eq "y");
	$loadface = "��̳��ͨ����(�鿴��������ʱ����ʾ)" if($loadface eq "n");
    }

    $output .=qq~<SCRIPT language=javascript>
function select_user(){
window.open("$thisprog?action=view&id="+document.FORM.file_name.options[document.FORM.file_name.selectedIndex].value,"_self");
}</SCRIPT>
<table cellPadding=6 cellSpacing=1 width=100%>
<form action="$thisprog" method="post" name=FORM>
<tr bgcolor=$miscbacktwo>
<td colspan=3 align=center><font color=$fontcolormisc><b>[ �� �� �� �� �� Ϣ - �ܹ��У�$membernum �� ]</b></font></td>
</tr>
<tr bgcolor=$miscbackone>
<td rowspan="8" width=150><DIV id="SHOW" style='padding:0;position:relative;top:0;left:0;width:140;height:226'></div></td>
<td width=550></td>
<td rowspan="8" width=150><select name=file_name size=16 onchange=select_user()>$userinfo</select></td></tr>~;

if($id ne '')
{
    for($i=1;$i<26;$i++)
    {
	@tempsp=split(/\_/,@buy_sp[$i]);
	next if(@tempsp eq "");
	for($j=0;$j<@tempsp;$j++)
	{
	    ($info1,$info2)=split(/\,/,@tempsp[$j]);

	    $/="";
	    my $filetoopen = "$lbdir" . "face/wpdata/$i.pl";
	    open(FILE,"$filetoopen");
	    my $sort=<FILE>;
	    close(FILE);
	    $/="\n";

	    if($sort !~ /$info1\t(.*)/)	# �Ҳ���ָ������ƷID
	    {
		$ladesign = $info2 eq 'Y' ? 1 : 0 ;
		$outinfo .=qq~'$info1|$info2||||$i|$j',~;
		$outinfo1 .=qq~'$ladesign',~;
		$outinfo2 .=qq~'$i',~;	
	    }
	    else
 	    {
	        my ($sp_name,$sp_money,$x,$sp_wear,$sp_fitherd,$sp_graphic,$sp_sxgraphic,$sp_suit,$sp_suitid)=split(/\t/,$1);
		$ladesign = $info2 eq 'Y' ? 1 : 0 ;
		$outinfo .=qq~'$sp_name|$info2|$sp_fitherd|$sp_graphic|$sp_sxgraphic|$sp_suitid|$j',~;
		$outinfo1 .=qq~'$ladesign',~;
		$outinfo2 .=qq~'$i',~;
		$outmoney += $sp_money;
	    }
	}
    }

    chop($outinfo);
    chop($outinfo1);
    chop($outinfo2);
$outmoney = 0 if ($outmoney eq "");
$output .=qq~
<SCRIPT LANGUAGE="JavaScript">
// 3FACE JS
var currface = "$currequip";
var showArray = currface.split('-');


var s="";
for (var i=0; i<=25; i++)
{
   if(showArray[i] != '0')
   {
	s+="<IMG src=$imagesurl/face/"+i+"/"+showArray[i]+".gif style='padding:0;position:absolute;top:0;left:0;width:140;height:226;z-index:"+i+";'>";
   }
}
s+="<IMG src=$imagesurl/face/blank.gif style='padding:0;position:absolute;top:0;left:0;width:140;height:226;z-index:50;'>";
SHOW.innerHTML=s;
</script>
  <tr bgcolor=$miscbackone> 
    <td>��ǰ�û�����$id</td>
  </tr>
  <tr bgcolor=$miscbackone> 
    <td>��������ʹ�÷�ʽ��$loadface</td>
  </tr>
  <tr bgcolor=$miscbackone> 
    <td></td>
  </tr>
  <tr bgcolor=$miscbackone> 
    <td></td>
  </tr>
  <tr bgcolor=$miscbackone> 
    <td>��ǰװ���ܽ�$outmoney $moneyname</td>
  </tr>
  <tr bgcolor=$miscbackone> 
    <td></td>
  </tr>
  <tr bgcolor=$miscbackone> 
    <td></td>
  </tr>

<script>
var AllArray = new Array($outinfo);
var LadeSign = new Array($outinfo1);
var SortArray = new Array($outinfo2);

function DispInfo(Sign)
{
    var Info = "<table border=0 cellPadding=3 cellSpacing=0 width=84 bgcolor=$tablebordercolor align=left>";
    var jj=0;

    for(i=0;i<AllArray.length;i++)
    {
	if(Sign == LadeSign[i])
	{
	    var UTemp = AllArray[i].split('|');	// �ֽ���Ʒ��Ϣ

	    if(UTemp[2] == 'f')
		SPSEX = 'Ů'
	    else if(UTemp[2] == 'm')
	        SPSEX = '��'
	    else
	        SPSEX = 'ͨ��'

	    if(jj == 0)
	        Info += "<tr>";
	    Info += "<td width=84 bgColor=$miscbackone>";

	    if(UTemp[2] == '')
		Info += "<img src=$imagesurl/face/images/abate.gif width=84 height=84 border=0' alt='��Ч��Ʒ\\n��Ʒ���"+UTemp[5]+"\\n��ƷID�ţ�"+UTemp[0]+"'></td>";
	    else
		Info += "<img src=$imagesurl/face/"+SortArray[i]+"/"+UTemp[4]+" width=84 height=84 border=0 alt='��Ʒ���ƣ�"+UTemp[0]+"\\n�����Ա�"+SPSEX+"'></td>";

	    if(jj == 7)
	        Info += "</tr>";
	    if(jj < 7)
	        jj++;
	    else
	        jj = 0;
	}
    }
    k = 8 - jj;
    Info += "<td colspan="+k+" bgColor=$miscbackone></td></tr></table>";
    if(Sign == 1)
	LoadArea.innerHTML = Info;
    else
	ULoadArea.innerHTML = Info;
}
</script>

<tr><td colspan=3 bgcolor=$miscbacktwo height=20><font color=$titlefont size=2><B>��ǰ�����Ʒ</B></font></td></tr>
<tr><td colspan=3 bgcolor=$miscbackone>
<div id=LoadArea><script>DispInfo(1);</script></div>
</td></tr>
<tr><td colspan=3 bgcolor=$miscbacktwo height=20><font color=$titlefont size=2><B>δ�����Ʒ</B></font></td></tr>
<tr><td colspan=3 bgcolor=$miscbackone>
<div id=ULoadArea><script>DispInfo(0);</script></div>
<div id=Area></div>
</td></tr>~;
}

    $output .=qq~</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
}

sub edit_sp
{
    my $filetoopen = "$lbdir" . "face/class.cgi";	# ��Ʒ���
    open(FILE,"$filetoopen");
    my @sort=<FILE>;
    close(FILE);
    my $id = $query -> param('id');

    foreach (@sort) 
    {
	($cateid,$sort_id,$sort_status,$sort_name,$sort_info)=split(/\t/,$_);
	$mainid .= qq~<option value="$sort_id">$sort_name</option>~;
	$mainid =~ s/value=\"$id\"/value=\"$id\" selected/;
    }

	$output .= qq~
<SCRIPT language=javascript>
function select_sort(){
window.open("$thisprog?action=edit&id="+document.FORM.sort.options[document.FORM.sort.selectedIndex].value,"_self");
}
</SCRIPT>
<table cellPadding=6 cellSpacing=1 width=100%>
<form action=$thisprog method=POST name=FORM>
<tr bgcolor=$miscbacktwo>
<td align=center><font color=$fontcolormisc><b>[ �� Ʒ �� �� ]</b></font></td>
</tr>
<tr bgcolor=#EEEEEE><td height=30>ѡ����Ʒ���<select name=sort size=1" onchange=select_sort()><option value=''>== ѡ����� ==</option>$mainid</select></td></tr></form>~;

if($id ne '')
{
	$filetoopen = "$lbdir" . "face/wpdata/$id.pl";
	$filetoopen = &stripMETA($filetoopen);
	open(FILE,"$filetoopen");
	my @sort=<FILE>;
	close(FILE);
	$sort = @sort;
	if ($sort eq '0')
	{
		$output .= qq~
<tr><td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>���������κ���Ʒ��</b></font></td></tr>
</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
		return;
	}
	$numid = $id;
	$output .=qq~
<script language="JavaScript" type="text/javascript">
function editface(forumid,countid,action){
var Win=window.open("editface.cgi?action="+action+"&num="+forumid+"&id="+countid,"FACE",'width=500,height=280,resizable=0,scrollbars=0,menubar=0,status=1');
}
function check(){if(!confirm("������ȥ�Ĳ��������ɻָ����Ƿ�ȷ��ɾ����"))return false;}
</script>
<tr bgcolor=$miscbackone><td>
<TABLE border=0 cellPadding=0 cellSpacing=1 width=100% align=center>~;


    my $page = $query -> param('page');
    $page = 1 if ($page eq "");
    my $allnum = @sort;
    my $temp = $allnum / 9;
    my $allpages = int($temp);
    $allpages++ if ($allpages != $temp);
    $page = 1 if ($page < 1);
    $page = $allpages if ($page > $allpages);
    my $showpage = "";
    if (!$allpages)
    {$showpage .= "��ǰû�м�¼";}
    elsif ($allpages == 1)
    {$showpage .= "��ǰ��¼ֻ�� <B>1</B> ҳ";}
    else
    {
	$showpage = "�ܹ� <b>$allpages</b> ҳ��<b>$sort</b> ����Ʒ��[";
	$i = $page - 3;
	$showpage .= qq~ <a href=$thisprog?action=edit&id=$id$searpage&page=$i title='�� $i ҳ'>��</a>~ if ($i > 0);
	$i++;
	$showpage .= qq~ <a href=$thisprog?action=edit&id=$id$searpage&page=$i>$i</a>~ if ($i > 0);
	$i++;
	$showpage .= qq~ <a href=$thisprog?action=edit&id=$id$searpage&page=$i>$i</a>~ if ($i > 0);
	$i++;
	$showpage .= qq~ <font color=#990000><B>$i</B></font>~;
	$i++;
	$showpage .= qq~ <a href=$thisprog?action=edit&id=$id$searpage&page=$i>$i</a>~ unless ($i > $allpages);
	$i++;
	$showpage .= qq~ <a href=$thisprog?action=edit&id=$id$searpage&page=$i>$i</a>~ unless ($i > $allpages);
	$i++;
	$showpage .= qq~ <a href=$thisprog?action=edit&id=$id$searpage&page=$i title='�� $i ҳ'>��</a>~ unless ($i > $allpages);
	$showpage .= " ]";
    }

    for ($i = $allnum - $page * 9  + 9 - 1; $i >= $allnum - $page * 9 && $i >= 0; $i--)
    { 
	($sp_id,$sp_name,$sp_money,$x,$sp_wear,$sp_fitherd,$sp_graphic,$sp_sxgraphic,$sp_suit,$sp_suitid)=split(/\t/,@sort[$i]);

	if($sp_suit eq 'Y')
	{
	    chop($sp_suitid);
	    @taoinfo=split(/\_/,$sp_suitid);
	    $numid = @taoinfo[0];
	}
	$sp_fitherd = '��' if($sp_fitherd eq 'm');
	$sp_fitherd = 'Ů' if($sp_fitherd eq 'f');
	$sp_fitherd = '��Ů' if($sp_fitherd eq 't');

	$output .=qq~<tr>~ if ($ii==0);

	$output .=qq~
<td width=33%>
<table border=0 cellPadding=0 cellSpacing=2 width=100%><TBODY>
<TR><TD bgColor=#eeeeee height=84 rowSpan=5 width=84><img src=$imagesurl/face/$numid/$sp_sxgraphic width=84 hegiht=84></TD>
<TD bgColor=#eeeeee height=20>$sp_name</TD></TR>
<TR><TD bgColor=#eeeeee height=20>�����ۣ�$sp_money.00</TD></TR>
<TR><TD bgColor=#eeeeee height=20>�ʡ��ã�$sp_fitherd</TD></TR>
<TR><TD bgColor=#eeeeee height=20 align=center><a href="javascript:editface('$id','$sp_id','edit_sp')">[�޸�]</a>����<a href="javascript:editface('$id','$sp_id','del_sp')" onclick="return check();">[ɾ��]</a></TD></TR>
</TBODY></TABLE>
</TD><TD width=10>&nbsp;</TD>~;

#<TR><TD bgColor=#eeeeee height=20>�;öȣ�$sp_wear</TD></TR>

	$output .=qq~</tr>~ if ($ii==2);
	if ($ii<2)
	{$ii++;} else {$ii=0;}
    }
$output .=qq~</table></td></tr>
<form action=$thisprog method=POST name="Jump">
<input type=hidden name="action" value="edit">
<input type=hidden name="id" value="$id">
<input type=hidden name=page value="">
<script>
function Page_Jump()
{
     document.Jump.page.value = document.Jump.N_Page.value;
}
</script>
<tr bgcolor=$miscbacktwo><td align=center><font color=$menufontcolor>$showpage</font> ���� <input type="text" name="N_Page" size="3" maxlength="3">  <input type="submit" name="Submit" value="ȷ��" onClick="return Page_Jump();"></td></tr></form>~;
}
    $output .=qq~</table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
}

&output("$plugname - ��̨����",\$output);
