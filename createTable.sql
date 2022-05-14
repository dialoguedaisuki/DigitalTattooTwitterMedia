-- 基本情報
create table info (
 	id bigint PRIMARY KEY, 
 	create_at timestamp,
 	screen_name text,
 	tweet_text text,
 	bio text,
	raw_json text,
	insert_at timestamp,
	delflag boolean,
  votescore bigint,
  uid bigint,
  post_at timestamp
);


-- 画像
create table image(
  id bigint, 
  num integer, 
  image text, 
  foreign key (id) references info(id)
);

-- RAW VIEW
CREATE VIEW rawinfoimage as 
SELECT info.id,
   info.create_at,
   info.screen_name,
   info.tweet_text,
   info.bio,
   image.image,
   image.num,
   info.delflag,
   image.score,
   info.votescore,
   info.uid
  FROM (info JOIN image ON ((info.id = image.id))); 

-- FILTER VIEW
CREATE VIEW infoimage as 
SELECT info.id,
   info.create_at,
   info.screen_name,
   info.tweet_text,
   info.bio,
   image.image,
   image.num,
   info.delflag,
   image.score,
   info.votescore,
   info.uid
  FROM (info JOIN image ON ((info.id = image.id)))
  WHERE bio NOT LIKE '%成人%' 
  AND bio NOT LIKE '%絵%'
  AND bio NOT LIKE '%創作%'
  AND bio NOT LIKE '%雑多%'
  AND bio NOT LIKE '%TRPG%'
  AND bio NOT LIKE '%転載%'
  AND bio NOT LIKE '%推%'
  AND tweet_text NOT LIKE '%ラフ%'
  AND tweet_text NOT LIKE '%描%'
  AND tweet_text NOT LIKE '%下書%'
  AND score < 1
  AND create_at > now() - interval '1 month';

-- RANKING VIEW
CREATE VIEW ranking as 
SELECT 
  info.id,
  info.create_at,
  info.screen_name,
  info.tweet_text,
  info.bio,
  info.votescore,
  info.uid,
  image.image,
  image.num
FROM (info JOIN image ON ((info.id = image.id)))
WHERE votescore is not null
ORDER BY info.votescore desc, info.id, image.num;


-- ARRIVAL VIEW(post)
CREATE VIEW arrival_post as 
SELECT 
  info.id,
  info.screen_name,
  info.uid,
  info.tweet_text,
  info.bio,
  info.post_at,
  image.image,
  image.num,
  info.votescore
FROM (info JOIN image ON ((info.id = image.id)))
WHERE post_at is not null
ORDER BY post_at desc
LIMIT 100;


-- ARRIVAL VIEW(insert)
CREATE VIEW arrival_insert as 
SELECT 
  info.id,
  info.screen_name,
  info.uid,
  info.tweet_text,
  info.bio,
  info.insert_at,
  image.image,
  image.num,
  info.votescore
FROM (info JOIN image ON ((info.id = image.id)))
WHERE insert_at is not null
ORDER BY insert_at desc
LIMIT 100;
