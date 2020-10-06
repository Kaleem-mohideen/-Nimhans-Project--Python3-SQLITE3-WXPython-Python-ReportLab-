

PRAGMA foreign_keys=1;


CREATE TABLE  reportFormats(
	reportId 	INTEGER PRIMARY KEY,
	reportFormat	TEXT NOT NULL/*JSON*/);


CREATE TABLE patientMaster(
	patientId 		INTEGER PRIMARY KEY,
	mobile 			TEXT,
	patientName		TEXT,
	patientDob		DATE,
	patientGender		TEXT CHECK(patientGender in ('M','F'))NOT NULL DEFAULT 'M',
	patientEmail		TEXT);

CREATE TABLE assayMaster(
	assayId 		INTEGER PRIMARY KEY,
	assayName		TEXT UNIQUE NOT NULL,
	assayDescription	TEXT,
	reportId		INTEGER,/*JSON*/
	enabled 		BOOLEAN NOT NULL CHECK(enabled IN (0,1)) DEFAULT 1,
	FOREIGN KEY(reportId) REFERENCES reportFormats(reportId));
CREATE TRIGGER disableAssay
	AFTER UPDATE ON assayMaster
	WHEN NEW.enabled = 0 AND OLD.enabled = 1
		BEGIN
			UPDATE antiBodies SET enabled = 0 WHERE assayId = NEW.assayId;
		END;

CREATE TABLE antiBodies(
	antiBodyId		INTEGER PRIMARY KEY,
	antiBody		TEXT NOT NULL,
	assayId			INTEGER NOT NULL,
	enabled 		BOOLEAN NOT NULL CHECK(enabled IN (0,1)) DEFAULT 1,
	comments		TEXT,
	UNIQUE(antiBodyId, assayId),
	UNIQUE (antiBody, assayId),
	UNIQUE(antiBodyId, antiBody, assayId),
	FOREIGN KEY(assayId) REFERENCES assayMaster(assayId));
CREATE TRIGGER disableAntibody
	AFTER UPDATE ON antiBodies
	WHEN NEW.enabled = 0 AND OLD.enabled = 1
		BEGIN
			UPDATE antiBodyOptions SET enabled = 0 WHERE assayId = NEW.assayId AND antiBodyId = NEW.antibodyId;
		END;

CREATE TABLE antiBodyOptions(
	optionId 		INTEGER PRIMARY KEY,
	assayId			INTEGER NOT NULL,
	antiBodyId		INTEGER NOT NULL,
	optionText		TEXT NOT NULL,
	enabled 		BOOLEAN NOT NULL CHECK(enabled IN (0,1)) DEFAULT 1,
	UNIQUE(optionId, antiBodyId, assayId),
	UNIQUE(assayId, antiBodyId, optionText),
	FOREIGN KEY(antiBodyId, assayId) REFERENCES antiBodies(antiBodyId, assayId));

CREATE TABLE hospitalMaster(
	hospitalName		TEXT PRIMARY KEY,
	enabled			BOOLEAN NOT NULL CHECK(enabled IN(0,1)) DEFAULT 1);


CREATE TABLE departmentMaster(
	departmentName		TEXT PRIMARY KEY,
	enabled			BOOLEAN NOT NULL CHECK(enabled IN(0,1)) DEFAULT 1);

CREATE TABLE labMaster(
	labName			TEXT PRIMARY KEY,
	enabled			BOOLEAN NOT NULL CHECK(enabled IN(0,1)) DEFAULT 1);


CREATE TABLE patientRequest(
	requestId		INTEGER PRIMARY KEY,
	requestTime		DATETIME NOT NULL DEFAULT(datetime('now', 'localtime')),
	patientId 		INTEGER,
	uhid   			TEXT,
	mrd 			TEXT,
	collectionPoint		TEXT,
	hospitalName		TEXT,
	departmentName 		TEXT,
	collectionDate		DATE,
	labReferenceNumber	TEXT,
	reportDate		DATE,
	labName			TEXT,
	reportFile		TEXT,/*FILE NAME OF REPORT TO BE STORED HERE*/
	FOREIGN KEY(labName) REFERENCES labMaster(labName),
	FOREIGN KEY(departmentName) REFERENCES departmentMaster(departmentName),
	FOREIGN KEY(hospitalName) REFERENCES hospitalMaster(hospitalName),
	FOREIGN KEY(patientId) REFERENCES patientMaster(patientId));



CREATE TABLE patientRequestList(
	requestListId		INTEGER PRIMARY KEY,
	requestId		INTEGER NOT NULL,
	assayId			INTEGER NOT NULL,
	UNIQUE (requestId, assayId),
	FOREIGN KEY(requestId) REFERENCES patientRequest(requestId),
	FOREIGN KEY(assayId) REFERENCES assayMaster(assayId));

