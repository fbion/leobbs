function Search()
{
    var TYPE = document.SEARFORM.type_search.value;	
    var KEY = document.SEARFORM.search_key.value;	
    parseFloat(KEY);
    var j=0;			
    SPINFO = SaveArray;		
    SPNUM = SaveArray.length;	

    if(TYPE == 0)
    { 
	var OPERATOR = document.SEARFORM.key_type.value;	
	if(OPERATOR == 'b')	
	{
	    for(var i=0;i<SPNUM;i++)
	    {
		var InfoA = SPINFO[i].split('|');	
		if(parseFloat(InfoA[2]) > KEY)
		{
		    SearchArray[j] = SPINFO[i];
		    j++;
		}
            }
	}
	else if(OPERATOR == 's')	
	{
	    for(var i=0;i<SPNUM;i++)
	    {
		var InfoA = SPINFO[i].split('|');

		if(parseFloat(InfoA[2]) < KEY)
		{
		    SearchArray[j] = SPINFO[i];
		    j++;
		}
            }
	}
	else	
	{
	    for(var i=0;i<SPNUM;i++)
	    {
		var InfoA = SPINFO[i].split('|');
		if(parseFloat(InfoA[2]) == KEY)
		{
		    SearchArray[j] = SPINFO[i];
		    j++;
		}
            }
	}
    }
    else if(TYPE == 1)
    { 
	for(i=0;i<SPNUM;i++)
	{
	    var InfoA = SPINFO[i].split('|');
	    if(InfoA[3] == KEY)
	    {
		SearchArray[j] = SPINFO[i];
		j++;
	    }
        }
    }
    else if(TYPE == 2)
    { 
	for(i=0;i<SPNUM;i++)
	{
	    var InfoA = SPINFO[i].split('|');
	    if(InfoA[1] == KEY)
	    {
		SearchArray[j] = SPINFO[i];
		j++;
	    }
        }
    }

    if(j < 1)
    {
	alert("��Ǹ����������Ҫ���������ݣ�");
	return;
    }
    else
	alert("������ "+j+" ������Ҫ�����Ʒ��");

    SPINFO = SearchArray;	
    SPNUM = j;			
    SPInfo(0);
}