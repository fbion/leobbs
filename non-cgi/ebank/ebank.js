<!--
function displaytime()
{
	time = new Date();
	year = time.getYear();
	month = time.getMonth() + 1;
	if (month < 10) month = "0" + month;
	day = time.getDate();
	if (day < 10) day = "0" + day;
	hour = time.getHours();
	if (hour < 10) hour = "0" + hour;
	minute = time.getMinutes();
	if (minute < 10) minute = "0" + minute;
	second = time.getSeconds();
	if (second < 10) second = "0" + second;
	showtime.innerHTML = year + "/" + month + "/" + day + " " + hour + ":" + minute + ":" + second;
	setTimeout("displaytime()", 1000);
}

function btransfriend()
{
	var friend = document.btrans.friends.options[document.btrans.friends.selectedIndex].value;
	if (friend != "") document.btrans.btransuser.value = friend;
}

function postfriend()
{
	var friend = document.post.friends.options[document.post.friends.selectedIndex].value;
	if (friend != "") document.post.postuser.value = friend;
}

clickmmtimes = 1;
function DoKiss()
{
	if (clickmmtimes > 9)
	{
		clickmmtimes = 1;
		if (confirm("��ʲô? ����˼�Լ����? �ȸ��˼���������...\n�� 50 ��Ǯ :) �˼ҿ��Ǳ����е�һ��ŮӴ��"))
		{
			window.open("ebankkiss.cgi", "", "width=118, height=118, resizable=0, scrollbars=no, menubar=no, status=no");
			setTimeout("Refresh()", 2000);
		}
		else
		{
			alert("��, ûǮ�����ݱ�С��? ����...\n����, �������һ�ϳ�ȥ!");
			this.close();
		}
	}
	else
	{
		clickmmtimes++;
	}
}

refreshpage = 0;
function Refresh()
{
	if (refreshpage = 1) this.location.reload();
	refreshpage++;
}
-->