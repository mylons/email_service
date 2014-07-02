drop table if exists email;
create table email (
    '{"to1": "fake@example.com", "to_name2": "Ms. Fake", "from": "noreply@uber.com", "from_name": "Uber", "subject": "A Message from Uber", "body": "<h1>Your Bill</h1><p>$10</p>"}'
    email_id integer primary key autoincrement,
    to_email string not null,
    to_name string not null,
    from_email string not null,
    from_name string not null,
    subject text not null,
    body text not null,
    sent boolean not null
);