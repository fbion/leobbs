#!/usr/bin/perl 

#########################################
# һɽ������̳�û����� --> LeoBBS ת����#
#########################################

$userhead= "/home/httpd/cgi-bin/qlbbs/members/";       	#һɽ������̳�û�Ŀ¼�����Ҫ��© /
$leobbsmember = "/home/httpd/cgi-bin/leobbs/members/";  #LeoBBS  �û�Ŀ¼�����Ҫ��© / ��ע������ 777 ����

###############���²����޸�################# 

$ending = ".cgi";
print ("Content-type: text/html\n\n");
$userdir=$userhead;
chop $userdir;
opendir (MEMBERDIR, "$userdir");
  @stats = readdir(MEMBERDIR);
closedir (MEMBERDIR);
@stats = grep(/cgi$/, @stats);
@stats = sort @stats;
$totaluserdata=$#stats+1;
for ($i=0;$i<$totaluserdata;$i++) {
    $name = @stats[$i];
    $filesname="$userhead$name";
    open(file,"$filesname");
    @array=<file>;
    close(file);
    $wuyu = "@array"; 
#   ($Password,$UserName,$Email,$URL,$DateRegistered,$Signature,$rdsex,$rdwork,$Location,$rdlove,$rdfy,$rdhf,$AvatarWording,$jiao,$iewin,$OICQnumber,$photo)=split(/|/,$wuyu);
    ($UserName,$Password,$Email,$URL,$rdsex,$xx,$yy,$jj,$Signature,$rdwork,$Location1)=split(/\|/,$wuyu);
    $AvatarWording="";$Location="";

    $TotalPosts = $rdfy+$rdhf;
    ($name,$temp)=split(/\./,$name);
    $DateRegistered = time();
    $name =~ s/ /_/gi;
    $name =~ tr/A-Z/a-z/;
    $name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\=\+\\\[\]\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
    open(IBMEMBER,">$leobbsmember$name$ending");
    print IBMEMBER "$UserName\t$Password\tMember\tme\t$TotalPosts\t$Email\tyes\t����\t$URL\t$OICQnumber\t$ICQnumber\t$Location\t\t$DateRegistered\tû�з����\t$Signature\t0\t\t$AvatarWording\t\t\t\t\t\t\t\n";
    close(IBMEMBER);
    print "�û� $UserName �Ѿ��ɹ�ת���� LeoBBS �û��ˣ�<BR><BR>";
}
print "�ܹ�ת���� $totaluserdata ���û���<BR><BR>\n";
exit;
