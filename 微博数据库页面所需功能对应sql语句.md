### 微博数据库页面所需功能对应sql语句

#### 登录

- 登录  参数：email，password  成功返回true，失败返回false

```sql
SELECT md5(email||password)=(SELECT pwd from userpeople where email=email); 
```

#### 消息热点、详情显示（显示消息详情、评论）

- 消息详情显示  参数： messageID

```sql
SELECT * from message WHERE "id"=messageID;
```

- 获取评论 参数：messageID

```sql
SELECT * FROM comm WHERE message_id=messageID;
```

- 获取热点  无需参数

```sql
with mess as(SELECT message_id,count(*) as cc from comm GROUP BY message_id ORDER BY count(*) DESC  LIMIT 10)
SELECT message.*,mess.cc FROM message ,mess WHERE message."id"=mess.message_id; 
```

#### 注册

- 注册 参数：email  判断返回是否为空

```sql
select * from userpeople where email=email;
```

#### 密码重置

- 密码重置 参数：email

```sql
update userpeople set is_reset=true,reset_date=now(),oldpw=pwd where email=email;
```

#### 查询界面（根据email查询用户并关注）

- 查询 参数 ：email

```sql
select * from userpeople where email=email;
```

- 关注 参数：想要关注的用户的email, 自己的id

```sql
insert into relation(relation_date,user_id,follower_id)SELECT now(),ID,"id" from userpeople where email=email;
```

#### 获取关注列表、粉丝列表

- 获取关注的人 参数： id or email

```sql
--若参数为id
SELECT * from userpeople WHERE "id" in (SELECT follower_id FROM relation WHERE user_id=id);
--若参数为email
SELECT * from userpeople WHERE "id" in (SELECT follower_id FROM relation WHERE user_id=(SELECT "id" FROM userpeople WHERE email=email));
```

- 获取关注我的人 参数：id or email

```sql
--若参数为id
SELECT * from userpeople WHERE "id" in (SELECT user_id FROM relation WHERE follower_id=id);
--若参数为email
SELECT * from userpeople WHERE "id" in (SELECT user_id FROM relation WHERE follower_id=(SELECT "id" FROM userpeople WHERE email=email));
```

#### 消息列表显示

- 消息列表 参数 id

```sql
--首先获取自己和关注的人发布的所有消息
SELECT * FROM message WHERE user_id in (SELECT follower_id from relation WHERE user_id=id)or user_id=id;
--接着获取自己和关注的人转发的消息
with mess as(SELECT message_id,info,user_id from transpond where user_id in (SELECT follower_id from relation WHERE user_id=id)or user_id=id)
SELECT mess.info,mess.user_id,message.* FROM mess,message where mess.message_id=message.message_id; 
```

#### 发布微博

- 发布 参数： id，info

```sql
insert into message(info,message_date,user_id)values(info,now(),id);
```

#### 个人信息编辑

- 编辑个人信息 参数: id,info,pictureurl

```sql
insert into userinfo(user_id,info,picture_url) values(id,info,picture_url);
```

