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

if ($inmembername eq "����") { $loginmessage = "���������¼���ܲ鿴���飬����ֻ��ʾ����̳��������ͼ����"; }
if ($membercode eq "ad" || $membercode eq 'smo') { $delcache = "����<B>[<a href=delmaincache.cgi title=����Ϸ�����Ϣ�в��������ͺ�Ļ��������ô˹���>����������ҳ����</a>]</B>"}
my $leopic = qq~<a href=http://www.LeoBBS.com target=_blank><img src=$imagesurl/images/lblogo.gif width=88 height=31 border=0 title="----------------    ��    ---------------\n�����ᳬ����̳(LeoBBS)���װ��Ƽ�������\n�������ʾ�� Powered By LeoBBS.com��\n����л���������ǵ���̳�����������ĸ��ã���\n----------------    ��    ---------------"></a>~ if ($noads ne "yes");
$output .= qq~</td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT><img src=$imagesurl/images/none.gif height=5><br><SCRIPT>valigntop()</SCRIPT>
<table cellspacing=0 cellpadding=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellspacing=1 cellpadding=6 width=100%>
<tr><td width=75% bgcolor=$titlecolor $catbackpic><b>-=> LeoBBS ��̳ͼ�� $delcache</td>
<td align=right noWrap bgcolor=$titlecolor width=25% $catbackpic>����ʱ���Ϊ - $basetimes &nbsp;</td></tr>
<tr><td bgcolor=$forumcolortwo colspan=3>
<table cellspacing=4 cellpadding=0 width=92% align=center>
<tr><td colspan=6>��̳ͼ���������¼���ҷ��ʺ����ʾ&nbsp;$loginmessage</font></div></td></tr>
<tr><td><font color=$fonthighlight TITLE=����ע���Ա���Ժͻظ�>������̳</font></td>
<td><font color=$fonthighlight TITLE=�����κ��˷��Ժͻظ�>������̳</font></td>
<td><font color=$fonthighlight TITLE=����̳���Ͱ������ԣ�����ע���û�ֻ�ܻظ�>������̳</font></td>
<td><font color=$fonthighlight TITLE=����ӵ�з���������Ѿ�������֤��ע���Ա����>������̳</font></td>
<td><font color=$fonthighlight TITLE=������֤��Ա���Ժͻظ�>��֤��̳</font></td>
<td colspan=2><font color=$fonthighlight>������̳</font></td></tr>
<tr><td><img src=$imagesurl/images/$skin/$zg_havenew> ���µ�����</td>
<td><img src=$imagesurl/images/$skin/$kf_havenew> ���µ�����</td>
<td><img src=$imagesurl/images/$skin/$pl_havenew> ���µ�����</td>
<td><img src=$imagesurl/images/$skin/$bm_havenew> ���µ�����</td>
<td><img src=$imagesurl/images/$skin/$rz_havenew> ���µ�����</td>
<td><img src=$imagesurl/images/$skin/$jh_pic TITLE=ֻ����̳���Ͱ������ԺͲ���> ֻ��������</td>
<td align=right valign=top rowspan=2>$leopic</td></tr>
<tr><td><img src=$imagesurl/images/$skin/$zg_nonew> û��������</td>
<td><img src=$imagesurl/images/$skin/$kf_nonew> û��������</td>
<td><img src=$imagesurl/images/$skin/$pl_nonew> û��������</td>
<td><img src=$imagesurl/images/$skin/$bm_nonew> û��������</td>
<td><img src=$imagesurl/images/$skin/$rz_nonew> û��������</td>
<td><img src=$imagesurl/images/$skin/shareforum.gif TITLE=�ͱ���̳�������ӵ�������̳> ������̳��</td></tr>
</table>~;
1;
