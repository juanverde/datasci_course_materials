select count (*) from (select term from frequency where docid = '10398_txt_earn' and count = 1 UNION select term from frequency where docid = '925_txt_trade' and count = 1);
