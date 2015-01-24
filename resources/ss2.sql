 
 
Create TABLE dbo.response_code(  
id int NOT NULL PRIMARY KEY CLUSTERED,  
response varchar(25) 
);  
 
insert into dbo.response_code (id, response) values(0, 'Allow');  
insert into dbo.response_code (id, response) values(1, 'Monitor');  
insert into dbo.response_code (id, response) values(2, 'Captcha');  
insert into dbo.response_code (id, response) values(3, 'Block');  
insert into dbo.response_code (id, response) values(4, 'FeedFakeData');  
 
 
Create TABLE dbo.subscriber (  
 
internal_sid int NOT NULL PRIMARY KEY CLUSTERED,  
external_sid varchar(75),  
 
 
name  varchar(256),  
address1 varchar(500),  
address2 varchar(500),  
phone1 varchar(25),  
phone2 varchar(25),  
email  varchar(500),  
status int,  
timezone varchar(10),  
 
 
r_browserIntgrity int,  
r_httpRequestIntegrity int,  
r_Aggregator int,  
r_behaviourIntegrity int,   
 
r_Pagepermin int,  
r_pagepersess  int,  
r_sesslength  int,  
 
Pagepermin int,  
pagepersess int,  
sesslength int,  
 
 
FOREIGN KEY (r_browserIntgrity) REFERENCES response_code(id),  
FOREIGN KEY (r_httpRequestIntegrity) REFERENCES response_code(id),  
FOREIGN KEY (r_Aggregator) REFERENCES response_code(id),  
FOREIGN KEY (r_behaviourIntegrity) REFERENCES response_code(id),  
FOREIGN KEY (r_Pagepermin) REFERENCES response_code(id),  
FOREIGN KEY (r_pagepersess) REFERENCES response_code(id),  
FOREIGN KEY (r_sesslength) REFERENCES response_code(id) 
);  
 
 
Create TABLE dbo.RulesSummary (  
sid  int,  
dt  date,  
hr  int,  
 
r_browserIntgrity bigint,  
r_httpRequestIntegrity bigint,  
r_Aggregator bigint,  
r_behaviourIntegrity bigint,  
r_Ratelimiting bigint,  
 
genuineusers    bigint,  
trustedbots   bigint,    
badbots   bigint,  
   
monitor    bigint,  
captcha    bigint,  
block    bigint,  
feedfakedata bigint,  
 
all_js    bigint,  
all_api    bigint, 
 
CONSTRAINT pk_rulessummaryperhour PRIMARY KEY clustered (sid, dt, hr) , 
FOREIGN KEY (sid) REFERENCES subscriber(internal_sid),  
 
);   
 
Create TABLE dbo.IPDetails(   
IP_FROM bigint,  
IP_TO bigint,  
country_code CHAR(2),  
country_name VARCHAR(64),  
isp VARCHAR(255),  
domain VARCHAR(128) , 
 
CONSTRAINT pk_IPDetails PRIMARY KEY clustered (IP_FROM , IP_TO)  
 
)  
 
 
Create TABLE dbo.IPaddressAccesslist (  
sid int,  
ipaddress varchar(50), 
accessstatus varchar(20), 
 
CONSTRAINT pk_IPaddressAccesslist PRIMARY KEY clustered (sid, ipaddress) , 
FOREIGN KEY (sid) REFERENCES subscriber(internal_sid),  
 
);  
 
Create TABLE dbo.IPAnalysis(  
 
sid int, 
dt date, 
ipaddress varchar(50), 
 
totalrequests bigint,  
browserIntgrity bigint,  
httpRequestIntegrity bigint,  
Aggregator bigint,  
behaviourIntegrity bigint,  
Ratelimiting bigint,  
 
genuinerequests bigint  
 
CONSTRAINT pk_IPAnalysis PRIMARY KEY clustered (sid, dt, ipaddress), 
 
); 
 
 
 
 
 
