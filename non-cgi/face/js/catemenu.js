//3FACE ��Ʒ���������˵�����
 var h;
 var w;
 var l;
 var t;
 var topMar = 1;
 var leftMar = 0;
 var space = 1;
 var isvisible;

function mOverNav(navTD, caption)
{
	if (!navTD.contains(event.fromElement))
	{navTD.style.backgroundColor='#EEEEEE';}
}
function mOutNav(navTD, caption)
{
	if (!navTD.contains(event.toElement))
	{navTD.style.backgroundColor='#FFFFFF';}
}

function _HideMenu() 
{
 var mX;
 var mY;
 var vDiv;
 var mDiv;
 if (isvisible == true)
 {
	vDiv = document.all("_menuDiv");
	mX = window.event.clientX + document.body.scrollLeft;
	mY = window.event.clientY + document.body.scrollTop;
	if ((mX < parseInt(vDiv.style.left)) || (mX > parseInt(vDiv.style.left)+vDiv.offsetWidth) || (mY < parseInt(vDiv.style.top)-h) || (mY > parseInt(vDiv.style.top)+vDiv.offsetHeight)){
		vDiv.style.visibility = "hidden";
		_Search.style.visibility = "visible";
		isvisible = false;
	}
 }
}

function ShowMenu(vMnuCode,tWidth) {
	vSrc = window.event.srcElement;
	vMnuCode = "<table id='submenu' cellspacing=1 cellpadding=3 style='width:"+tWidth+"' bgcolor=#A0BCE7 border=0 onmouseout='_HideMenu()'>" + vMnuCode + "</table>";

	h = vSrc.offsetHeight;
	w = vSrc.offsetWidth;
	l = vSrc.offsetLeft + leftMar;
	t = vSrc.offsetTop + topMar + h + space;
	vParent = vSrc.offsetParent;
	while (vParent.tagName.toUpperCase() != "BODY")
	{
		l += vParent.offsetLeft;
		t += vParent.offsetTop;
		vParent = vParent.offsetParent;
	}
	_Search.style.visibility = "hidden";
	_menuDiv.innerHTML = vMnuCode;
	_menuDiv.style.top = t;
	_menuDiv.style.left = l;
	_menuDiv.style.visibility = "visible";
	isvisible = true;
}

//������
var MENU2 = "<tr onMouseOut=\"mOutNav(this, '')\" onMouseOver=\"mOverNav(this, '1')\" bgcolor='#FFFFFF'><td> <span onClick=DispSubMenu('2'); onMouseOver=DispSubMenu1('2'); style=cursor:hand; title='��ѣ����'>��ѣ����</span></td></tr>"

//�·���
var MENU3 = "<tr onMouseOut=\"mOutNav(this, '')\" onMouseOver=\"mOverNav(this, '1')\" bgcolor='#FFFFFF'><td> <span onClick=DispSubMenu('8'); onMouseOver=DispSubMenu1('8'); style=cursor:hand; title='��ȹ'>��ȹ</span></td></tr><tr onMouseOut=\"mOutNav(this, '')\" onMouseOver=\"mOverNav(this, '1')\" bgcolor='#FFFFFF'><td> <span onClick=DispSubMenu('9'); onMouseOver=DispSubMenu1('9'); style=cursor:hand; title='����'>����</span></td></tr>"

//ͷ����
var MENU4 = "<tr onMouseOut=\"mOutNav(this, '')\" onMouseOver=\"mOverNav(this, '1')\" bgcolor='#FFFFFF'><td> <span onClick=DispSubMenu('14'); onMouseOver=DispSubMenu1('14'); style=cursor:hand; title='�沿����'>�沿����</span></td></tr><tr onMouseOut=\"mOutNav(this, '')\" onMouseOver=\"mOverNav(this, '1')\" bgcolor='#FFFFFF'><td> <span onClick=DispSubMenu('18'); onMouseOver=DispSubMenu1('18'); style=cursor:hand; title='����'>����</span></td></tr><tr onMouseOut=\"mOutNav(this, '')\" onMouseOver=\"mOverNav(this, '1')\" bgcolor='#FFFFFF'><td> <span onClick=DispSubMenu('20'); onMouseOver=DispSubMenu1('20'); style=cursor:hand; title='ñ��'>ñ��</span></td></tr><tr onMouseOut=\"mOutNav(this, '')\" onMouseOver=\"mOverNav(this, '1')\" bgcolor='#FFFFFF'><td> <span onClick=DispSubMenu('21'); onMouseOver=DispSubMenu1('21'); style=cursor:hand; title='�۾�'>�۾�</span></td></tr>"

//�����
var MENU5 = "<tr onMouseOut=\"mOutNav(this, '')\" onMouseOver=\"mOverNav(this, '1')\" bgcolor='#FFFFFF'><td> <span onClick=DispSubMenu('10'); onMouseOver=DispSubMenu1('10'); style=cursor:hand; title='����Ʒ'>����Ʒ</span></td></tr><tr onMouseOut=\"mOutNav(this, '')\" onMouseOver=\"mOverNav(this, '1')\" bgcolor='#FFFFFF'><td> <span onClick=DispSubMenu('23'); onMouseOver=DispSubMenu1('23'); style=cursor:hand; title='����'>����</span></td></tr>"



function displayMenu()
{
    s = "<table cellspacing=0 cellpadding=0 border=0><tr align=center><td><span style='width=80;cursor: hand;' onMouseOver='ShowMenu(MENU2,80)' title='���ָ����ı���ͼƬ1'>������</span></td><td><span style='width=80;cursor: hand;' onMouseOver='ShowMenu(MENU3,80)' title='���ºͿ�ȹ'>�·���</span></td><td><span style='width=80;cursor: hand;' onMouseOver='ShowMenu(MENU4,80)' title='�������͡��ڱǡ����ӡ�ñ�ӡ��۾���'>ͷ����</span></td><td><span style='width=80;cursor: hand;' onMouseOver='ShowMenu(MENU5,80)' title='������Ʒ'>�����</span></td></tr></table>";
    document.write(s);
}
