-- Recherche par date de début du contrat
CREATE INDEX IF NOT EXISTS idx_job_offers_contract_start
    ON lba.job_offers (contract_start);

-- Recherche dans le tableau des types de contrats
CREATE INDEX IF NOT EXISTS idx_job_offers_contract_types
    ON lba.job_offers
    USING GIN (contract_types);

-- Filtrage par date d’expiration
CREATE INDEX IF NOT EXISTS idx_job_offer_content_expiration
    ON lba.job_offer_content (publication_expiration_at);

-- Filtrage par niveau de diplôme
CREATE INDEX IF NOT EXISTS idx_job_offer_content_diploma_level
    ON lba.job_offer_content (target_diploma_european_level);

-- Recherche dans les codes ROME
CREATE INDEX IF NOT EXISTS idx_job_offer_content_rome_codes
    ON lba.job_offer_content
    USING GIN (rome_codes);