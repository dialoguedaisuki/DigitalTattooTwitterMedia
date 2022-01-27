-- 基本情報
create table info (
 	id text PRIMARY KEY, 
 	create_at timestamp,
 	screen_name text,
 	tweet_text text,
 	bio text,
	raw_json text
);

-- 画像
create table image(
  id text, 
  num integer, 
  image bytea, 
  foreign key (id) references info(id)
);