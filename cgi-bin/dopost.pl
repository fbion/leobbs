########################
#
#�ϴ����� By ·��
#
########################

sub upfileonpost #�ύ��ʱ������ʱ�ļ������ʵĵط�������������
{
  my ($inpost,$inforum,$intopic) = @_;

  if ( $$inpost =~/\[UploadFile.{0,6}=tmp_([^\]]+?)\]/is)
  {
    use File::Copy;
    my $tmppath=&getusrdir(1); #��ʱĿ¼

    $topic =$intopic%100;
    my $topath = "${imagesdir}$usrdir/$inforum/$topic"; #Ŀ��Ŀ¼
    mkdir ("${imagesdir}$usrdir/$inforum", 0777) if (!(-e "${imagesdir}$usrdir/$inforum"));
    chmod(0777,"${imagesdir}$usrdir/$inforum");
    mkdir ("$topath", 0777) if (!(-e "$topath"));
    chmod(0777,"$topath");

    my $tmpshow=$$inpost;
    while ($tmpshow =~ /\[UploadFile.{0,6}=tmp\_([^\]]+?)\]/i) {
      my $filename = $1;
      if (!(-e "$tmppath/tmp_$filename")) { $$inpost=~ s/\[UploadFile.{0,6}=tmp\_$filename\]//isg; }  #ɾ�����ڵ��ļ�
      else {
    	if ($filename =~ /\.torrent/i) {
	    copy("$tmppath/tmp_$filename", "$topath/$filename"); unlink("$tmppath/tmp_$filename"); copy("$tmppath/tmp_$filename.btfile", "$topath/$filename.btfile"); unlink("$tmppath/tmp_$filename.btfile");
    	} else {
 	    copy("$tmppath/tmp_$filename", "$topath/$filename"); unlink("$tmppath/tmp_$filename");
    	}
	$tmpprint = "$tmpprint$filename\n";  #Ҫд��cache������
      }
      $tmpshow =~ s/\[UploadFile.{0,6}=tmp\_$filename\]//isg;
    }
    
    $$inpost=~ s/(\[UploadFile.{0,6}=)tmp\_(([^\]]+?)\])/$1$2/isg; #��������

    mkdir("${lbdir}FileCount/$inforum", 0777) if (!(-e "${lbdir}FileCount/$inforum"));
    chmod(0777,"${lbdir}FileCount/$inforum");
    open (FILE, ">>${lbdir}FileCount/$inforum/$inforum\_$intopic.pl"); #д��cache
    print FILE "$tmpprint";
    close(FILE);
    my @tmpprint = split(/\n/,$tmpprint);
    $tmpprint = $tmpprint[0];
    my ($up_name,$up_ext) = split(/.*\./,$tmpprint);
    return $up_ext;  ##�и�������BT�������ж�
   }
  else {return 0; } ###�޸�����Ȼ��BT
}

sub delupfiles #ɾ����ǰ����ȫ���������������ӷ�ʽ��---ɾ���ظ�ʱ����
{
  my ($inpost,$inforum,$intopic) = @_;
  if ( $$inpost =~/\[UploadFile.{0,6}=([^\]]+?)\]/is)
  {
    $topic =$intopic%100;
    my $topath = "${imagesdir}$usrdir/$inforum/$topic"; #Ŀ��Ŀ¼

    my $usruploadfile = "${lbdir}FileCount/$inforum/${inforum}\_${intopic}.pl";
    if (open(FILEUP,"$usruploadfile")) 
    {
      sysread(FILEUP, $tmpprint,(stat(FILEUP))[7]);
      close(FILEUP);
      $tmpprint =~ s/\r//isg;
    }

    my $tmpshow=$$inpost;
    $tmpshow =~ s/\[UploadFile.{0,6}=tmp\_[^\]]+?\]//isg;  #��ʱ�ļ���������Ϊ������ϴ���

    while ($tmpshow =~ /\[UploadFile.{0,6}=([^\]]+?)\]/i) {
    	my $filename = $1;
    	if ($filename =~ /\.torrent/i) {
	    unlink("$topath/$filename"); unlink("$topath/$filename.btfile");  $tmpprint =~ s/$filename//isg;
    	} else {
 	    unlink("$topath/$filename"); unlink("$topath/$filename.waterpicture"); $tmpprint =~ s/$filename//isg;
    	}
        $tmpshow =~ s/\[UploadFile.{0,6}=([^\]]+?)\]//i;
    }
