#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

package testinfo;
use strict;

use vars qw(@ISA @EXPORT);
require Exporter;
@ISA = qw(Exporter);
@EXPORT = qw(ipwhere osinfo browseinfo);

sub ipwhere
{
	my $ip = shift;
	my @ip = split(/\./, $ip);
	my $ipNum = $ip[0] * 16777216 + $ip[1] * 65536+ $ip[2] * 256 + $ip[3];

	my $file = "${main::lbdir}data/$ip[0].txt";
	if (open(IPF,$file)){
		my $ips=$ip[0]*1000000000+$ip[1]*1000000+$ip[2]*1000+$ip[3];
		my @ipdata=<IPF>;
		close(IPF);
		my ($ip, $i, $ip1, $ip2, $from1, $from2, $fromwhere);
		for ($i=0;$i<@ipdata;$i++) {
			($ip1,$ip2,$from1,$from2)=split(/__/,$ipdata[$i]);
			(my $ipa1,my $ipa2,my $ipa3,my $ipa4)=split(/\./,$ip1);
			(my $ipb1,my $ipb2,my $ipb3,my $ipb4)=split(/\./,$ip2);
			my $ipbegin =$ipa1*1000000000+$ipa2*1000000+$ipa3*1000+$ipa4;
			my $ipend =$ipb1*1000000000+$ipb2*1000000+$ipb3*1000+$ipb4;
			if (($ips<=$ipend)&&($ips>=$ipbegin)) {
				$fromwhere="$from1$from2";
				last;
			}
		}
		$fromwhere =~ s/[\a\f\n\e\0\r\t\)\(\*\+\?]//isg;
		return $fromwhere if($fromwhere) ;
	}

	my $ipfile="${main::lbdir}data/CoralWry.dat";
	$ipfile="${main::lbdir}data/QQWry.Dat" if (!(-e "$ipfile"));
	$ipfile="${main::lbdir}data/QQWry.dat" if (!(-e "$ipfile"));

	return "δ֪����!" if (!(-e "$ipfile"));

	open(FILE, "$ipfile");
	binmode(FILE);
	sysread(FILE, my $ipbegin, 4);
	sysread(FILE, my $ipend, 4);
	$ipbegin = unpack("L", $ipbegin);
	$ipend = unpack("L", $ipend);
	my $ipAllNum = ($ipend - $ipbegin) / 7 + 1;

	my $BeginNum = 0;
	my $EndNum = $ipAllNum;
	
	my $iptime = 0;
	my ($ipAddr1, $ipAddr2, $ip1num, $ip2num);
	while ($ip1num > $ipNum || $ip2num < $ipNum)
	{
		$iptime ++;
		last if ($iptime > 100);
		my $Middle = int(($EndNum + $BeginNum) / 2);

		seek(FILE, $ipbegin + 7 * $Middle, 0);
		read(FILE, my $ipData1, 4);
		$ip1num = unpack("L", $ipData1);
		if ($ip1num > $ipNum)
		{
			$EndNum = $Middle;
			next;
		}

		read(FILE, my $DataSeek, 3);
		$DataSeek = unpack("L", $DataSeek."\0");
		seek(FILE, $DataSeek,0 );
		read(FILE, my $ipData2, 4);
		$ip2num = unpack("L", $ipData2);
		if ($ip2num < $ipNum)
		{
			return 'δ֪����' if ($Middle == $BeginNum);
			$BeginNum = $Middle;
		}
	}

	$/ = "\0";
	read(FILE, my $ipFlag, 1);
	if ($ipFlag eq "\1")
	{
		my $ipSeek;
		read(FILE, $ipSeek, 3);
		$ipSeek = unpack("L", $ipSeek."\0");
		seek(FILE, $ipSeek, 0);
		read(FILE, $ipFlag, 1);
	}
	if ($ipFlag eq "\2")
	{
		my $AddrSeek;
		read(FILE, $AddrSeek, 3);
		read(FILE, $ipFlag, 1);
		if ($ipFlag eq "\2")
		{
			my $AddrSeek2;
			read(FILE, $AddrSeek2, 3);
			$AddrSeek2 = unpack("L", $AddrSeek2."\0");
			seek(FILE, $AddrSeek2, 0);
		}
		else
		{
			seek(FILE, -1, 1);
		}
		$ipAddr2 = <FILE>;
		$AddrSeek = unpack("L", $AddrSeek."\0");
		seek(FILE, $AddrSeek, 0);
		$ipAddr1 = <FILE>;
	}
	else
	{
		seek(FILE, -1, 1);
		$ipAddr1 = <FILE>;
		read(FILE, $ipFlag, 1);
		if($ipFlag eq "\2")
		{
			my $AddrSeek2;
			read(FILE, $AddrSeek2, 3);
			$AddrSeek2 = unpack("L", $AddrSeek2."\0");
			seek(FILE, $AddrSeek2, 0);
		}
		else
		{
			seek(FILE, -1, 1);
		}
		$ipAddr2 = <FILE>;
	}

	chomp($ipAddr1, $ipAddr2);
	$/ = "\n";
	close(FILE);

	$ipAddr2 = '' if ($ipAddr2 =~ /http/i);
	my $ipaddr = "$ipAddr1 $ipAddr2";
	$ipaddr =~ s/CZ88\.NET//isg;
	$ipaddr =~ s/^\s*//sg;
	$ipaddr =~ s/\s*$//sg;
	$ipaddr = 'δ֪����' if ($ipaddr=~/δ֪|http/i || $ipaddr eq '');
	return $ipaddr;
}

