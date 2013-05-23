SELECT sum(product)
FROM (
  SELECT ( a.value * b.value ) AS product
  FROM a AS a inner join b AS b
  ON a.col_num = b.row_num
  WHERE  a.row_num = 2 AND b.col_num = 3
);

