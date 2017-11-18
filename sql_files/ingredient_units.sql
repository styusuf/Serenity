select * into ingredient_units from (select A.ing as id, json_agg(DISTINCT lower(A.unit))
as units from (select jsonb_array_elements(ingredients)->>'id' as ing, jsonb_array_elements(ingredients)->>'unitLong'
as unit from recipes)A group by A.ing)B;