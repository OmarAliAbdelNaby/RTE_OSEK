/* This file is Auto-Generated to configure the AUTOSAR OS */



/************************** GENERAL CONFIGURATION ***************************/

#define CPU_CLOCK_HZ					16000000
#define OSTICKDURATION					1000
#define NUMBER_OF_EXTENDEDTASK			1
#define NUMBER_OF_BASICTASK				2
#define NUMBER_OF_PRIORITES				1
#define NUMBER_OF_EVENTS				3
#define NUMBER_OF_RESOURCES				4
#define NUMBER_OF_COUNTER				5
#define NUMBER_OF_ALARM					6
#define NUMBER_OF_ISR					7
#define NUMBER_OF_CALLBACK_FUNCTION		0

#define ALARM_CALLBACK					0
#define IDLETASK_STACK_SIZE				128
/**************************** TASK CONFIGURATION ****************************/

#define OS_TASK_NAME_1					T1
#define OS_TASK_PRIORITY_1				3
#define OS_TASK_SCHEDULE_1				1
#define OS_TASK_ACTIVATION_1			128
#define OS_TASK_AUTOSTART_1				FULL
#define OS_TASK_TYPE_1					EXTENDED
#define OS_TASK_SIZE_1					TRUE
#define TASK_1_NUMBER_OF_EVENT_IN_TASK	2
#define TASK_1_NUMBER_OF_RES_IN_TASK	2
#define TASK_1_EVENT_1					Ev1
#define TASK_1_EVENT_2					EV2
#define TASK_1_RESOURCE_1				Res1
#define TASK_1_RESOURCE_2				Res2

#define OS_TASK_NAME_2					T2
#define OS_TASK_PRIORITY_2				2
#define OS_TASK_SCHEDULE_2				1
#define OS_TASK_ACTIVATION_2			128
#define OS_TASK_AUTOSTART_2				FULL
#define OS_TASK_TYPE_2					EXTENDED
#define OS_TASK_SIZE_2					FALSE
#define TASK_2_NUMBER_OF_EVENT_IN_TASK	1
#define TASK_2_NUMBER_OF_RES_IN_TASK	1
#define TASK_2_EVENT_1					Ev2
#define TASK_2_RESOURCE_1				Res2
/*************************** ALARM CONFIGURATION ****************************/

#define OS_ALARM_NAME_1					RTE_Alarm_alarm1
#define AUTOSTART_1						TRUE
#define ALARM_TIME_1					3
#define CYCLE_TIME_1					NULL
#define OS_ALARM_COUNTER_REF_1			RTE_Counter_counter1
#define OS_ALARM_ACTIVATE_TASK_REF_1	T2
#define OS_ALARM_SET_EVENT_REF_1		SETEVENT
#define OS_ALARM_SET_EVENT_TASK_REF_1	RTE_Event_E3
/************************* COUNTER CONFIGURATION ****************************/

#define OS_COUNTER_Name_1					RTE_Counter_counter1
#define OS_COUNTER_TYPE_1					HARDWARE
#define OS_SECONDS_PER_TICK_1				1e-09
#define OS_COUNTER_MAX_ALLOWED_VALUE_1		65535
#define OS_COUNTER_TICKS_PER_BASE_1			1
#define OS_COUNTER_MIN_CYCLE_1				0
/*************************** EVENT CONFIGURATION ****************************/

#define OS_EVENT_NAME_1					RTE_Event_E1
#define OS_EVENT_MASK_1					300

#define OS_EVENT_NAME_2					RTE_Event_E3
#define OS_EVENT_MASK_2					300

#define OS_EVENT_NAME_3					RTE_Event_E4
#define OS_EVENT_MASK_3					300
/************************ RESOURCE CONFIGURATION ****************************/