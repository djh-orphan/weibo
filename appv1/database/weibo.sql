/*
 Navicat Premium Data Transfer

 Source Server         : duan
 Source Server Type    : PostgreSQL
 Source Server Version : 110002
 Source Host           : localhost:5432
 Source Catalog        : weibo_fix
 Source Schema         : weibo

 Target Server Type    : PostgreSQL
 Target Server Version : 110002
 File Encoding         : 65001

 Date: 02/08/2021 18:30:01
*/


-- ----------------------------
-- Sequence structure for comm_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "weibo"."comm_seq";
CREATE SEQUENCE "weibo"."comm_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for info_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "weibo"."info_seq";
CREATE SEQUENCE "weibo"."info_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for message_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "weibo"."message_seq";
CREATE SEQUENCE "weibo"."message_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for user_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "weibo"."user_seq";
CREATE SEQUENCE "weibo"."user_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Table structure for comm
-- ----------------------------
DROP TABLE IF EXISTS "weibo"."comm";
CREATE TABLE "weibo"."comm" (
  "id" int8 NOT NULL DEFAULT nextval('"weibo".comm_seq'::regclass),
  "comment_info" text COLLATE "pg_catalog"."default" NOT NULL,
  "comment_date" timestamptz(6) NOT NULL,
  "message_id" int8 NOT NULL,
  "user_id" int8 NOT NULL
)
;

-- ----------------------------
-- Table structure for message
-- ----------------------------
DROP TABLE IF EXISTS "weibo"."message";
CREATE TABLE "weibo"."message" (
  "id" int8 NOT NULL DEFAULT nextval('"weibo".message_seq'::regclass),
  "info" text COLLATE "pg_catalog"."default" NOT NULL,
  "message_date" timestamptz(6) NOT NULL,
  "user_id" int8 NOT NULL,
  "comment_count" int4 DEFAULT 0
)
;

-- ----------------------------
-- Table structure for picture
-- ----------------------------
DROP TABLE IF EXISTS "weibo"."picture";
CREATE TABLE "weibo"."picture" (
  "picturl_url" text COLLATE "pg_catalog"."default" NOT NULL,
  "picture_date" timestamptz(6),
  "message_id" int8 NOT NULL
)
;

-- ----------------------------
-- Table structure for relation
-- ----------------------------
DROP TABLE IF EXISTS "weibo"."relation";
CREATE TABLE "weibo"."relation" (
  "relation_date" timestamptz(0),
  "user_id" int8 NOT NULL,
  "follower_id" int8 NOT NULL
)
;

