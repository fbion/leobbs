#!/usr/bin/perl
#########################
# �ֻ���̳WAP��
# By Maiweb 
# 2005-11-08
# leobbs-vip.com
#########################
BEGIN {
    $startingtime=(times)[0]+(times)[1];
    foreach ($0,$ENV{'PATH_TRANSLATED'},$ENV{'SCRIPT_FILENAME'}){
    	my $LBPATH = $_;
    	next if ($LBPATH eq '');
    	$LBPATH =~ s/\\/\//g; $LBPATH =~ s/\/[^\/]+$//o;
        unshift(@INC,$LBPATH);
    }
}
use LBCGI;
$query = new LBCGI;
require "data/boardinfo.cgi";
require "wap.pl";
$check = $query -> param('check');
$lid = $query -> param('lid');
&waptitle;
$show.= qq~<card  title="$boardname-��½">~;
if($check eq '1'){
	&check($lid);
	if($inmembername ne ''&&$inmembername ne '����'){
	$pre = $query -> param('pre');
	$mastnum = $query -> param('mastnum');
	$mastnum2 = $query -> param('mastnum2');
	$pre_index = $query -> param('pre_index');
	$topicpre = $query -> param('topicpre');
	open(file,"${lbdir}wap/$lid");
		my $bf=<file>;
		close(file);
		my ($inmembername,$xh2)=split(/\,/,$bf);
		open(file,">${lbdir}wap/$lid");
    print file "$inmembername,$xh2,$pre,$topicpre,$pre_index,$mastnum,$mastnum2";
    close(file);
    $show.= qq~<p>�ɹ��������ã�</p><p><a href='wap.cgi?lid=$lid'>������ҳ</a></p>~;
	}else{
		$show.=qq~<p>��ݺ���ʧ�ܣ������µ�½</p><p><a href='wap_login.cgi'>��½</a></p>~;
	}
	&wapfoot;
}
&check($lid);
$show.=  qq~<p>�������� <br/>\n</p><p>
	�б�����ʾ��<select name="pre" value="$pre">
		<option value="5">5ƪ</option>
		<option value="10">10ƪ</option>
	<option value="20">20ƪ</option>
	<option value="30">30ƪ</option></select>
	</p>
	<p>
	���ӻظ�ÿҳ��ʾ��<select name="topicpre" value="$topicpre">
		<option value="1">1ƪ</option>
		<option value="3">3ƪ</option>
	<option value="10">10ƪ</option>
	<option value="15">15ƪ</option></select>
	</p>
	<p>
	��̳��ҳ��ʾ�����У�<select name="pre_index" value="$pre_index">
		<option value="10">10ƪ</option>
		<option value="16">16ƪ</option>
	<option value="25">25ƪ</option></select>
	</p>
	<p>
	������ʾ���֣�<select name="mastnum" value="$mastnum">
		<option value="50">50��</option>
		<option value="100">100��</option>
	<option value="125">125��</option>
	<option value="500">500��</option></select>
	</p>
	<p>
	����������ʾ���֣�<select name="mastnum2" value="$mastnum2">
		<option value="340">340��</option>
		<option value="500">500��</option>
	<option value="1000">1000��</option>
	<option value="2000">2000��</option></select>
	</p>
	<p>
<anchor>[����]<go href="wap_set.cgi" method="post">
<postfield name="pre" value="\$(pre)"/>
<postfield name="topicpre" value="\$(topicpre)"/>
<postfield name="pre_index" value="\$(pre_index)"/>
<postfield name="mastnum" value="\$(mastnum)"/>
<postfield name="check" value="1"/>
<postfield name="lid" value="$lid"/>
<postfield name="mastnum2" value="\$(mastnum2)"/></go>
</anchor> ~;
$show.=  qq~
</p>~;
&wapfoot;
