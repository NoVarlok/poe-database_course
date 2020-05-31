create extension if not exists dblink;

CREATE OR REPLACE FUNCTION f_create_db(dbname text, username text)
  RETURNS integer AS
$func$
BEGIN

IF EXISTS (SELECT 1 FROM pg_database WHERE datname = dbname) THEN
   RAISE EXCEPTION 'Database already exists'; 
   return 0;
ELSE
   PERFORM dblink_exec('user=postgres password=1111 dbname=' || current_database()   -- current db
                     , 'CREATE DATABASE ' || quote_ident(dbname));
	perform dblink_exec('user=postgres password=1111 dbname=' || quote_ident(dbname)
                     , 'create table ascendancy_table(
							ascendancy_id smallint primary key,
							ascendancy varchar(20) unique not null,
							base_class varchar(15) not null,
							specialization varchar(15) not null,
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
						end;'
					   );
	perform dblink_exec('user=postgres password=1111 dbname=' || quote_ident(dbname)   -- current db
				, format('grant all privileges on all tables in schema public to %I;', username)
					);				   
END IF;
return 1;
END
$func$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION f_delete_db(dbname text)
  RETURNS integer AS
$func$
BEGIN
	perform dblink_exec('user=postgres password=1111 dbname=postgres'
				, format('drop database if exists %I;', dbname)
					);				   
return 1;
END
$func$ LANGUAGE plpgsql;
--select f_create_db('test', 'lab_user');
--select f_delete_db('gui')