#!/usr/bin/perl
#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

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
$LBCGI::POST_MAX=500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "userratinglog.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

$action        = $query -> param("action");
$action        = &cleaninput("$action");


$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&admintitle;
            

if ($action eq "process") {
        
        &getmember("$inmembername","no");
        
                if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) { 
           $filetoopen = "$lbdir" . "data/userratinglog.cgi";

                open (FILE, "$filetoopen");
                @baddel = <FILE>;
                close (FILE);
		$baddels = @baddel;
		
		if ($baddels > 100) { $baddels = 100; }

                open (FILE, ">$filetoopen");
                for ($i=0;$i<$baddels;$i++) {
                    $j=$i-$baddels;
                    $info = $baddel[$j];
                    chomp $info;
                    print FILE "$info\n";
                }
                close (FILE);

           print qq~
           <tr><td bgcolor=#2159C9><font color=#FFFFFF>
		<b>��ӭ������̳�������� / ɾ���û�����������־</b>
		</td></tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center>
		<font color=#333333><b>�ļ�ɾ��������־</b>
		</td></tr>
		<tr><td align=center><br><br>�������100����¼���������ڵ��û�����������־��¼�Ѿ�ɾ��!</td></tr>
           ~;
         
                }
		else {
           print qq~
           <tr><td bgcolor=#2159C9><font color=#FFFFFF>
		<b>��ӭ������̳�������� / ɾ���û�����������־</b>
		</td></tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center>
		<font color=#333333><b>�ļ�ɾ��������־</b>
		</td></tr>
		<tr><td align=center><br><br>�ܰ�����Ȩɾ����־!</td></tr>
           ~;
		}
        
        }
        
    else {
        
        &getmember("$inmembername","no");
        
        if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

                $filetoopen = "$lbdir" . "data/userratinglog.cgi";
                open (FILE, "$filetoopen");
                @baddel = <FILE>;
                close (FILE);

		my $key = $query->param('key');
		my $type = $query->param('type');
		if ($key ne "")
		{
			if ($type eq "time")
			{
				my ($begin, $end);
				for ($begin = 0; $begin < @baddel; $begin++)
				{
					my ($temp1, $temp2, $temp3, $temptime, $temp4, $temp5, $temp6) = split(/\t/, $baddel[$begin]);
					$temptime = &shortdate($temptime + $timezone * 3600 + $timedifferencevalue * 3600);
					last if ($key eq $temptime);
				}
				for ($end = @baddel - 1; $end >= $begin - 1; $end--)
				{
					my ($temp1, $temp2, $temp3, $temptime, $temp4, $temp5, $temp6) = split(/\t/, $baddel[$end]);
					$temptime = &shortdate($temptime + $timezone * 3600 + $timedifferencevalue * 3600);
					last if ($key eq $temptime);
				}
				if ($begin > $end)
				{
					undef(@baddel);
				}
				else
				{
					@baddel = @baddel[$begin..$end];
				}
			}
			elsif ($type eq "target")
			{
				@baddel = grep(/^$key\t/i, @baddel);
			}
			else
			{
				@baddel = grep(/^.+\t$key\t.+\t.+\t.+\t.+\t.+$/i, @baddel);
			}
		}
                $page = $query->param('page');
                $page = 1 unless($page);
		my $allnum = @baddel;
		my $temp = $allnum / 12;
		my $allpages = int($temp);
		$allpages++ if ($allpages != $temp);
		$page = 1 if ($page < 1);
		$page = $allpages if ($page > $allpages);
		my $showpage = "";
		if (!$allpages)
		{
			$showpage .= "��ǰû�м�¼";
		}
		elsif ($allpages == 1)
		{
			$showpage .= "��ǰ��¼ֻ�� 1 ҳ";
		}
		else
		{
			$showpage .= qq~��¼�� <b>$allpages</b> ҳ ~;
			$i = $page - 1;
			$showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();" title="��һҳ"><<</span> ~ if ($i > 0);
			$showpage .= "[ ";
			$i = $page - 3;
			$showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();">��</span> ~ if ($i > 0);
			$i++;
			$showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();">$i</span> ~ if ($i > 0);
			$i++;
			$showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();">$i</span> ~ if ($i > 0);
			$i++;
			$showpage .= qq~<font color=#990000>$i</font> ~;
			$i++;
			$showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();">$i</span> ~ if ($i <= $allpages);
			$i++;
			$showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();">$i</span> ~ if ($i <= $allpages);
			$i++;
			$showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();">��</span> ~ if ($i <= $allpages);
			$showpage .= "] ";
			$i = $page + 1;
			$showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();" title="��һҳ">>></span> ~ if ($i <= $allpages);
		}
                
                print qq(
                <tr><td bgcolor=#2159C9 colspan=8><font color=#FFFFFF>
		<b>��ӭ������̳�������� / �û��������ֲ�����־</b>
		</td></tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=8>
		<font color=#333333><b>�û��������ֲ�����־</b>
		</td></tr>
		<tr><td>����</td><td>����</td><td>������</td><td>��Ӧ����</td><td>IP ��ַ</td><td>���� IP</td><td>����ʱ��</td><td>����</td></tr>
		);
		if ($allnum) {
		for ($i = $allnum - $page * 12  + 11; $i >= $allnum - $page * 12 && $i >= 0; $i--) {
		(my $name1, my $name2,my $rate, my $oldtime,my $forum1,my $topic1, my $ip, my $proxy, my $reson) = split(/\t/,$baddel[$i]);
    		$oldtime = $oldtime + ($timedifferencevalue*3600) + ($timezone*3600);
    		$oldtime = &dateformatshort($oldtime);
    		chomp $reson;
    		chomp $proxy;
    		$reson = "��" if ($reson eq "");
		print qq~
		<tr><td>$name1</td><td>$rate</td><td>$name2</td><td><a href=topic.cgi?forum=$forum1&topic=$topic1 target=_blank>����</a></td><td>$ip</td><td>$proxy</td><td>$oldtime</td><td><span title="����:$reson">����</span></td></tr>
		~;
		   }
		}
                $tempoutput = qq~
                <form name=MAINFORM action=$thisprog method=POST><td bgcolor=#EEEEEE valign=middle colspan=3><br>
		<input type=hidden name=page value=$page><select name=type><option value="name">��������</option><option value="target">������</option><option value="time">���ض�����</option></select> <input name=key type=text size=12 value=$key> <input type=submit value="��Ѱ">
		</td></form>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=3><br>
		$showpage
		</td>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=2><br>
		<font color=#333333><b><a href=$thisprog?action=process OnClick="return confirm('Ϊ�˰�ȫ���˲������ᱣ�����100����¼�ġ�\\n���Ҫ����û�����������־ô��');">����û�����������־</a></b>
		</td></tr>
                ~;
		$tempoutput =~ s/<option value="$type">/<option value="$type" selected>/g;
		print $tempoutput;
                }
                else {
                    &adminlogin;
                    }
        }
print qq~</td></tr></table></body></html>~;
exit;
