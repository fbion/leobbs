    if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
        &error("����&��Ļ���Ϊ $jifen��������ֻ̳�л��ִ��ڵ��� $postminjf �Ĳ��ܷ��ԣ�") if ($postminjf > 0 && $jifen < $postminjf);
    }

    if ($payopen eq "no") { &error("��������&�Բ��𣬱���̳��������������"); }

    &error("����&�벻Ҫ���ⲿ���ӱ�����") if (($ENV{'HTTP_REFERER'} !~ /$ENV{'HTTP_HOST'}/i && $ENV{'HTTP_REFERER'} ne '' && $ENV{'HTTP_HOST'} ne '')&&($canotherlink ne "yes"));
    for ('alipayid','warename','wareurl','wareprice','transport','postage_mail','postage_express','postage_ems') {
    next unless defined $_;
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
if(length($inpost)>400){
&error("����&��Ʒ�������ܳ���400���ַ�");
}
&error("����&���Բ����Ϲ涨�ļ۸�")if($wareprice!~/^[0-9\.]+$/i);
&error("����&���Բ����Ϲ涨�ļ۸�")if($postage_mail!~/^[0-9\.]+$/i && $postage_mail ne '');
&error("����&���Բ����Ϲ涨�ļ۸�")if($postage_express!~/^[0-9\.]+$/i && $postage_express ne '');
&error("����&���Բ����Ϲ涨�ļ۸�")if($postage_ems!~/^[0-9\.]+$/i && $postage_ems ne '');

$transport = 's' if ($postage_mail eq "" && $postage_express eq "" && $postage_ems eq "");

if ($transport eq 's') {
    $postage_mail = "";
    $postage_express = "";
    $postage_ems = "";
}

    $alipayid  = lc($alipayid);
    $alipayid =~ s/[\ \a\f\n\e\0\r\t\`\~\!\$\%\^\&\*\(\)\=\+\\\{\}\;\'\:\"\,\/\<\>\?\|]//isg;
    if($alipayid !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,4}|[0-9]{1,4})(\]?)$/) { &error("����&֧�����˺Ŵ���"); }

    $wareurl =~ s/[\a\f\n\e\0\r\t]//isg;
    $wareurl =~ s/^http:\/\///isg;

    $k="\[ALIPAYE\]$alipayid\[ALIPAYE\]$warename\[ALIPAYE\]$inpost\[ALIPAYE\]$wareprice\[ALIPAYE\]$wareurl\[ALIPAYE\]$postage_mail\[ALIPAYE\]$postage_express\[ALIPAYE\]$postage_ems\[ALIPAYE\]";
    $inpost = $k;
    
    require "doaddnewtopic.pl";

1;
