SELECT Users.[USER_ID],
	   Users.[USER_NAME],
	   Time_Entries.TIME_START,
	   Time_Entries.TIME_END,
	   Time_Entries.[Description] AS [DESCRIPTION],
	   Projects.projectId AS PROJECT_ID,
	   projects.projectName AS PROJECT_NAME,
	   Clients.clientId AS CLIENT_ID,
	   clients.clientName AS CLIENT_NAME
FROM Time_Entries
LEFT JOIN Projects ON Time_Entries.[PROJECT_ID] = Projects.[projectId]
LEFT JOIN Users ON Time_Entries.[USER_ID] = Users.[USER_ID]
LEFT JOIN Clients ON Time_Entries.[CLIENT_ID] = Clients.[clientId]
WHERE Users.[USER_ID] = '6290fc291efa6c3711176bed'
--AND Time_Entries.[DESCRIPTION] LIKE '%Clockify%'
ORDER BY Time_Entries.[TIME_START]