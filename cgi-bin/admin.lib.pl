#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

sub getadmincheck {
    my $currenttime = time;
    $memberfilename = $inmembername;
    $memberfilename =~ y/ /_/;
    $memberfilename =~ tr/A-Z/a-z/;
    $memberfilename = "${lbdir}verifynum/login/$memberfilename.cgi";

    if (-e $memberfilename) {
        open (FILE, "$memberfilename");
        my $logintime = <FILE>;
        close(FILE);
        chomp $logintime;
        if ($currenttime > $logintime + 900 ) { # ����Ա��¼���15����δ���κβ�������Ҫ���µ�¼
            unlink ("$memberfilename");
	    print "Set-Cookie: adminpass=\"\"\n";
	    $inpassword = "";
        } else {
	    open (FILE, ">$memberfilename");
	    print FILE "$currenttime\n";
	    close(FILE);
        }
        
    } else {
        print "Set-Cookie: adminpass=\"\"\n";
	$inpassword = "";
    }
}

sub adminlogin {
    $inmembername =~ s/\_/ /g;
    if ($useverify eq "yes") {

        if ($verifyusegd ne "no") {
	    eval ('use GD;');
	    if ($@) {
                $verifyusegd = "no";
            }
        }
        if ($verifyusegd eq "no") {
	    $houzhui = "bmp";
        } else {
	    $houzhui = "png";
        }
        
    	require 'verifynum.cgi';
    }
    $loginprog = $thisprog if ($loginprog eq "");
    print qq~
<tr><td bgcolor="#2159C9" colspan=2><font color=#FFFFFF>
<b>��ӭ���� LeoBBS ��̳��������</b>
</td></tr>
<form action=admin.cgi method=post>
<input type=hidden name=action value=login>
<input type=hidden name=loginprog value=$loginprog>
<tr><td bgcolor=#EEEEEE valign=middle colspan=2 align=center><font color=#333333><b>�����������û����������¼</b></font></td></tr>
<tr><td bgcolor=#FFFFFF valign=middle width=40% align=right><BR><font color=#555555>�����������û���</font></td>
<td bgcolor=#FFFFFF valign=middle><BR><input type=text name=membername value="$inmembername" maxlength=15></td></tr>
<tr><td bgcolor=#FFFFFF valign=middle width=40% align=right><font color=#555555>��������������</font></td>
<td bgcolor=#FFFFFF valign=middle><input type=password name=password maxlength=20></td></tr>
~;
print qq~<tr><td bgcolor=#FFFFFF valign=middle width=40% align=right><font color=#555555>�������ұ�ͼƬ������</font></td><td bgcolor=#FFFFFF valign=middle><input type=hidden name=sessionid value="$sessionid"><input type=text name="verifynum" size=4 maxlength=4>����<img src=$imagesurl/verifynum/$sessionid.$houzhui border=0 align=absmiddle> ��������壬��ˢ�±�ҳ</td></tr>~ if ($useverify eq "yes");
print qq~<tr><td bgcolor=#FFFFFF valign=middle colspan=2 align=center><BR><input type=submit name=submit value="�� ¼"></form></td></tr>
<tr><td bgcolor=#FFFFFF valign=middle align=left colspan=2><font color=#555555>
<blockquote><b>��ע��:</b><p><b>ֻ����̳��̳�����ܵ�¼��̳�������ġ�δ������Ȩ�ĳ��Ե�¼��Ϊ���ᱻ��¼�ڰ���</b><p>�ڽ�����̳��������ǰ����ȷ�������������� Cookie ѡ�<br> Cookie ֻ������ڵ�ǰ������������С�Ϊ�˰�ȫ���������ر����������Cookie ��ʧЧ�����Զ�ɾ����</blockquote>
</td></tr></table></td></tr></table>
~;
}

