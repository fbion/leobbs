#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

$maxpoststr = "" if ($maxpoststr eq 0);
$maxpoststr = 100 if (($maxpoststr < 100)&&($maxpoststr ne ""));
    if ($startnewthreads eq "no")        { $startthreads = "�ڴ���̳���µ���������ӻظ�ֻ����̳������������"; }
    elsif ($startnewthreads eq "follow") { $startthreads = "�ڴ���̳���µ�����ֻ����̳��������������ͨ��Աֻ���Ը�����"; }
    elsif ($startnewthreads eq "all")    { $startthreads = "�κ��˾����Է���ͻظ����⣬δע���û��������������գ�"; }
    elsif ($startnewthreads eq "cert")   { $startthreads = "�ڴ���̳���µ�����ֻ����̳������������֤�Ļ�Ա����"; }
    else { $startthreads = "����ע���Ա�����Է���ͻظ����⣡"; }

    if ($emailfunctions eq "on") {
	if ($innotify eq "yes") { $requestnotify = " checked"; } else { $requestnotify = ""; }
	$requestnotify = qq~&nbsp;<input type=checkbox name="notify" value="yes"$requestnotify>�лظ�ʱʹ���ʼ�֪ͨ����<br>~;
    }
    if ($emoticons eq "on") {
       $emoticonslink = qq~<li><span style=cursor:hand onClick="javascript:openScript('$miscprog?action=showsmilies',300,350)">����<B>ʹ��</B>�����ַ�ת��</span>~;
       $emoticonsbutton =qq~&nbsp;<input type=checkbox name="inshowemoticons" value="yes" checked>���Ƿ�ϣ��<b>ʹ��</b>�����ַ�ת����<br>~;
    }
    $maxpoststr = "(������������ <B>$maxpoststr</B> ���ַ�)" if ($maxpoststr ne "");
if ($canchgfont ne "no") {
    $fontpost = qq~&nbsp;<input type=checkbox name="inshowchgfont" value="yes">ʹ������ת����<br>~;
} else {
    undef $fontpost;
}

if ($idmbcodestate eq "on") {
    $idmbcodestates = qq~&nbsp;<input type=checkbox name="uselbcode" value="yes" checked>ʹ�� LeoBBS ��ǩ��<BR>~;
} else {
    $idmbcodestates = "";
}

    $output .= qq~<script>
function HighlightAll(theField) {
var tempval=eval("document."+theField)
tempval.focus()
tempval.select()
therange=tempval.createTextRange()
therange.execCommand("Copy")}
function DoTitle(addTitle) { var revisedTitle;var currentTitle = document.FORM.intopictitle.value;revisedTitle = addTitle+currentTitle;document.FORM.intopictitle.value=revisedTitle;document.FORM.intopictitle.focus();return;}
</script><form action=post.cgi method=post name="FORM" enctype="multipart/form-data">
<input type=hidden name=action value=addnew>
<input type=hidden name=forum value="$inforum">
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor colspan=2 $catbackpic>&nbsp;<font color=$titlefontcolor><b>���ٷ���������</b></font> -- $startthreads</td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <B><u><font color=$fonthighlight>$inmembername</font></u></B> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbacktwo width=220>&nbsp;<font color=$fontcolormisc><b>�����û���������:</b></font></td><td bgcolor=$miscbacktwo>��<font color=$fontcolormisc><b>�û���</b>: <input type=text name=membername> <span onclick="javascript:location.href='register.cgi?forum=$inforum'" style=cursor:hand>û��ע�᣿</span>��<b>����:</b> <input type=password name=password> <a href=profile.cgi?action=lostpass style=cursor:help>�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbackone>&nbsp;<font color=$fontcolormisc><b>�������</b></font>��
<select name=font onchange=DoTitle(this.options[this.selectedIndex].value)>
<OPTION selected value="">ѡ����</OPTION> <OPTION value=[ԭ��]>[ԭ��]</OPTION><OPTION value=[ת��]>[ת��]</OPTION><OPTION value=[��ˮ]>[��ˮ]</OPTION><OPTION value=[����]>[����]</OPTION><OPTION value=[����]>[����]</OPTION><OPTION value=[�Ƽ�]>[�Ƽ�]</OPTION><OPTION value=[����]>[����]</OPTION><OPTION value=[ע��]>[ע��]</OPTION><OPTION value=[��ͼ]>[��ͼ]</OPTION><OPTION value=[����]>[����]</OPTION><OPTION value=[����]>[����]</OPTION><OPTION value=[����]>[����]</OPTION>
</SELECT></td>
<td bgcolor=$miscbackone>��<input type=text size=60 maxlength=80 name="intopictitle" value="$intopictitle">�����ó��� 40 ������</td></tr>
<td bgcolor=$miscbacktwo valign=top>&nbsp;<font color=$fontcolormisc><b>ѡ��</b>��~;

