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