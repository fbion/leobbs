#! /usr/bin/perl

#
# ������ƣ�����
# ����һ��������ת�����򣬽������ǰ�����һɽ��̳�û����ݵ�LeoBBSת�����򣬿��԰�ԭһɽ��̳
# �Ƚ���������ֲ��LeoBBS��
#
# ���������� 
#   �Ѹó����ϴ�����̳����Ŀ¼������Ȩ��Ϊ755��Ȼ���޸����е�$key_input="5";�������еġ�5��
#   ��Ϊ��Ҫת������̳�ľ����ĸ���Ŀ��Ӧ�����֣�Ȼ��ִ�м��ɡ�������Զ��ڸ�Ŀ¼�´���trans��
#   Ŀ¼�����ת������Ŀ������5�������Զ���transĿ¼�´���5��Ŀ¼��ת��������ݾͷ������档
#   ת�����������ʾӦ��ת�����٣�ʵ��ת�����٣���������ֱ���һ�£�������ת���ɹ��ˡ� 
#   Ȼ���� LeoBBS ��ͨ���������Ĵ���һ����̳��Ʃ�紴��һ����̳������Ϊ���������ҡ�����Ӧ��
#   Ŀ¼Ϊforum21����ת����������跨������forum21Ŀ¼����ø�Ŀ¼�������ļ�Ȩ��Ϊ666�� 
#   ����������ģ������������̳���ɡ��������ͳ��һ��������̳�����������Ϳ������ˡ� 
#   �ڳ�������һ���������ܶԴ�����ã�����t2t��������ʹ����localtime��������ʱ����й��ֽ⡣
#   ����Ҫ�ѷֽ�����ʱ�仹ԭ��time�������ɵ�ʱ�䴮�����Բ��������t2t������ֱ�Ӱ��������
#   �Ӻ�����������ĳ����Ȼ���ڳ���ʼ�ĵط�����use Time::Local; �����ˡ� 
#
#   ���Ҫע����ǣ��ó������������з�ʽ��ִ�еģ�����perl ys2leobbs_thread.cgi
#   �����̳�����������ʱ��᳤һ�㣬����ת������������ʾת�����ٵġ�
#

use Time::Local;
require "config.pl";

	$key_input="5";
	my $transdir="$filehead"."trans";
	my $filedata="$filehead$key_input/";
	my $maxsavepost=14;
	
	mkdir("$transdir",0777);
	mkdir("$transdir/$key_input",0777);

	dbmopen(%USERFILE,"$filedata$userfile",0666);
       	%TEMP=%USERFILE;      
   	dbmclose(%USERFILE);
	@wennototal=keys %TEMP;
	@wennototal=sort @wennototal;
	$wennototal=$#wennototal+1;

	foreach $usernotemp(@wennototal){
		($marktemp,$usernametemp,$useremailtemp,$userurltemp,$usertitletemp,$emailtruetemp,$userpasstemp,$userclicktemp,$usernumberstemp,$userhometemp,$vtemp,$datentimentemp,$markendtemp,$lasttemp)=split(/��/,$TEMP{$usernotemp});
#		print "-$marktemp-$usernametemp--$usertitletemp-$markendtemp-\n";
		if (($marktemp eq "start") && ($markendtemp eq "end")) {
			if ($userhometemp==0){
				push(@usernotmp,$usernotemp);
			}
		}
	}
	@usernotmp=sort @usernotmp;
	$usertotalall=$#usernotmp+1;

   	$wennowno=0; $wentotal=0;
	foreach $userno(@usernotmp) {
		$plfilename="${wennowno}.pl"; $cgifilename="${wennowno}.thd.cgi";
		$wennowno +=1;
		$theplfile=""; $thecgifile="";
   		if ($TEMP{$userno}) {
   	   		($mark,$username,$useremail,$userurl,$usertitle,$emailtrue,$userpass,$userclick,$usernumbers,$userhome,$v,$datentimen,$markend,$last)=split(/��/,$TEMP{$userno});
      			if (($mark eq "start") && ($markend eq "end")) {
       			} 
   		}
   		
   		open (FILE, "$filedata$userno");
		$userinfo=<FILE>;
		close (FILE);
		$wentotal++;
		$ttime=t2t($datentimen);
		$thecgifile="$username\t$usertitle\t\tyes\tyes\t$ttime\t$userinfo\t\t\n";
	
		@usernototal=keys %TEMP;
		@usernototal=sort @usernototal;
		$usernototal=$#usernototal+1;
		foreach $userno1(@usernototal){
			($mark,$username1,$useremail1,$userurl1,$usertitle1,$emailtrue1,$userpass1,$userclick1,$usernumbers1,$userhome1,$vv,$datentimen1,$markend,$last)=split(/��/,$TEMP{$userno1});
			if (($mark eq "start") && ($markend eq "end")) {
				if (($usernumbers1 == $usernumbers)&&($userhome1 !=0 )){
					push(@list5,$userno1);
				}
			}
				}
		@list5=sort @list5;
		$no1=@list5;
	######################################################################
		foreach $userno2(@list5){
			if ($TEMP{$userno2}) {
                		($mark,$username2,$useremail2,$userurl2,$usertitle2,$emailtrue2,$userpass2,$userclick2,$usernumbers2,$userhome2,$vvv,$datentimen2,$markend,$last)=split(/��/,$TEMP{$userno2});
                		open (FILE, "${filedata}${userno2}");
				my $userinfo2=<FILE>;
				close (FILE);
				$wentotal++;
				my $ttime2=t2t($datentimen2);
				$thecgifile .="$username2\t$usertitle\t\tyes\tyes\t$ttime2\t$userinfo2\t\t\n";
			}
		}
		undef(@list5);
		my $theinfo=weninfo($userinfo2);
		$theplfile="$wennowno\t$usertitle\t\topen\t$no1\t$userclick\t$username\t$ttime\t$username2\t$ttime2\t$theinfo\t";

#		print "$transdir/$key_input/${wennowno}.pl---$theplfile--\n";
		open(FILE,">$transdir/$key_input/${wennowno}.pl");
		print FILE $theplfile;
		close FILE;

		open(FILE,">$transdir/$key_input/${wennowno}.thd.cgi");
		print FILE $thecgifile;
		close FILE;
		
		print "��ת�� $wennowno ������\n";
	}
	print "ת��ר�� $key_input ����.\n";
	print "Ӧת�� $wennowno �����⣬ʵ��ת�� $usertotalall ������.\n";
	print "Ӧת�� $wennototal ƪ���£�ʵ��ת�� $wentotal ƪ����.\n";
	print "�뵽 $transdir/$key_input Ŀ¼��鿴ת���Ƿ���ȷ��\n";
sub t2t{
#ת��֮ǰ�����ڸ�ʽΪ2001/04/28(13:04:04)��
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