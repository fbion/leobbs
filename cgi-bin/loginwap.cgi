#!/usr/bin/perl
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
require "bbs.lib.pl"; 
require "wap.pl"; 
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
print "<title>��������ID</title>";
$inmembername   = $query->cookie("amembernamecookie");
$inpassword     = $query->cookie("apasswordcookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ((!$inmembername) or ($inmembername eq "����")) { &error("��ͨ����&���˲��ܽ��в���");}
else {
    &getmember("$inmembername","no");
     if ($inpassword ne $password) {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("��ͨ����&�������û���������������µ�¼��");
     }
    &error("��ͨ����&�û�û�е�¼��ע�ᣡ") if ($userregistered eq "no");
}

$ip = $query->param('ip');
if($ip ne ''){
	FILE:my $x = int(rand(99999999999999));
    $x = substr($x, 2, 9);  
    if(-e "${lbdir}wap/$x"){goto FILE;}
    my $xh2 = $ip;
    open(file,">${lbdir}wap/$x");
    print file "$inmembername,$xh2,$pre,$topicpre,$pre_index,$mastnum,$mastnum2";
    close(file);
    
    open(file,"${lbdir}wap/all.h");
    my @s=<file>;
    close(file);
    
    open(file,">${lbdir}wap/all.h");
    foreach(@s){
    	chomp;
    	my($n,$s)=split(/\,/,$_);
    	if($inmembername eq $n){
    		unlink "${lbdir}wap/$s";
    	}else{print file "$_\n";}
    }
    print file "$inmembername,$x\n";
    close(file);
    print qq~<p>��������IDΪ��$x,����IPΪ��$xh2���벻Ҫй©��������ID���κ��ˣ��������������ҳ��ַ�����ֻ���ǩ(��ǩ��ַ��$boardurl/wap.cgi?lid=$x ������֮������½) �������벻Ҫ������ǩ��</p><p>ע�⣺������IDȫΪ���֡�</p>~;
}else{
print "<form name=post method=post action=loginwap.cgi>�����������ֻ�IP��<br><br>�����ֻ�WAP��$boardurl/wap.cgi���������½������ȡ�ֻ�IP<br><input name=ip value='' type=text><input type=submit value=����Url></form>";
}
exit;