#!/usr/bin/perl 

####################################
# BBS3000 --> LeoBBS �û�����ת����#
####################################

$userhead= "d:/www/";       				     #BBS3000 �û�Ŀ¼�����Ҫ��© /
$leobbsmember = "c:/apache/htdocs/cgi-bin/leobbs/members/";  #LeoBBS  �û�Ŀ¼�����Ҫ��© /��ע�����ú� 777 ���� 

###############���²����޸�################# 

$ending = ".cgi";
print ("Content-type: text/html\n\n");
$userdir=$userhead;
chop $userdir;
opendir (MEMBERDIR, "$userdir");
  @stats = readdir(MEMBERDIR);
closedir (MEMBERDIR);
@stats = grep(/cgi$/, @stats);
$totaluserdata=$#stats+1;
if ($totaluserdata eq 0) {
  opendir (MEMBERDIR, "$userdir");
  @stats = readdir(MEMBERDIR);
  closedir (MEMBERDIR);
  @stats = grep(/pl$/, @stats);
  $totaluserdata=$#stats+1;
}
@stats = sort @stats;
$DateRegistered = time();
for ($i=0;$i<$totaluserdata;$i++) {
    $name = @stats[$i];
    $filesname="$userhead$name";
    open(file,"$filesname");
    @array=<file>;
    close(file);
    $wuyu = "@array";
    ($Password,$UserName,$Email,$URL,$DateRegistered,$Signature,$rdsex,$rdwork,$Location,$rdlove,$rdfy,$rdhf,$AvatarWording,$jiao,$iewin,$OICQnumber,$photo,$savecookie,$dejiname,$deji)=split(/\t/,$wuyu);

    ($name,$temp)=split(/\./,$name);
    $name =~ s/ /_/gi;
    $name =~ tr/A-Z/a-z/;
    $name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\=\+\\\[\]\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
    open(IBMEMBER,">$leobbsmember$name$ending");
    print IBMEMBER "$UserName\t$Password\tMember\tme\t$rfy|$rhf\t$Email\tyes\txxx.xxx.xxx.xxx\t$URL\t$OICQnumber\t$ICQnumber\t$Location\t$rdlove\t$DateRegistered\tû�з����\t$Signature\t0\t\t$AvatarWording\t$misc1\t$misc2\t$misc3\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$addjy\t$meili\t$mymoney\t$postdel\t$rdsex\t$education\t$marry\t$rdwork\t$born\t$useradd1\t$useradd2\t$jhmp\t\n";
    close(IBMEMBER);
    print "�û� $UserName �Ѿ��ɹ�ת���� LeoBBS �û��ˣ�<BR><BR>";
}
print "�ܹ�ת���� $totaluserdata ���û���<BR><BR>";
exit;
