select count(*) from (select sum(count) as total from frequency group by docid) where total > 300;