CREATE TABLE patientReport(
	requestId	INTEGER NOT NULL,
	assayId		INTEGER NOT NULL,
	antiBodyId	INTEGER NOT NULL,
	optionId	INTEGER NOT NULL,
	comments	TEXT,
	updateTime	DATETIME NOT NULL DEFAULT(datetime('now', 'localtime')),
	FOREIGN KEY(optionId, antiBodyId, assayId) REFERENCES antiBodyOptions(optionId, antiBodyId, assayId),
	FOREIGN KEY(requestId, assayId) REFERENCES patientRequestList(requestId, assayId),
	FOREIGN KEY(requestId) REFERENCES patientRequest(requestId),
	FOREIGN KEY(assayId) REFERENCES assayMaster(assayId));


CREATE VIEW viewAssays AS SELECT * FROM assayMaster WHERE enabled = 1;

CREATE VIEW viewAntiBodies AS SELECT * FROM antiBodies WHERE enabled = 1;

CREATE VIEW viewOptions AS SELECT * FROM antiBodyOptions WHERE enabled = 1;

CREATE VIEW viewAntiBodyOptions AS SELECT assay.assayId, assay.assayName, assay.assayDescription, 
					body.antiBodyId, body.antiBody, body.comments,
					options.optionId, options.optionText 
			FROM viewAssays assay LEFT JOIN viewAntiBodies body 
			ON assay.assayId = body.assayId
			LEFT JOIN viewOptions options 
			ON body.assayId = options.assayId AND body.antiBodyId = options.antiBodyId;



CREATE VIEW viewLabs AS SELECT * FROM labMaster WHERE enabled = 1;

CREATE VIEW viewHospitals AS SELECT * FROM hospitalMaster WHERE enabled = 1;

CREATE VIEW viewDepartments AS SELECT * FROM departmentMaster WHERE enabled = 1;

CREATE VIEW viewPendingReports AS  
	SELECT p.requestId AS requestId, a.assayId AS assayId, a.antiBodyId AS antiBodyId FROM 
	patientRequestList p LEFT JOIN viewAntiBodies a ON p.assayId = a.assayId EXCEPT 
	SELECT r.requestId, r.assayId , r.antiBodyId FROM patientReport r;

CREATE VIEW viewPatientRequest AS
	SELECT r.*, p.patientName, p.mobile, p.patientDob, p.patientGender, p.patientEmail 
	FROM patientRequest r LEFT JOIN patientMaster p ON r.patientId = p.patientId;


CREATE VIEW viewPendingPatients AS 
	SELECT p.patientId AS patientId, p.patientName AS patientName, p.patientGender AS patientGender, 
	p.patientDob as patientDob, p.patientEmail as patientEmail,
	r.requestId AS requestId, r.requestTime AS requestTime FROM
	patientMaster p INNER JOIN patientRequest r ON p.patientId = r.patientId WHERE 
	r.requestId IN (SELECT requestId FROM viewPendingReports GROUP BY requestId);

CREATE VIEW viewCompletedPatients AS 
	SELECT p.patientId AS patientId, p.patientName AS patientName, p.patientGender AS patientGender, 
	p.patientDob as patientDob, p.patientEmail as patientEmail,
	r.requestId AS requestId, r.requestTime AS requestTime FROM
	patientMaster p INNER JOIN patientRequest r ON p.patientId = r.patientId WHERE 
	r.requestId NOT IN (SELECT requestId FROM viewPendingReports GROUP BY requestId);


CREATE VIEW viewPendingReportDetails AS 
	SELECT vpr.requestId, vabo.assayId, vabo.assayName, vabo.assayDescription, 
	vabo.antiBodyId, vabo.antiBody, vabo.comments, vabo.optionId, vabo.optionText FROM 
	viewPendingReports vpr LEFT JOIN viewAntiBodyOptions vabo ON 
	vpr.assayId = vabo.assayId AND vpr.antiBodyId = vabo.antiBodyId;

CREATE VIEW viewPatientReport AS 
	SELECT report.requestId, report.assayId, assay.assayName, report.antiBodyId, 
	assay.antiBody, assay.comments, report.optionId, assay.optionText 
	FROM patientReport report INNER JOIN viewAntiBodyOptions assay ON 
	report.assayId = assay.assayId AND report.antiBodyId = assay.antiBodyId AND report.optionId = assay.optionId
	ORDER BY report.assayId, report.antiBodyId, report.optionId;

