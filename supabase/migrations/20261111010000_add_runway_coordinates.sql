ALTER TABLE public.runways
    ADD COLUMN le_latitude_deg double precision,
    ADD COLUMN le_longitude_deg double precision,
    ADD COLUMN he_latitude_deg double precision,
    ADD COLUMN he_longitude_deg double precision;