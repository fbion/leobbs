#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

if ($inmembername eq "����") {
    print "<script language='javascript'>document.location = 'loginout.cgi?forum=$inforum'</script>";
    exit;
}
if ((($userregistered ne "no")&&($allowedentry{$inforum} eq "yes"))||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")||(($userregistered ne "no") && ($forumpassword eq $forumpass))) {
    $allowforumcookie = cookie(-name => "forumsallowed$inforum", -value => "$forumpass", -path => "$cookiepath/", -expires => "0");

    print header(-cookie=>[$allowforumcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

    print qq ~<script>location.href="$thisprog?forum=$inforum";</script>~;
    exit;
}
&error("������̳&�㲻����������̳��");
1;
