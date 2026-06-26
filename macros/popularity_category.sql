{% macro get_popularity_category(popularity_column) %}
    case
        when {{ popularity_column }} >= 500 then 'Very High'
        when {{ popularity_column }} >= 300 then 'High'
        when {{ popularity_column }} >= 100 then 'Medium'
        else 'Low'
    end
{% endmacro %}