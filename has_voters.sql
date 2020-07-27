SELECT p.state, LISTAGG(DISTINCT r.userid, ',') AS member_ids
FROM reach.tmc__mvo_people p
JOIN reach.tmc__mvo_relationships r ON r.reachid = p.reachid
WHERE p.state != ''
GROUP BY 1