#    $tmpshow =~ s/(.*?)(\[UploadFile.{0,6}=[^\]]+?\])(.*?)/$2/isg;
#    $tmpshow=~ s/\[UploadFile.{0,6}=([^\]]+?(\.torrent))\]/unlink\("$topath\/$1"\)\; unlink\("$topath\/$1\.btfile"\)\;  $tmpprint\=\~ s\/$1\/\/isg\;/isg;  ##ɾ��BT�ļ�
#    $tmpshow=~ s/\[UploadFile.{0,6}=([^\]]+?)\]/ unlink\("$topath\/$1"\)\;/isg; ###unlink\("$topath\/$1"\)\;$tmpprint\=\~ s\/$1\/\/isg\;/isg; 

#    $err=0;
 #   eval $tmpshow; #unlink
#    if ($@) {$err=1;} 

    ### $tmpprint=~ s/$1//isg;  #Ҫд��cache������

    $$inpost =~ s/\[UploadFile(.{0,6})=(tmp\_[^\]]+?)\]/\[Uploadhtc$1=$2\]/isg;
    $$inpost =~ s/\[UploadFile.{0,6}=(.+?)\]//isg;
    $$inpost =~ s/\[Uploadhtc(.{0,6})=(tmp\_[^\]]+?)\]/\[UploadFile$1=$2\]/isg;

    $tmpprint =~ s/\n\n/\n/isg;
    
    open (FILE, ">${lbdir}FileCount/$inforum/$inforum\_$intopic.pl"); #д��cache
    print FILE "$tmpprint";
    close(FILE);
    return $err; 
   }
  else {return 0; }
}

sub delallupfiles #ɾ����ǰ����ȫ������,ȫ��ɾ����ʱ����ã�cache��ʽ��
{
  my ($inforum,$intopic) = @_;

    $topic =$intopic%100;
    my $topath = "${imagesdir}$usrdir/$inforum/$topic"; #Ŀ��Ŀ¼

    my $usruploadfile = "${lbdir}FileCount/$inforum/${inforum}\_${intopic}.pl";
    if (open(FILEUP,"$usruploadfile")) 
    {
      sysread(FILEUP, $files,(stat(FILEUP))[7]);
      close(FILEUP);
      $files =~ s/\r//isg;
      my @files=split(/\n/,$files);
      foreach my $line (@files)  {  chomp $line; unlink("$topath/$line"); unlink("$topath/$line.waterpicture"); }
    }
    unlink ("$usruploadfile");
    return ; 

}

sub moveallupfiles #�ƶ�/copy��ǰ����ȫ������,�ƶ�/copy��ʱ����ã�cache��ʽ��
{
  my ($oldforum,$oldtopic,$newforum,$newtopic,$copy) = @_;

    my $topic =$oldtopic%100;
    my $nowpath = "${imagesdir}$usrdir/$oldforum/$topic"; #ԭ��Ŀ¼

    $topic =$newtopic%100;
    my $topath = "${imagesdir}$usrdir/$newforum/$topic"; #Ŀ��Ŀ¼
    mkdir ("${imagesdir}$usrdir/$newforum", 0777) if (!(-e "${imagesdir}$usrdir/$newforum"));
    chmod(0777,"${imagesdir}$usrdir/$newforum");
    mkdir ("$topath", 0777) if (!(-e "$topath"));
    chmod(0777,"$topath");


    my $usruploadfile = "${lbdir}FileCount/$oldforum/${oldforum}\_${oldtopic}.pl";
    mkdir("${lbdir}FileCount/$newforum", 0777) if (!(-e "${lbdir}FileCount/$newforum"));
    chmod(0777,"${lbdir}FileCount/$newforum");
    my $newusruploadfile = "${lbdir}FileCount/$newforum/${newforum}\_${newtopic}.pl";
    if (open(FILEUP,"$usruploadfile")) 
    {
      sysread(FILEUP, $files,(stat(FILEUP))[7]);
      close(FILEUP);
      $files =~ s/\r//isg;
      my @files=split(/\n/,$files);
      foreach my $line (@files)  
      {  
        chomp $line; 
        copy("$nowpath/$line","$topath/$line");
        unlink("$nowpath/$line") if ($copy eq "no");
        unlink("$nowpath/$line.waterpicture") if ($copy eq "no");
       }
    }

    copy("$usruploadfile","$newusruploadfile");
    open(FILEUP,"$newusruploadfile");
    sysread(FILEUP, $files,(stat(FILEUP))[7]);
    close(FILEUP);
    $files =~ s/\r//isg;
    $files =~ s/$oldforum\_$oldtopic\_/$newforum\_$newtopic\_/isg;
    $files =~ s/$oldforum\_$oldtopic\./$newforum\_$newtopic\./isg;
    open(FILEUP,">$newusruploadfile");
    print FILEUP "$files";
    close(FILEUP);
    unlink ("$usruploadfile") if ($copy eq "no");
    return ; 

}

