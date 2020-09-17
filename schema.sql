

PRAGMA foreign_keys=1;


CREATE TABLE  reportFormats(
	reportId 	INTEGER PRIMARY KEY,
	reportFormat	TEXT NOT NULL/*JSON*/);
CREATE TABLE patientMaster(
	patientId 		INTEGER PRIMARY KEY,
	mobile 			TEXT,
	patientName		TEXT,
	patientDob		DATE,
	patientGender		TEXT CHECK(patientGender in ('M','F'))NOT NULL,
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
	requestTime		DATETIME NOT NULL DEFAULT(datetime('now')),
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
	updateTime	DATETIME NOT NULL DEFAULT(datetime('now')),
	FOREIGN KEY(optionId, antiBodyId, assayId) REFERENCES antiBodyOptions(optionId, antiBodyId, assayId),
	FOREIGN KEY(requestId, assayId) REFERENCES patientRequestLis(requestId, assayId),
	FOREIGN KEY(requestId) REFERENCES patientRequest(requestId),
	FOREIGN KEY(assayId) REFERENCES assayMaster(assayId));


CREATE VIEW viewEnabledAssays AS SELECT * FROM assayMaster WHERE enabled = 1;

CREATE VIEW viewEnabledAntiBodies AS SELECT * FROM antiBodies WHERE enabled = 1;

CREATE VIEW viewEnabledOptions AS SELECT * FROM antiBodyOptions WHERE enabled = 1;

CREATE VIEW viewAntiBodyOptions AS SELECT assay.assayId, assay.assayName, assay.assayDescription, 
					body.antiBodyId, body.antiBody,
					options.optionId, options.optionText 
			FROM viewEnabledAssays assay LEFT JOIN viewEnabledAntiBodies body 
			ON assay.assayId = body.assayId
			LEFT JOIN viewEnabledOptions options 
			ON body.assayId = options.assayId AND body.antiBodyId = options.antiBodyId;



CREATE VIEW viewLabs AS SELECT * FROM labMaster WHERE enabled = 1;

CREATE VIEW viewHospitals AS SELECT * FROM hospitalMaster WHERE enabled = 1;

CREATE VIEW viewDepartments AS SELECT * FROM departmentMaster WHERE enabled = 1;
