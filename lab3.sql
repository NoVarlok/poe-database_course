drop table if exists ascendancy_table cascade;
drop table if exists character_table;

create table ascendancy_table(
	ascendancy_id smallint primary key,
	ascendancy varchar(20) unique not null,
	base_class varchar(15) not null,
	specializaion varchar(15) not null,
	ascendancy_popularity integer default 0
);

create table character_table(
	name varchar(15) primary key,
	lvl smallint not null check(lvl > 0 and lvl <= 100),
	life integer not null check(life > 0),
	energy_shield integer not null check(energy_shield >= 0),
	ascendancy_id smallint not null references ascendancy_table on delete cascade,
	main_skill varchar(20) not null
);

begin;
CREATE INDEX base_class_index
    ON ascendancy_table USING btree
    (base_class ASC NULLS LAST);
end;

begin;
CREATE INDEX main_skill_index
    ON character_table USING btree
    (main_skill ASC NULLS LAST);
end;

create or replace function calc_ascendancy_popularity() returns trigger as $$
begin
if (TG_OP = 'DELETE') then
	update ascendancy_table set ascendancy_popularity = ascendancy_popularity - 1
	where ascendancy_id = old.ascendancy_id;
	return old;
elsif (TG_OP = 'UPDATE') then
	update ascendancy_table set ascendancy_popularity = ascendancy_popularity - 1
	where ascendancy_id = old.ascendancy_id;
	update ascendancy_table set ascendancy_popularity = ascendancy_popularity + 1
	where ascendancy_id = new.ascendancy_id;
	return new;
elsif (TG_OP = 'INSERT') then
	update ascendancy_table set ascendancy_popularity = ascendancy_popularity + 1
	where ascendancy_id = new.ascendancy_id;
	return new;
elsif (TG_OP = 'TRUNCATE') then
	update ascendancy_table set ascendancy_popularity = 0;
end if;
return null;
end;
$$ language plpgsql;

create trigger popularity_trigger
after insert or update or delete on character_table
for each row
execute procedure calc_ascendancy_popularity();

create trigger truncate_popularity_trigger
after truncate on character_table
execute procedure calc_ascendancy_popularity();

insert into ascendancy_table values
(1, 'slayer', 'duelist', 'normal'),
(2, 'saboteur', 'shadow', 'mines');

insert into character_table values
('kekw', 100, 5000, 20, 1, 'cyclone'),
('pogchamp', 99, 1500, 7500, 2, 'arc mine'),
('lul', '75', 1, 9000, 2, 'ball of lightning'),
('zulul', '75', 1, 9000, 2, 'ball of lightning');

-- select * from ascendancy_table;

-- delete from character_table
-- where name = 'zulul' or name = 'pogchamp';

-- update character_table set ascendancy_id = 2 where asceddancy_id = 1;

-- select * from character_table;

create or replace procedure add_character(name text, lvl integer, life integer, energy_shield integer, ascendancy_id integer, main_skill text)
language plpgsql 
as $$
begin
insert into character_table values (name, lvl, life, energy_shield, ascendancy_id, main_skill);
end;
$$;

create or replace procedure add_ascendancy(ascendancy_id integer, ascendancy text, base_class text, specializaion text)
language plpgsql 
as $$
begin
insert into ascendancy_table values (ascendancy_id, ascendancy, base_class, specializaion);
end;
$$;

call add_ascendancy(3, 'raider', 'ranger', 'bows');

select * from ascendancy_table;

create or replace procedure delete_character_table()
language plpgsql
as $$
begin
truncate character_table;
end;
$$;

create or replace procedure delete_ascendancy_table()
language plpgsql
as $$
begin
truncate ascendancy_table cascade;
end;
$$;

-- create or replace function show_all() returns table(name varchar, lvl smallint, life integer, energy_shield integer, main_skill varchar, ascendancy_id smallint, ascendancy varchar, base_class varchar, specializaion varchar, ascendancy_popularity integer) as $$
-- begin
-- return query select (character_table.name, character_table.lvl, character_table.life, character_table.energy_shield, character_table.main_skill, character_table.ascendancy_id, ascendancy_table.ascendancy, ascendancy_table.base_class, ascendancy_table.specializaion, ascendancy_table.ascendancy_popularity) from character_table join ascendancy_table on  ascendancy_table.ascendancy_id = character_table.ascendancy_id;
-- end;
-- $$ language plpgsql;

create or replace function show_all() returns table(name varchar, lvl smallint, life integer, energy_shield integer, main_skill varchar, ascendancy_id smallint, ascendancy varchar, base_class varchar, specializaion varchar, ascendancy_popularity integer) as $$
begin
return query select character_table.name, character_table.lvl, character_table.life, character_table.energy_shield, character_table.main_skill, ascendancy_table.ascendancy_id, ascendancy_table.ascendancy, ascendancy_table.base_class, ascendancy_table.specializaion, ascendancy_table.ascendancy_popularity from character_table join ascendancy_table on ascendancy_table.ascendancy_id = character_table.ascendancy_id;
end;
$$ language plpgsql;