sub getusrdir #��ȡ��ʱ�ļ���
{
 my $incanshu=shift;
# my $tmpname = $inmembername;
 my $tmpname = $query->cookie("amembernamecookie");
 $tmpname =~ s/ /\_/g;
 $tmpname =~ tr/A-Z/a-z/;
 $tmpname =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
 mkdir ("${imagesdir}$usrdir/tmp", 0777) if (!(-e "${imagesdir}$usrdir/tmp"));
 chmod(0777,"${imagesdir}$usrdir/tmp");
 my $pathtocheck ="${imagesdir}$usrdir/tmp/$tmpname";

 mkdir ("$pathtocheck", 0777) if (!(-e "$pathtocheck"));
 chmod(0777,"$pathtocheck");

 opendir (DIR, "$pathtocheck"); #��1��
 my @files = readdir(DIR);
 closedir (DIR);

 foreach (@files) {unlink("$pathtocheck/$_") if ((-M "$pathtocheck/$_") *86400 > 60*60);} #��ʱ�ϴ�����60min


 opendir (DIR, "$pathtocheck"); #��2��
 @files = readdir(DIR);
 closedir (DIR);
 $filesno = @files;
 $filesno = $filesno - 2;
 $maxaddnum = 10 if ($maxaddnum eq "" || $maxaddnum < 1);
 if ($incanshu ne 1) {
     if ($filesno > $maxaddnum && $membercode ne "ad" && $membercode ne "smo") {$pathtocheck = "ERR";} ##ͬʱ�ϴ���������޶�##{$thisout="�������ϴ��Ķ���̫���˻����벻Ҫͬʱ�ڼ�����ͬʱ�ϴ���лл����";&thisout("$thisoutput");exit;}
 }
 return "$pathtocheck" ;
}

sub gettmpname #��ȡ��ʱ�ļ�����
{
 my $thisname =shift;
 $thisname=uri_escape($thisname); #�����ϴ����ļ���Ҫ������(·��)
 $thisname =~ s/%/1/isg;#�����ϴ����ļ���Ҫ������(·��)
 $thisname =~ s/\./2/isg;
 $thisname =~ s/\\/3/isg;
 $thisname =~ s/\//4/isg;
 $thisname =~ s/\=/5/isg;
 $thisname =~ s/\-/6/isg;
 $thisname =~ s/\)/7/isg;
 $thisname =~ s/\(/8/isg;
 $thisname =~ s/\+/9/isg;
 $thisname =~ s/\|/0/isg;
 $thisname =~ s/\$/1/isg;
 $thisname =~ s/\,/2/isg;
 $thisname =~ s/\{/3/isg;
 $thisname =~ s/\}/4/isg;
 $thisname =~ s/\[/5/isg;
 $thisname =~ s/\]/6/isg;
 $thisname =~ s/[\W]/0/isg;
 $thisname = substr($thisname,0,16) if (length($thisname)>16);
 my $prefix = "tmp";
 if ($thisname=~/^tmp/) {$prefix .= "_up";} #tmp��ͷ��Ϊʶ�����������ͷ��tmp�����upǰ׺
 my $thistime =time;
 $thisname = "${prefix}_${thisname}_$thistime";
 return "$thisname";
}
1;