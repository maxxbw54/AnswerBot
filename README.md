# AnswerBot [Tool Demo](http://answerbot.cn/)


## Required Database
```odpsql
drop database if exists `answerbot`;
CREATE DATABASE IF NOT EXISTS `answerbot` DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
```

## Required tables
### postlink

1. Create table
```odpsql
use answerbot;
CREATE TABLE post_links (
    Id INT NOT NULL PRIMARY KEY,  
    CreationDate DATETIME,
    PostId INT,
	RelatedPostId INT,
	LinkTypeId INT
);

load xml local infile '/data/bowen/Post2Vec/data/sources/SO-05-Sep-2018/PostLinks.xml'
into table post_links
rows identified by '<row>';
```

### java_qs

1. Create table
```odpsql
CREATE TABLE java_qs (
    Id INT NOT NULL PRIMARY KEY,
    PostTypeId SMALLINT,
    AcceptedAnswerId INT,
	CreationDate DATETIME,
	Score INT NULL,
	ViewCount INT NULL,
	Body text NULL,
	OwnerUserId INT,
	LastEditorUserId INT,
	LastEditDate DATETIME,
	LastActivityDate DATETIME,
	Title varchar(256),
	Tags VARCHAR(256),
	AnswerCount INT,
	CommentCount INT,
	FavoriteCount INT,
	CommunityOwnedDate DATETIME,
    ParentId INT       
);

# index
create index java_qs_idx on java_qs(Id);
```

2. Insert data
```odpsql
INSERT INTO answerbot.java_qs SELECT * FROM `05-Sep-2018-SO`.posts WHERE Tags LIKE '%<java>%' AND AnswerCount > 0 AND PostTypeId = 1;
```

### java_ans
```odpsql
CREATE TABLE java_ans (
    Id INT NOT NULL PRIMARY KEY,
    PostTypeId SMALLINT,
    AcceptedAnswerId INT,
	CreationDate DATETIME,
	Score INT NULL,
	ViewCount INT NULL,
	Body text NULL,
	OwnerUserId INT,
	LastEditorUserId INT,
	LastEditDate DATETIME,
	LastActivityDate DATETIME,
	Title varchar(256),
	Tags VARCHAR(256),
	AnswerCount INT,
	CommentCount INT,
	FavoriteCount INT,
	CommunityOwnedDate DATETIME,
    ParentId INT       
);

# index
create index java_ans_idx on java_ans(Id);
ALTER TABLE java_ans ADD INDEX pid2(PostTypeId, ParentId);
```

2. Insert data
```odpsql
INSERT INTO answerbot.java_ans select * from `05-Sep-2018-SO`.posts where PostTypeId = 2 AND ParentId in (select Id from `05-Sep-2018-SO`.posts where Tags like '%<java>%' and PostTypeId = 1);
```
