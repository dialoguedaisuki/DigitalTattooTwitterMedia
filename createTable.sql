-- 基本情報
create table info (
 	id bigint PRIMARY KEY, 
 	create_at timestamp,
 	screen_name text,
 	tweet_text text,
 	bio text,
	raw_json text,
	insert_at timestamp,
	delflag boolean
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
   info.delflag
  FROM (info JOIN image ON ((info.id = image.id))) 

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
   image.score
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
  AND tweet_text NOT LIKE '%下書%';