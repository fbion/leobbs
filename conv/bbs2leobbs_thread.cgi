#!/usr/bin/perl

#
# ������ƣ�����
#  ����һ��������ת�����򣬽��BBS3000�û����ݵ�LeoBBSת�����򣬿��԰�ԭBBS3000������
#  �Ƚ���������ֲ��LeoBBS��
#  ���������� 
#   �Ѹó����ϴ�����̳����Ŀ¼������Ȩ��Ϊ755��Ȼ���޸����е�$id="admin";�������еġ�admin��
#   ��Ϊ��Ҫת������̳�ľ����ĸ���Ŀ��Ӧ��$id����$filepath= "/home/httpd/cgi-bin/bbs3000"�� 
#   ������ʾ���ض����޸ġ�Ȼ���BBS3000��Ŀ¼��Ҳ����$filepath��Ӧ��Ŀ¼Ȩ������Ϊ777����
#   ִ�м��ɡ�������Զ��ڸ�Ŀ¼�´���trans��Ŀ¼�����ת����id��admin�������Զ���transĿ¼
#   �´���admin��Ŀ¼��ת��������ݾͷ������档ת�����������ʾӦ��ת�����٣�ʵ��ת�����٣�
#   ��������ֱ���һ�£�������ת���ɹ��ˡ� 
#   Ȼ����LB5000��ͨ���������Ĵ���һ����̳��Ʃ�紴��һ����̳������Ϊ���������ҡ�����Ӧ��Ŀ¼
#   Ϊforum21����ת����������跨������forum21Ŀ¼����ø�Ŀ¼�������ļ�Ȩ��Ϊ666��
#   ����������ģ������������̳���ɡ��������ͳ��һ��������̳�����������Ϳ������ˡ�
#   �ڳ�������һ���������ܶԴ�����ã�����t2t��������ʹ����localtime��������ʱ����й��ֽ⡣
#   ����Ҫ�ѷֽ�����ʱ�仹ԭ��time�������ɵ�ʱ�䴮�����Բ��������t2t������ֱ�Ӱ��������
#   �Ӻ�����������ĳ����Ȼ���ڳ���ʼ�ĵط�����use Time::Local; �����ˡ� 

#   ���У��Ǹ�$id,����LeoBBS��Ķ�������BBS3000�����̳ID��Ʃ�磬�и���CGI��̳�����㿴����
#   ������http://www.yuzi.net/cgi-bin/bbs3000/bbs.cgi?id=yuzi�����������yuzi����$id��Ҳ��
#   ��˵�����ת�����CGI��̳����Ȼ��ֻ��������̳���һ������̳������ôӦ����ô����$id="yuzi";��
#   ����ܹ����룬���á���������������һ������ô��Ӧ�ҵ���̳��
#   URL����http://www.yuzi.net/cgi-bin/bbs3000/bbs.cgi?id=��������ô���þ�Ӧ����$id="����"; 



use Time::Local;
print ("Content-type: text/html\n\n"); 

my $filepath     = "/home/httpd/cgi-bin/bbs3000";   # ��BBS3000�е�$filepath���ݱ���һ��

my $id="admin"; # ΪҪת������̳����

my $transdir="${filepath}/trans";
my $maxsavepost=14;

mkdir("$transdir",0777);
mkdir("$transdir/$id",0777);



$wennowno=0; $wentotal=0;

open(TITLES,"$filepath/list/$id/bbs");
@hastitles=<TITLES>;
close(TITLES);
@hastitles=sort @hastitles;
$usertotalall=@hastitles;

foreach $wentitletmp(@hastitles) {
	$wentitletmp=~ s/\n//g;
	if($wentitletmp ne "") {
		$wentitle=substr($wentitletmp,0,14);
	}

	$wennowno +=1;
	$theplfile=""; $thecgifile="";

	$wen="$filepath/list/$id/$wentitle";
	if (-f $wen){
   		open (FILE, "$wen");
		$weninfo=<FILE>;
		close (FILE);
		($rtitles,$rthistime,$rusername,$nr,$rfrom,$rhasreply,$remote,$rlastname,$rlasttime,$re,$rhassee,$jing,$lock)=split(/\t/,$weninfo);
	}
	
	$wentotal++;
	$ttime=t2t($rthistime);
	$thecgifile="$rusername\t$rtitles\t\tyes\tyes\t$ttime\t$nr\t\t\n";
	$ttimelast=t2t($rlasttime);

	if($rhasreply > 0){
		$wenre="$filepath/list/$id/$re";
		if (-f $wenre){
			open(REPLY,"$wenre");
			@hasreply=<REPLY>;
			close(REPLY);
			@hasreply=sort @hasreply;
			$no1=@hasreply;
			foreach $m (@hasreply){
				$m=~ s/\n//g;
				if($m ne ""){
					($rtime2,$rthistime2,$rusername2,$rcomment2,$rfrom2,$remote2,$retitles2)=split(/\t/,$m);
					if ($rtime2 eq $wentitle) {
						$wentotal++;
						$ttime2=t2t($rthistime2);
						$thecgifile .="$rusername2\t$rtitles\t\tyes\tyes\t$ttime2\t$rcomment2\t\t\n";
					}
				}
			}
			undef(@hasreply);
		}
	}
	my $theinfo=weninfo($rcomment2);
	$theplfile="$wennowno\t$rtitles\t\topen\t$no1\t$rhassee\t$rusername\t$ttime\t$rlastname\t$ttimelast\t$theinfo\t";

	open(FILE,">$transdir/$id/${wennowno}.pl");
	print FILE $theplfile;
	close FILE;

	open(FILE,">$transdir/$id/${wennowno}.thd.cgi");
	print FILE $thecgifile;
	close FILE;
		
	print "��ת�� $wennowno ������\n";
}
print "ת��ר�� $id ����.\n";
print "Ӧת�� $usertotalall �����⣬ʵ��ת�� $wennowno ������.\n";
print "ʵ��ת�� $wentotal ƪ����.\n";
print "�뵽 $transdir/$id Ŀ¼��鿴ת���Ƿ���ȷ��\n";


sub t2t{
#ת��֮ǰ�����ڸ�ʽΪ2001-05-08.00:15:38,
#��������������߱��⼸������,���ո�ʽ������ʱ��Ķ�λ��һЩ�޸ģ��Ϳ������������
	my $ntime=shift;
	my($secn,$minn,$hourn,$dayn,$monn,$yearn);
	$yearn=substr($ntime,0,4); $monn=substr($ntime,5,2); $dayn=substr($ntime,8,2);
	$hourn=substr($ntime,11,2); $minn=substr($ntime,14,2); $secn=substr($ntime,17,2);
	$yearn=int($yearn)-1900;   
	$monn=dotime($monn)-1;
	$dayn=dotime($dayn);
	$hourn=dotime($hourn);
	$minn=dotime($minn);
	$secn=dotime($secn);
	$time = timelocal($secn,$minn,$hourn,$dayn,$monn,$yearn);
	return $time;
}

sub dotime {
	my $dtime=shift;
	$dtime=substr($dtime,1,1) if(substr($dtime,0,1) eq "0");
	$dtime=int($dtime);
	$dtime=1 if($dtime<1);
	return $dtime;
}

sub weninfo {
	my $inposttemp=shift;
        if (length($inposttemp)>$maxsavepost) {
            $inposttemp = substr($inposttemp,0,$maxsavepost)."  ...";
        }
        return $inposttemp;
}