insert into
	content.filmwork (
		id,
		title,
		type,
		creation_date,
		rating,
		created,
		modified
	)
select
	uuid_generate_v4(),
	'some name',
	case
		when RANDOM() < 0.3 then 'movie'
		else 'tv_show'
	end,
	date::DATE,
	floor(random() * 100),
	NOW(),
	NOW()
from
	generate_series(
		'1900-01-01'::DATE,
		'2021-01-01'::DATE,
		'1 hour'::interval
	) date;
