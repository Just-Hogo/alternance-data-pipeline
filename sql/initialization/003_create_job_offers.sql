CREATE TABLE IF NOT EXISTS lba.job_offers (
    job_offer_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    source TEXT NOT NULL DEFAULT 'la_bonne_alternance',
    source_offer_id TEXT NOT NULL,

    partner_label TEXT,
    partner_job_id TEXT,

    workplace_name TEXT,
    workplace_legal_name TEXT,
    workplace_address TEXT,

    apply_url TEXT,
    apply_phone TEXT,

    contract_start TIMESTAMPTZ,
    contract_types TEXT[],

    is_delegated BOOLEAN NOT NULL,

    CONSTRAINT job_offers_source_offer_unique
        UNIQUE (source, source_offer_id)
);