sub osinfo
{
	my $os = "";
	my $Agent = $ENV{"HTTP_USER_AGENT"};

	if ($Agent =~ /Google/i)
	{
		$os = "Google Bot";
	}
	elsif ($Agent =~ /baiduspider/i)
	{
		$os = "BaiDu Spider";
	}
	elsif ($Agent =~ /Lycos/i)
	{
		$os = "Lycos Bot";
	}
	elsif ($Agent =~ /Yahoo! Slurp/i)
	{
		$os = "Yahoo Web Crawler";
	}
	elsif ($Agent =~ /Inktomi/i)
	{
		$os = "Yahoo Seeker";
	}
	elsif ($Agent =~ /yahooseeker/i)
	{
		$os = "Yahoo Seeker";
	}
	elsif ($Agent =~ /MSNBOT/i)
	{
		$os = "MSN Bot";
	}
	elsif ($Agent =~ /InfoSeek/i)
	{
		$os = "InfoSeek Bot";
	}
	elsif ($Agent =~ /win/i && $Agent =~ /95/i)
	{
		$os = "Windows 95";
	}
	elsif ($Agent =~ /win 9x/i && $Agent =~ /4.90/i)
	{
		$os = "Windows Me";
	}
	elsif ($Agent =~ /win/i && $Agent =~ /98/i)
	{
		$os = "Windows 98";
	}
	elsif ($Agent =~ /win/i && $Agent =~ /nt 5\.0/i)
	{
		$os = "Windows 2000";
	}
	elsif ($Agent =~ /win/i && $Agent =~ /nt 5\.1/i)
	{
		if ($Agent =~ /SV1/i) { $os = "Windows XP SP2"; } else { $os = "Windows XP"; }
		
	}
	elsif ($Agent =~ /win/i && $Agent =~ /nt 5\.2/i)
	{
		$os = "Windows 2003";
	}
	elsif ($Agent =~ /win/i && $Agent =~ /nt 6\.0/i)
	{
		$os = "Windows Vista";
	}
	elsif ($Agent =~ /win/i && $Agent =~ /nt/i)
	{
		$os = "Windows NT";
	}
	elsif ($Agent =~ /win/i && $Agent =~ /32/i)
	{
		$os = "Windows 32";
	}
	elsif ($Agent =~ /linux/i)
	{
		$os = "Linux";
	}
	elsif ($Agent =~ /unix/i)
	{
		$os = "Unix";
	}
	elsif ($Agent =~ /sun/i && $Agent =~ /os/i)
	{
		$os = "SunOS";
	}
	elsif ($Agent =~ /ibm/isg && $Agent =~ /os/isg)
	{
		$os = "IBM OS/2";
	}
	elsif ($Agent =~ /Mac/i && $Agent =~ /PC/i)
	{
		$os = "Macintosh";
	}
	elsif ($Agent =~ /FreeBSD/i)
	{
		$os = "FreeBSD";
	}
	elsif ($Agent =~ /PowerPC/i)
	{
		$os = "PowerPC";
	}
	elsif ($Agent =~ /AIX/i)
	{
		$os = "AIX";
	}
	elsif ($Agent =~ /HPUX/i)
	{
		$os = "HPUX";
	}
	elsif ($Agent =~ /NetBSD/i)
	{
		$os = "NetBSD";
	}
	elsif ($Agent =~ /BSD/i)
	{
		$os = "BSD";
	}
	elsif ($Agent =~ /OSF1/i)
	{
		$os = "OSF1";
	}
	elsif ($Agent =~ /IRIX/i)
	{
		$os = "IRIX";
	}
	else
	{
#		$os = "[$Agent]";
		$os = "Unknow";
	}
	$os =~ s/[\a\f\n\e\0\r\t\)\(\*\+\?]//isg;
	return $os;
}

