#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

$cookie     = cookie(-name => "lastvisit"    , -value => "$lvisit", -path => "$cookiepath/", -expires => "+30d");
$tempcookie = cookie(-name => "templastvisit", -value => "$lvisit", -path => "$cookiepath/", -expires => "+30d");
print header(-cookie  =>[$cookie, $tempcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
print qq ~<script>location.href="$thisprog";</script>~;
exit;
1;
