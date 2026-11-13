ALTER TABLE public.aircraft_positions
ADD COLUMN source text NOT NULL DEFAULT 'simulated';

ALTER TABLE public.aircraft_positions
ADD CONSTRAINT aircraft_positions_source_valid
CHECK (source IN ('simulated', 'opensky'));