if ($magicface ne 'off') {
$output .= qq~
<style>
.gray	{cursor: hand; filter:gray}
</style>
<script>
function magicfaceopen() {javascript:openScript('misc.cgi?action=showmagicface',400,550);}
function enable(btn){btn.filters.gray.enabled=0;}
function disable(btn){btn.filters.gray.enabled=1;}
</script>

<IMG onclick=magicfaceopen() align=absmiddle height=22 alt=����ħ������ src=$imagesurl/btg/magicface.gif width=23  class="gray" onmouseover="enable(this)" onmouseout="disable(this)">
~;
}

$output .= qq~
<br>$maxpoststr<BR>$idmbcodestates
&nbsp;<input type=checkbox name="inshowsignature" value="yes" checked>��ʾǩ����<br>
$requestnotify$emoticonsbutton$fontpost</center>
<td bgcolor=$miscbacktwo>��<TEXTAREA cols=80 name=inpost rows=9 wrap="soft" onkeydown=ctlent()>$inpost</TEXTAREA><br></td></tr>~;

    if (($arrowupload ne "off")||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) {
    $uploadreqire = "" if ($uploadreqire <= 0);
    $uploadreqire = "<BR>������Ҫ���� <B>$uploadreqire</B> ƪ(��֤�û�����)" if ($uploadreqire ne "");
	$output .= qq~<script language="javascript">function jsupfile(upname) {upname='[UploadFile$imgslt='+upname+']';if (document.FORM.inpost.createTextRange && document.FORM.inpost.caretPos) {var caretPos = document.FORM.inpost.caretPos;caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? upname + ' ' : upname;document.FORM.inpost.focus();} else {document.FORM.inpost.value+=upname;document.FORM.inpost.focus();}}</script>~;
        $output .= qq~<tr><td bgcolor=$miscbackone><b>�ϴ�������ͼƬ</b> (������� <B>$maxupload</B>KB)$uploadreqire</td><td bgcolor=$miscbackone> <iframe id="upframe" name="upframe" src="upfile.cgi?action=uppic&forum=$inforum&topic=$intopic" width=100% height=40 marginwidth=0 marginheight=0 hspace=0 vspace=0 frameborder=0 scrolling=NO></iframe><br><font color=$fonthighlight>Ŀǰ����:(�粻��Ҫĳ��������ֻ��ɾ�������е���Ӧ [UploadFile$imgslt ...] ��ǩ����)  [<a href=upfile.cgi?action=delup&forum=$inforum target=upframe title=ɾ������δ�������ĸ�����ʱ�ļ� OnClick="return confirm('ȷ��ɾ������δ�������ĸ�����ʱ�ļ�ô��');">ɾ��</a>] </font><SPAN id=showupfile name=showupfile></SPAN></td></tr>~;
    }
    $output .= qq~<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=Submit value="�� �� �� �� ��" name=Submit onClick="return clckcntr();">����<input type=button value='Ԥ �� �� ��' name=Button onclick=gopreview()>����<input type="reset" name="Clear" value="�� ��"></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT></form>
<form name=preview action=preview.cgi method=post target=preview_page><input type=hidden name=body value=""><input type=hidden name=forum value="$inforum"></form>
<script>
function gopreview(){
document.preview.body.value=document.FORM.inpost.value;
var popupWin = window.open('', 'preview_page', 'scrollbars=yes,width=600,height=400');
document.preview.submit()
}
</script>~;
1;
