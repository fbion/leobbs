#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

    if ("$userregistered" eq "no") {&error("�޸�����&û�д��û�����"); }
    if ("$oldpassword" eq "") {&error("�޸�����&��������ԭ������̳���룡"); }
    if ($oldpassword ne "") {
        eval {$oldpassword = md5_hex($oldpassword);};
        if ($@) {eval('use Digest::MD5 qw(md5_hex);$oldpassword = md5_hex($oldpassword);');}
        unless ($@) {$oldpassword = "lEO$oldpassword";}
    }
    if ("$oldpassword" ne "$password") {&error("�޸�����&��̳�������"); }

    $nowpassword            = $query -> param('nowpassword');
    $newpassword1           = $query -> param('newpassword1');
    $newpassword2           = $query -> param('newpassword2');
    $newshowemail           = $query -> param('newshowemail');
    $newhomepage            = $query -> param('newhomepage');
    $newoicqnumber          = $query -> param('newoicqnumber');
    $newicqnumber           = $query -> param('newicqnumber');
    $newlocation            = $query -> param('newlocation');
    $newinterests           = $query -> param('newinterests');
    $newtimedifference      = $query -> param('newtimedifference');
    $newpersonalavatar      = $query -> param('newpersonalavatar');
    $newpersonalwidth       = $query -> param('newpersonalwidth');
    $newpersonalheight      = $query -> param('newpersonalheight');
    $newemailaddress        = $query -> param('newemailaddress');
    $newmembertitle         = $query -> param('newmembertitle');
    $newjhmp                = $query -> param('newjhmp');
    $inuserflag		    = $query -> param('userflag');
    $inuserxz		    = $query -> param('userxz');
    $inusersx		    = $query -> param('usersx');
    $newyear                = $query -> param('newyear');
    $newmonth               = $query -> param('newmonth');
    $newday                 = $query -> param('newday');
    $newsex                 = $query -> param('newsex');
    $neweducation           = $query -> param('neweducation');
    $newmarry               = $query -> param('newmarry');
    $newwork                = $query -> param('newwork');
    $newsignature           = $query -> param('newsignature');
    $inuseravatar           = $query -> param('useravatar');
    $newuserquestion          = &cleanarea($query -> param('getpassq')."|".$query -> param('getpassa')); 

    $newsignature           = &unHTML("$newsignature");

    $newpassword1           = &cleanarea("$newpassword1");
    $newpassword2           = &cleanarea("$newpassword2");
    $newshowemail           = &cleanarea("$newshowemail");
    $newhomepage            = &cleanarea("$newhomepage");
    $newoicqnumber          = &cleanarea("$newoicqnumber");
    $newicqnumber           = &cleanarea("$newicqnumber");
    $newlocation            = &cleanarea("$newlocation");
    $newinterests           = &cleanarea("$newinterests");
    $newtimedifference      = &cleanarea("$newtimedifference");
    $newpersonalavatar      = &cleanarea("$newpersonalavatar");
    $newpersonalwidth       = &cleanarea("$newpersonalwidth");
    $newpersonalheight      = &cleanarea("$newpersonalheight");
    $newemailaddress        = &cleanarea("$newemailaddress");
    $newmembertitle         = &cleanarea("$newmembertitle");
    $newjhmp                = &cleanarea("$newjhmp");
    $inuserflag		    = &cleanarea("$inuserflag");
    $inuserxz		    = &cleanarea("$inuserxz");
    $inusersx		    = &cleanarea("$inusersx");
    $newyear                = &cleanarea("$newyear");
    $newmonth               = &cleanarea("$newmonth");
    $newday                 = &cleanarea("$newday");
    $neweducation           = &cleanarea("$neweducation");
    $newmarry               = &cleanarea("$newmarry");
    $newwork                = &cleanarea("$newwork");
    $newsignature           = &cleanarea("$newsignature");
    $inuseravatar           = &cleanarea("$inuseravatar");
    $newsex                 = &cleanarea("$newsex");
    $newoldsex              = $query -> param('oldsex');
    $newoldsex              = &cleanarea("$newoldsex");

    if ($userface ne '') {
        if (($newoldsex ne "no")&&($newsex ne $newoldsex)) {
	    &error("����&�������Ѿ�ʹ���������������ԣ�����Ա�Ŀǰ���ܸ��ģ�<BR>���ʵ����Ҫ�����Ա���ô����ȥ��������ĸ��������У�����������ϣ�Ȼ�����ԣ�");
        }
    }

    if ($newsignature) {
        $newsignature =~ s/\t//g;
        $newsignature =~ s/\r//g;
        $newsignature =~ s/  / /g;
        $newsignature =~ s/\&amp;nbsp;/\&nbsp;/g;
        $newsignature =~ s/\n\n/\n\&nbsp;\n/isg;
        $newsignature =~ s/\n/\[br\]/isg;
        $newsignature =~ s/\[br\]\[br\]/\[br\]\&nbsp;\[br\]/isg;
    }

    if ($newinterests) {
        $newinterests =~ s/<P>/<BR>/ig;
        $newinterests =~ s/<BR><BR>/<BR>/ig;
    }

    @testsig = split(/\[br\]/,$newsignature);
    $siglines = @testsig;
    &error("��̳������ʾ����ʹ�&��̳������ʾ����ʹ��У��������зǷ��ַ�����������ʺʹ𰸣�") if ($query -> param('getpassq') =~ /[\||\a|\f|\n|\e|\0|\r|\t]/ || $query -> param('getpassa') =~ /[\||\a|\f|\n|\e|\0|\r|\t]/);
    if(length($newlocation)>16) { &error("�޸�����&���Ե����������벻Ҫ����16���ַ���8�����֣���"); }
    if ($siglines > $maxsignline) { &error("�޸�����&�Բ���������ǩ����ֻ������ $maxsignline �У�"); }
    if (length($newsignature) > $maxsignlegth) { &error("�޸�����&�Բ���ǩ�����ܳ��� $maxsignlegth �ַ���"); }
    if($newpassword1 =~ /[^a-zA-Z0-9]/)     { &error("�޸�����&��̳����ֻ�����Сд��ĸ�����ֵ���ϣ���"); }
    if($newpassword1 =~ /^lEO/)     { &error("�û�ע��&��̳���벻������ lEO ��ͷ�����������"); }

    if(length($newmembertitle)>21) { &error("�޸�����&����ͷ�ι������벻Ҫ����20���ַ���10�����֣���"); }
    $newmembertitle =~ s/\t//isg;
    if(length($newjhmp)>21) { &error("�޸�����&�������ɹ������벻Ҫ����20���ַ���10�����֣���"); }
    $newjhmp =~ s/\t//isg;

    @testins = split(/\<br\>/,$newinterests);
    $inslines = @testins;
    if ($inslines > $maxinsline) { &error("�û�ע��&�Բ��𣬸��˼��ֻ������ $maxinsline �У�"); }

    if (length($newinterests) > $maxinslegth) {&error("�޸�����&�Բ��𣬸��˼�鲻�ܳ��� $maxinslegth �ַ���"); }

    $newyear =~ s/\D//g;

    $newyear = "19$newyear"if ($newyear < 1900 && $newyear ne "");
    my (undef, undef, undef, undef, undef, $yeartemp, undef, undef) = localtime(time + $timezone * 3600);
    $yeartemp = 1900 + $yeartemp if ($yeartemp < 1900);

    if ($newyear ne "") {
        &error("�û�ע��&����ȷ������ĳ�����ݣ�") if ($newyear <= 1900 || $newyear >= $yeartemp - 3);
    }

    if (($newyear eq "")||($newmonth eq "")||($newday eq "")) {
    	$newyear  = "";
    	$newmonth = "";
    	$newday   = "";
    }
    $newborn = "$newyear/$newmonth/$newday";

    if ($newborn ne "//") { #��ʼ�Զ��ж�����
    	if ($newmonth eq "01") {
    	    if (($newday >= 1)&&($newday <=19)) {
    	        $inuserxz = "z10";
    	    }
    	    else {
    	        $inuserxz = "z11";
    	    }
    	}
        elsif ($newmonth eq "02") {
    	    if (($newday >= 1)&&($newday <=18)) {
    	        $inuserxz = "z11";
    	    }
    	    else {
    	        $inuserxz = "z12";
    	    }
        }
        elsif ($newmonth eq "03") {
    	    if (($newday >= 1)&&($newday <=20)) {
    	        $inuserxz = "z12";
    	    }
    	    else {
    	        $inuserxz = "z1";
    	    }

        }
        elsif ($newmonth eq "04") {
    	    if (($newday >= 1)&&($newday <=19)) {
    	        $inuserxz = "z1";
    	    }
    	    else {
    	        $inuserxz = "z2";
    	    }
        }
        elsif ($newmonth eq "05") {
    	    if (($newday >= 1)&&($newday <=20)) {
    	        $inuserxz = "z2";
    	    }
    	    else {
    	        $inuserxz = "z3";
    	    }
        }
        elsif ($newmonth eq "06") {
    	    if (($newday >= 1)&&($newday <=21)) {
    	        $inuserxz = "z3";
    	    }
    	    else {
    	        $inuserxz = "z4";
    	    }
        }
        elsif ($newmonth eq "07") {
    	    if (($newday >= 1)&&($newday <=22)) {
    	        $inuserxz = "z4";
    	    }
    	    else {
    	        $inuserxz = "z5";
    	    }
        }
        elsif ($newmonth eq "08") {
    	    if (($newday >= 1)&&($newday <=22)) {
    	        $inuserxz = "z5";
    	    }
    	    else {
    	        $inuserxz = "z6";
    	    }
        }
        elsif ($newmonth eq "09") {
    	    if (($newday >= 1)&&($newday <=22)) {
    	        $inuserxz = "z6";
    	    }
    	    else {
    	        $inuserxz = "z7";
    	    }
        }
        elsif ($newmonth eq "10") {
    	    if (($newday >= 1)&&($newday <=23)) {
    	        $inuserxz = "z7";
    	    }
    	    else {
    	        $inuserxz = "z8";
    	    }
        }
        elsif ($newmonth eq "11") {
    	    if (($newday >= 1)&&($newday <=21)) {
    	        $inuserxz = "z8";
    	    }
    	    else {
    	        $inuserxz = "z9";
    	    }
        }
        elsif ($newmonth eq "12") {
    	    if (($newday >= 1)&&($newday <=21)) {
    	        $inuserxz = "z9";
    	    }
    	    else {
    	        $inuserxz = "z10";
    	    }
        }

    }

    if (($newpersonalavatar)&&($newpersonalwidth)&&($newpersonalheight)) {
        if ($newpersonalavatar !~ /^http:\/\/[\w\W]+\.[\w\W]+$/) {
            &error("�û�ע��&�Զ���ͷ��� URL ��ַ�����⣡");
        }
        if (($newpersonalavatar !~ /\.gif$/i)&&($newpersonalavatar !~ /\.jpg$/isg)&&($newpersonalavatar !~ /\.png$/isg)&&($newpersonalavatar !~ /\.bmp$/isg)&&($newpersonalavatar !~ /\.swf$/isg)) {
            &error("�û�ע��&�Զ���ͷ�����Ϊ PNG��GIF��JPG��BMP��SWF ��ʽ") ;
        }
        if (($newpersonalwidth < 20)||($newpersonalwidth > $maxposticonwidth)) {
           &error("�û�ע��&�Բ�������д���Զ���ͼ���ȱ����� 20 -- $maxposticonwidth ����֮�䣡");
        }
        if (($newpersonalheight < 20)||($newpersonalheight > $maxposticonheight)) {
           &error("�û�ע��&�Բ�������д���Զ���ͼ��߶ȱ����� 20 -- $maxposticonheight ����֮�䣡");
        }
        $inuseravatar = "noavatar";
        $newpersonalavatar =~ s/${imagesurl}/\$imagesurl/o;
    }
    else {
    	if ($addme){
    	    $newpersonalavatar="";
    	}else{
    	    $newpersonalavatar=""; $newpersonalwidth=""; $newpersonalheight="";
    	}
    }

    $newemailaddress = lc($newemailaddress);
    my $allow_eamil_file = "$lbdir" . "data/allow_email.cgi";
    if(-e $allow_eamil_file) {
	open(AEFILE,$allow_eamil_file);
	my $allowtype = <AEFILE>;
	my $allowmail = <AEFILE>;
	close(AEFILE);
	chomp $allowtype;
	chomp $allowmail;
	my $check_result = 0;
	my $get_email_server = substr($newemailaddress,rindex($newemailaddress,'@')+1);
	if($allowmail ne ""){
	    my @allowmail = split(/\t/,$allowmail);
	    chomp @allowmail;
	    foreach (@allowmail) {
		next if($_ eq "");
		if(lc($get_email_server) eq lc($_)) {
		    $check_result = 1;
		    last;
		}
	    }
	    if ($allowtype eq "allow") {
		if($check_result == 0) {
		    &error("�޸�����&����ʹ��ָ�������䣡<a href=\"javascript:openScript('dispemail.cgi',200,300);\">[�б�]</a>");
		}
	    } else {
		if($check_result == 1){
		    &error("�޸�����&���ṩ�����䱻��ֹʹ�ã�<a href=\"javascript:openScript('dispemail.cgi',200,300);\">[�б�]</a>");
		}
	    }
	}
    }
    if ($newemailaddress eq "") { $blankfields = "yes"; }
    if ($newpassword1 ne $newpassword2)  {&error("�޸�����&�������������̳���벻��ͬ������㲻���޸���̳���룬�뱣��������Ϊ�գ�"); }

    if (($newpassword1 ne "")&&($newpassword2 ne "")) {
        if(length($newpassword1)<8) { &error("�û�ע��&��̳����̫���ˣ����������̳������� 8 λ���ϣ�"); }
#       if ($newpassword1 =~ /^[0-9]+$/) { &error("�û�ע��&��̳�����벻Ҫȫ��Ϊ���֣��������"); }
        $newpassword = $newpassword1;
	if ($newpassword ne "") {
	    eval {$newpassword = md5_hex($newpassword);};
	    if ($@) {eval('use Digest::MD5 qw(md5_hex);$newpassword = md5_hex($newpassword);');}
	    unless ($@) {$newpassword = "lEO$newpassword";}
	}
    }
    else { $newpassword = $oldpassword; }

    if ($blankfields) {
       &error("�޸�����&�������û������ʼ���ַ����Щ�Ǳ���ģ�");
    }

    $memberfiletitle = $inmembername;
    $memberfiletitle =~ s/ /\_/isg;
    $memberfiletitle =~ tr/A-Z/a-z/;
    $memberfiletitletemp = unpack("H*","$memberfiletitle");
    
    my $temp = &dofilter("$newsignature\t$newlocation\t$membertitle\t$newinterests\t$jhmp\t$newhomepage");
    ($newsignature,$newlocation,$membertitle,$newinterests,$jhmp,$newhomepage) = split(/\t/,$temp);
    $newhomepage =~ s/[\ \a\f\n\e\0\r\t\|\$\@]//isg;
    $newhomepage =~ s/ARGV//isg;
    $newhomepage =~ s/system//isg;
    
    if ($addme) {
            unlink ("${imagesdir}usravatars/$memberfiletitle.gif");
            unlink ("${imagesdir}usravatars/$memberfiletitle.png");
            unlink ("${imagesdir}usravatars/$memberfiletitle.jpg");
            unlink ("${imagesdir}usravatars/$memberfiletitle.swf");
            unlink ("${imagesdir}usravatars/$memberfiletitle.bmp");
            unlink ("${imagesdir}usravatars/$memberfiletitletemp.gif");
            unlink ("${imagesdir}usravatars/$memberfiletitletemp.png");
            unlink ("${imagesdir}usravatars/$memberfiletitletemp.jpg");
            unlink ("${imagesdir}usravatars/$memberfiletitletemp.swf");
            unlink ("${imagesdir}usravatars/$memberfiletitletemp.bmp");


          my ($filename) = $addme =~ m|([^/:\\]+)$|; #ע��,��ȡ�ļ����ֵ���ʽ�仯

          my @filename = split(/\./,$filename); #ע��
          my $up_name = $filename[0];
          $fileexp = $filename[-1];
          $fileexp = lc($fileexp);


        $fileexp = ($fileexp =~ /jpe?g$/i) ? 'jpg'
                  :($fileexp =~ /gif$/i)  ? 'gif'
                  :($fileexp =~ /png$/i)  ? 'png'
                  :($fileexp =~ /swf$/i)  ? 'swf'
                  :($fileexp =~ /bmp$/i)  ? 'bmp'
                  :undef;
        $maxuploadava = 200 if (($maxuploadava eq "")||($maxuploadava < 1));
        if (($fileexp eq "swf")&&($flashavatar ne "yes")) {
            &error("��֧�������ϴ���ͼƬ��������ѡ��&��֧�� GIF��JPG��PNG��BMP ����!");
        }

        if (!defined $fileexp) {
            &error("��֧�������ϴ���ͼƬ��������ѡ��&��֧�� GIF��JPG��PNG��BMP��SWF ����!");
        }

        my $filesize=0;
        my $buffer;
        open (FILE,">${imagesdir}usravatars/$memberfiletitletemp.$fileexp");
        binmode (FILE);
        while (((read($addme,$buffer,4096)))&&!(($filesize>$maxupload)&&($membercode ne "ad"))) {
               print FILE $buffer;
               $filesize=$filesize+4;
         }
        close (FILE);
        close ($addme); #ע��

        if ($fileexp eq "gif"||$fileexp eq "jpg"||$fileexp eq "bmp"||$fileexp eq "jpeg"||$fileexp eq "png") {
	  eval("use Image::Info qw(image_info);"); 
	  if ($@ eq "") { 
    	    my $info = image_info("${imagesdir}usravatars/$memberfiletitletemp.$fileexp");
	    if ($info->{error} eq "Unrecognized file format"){
                unlink ("${imagesdir}usravatars/$memberfiletitletemp.$fileexp");
                &error("�ϴ�����&�ϴ��ļ�����ͼƬ�ļ������ϴ���׼��ͼƬ�ļ���");
            }
            if ($newpersonalwidth eq "" || $newpersonalwidth eq 0) {
            	if ($info->{width} ne "") { $newpersonalwidth = $info->{width}; }
            	elsif ($info->{ExifImageWidth} ne "") { $newpersonalwidth = $info->{ExifImageWidth}; }
            }
            if ($newpersonalheight eq "" || $newpersonalheight eq 0) {
            	if ($info->{height} ne "") { $newpersonalheight = $info->{height}; }
            	elsif ($info->{ExifImageLength} ne "") { $newpersonalheight = $info->{ExifImageLength}; }
            }
            undef $info;
          }
	}
	if ($filesize>$maxuploadava) {
            unlink ("${imagesdir}usravatars/$memberfiletitletemp.$fileexp");
	    &error("�ϴ�����&�ϴ��ļ���С����$maxuploadava��������ѡ��");
	}
	if (($newpersonalwidth < 20)||($newpersonalwidth > $maxposticonwidth)) { &error("�û�ע��&�Բ�������д���Զ���ͼ����($newpersonalwidth)������ 20 -- $maxposticonwidth ����֮�䣡"); }
        if (($newpersonalheight < 20)||($newpersonalheight > $maxposticonheight)) { &error("�û�ע��&�Բ�������д���Զ���ͼ��߶�($newpersonalheight)������ 20 -- $maxposticonheight ����֮�䣡"); }

	$inuseravatar="noavatar";
	$newpersonalavatar="\$imagesurl/usravatars/$memberfiletitletemp.$fileexp";
    }

    if($newemailaddress !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/) { &error("ע��&Email ��ַ�Ƿ�$newemailaddress��"); }
    $newemailaddress =~ s/[\ \a\f\n\e\0\r\t\`\~\!\#\$\%\^\&\*\(\)\=\+\\\[\]\{\}\;\'\:\"\,\/\<\>\?\|]//isg;

   &getmember("$inmembername");
    
#    &getmember("$inmembername","no");

    if ($newemailaddress ne $emailaddress) {
	my $charone = substr($newemailaddress, 0, 1);
	$charone = lc($charone);
	$charone = ord($charone);
	my $charone1 = substr($emailaddress, 0, 1);
	$charone1 = lc($charone1);
	$charone1 = ord($charone1);

	$/ = "";
	open (MEMFILE, "${lbdir}data/lbemail/$charone.cgi");
	my $allmemberemails = <MEMFILE>;
	close(MEMFILE);
	open (MEMFILE1, "${lbdir}data/lbemail/$charone1.cgi");
	my $allmemberemails1 = <MEMFILE1>;
	close(MEMFILE1);
	$/ = "\n";
	$allmemberemails = "\n$allmemberemails\n";
	chomp($allmemberemails);
	$allmemberemails = "\t$allmemberemails";

	if (($allmemberemails =~ /\n$newemailaddress\t(.+?)\n/i)&&($oneaccountperemail eq "yes")) {
	   &error("�����޸�&�Բ���������� Email �Ѿ���ע���û���<u>$1</u> ʹ����");
	}
	$allmemberemails1 =~ s/$emailaddress\t$inmembername\n//isg;
	open(MEMFILE1, ">${lbdir}data/lbemail/$charone1.cgi");
	print MEMFILE1 "$allmemberemails1";
	close(MEMFILE1);
	open(MEMFILE, ">>${lbdir}data/lbemail/$charone.cgi");
	print MEMFILE "$newemailaddress\t$inmembername\n";
	close(MEMFILE);
   }
   
    if ($newborn ne $born) {
        $filetomakeopen = "${lbdir}data/lbmember3.cgi";
        open (MEMFILE, "$filetomakeopen");
        @allmembers = <MEMFILE>;
        close (MEMFILE);

	if (open (MEMFILE, ">$filetomakeopen")) {
	    $writeborn=0;
            foreach (@allmembers) {
                chomp $_;
                ($user, $no) = split(/\t/,$_);
                if (lc($user) eq lc($inmembername)) {
	            print MEMFILE "$inmembername\t$newborn\t\n" if (($newborn ne "")&&($newborn ne "//"));
	            $writeborn=1;
                } else {
	            print MEMFILE "$_\n";
                }
            }
	    print MEMFILE "$inmembername\t$newborn\t\n" if (($writeborn==0)&&($newborn ne "")&&($newborn ne "//"));
            close (MEMFILE);
	}

	($oyear,$omonth,$oday) = split(/\//,$born);
	if ($omonth ne "") {
	    $omonth = int($omonth);
	    open (MEMFILE, "${lbdir}calendar/borninfo$omonth.cgi");
	    @birthdaydata = <MEMFILE>;
	    close (MEMFILE);

	    if (open (MEMFILE, ">${lbdir}calendar/borninfo$omonth.cgi")) {
                foreach (@birthdaydata) {
                    chomp $_;
                    ($user, $no) = split(/\t/,$_);
                    next if (lc($user) eq lc($inmembername));
	            print MEMFILE "$_\n";
	        }
            }
            close (MEMFILE);
	}

	if (($newborn ne "")&&($newborn ne "//")) {
	    $newmonth = int($newmonth);
	    open (MEMFILE, ">>${lbdir}calendar/borninfo$newmonth.cgi");
	    print MEMFILE "$inmembername\t$newborn\t\n";
	    close (MEMFILE);
	}
    }

    if (($passwordverification eq "yes") && ($emailfunctions ne "off") && ($newemailaddress ne $emailaddress)) {
	$seed = int(myrand(100000));
	$password = crypt($seed, aun);
	$password =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$password =~ s/\.//g;
        $password =~ s/\|//g;
	$newpassword = substr($password, 0, 8);

	$passcookie = cookie(-name => "apasswordcookie", -value => "", -path => "$cookiepath/", -expires => "0");

	eval("use MAILPROG qw(sendmail);");

	$to = $newemailaddress;
	$from = $adminemail_out;
	$subject = "���ı����� $boardname ��ע����ʼ���ַ";

	$message .= "\n";
	$message .= "$homename <br>\n";
	$message .= "$boardurl/leobbs.cgi\n <br><br>\n <br>\n";
	$message .= "------------------------------------<br>\n";
	$message .= "�����û���������̳�������£�\n <br><br>\n";
	$message .= "�û����� $inmembername <br>\n";
	$message .= "����̳���룺 $newpassword\n <br><br>\n <br>\n";
	$message .= "��ע�⣺�û�������̳�������ִ�Сд��\n <br>\n";
	$message .= "------------------------------------<br>\n";

	&sendmail($from, $adminemail_in, $to, $subject, $message);

	if ($newpassword ne "") {
	    eval {$newpassword = md5_hex($newpassword);};
	    if ($@) {eval('use Digest::MD5 qw(md5_hex);$newpassword = md5_hex($newpassword);');}
	    unless ($@) {$newpassword = "lEO$newpassword";}
	}
    }

    if (($editusertitleself eq "post") && ($jifen >= $needpoststitle)) { $editusertitleself = "on"; }
    
    if ($editusertitleself eq "on") {
        $newmembertitle = "Member" if ($newmembertitle eq "");
        $membertitle = $newmembertitle;
    }

    if (($editjhmpself eq "post") && (($numberofposts + $numberofreplys) >= $needpostsjhmp)) { $editjhmpself = "on"; }

    if ($editjhmpself eq "on") {
        $jhmp = $newjhmp;
    }
    elsif ($editjhmpself eq "system") {
	my $jumpfile="$lbdir" . "data/jhmp.cgi";
	open(FILE,$jumpfile);
	my @JUMP=<FILE>;
	close(FILE);
	chomp @JUMP;
	if($membercode eq "ad" || $membercode eq "smo"){
		@JUMP = grep(/^(.+?)\t[1|0]\t/,@JUMP);
	}else{
        	@JUMP1 = grep(/^$jhmp\t0\t/,@JUMP);
		@JUMP = grep(/^(.+?)\t1\t/,@JUMP);
		push(@JUMP,@JUMP1);
	}
	$newjhmp = 1000 unless(@JUMP && -e $jumpfile);
	$newjhmp = (defined $JUMP[$newjhmp])?$newjhmp:1000;
	($JUMP[$newjhmp],my $no) = split(/\t/,$JUMP[$newjhmp]);
	$jhmp = ($newjhmp < 1000)?$JUMP[$newjhmp]:'��������';
    }

    if(($userquestion eq "|")||($userquestion eq "")){ 
	$userquestion = $newuserquestion; 
    }
    
    if (($inmembername ne "")&&($newpassword ne "")) {
	require "dosignlbcode.pl";
	$signature1=&signlbcode($newsignature); 
	$newsignature=$newsignature."aShDFSiod".$signature1;
	my $namenumber = &getnamenumber($memberfiletitle);
	&checkmemfile($memberfiletitle,$namenumber);
	$filetomake = "$lbdir" . "$memdir/$namenumber/$memberfiletitle.cgi";
	&winlock($filetomake) if ($OS_USED eq "Nt");
	if (open(FILE, "+<$filetomake")) {
	    flock(FILE, 2) if ($OS_USED eq "Unix");
	    seek(FILE,0,0);
	    print FILE "$inmembername\t$newpassword\t$membertitle\t$membercode\t$numberofposts|$numberofreplys\t$newemailaddress\t$newshowemail\t$ipaddress\t$newhomepage\t$newoicqnumber\t$newicqnumber\t$newlocation\t$newinterests\t$joineddate\t$lastpostdate\t$newsignature\t$newtimedifference\t$privateforums\t$inuseravatar\t$inuserflag\t$inuserxz\t$inusersx\t$newpersonalavatar\t$newpersonalwidth\t$newpersonalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$newsex\t$neweducation\t$newmarry\t$newwork\t$newborn\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
	    close(FILE);
	}
	if (open(FILE, ">${lbdir}$memdir/old/$memberfiletitle.cgi")) {
	    print FILE "$inmembername\t$newpassword\t$membertitle\t$membercode\t$numberofposts|$numberofreplys\t$newemailaddress\t$newshowemail\t$ipaddress\t$newhomepage\t$newoicqnumber\t$newicqnumber\t$newlocation\t$newinterests\t$joineddate\t$lastpostdate\t$newsignature\t$newtimedifference\t$privateforums\t$inuseravatar\t$inuserflag\t$inuserxz\t$inusersx\t$newpersonalavatar\t$newpersonalwidth\t$newpersonalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$newsex\t$neweducation\t$newmarry\t$newwork\t$newborn\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
	    close(FILE);
	}
	&winunlock($filetomake) if ($OS_USED eq "Nt");
        unlink ("${lbdir}cache/myinfo/$memberfiletitle.pl");
        unlink ("${lbdir}cache/meminfo/$memberfiletitle.pl");
    }

    $previewsig = $signature1;

    if ($newpassword1 ne "") {
	$info = qq~<ul><li><a href="loginout.cgi"><font color=$fonthighlight>��Ϊ���޸�����̳���룬���������µ�¼һ�Σ�</font></a></ul>~;
    } else { $info = qq~<ul><li><a href="leobbs.cgi">������̳��ҳ</a></ul>~; }
	$output .= qq~
<tr><td bgcolor=$titlecolor $catbackpic valign=middle align=center><font color=$fontcolormisc><b>������Ϣ�Ѿ�����</b></font></td></tr>
<tr><td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>
���������$info</td></tr>
<tr><td bgcolor=$miscbackone valign=middle><font color=$postfontcolor>
�����ǩ��Ԥ����<br><hr><br>
$previewsig
<br><hr></font>
</td></tr></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
	if (($passwordverification eq "yes") && ($emailfunctions ne "off") && ($newemailaddress ne $emailaddress)) {
	    $output =~ s/���������/<B>�������޸��� Email��������ֱ���޸ĵ���̳��������Ч�ģ����������̳�����Ѿ�ͨ�� Email ���͸����ˣ�<\/B>/g;
	}
1;