sub admintitle {
    print qq~
<html>
<head>
<title>LeoBBS - ��̳��������</title>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<style>
BODY {BACKGROUND: #799ae1; FONT: 9pt ����;}
TABLE {BORDER-BOTTOM: 0px; BORDER-LEFT: 0px; BORDER-RIGHT: 0px; BORDER-TOP: 0px}
TD {FONT: 12px ����}
IMG {BORDER-BOTTOM: 0px; BORDER-LEFT: 0px; BORDER-RIGHT: 0px; BORDER-TOP: 0px;}
A {COLOR: #215dc6; FONT: 12px ����; TEXT-DECORATION: none}
A:hover {COLOR: #428eff}
.sec_menu {BACKGROUND: #d6dff7; BORDER-BOTTOM: white 1px solid; BORDER-LEFT: white 1px solid; BORDER-RIGHT: white 1px solid; OVERFLOW: hidden}
.menu_title {}
.menu_title SPAN {COLOR: #215dc6; FONT-WEIGHT: bold; LEFT: 8px; POSITION: relative; TOP: 2px}
.menu_title2 {}
.menu_title2 SPAN {COLOR: #428eff; FONT-WEIGHT: bold; LEFT: 8px; POSITION: relative; TOP: 2px}
</STYLE>
<script language="javascript"> 
function save_changes() { document.the_form.process.value="true"; } 
function preview_template() {document.the_form.target="_blank"; document.the_form.process.value="preview template";}
</script>

</head>
<body alink=#333333 vlink=#333333 link=#333333 topmargin=0 leftmargin=2>

<table width=97% cellpadding=0 cellspacing=0 bgcolor=#483D95 align=center valign=top>
<tr><td>
  <table width=100% cellpadding=0 cellspacing=0>
  <tr><td width=17% valign=top bgcolor=#799ae1>
    <table width=100% cellpadding=6 cellspacing=0>
	<tr><td bgcolor=#799ae1>
	<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <tr>
          <TD vAlign=top><IMG src="$imagesurl/images/title.gif" width=200 height=38><BR>
	  <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
              <TR><TD height=20 align=center><font color=#336333><b>ע���ܰ���ɲ����� (*) ����Ŀ</b></TD></TR>
	  </TABLE>
	</TD></TR>
 	</TABLE>
        </td></tr>

<tr><td bgcolor=#799ae1>
<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <TBODY>
        <tr>
          <TD background=$imagesurl/images/title_bg_show.gif class=menu_title height=25 onmouseout="this.className='menu_title';" onmouseover="this.className='menu_title2';">
          <SPAN>�� ������</SPAN> </TD></TR>
        <TR>
          <TD>
            <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
              <TR><TD height=18>&nbsp;>> <a href="admin.cgi">����������ҳ(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="leobbs.cgi">����������̳(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="indexshow.cgi">��ҳJavaScript������</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="admin.cgi?action=logout">�˳���������(*)</a></TD></TR>
	    </TABLE>
	    </TD></TR></TABLE>
</td></tr>

<tr><td bgcolor=#799ae1>
<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <TBODY>
        <tr>
          <TD background=$imagesurl/images/title_bg_show.gif class=menu_title height=25 onmouseout="this.className='menu_title';" onmouseover="this.className='menu_title2';">
          <SPAN>�� �û�����</SPAN> </TD></TR>
        <TR>
          <TD>
            <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
              <TR><TD height=18>&nbsp;>> <a href="setmembers.cgi">�û�����/����(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="usermanager.cgi">�û�����/����(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="cansale.cgi">���������û�����(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setmemberbak.cgi">�û��ⱸ��/��ԭ</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="resetusr.cgi">�û������������</a></TD></TR>
	    </TABLE>
	    </TD></TR></TABLE>
</td></tr>

<tr><td bgcolor=#799ae1>
<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <TBODY>
        <tr>
          <TD background=$imagesurl/images/title_bg_show.gif class=menu_title height=25 onmouseout="this.className='menu_title';" onmouseover="this.className='menu_title2';">
          <SPAN>�� ע�����</SPAN> </TD></TR>
        <TR>
          <TD>
            <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
              <TR><TD height=18>&nbsp;>> <a href="noreg.cgi">���������û���(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="noregemail.cgi">�������� Email(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setallowemail.cgi">����(����)��ע���������(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="noregip.cgi">��ֹ���� IP ע���û�(*)</a></TD></TR>
	    </TABLE>
	    </TD></TR></TABLE>
</td></tr>

<tr><td bgcolor=#799ae1>
<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <TBODY>
        <tr>
          <TD background=$imagesurl/images/title_bg_show.gif class=menu_title height=25 onmouseout="this.className='menu_title';" onmouseover="this.className='menu_title2';">
          <SPAN>�� ��̳����</SPAN> </TD></TR>
        <TR>
          <TD>
            <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
              <TR><TD height=18>&nbsp;>> <a href="setforums.cgi">��̳���ú͹���</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setcatedisplay.cgi">��̳����Ϣ����ģʽ</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="merge.cgi">�ϲ���̳</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="adbackup.cgi">��̳���ݵ�����/��ԭ</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="shareforums.cgi">������̳����</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="rebuildall.cgi">�ؽ�������̳</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="rebuildmain.cgi">���½�����̳������(*)</a></TD></TR>
	    </TABLE>
	    </TD></TR></TABLE>
</td></tr>

<tr><td bgcolor=#799ae1>
<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <TBODY>
        <tr>
          <TD background=$imagesurl/images/title_bg_show.gif class=menu_title height=25 onmouseout="this.className='menu_title';" onmouseover="this.className='menu_title2';">
          <SPAN>�� ���ù���</SPAN> </TD></TR>
        <TR>
          <TD>
            <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
              <TR><TD height=18>&nbsp;>> <a href="foruminit.cgi">��ʼ����̳����</a> <B>(ע)</B></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setstyles.cgi">Ĭ�Ϸ������</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setvariables.cgi">������������</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setmpic.cgi">��̳��ɫ&ͼƬ����</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setbank.cgi">������������</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setcity.cgi">������������</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setawards.cgi">����ѫ�¹���</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setmembertitles.cgi">�û��ȼ�����</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setjhmp.cgi">�������ɹ�����</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setemoticon.cgi">����ת�����ù���</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setemotes.cgi">EMOTE ����</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setad.cgi">���������������</a></TD></TR>
	    </TABLE>
	    </TD></TR></TABLE>
</td></tr>

<tr><td bgcolor=#799ae1>
<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <TBODY>
        <tr>
          <TD background=$imagesurl/images/title_bg_show.gif class=menu_title height=25 onmouseout="this.className='menu_title';" onmouseover="this.className='menu_title2';">
          <SPAN>�� ���ƹ���</SPAN> </TD></TR>
        <TR>
          <TD>
            <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
              <TR><TD height=18>&nbsp;>> <a href="setbadwords.cgi">�����Զ�ת��</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setfilter.cgi">�����������(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setipbans.cgi">IP ��ֹ(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setidbans.cgi">ID ��ֹ(*)</a></TD></TR>
	    </TABLE>
	    </TD></TR></TABLE>
</td></tr>

<tr><td bgcolor=#799ae1>
<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <TBODY>
        <tr>
          <TD background=$imagesurl/images/title_bg_show.gif class=menu_title height=25 onmouseout="this.className='menu_title';" onmouseover="this.className='menu_title2';">
          <SPAN>�� ���⹦��</SPAN> </TD></TR>
        <TR>
          <TD>
            <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
              <TR><TD height=18>&nbsp;>> <a href="exportemail.cgi">������Ա Email ��ַ</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="massmsg.cgi">����Ϣ�㲥</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="mailmembers.cgi">Email Ⱥ��</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="filemanage.cgi">��̳�ļ�����������</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setplugin.cgi">��̳����趨</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setskin.cgi">����������趨</a></TD></TR>
	    </TABLE>
	    </TD></TR></TABLE>
</td></tr>

<tr><td bgcolor=#799ae1>
<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <TBODY>
        <tr>
          <TD background=$imagesurl/images/title_bg_show.gif class=menu_title height=25 onmouseout="this.className='menu_title';" onmouseover="this.className='menu_title2';">
          <SPAN>�� ��̳�༭</SPAN> </TD></TR>
        <TR>
          <TD>
            <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
              <TR><TD height=18>&nbsp;>> <a href="setregrules.cgi">�޸�ע������</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setregmsg.cgi">�޸Ķ���Ϣ��ӭ��Ϣ</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="settemplate.cgi">�༭��̳ģ��</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="setcss.cgi">��̳ CSS ��������</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="newstyles.cgi">�½�/�޸ķ���ļ�</a></TD></TR>
	    </TABLE>
	    </TD></TR></TABLE>
</td></tr>

<tr><td bgcolor=#799ae1>
<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <TBODY>
        <tr>
          <TD background=$imagesurl/images/title_bg_show.gif class=menu_title height=25 onmouseout="this.className='menu_title';" onmouseover="this.className='menu_title2';">
          <SPAN>�� ��������</SPAN> </TD></TR>
        <TR>
          <TD>
            <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
              <TR><TD height=18>&nbsp;>> <a href="userratinglog.cgi">�û��������ֲ�����־(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="baddellogs.cgi">��̳��ȫ��־</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="adminloginlogs.cgi">��������ȫ��־</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="sizecount.cgi">ͳ����̳ռ�ÿռ�</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="vercheck.cgi">��̳�汾/����</a></TD></TR>
	    </TABLE>
	    </TD></TR></TABLE>
</td></tr>
    ~;
    
    if (-e "${lbdir}data/leoskin.cgi"){
	eval { require "${lbdir}data/leoskin.cgi"; };
	if ($@) {
	} else {
	    if ($skin1name ne ""){
	        print qq~
<tr><td bgcolor=#799ae1>
<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <TBODY>
        <tr>
          <TD background=$imagesurl/images/title_bg_show.gif class=menu_title height=25 onmouseout="this.className='menu_title';" onmouseover="this.className='menu_title2';">
          <SPAN>�� ��̳���</SPAN> </TD></TR>
        <TR>
          <TD>
            <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
	~;    
        print qq~<TR><TD height=18>&nbsp;>> <a href="$skin1url">$skin1name</a></TD></TR>~ if ($skin1name ne "");
        print qq~<TR><TD height=18>&nbsp;>> <a href="$skin2url">$skin2name</a></TD></TR>~ if ($skin2name ne "");
        print qq~<TR><TD height=18>&nbsp;>> <a href="$skin3url">$skin3name</a></TD></TR>~ if ($skin3name ne "");
        print qq~<TR><TD height=18>&nbsp;>> <a href="$skin4url">$skin4name</a></TD></TR>~ if ($skin4name ne "");
        print qq~<TR><TD height=18>&nbsp;>> <a href="$skin5url">$skin5name</a></TD></TR>~ if ($skin5name ne "");
        print qq~<TR><TD height=18>&nbsp;>> <a href="$skin6url">$skin6name</a></TD></TR>~ if ($skin6name ne "");
        print qq~<TR><TD height=18>&nbsp;>> <a href="$skin7url">$skin7name</a></TD></TR>~ if ($skin7name ne "");
        print qq~<TR><TD height=18>&nbsp;>> <a href="$skin8url">$skin8name</a></TD></TR>~ if ($skin8name ne "");
        print qq~<TR><TD height=18>&nbsp;>> <a href="$skin9url">$skin9name</a></TD></TR>~ if ($skin9name ne "");
        print qq~<TR><TD height=18>&nbsp;>> <a href="$skin10url">$skin10name</a></TD></TR>~ if ($skin10name ne "");
        print qq~</TABLE></TD></TR></TABLE></td></tr>~;
	    }
        }
    }

    print qq~
<tr><td bgcolor=#799ae1>
<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <tr>
          <TD background=$imagesurl/images/title_bg_show.gif class=menu_title height=25 onmouseout="this.className='menu_title';" onmouseover="this.className='menu_title2';">
          <SPAN>�� ������</SPAN> </TD></TR>
        <TR>
          <TD>
            <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
              <TR><TD height=18>&nbsp;>> <a href="admin.cgi">����������ҳ(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="leobbs.cgi">����������̳(*)</a></TD></TR>
              <TR><TD height=18>&nbsp;>> <a href="admin.cgi?action=logout">�˳���������(*)</a></TD></TR>
	    </TABLE>
	    </TD></TR></TABLE>
</td></tr>

<tr><td bgcolor=#799ae1>
<TABLE align=left cellPadding=0 cellSpacing=0 width=200>
        <tr>
          <TD background=$imagesurl/images/title_bg_show.gif class=menu_title height=25 onmouseout="this.className='menu_title';" onmouseover="this.className='menu_title2';">
          <SPAN>�� LeoBBS ��Ϣ</SPAN> </TD></TR>
        <TR>
          <TD>
            <TABLE align=center cellPadding=0 cellSpacing=0 width=200 class=sec_menu>
              <TR><TD height=18>&nbsp;����汾: $versionnumber</TD></TR>
              <TR><TD height=18>&nbsp;��Ȩ����: ɽӥ(��)������ȱ</TD></TR>
              <TR><TD height=18>&nbsp;����֧��: <a href="http://bbs.leobbs.com/" target=_blank>���ᳬ����̳</a></TD></TR>
	    </TABLE>
	    </TD></TR></TABLE>
</td></tr>

</table>
    </td><td width=70% valign=top bgcolor=#ffffff>
    <table width=100% cellpadding=5 cellspacing=0><tr><td bgcolor=#799ae1><img src=$imagesurl/images/none.gif width=0 height=6></td></tr></table><table width=100% cellpadding=6 cellspacing=0><tr><td bgcolor=#799ae1>
    ~;
}
1;  
