#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

    $helpurl = &helpfiles("��������");
    $helpurl = qq~$helpurl<img src="$imagesurl/images/$skin/help_b.gif" border=0></a>~;

    $output =~ s/\ �û�����/\ ������̳����/g;
    $output .= qq~<p>
<tr><td bgcolor=$titlecolor $catbackpic valign=middle colspan=2 align=center>
<form action=$thisprog method=post>
<input type=hidden name=action value=sendpassword>
<font color=$fontcolormisc><b>�����������û��������ǿ��Խ�������̳����ȡ�÷�ʽͨ���ʼ���������</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</td>
<td bgcolor=$miscbackone><input type=text name=membername>�� $helpurl<BR><font color=$fonthighlight>�в������䣨���� Hotmail�������̳�����ŷ��������ʼ��У���ע���飡</font></td></tr>
<tr><td bgcolor=$miscbacktwo valign=middle colspan=2 align=center> 
<font color=$fontcolormisc><b>����û����д��ȷ��E-Mail����������̳������ʾ����ʹ�ȡ����̳�����ȡ��ʽ��</b></font></td></tr> 
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������̳������ʾ����</td> 
<td bgcolor=$miscbackone><input type=text size=20 name=getpassq></td></tr> 
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������̳������ʾ��</td> 
<td bgcolor=$miscbackone><input type=text size=20 name=getpassa></td></tr> 
<td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name=submit value="�� ��">
</td></form></tr></table></td></tr></table>
~;
1;
