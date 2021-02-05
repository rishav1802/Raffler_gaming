# Raffler_gaming
Schema:
1. User(uid, name)  : UID is primary key

2. Events(eid, edate, Reward) : Eid is primary key

3. Participate(uid, eid) : (uid,eid) : primary key ; uid is foreign key with reference to User uid
eid is foreign key of event eid;

4. winner(Eid, Name, Award) : primary key is eid  ; name is foreign key with reference to User table name and award is foreign key with events table;





