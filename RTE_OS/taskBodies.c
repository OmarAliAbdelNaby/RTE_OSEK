DeclareTask(T1);
DeclareTask(T2);

DeclareEvent(RTE_Event_HeatRegulatorEvent);
DeclareEvent(RTE_Event_SeatHeaterEvent);
DeclareEvent(RTE_Event_HeatingUpdateEvent);
DeclareEvent(RTE_Event_SeatSensorLeftUpdateTimer);
DeclareEvent(RTE_Event_SeatSensorRightUpdateTimer);

TASK(T1)
{
	EventMaskType NewEvent;
	while(true)
	{
		WaitEvent(RTE_Event_HeatRegulatorEvent | RTE_Event_SeatHeaterEvent | RTE_Event_HeatingUpdateEvent);
		GetEvent(T1, &NewEvent);
		ClearEvent(NewEvent);
		if(NewEvent & RTE_Event_HeatRegulatorEvent)
		{
			HeatRegulatorRunnable();
		}
		if(NewEvent & RTE_Event_SeatHeaterEvent)
		{
			SeatHeaterRunnable();
		}
		if(NewEvent & RTE_Event_HeatingUpdateEvent)
		{
			UpdateHeating();
		}
		TerminateTask();
	}
}
TASK(T2)
{
	EventMaskType NewEvent;
	while(true)
	{
		WaitEvent(RTE_Event_SeatSensorLeftUpdateTimer | RTE_Event_SeatSensorRightUpdateTimer);
		GetEvent(T2, &NewEvent);
		ClearEvent(NewEvent);
		if(NewEvent & RTE_Event_SeatSensorLeftUpdateTimer)
		{
			SeatSensorRunnableLeft();
		}
		if(NewEvent & RTE_Event_SeatSensorRightUpdateTimer)
		{
			SeatSensorRunnableRight();
		}
		TerminateTask();
	}
}
