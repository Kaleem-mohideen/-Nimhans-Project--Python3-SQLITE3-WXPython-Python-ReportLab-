PRAGMA foreign_keys=1;

INSERT INTO assayMaster(assayName, assayDescription) VALUES 
			('Ana', 'Ana profile'),
			('ANCA', 'ANCA profile'),
			('PANCA', 'PANCA profile');

 
INSERT INTO antiBodies (assayId, antiBody) VALUES (1, 'ana1');
INSERT INTO antiBodies (assayId, antiBody, comments) VALUES(1, 'ana2', 'ana2 comment\nis just terrific');
INSERT INTO antiBodies (assayId, antiBody) VALUES(1, 'ana3');
INSERT INTO antiBodies (assayId, antiBody, comments) VALUES(1, 'ana4', 'ana4 comment\n this is mediocre stuff');
INSERT INTO antiBodies (assayId, antiBody) VALUES(2,'anca1');
INSERT INTO antiBodies (assayId, antiBody, comments) VALUES(2,'anca2', 'anca2 comment\n this is my favourite');
INSERT INTO antiBodies (assayId, antiBody) VALUES(2,'anca3');
INSERT INTO antiBodies (assayId, antiBody, comments) VALUES(3,'Panca1', 'panca1 comment\n this rocks!!!');
INSERT INTO antiBodies (assayId, antiBody, comments) VALUES(3,'Panca2', 'panca2 comment\n hell no!!!');
INSERT INTO antiBodies (assayId, antiBody) VALUES(3,'Panca3');

			
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES
			(1,1, 'Positive +3'),
			(1,1, 'Positive'),
			(1,1, 'Negative'),
			(1,2, 'Positive +3'),
			(1,2, 'Positive'),
			(1,2, 'Negative'),
			(1,3, 'Positive +3'),
			(1,3, 'Positive'),
			(1,3, 'Negative'),
			(1,4, 'Positive +3'),
			(1,4, 'Positive'),
			(1,4, 'Negative'),
			(2,5, 'Positive +3'),
			(2,5, 'Positive'),
			(2,5, 'Negative'),
			(2,6, 'Positive +3'),
			(2,6, 'Positive'),
			(2,6, 'Negative'),
			(2,7, 'Positive +3'),
			(2,7, 'Positive'),
			(2,7, 'Negative'),
			(3,8, 'Positive +3'),
			(3,8, 'Positive'),
			(3,8, 'Negative'),
			(3,9, 'Positive +3'),
			(3,9, 'Positive'),
			(3,9, 'Negative'),
			(3,10, 'Positive +3'),
			(3,10, 'Positive'),
			(3,10, 'Negative');

INSERT INTO hospitalMaster(hospitalName) VALUES
	('Apollo'), ('VMC'), ('VDC');


INSERT INTO departmentMaster(departmentName) VALUES
	('Biochemistry'), ('Ward');


INSERT INTO labMaster(labName) VALUES
	('Microlab'), ('Anand Diagnostics');


INSERT INTO patientMaster(mobile, patientName, patientGender, patientDob, patientEmail) VALUES
	('9384674004', 'Vivek', 'M', '1980-04-17', 'vivek@cpcdiagnostics.in'),
	('8072383129', 'Kaleem', 'M', '1999-05-16', 'kaleemohideen@gmail.com'),
	('9999999999', 'Ashwin', 'M', '1987-02-08', 'ashwin@cpcdiagnostics.in');


INSERT INTO patientRequest(patientId, uhid, mrd, hospitalName, collectionDate) 
			VALUES(1,'123', '456', 'Apollo', '2020-09-24');
INSERT INTO patientRequest(patientId, uhid, mrd, labName, collectionDate, labReferenceNumber) 
			VALUES(2,'234','567', 'Microlab', '2020-09-20', '54321');
INSERT INTO patientRequest(patientId, uhid, mrd, labName, collectionDate, labReferenceNumber) 
			VALUES(3,'345', '678', 'Anand Diagnostics', '2020-09-21', '65432');


INSERT INTO patientRequestList(requestId, assayId) VALUES (1,1),(1,2);

INSERT INTO patientRequestList(requestId, assayId) VALUES (2,2),(2,3);


INSERT INTO patientRequestList(requestId, assayId) VALUES (3,1),(3,3);


