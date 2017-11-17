drop table if exists people_choices;
drop table if exists people;

create table people (
    username varchar(256) primary key,
    password varchar(256)
);

create table people_choices (
    username varchar(256) primary key,
    recipes json,
    foreign key(username) references people(username)
    on delete cascade on update cascade
);

insert into people(username, password) values('admin', 'password');