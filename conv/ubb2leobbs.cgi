#!/usr/bin/perl

################################
# UBB --> LeoBBS �û�����ת����#
################################

$ubbmember    = "/path/to/UBB members dir/";   	# ���� UBB �û��������ڵ�Ŀ¼�ľ���·�������Ҫ��© / ��
$leobbsmember = "/path/to/LeoBBS members dir/"; # ������ LeoBBS �û��������ڵ�Ŀ¼�ľ���·�������Ҫ��© /  ��ע������ 777 ���ԡ�

### ����㲻�� CGI�����²�����ǧ��Ҫ�޸ģ�
$ending = ".cgi"; 		# LeoBBS ���û������ļ���׺Ϊ .cgi
$membernumber = 00000001;	# UBB �û���ʼ���
$totlenumber = 0;		# �û������� 0
$nowtime = time;
print "Content-type: text/html\n\n";
print "UBB --> LeoBBS �û�����ת����<BR><BR>\n";
while ($membernumber < 100000)    {
   if ($membernumber < 10) 	 { $membernumber = "0000000$membernumber"; }
   elsif ($membernumber < 100)   { $membernumber = "000000$membernumber";  }
   elsif ($membernumber < 1000)  { $membernumber = "00000$membernumber";   }
   elsif ($membernumber < 10000) { $membernumber = "0000$membernumber";   }
   elsif ($membernumber < 100000){ $membernumber = "000$membernumber";   }
   if (open(FILE,"$ubbmember$membernumber$ending")){
      @ubbmem = <FILE>;
      close(FILE);
      print "��ȡ�û��ļ��� $ubbmember$membernumber$ending<BR>\n";
      for ($i=0;$i<=14;$i++) { chop (@ubbmem[$i]); }
      $name = "@ubbmem[0]";
      print "��ȡ�û����� $name<BR>\n";
      $realname = $name;
      $name =~ s/ /_/gi;
      $name =~ tr/A-Z/a-z/;
      $name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\=\+\\\[\]\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
      $filetocheck = "$leobbsmember" . "$name$ending";
      if (-e $filetocheck) { print "�û� $realname �Ѿ����ڣ�����ת����"; next; }
      open(IBMEMBER,">$leobbsmember$name$ending");
      print IBMEMBER "$realname\t@ubbmem[1]\tMember\tme\t@ubbmem[7]\t@ubbmem[2]\t@ubbmem[11]\txxx.xxx.xxx.xxx\t@ubbmem[3]\t\t@ubbmem[13]\t@ubbmem[6]\t@ubbmem[9]\t$nowtime\tNot Posted\t@ubbmem[12]\t\t\t\t\t\t\t\n";
      close(IBMEMBER);
      print "�û� $realname �Ѿ��ɹ�ת���� LeoBBS �û��ˣ�<BR><BR>";
      $totlenumber ++;
   }
   $membernumber = $membernumber+1;
}
print "�ܹ�ת���� $totlenumber ���û���<BR><BR>\n";
exit;
