-- 基本情報
create table info (
 	id bigint PRIMARY KEY, 
 	create_at timestamp,
 	screen_name text,
 	tweet_text text,
 	bio text,
	raw_json text,
	insert_at timestamp
);


-- 画像
create table image(
  id bigint, 
  num integer, 
  image text, 
  foreign key (id) references info(id)
);

-- VIEW
CREATE VIEW infoimage as 
SELECT info.id,
   info.create_at,
   info.screen_name,
   info.tweet_text,
   info.bio,
   image.image,
   image.num,
   info.delflag
  FROM (info JOIN image ON ((info.id = image.id)));