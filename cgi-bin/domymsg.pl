#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

open (MSGIN, "${lbdir}$msgdir/in/${memberfilename}_msg.cgi");
sysread(MSGIN, $totalmessages,(stat(MSGIN))[7]);
close (MSGIN);
$totalmessages =~ s/\r//isg;
my @allmessages = split (/\n/, $totalmessages);
$totalmessages = @allmessages;
my @newmessages=grep(/^(.+)\tno\t/,@allmessages);
$unread = @newmessages;
if ($unread && $allowusemsg ne "off") {
    my $intanchumsg = $query->cookie("tanchumsg");
    my $popnew = qq~<script>if (confirm("�����µĶ���Ϣ���Ƿ���ռ���鿴��")) openScript("messanger.cgi?action=inbox",600,400);</script>~ if ((($newmsgpop eq "on")||($newmsgpop eq "popup"))&&($intanchumsg eq ""));
    my $lightnew = qq~<script language="JavaScript">pmBox.bgColor='Lightblue';setInterval("Timer()", 500);x=1;function Timer(){set=1;if(x==0 && set==1){pmBox.bgColor='Lightblue';x=1;set=0;}if(x==1 && set==1){pmBox.bgColor='';x=0;set=0;}}</script>~ if ((($newmsgpop eq "on")||($newmsgpop eq "light")));
    $newmail = qq(<table width=$tablewidth cellpadding=2 cellspacing=0 align=center><tr><td width="*"></td><td align=right id="pmBox" width=215><bgsound src=$imagesurl/images/mail.wav border=0>$lightnew$popnew<span style="cursor:hand" onClick="javascript:openScript('messanger.cgi?action=inbox',600,400)"><img src=$imagesurl/images/newmail.gif border=0><font color=$fonthighlight>���� <B>$unread</B> ���µĶ���Ϣ����ע�����</font></span></td></tr></table>);
}
#д�� cache
open (FILE, ">${lbdir}cache/mymsg/$memberfilename.pl");
print FILE qq~\$totalmessages = $totalmessages;\n~;
print FILE qq~\$unread = $unread;\n~;
print FILE qq~\$newmail = qq($newmail);\n~;
print FILE "1;\n";
close (FILE);
1;
