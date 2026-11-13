CREATE TABLE public.aircraft_positions (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    icao24 text NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    observed_at timestamptz NOT NULL,

    CONSTRAINT aircraft_positions_icao24_observed_at_unique
        UNIQUE (icao24, observed_at),

    CONSTRAINT aircraft_positions_latitude_valid
        CHECK (latitude BETWEEN -90 AND 90),

    CONSTRAINT aircraft_positions_longitude_valid
        CHECK (longitude BETWEEN -180 AND 180)
);