#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

sub sendtoposter {
    my ($senduser,$sendto, $moveto,$action,$forum,$topic,$topictitle,$sendly) = @_;
    $sendly = "<BR>���ɣ�<font color=red>$sendly</font><BR>" if ($sendly ne "" && $sendly ne " ");
    $topictitle=~s/����������//;
    $topictitle = "���˲鿴" if ($topictitle eq "");
    my $memberfilename = $sendto;
    $memberfilename =~ s/ /\_/g;
    $memberfilename =~ tr/A-Z/a-z/;
    my $currenttime = time;
    my $filetoopen = "${lbdir}$msgdir/in/$memberfilename" . "_msg.cgi";
    $filetoopen = &stripMETA($filetoopen);
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open (FILE, "$filetoopen");
    flock (FILE, 1) if ($OS_USED eq "Unix");
    sysread(FILE, my $inboxmessages,(stat(FILE))[7]);
    close (FILE);
    $inboxmessages =~ s/\r//isg;

    $topictitle = "<a href=topic.cgi?forum=$forum&topic=$topic target=_blank>$topictitle</a>";
    open (FILE, ">$filetoopen");
    flock (FILE, 2) if ($OS_USED eq "Unix");
    if ($action eq "move") {
        print FILE "����������$senduser\tno\t$currenttime\t����ϵͳѶϢ\t������ӡ�$topictitle���ѱ�����Ա $senduser ���� $moveto <br>�����κ�������Է���Ѷ������Ա $senduser ��ѯ<br><br>---------------------------------------<br>�װ����ᳬ����̳ http://bbs.LeoBBS.com\n";
    }
    elsif ($action eq "jinghua") {
        print FILE "����������$senduser\tno\t$currenttime\t����ϵͳѶϢ\t������ӡ�$topictitle���ѱ�����Ա $senduser ��ѡΪ��������!!��л��Ϊ����̳�����ĺ����ӣ�лл��<br><br>�����κ�������Է���Ѷ������Ա $senduser ��ѯ<br><br>---------------------------------------<br>�װ����ᳬ����̳ http://bbs.LeoBBS.com\n";
    }
    elsif ($action eq "deletethread") {
        print FILE "����������$senduser\tno\t$currenttime\t����ϵͳѶϢ\t������ӡ�$topictitle���ѱ�����Ա $senduser ɾ����<br>$sendly<br>�����κ�������Է���Ѷ������Ա $senduser ��ѯ<br><br>---------------------------------------<br>�װ����ᳬ����̳ http://bbs.LeoBBS.com\n";
    }
    elsif ($action eq "deletepost") {
        print FILE "����������$senduser\tno\t$currenttime\t����ϵͳѶϢ\t�������ӡ�$topictitle���еĻظ��ѱ�����Ա $senduser ɾ����<br>$sendly<br>�����κ�������Է���Ѷ������Ա $senduser ��ѯ<br><br>---------------------------------------<br>�װ����ᳬ����̳ http://bbs.LeoBBS.com\n";
    }
    elsif ($action eq "lock") {
        print FILE "����������$senduser\tno\t$currenttime\t����ϵͳѶϢ\t������ӡ�$topictitle���ѱ�����Ա $senduser ������<br>$sendly<br>�����κ�������Է���Ѷ������Ա $senduser ��ѯ<br><br>---------------------------------------<br>�װ����ᳬ����̳ http://bbs.LeoBBS.com\n";
    }
    elsif ($action eq "postdeleteonce") {
        print FILE "����������$senduser\tno\t$currenttime\t����ϵͳѶϢ\t������ӡ�$topictitle���ѱ�����Ա $senduser ���Ρ�<br>$sendly<br>�����κ�������Է���Ѷ������Ա $senduser ��ѯ<br><br>---------------------------------------<br>�װ����ᳬ����̳ http://bbs.LeoBBS.com\n";
    }
    elsif ($action eq "unpostdeleteonce") {
        print FILE "����������$senduser\tno\t$currenttime\t����ϵͳѶϢ\t������ӡ�$topictitle���ѱ�����Ա $senduser ���Ρ�<br>$sendly<br>�����κ�������Է���Ѷ������Ա $senduser ��ѯ<br><br>---------------------------------------<br>�װ����ᳬ����̳ http://bbs.LeoBBS.com\n";
    }
    print FILE "$inboxmessages\n";
    close (FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
}
1;
