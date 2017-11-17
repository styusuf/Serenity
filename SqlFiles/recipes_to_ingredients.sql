select * into recipes_index from
(select A.id, json_agg(A.ing::int) as ingredients from (select id, jsonb_array_elements(ingredients)->>'id' as ing from recipes) A group by A.id)B;
