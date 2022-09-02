use analytics;

create table ADVERTISER
(
    id             int          null,
    name           varchar(100) null,
    organisationId int          not null,
    constraint ADVERTISER_pk
        unique (id),
    constraint ADVERTISER_ORGANISATION_id_fk
        foreign key (organisationId) references ORGANISATION (id)
);

INSERT INTO analytics.ADVERTISER (id, name, organisationId) VALUES (1, 'ADV1', 1);
INSERT INTO analytics.ADVERTISER (id, name, organisationId) VALUES (2, 'ADV2', 2);
INSERT INTO analytics.ADVERTISER (id, name, organisationId) VALUES (3, 'ADV3', 3);
