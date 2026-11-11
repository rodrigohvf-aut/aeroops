CREATE TABLE public.runways (
    id bigint PRIMARY KEY,
    airport_ident text NOT NULL,
    le_ident text,
    he_ident text,
    length_ft integer,
    width_ft integer,
    surface text,
    lighted smallint,
    closed smallint
);