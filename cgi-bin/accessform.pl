#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

$output .= qq~
<form action=forums.cgi method=post>
<input type=hidden name=forum value=$inforum>
<input type=hidden name=action value=accessrequired>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td>
<table cellpadding=3 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center><font color=$fontcolormisc><b>�������������ơ������¼˽����̳</b></font></td></tr>
<tr><td bgcolor=$miscbackone colspan=2><font color=$fontcolormisc><br>ÿ�������ֻ��Ҫ��¼һ�Σ�ͬʱ��ȷ�����Ѿ������������ Cookies ѡ�<br>ֻ�о�������Ա��ɵ��û��ſ��Է��ʸ���̳������㲻�ܵ�¼������ϵ����Ա��<br><br></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> �����Ҫ�������û���ݽ��룬��<a href=loginout.cgi>�������µ�¼</a>��</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������̳��������</font></td>
<td bgcolor=$miscbackone>��<input type=password name=forumpassword value="$forumpassword">�� <font color=$fontcolormisc>������Ѿ���Ȩ������룬�򲻱���������.</font></td></tr>
<tr height=28><td bgcolor=$miscbackone colspan=2 align=center><font color=$fontcolormisc>�����ȷ����������ȷ�����룬�������޷���¼�Ļ�����ˢ�´�ҳ��(�����ٴΰ���¼��һ��)��</td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name=submit value="��  ¼"></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT></form>
~;
&output("$forumname",\$output);
exit;
1;
