#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

		if ($firstcome ne 'yes')
		{
			if (@onlinefr)
			{
				my $onlinefriend = join('����', @onlinefr);
				$onlinepopup = "��������Щ���Ѹո������ˣ�<p>$onlinefriend";
				require 'onlinepop.pl';
			}
			$onlineprompt = uri_escape($onlineprompt);
			$output .= qq~<script>var exp = new Date(); exp.setTime(exp.getTime() + ($membergone*60*1000)); document.cookie="onlineprompt=$onlineprompt; expires=" + exp.toGMTString();</script>~;
		}
		else
		{
			my $temptempuser = $tempusername;
			$temptempuser =~ s/ /\_/g;
			$temptempuser =~ tr/A-Z/a-z/;
			$temptempuser =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\|\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
			if (open(FRD, "${lbdir}memfriend/$temptempuser.cgi"))
			{
				sysread(FRD, my $friendlist, (stat(FRD))[7]);
				close(FRD);
				$friendlist =~ s/\r//isg;
				my @friendlist = split($/, $friendlist);
				my @noonlinefr = ();
				my @onlinefr = ();
				foreach my $friend (@friendlist)
				{
					$friend =~ s/^����������//;
					$friend =~ s/[\r\n]*$//;
					next if ($friend eq '');
					if (grep(/^$friend\t/i, @onlinedata) > 0)
					{
						push(@onlinefr, $friend);
					}
					else
					{
						push(@noonlinefr, $friend);
					}
				}
				if (@onlinefr)
				{
					my $onlinefriend = join('����', @onlinefr);
					$onlinepopup = "��������Щ�����������ϣ�<p>$onlinefriend";
					require 'onlinepop.pl';
				}
				if (@noonlinefr)
				{
					my $onlineprompt = join(',', @noonlinefr);
					$onlineprompt = uri_escape($onlineprompt);
					$output .= qq~<script>var exp = new Date(); exp.setTime(exp.getTime() + ($membergone*60*1000)); document.cookie="onlineprompt=,$onlineprompt,; expires=" + exp.toGMTString();</script>~;
				}
			}
		}
1;
