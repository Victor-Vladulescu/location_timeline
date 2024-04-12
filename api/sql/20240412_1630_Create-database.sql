/* Connect to RDBMS with PSQL */
CREATE DATABASE location_timeline;

/* \c location_timeline */
CREATE TABLE public.users (
	id		    serial PRIMARY KEY,
    google_id   numeric not null,
	name		varchar not null,
    password    varchar not null,
	last_ping	bigint not null
);

CREATE TABLE public.history (
	id		    bigserial PRIMARY KEY,
	user_id 	int references public.users(id) not null,
	ping		bigint not null,
	latitude	real not null,
	longitude	real not null,
	accuracy	int,
	battery		int,
	charging	boolean
);