WITH voterless_users AS
  (SELECT DISTINCT u.userid
   FROM reach.tmc__mvo_users u
   LEFT JOIN reach.tmc__mvo_relationships r ON r.userid = u.userid
   GROUP BY 1
   HAVING COUNT(DISTINCT r.reachid) = 1)
SELECT LISTAGG(DISTINCT userid, ',') AS member_ids
FROM voterless_users
