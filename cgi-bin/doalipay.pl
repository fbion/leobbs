#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

    my ($no,$alipayid,$warename,$oldpost,$wareprice,$wareurl,$postage_mail,$postage_express,$postage_ems) = split(/\[ALIPAYE\]/,$$post);
    
    my $zanshi; my $youfei;
    $wareurl = "http://$wareurl" if ($wareurl ne "");
    if ($wareurl ne "") { $zanshi = " ��[<a href=\"$wareurl\">��Ʒչʾ</a>]"; }
    if ($postage_mail ne "" || $postage_express ne "" || $postage_ems ne "") {
	$youfei = "��ҳе��ʷѣ�"; $youfei .= "ƽ�� $postage_mail Ԫ / " if ($postage_mail ne ""); $youfei .= "��� $postage_express Ԫ / " if ($postage_express ne ""); $youfei .= "EMS $postage_ems Ԫ / " if ($postage_ems ne "");
	chop $youfei;chop $youfei;chop $youfei;
    } else {
	$youfei = "���ҳе��ʷ�";
    }

    my $firstline = $oldpost;
    $firstline =~ s/(\[������������.+?��.+?�α༭\])/$1/isg;
    $firstline = $1;
    $oldpost=~ s/\[������������.+?��.+?�α༭\]<br>//isg;

    my $post1 = qq~$firstline<BR><BR>
<B>�������ƣ�</B> $alipayid ��[<a href=https://www.alipay.com/trade/i_credit.do?email=$alipayid target=_blank>�鿴����������</a>] <BR><BR>
<B>��Ʒ���ƣ�</B> $warename$zanshi<BR><BR>
<B>��Ʒ�۸�</B> $wareprice Ԫ<BR><BR>
<B>�ʷ������</B> $youfei<BR><BR>
<B>��Ʒ������</B><BR>
$oldpost<BR><BR>
~;
$warename=uri_escape($warename);
$oldpost=~ s/\[UploadFile.{0,6}=.+?\]//isg; $oldpost = &temppost($oldpost);
$oldpost=uri_escape($oldpost);
$wareurl=uri_escape($wareurl);
$$post = qq~
<a href=https://www.alipay.com/payto:$alipayid?subject=$warename&body=$oldpost&price=$wareprice&url=$wareurl&ordinary_fee=$postage_mail&express_fee=$postage_express&ems_fee=$postage_ems&readonly=true target=_blank><img src=http:\/\/img.alipay.com\/pimg\/button_alipaybutton_o.gif border=0><\/a><BR>
$post1<BR>
<a href=https://www.alipay.com/payto:$alipayid?subject=$warename&body=$oldpost&price=$wareprice&url=$wareurl&ordinary_fee=$postage_mail&express_fee=$postage_express&ems_fee=$postage_ems&readonly=true target=_blank><img src=http:\/\/img.alipay.com\/pimg\/button_alipaybutton_o.gif border=0><\/a><BR>
~;
1;