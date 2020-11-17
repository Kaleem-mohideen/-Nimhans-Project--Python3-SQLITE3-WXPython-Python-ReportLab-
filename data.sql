PRAGMA foreign_keys=1;

INSERT INTO assayMaster(assayName) VALUES ('AANA Profile 3');



INSERT INTO antiBodies (assayId, antiBody) VALUES (1,'nRNP-Sm');
INSERT INTO antiBodies (assayId, antiBody) VALUES (1,'Sm');
INSERT INTO antiBodies (assayId, antiBody) VALUES (1,'SS-A');
INSERT INTO antiBodies (assayId, antiBody) VALUES (1,'Ro-52');
INSERT INTO antiBodies (assayId, antiBody) VALUES (1,'SS-B');
INSERT INTO antiBodies (assayId, antiBody) VALUES (1,'Scl-70');
INSERT INTO antiBodies (assayId, antiBody) VALUES (1,'PM-Scl 100');
INSERT INTO antiBodies (assayId, antiBody) VALUES (1,'Jo-1');
INSERT INTO antiBodies (assayId, antiBody) VALUES (1,'CENP B');
INSERT INTO antiBodies (assayId, antiBody) VALUES (1,'PCNA');
INSERT INTO antiBodies (assayId, antiBody) VALUES (1,'dsDNA');
INSERT INTO antiBodies (assayId, antiBody) VALUES (1,'Nucleosomes');

 

INSERT INTO assayMaster(assayName) VALUES ('Paraneoplastic Antigens Profile');
INSERT INTO antiBodies (assayId, antiBody) VALUES (2,'Anti-Hu ');
INSERT INTO antiBodies (assayId, antiBody) VALUES (2,'Anti-Ri');
INSERT INTO antiBodies (assayId, antiBody) VALUES (2,'Anti-Yo');
INSERT INTO antiBodies (assayId, antiBody) VALUES (2,'Anti-CV-2');
INSERT INTO antiBodies (assayId, antiBody) VALUES (2,'Anti-PNMA2');
INSERT INTO antiBodies (assayId, antiBody) VALUES (2,'Anti-amphiphysin');
INSERT INTO antiBodies (assayId, antiBody) VALUES (2,'Anti - SOX1');
INSERT INTO antiBodies (assayId, antiBody) VALUES (2,'Anti-glial nuclear antibody');
INSERT INTO antiBodies (assayId, antiBody) VALUES (2,'Anti-Tr');
INSERT INTO antiBodies (assayId, antiBody) VALUES (2,'Anti GAD65');
INSERT INTO antiBodies (assayId, antiBody) VALUES (2,'Anti Zic4');
INSERT INTO antiBodies (assayId, antiBody) VALUES (2,'Anti- titin'); 
INSERT INTO antiBodies (assayId, antiBody) VALUES (2,'Anti-Recoverin');


INSERT INTO assayMaster(assayName) VALUES ('Gangliosides Profile IgG');
INSERT INTO antiBodies (assayId, antiBody) VALUES (3, 'GM1');
INSERT INTO antiBodies (assayId, antiBody) VALUES (3, 'GM2');
INSERT INTO antiBodies (assayId, antiBody) VALUES (3, 'GM3');
INSERT INTO antiBodies (assayId, antiBody) VALUES (3, 'GD1a');
INSERT INTO antiBodies (assayId, antiBody) VALUES (3, 'GD1b');
INSERT INTO antiBodies (assayId, antiBody) VALUES (3, 'GT1a');
INSERT INTO antiBodies (assayId, antiBody) VALUES (3, 'GQ1b');

INSERT INTO assayMaster(assayName) VALUES ('Gangliosides Profile IgM');


INSERT INTO antiBodies (assayId, antiBody) VALUES (4, 'GM1');
INSERT INTO antiBodies (assayId, antiBody) VALUES (4, 'GM2');
INSERT INTO antiBodies (assayId, antiBody) VALUES (4, 'GM3');
INSERT INTO antiBodies (assayId, antiBody) VALUES (4, 'GD1a');
INSERT INTO antiBodies (assayId, antiBody) VALUES (4, 'GD1b');
INSERT INTO antiBodies (assayId, antiBody) VALUES (4, 'GT1a');
INSERT INTO antiBodies (assayId, antiBody) VALUES (4, 'GQ1b');

