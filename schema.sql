drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username text not null,
  role text not null,
  password text not null
);
