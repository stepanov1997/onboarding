create schema analytics;
use analytics;

create table ORGANISATION
(
    id          int          null,
    name        varchar(100) null,
    website     varchar(500) null,
    description varchar(500) null,
    constraint ORGANISATION_pk
        unique (id)
);

INSERT INTO analytics.ORGANISATION (id, name, website, description) VALUES (1, 'Coca Cola', 'www.cocacola.ba', 'asxsaxas');
INSERT INTO analytics.ORGANISATION (id, name, website, description) VALUES (2, 'Marbo', 'www.chipsy.com', 'cscdsc');
INSERT INTO analytics.ORGANISATION (id, name, website, description) VALUES (3, 'Pepsi', 'www.pepsi.com', 'xsaxa');
INSERT INTO analytics.ORGANISATION (id, name, website, description) VALUES (4, 'Nike', 'www.nike.rs', 'xsaxasx');