INSERT INTO assayMaster(assayName) VALUES ('Myositis Profile 4G');


INSERT INTO antiBodies (assayId, antiBody) VALUES (5, 'Mi-2α');
INSERT INTO antiBodies (assayId, antiBody) VALUES (5, 'Mi-2β');
INSERT INTO antiBodies (assayId, antiBody) VALUES (5, 'TIF1');
INSERT INTO antiBodies (assayId, antiBody) VALUES (5, 'MDA5');
INSERT INTO antiBodies (assayId, antiBody) VALUES (5, 'NXP2');
INSERT INTO antiBodies (assayId, antiBody) VALUES (5, 'SAE1');
INSERT INTO antiBodies (assayId, antiBody) VALUES (5, 'Ku');
INSERT INTO antiBodies (assayId, antiBody) VALUES (5, 'PM-Scl100');
INSERT INTO antiBodies (assayId, antiBody) VALUES (5, 'PM-Scl75');
INSERT INTO antiBodies (assayId, antiBody) VALUES (5, 'Jo-1');
INSERT INTO antiBodies (assayId, antiBody) VALUES (5, 'SRP');
INSERT INTO antiBodies (assayId, antiBody) VALUES (5, 'PL-7');
INSERT INTO antiBodies (assayId, antiBody) VALUES (5, 'PL-12');
INSERT INTO antiBodies (assayId, antiBody) VALUES (5, 'EJ');
INSERT INTO antiBodies (assayId, antiBody) VALUES (5, 'OJ');
INSERT INTO antiBodies (assayId, antiBody) VALUES (5, 'Ro-52');




INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(1,1, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(1,1, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(1,1, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(1,2, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(1,2, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(1,2, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(1,3, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(1,3, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(1,3, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(1,4, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(1,4, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(1,4, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(1,5, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(1,5, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(1,5, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(1,6, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(1,6, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(1,6, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(1,7, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(1,7, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(1,7, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(1,8, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(1,8, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(1,8, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(1,9, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(1,9, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(1,9, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(1,10, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(1,10, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(1,10, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(1,11, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(1,11, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(1,11, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(1,12, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(1,12, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(1,12, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,13, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,13, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(2,13, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,14, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,14, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(2,14, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,15, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,15, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(2,15, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,16, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,16, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(2,16, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,17, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,17, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(2,17, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,18, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,18, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(2,18, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,19, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,19, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(2,19, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,20, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,20, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(2,20, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,21, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,21, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(2,21, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,22, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,22, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(2,22, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,23, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,23, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(2,23, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,24, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,24, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(2,24, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,25, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(2,25, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(2,25, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(3,26, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(3,26, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(3,26, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(3,27, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(3,27, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(3,27, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(3,28, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(3,28, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(3,28, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(3,29, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(3,29, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(3,29, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(3,30, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(3,30, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(3,30, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(3,31, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(3,31, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(3,31, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(3,32, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(3,32, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(3,32, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(4,33, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(4,33, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(4,33, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(4,34, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(4,34, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(4,34, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(4,35, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(4,35, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(4,35, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(4,36, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(4,36, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(4,36, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(4,37, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(4,37, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(4,37, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(4,38, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(4,38, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(4,38, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(4,39, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(4,39, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(4,39, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,40, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,40, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(5,40, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,41, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,41, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(5,41, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,42, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,42, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(5,42, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,43, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,43, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(5,43, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,44, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,44, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(5,44, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,45, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,45, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(5,45, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,46, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,46, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(5,46, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,47, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,47, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(5,47, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,48, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,48, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(5,48, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,49, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,49, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(5,49, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,50, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,50, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(5,50, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,51, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,51, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(5,51, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,52, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,52, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(5,52, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,53, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,53, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(5,53, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,54, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,54, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(5,54, 'Negative', 1);
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,55, 'Strongly Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText) VALUES(5,55, 'Positive');
INSERT INTO antiBodyOptions(assayId, antiBodyId, optionText, isDefault) VALUES(5,55, 'Negative', 1);
			
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


