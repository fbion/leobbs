#########################
# �ֻ���̳WAP��
# By Maiweb 
# 2005-11-08
# leobbs-vip.com
#########################
$plug="By Maiweb V060803"; #�벻Ҫȥ��!!!
##############��������##########################
# �����ֻ���Ļ�Ĵ�С�����ԣ��뾡������Ĭ������
$pre = 10 ; # ����б�����
$topicpre=3;# ������ʾÿ��Ƭ��ʾ�Ļظ�����
$pre_index=16;#��ҳ��̳�б�ÿҳ��ʾ������
$mastnum =125;#������ʾ����ÿ��������߻ظ���ʾ�ĳ���
$mastnum2=340;#��������ÿҳ��ʵ�ĳ���
#############���#################################
use UTF8simple;
$uref = new UTF8simple;
$maiweb_sl = "off";
sub waptitle{
print "Content-type: text/vnd.wap.wml;charset=utf-8\n\n";
print "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"; 
print "<!DOCTYPE wml PUBLIC \"-//WAPFORUM//DTD WML 1.1//EN\"
\"http://www.wapforum.org/DTD/wml_1.1.xml\">\n";
print "<wml>";
}
sub wapfoot{
my ($no,$min,$hour)= localtime(time+(3600*$time_hour));
if($hour<10){$hour="0".$hour;}
if($min<10){$min="0".$min;}
$show.= "<p><br/>��ʱ:$hour:$min</p></card></wml>\n";
$u=$uref->toUTF8("gb2312",$show);
print $u;
exit;
}
sub errorout{
my $a=shift();
my($a,$b)=split(/\&/,$a);
$show.= qq~<p>$a<br/><br/>$b<br/><a href="wap_login.cgi">����¼��</a>  <a href="wap_reg.cgi">��ע�᡹</a></p></card></wml>~;
$u=$uref->toUTF8("gb2312",$show);
print $u ;exit;
}
sub msg{
	my ($memberfilename,$p) = @_;
	return if($inmembername eq '����'||$inmembername eq '');
	open (MSGIN, "${lbdir}$msgdir/in/${memberfilename}_msg.cgi");
	sysread(MSGIN, $totalmessages,(stat(MSGIN))[7]);
	close (MSGIN);
	$totalmessages =~ s/\r//isg;
	my @allmessages = split (/\n/, $totalmessages);
	$totalmessages = @allmessages;
	my @newmessages=grep(/^(.+)\tno\t/,@allmessages);
	my $unread = @newmessages;
	$memberfilename=uri_escape($memberfilename);
	my $r= ($unread >0)?"<a href=\"wap_sms.cgi?lid=$lid\">����$unread���µĶ���Ϣ</a><br/>":"";
	return $r;
}
sub check{
	#my $af=shift;
$lid =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
	if(-e "${lbdir}wap/$lid" && $lid ne 'a'){
		open(file,"${lbdir}wap/$lid");
		my $bf=<file>;
		close(file);
		($inmembername,$xh2,$pre,$topicpre,$pre_index,$mastnum,$mastnum2,$city1,$where)=split(/\,/,$bf);
		if($xh2 ne $ENV{'REMOTE_ADDR'}){
		$inmembername = '����';unlink "${lbdir}wap/$lid";$lid='a';
		}
	}else{
		$inmembername = '����';$lid='a';
	}
}