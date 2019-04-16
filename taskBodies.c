TASK(T1)
{
	EventMaskType NewEvents;
	while(true)
	{
		WaitEvent(E1 | E2);
		GetEvent(T1, &NewEvents);
		ClearEvent(NewEvents);
		if(NewEvent & E1)
		{
			R1();
		}
		if(NewEvent & E2)
		{
			R2();
		}
	}
}
TASK(T2)
{
	EventMaskType NewEvents;
	while(true)
	{
		WaitEvent(E3 | E4 | None);
		GetEvent(T2, &NewEvents);
		ClearEvent(NewEvents);
		if(NewEvent & E3)
		{
			R3();
		}
		if(NewEvent & E4)
		{
			R4();
		}
		if(NewEvent & None)
		{
			R5();
		}
	}
}
