"""Define IQVIA constants."""
DOMAIN = 'iqvia'

DATA_CLIENT = 'client'
DATA_LISTENER = 'listener'

TOPIC_DATA_UPDATE = 'data_update'

TYPE_ALLERGY_FORECAST = 'allergy_average_forecasted'
TYPE_ALLERGY_INDEX = 'allergy_index'
TYPE_ALLERGY_OUTLOOK = 'allergy_outlook'
TYPE_ALLERGY_TODAY = 'allergy_index_today'
TYPE_ALLERGY_TOMORROW = 'allergy_index_tomorrow'
TYPE_ASTHMA_FORECAST = 'asthma_average_forecasted'
TYPE_ASTHMA_INDEX = 'asthma_index'
TYPE_ASTHMA_TODAY = 'asthma_index_today'
TYPE_ASTHMA_TOMORROW = 'asthma_index_tomorrow'
TYPE_DISEASE_FORECAST = 'disease_average_forecasted'

SENSORS = {
    TYPE_ALLERGY_FORECAST: ('Allergy Index: Forecasted Average', 'mdi:flower'),
    TYPE_ALLERGY_TODAY: ('Allergy Index: Today', 'mdi:flower'),
    TYPE_ALLERGY_TOMORROW: ('Allergy Index: Tomorrow', 'mdi:flower'),
    TYPE_ASTHMA_TODAY: ('Asthma Index: Today', 'mdi:flower'),
    TYPE_ASTHMA_TOMORROW: ('Asthma Index: Tomorrow', 'mdi:flower'),
    TYPE_ASTHMA_FORECAST: ('Asthma Index: Forecasted Average', 'mdi:flower'),
    TYPE_DISEASE_FORECAST: ('Cold & Flu: Forecasted Average', 'mdi:snowflake')
}
