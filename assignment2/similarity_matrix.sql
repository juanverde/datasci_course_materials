SELECT sum(product)
FROM (
  SELECT ( a.count * b.count ) AS product
  FROM frequency AS a inner join frequency AS b
  ON a.term = b.term
  WHERE  a.docid = '10080_txt_crude' AND b.docid = '17035_txt_earn'
);