create or replace function show_character_table() returns table(name varchar, lvl smallint, life integer, energy_shield integer, ascendancy_id smallint, main_skill varchar) as $$
begin
return query select character_table.name, character_table.lvl, character_table.life, character_table.energy_shield, character_table.ascendancy_id, character_table.main_skill from character_table;
end;
$$ language plpgsql;


create or replace function show_ascendancy_table() returns table(ascendancy_id smallint, ascendancy varchar, base_class varchar, specializaion varchar, ascendancy_popularity integer) as $$
begin
return query select ascendancy_table.ascendancy_id, ascendancy_table.ascendancy, ascendancy_table.base_class, ascendancy_table.specializaion, ascendancy_table.ascendancy_popularity from ascendancy_table;
end;
$$ language plpgsql;

create or replace function base_class_search(search_base_class text) returns table(ascendancy_id smallint, ascendancy varchar, base_class varchar, specializaion varchar, ascendancy_popularity integer) as $$
begin
return query select ascendancy_table.ascendancy_id, ascendancy_table.ascendancy, ascendancy_table.base_class, ascendancy_table.specializaion, ascendancy_table.ascendancy_popularity from ascendancy_table where ascendancy_table.base_class = search_base_class;
end;
$$ language plpgsql;


create or replace function base_class_search_all(search_base_class text) returns table(name varchar, lvl smallint, life integer, energy_shield integer, main_skill varchar, ascendancy_id smallint, ascendancy varchar, base_class varchar, specializaion varchar, ascendancy_popularity integer) as $$
begin
return query select character_table.name, character_table.lvl, character_table.life, character_table.energy_shield, character_table.main_skill, ascendancy_table.ascendancy_id, ascendancy_table.ascendancy, ascendancy_table.base_class, ascendancy_table.specializaion, ascendancy_table.ascendancy_popularity from character_table join ascendancy_table on ascendancy_table.ascendancy_id = character_table.ascendancy_id where ascendancy_table.base_class = search_base_class;
end;
$$ language plpgsql;

create or replace function main_skill_search(search_main_skill text) returns table(name varchar, lvl smallint, life integer, energy_shield integer, ascendancy_id smallint, main_skill varchar) as $$
begin
return query select character_table.name, character_table.lvl, character_table.life, character_table.energy_shield, character_table.ascendancy_id, character_table.main_skill from character_table where character_table.main_skill = search_main_skill;
end;
$$ language plpgsql;

create or replace function main_skill_search_all(search_main_skill text) returns table(name varchar, lvl smallint, life integer, energy_shield integer, main_skill varchar, ascendancy_id smallint, ascendancy varchar, base_class varchar, specializaion varchar, ascendancy_popularity integer) as $$
begin
return query select character_table.name, character_table.lvl, character_table.life, character_table.energy_shield, character_table.main_skill, ascendancy_table.ascendancy_id, ascendancy_table.ascendancy, ascendancy_table.base_class, ascendancy_table.specializaion, ascendancy_table.ascendancy_popularity from character_table join ascendancy_table on ascendancy_table.ascendancy_id = character_table.ascendancy_id where character_table.main_skill = search_main_skill;
end;
$$ language plpgsql;

create or replace procedure delete_by_skill(delete_main_skill text)
language plpgsql
as $$
begin
delete from character_table where character_table.main_skill = delete_main_skill;
end;
$$;

create or replace procedure delete_character(character_name text)
language plpgsql
as $$
begin
delete from character_table where character_table.name = character_name;
end;
$$;

create or replace procedure delete_ascendancy(id integer)
language plpgsql
as $$
begin
delete from ascendancy_table where ascendancy_table.ascendancy_id = id;
end;
$$;

create or replace procedure update_ascendancy_table(id integer, new_ascendancy text, new_base_class text, new_specializaion text)
language plpgsql
as $$
begin
if (new_ascendancy != '') then
	update ascendancy_table set ascendancy = new_ascendancy where ascendancy_id = id;
end if;
if (new_base_class != '') then
	update ascendancy_table set base_class = new_base_class where ascendancy_id = id;
end if;
if (new_specializaion != '') then
	update ascendancy_table set specializaion = new_specializaion where ascendancy_id = id;
end if;
end;
$$;

create or replace procedure update_character_table(upt_name text, new_lvl integer, new_life integer, new_energy_shield integer, new_ascendancy_id integer, new_main_skill text)
language plpgsql
as $$
begin
if (new_lvl != -1) then
	update character_table set lvl = new_lvl where name = upt_name;
end if;
if (new_life != -1) then
	update character_table set life = new_life where name = upt_name;
end if;
if (new_energy_shield != -1) then
	update character_table set energy_shield = new_energy_shield where name = upt_name;
end if;
if (new_ascendancy_id != -1) then
	update character_table set ascendancy_id = new_ascendancy_id where name = upt_name;
end if;
if (new_main_skill != '') then
	update character_table set main_skill = new_main_skill where name = upt_name;
end if;
end;
$$;

call update_character_table('kekw', -1, -1, 1000, 2, '');

select * from character_table;
select * from ascendancy_table;

grant all privileges on all tables in schema public to lab_user;



