CREATE TABLE IF NOT EXISTS lba.job_offer_content (
    job_offer_id BIGINT PRIMARY KEY
        REFERENCES lba.job_offers(job_offer_id)
        ON DELETE CASCADE,

    title TEXT NOT NULL,
    description TEXT NOT NULL,

    rome_codes TEXT[],
    desired_skills TEXT[],
    to_be_acquired_skills TEXT[],
    access_conditions TEXT[],
    target_diploma_european_level SMALLINT,

    opening_count INTEGER,
    status TEXT NOT NULL,

    publication_created_at TIMESTAMPTZ NOT NULL,
    publication_expiration_at TIMESTAMPTZ NOT NULL
);