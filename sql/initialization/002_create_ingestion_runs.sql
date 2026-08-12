CREATE TABLE IF NOT EXISTS lba.ingestion_runs (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    kestra_execution_id TEXT NOT NULL UNIQUE,

    source TEXT NOT NULL DEFAULT 'la_bonne_alternance',

    collected_at TIMESTAMPTZ NOT NULL,

    raw_file_path TEXT NOT NULL,

    fetched_offer_count INTEGER NOT NULL
        CHECK (fetched_offer_count >= 0),

    processed_at TIMESTAMPTZ,

    valid_offer_count INTEGER
        CHECK (valid_offer_count >= 0),

    rejected_offer_count INTEGER
        CHECK (rejected_offer_count >= 0)
);