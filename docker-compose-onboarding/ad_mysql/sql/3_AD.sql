use analytics;

create table AD
(
    id           int          null,
    name         varchar(100) null,
    type         varchar(100) null,
    advertiserId int          null,
    constraint AD_pk
        unique (id),
    constraint AD_ADVERTISER_id_fk
        foreign key (advertiserId) references ADVERTISER (id)
);

INSERT INTO analytics.AD (id, name, type, advertiserId) VALUES (1, 'AD1', 'BANNER', 1);
INSERT INTO analytics.AD (id, name, type, advertiserId) VALUES (2, 'AD2', 'VIDEO', 2);
INSERT INTO analytics.AD (id, name, type, advertiserId) VALUES (3, 'AD3', 'AUDIO', 3);
