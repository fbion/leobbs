#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

require "${lbdir}data/outputbutton.pl" if (-e "${lbdir}data/outputbutton.pl");
$outputbutton =~ s/\<\!\-\-h (.+?) \-\-\>/$1/isg if ($disphideboard eq "yes");
$outputbutton =~ s/\<\!\-\-c (.+?) \-\-\>/$1/isg if ($dispchildjump ne "no");

if ($query->cookie("selectstyle")) { $inselectstyle = $query->cookie("selectstyle"); }
$inselectstyle   = $skinselected if ($inselectstyle eq "");

$output .= qq~<tr><td bgcolor=$titlecolor colspan=3 $catbackpic><font color=$titlefontcolor><B>-=> ���ٵ�¼���</B>�� [ ���ԣ�$trueipaddress��$fromwhere1 ��ϵͳ��$osinfo��$browseinfo ]</td></tr>
<script>
function submitonce(theform){
if (document.all||document.getElementById){
for (i=0;i<theform.length;i++){
var tempobj=theform.elements[i]
if(tempobj.type.toLowerCase()=="submit"||tempobj.type.toLowerCase()=="reset")
tempobj.disabled=true
}}}
</script>
<FORM name=login method=post action=loginout.cgi onSubmit="submitonce(this)">
<tr><td bgcolor=$forumcolorone align=center width=26><img src=$imagesurl/images/userlist2.gif width=17></td>
<td bgcolor=$forumcolortwo colspan=1 width=*>
<input type=hidden name=action value=login>
<input type=hidden name=selectstyle value="$inselectstyle">
���û��� �� <input type=text name=inmembername size=12 maxlength=16 onmouseover=this.focus() onfocus=this.select()>�����ܡ��� �� <input type=password name=inpassword size=12 maxlength=20 onmouseover=this.focus() onfocus=this.select()>�� Cookie �� <select name=CookieDate><option selected value=0>������</option><option value=+1d>����һ��</option><option value=+30d>����һ��</option><option value=+20y>���ñ���</option></select><BR><BR>
����¼�� �� <select name=forum><option selected value=>��̳��ҳ</option>$outputbutton</select>������<input type=submit name=submit value="���ǡ� ¼��">���� <B><a href=register.cgi><U><font color=$fonthighlight>ע�����û�</font></u></a></B><BR><BR>
</td>~;

1;
