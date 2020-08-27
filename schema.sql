

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

CREATE TABLE antiBodies(
	antiBodyId		INTEGER PRIMARY KEY,
	antiBody		TEXT NOT NULL,
	assayId			INTEGER NOT NULL,
	enabled 		BOOLEAN NOT NULL CHECK(enabled IN (0,1)) DEFAULT 1,
	UNIQUE(antiBodyId, assayId),
	UNIQUE(antiBodyId, antiBody, assayId),
	FOREIGN KEY(assayId) REFERENCES assayMaster(assayId));

CREATE TABLE antiBodyOptions(
	optionId 		INTEGER PRIMARY KEY,
	assayId			INTEGER NOT NULL,
	anitBodyId		INTEGER NOT NULL,
	optionText		TEXT NOT NULL,
	enabled 		BOOLEAN NOT NULL CHECK(enabled IN (0,1)) DEFAULT 1,
	UNIQUE(optionId, antiBodyId, assayId),
	FOREIGN KEY(antiBodyId, assayId) REFERENCES antiBodies(antiBodyId, assayId));



CREATE TABLE patientRequest(
	requestId		INTEGER PRIMARY KEY,
	requestTime		DATETIME NOT NULL DEFAULT(datetime('now')),
	patientId 		INTEGER,
	uhid   			TEXT,
	mrd 			TEXT,
	collectionPoint		TEXT,
	referingHospital	TEXT,
	referingDepartment	TEXT,
	collectionDate		DATE,
	labReferenceNumber	TEXT,
	reportDate		DATE,
	labName			TEXT,
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
	FOREIGN KEY(antiBodyId, antiBody, assayId) REFERENCES antiBodyOptions(antiBodyId, antiBody, assayId),
	FOREIGN KEY(requestId, assayId) REFERENCES patientRequestLis(requestId, assayId),
	FOREIGN KEY(requestId) REFERENCES patientRequest(requestId),
	FOREIGN KEY(assayId) REFERENCES assayMaster(assayId));


