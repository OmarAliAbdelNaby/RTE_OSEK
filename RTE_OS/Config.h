/* This file is Auto-Generated to configure the AUTOSAR OS */



/************************** GENERAL CONFIGURATION ***************************/

#define CPU_CLOCK_HZ					16000000
#define OSTICKDURATION					1000
#define NUMBER_OF_EXTENDEDTASK			2
#define NUMBER_OF_BASICTASK				0
#define NUMBER_OF_PRIORITES				2
#define NUMBER_OF_EVENTS				5
#define NUMBER_OF_RESOURCES				0
#define NUMBER_OF_COUNTER				3
#define NUMBER_OF_ALARM					5
#define NUMBER_OF_ISR					0
#define NUMBER_OF_CALLBACK_FUNCTION		0

#define ALARM_CALLBACK					0
#define IDLETASK_STACK_SIZE				128
/**************************** TASK CONFIGURATION ****************************/

#define OS_TASK_NAME_1					T1
#define OS_TASK_PRIORITY_1				3
#define OS_TASK_SCHEDULE_1				FULL
#define OS_TASK_ACTIVATION_1			1
#define OS_TASK_AUTOSTART_1				TRUE
#define OS_TASK_TYPE_1					EXTENDED
#define OS_TASK_SIZE_1					128
#define TASK_1_NUMBER_OF_EVENT_IN_TASK	3
#define TASK_1_NUMBER_OF_RES_IN_TASK	2
#define TASK_1_EVENT_1					RTE_Event_HeatRegulatorEvent
#define TASK_1_EVENT_2					RTE_Event_SeatHeaterEvent
#define TASK_1_EVENT_3					RTE_Event_HeatingUpdateEvent
#define TASK_1_RESOURCE_1				Res1
#define TASK_1_RESOURCE_2				Res2

#define OS_TASK_NAME_2					T2
#define OS_TASK_PRIORITY_2				2
#define OS_TASK_SCHEDULE_2				FULL
#define OS_TASK_ACTIVATION_2			1
#define OS_TASK_AUTOSTART_2				TRUE
#define OS_TASK_TYPE_2					EXTENDED
#define OS_TASK_SIZE_2					128
#define TASK_2_NUMBER_OF_EVENT_IN_TASK	2
#define TASK_2_NUMBER_OF_RES_IN_TASK	1
#define TASK_2_EVENT_1					RTE_Event_SeatSensorLeftUpdateTimer
#define TASK_2_EVENT_2					RTE_Event_SeatSensorRightUpdateTimer
#define TASK_2_RESOURCE_1				Res3
/*************************** ALARM CONFIGURATION ****************************/

#define OS_ALARM_NAME_1					RTE_Alarm_alarm1
#define AUTOSTART_1						TRUE
#define ALARM_TIME_1					NULL
#define CYCLE_TIME_1					1
#define OS_ALARM_COUNTER_REF_1			0
#define OS_ALARM_ACTION_1				SETEVENT
#define OS_ALARM_ACTION_TASK_REF_1		T1
#define OS_ALARM_ACTION_EVENT_REF_1		RTE_Event_HeatRegulatorEvent

#define OS_ALARM_NAME_2					RTE_Alarm_alarm2
#define AUTOSTART_2						TRUE
#define ALARM_TIME_2					NULL
#define CYCLE_TIME_2					1
#define OS_ALARM_COUNTER_REF_2			0
#define OS_ALARM_ACTION_2				SETEVENT
#define OS_ALARM_ACTION_TASK_REF_2		T1
#define OS_ALARM_ACTION_EVENT_REF_2		RTE_Event_SeatHeaterEvent

#define OS_ALARM_NAME_3					RTE_Alarm_alarm3
#define AUTOSTART_3						TRUE
#define ALARM_TIME_3					NULL
#define CYCLE_TIME_3					1
#define OS_ALARM_COUNTER_REF_3			1
#define OS_ALARM_ACTION_3				SETEVENT
#define OS_ALARM_ACTION_TASK_REF_3		T1
#define OS_ALARM_ACTION_EVENT_REF_3		RTE_Event_HeatingUpdateEvent

#define OS_ALARM_NAME_4					RTE_Alarm_alarm4
#define AUTOSTART_4						TRUE
#define ALARM_TIME_4					NULL
#define CYCLE_TIME_4					1
#define OS_ALARM_COUNTER_REF_4			1
#define OS_ALARM_ACTION_4				SETEVENT
#define OS_ALARM_ACTION_TASK_REF_4		T2
#define OS_ALARM_ACTION_EVENT_REF_4		RTE_Event_SeatSensorLeftUpdateTimer

#define OS_ALARM_NAME_5					RTE_Alarm_alarm5
#define AUTOSTART_5						TRUE
#define ALARM_TIME_5					NULL
#define CYCLE_TIME_5					1
#define OS_ALARM_COUNTER_REF_5			2
#define OS_ALARM_ACTION_5				SETEVENT
#define OS_ALARM_ACTION_TASK_REF_5		T2
#define OS_ALARM_ACTION_EVENT_REF_5		RTE_Event_SeatSensorRightUpdateTimer
/************************* COUNTER CONFIGURATION ****************************/

#define OS_COUNTER_Name_1					0
#define OS_COUNTER_TYPE_1					HARDWARE
#define OS_SECONDS_PER_TICK_1				1e-09
#define OS_COUNTER_MAX_ALLOWED_VALUE_1		65535
#define OS_COUNTER_TICKS_PER_BASE_1			1
#define OS_COUNTER_MIN_CYCLE_1				0

#define OS_COUNTER_Name_2					1
#define OS_COUNTER_TYPE_2					HARDWARE
#define OS_SECONDS_PER_TICK_2				1e-09
#define OS_COUNTER_MAX_ALLOWED_VALUE_2		65535
#define OS_COUNTER_TICKS_PER_BASE_2			1
#define OS_COUNTER_MIN_CYCLE_2				0

#define OS_COUNTER_Name_3					2
#define OS_COUNTER_TYPE_3					HARDWARE
#define OS_SECONDS_PER_TICK_3				1e-09
#define OS_COUNTER_MAX_ALLOWED_VALUE_3		65535
#define OS_COUNTER_TICKS_PER_BASE_3			1
#define OS_COUNTER_MIN_CYCLE_3				0
/*************************** EVENT CONFIGURATION ****************************/

#define OS_EVENT_NAME_1					RTE_Event_HeatRegulatorEvent
#define OS_EVENT_MASK_1					300

#define OS_EVENT_NAME_2					RTE_Event_SeatHeaterEvent
#define OS_EVENT_MASK_2					300

#define OS_EVENT_NAME_3					RTE_Event_HeatingUpdateEvent
#define OS_EVENT_MASK_3					300

#define OS_EVENT_NAME_4					RTE_Event_SeatSensorLeftUpdateTimer
#define OS_EVENT_MASK_4					300

#define OS_EVENT_NAME_5					RTE_Event_SeatSensorRightUpdateTimer
#define OS_EVENT_MASK_5					300
/************************ RESOURCE CONFIGURATION ****************************/