#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

if ($inmembername ne "����") {
    if (($membercode eq "ad" || $inmembmod eq "yes" || $membercode eq 'smo')&&($membercode ne 'amo')) {
	$deltopicmore1 = qq~��̳ѡ��~;
	$deltopicmore2 = qq~<img src=$imagesurl/images/$skin/adminlock.gif width=12 height=15> <a href=forumoptions.cgi?action=prune&forum=$inforum>������������</a>~;
	$deltopicmore3 = qq~<img src=$imagesurl/images/$skin/adminlock.gif width=12 height=15> <a href=postings.cgi?action=repireforum&forum=$inforum>�޸������̳</a>~;
    } else { $deltopicmore1=""; $deltopicmore2=""; $deltopicmore3=""; }

    $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellspacing=0 cellpadding=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellspacing=1 cellpadding=6 width=100%>
<tr><td width=80% bgcolor=$titlecolor $catbackpic><font color=$titlefontcolor><b>-=> LeoBBS ��̳ͼ��</b></font> (<a href=delforumcache.cgi?forum=$inforum title=��������в��������ͺ�Ļ��������ô˹���>���¸�������</a>)</td>
<td noWrap bgcolor=$titlecolor width=20% align=right $catbackpic><font color=$titlefontcolor> ����ʱ���Ϊ - $basetimes &nbsp;</td></tr><tr><td colspan=3 bgcolor=$forumcolorone>
<table cellspacing=4 cellpadding=0 width=94% align=center><tr>
<td width=20%><font color=$fonthighlight>�򿪵�����</font></td>
<td width=21%><font color=$fonthighlight>�ظ��� $hottopicmark �ε�������</font></td>
<td width=22%><font color=$fonthighlight>��������ͼ��</font></td>
<td width=21%><font color=$fonthighlight>��������ͼ��</font></td>
<td width=14%><font color=$fonthighlight>$deltopicmore1</font></td></tr><tr>
<td><img src=$imagesurl/images/$skin/topicnew3.gif> �ϴ���֮�󷢱�</td>
<td><img src=$imagesurl/images/$skin/topichot3.gif> <img src=$imagesurl/images/$skin/closedbhot.gif> �ϴ���֮�󷢱�</td>
<td><img src=$imagesurl/images/$skin/topiclocked3.gif> �����ܻظ�������</td>
<td><img src=$imagesurl/images/$skin/abstop.gif> <img src=$imagesurl/images/$skin/lockcattop.gif> <img src=$imagesurl/images/$skin/locktop.gif> �̶�������</td>
<td>$deltopicmore2</td></tr><tr>
<td><img src=$imagesurl/images/$skin/topicnonew.gif> �ϴ���֮�����»ظ�</td>
<td><img src=$imagesurl/images/$skin/topichotnonew.gif> �ϴ���֮�����»ظ�</td>
<td><img src=$imagesurl/images/$skin/closedb1.gif> �����ܻظ���ͶƱ</td>
<td><img src=$imagesurl/images/$skin/closedb.gif> ͶƱ��������</td>
<td>$deltopicmore3</td></tr></table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT><BR>
~;
} else {
    $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellspacing=0 cellpadding=0 width=$tablewidth align=center bgcolor=$tablebordercolor>
<tr><td><table cellspacing=1 cellpadding=6 width="100%"><tr>
<td width=80% bgcolor=$titlecolor $catbackpic><font color=$titlefontcolor><b>-=> LeoBBS ��̳ͼ��</b></font> (<a href=delforumcache.cgi?forum=$inforum title=��������в��������ͺ�Ļ��������ô˹���>���¸�������</a>)</td>
<td noWrap bgcolor=$titlecolor width=20% align=right $catbackpic><font color=$titlefontcolor>����ʱ���Ϊ - $basetimes &nbsp;</td></tr><tr><td colspan=3 bgcolor=$forumcolorone>
<table cellspacing=4 cellpadding=0 width=92% align=center><tr>
<td width=21%><img src=$imagesurl/images/$skin/topicnonew.gif> �����۵�����</td>
<td width=21%><img src=$imagesurl/images/$skin/closedb.gif> ͶƱ��������</td>
<td width=28%><img src=$imagesurl/images/$skin/topiclocked3.gif> <img src=$imagesurl/images/$skin/closedb1.gif> �ر��˵����⣬�����ܻظ�</td>
<td width=21%><img src=$imagesurl/images/$skin/abstop.gif> <img src=$imagesurl/images/$skin/lockcattop.gif> <img src=$imagesurl/images/$skin/locktop.gif> (�ܡ���)�̶�������</td>
</tr></table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT><BR>
~;
}
1;
