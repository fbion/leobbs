#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

sub dosalepost {
	    require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
    	    my $postno = $rn;
            my $isbuyer = "";
            my $allbuyer = "";
            my $allbuyerno = "";
            undef @allbuyer;
            if (open(FILE, "${lbdir}$saledir/$inforum\_$intopic\_$postno.cgi")) {
                my $allbuyer = <FILE>;
                close(FILE);
                chomp $allbuyer;
		$allbuyer =~ s/\t\t/\t/isg;
                $allbuyer =~ s/\t$//gi;
                $allbuyer =~ s/^\t//gi;
		@allbuyer = split(/\t/, $allbuyer);
		$allbuyerno = @allbuyer;
	        $allbuyer = "\t$allbuyer\t";
		$isbuyer="yes" if ($allbuyer =~ /\t$inmembername\t/i);
            }
            $allbuyerno = 0 if (($allbuyerno < 0)||($allbuyerno eq ""));
            { @allexege = ($$post =~ /\[buyexege\].*?\[\/buyexege\]/ig); }
            unless ((lc($inmembername) eq lc($membername))||($mymembercode eq "ad")||($mymembercode eq 'smo')||($myinmembmod eq "yes")||($isbuyer eq "yes")) {
                $$post=qq~<FONT COLOR=$fonthighlight><B>[Sale Post: Money $1]</B></FONT><BR>  <BR><FONT COLOR=$posternamecolor>[�鿴���������Ҫ <b>$1</b> $moneyname��Ŀǰ���� <B>$allbuyerno</B> �˹���]</FONT><BR><br><script>function salesubmitonce(theform){if (document.all||document.getElementById){for (i=0;i<theform.length;i++){ var tempobj=theform.elements[i]; if(tempobj.type.toLowerCase()=="submit"||tempobj.type.toLowerCase()=="reset") { tempobj.disabled=true; }}}}</script>
                <FORM action=buypost.cgi method=post onSubmit="salesubmitonce(this)"><input name=inforum type=hidden value=$inforum><input name=intopic type=hidden value=$intopic><input name=postnumber type=hidden value=$postno><input name=salemembername type=hidden value="$membername"><input name=moneynumber type=hidden value=$1><INPUT name=B1 type=submit value="����ݡ��������Ҹ�Ǯ"></form><BR> ~;
                $$post .= join ('<BR>', @allexege);
                $addme="��������!<br><br>" if ($addme);
	    } else {
	    	$buyeroutput = "";
	    	if ((lc($inmembername) eq lc($membername))||($mymembercode eq "ad")||($mymembercode eq 'smo')||($myinmembmod eq "yes")) {
                    if ($allbuyerno > 0 ) {
	                $buyeroutput = qq~<SCRIPT LANGUAGE="JavaScript">function surfto(list) { var myindex1  = list.selectedIndex; if (myindex1 != 0 & myindex1 != 1) { var newwindow = list.options[myindex1].value; var msgwindow = window.open("profile.cgi?action=show&member=" + newwindow,"",""); } }</SCRIPT><img src=$imagesurl/images/team2.gif width=19 height=19 align=absmiddle><select onchange="surfto(this)">
<option>����������</option><option>------------</option>
~;
	                foreach (@allbuyer) {
	                    chomp $_;
	                    next if ($_ eq "");
	                    my $cleanedmodname = $_;
	                    $cleanedmodname =~ s/ /\_/g;
	                    $cleanedmodname =~ tr/A-Z/a-z/;
	                    $cleanedmodname = uri_escape($cleanedmodname);
    	                    $buyeroutput .= qq~<option value="$cleanedmodname">$_</option>~;
	                }
	                $buyeroutput .= qq~</select></form><BR>\n~;
                    }
                }
	        $$post=~s/LBSALE\[(.*?)\]LBSALE/$buyeroutput<font color=$fonthighlight>�������ۼ� <B>$1<\/B> $moneyname��Ŀǰ���� <B>$allbuyerno<\/B> �˹���<\/font><br><br>/sg;   
	    }
	    $$post =~ s/\[buyexege\](.*?)\[\/buyexege\]/<blockquote><font color=$posternamecolor>��������ע�����ݣ� <hr noshade size=1>$1<hr noshade size=1><\/blockquote><\/font>/g;
	}
1;