-- ----------------------------
-- Table structure for transpond
-- ----------------------------
DROP TABLE IF EXISTS "weibo"."transpond";
CREATE TABLE "weibo"."transpond" (
  "message_id" int8 NOT NULL,
  "user_id" int8 NOT NULL,
  "info" text COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Table structure for userinfo
-- ----------------------------
DROP TABLE IF EXISTS "weibo"."userinfo";
CREATE TABLE "weibo"."userinfo" (
  "id" int8 NOT NULL DEFAULT nextval('"weibo".info_seq'::regclass),
  "info" text COLLATE "pg_catalog"."default",
  "picture_url" text COLLATE "pg_catalog"."default",
  "user_id" int8 NOT NULL
)
;

-- ----------------------------
-- Table structure for userpeople
-- ----------------------------
DROP TABLE IF EXISTS "weibo"."userpeople";
CREATE TABLE "weibo"."userpeople" (
  "username" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "email" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "pwd" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "signup_date" timestamptz(0) NOT NULL,
  "reset_date" timestamptz(0),
  "oldpassword" varchar(255) COLLATE "pg_catalog"."default",
  "is_activated" bool,
  "activated_link" text COLLATE "pg_catalog"."default",
  "is_reset" bool NOT NULL DEFAULT false,
  "is_delete" bool NOT NULL DEFAULT false,
  "id" int8 NOT NULL DEFAULT nextval('"weibo".user_seq'::regclass)
)
;

-- ----------------------------
-- Procedure structure for addcomment
-- ----------------------------
DROP PROCEDURE IF EXISTS "weibo"."addcomment"();
CREATE OR REPLACE PROCEDURE "weibo"."addcomment"()
 AS $BODY$
 DECLARE mid int8;
 DECLARE info TEXT;
 DECLARE uid int8;
 DECLARE tt timestamptz;
 DECLARE 
 BEGIN
	-- Routine body goes here...
FOR n IN  1..100000 LOOP
	mid:=1000+n;
	tt:=now();
	FOR i IN  ceil(random()*(50-1)+1)..ceil(random()*(100-50)+50) LOOP
	uid:=1000+i;
	info:='duan'||uid||'发表：这是一条评论';
	INSERT  into comm(comment_info,user_id,message_id,comment_date) VALUES(info,uid,mid,tt);
END LOOP;

END LOOP;

FOR n IN  1..300 LOOP
	mid:=1000+n;
	tt:=now();
	FOR i IN  ceil(random()*(n-1)+1)..ceil(random()*(10-5)+5)+n  LOOP
	uid:=1000+i;
	info:='duan'||uid||'发表：这是一条评论';
	INSERT  into comm(comment_info,user_id,message_id,comment_date) VALUES(info,uid,mid,tt);
END LOOP;

END LOOP;


-- FOR n IN ceil(random()*(2000-1)+1)..ceil(random()*(5000-2000)+2000) LOOP
-- 	mid:=3456+n;
-- 	tt:=TIMESTAMP'2021-07-30 8:00:00.000000';
-- 	FOR i IN  ceil(random()*(10-1)+1)..ceil(random()*(50-10)+10) LOOP
-- 	uid:=1000+i;
-- 	info:='duan'||uid||'发表：这是一条评论';
-- 	INSERT  into "comment"(comment_info,user_id,message_id,comment_time) VALUES(info,uid,mid,tt);
-- END LOOP;
-- 
-- END LOOP;
-- 


END$BODY$
  LANGUAGE plpgsql;

-- ----------------------------
-- Procedure structure for addmessage
-- ----------------------------
DROP PROCEDURE IF EXISTS "weibo"."addmessage"();
CREATE OR REPLACE PROCEDURE "weibo"."addmessage"()
 AS $BODY$
 DECLARE info TEXT;
 DECLARE tt TIMESTAMPTZ;
 DECLARE uid int8;
 BEGIN
	-- Routine body goes here...
FOR id IN  1..2000 LOOP
	uid:=1000+id;
	tt:=now();
	FOR n IN  1..50 LOOP
	info:='Hi,I am duan'||uid||'这是我第'||n||'条消息';
	INSERT INTO message(info,message_date,user_id)VALUES(info,tt,uid);
END LOOP;
END LOOP;

END$BODY$
  LANGUAGE plpgsql;

-- ----------------------------
-- Procedure structure for addrelation
-- ----------------------------
DROP PROCEDURE IF EXISTS "weibo"."addrelation"();
CREATE OR REPLACE PROCEDURE "weibo"."addrelation"()
 AS $BODY$
 DECLARE uid int8;
 DECLARE fid int8;
 BEGIN
	-- Routine body goes here...
FOR n IN  1..2000 LOOP
	uid:=1000+n;
	fid:=ceil(random()*(2999-1001)+1001);
	INSERT into  relation(user_id,follower_id,relation_date)VALUES(uid,fid,now());
	IF mod(uid,25)=0 THEN
	INSERT into  relation(user_id,follower_id,relation_date)VALUES(uid,fid+1,now());
END IF;

END LOOP;


END$BODY$
  LANGUAGE plpgsql;

-- ----------------------------
-- Procedure structure for adduser
-- ----------------------------
DROP PROCEDURE IF EXISTS "weibo"."adduser"();
CREATE OR REPLACE PROCEDURE "weibo"."adduser"()
 AS $BODY$
	DECLARE na VARCHAR;
	DECLARE email VARCHAR;
	DECLARE pw VARCHAR;
	DECLARE tm timestamptz;
 BEGIN
	FOR uid IN 1..2000 LOOP
	na:='duan'||uid;
	email:='duan'||uid||'@163.com';
	pw:=md5(na||'123456');
	tm:=now();			
	INSERT INTO userpeople(username,email,pwd,signup_date)VALUES(na,email,pw,tm);
END LOOP;
END$BODY$
  LANGUAGE plpgsql;

-- ----------------------------
-- Function structure for comtri
-- ----------------------------
DROP FUNCTION IF EXISTS "weibo"."comtri"();
CREATE OR REPLACE FUNCTION "weibo"."comtri"()
  RETURNS "pg_catalog"."trigger" AS $BODY$
	DECLARE mess_id int8;
	BEGIN
	-- Routine body goes here...
		mess_id:=(SELECT message_id from comm WHERE "id"=new."id");
UPDATE message set comment_count=comment_count+1 WHERE "id"=mess_id;
	RETURN null;
END$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

-- ----------------------------
-- Function structure for delnum
-- ----------------------------
DROP FUNCTION IF EXISTS "weibo"."delnum"();
CREATE OR REPLACE FUNCTION "weibo"."delnum"()
  RETURNS "pg_catalog"."trigger" AS $BODY$
	
	DECLARE mess_id int8;
	BEGIN
	-- Routine body goes here...
mess_id:=(SELECT message_id FROM comm WHERE "id"=OLD."id");
UPDATE message SET comment_count=comment_count-1 WHERE "id"=mess_id;
	RETURN OLD;
END$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
SELECT setval('"weibo"."comm_seq"', 5066901, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
SELECT setval('"weibo"."info_seq"', 2, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
SELECT setval('"weibo"."message_seq"', 101001, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
SELECT setval('"weibo"."user_seq"', 3001, true);

-- ----------------------------
-- Indexes structure for table comm
-- ----------------------------
CREATE INDEX "messageid_comm_idx" ON "weibo"."comm" USING hash (
  "message_id" "pg_catalog"."int8_ops"
);
CREATE INDEX "userid_comm_idx" ON "weibo"."comm" USING hash (
  "user_id" "pg_catalog"."int8_ops"
);

-- ----------------------------
-- Triggers structure for table comm
-- ----------------------------
CREATE TRIGGER "comtri" AFTER INSERT ON "weibo"."comm"
FOR EACH ROW
EXECUTE PROCEDURE "weibo"."comtri"();
CREATE TRIGGER "delnum" BEFORE DELETE ON "weibo"."comm"
FOR EACH ROW
EXECUTE PROCEDURE "weibo"."delnum"();

-- ----------------------------
-- Primary Key structure for table comm
-- ----------------------------
ALTER TABLE "weibo"."comm" ADD CONSTRAINT "comm_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table message
-- ----------------------------
CREATE INDEX "userid_message_idx" ON "weibo"."message" USING hash (
  "user_id" "pg_catalog"."int8_ops"
);

-- ----------------------------
-- Primary Key structure for table message
-- ----------------------------
ALTER TABLE "weibo"."message" ADD CONSTRAINT "message_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table picture
-- ----------------------------
CREATE INDEX "messageid_picture_idx" ON "weibo"."picture" USING hash (
  "message_id" "pg_catalog"."int8_ops"
);

-- ----------------------------
-- Primary Key structure for table picture
-- ----------------------------
ALTER TABLE "weibo"."picture" ADD CONSTRAINT "picture_pkey" PRIMARY KEY ("picturl_url", "message_id");

-- ----------------------------
-- Indexes structure for table relation
-- ----------------------------
CREATE INDEX "followerid_relation_idx" ON "weibo"."relation" USING hash (
  "follower_id" "pg_catalog"."int8_ops"
);
CREATE INDEX "userid_relation_idx" ON "weibo"."relation" USING hash (
  "user_id" "pg_catalog"."int8_ops"
);

-- ----------------------------
-- Primary Key structure for table relation
-- ----------------------------
ALTER TABLE "weibo"."relation" ADD CONSTRAINT "relation_pkey" PRIMARY KEY ("user_id", "follower_id");

-- ----------------------------
-- Indexes structure for table transpond
-- ----------------------------
CREATE INDEX "messageid_transpond_idx" ON "weibo"."transpond" USING hash (
  "message_id" "pg_catalog"."int8_ops"
);
CREATE INDEX "userid_transpond_idx" ON "weibo"."transpond" USING hash (
  "user_id" "pg_catalog"."int8_ops"
);

-- ----------------------------
-- Primary Key structure for table transpond
-- ----------------------------
ALTER TABLE "weibo"."transpond" ADD CONSTRAINT "transpond_pkey" PRIMARY KEY ("message_id", "user_id");

-- ----------------------------
-- Indexes structure for table userinfo
-- ----------------------------
CREATE INDEX "userid_userinfo_idx" ON "weibo"."userinfo" USING hash (
  "user_id" "pg_catalog"."int8_ops"
);

-- ----------------------------
-- Primary Key structure for table userinfo
-- ----------------------------
ALTER TABLE "weibo"."userinfo" ADD CONSTRAINT "userinfo_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table userpeople
-- ----------------------------
ALTER TABLE "weibo"."userpeople" ADD CONSTRAINT "userpeople_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Foreign Keys structure for table comm
-- ----------------------------
ALTER TABLE "weibo"."comm" ADD CONSTRAINT "messageid_comm_fkey" FOREIGN KEY ("message_id") REFERENCES "weibo"."message" ("id") ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE "weibo"."comm" ADD CONSTRAINT "userid_comm_fkey" FOREIGN KEY ("user_id") REFERENCES "weibo"."userpeople" ("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table message
-- ----------------------------
ALTER TABLE "weibo"."message" ADD CONSTRAINT "userid_message_fkey" FOREIGN KEY ("user_id") REFERENCES "weibo"."userpeople" ("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table picture
-- ----------------------------
ALTER TABLE "weibo"."picture" ADD CONSTRAINT "messageid_picture_fkey" FOREIGN KEY ("message_id") REFERENCES "weibo"."message" ("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table relation
-- ----------------------------
ALTER TABLE "weibo"."relation" ADD CONSTRAINT "followerid_relation_fkey" FOREIGN KEY ("follower_id") REFERENCES "weibo"."userpeople" ("id") ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE "weibo"."relation" ADD CONSTRAINT "userid_relation_fkey" FOREIGN KEY ("user_id") REFERENCES "weibo"."userpeople" ("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table transpond
-- ----------------------------
ALTER TABLE "weibo"."transpond" ADD CONSTRAINT "messageid_tranpoand_fkey" FOREIGN KEY ("message_id") REFERENCES "weibo"."message" ("id") ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE "weibo"."transpond" ADD CONSTRAINT "userid_transpond_fkey" FOREIGN KEY ("user_id") REFERENCES "weibo"."userpeople" ("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table userinfo
-- ----------------------------
ALTER TABLE "weibo"."userinfo" ADD CONSTRAINT "userid_userinfo_fkey" FOREIGN KEY ("user_id") REFERENCES "weibo"."userpeople" ("id") ON DELETE CASCADE ON UPDATE CASCADE;
