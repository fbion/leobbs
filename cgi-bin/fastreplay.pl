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
if ($emoticons eq "on") { $emoticonslink = qq~<input CHECKED name=inshowemoticons type=checkbox value=yes>ʹ�ñ����ַ�ת����~; }
if ($emailfunctions eq "on") {
    if ($innotify eq "yes") { $requestnotify = qq~<input name=notify type=checkbox value=yes checked>�лظ�ʱʹ���ʼ�֪ͨ����<br>~; }
	               else { $requestnotify = qq~<input name=notify type=checkbox value=yes>�лظ�ʱʹ���ʼ�֪ͨ����<br>~;}
}
if ($canchgfont ne "no") {
    $fontpost = qq~<input type=checkbox name="inshowchgfont" value="yes">ʹ������ת����<br>~;
} else {
    undef $fontpost;
}
if ($idmbcodestate eq "on") {
    $idmbcodestates = qq~<input type=checkbox name="uselbcode" value="yes" checked>ʹ�� LeoBBS ��ǩ��<BR>~;
} else {
    $idmbcodestates = "";
}

$maxpoststr = "[������������ <B>$maxpoststr</B> ���ַ�]" if ($maxpoststr ne "");
$output .= qq~<form action=post.cgi method=post name="FORM" enctype="multipart/form-data">
<input type=hidden name=action value=addreply>
<input type=hidden name=forum value=$inforum>
<input type=hidden name=topic value=$intopic>
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=5 cellSpacing=1 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td bgcolor=$titlecolor width=220 $catbackpic><font color=$fontcolormisc><b>���ٻظ�����:</b></font></td><td bgcolor=$titlecolor width=500 $catbackpic> <font color=$fontcolormisc>$topictitletemp</font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=3><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>�����û���������:</b></font></td><td bgcolor=$miscbackone> <font color=$fontcolormisc><b>�û���</b>: <input type=text name=membername> <span onclick="javascript:location.href='register.cgi?forum=$inforum'" style=cursor:hand>û��ע�᣿</span>��<b>����:</b> <input type=password name=password> <a href=profile.cgi?action=lostpass style=cursor:help>�������룿</a></font></td></tr>
~;

if (($allowattachment ne "no")||($mymembercode eq "ad")||($mymembercode eq 'smo')||($myinmembmod eq "yes")) {
    $uploadreqire = "" if ($uploadreqire <= 0);
    $uploadreqire = "<BR>������Ҫ���� <B>$uploadreqire</B> ƪ(��֤�û�����)" if ($uploadreqire ne "");
	$output .= qq~<script language="javascript">function jsupfile(upname) {upname='[UploadFile$imgslt='+upname+']';if (document.FORM.inpost.createTextRange && document.FORM.inpost.caretPos) {var caretPos = document.FORM.inpost.caretPos;caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? upname + ' ' : upname;document.FORM.inpost.focus();} else {document.FORM.inpost.value+=upname;document.FORM.inpost.focus();}}</script>~;
        $output .= qq~<tr><td bgcolor=$miscbackone><b>�ϴ�������ͼƬ</b> (������� <B>$maxupload</B>KB)$uploadreqire</td><td bgcolor=$miscbackone colspan=2> <iframe id="upframe" name="upframe" src="upfile.cgi?action=uppic&forum=$inforum&topic=$intopic" width=100% height=40 marginwidth=0 marginheight=0 hspace=0 vspace=0 frameborder=0 scrolling=NO></iframe><br><font color=$fonthighlight>Ŀǰ����:(�粻��Ҫĳ��������ֻ��ɾ�������е���Ӧ [UploadFile$imgslt ...] ��ǩ����)  [<a href=upfile.cgi?action=delup&forum=$inforum target=upframe title=ɾ������δ�������ĸ�����ʱ�ļ� OnClick="return confirm('ȷ��ɾ������δ�������ĸ�����ʱ�ļ�ô��');">ɾ��</a>] </font></font><SPAN id=showupfile name=showupfile></SPAN></td></tr>~;
}
$output .= qq~
<tr><td bgcolor=$miscbacktwo valign=top><font color=$fontcolormisc><b>ѡ��</b>��~;

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
<br>$maxpoststr<BR>
$idmbcodestates
<input CHECKED name=inshowsignature type=checkbox value=yes>��ʾ����ǩ����<br>
$requestnotify$emoticonslink<BR>$fontpost</font></td>
<td bgcolor=$miscbacktwo width=*> <A name=sub></A><textarea cols=75 name=inpost onKeyDown=ctlent() rows=8 title='ʹ�� Ctrl+Enter ֱ���ύ����'></textarea><br>
 <INPUT name=Submit onclick="return clckcntr();" type=submit value="�� �� �� ��">��<input type=button value="Ԥ �� �� ��" name=Button onclick=gopreview()>��<INPUT name=Clear type=reset value="�� ��">�����������õ� <input name=floor value="" size="4" maxlength="4"> ¥��Ļظ�
</td></tr></table><SCRIPT>valignend()</SCRIPT></form>
<form name=preview action=preview.cgi method=post target=preview_page><input type=hidden name=body value=""><input type=hidden name=forum value="$inforum"></form>
<script>
function gopreview(){
document.preview.body.value=document.FORM.inpost.value;
var popupWin = window.open('', 'preview_page', 'scrollbars=yes,width=600,height=400');
document.preview.submit()
}
</script>
~;
1;
