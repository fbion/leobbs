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
# 2005-07-1 maiweb ������ -------- For leobbs 0926 �Ժ�İ汾
# 1��������Ա���ϱ��ݡ��ָ�Bug ------�������� oldĿ¼���������
# 2�������฽����Ŀ¼����bug
# 3��������ӻָ�֮����Ҫ�����̨����ͳ��һ�Σ�
# 4������ϵͳ���ñ�����ȫ
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
use Archive::Tar;
use Cwd;
use File::DosGlob 'glob';
use File::Copy;
$loadcopymo = 1;

$LBCGI::POST_MAX=200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "admin.lib.pl";
require "bbs.lib.pl";
$|++;

$thisprog = "adbackup.cgi";

$query = new LBCGI;

$action          = $query -> param('action');
$action          = &unHTML("$action");
@dirtoopen     = $query -> param('dirtoopen');

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

$attachement  = $query-> param('attachement');
$fn=            $query-> param('fn');
$an=            $query-> param('an');
$mn=            $query-> param('mn');
$un=            $query-> param('un');
$comeon=        $query-> param('comeon');
$step=        $query-> param('step');
$ttarnum=        $query-> param('ttarnum');
$atarnum=        $query-> param('atarnum');
$mtarnum=        $query-> param('mtarnum');
$utarnum=        $query-> param('utarnum');
$tarname=        $query-> param('tarname');
$totalnum=        $query-> param('totalnum');
$currentnum=        $query-> param('currentnum');
$oldversion=        $query-> param('oldversion');
$packall=        $query-> param('packall');
$mgn=  $query-> param('mgn');

##########�ָ�����
@restorelist=        $query-> param('restorelist');
$toopen=        $query-> param('toopen');

if ($memdir ne "")
 {$memberdir=$memdir;} elsif ($memberdir eq "") {$memberdir="members";}

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");       
&admintitle;
        
&getmember("$inmembername","no");
        
        if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
            
            print qq~
            <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
            <b>��ӭ������̳�������� / ��̳���ݱ���</b>
            </td></tr>
            ~;
            
            my %Mode = ( 
            'prebackup'             =>    \&prebackup,
            'delete'            =>    \&delete,
            'restore'            =>    \&restore,
            'dorestore'            =>    \&dorestore,
            'backup'              =>     \&backup,
            'select'           =>       \&memberoptions1,
            'untar'              =>       \&untar
            );


            if($Mode{$action}) { 
               $Mode{$action}->();
               }
                else { &memberoptions; }
            
            print qq~</table></td></tr></table>~;
            }
                
            else {
               &adminlogin;
               }
        

sub restore {
print qq~
    <form action="$thisprog" method=post name=form>
    <input type=hidden name="action" value="dorestore">
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#990000><b>��������Ҫ��ԭ�ı����ļ�����</b>    
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <div align=center><font color=#333333><BR>��������Ҫ��ԭ�ı����ļ����ƣ�����ȷ�����Ѿ���FTP�ϴ������$lbdir��ǰĿ¼�� <br><br><B><input type=input size=40 name="dirtoopen" value="xqlb.tar"></B><p></div>
    >***�����Ҫ��ԭ����Ŀ�����ʱδѡȡ<font color=blue>���ܴ��</font>ѡ��뽫���е������ļ��������$lbdir��ǰĿ¼�����������������<font color=blue>tarfilelist.txt</font>***
    <br><Br>
    <div align=center>
    <input type="checkbox" name="oldversion" value="yes"><font color=red>�ɰ汾���</font><br>
    �������ļ�������ʹ���°汾���ݳ��������ģ������ѡȡ���
    <p>
    <input type="submit" name="Submit" value="ȷ�ϻ�ԭ����"></div>
    <p>
    </td>
    </tr>
    
    </form>
    
   
   ~;           
}

