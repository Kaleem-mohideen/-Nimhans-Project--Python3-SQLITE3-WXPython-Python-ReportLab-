

PRAGMA foreign_keys=1;



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
	assayDescription	TEXT);

CREATE TABLE antiBodies(
	antiBodyId		INTEGER PRIMARY KEY,
	antiBody		TEXT NOT NULL,
	assayId			INTEGER NOT NULL,
	FOREIGN KEY(assayId) REFERENCES assayMaster(assayId));


CREATE TABLE patientRequest(
	requestId		INTEGER PRIMARY KEY,
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




