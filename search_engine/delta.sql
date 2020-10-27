/*alter table movie_details
add constraint unique_name_for_movie unique(name);*/

ALTER TABLE movie_details ADD COLUMN id SERIAL PRIMARY KEY;