sub browseinfo
{
	my $browser = "";
	my $browserver = "";
	my ($Agent, $Part, $browseinfo);
	$Agent = $ENV{"HTTP_USER_AGENT"};

	if ($Agent =~ /Google/i)
	{
		$browser = "Google Bot";
	}
	elsif ($Agent =~ /baiduspider/i)
	{
		$browser = "BaiDu Spider";
	}
	elsif ($Agent =~ /Lycos/i)
	{
		$browser = "Lycos Bot";
	}
	elsif ($Agent =~ /Yahoo! Slurp/i)
	{
		$browser = "Yahoo Web Crawler";
	}
	elsif ($Agent =~ /Inktomi/i)
	{
		$browser = "Yahoo Seeker";
	}
	elsif ($Agent =~ /yahooseeker/i)
	{
		$browser = "Yahoo Seeker";
	}
	elsif ($Agent =~ /MSNBOT/i)
	{
		$browser = "MSN Bot";
	}
	elsif ($Agent =~ /InfoSeek/i)
	{
		$browser = "InfoSeek Bot";
	}
	elsif ($Agent =~ /Lynx/i)
	{
		$browser = "Lynx";
	}
	elsif ($Agent =~ /MOSAIC/i)
	{
		$browser = "MOSAIC";
	}
	elsif ($Agent =~ /AOL/i)
	{
		$browser = "AOL";
	}
	elsif ($Agent =~ /Lynx/i)
	{
		$browser = "Lynx";
	}
	elsif ($Agent =~ /Opera/i)
	{
		$browser = "Opera";
	}
	elsif ($Agent =~ /JAVA/i)
	{
		$browser = "JAVA";
	}
	elsif ($Agent =~ /MacWeb/i)
	{
		$browser = "MacWeb";
	}
	elsif ($Agent =~ /WebExplorer/i)
	{
		$browser = "WebExplorer";
	}
	elsif ($Agent =~ /OmniWeb/i)
	{
		$browser = "OmniWeb";
	}
	elsif ($Agent =~ /Mozilla/i)
	{
		if ($Agent =~ "MSIE")
		{
			if ($Agent =~ /Maxthon/)
			{
				$browser = "Maxthon";
				$browserver = "";
			}
			elsif ($Agent =~ /MyIE(\d*)/)
			{
				$browserver = $1;
				$browser = "MyIE";
			}
			else
			{
				$Part = (split(/\(/, $Agent))[1];
				$Part = (split(/\;/,$Part))[1];
				$browserver = (split(/ /,$Part))[2];
				$browserver =~ s/([\d\.]+)/$1/isg;
				$browser = "Internet Explorer";
			}
		}
		elsif ($Agent =~ "Opera")
		{
			$Part = (split(/\(/, $Agent))[1];
			$browserver = (split(/\)/, $Part))[1];
			$browserver = (split(/ /,$browserver))[2];
			$browserver =~ s/([\d\.]+)/$1/isg;
			$browser = "Opera";
		}
                elsif ($Agent =~ "Firefox")
                {
                       $browser = "Firefox";
                       $browserver = (split(/Firefox/, $Agent))[1];
                       $browserver =~ s/\///isg;
                }
                elsif ($Agent =~ "Firebird")
                {
                       $browser = "Firebird";
                       $browserver = (split(/Firebird/, $Agent))[1];
                       $browserver =~ s/\///isg;
                }
                elsif ($Agent =~ "Gecko")
                {
                       $browser = "Mozilla";
                       $Part = (split(/\(/, $Agent))[1];
                       $browserver = (split(/\)/, $Part))[0];
                       $browserver = (split(/\:/, $browserver))[-1];
                }
		else
		{
			$Part = (split(/\(/, $Agent))[0];
			$browserver = (split(/\//, $Part))[1];
			$browserver = (split(/ /,$browserver))[0];
			$browserver =~ s/([\d\.]+)/$1/isg;
			$browser = "Netscape Navigator";
		}
	}

	if ($browser ne '')
	{
		$browserver =~ s/[^0-9a\.b]//isg;
		$browserver = &lbhz($browserver, 4) if (length($browserver) > 10);
		$browseinfo = "$browser $browserver";
	}
	else
	{
#		$browseinfo = "[$Agent]";
		$browseinfo = "Unknow";
	}
	$browseinfo =~ s/[\a\f\n\e\0\r\t\)\(\*\+\?]//isg;
        $browseinfo = substr($browseinfo, 0, 28) if (length($browseinfo) > 28);
	return $browseinfo;
}
1;