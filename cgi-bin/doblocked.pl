#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

if ($inmembername eq "") { $inusername = "����"; }
$ipaddress = "$ENV{'REMOTE_ADDR'}($ENV{'HTTP_X_FORWARDED_FOR'} -- $ENV{'HTTP_CLIENT_IP'})";
$inmembername =~ s/\_/ /g;

$output .= qq~<p>
<tr>
<td bgcolor=$titlecolor $catbackpic valign=middle colspan=2 align=center><font color=$fontcolormisc><b><font color=$fonthighlight>�������͹���Ա����̳����</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
<b>�Ӱ�ȫ�Ƕȿ��ǣ�̳�����ܰ�������̳�����������ģ�������ͨ�� Email ���߻ش����������͡�</b><p>
Ϊ�˷�ֹ�� hacker ��������������� IP ��ַ $ipaddress ������û��� $inmembername �Ѿ�����¼��<br>
���õ�������� $ENV{'HTTP_USER_AGENT'}<p>
����㲻�ǹ���ģ��㲻Ҫ���ڵ��ġ�<p><p>
</td></tr></table></td></tr></table>
~;
$output =~ s/�û�����/���棡/g;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&output($boardname,\$output);
1;
