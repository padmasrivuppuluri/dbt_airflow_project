{% macro get_rating_category(rating_column) %}
    case
        when {{ rating_column }} >= 8 then 'Excellent'
        when {{ rating_column }} >= 6 then 'Good'
        when {{ rating_column }} >= 4 then 'Average'
        else 'Low'
    end
{% endmacro %}