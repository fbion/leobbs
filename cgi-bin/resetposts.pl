#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

my $nowtime = $currenttime + 10;
&setlastvisit("$inforum,$nowtime,1");
$forumlastvisit = $currenttime;
print header(-cookie=>[$tempvisitcookie, $permvisitcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
print qq ~<script>location.href="$thisprog?forum=$inforum";</script>~;
exit;
1;
