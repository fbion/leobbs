#!/usr/bin/perl
###############################################
#  Ubb X.XX => LeoBBS ����ת��
###############################################
#ʹ�ð�����
#
#����$ubbnoncgiĿ¼Ϊubb��noncgiĿ¼
#
#����$leobbspathĿ¼ΪLeoBBS��cgi-binĿ¼
#
#����["$ubbnoncgi/Forum4","4"],�޸�ǰ���Forum4
#�е�4����Ҫת����ubb��̳Ŀ¼id,�����4��LeoBBS
#����̳id��Ҫת�������̳�����ö��У������Ǻ�
#��Ķ���
#
#����$truetime�Ƿ����timeģ�飬��Щ������֧�֣�
#�����֧��ѡ0, �������з����ͻظ�ʱ��Ϊ��ǰʱ�䣬
#֧��ѡ1�������Լ�����
#
###############################################
use CGI qw(:standard);
$CGI::POST_MAX=1024;
$CGI::DISABLE_UPLOADS = 1;
$CGI::HEADERS_ONCE = 1;
use Time::Local;

$ubbnoncgi ='/home/public_html/non'; #UBB Ŀ¼�����Ҫ��© / 
$leobbspath='/home/cgi-bin/leobbs';  #LeoBBS ��Ŀ¼�����Ҫ��© / ��ע������ 777 ����

$convertdata=
[
	["$ubbnoncgi/Forum12","1"],
	["$ubbnoncgi/Forum13","2"],
	["$ubbnoncgi/Forum4","3"],
	["$ubbnoncgi/Forum9","4"],
	["$ubbnoncgi/Forum10","5"],
	["$ubbnoncgi/Forum11","6"],
	["$ubbnoncgi/Forum5","7"],
	["$ubbnoncgi/Forum6","8"],
	["$ubbnoncgi/Forum7","9"],
	["$ubbnoncgi/Forum8","10"],
	["$ubbnoncgi/Forum1","11"],
	["$ubbnoncgi/Forum2","12"]
	
	
];
 

###ÿ100����ӡһ����Ϣ
$hz=100;
$truetime=1;#�����Ƿ����timeģ�飬�ҷ�����Щ������֧�֣������֧��ѡ0, �������з����ͻظ�ʱ��Ϊ��ǰʱ��

print "Content-type: text/html\n\n";

print "ת����ʼ ",time(),"<br><br><hr>\n\n";


foreach $tempturn (@$convertdata)
{
	$oldforumpost=$tempturn->[0];
	$newboardid=$tempturn->[1];
	print "old:$oldforumpost  new:$newboardid\n<br>";	
		
	opendir(CURDIR,$oldforumpost) || die "forum path read error";
	@postfiles=readdir(CURDIR);
	close(CURDIR);
	
	mkdir("$leobbspath/forum$newboardid",0777);
	
	$i=0;
	
	print "ת�� $oldforumpost �� $newboardid ��ʼ " ,time()," <br><br>","\n";
	$count=0;
	foreach $temp(@postfiles)
	{
		
		if($temp=~/(\d{6})\.cgi/)
		{	
			
			$id=$1;
			$count++; 
			open(TEMPF,"$oldforumpost/$temp");		
			@filelines=<TEMPF>;
			close(TEMPF);
			
			
			$startline=$filelines[0];
			if($startline=~/^A/)
			{			
				
				###table ut_topics
				### id  subject boardId top locked lockMoveTitle lockMoveText 
				### PostNum lastPostTime lastPostName lastPostId
				
				###��һ��:A||����״̬||�ظ�����||�û���||����||�鵵����Ϣ||����ͼ||ע��(���类ת��)
				###����:  Z||�ظ����||�ظ��û���||�ظ�����||�ظ�ʱ��||�ʼ�||�ظ���Ϣ||IP��ַ||�Ƿ�ע��||����ͼ��
				($subject,$locked)=('','open');
				
					
				@startlines=split(/\|\|/,$startline);
				$subject=$startlines[4];
				$locked="closed" if($startlines[1]=~/X/);
				$PostNum=$startlines[2]||1;
				$postname=$startlines[3];
				
				$lastline=$filelines[1];
				
				@lastlines=split(/\|\|/,$lastline);
				$posttime=&get_time($lastlines[3],$lastlines[4]);
				
				$tempcount=@filelines;
				$lastline=$filelines[$tempcount-1];
				@lastlines=split(/\|\|/,$lastline);
				$lastPostTime=&get_time($lastlines[3],$lastlines[4]);
				
				$lastPostName=$lastlines[2];
				
				
				
				open(TEMPT,">$leobbspath/forum$newboardid/$count.pl");		
				print TEMPT "$count\t$subject\t\t$locked\t$PostNum\t0\t$postname\t$posttime\t$lastPostName\t$lastPostTime\t\n";
				close(TEMPT);
				
				
				
				### table ut_posts
				###id userId userNameBak postSubject boardid topicId parentId 
				###ip postTime &&body&& 
				###����:  Z||�ظ����||�ظ��û���||�ظ�����||�ظ�ʱ��||�ʼ�||�ظ���Ϣ||IP��ַ||�Ƿ�ע��||����ͼ��
				#               1           2         3        4        5        6       7        8         9
				open(TEMPT,">$leobbspath/forum$newboardid/$count.thd.cgi");
				foreach $eachline (@filelines)
				{
					if($eachline=~/^Z/){
					
					@eachlines=split(/\|\|/,$eachline);
					
					
					$userNameBak=$eachlines[2];
					$ip=$eachlines[7];
					$postTime=&get_time($eachlines[3],$eachlines[4]);
					
					$body=$eachlines[6];			
					$body=$body;
								
				print TEMPT "$userNameBak\t$subject\t$ip=\tyes\tyes\t$postTime\t$body\t\t\n";
				}
									
				}
				close(TEMPT);	
				
			}
			$i++;
			if(($i/$hz)==0)	{print "����ת�� $i ����,��ʼ�µ�ת�� ...\n<br>";}
		}
	}
	
	
	print "�ܹ� $i ������,ת����� ",time(),"<br><hr>\n\n";

}



print "ת��ȫ����� ",time(),"\n<br>";


exit;

#=====================================

sub  get_time
{
	
	($datestr,$timestr)=@_;
	
	($month,$day,$year)=split(/\-/,$datestr);
	($temp,$ampm)=split(/\s/,$timestr);
	($hour,$minute)=split(/\:/,$temp);
	$month=&getridzero($month);
	$day=&getridzero($day);
	$hour=&getridzero($hour);
	$minute=&getridzero($minute);
	$ss=0;
		
		
	###$year=int($year)-1900;
    	if ($truetime ==1){
    	$time = timelocal($ss,$minute,$hour,$day,$month-1,$year);
    	}else{
    	$time=time();
    	}
    	
    	return($time);	
    	
}

sub getridzero
{
	
    $str=shift;
    $str=~s/^0//;
    return($str);    
}






sub htmlhead
{
   if (!$htmlhead)
   {
      print "Content-type: text/html\n\n";
   }
   $htmlhead = 1;
}


1;