sub dorestore
{
  
   chdir $lbdir;
   if ($oldversion eq "yes") 
   {&oldrestore;} 
   else #new restore
   {
    $toopen=@dirtoopen[0];
    if (-e "${lbdir}$toopen") #do
    {
      #################### δ���ܴ��� ##   
      if ($toopen eq "tarfilelist.txt")
      {
       $packall="no";
       chdir $lbdir;
       open(FILE,"$toopen"); 
       @tarinfo=<FILE>;
       chomp(@tarinfo);
       close(FILE);        
       (my $a,$tarname)=split(/\t/,$tarinfo[1]) ;
       @tarfile=glob("$tarname*.tar");
       unshift(@tarfile,"$toopen");                         
      }
      
      
      
      
      if ($packall ne "no")
      
      {
      my $tar =  Archive::Tar->new();
      unless ($tar->read("${lbdir}$toopen", 0)) {
	        print qq~<td class='w' align='left' width='60%'>${lbdir}$toopen���ܶ�ȡ�������Ƿ�ʹ�ö�����ģʽ�ϴ�(һ��Ҫ���ģʽ�ϴ����ѹ����)</td></tr>~;
            exit;
        }                                        
      @tarfile=$tar->list_files(); 
      chdir $lbdir;
      $tar->extract($tarfile[0],$lbdir);
      }  
     

       	     

      if ($tarfile[0] eq "tarfilelist.txt")
      {       
         
       open(FILE,">tarfileindex.txt");
       foreach(@tarfile)
        {
        print FILE "$_";
        print FILE "\n";
       }
       close(FILE);
                  
       ################## ��ȡ����Ϣ
       open(FILE,"tarfilelist.txt"); 
       @tarinfo=<FILE>;
       chomp(@tarinfo);
       close(FILE);
        
       (my $a,$tartime)=split(/\t/,$tarinfo[0]) ;
       (my $a,$tarname)=split(/\t/,$tarinfo[1]) ;
       (my $a,$totalnum)=split(/\t/,$tarinfo[2]);
       (my $a,$havemember)=split(/\t/,$tarinfo[3]);
       (my $a,$haveavatar)=split(/\t/,$tarinfo[4]);
       (my $a,$havesystem)=split(/\t/,$tarinfo[5]);
       (my $a,$havetopic)=split(/\t/,$tarinfo[6]);
       (my $a,$haveattachement)=split(/\t/,$tarinfo[7]);
       (my $a,$havemsg1)=split(/\t/,$tarinfo[8]);
       (my $a,$havemsg2)=split(/\t/,$tarinfo[9]);

       if ($havemember>0)
       {
       	$showmember="<input type='checkbox' name='restorelist' value='memdir'>�û������ļ�";
       	}
       if ($havemsg1>0)
       {
       $showmsg="<input type='checkbox' name='restorelist' value='msg'>����Ϣ�ļ�";
       }
       if ($havemsg2>0)
       {
       $showmsg="<input type='checkbox' name='restorelist' value='msg'>����Ϣ�ļ�";
       }
       if ($haveavatar>0)
       {
       	$showavatar="<input type='checkbox' name='restorelist' value='avatar'>�û��Զ���ͷ��";
       	}
       if ($havesystem>0)
       {
       $showsystem="<input type='checkbox' name='restorelist' value='system'>ϵͳ�����ļ�";
       }
       
       if ($havetopic>0)
       {
       @forumlist=();
       for ($i=13;$i<$#tarinfo;$i++)
        {
 
        if ($tarinfo[$i] =~ m/forum/) 
        
        {push(@forumlist,$tarinfo[$i]);}
        }
       chomp(@forumlist);
       $showforum="<table width=97% align=center>";
       $ii=0;
       foreach(@forumlist)
        {
          ($forumid,$forumname)=split(/\t/,$_);
          ($a,$forumid)=split(/m/,$forumid);
                    
          $showforum.="<tr>" if ($ii==0);
          $showforum=$showforum."<td><p><input type='checkbox' name='restorelist' value=$forumid>${forumname}</td><td>��ԭ��$forumid�Ű���</td>";
          $showforum.="</tr>" if ($ii==2);
          $ii=($ii>2)?0:++$i;
        }
        $showforum.="</table>";
        }
        else
        {
        $showforum="<p>�ð���û�б�����̳��������<p>";
        }
      if($haveattachement>0)
       {
       $showattachement="<input type='checkbox' name='restorelist' value='attachement' checked>��ԭ����ͬʱ�ָ��ð��渽��<br>"
       }
       else
       {
       $showattachement="�ð���û�б�����̳�������Ӹ���";
       }
       
      print qq~
       <form action="$thisprog" method=post name=form>
       <input type=hidden name="action" value="untar">
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>��ѡ����Ҫ��ԭ����Ŀ</b>
        <p>
        ����ʱ��:$tartime
        </td>
        </tr>          
        

                
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <p>
    <font color=red>ϵͳ���ݣ�</font>
    <hr>
    $showmember &nbsp $showmsg &nbsp $showavatar &nbsp $showsystem
    <p>
    <font color=red>��Ҫ�ָ��İ���</font>
    <hr>
    $showforum
    <p>
    <div align=center>$showattachement</div>
    <hr>
    <div align=center>
                <input type=hidden name="tarname" value="$tarname">
                <input type=hidden name="step" value="preuntar">
                <input type=hidden name="toopen" value="$toopen">
                <input type=hidden name="packall" value="$packall">
                <input type=hidden name="totalnum" value="$totalnum">
                <input type="submit" name="Submit" value="�ָ��ļ�Ԥ����">
                <input type="reset" name="Submit2" value="����ѡ��">

    </td>
    </tr>
    </form>
~; 
        
        
        
        
   
       print "</td></tr>";
      } 
      else
      {
           print qq~	
      <tr>
    <td bgcolor=#FFFFFF colspan=2>
    �޷��ҵ������ļ�.(����ԭ��:���п�������ļ�����ʹ�ñ��汾���....!����.�ļ������Ĺ�) 
     </td>
      </tr>
      ~;
     exit;
      
      } 
       
         
      
      } # end if do 
     else  #abc
     {
     
     print qq~	
      <tr>
    <td bgcolor=#FFFFFF colspan=2>
    ��������û�ҵ��ҵ�������������ļ������Ƿ��Ѿ��ϴ���
     </td>
      </tr>
      ~;
     exit;
     
     
     }  #end else abc
   
   }
}


sub untar
{

opendir (DIRS, "$lbdir");
my @files2 = readdir(DIRS);
closedir (DIRS);
@files2 = grep(/^\w+?$/i, @files2);
my @msgdir = grep(/^messages/i, @files2);
$msgdir = $msgdir[0];
       
       chdir $lbdir;
       if ($step eq "preuntar")
        {
        print qq~
       <form action="$thisprog" method=post name=form>
       <input type=hidden name="action" value="untar">
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>���Ԥ����</b>
        </td>
        </tr>
        <tr>       
        <td align=center colspan=2>
         ~;        
         if (-e "tarfileindex.txt")
         {
         
         open(FILE,"tarfileindex.txt");
         @filelist=<FILE>;
         chomp(@filelist);
         close(FILE);
         if($restorelist[$#restorelist] eq "attachement")
         {
         $attachement="yes";
         pop(@restorelist);
         }
         
         @needtotar=();
         foreach $rl (@restorelist)
         {
          
           if($rl eq "memdir")  
               {
               	foreach $fl (@filelist)
               	   {
               	      $a=$tarname."m";
               	      if ($fl =~ m/$a/) {push(@needtotar,"$fl\t${lbdir}${memberdir}/old");# ����by maiweb
               	      }
               	   }
               	}
           elsif($rl eq "msg")  
                {
                     	foreach $fl (@filelist)
               	   {
               	      $a=$tarname."gin";
               	      if ($fl =~ m/$a/) {push(@needtotar,"$fl\t${lbdir}$msgdir/in");}
               	   }
                     	foreach $fl (@filelist)
               	   {
               	      $a=$tarname."gout";
               	      if ($fl =~ m/$a/) {push(@needtotar,"$fl\t${lbdir}$msgdir/out");}
               	   }
                }
           elsif($rl eq "avatar")  
                {
                     	foreach $fl (@filelist)
               	   {
               	      $a=$tarname."u";
               	      if ($fl =~ m/$a/) {push(@needtotar,"$fl\t${imagesdir}usravatars");}
               	   }
                }
           elsif($rl eq "system")  
               {
               		foreach $fl (@filelist)
               	   {
               	      $a=$tarname."s";
               	      if ($fl =~m /$a/) {push(@needtotar,"$fl\t${lbdir}data");}
               	   }
               	}
           elsif ($rl=~ /\d/)
           {
                  
                
                  foreach $fl (@filelist)
                     {
                     $a=$tarname."t_".$rl."_";
                     $b=$tarname."a_".$rl."_";
                     if ($fl =~m /$a/) {push(@needtotar,"$fl\t${lbdir}forum$rl");}
                     if ($attachement eq "yes")
                     {
                     if ($fl =~m /$b/) {push(@needtotar,"$fl\t${imagesdir}$usrdir/$rl");}
                     }
                    
                     }
                   
           
           }  #end elsif.....
           
        
           } #end foreach(@restorelist)
            
           chomp(@needtotar);
           open(FILE,">needtotar.txt");
           foreach(@needtotar)
           {
           print FILE "$_";
           print FILE "\n";
           }
           close(FILE);
          
           if ($packall ne "no")
           {
           my $tar =  Archive::Tar->new();
           unless ($tar->read("${lbdir}$toopen", 0)) {
	        print qq~<td class='w' align='left' width='60%'>${lbdir}$toopen���ܶ�ȡ�������Ƿ�ʹ�ö�����ģʽ�ϴ�(һ��Ҫ���ģʽ�ϴ����ѹ����)</td></tr>~;
            exit;
           }           
        
           @needtotar1=();
           foreach(@needtotar)
           {
           ($a,$b)=split(/\t/,$_);
           push(@needtotar1,$a);
           }
           
           
           chdir $lbdir;
           $tar->extract(@needtotar1, $lbdir);
           }
           
          $error="no";
          $status="<div align=left><p><font color=red>";
          foreach(@needtotar)
          {
            (my $isok,my $dirname)=split(/\t/,$_);
             if  (-e "$isok")  {$status.="$isok �ְ��ɹ�<br>";} else {$status.="$isok �ְ�<font color=blue>δ�ɹ�</font>�������Ƿ�ʹ�ö�����ģʽ�ϴ���<br>";$error="yes";}   
             if  (opendir(DIR,"$dirname")) {$status.="$dirname ����<br>";} 
                   else {$status.="$dirname <font color=blue>������</font>";
                         if (mkdir("$dirname",777)) {
							 chmod(0777,"$dirname");
							 $status.="&nbsp Ŀ¼�����ɹ�<br>";}
                            else{$status.="&nbspĿ¼����ʧ��<br>";$error="yes";}                         
                         } #else 
         
          
          }                  
          
          $status.="</font></div>";
          chdir $lbdir;
          open(FILE,">restorestatus.txt");
          print FILE "<div align=left><p>";
          close(FILE);
          
          print qq~
          $status
          <p>
          <div align=center>Ԥ�������</div>
          <p>
          ~;
           if ($error eq "yes")
           {
             print qq~
          <p><font color=red>
          <div align=center>Ԥ�����������ݴ�����ʾ�����¼��һ�顣</font>
          </td></tr>
          ~;
          exit;
           
           }
           
           
           
           
         }
         else
         {
         print qq~
         <p><font color=red>
         <div align=center>Ԥ��������뷵�أ�����һ�顣</font>
         </td></tr>
         ~;
         exit;
         }
        
        
        
        
      print qq~      
            <div align=center>
                <input type=hidden name="currentnum" value="0">
                <input type=hidden name="tarname" value="$tarname">
                <input type=hidden name="step" value="untar">
                <input type=hidden name="totalnum" value="$totalnum">
                <input type=hidden name="packall" value="$packall">
                <input type="submit" name="Submit" value="�ָ��ļ�">
        </form>
        </td>
        </tr>
        ~;
        }
       
        elsif ($step eq "untar")
        {
        print qq~
       <form action="$thisprog" method=post name=form>
       <input type=hidden name="action" value="untar">
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>����ָ��С���������</b>
        </td>
        </tr>
        <tr>       
        <td align=center colspan=2>
         ~;        
        chdir $lbdir;
        open(FILE,"needtotar.txt");
        @needtotar=<FILE>;
        close(FILE);
        chomp(@needtotar);
        $totar=shift(@needtotar);
        ($name,$dir)=split(/\t/,$totar);
		chdir $dir;
          my $tar =  Archive::Tar->new();
           $status="${lbdir}$name��ԭ��ϡ�";         
           unless ($tar->read("${lbdir}$name", 0)) {
	        print qq~
	        ${lbdir}$name���ܶ�ȡ�������Ƿ�ʹ�ö�����ģʽ�ϴ�(һ��Ҫ���ģʽ�ϴ����ѹ����)
	        ~;
                $status="${lbdir}$name���ܶ�ȡ�������Ƿ�ʹ�ö�����ģʽ�ϴ�(һ��Ҫ���ģʽ�ϴ����ѹ����)";

           }
        
            my @files = $tar->list_files();
            chdir $dir;
            $tar->extract(@files, $dir);
            $currentnum=$currentnum+$#files+1;
            chdir $lbdir;
            
            if ($packall ne "no") {
            	unlink("$name");
		$forumid = $name;
		$forumid =~ s/^$tarname//;
            	if ($forumid =~ /^t\_/i) {
		    $forumid =~ s/^t\_(\d+)\_(\d+)\.tar/$1/;
	    copy("${lbdir}forum$forumid/list$forumid.cgi","${lbdir}boarddata/listno$forumid.cgi");
	    copy("${lbdir}forum$forumid/xzb$forumid.cgi","${lbdir}boarddata/xzb$forumid.cgi");
	    copy("${lbdir}forum$forumid/xzbs$forumid.cgi","${lbdir}boarddata/xzbs$forumid.cgi");
	    copy("${lbdir}forum$forumid/lastnum$forumid.cgi","${lbdir}boarddata/lastnum$forumid.cgi");
	    copy("${lbdir}forum$forumid/ontop$forumid.cgi","${lbdir}boarddata/ontop$forumid.cgi");
	    copy("${lbdir}forum$forumid/jinghua$forumid.cgi","${lbdir}boarddata/jinghua$forumid.cgi");
	    chmod(0666,"${lbdir}boarddata/listno$forumid.cgi");
	    chmod(0666,"${lbdir}boarddata/xzb$forumid.cgi");
	    chmod(0666,"${lbdir}boarddata/xzbs$forumid.cgi");
	    chmod(0666,"${lbdir}boarddata/lastnum$forumid.cgi");
	    chmod(0666,"${lbdir}boarddata/ontop$forumid.cgi");
	    chmod(0666,"${lbdir}boarddata/jinghua$forumid.cgi");
	    unlink "${lbdir}forum$forumid/list$forumid.cgi";
	    unlink "${lbdir}forum$forumid/xzb$forumid.cgi";
	    unlink "${lbdir}forum$forumid/xzbs$forumid.cgi";
	    unlink "${lbdir}forum$forumid/lastnum$forumid.cgi";
	    unlink "${lbdir}forum$forumid/ontop$forumid.cgi";
	    unlink "${lbdir}forum$forumid/jinghua$forumid.cgi";
            	}
            }
         if ($#needtotar>=0)
         {
         open(FILE,">needtotar.txt");
         foreach(@needtotar)
         {
         print FILE "$_";
         print FILE "\n";
         }
                       chdir $lbdir;
                       open(FILE,">>restorestatus.txt");
                       print FILE "$status <br>";
                       close(FILES);
         
         }        
        
                              else { 
                              	
                       chdir $lbdir;
                       open(FILE,">>restorestatus.txt");
                       print FILE "$status <br>";
                       close(FILES);
                       
                       
                              	    print qq~      
                 <div align=center>
                
                <input type=hidden name="packall" value="$packall">
                <input type=hidden name="tarname" value="$tarname">
                <input type=hidden name="step" value="finish">
                <input type=hidden name="totalnum" value="$totalnum">
                <input type="submit" name="Submit" value="�ָ��ļ�">
        <script>
        setTimeout('document.form.submit()',2000);
        </script>
                   </div>
        
        
               </form>
               </td>
               </tr>
               ~;
                              	
                   exit;           	
                              	
                              	}
        
        $percent=int(($currentnum/$totalnum)*100);
        $percent1=int(100-$percent);                  
        
             print qq~      
           
            
            <div align=center>
                  <b>��ԭ����</b><br>
       (��ԭ�������ֵ����Ի�ԭ�ļ������ļ����еı���,�����Դ���Ϊ��ԭ����ʱ����ƶ�)
       <table width=80% board=0 height=20>
       <tr>
       <td width=$percent% bgcolor=blue></td>
       <td width=$percent1%></td>
       </tr>
       </table>
           
                <input type=hidden name="packall" value="$packall">
                <input type=hidden name="currentnum" value="$currentnum">
                <input type=hidden name="tarname" value="$tarname">
                <input type=hidden name="step" value="untar">
                <input type=hidden name="totalnum" value="$totalnum">
                <input type="submit" name="Submit" value="�ָ��ļ�">
        <script>
        setTimeout('document.form.submit()',2000);
        </script>
            </div>
        
        
        </form>
        </td>
        </tr>
        ~;
        
        
        
        
        }               
        elsif($step eq "finish")
        {
        chdir $lbdir;      
        open (FILE,"restorestatus.txt");
        @status=<FILE>;
        close(FILE);        
        chomp(@status);
        unlink("restorestatus.txt");
        unlink("tarfileindex.txt");
        unlink("needtotar.txt");
        unlink("tarfilelist.txt") if ($packall ne "no"); 
        
        
        print qq~
        <tr>
        <td>
        ��ԭ����..״̬����:
        @status
        </td>
        </tr>
        ~;
        }
        
        
        
       
         

}




sub oldrestore {
$toopen=@dirtoopen[0];
if (-e "${lbdir}$toopen"){
print qq~
<tr>
    <td bgcolor=#FFFFFF colspan=2>
    ���������ҵ������ڿ�ʼ��ԭ��
</td>
</tr>
~;
{
        my $cwd = cwd();
        my $tar =  Archive::Tar->new();
        unless ($tar->read("${lbdir}$toopen", 0)) {
	        print qq~<td class='w' align='left' width='60%'>${lbdir}$toopen���ܶ�ȡ�������Ƿ�ʹ�ö�����ģʽ�ϴ�(һ��Ҫ���ģʽ�ϴ����ѹ����)</td></tr>~;
            exit;
        }
        chdir $lbdir;
        my @files = $tar->list_files();
        $tar->extract(@files, $lbdir);
        chdir $cwd;
}
print qq~
<tr>
    <td bgcolor=#FFFFFF colspan=2>
    ��ԭ��ɣ�
</td>
</tr>
~;
}else {
print qq~	
<tr>
    <td bgcolor=#FFFFFF colspan=2>
    ��������û�ҵ��ҵ�������������ļ������Ƿ��Ѿ��ϴ��� 
</td>
</tr>
~;
exit;
}

}	
sub memberoptions
{
chdir $lbdir; 
    $dirtoopen = "${imagesdir}";
    opendir (DIR, "$dirtoopen"); 
    @filedata = readdir(DIR);
    closedir (DIR);

    @sortedfile = grep(/\.tar$/,@filedata);
    
    $backupfile = @sortedfile;
    if ($backupfile > 0) {
    	$last_backup = "���������ļ����ڣ��뼰ʱɾ��!";
           $bakuptrue = 0;
    }
    else {
           $last_backup = "���������ļ�û���ҵ�����̳��ȫ";
           $bakuptrue = 1;
    }   


     
    print qq~

    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#990000><b>��ѡ����Ҫ���ݵ�����</b>
    </td>
    </tr>          
        
                
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><BR>�����������ļ��� <B>$last_backup</B><BR>
    <font color=red>�����ֻ���� $imagesdir ���Ƿ��вд�ı����ļ���</font>
    <BR>
     
    </td>
    </tr>
~;
    print qq~
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b><a href="$thisprog?action=delete">ɾ�����������ļ�</a></b>��<font color=#990000>(Ϊ�˰�ȫ������뼰ʱɾ�����������ļ���)</font><br>
     ע�⣺һ�㱸�ݵ�������ɺ�Ӧ��ֱ��ɾ�����������ļ������ⲻ��Ҫ�İ�ȫ©����<BR><BR>
    </td>
    </tr>
    ~ if ($bakuptrue == 0);
    
    print qq~
    <tr>
    <td colspan=2>
    <hr>
    <br>
    <div align=center>ʹ��˵��<br></div>
    <p>
    &nbsp&nbsp&nbsp&nbsp�������Ŀ����Ϊ�˽�������ļ��ߴ��С�����µ���̳���� �ϴ������� Ч�ʵ��µ����⡣<p>
    &nbsp&nbsp&nbsp&nbsp����ʹ��ǰע�����¼��㣺<p>
    <table width=70% align=center>
    <tr>
    <td>
    1���������������У�·���������Ƿ�ʹ�þ���·�������û�У���ĳɾ���·����
    <p>
    2��$lbdir <br> $imagesdir <br>${lbdir}backup/ <br>����Ŀ¼�Ƿ����óɿ�д�����û�У�����Ϊ��д��
    <p>
    3���ڳ��򱸷ݻ�ԭ�Ĳ����У���Ҫ��Ϊ������Զ�ˢ�¶��ر����������ʱ�������ڽ��С�
    <p>
    4������ڳ���ִ�еĹ����г��ְ���������Ļ����ʾ time out ��memory out ����������Ҫ���ţ������ŵ���һ�²�����ͨ�������Խ����
    <p>
    </td>
    </tr>
    </table>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF colspan=2 align=center>
    <p><p>
    <hr>
    <font color=#333333><a href=$thisprog?action=restore>--[��ԭ]--</a>&nbsp&nbsp&nbsp<a href=$thisprog?action=select>--[����]--
    <hr>
    <p><p>
    </td>
    </tr>

~;
}
sub memberoptions1 {
print qq~
    <form action="$thisprog" method=post name=form>
    <input type=hidden name="action" value="prebackup">
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#990000><b>��ѡ����Ҫ���ݵ�����</b>
    </td>
    </tr>
  ~;      

print qq~    
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    
                    <font color=red>��ѡ��Ҫ���ݵ�ϵͳ�������ϣ�</font>
                    <hr>
                    <p> 
                      <input type="checkbox" name="dirtoopen" value="memdir">�û������ļ�&nbsp&nbsp&nbsp
                      <input type="checkbox" name="dirtoopen" value="message">�û�����Ϣ�ļ�&nbsp&nbsp&nbsp
                      <input type="checkbox" name="dirtoopen" value="avatar">�û��Զ���ͷ��&nbsp&nbsp&nbsp
                      <input type="checkbox" name="dirtoopen" value="system">ϵͳ�����ļ�
                      
                    <p><font color=red>��ѡ��Ҫ���ݵİ��棺</font><hr>
    ~;
my $filetoopen = "$lbdir" . "data/allforums.cgi";
flock(FILE, 2) if ($OS_USED eq "Unix");
open(FILE, "$filetoopen");
my @forums = <FILE>;
close(FILE);                 
$ii=0;
print "<table width=97% align=center>";
foreach my $forum (@forums) { #start foreach @forums
    chomp $forum;
    next if ($forum eq "");
    (my $forumid, my $category, my $categoryplace, my $forumname, my $forumdescription, my $tmp , $tmp , $tmp , $tmp,  $tmp , $tmp , $tmp,  $tmp,  $tmp,  $tmp, $tmp, $tmp, $tmp,my $hiddenforum,$tmp) = split(/\t/,$forum);
print "<tr>" if ($ii==0);
print qq~
<td width=33%>
<input type="checkbox" name="dirtoopen" value="forum$forumid">
                      $forumname</p>
</td>
~; 
print "</tr>" if ($ii==2);
if ($ii<2)
{$ii++;} else {$ii=0;}
}
print "</table>";                      
    print qq~
                     
                    <hr>
                    <div align=center><input type="checkbox" name="attachement" value="yes" checked>ͬʱ���������������������ļ�&nbsp&nbsp&nbsp<input type="checkbox" name="packall" value="yes" checked>���ܳ�һ���������<br>
                    
                    <font color=red>(�Ƽ�ʹ�û��ܴ���������Ϊ��ķ������ṩ����Դ���⣬��������̳�������Ϲ���������޷����У���ȡ������)</font>                  
                    </div>
                    *С���ɣ���������ʵ�����ѡȡһ�δ���Ķ��١��Ƿ���ܡ������ְ����ݵȡ���������Σ���Ȼ���Գɹ����ݡ�
                    
                    <hr>
                    �ְ�����(ÿ���ְ�����������һ����Ŀ)��<br>
                    <input type=text size=4 name="fn" value="500">�������ļ�&nbsp&nbsp<input type=text size=4 name="an" value="50">�������ļ�&nbsp&nbsp<input type=text size=4 name="mn" value="500">���û������ļ�&nbsp&nbsp<input type=text size=4 name="un" value="50">���û��Զ���ͷ���ļ�&nbsp&nbsp<input type=text size=4 name="mgn" value="500">������Ϣ�ļ�<br>
                    <font color=red>(�������������ÿ����ѹ�����а����ļ������ģ�������Լ��ķ��������ã�ͨ��ȱʡ����)</font>
                    <hr>
                    <div align=center>
                      <input type="submit" name="Submit" value="�����ļ�����">
                      <input type="reset" name="Submit2" value="����ѡ��">
                    </div>
                    </p>
    
    </td>
    </tr>                
                  </form>
    ~;
    

}

sub prebackup {
	
print qq~
        <tr>
       <tr>
        <td bgcolor=#FFFFFF align=left colspan=2>
        <font color=#990000>
                    
        <b>�������׼��</b><p>
~;        	
        chdir $lbdir;
        
        if (-e "tarfilelist.txt") {unlink("tarfilelist.txt");}
        @del=glob("backup*.temp");
        foreach(@del)
        {
        unlink("$_");
        }
        
@avatardata=();
@systemdata=();
@emoticondata=();
@attachedata=();
@memberdata=();
@msgdatain=();
@msgdataout=();

$step="unknow";

if ($dirtoopen[0] eq "memdir")
{
chdir "$lbdir$memberdir/old/";
@memberdata=glob("*");
shift(@dirtoopen);
chdir $lbdir;
$step="member";
}

if ($dirtoopen[0] eq "message")
{
chdir "${lbdir}$msgdir/in";
@msgdatain=glob("*");

chdir "${lbdir}$msgdir/out";
@msgdataout=glob("*");

shift(@dirtoopen);
chdir $lbdir;
$step="msgin" if ($step eq "unknow");
}

if ($dirtoopen[0] eq "avatar")
{
chdir "${imagesdir}usravatars";
@avatardata=glob("*");
shift(@dirtoopen);
chdir $lbdir;
$step="avatar" if ($step eq "unknow");
}

if ($dirtoopen[0] eq "system")
{
chdir "${lbdir}data";

# ���� by maiweb begin
    	@systemdata=glob("*\.*");     
    	foreach $adas(@systemdata){
        next if ($adas=~/\./);
        @temp223=glob("$adas/*");
        push(@systemdata,@temp223);
        }# ���� By maiweb end
shift(@dirtoopen);
chdir $lbdir;
$step="system" if ($step eq "unknow");
}

if ($dirtoopen[0]=~m/forum/)
{
   $ttotal=0;
   $atotal=0;
   @forumtotar=@dirtoopen;
   foreach $dirtoopen (@dirtoopen){
    ($a,$b)=split(/m/,$dirtoopen);
    chdir "$lbdir$dirtoopen";
    @temp1=glob("*");      
    if (($dirtoopen=~m/forum/)&&($attachement eq "yes"))
    {   
    	chdir "${imagesdir}$usrdir/$b";
    	# ���� by maiweb begin
    	@temp2=glob("$b\_*");     
    	my @alladad=glob("*");
    	foreach $adas(@alladad){
        next if ($adas=~/\_/);
        @temp223=glob("$adas/*");
        push(@temp2,@temp223);
        }# ���� By maiweb end
    }
   chdir $lbdir;
   open(FILE,">backuptopic_$b.temp");
   foreach(@temp1)
        {
        print FILE "$_";
        print FILE "\n";
        }
   close(FILE);
   open(FILE,">backupattachement_$b.temp");
   foreach(@temp2)
        {
        print FILE "$_";
        print FILE "\n";
        }
   close(FILE);   
   ########�������Ӻ͸�����
   $ttotal=$#temp1+1+$ttotal;
   $atotal=$#temp2+1+$atotal;
   
   @emoticondata=(@emoticondata,"backuptopic_$b.temp");
   @attachedata=(@attachedata,"backupattachement_$b.temp");
   @temp1=();
   @temp2=();
   $step="topic" if ($step eq "unknow");
   }
}
        
        chdir $lbdir;
        
        if ($#systemdata>=0)
        {
        open(FILE,">backupsystem.temp");
        foreach(@systemdata)
        {
        print FILE "$_";
        print FILE "\n";
        }
        close(FILE);
        }
        
        if ($#avatardata>=0)
        {
        open(FILE,">backupavatar.temp");
        foreach(@avatardata)
        {
        print FILE "$_";
        print FILE "\n";
        }
        close(FILE);
        }
                         
        if ($#msgdatain>=0)
        {
        open(FILE,">backupmsgin.temp");
        foreach(@msgdatain)
        {
        print FILE "$_";
        print FILE "\n";
        }
        close(FILE);
        }
        
        if ($#msgdataout>=0)
        {
        open(FILE,">backupmsgout.temp");
        foreach(@msgdataout)
        {
        print FILE "$_";
        print FILE "\n";
        }
        close(FILE);
        }
        
        if ($#memberdata>=0)
        {
        open(FILE,">backupmember.temp");
        foreach(@memberdata)
        {
        print FILE "$_";
        print FILE "\n";
        }
        close(FILE);
        }

        if($#emoticondata>=0)
        {
        open(FILE,">backuptopic.temp");
        foreach(@emoticondata)
        {
        print FILE "$_";
        print FILE "\n";
        }
        close(FILE);
        }
        
        if($#attachedata>=0)
        {
        open(FILE,">backupattachement.temp");
        foreach(@attachedata)
        {
        print FILE "$_";
        print FILE "\n";
        }
        close(FILE);
        }
        
        if ($atotal<=0) {$aa=0;} else {$aa=$atotal;}
        if ($ttotal<=0) {$bb=0;} else {$bb=$ttotal;}
        if ($#memberdata<0) {$cc=0;} else {$cc=$#memberdata+1;}
        if ($#systemdata<0) {$dd=0;} else {$dd=$#systemdata+1;}
        if ($#avatardata<0) {$ee=0;} else {$ee=$#avatardata+1;}
        if ($#msgdatain<0) {$ff=0;} else {$ff=$#msgdatain+1;}
        if ($#msgdataout<0) {$gg=0;} else {$gg=$#msgdataout+1;}
        
        $totalnum=$aa+$bb+$cc+$dd+$ee+$ff+$gg;       
        
        my $time=time;
        $current_time=$time;
        $time=crypt($time,"lb");
        $time=~s /\///isg;
        $time=~s /\.//isg;
        $tarname=$time;        
        $current_time = &dateformatshort($current_time + ($timezone*3600) + ($timedifferencevalue*3600));

       chdir "${lbdir}data";
        
        
        chdir $imagesdir;
        open (FILE,">tarfilelist.txt");
        print FILE "����ʱ�䣺\t$current_time\n";
        print FILE "�ļ�����\t$tarname\n";
        print FILE "�˴α������ļ���:\t$totalnum\n";     
        print FILE "�û������ļ���:\t$cc\n";
        print FILE "�û��Զ���ͷ����:\t$ee\n";
        print FILE "ϵͳ�����ļ���:\t$dd\n";
        print FILE "�����ļ���:\t$bb\n";
        print FILE "�����ļ���:\t$aa\n";
        print FILE "����Ϣ�������ļ���:\t$ff\n";
        print FILE "����Ϣ�ռ����ļ���:\t$gg\n";
        print FILE "\n\n\n";  #Ϊ�Ժ�Ԥ��
        print FILE "���ݵ���̳���£�\n";
#########ȡ��̳��
       open(FILE1, "${lbdir}/data/allforums.cgi");
       flock(FILE1, 1) if ($OS_USED eq "Unix");
       my @forums = <FILE1>;
       close(FILE1);

                        
     
        if ($#forumtotar>=0)
        {
        foreach $forumtotar (@forumtotar)
        {
        foreach $forum (@forums) { #start foreach @forums
         chomp $forum;
         next if ($forum eq "");
       (my $forumid, my $category, my $categoryplace, $forumname, my $forumdescription, my $tmp , $tmp , $tmp , $tmp,  $tmp , $tmp , $tmp,  $tmp,  $tmp,  $tmp, $tmp, $tmp, $tmp,my $hiddenforum,$tmp) = split(/\t/,$forum);
         my $tfu="forum".$forumid;
         if ($forumtotar eq $tfu) {last;}
        } 
        
        print FILE "$forumtotar";
        print FILE "\t";
        print FILE "$forumname";
        print FILE "\n";
        }
        }
        print FILE "����ر��ְ��ļ�����������Ҫ�Ķ����ļ�";
        close(FILE);
        chdir $lbdir;


        if ($step ne "unknow")
        {
        print qq~
        </td></tr>
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=red><div align=center>�����ļ�����׼��������</div></font>
       <p>
       �˴α��ݹ��� $totalnum ���ļ�:
       <p>
       �û������ļ� $cc ��<br>
       ����Ϣ�������ļ� $ff ��<br>
       ����Ϣ�ռ����ļ� $gg ��<br>
       �û��Զ���ͷ�� $ee ��<br>
       ϵͳ�����ļ� $dd��<br>
       �����ļ� $bb ��<br>
       �����ļ� $aa ��
       <p>
       <form action="$thisprog" method=post name=form>
       <input type=hidden name="action" value="backup">
       <input type=hidden name="fn" value="$fn">
       <input type=hidden name="packall" value="$packall">
       <input type=hidden name="an" value="$an">
       <input type=hidden name="mn" value="$mn">
       <input type=hidden name="un" value="$un">
       <input type=hidden name="mgn" value="$mgn">     
       <input type=hidden name="step" value="$step">
       <input type=hidden name="ttarnum" value="1">
       <input type=hidden name="atarnum" value="1">
       <input type=hidden name="mtarnum" value="1">
       <input type=hidden name="utarnum" value="1">
       <input type=hidden name="totalnum" value="$totalnum">
       <input type=hidden name="currentnum" value="0">
       <input type=hidden name="tarname" value="$tarname">
       <input type=hidden name="attachement" value="$attachement">
       <input type="submit" name="Submit" value="�����ļ�">
      </p>

        </td></tr>
         ~;
        }
        else
        {
        
        print qq~
        <p>
        <div align=center><font color=red>
        ������ѡ��һ��������Ŀ.....
        </font></div>
        </td></tr></tr>
        ~;
        
        }
         
     } # end routine


sub backup
{
print qq~
        <tr>
       <tr>
        <td bgcolor=#FFFFFF align=left colspan=2>
        <font color=#990000>
                    
        
        ~;
       chdir $lbdir;
       
    if (($step eq "member")&&(-e "backupmember.temp"))  #member backup
        {
        @untarname=();
        chdir $lbdir;
        open(FILE,"backupmember.temp");
        @filename=<FILE>;
        chomp @filename;
        close(FILE); 
        @untarname=splice(@filename,$mn);
        
        $currentnum=($#untarname>=0)?$currentnum+$mn:$currentnum+$#filename;
        chdir "$lbdir$memberdir/old";#���� By maiweb
        
        if ($#filename>=0)
        {
        $tar = Archive::Tar->new();
        $tar->add_files(@filename);
        $tar->write("${imagesdir}${tarname}m_$ttarnum.tar");
        $ttarnum++;
        }
        chdir $lbdir;
        if ($#untarname>=0)
        {
        open(FILE,">backupmember.temp");
        foreach(@untarname)
        {
        print FILE "$_";
        print FILE "\n";
        }
        close(FILE);
        $step="member";
        print qq~
        <p>
        <div align=center>������2����Զ����У���������û���Զ���ǰ���У����� ���������ļ� ��ť</div>
        ~;
        }
        else
        {
print qq~
        <p>
        <font color=red><div align=center>�û����ϱ�����ϡ��������</div></font>
        <p>
        <div align=center>������2����Զ����У���������û���Զ���ǰ���У����� ���������ļ� ��ť</div>        
        ~;
        $step="msgin";    
        $ttarnum=1;
        }   
        goto COMEON;
        chdir $lbdir;
        }
       else
        {
        $step="msgin" if ($step eq "member")
        }
#############################################

print qq~
        <tr>
       <tr>
        <td bgcolor=#FFFFFF align=left colspan=2>
        <font color=#990000>
                    
        
        ~;
       chdir $lbdir;
       
    if (($step eq "msgin")&&(-e "backupmsgin.temp"))  #member backup
        {
        @untarname=();
        chdir $lbdir;
        open(FILE,"backupmsgin.temp");
        @filename=<FILE>;
        chomp @filename;
        close(FILE); 
        @untarname=splice(@filename,$mgn);
        
        $currentnum=($#untarname>=0)?$currentnum+$mgn:$currentnum+$#filename;
        chdir "${lbdir}$msgdir/in";
        
        if ($#filename>=0)
        {
        $tar = Archive::Tar->new();
        $tar->add_files(@filename);
        $tar->write("${imagesdir}${tarname}gin_$ttarnum.tar");
        $ttarnum++;
        }
        chdir $lbdir;
        if ($#untarname>=0)
        {
        open(FILE,">backupmsgin.temp");
        foreach(@untarname)
        {
        print FILE "$_";
        print FILE "\n";
        }
        close(FILE);
        $step="msgin";
        print qq~
        <p>
        <div align=center>������2����Զ����У���������û���Զ���ǰ���У����� ���������ļ� ��ť</div>
        ~;
        }
        else
        {
print qq~
        <p>
        <font color=red><div align=center>����Ϣ���ϱ�����ϡ��������</div></font>
        <p>
        <div align=center>������2����Զ����У���������û���Զ���ǰ���У����� ���������ļ� ��ť</div>        
        ~;
        $step="msgout";    
        $ttarnum=1;
        }   
        goto COMEON;
        chdir $lbdir;
        }
       else
        {
        $step="msgout" if ($step eq "msgin")
        }

#############################################

print qq~
        <tr>
       <tr>
        <td bgcolor=#FFFFFF align=left colspan=2>
        <font color=#990000>
                    
        
        ~;
       chdir $lbdir;
       
    if (($step eq "msgout")&&(-e "backupmsgout.temp"))  #member backup
        {
        @untarname=();
        chdir $lbdir;
        open(FILE,"backupmsgout.temp");
        @filename=<FILE>;
        chomp @filename;
        close(FILE); 
        @untarname=splice(@filename,$mgn);
        
        $currentnum=($#untarname>=0)?$currentnum+$mgn:$currentnum+$#filename;
        chdir "${lbdir}$msgdir/out";
        
        if ($#filename>=0)
        {
        $tar = Archive::Tar->new();
        $tar->add_files(@filename);
        $tar->write("${imagesdir}${tarname}gout_$ttarnum.tar");
        $ttarnum++;
        }
        chdir $lbdir;
        if ($#untarname>=0)
        {
        open(FILE,">backupmsgout.temp");
        foreach(@untarname)
        {
        print FILE "$_";
        print FILE "\n";
        }
        close(FILE);
        $step="msgout";
        print qq~
        <p>
        <div align=center>������2����Զ����У���������û���Զ���ǰ���У����� ���������ļ� ��ť</div>
        ~;
        }
        else
        {
print qq~
        <p>
        <font color=red><div align=center>����Ϣ���ϱ�����ϡ��������</div></font>
        <p>
        <div align=center>������2����Զ����У���������û���Զ���ǰ���У����� ���������ļ� ��ť</div>        
        ~;
        $step="avatar";    
        $ttarnum=1;
        }   
        goto COMEON;
        chdir $lbdir;
        }
       else
        {
        $step="avatar" if ($step eq "msgout")
        }







        #####################################
        
       if (($step eq "avatar")&&(-e "backupavatar.temp"))  #member backup
        {
        @untarname=();
        chdir $lbdir;
        open(FILE,"backupavatar.temp");
        @filename=<FILE>;
        chomp @filename;
        close(FILE); 
        @untarname=splice(@filename,$un);
        $currentnum=($#untarname>=0)?$currentnum+$mn:$currentnum+$#filename;
        chdir "${imagesdir}usravatars";
        
        if ($#filename>0)
        {
        $tar = Archive::Tar->new();
        $tar->add_files(@filename);
        $tar->write("${imagesdir}${tarname}u_$ttarnum.tar");
        }
        
        $ttarnum++;
        chdir $lbdir;
        if ($#untarname>=0)
        {
        open(FILE,">backupavatar.temp");
        foreach(@untarname)
        {
        print FILE "$_";
        print FILE "\n";
        }
        close(FILE);
        $step="avatar";
        print qq~
        <p>
        <div align=center>������2����Զ����У���������û���Զ���ǰ���У����� ���������ļ� ��ť</div>
        ~;
        }
        else
        {
print qq~
        <p>
        <font color=red><div align=center>�û��Զ���ͷ���ļ�������ϡ��������</div></font>
        <p>
        <div align=center>������2����Զ����У���������û���Զ���ǰ���У����� ���������ļ� ��ť</div>
        ~;
        $step="system";    
        $ttarnum=1;
        }   
        $skip=1;
        chdir $lbdir;
        goto COMEON;
        }
        else
        {
        $step="system" if ($step eq "avatar")
        }

        
        
        #####################################
        
       if (($step eq "system")&&(-e "backupsystem.temp"))  #member backup
        {
        chdir $lbdir;
        open(FILE,"backupsystem.temp");
        @filename=<FILE>;
        chomp @filename;
        close(FILE); 
        @untarname=();
        $currentnum=($#untarname>=0)?$currentnum+$mn:$currentnum+$#filename;
        chdir "${lbdir}data";
        if($#filename>=0)
        {
        $tar = Archive::Tar->new();
        $tar->add_files(@filename);
        $tar->write("${imagesdir}${tarname}s.tar");
        }
        chdir $lbdir;

      
print qq~
        <p>
        <font color=red><div align=center>ϵͳ�����ļ��ļ�������ϡ��������</div></font>
        <p>
        <div align=center>������2����Զ����У���������û���Զ���ǰ���У����� ���������ļ� ��ť</div>
        ~;
                

        chdir $lbdir;
        $step="topic";
        goto COMEON;
        }
        else
        {
        $step="topic" if ($step eq "system");
        }
        
        
        
        #####################################
        if (($step eq "topic")&&(-e "backuptopic.temp"))  #topic backup
        {

        @untarname=();
        chdir $lbdir;
     ################# ȡ�ļ��б�
        open(FILE,"backuptopic.temp");
        @filelist=<FILE>;
        chomp @filelist;
        close(FILE);
        
        if ($#filelist>=0)
        
        {
        ($aa,$bb)=split(/\./,$filelist[0]);
        ($bb,$fid)=split(/\_/,$aa);
        open(FILE,"$filelist[0]");
        @filename=<FILE>;
        chomp @filename;
        close(FILE); 
        @untarname=splice(@filename,$fn);
        $currentnum=($#untarname>=0)?$currentnum+$mn:$currentnum+$#filename;
        chdir "${lbdir}forum${fid}";
        if($#filename>=0)
        {
        $tar = Archive::Tar->new();
        $tar->add_files(@filename);
        $tar->write("${imagesdir}${tarname}t_${fid}_${ttarnum}.tar");
        }
        $ttarnum++;
        chdir $lbdir;
        if ($#untarname>=0)
        {
        open(FILE,">$filelist[0]");
        foreach(@untarname)
        {
        print FILE "$_";
        print FILE "\n";
        }
        close(FILE);

        print qq~
        <p>
        <div align=center>������2����Զ����У���������û���Զ���ǰ���У����� ���������ļ� ��ť</div>
        ~;
          } #end if $#untarname>=0
         else
         {
        open(FILE,"backuptopic.temp");
        @filelist=<FILE>;
        chomp @filelist;
        close(FILE);
        shift(@filelist);
        if ($#filelist>=0)
        {
        open(FILE,">backuptopic.temp");
        foreach(@filelist)
        {
          print FILE "$_";
          print FILE "\n";
        }
        close(FILE);
        $ttarnum=1;
         print qq~
        <p>
        <div align=center>������2����Զ����У���������û���Զ���ǰ���У����� ���������ļ� ��ť</div>
        ~;
        }
        else 
          {
        chdir "${lbdir}boarddata";
        @filename =();
	@data1=glob("list${fid}.cgi");
	push (@filename, @data1) if($#data1>=0);
	@data1=glob("xzb${fid}.cgi");
	push (@filename, @data1) if($#data1>=0);
	@data1=glob("xzbs${fid}.cgi");
	push (@filename, @data1) if($#data1>=0);
	@data1=glob("ontop${fid}.cgi");
	push (@filename, @data1) if($#data1>=0);
	@data1=glob("lastnum${fid}.cgi");
	push (@filename, @data1) if($#data1>=0);
	@data1=glob("jinghua${fid}.cgi");
	push (@filename, @data1) if($#data1>=0);
#        my $ttarnum1 =$ttarnum-1;
        if($#filename>=0)
        {
        $tar = Archive::Tar->new();
        $tar->add_files(@filename);
        $tar->write("${imagesdir}${tarname}t_${fid}_${ttarnum}.tar");
        }
          	$step="attachement";          
              print qq~
             <p>
             <font color=red><div align=center>��̳�������ϱ�����ϡ��������</div></font>
             <p>
             <div align=center>������2����Զ����У���������û���Զ���ǰ���У����� ���������ļ� ��ť</div>
        ~;   
          }
         }
         
         }#end if filelist>=0
        else
        {
        $step="attachement";          
        print qq~
        <p>
        <font color=red><div align=center>��̳�������ϱ�����ϡ��������</div></font>
        <p>
        <div align=center>������2����Զ����У���������û���Զ���ǰ���У����� ���������ļ� ��ť</div>
        ~;       
        }
        chdir $lbdir;
        goto COMEON;
        }
        else
        {
        $step="tarall" if ($step eq "topic")
        }
        


        ############################

        if (($step eq "attachement")&&(-e "backupattachement.temp")&&($attachement eq "yes"))  #attachement backup
        {
        @untarname=();
        chdir $lbdir;
        
        open(FILE,"backupattachement.temp");
        @filelist=<FILE>;
        chomp @filelist;
        close(FILE);
        
        if ($#filelist>=0)
        
        {
        
        ($aa,$bb)=split(/\./,$filelist[0]);
        ($bb,$fid)=split(/\_/,$aa);
        
        open(FILE,"$filelist[0]");
        @filename=<FILE>;
        chomp @filename;
        close(FILE); 
        @untarname=splice(@filename,$an);
        $currentnum=($#untarname>=0)?$currentnum+$mn:$currentnum+$#filename;
        chdir "${imagesdir}$usrdir/$fid";       
        if ($#filename>=0)
        {
        $tar = Archive::Tar->new();
        $tar->add_files(@filename);
        $tar->write("${imagesdir}${tarname}a_${fid}_${atarnum}.tar");
        }
        $atarnum++;
        chdir $lbdir;
        if ($#untarname>=0)
        {
        open(FILE,">$filelist[0]");
        foreach(@untarname)
        {
        print FILE "$_";
        print FILE "\n";
        }
        close(FILE);
        
        print qq~
        <p>
        <div align=center>������2����Զ����У���������û���Զ���ǰ���У����� ���������ļ� ��ť</div>
        ~;
        } # end untarname>=0
        else
        {
        open(FILE,"backupattachement.temp");
        @filelist=<FILE>;
        chomp @filelist;
        close(FILE);
        shift(@filelist);
        if ($#filelist>=0)
        {
        open(FILE,">backupattachement.temp");
        foreach(@filelist)
        {
          print FILE "$_";
          print FILE "\n";
        }
        close(FILE);
        $atarnum=1;
         print qq~
        <p>
        <div align=center>������2����Զ����У���������û���Զ���ǰ���У����� ���������ļ� ��ť</div>
        ~;
        }
        else 
          {
          	$step="tarall";
          	$skip="yes";          
              print qq~
             <p>
             <font color=red><div align=center>��̳���Ӹ���������ϡ��������</div></font>
             <p>
             <div align=center>������2����Զ����У���������û���Զ���ǰ���У����� ���������ļ� ��ť</div>
        ~;   
          }
         }
        
         }# end filelist
        else
        {
        
        $step="tarall";
        $skip="yes";
        print qq~
        <p>
        <font color=red><div align=center>��̳���Ӹ���������ϡ��������</div></font>
        <p>
        <div align=center>������2����Զ����У���������û���Զ���ǰ���У����� ���������ļ� ��ť</div>
        ~;       
        }
        chdir $lbdir;
        }
       else
        {
        $step="tarall" if ($step eq "attachement")
        }

COMEON:{
        ###################################3
        if (($step eq "tarall")&&($skip ne "yes"))  #make together
        {
        chdir $lbdir;
        @filetodel=glob("back*.temp");
        foreach(@filetodel) {unlink("$_");}
        
               
        if($packall eq "yes")                                                                               
        {
        chdir $imagesdir;
        @filename=glob("${tarname}*.tar");
        unshift(@filename,"tarfilelist.txt");
        $tar = Archive::Tar->new();
        $tar->add_files(@filename);
        $tar->write("${imagesdir}xq${tarname}.tar");
        foreach(@filename)
        {
        unlink("$_");
        }
        if (-e "tarfilelist.txt") {unlink("tarfilelist.txt");}
 
 print qq~     
        <a href=$imagesurl/xq${tarname}.tar>��������ص�����</a><br>
        <a href=$thisprog?action=delete>�����ɾ������<font color=red>��ز���</font></a><Br>
~;        
        }
        else
        {
         chdir $imagesdir;
        @filename=glob("${tarname}*.tar");
        unshift(@filename,"tarfilelist.txt");
       
        foreach $fn (@filename)
         {
             print "<a href=$imagesurl/$fn>�ļ� $fn ��������ص�����</a><br>";
         }
         $nn=$#filename+1;
         print "<p><div align=center><font color=red>���� $nn ���ļ��������غ�ͳһ���ܣ���˽�ԸĶ��������ݻ��ļ������ָ�ʱһ���ϴ�</font></div><p>";       
         print "<a href=$thisprog?action=delete>�����ɾ������<font color=red>��ز���</font></a><Br>";
         print qq~</div>~;
        }
        
        
        
        }

        else
        {

$percent=int(($currentnum/$totalnum)*100);
$percent1=int(100-$percent);


print qq~
       <b>�����С���������</b><p>
       <form action="$thisprog" method=post name=form>
       <input type=hidden name="action" value="backup">
       <input type=hidden name="fn" value="$fn">
       <input type=hidden name="an" value="$an">
       <input type=hidden name="mn" value="$mn">
       <input type=hidden name="un" value="$un">
       <input type=hidden name="mgn" value="$mgn">
       <input type=hidden name="step" value="$step">
       <input type=hidden name="ttarnum" value="$ttarnum">
       <input type=hidden name="packall" value="$packall">
       <input type=hidden name="atarnum" value="$atarnum">
       <input type=hidden name="mtarnum" value="$mtarnum">
       <input type=hidden name="utarnum" value="$utarnum">
       <input type=hidden name="tarname" value="$tarname">
       <input type=hidden name="currentnum" value="$currentnum">
       <input type=hidden name="totalnum" value="$totalnum">
       <input type=hidden name="attachement" value="$attachement">
       <div align=center><input type="submit" name="Submit" value="���������ļ�"></div>
       </p>
      
       <div align=center>
       <b>���ݽ���</b><br>
       (���ݽ������ֵ����Ա����ļ������ļ����еı���,�����Դ���Ϊ���ݻ���ʱ����ƶ�)
       <table width=80% board=0 height=20>
       <tr>
       <td width=$percent% bgcolor=blue></td>
       <td width=$percent1%></td>
       </tr>
       </table>
       
       </div>
        <script>
        setTimeout('document.form.submit()',2000);
        </script>
        ~;
        }


}


print qq~     
       
        </td>
       </tr>
       </tr>
      ~;   



}

sub delete {
   $dirtoopen = "${imagesdir}";
    opendir (DIR, "$dirtoopen"); 
    @filedata = readdir(DIR);
    closedir (DIR);

    @sortedfile = grep(/\.tar$/,@filedata);
    
    foreach $backupfile (@sortedfile){
    
    if (-e "${imagesdir}$backupfile") {
     unlink "${imagesdir}$backupfile";
     print "<tr><td bgcolor=#FFFFFF align=left colspan=2>ɾ�����������ļ�${imagesdir}$backupfile�ɹ�!<br></td></tr>";
    }
}
if (-e "${imagesdir}tarfilelist.txt") {
     unlink "${imagesdir}tarfilelist.txt";
     print "<tr><td bgcolor=#FFFFFF align=left colspan=2>ɾ�����������ļ�${imagesdir}tarfilelist.txt�ɹ�!<br></td></tr>";
    }
print qq~
<tr><td bgcolor=#FFFFFF align=left colspan=2>
<b>���������ļ��Ѿ�ȫ��ɾ��!</b>
</td></tr>
~;

}

print qq~</td></tr></table></body></html>~;
exit;
