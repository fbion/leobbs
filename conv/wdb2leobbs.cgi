#!/usr/bin/perl

######################################
# WDB ����+�û����� --> LeoBBS ת����#
######################################

$wdbdir = "/path/to/WDB main dir/";       # ������WDB ���������ڵ�Ŀ¼�ľ���·�������Ҫ��© / ��
$leobbsdir = "/path/to/LeoBBS main dir/"; # ������ LeoBBS ���������ڵ�Ŀ¼�ľ���·�������Ҫ��© / ��ע�����ú� 777 ���ԡ�

$userhead= "g:/www/9438/wdbmember/";      # WDB �û�Ŀ¼�����Ҫ��© /
$leobbsmember = "g:/www/9438/leobbs/";    # LB5000 �û�Ŀ¼�����Ҫ��© / ��ע������ 777 ����

################���²����޸�
$nowtime = time;
$ending = ".cgi";
print ("Content-type: text/html\n\n");
$userdir=$userhead;
chop $userdir;
opendir (MEMBERDIR, "$userdir");
  @stats = readdir(MEMBERDIR);
closedir (MEMBERDIR);
@stats = sort @stats;
$totaluserdata=$#stats+1;
for ($i=0;$i<$totaluserdata;$i++) {
$name = @stats[$i];
     $filesname="$userhead$name";
     open(file,"$filesname");
     @array=<file>;
     close(file);
     $wuyu = "@array";
     $wuyu =~ s/^\<\?die\(\)\;\?\>\|//isg;
    ($name,$password,$usericon,$email,$oicq,$regdate,$signature,$homepage,$area,$no,$no,$no,$postamount,$publicemail,$no)=split(/\|/,$wuyu);

    ($name,$temp)=split(/\./,$name);
     $name =~ s/ /_/gi;
     $name =~ tr/A-Z/a-z/;
    open(IBMEMBER,">$leobbsmember$name$ending");
    print IBMEMBER "$name\t$password\tMember\tme\t$postamount\t$email\t$publicemail\txxx.xxx.xxx.xxx\t$homepage\t$oicq\t$icqnumber\t$area\t\t$nowtime\tNot Posted\t$signature\t\t\t$usericon\t\t\t\t\t80\t80\t\n";
    close(IBMEMBER);
    print "�û� $UserName �Ѿ��ɹ�ת���� LeoBBS �û��ˣ�<BR>";
}

opendir (DIRS, "$wdbdir");
my @dirs1 = readdir(DIRS);
closedir (DIRS);
my @dirs1 = grep(/^forum/i, @dirs1);
$dir2 = @dirs1;

foreach $dirs1 (@dirs1) {
    if ($dirs1 !~ /forum[0-9]+$/) { $dir2--; next;}
    mkdir ("$leobbsdir/$dirs1", 0777);
    chmod (0777,"$leobbsdir/$dirs1");

    opendir (DIRS, "${wdbdir}$dirs1");
    my @files = readdir(DIRS);
    closedir (DIRS);
    @files = grep(/^f\_/i, @files);
    $a = 1;
    foreach $files1 (@files) {
        open (FILE, "${wdbdir}${dirs1}/$files1");
        @allthreads = <FILE>;
        close (FILE);
        open (FILE, ">${leobbsdir}${dirs1}/$a.thd.cgi");
        foreach $thread (@allthreads) {
            ($topictitle,$membername,$post,$postdate,$postipaddresstemp,$posticon,$showsignature) = split (/\|/,$thread);
            if ($showsignature eq 1) { $showsignature = "yes"; } else { $showsignature = "no"; }
            if ($posticon eq "ran") { $posticon = ""; }
            print FILE "$membername\t����������$topictitle\t$postipaddresstemp=$postipaddresstemp\tyes\t$showsignature\t$postdate\t$post\t$posticon\t\n";
        }
        close (FILE);
        $a++;
    }
}
$dir1 = @dirs1;
print "<BR><BR>�ܹ�ת���� $dir2 ������̳��<BR><BR>������������������޸���̳�����棬�����ؽ�������̳һ��\n";
exit;
