SELECT a_docid, b_docid, sum(product) as similarity
FROM (
  SELECT a.docid AS a_docid, b.docid AS b_docid, a.term, ( a.count * b.count ) AS product
  FROM (
    SELECT * FROM frequency
    UNION SELECT 'query' as docid, 'washington' as term, 1 as count
    UNION SELECT 'query' as docid, 'taxes' as term, 1 as count
    UNION SELECT 'query' as docid, 'treasury' as term, 1 as count
  ) AS a INNER JOIN frequency AS b
  ON a.term = b.term
  WHERE  a.docid = 'query'
)
GROUP BY a_docid, b_docid
ORDER BY similarity DESC
LIMIT 10;

