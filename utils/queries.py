FIVE_ROWS = "SELECT * FROM TRANSACTIONS LIMIT 5"
CARDS_DESC_STATS = """WITH 
                    total_trans AS (
                    SELECT COUNT(1) AS total FROM transactions
                    ),
                    fraud_total AS (
                    SELECT COUNT(1) AS total_fraud FROM transactions WHERE is_fraud = TRUE
                    ),
                    max_min_amount AS (
                    SELECT 
                        MAX(trans_amount) AS max_amount,
                        MIN(trans_amount) AS min_amount
                    FROM transactions
                    )
                    SELECT 
                    t.total, 
                    f.total_fraud, 
                    m.max_amount, 
                    m.min_amount
                    FROM total_trans t
                    JOIN fraud_total f ON 1=1
                    JOIN max_min_amount m ON 1=1;"""
TRANS_MONTH = """SELECT
                DATE_PART('month', trans_date_trans_time) AS mes,
                COUNT(1) AS "total transacciones"
                FROM transactions
                GROUP BY mes
                ORDER BY "total transacciones" DESC;"""
TRANS_WEEKDAY = """SELECT
                CASE
                    WHEN DATE_PART('dow', trans_date_trans_time) = 0 THEN 'Domingo'
                    WHEN DATE_PART('dow', trans_date_trans_time) = 1 THEN 'Lunes'
                    WHEN DATE_PART('dow', trans_date_trans_time) = 2 THEN 'Martes'
                    WHEN DATE_PART('dow', trans_date_trans_time) = 3 THEN 'Miércoles'
                    WHEN DATE_PART('dow', trans_date_trans_time) = 4 THEN 'Jueves'
                    WHEN DATE_PART('dow', trans_date_trans_time) = 5 THEN 'Viernes'
                    WHEN DATE_PART('dow', trans_date_trans_time) = 6 THEN 'Sábado'
                END AS "dia de la semana",
                COUNT(1) AS "total transacciones"
            FROM transactions
            GROUP BY DATE_PART('dow', trans_date_trans_time)
            ORDER BY "total transacciones" DESC;"""
FRAUD_1K_MONTH = """with
fraud_trans AS (
  SELECT
    CASE 
      WHEN extract('month' from  trans_date_trans_time) = 1 THEN 'Enero'
      WHEN extract('month' from  trans_date_trans_time) = 2 THEN 'Febrero'
      WHEN extract('month' from  trans_date_trans_time) = 3 THEN 'Marzo'
      WHEN extract('month' from  trans_date_trans_time) = 4 THEN 'Abril'
      WHEN extract('month' from  trans_date_trans_time) = 5 THEN 'Mayo'
      WHEN extract('month' from  trans_date_trans_time) = 6 THEN 'Junio'
      WHEN extract('month' from  trans_date_trans_time) = 7 THEN 'Julio'
      WHEN extract('month' from  trans_date_trans_time) = 8 THEN 'Agosto'
      WHEN extract('month' from  trans_date_trans_time) = 9 THEN 'Septiembre'
      WHEN extract('month' from  trans_date_trans_time) = 10 THEN 'Octubre'
      WHEN extract('month' from  trans_date_trans_time) = 11 THEN 'Noviembre'
      WHEN extract('month' from  trans_date_trans_time) = 12 THEN 'Diciembre'
    END AS "mes",
    count(1) AS "total"
  FROM transactions
  WHERE is_fraud = True
  GROUP BY extract('month' from  trans_date_trans_time)
),
month_trans AS (
  SELECT
    CASE 
      WHEN extract('month' from  trans_date_trans_time) = 1 THEN 'Enero'
      WHEN extract('month' from  trans_date_trans_time) = 2 THEN 'Febrero'
      WHEN extract('month' from  trans_date_trans_time) = 3 THEN 'Marzo'
      WHEN extract('month' from  trans_date_trans_time) = 4 THEN 'Abril'
      WHEN extract('month' from  trans_date_trans_time) = 5 THEN 'Mayo'
      WHEN extract('month' from  trans_date_trans_time) = 6 THEN 'Junio'
      WHEN extract('month' from  trans_date_trans_time) = 7 THEN 'Julio'
      WHEN extract('month' from  trans_date_trans_time) = 8 THEN 'Agosto'
      WHEN extract('month' from  trans_date_trans_time) = 9 THEN 'Septiembre'
      WHEN extract('month' from  trans_date_trans_time) = 10 THEN 'Octubre'
      WHEN extract('month' from  trans_date_trans_time) = 11 THEN 'Noviembre'
      WHEN extract('month' from  trans_date_trans_time) = 12 THEN 'Diciembre'
    END AS "mes",
    COUNT(1) AS total_transacciones
  FROM transactions
  GROUP BY mes
)
select 
  f.mes,
  total,
  total_transacciones,
  ROUND((total::numeric(7,2)/total_transacciones)*1000,0) AS "fraudes c/1000"
FROM fraud_trans f JOIN month_trans m ON f.mes=m.mes
ORDER BY "fraudes c/1000" DESC; 
"""
FRAUD_1K_WEEKDAY = """with
fraud_trans AS (
  SELECT
    CASE
        WHEN DATE_PART('dow', trans_date_trans_time) = 0 THEN 'Domingo'
        WHEN DATE_PART('dow', trans_date_trans_time) = 1 THEN 'Lunes'
        WHEN DATE_PART('dow', trans_date_trans_time) = 2 THEN 'Martes'
        WHEN DATE_PART('dow', trans_date_trans_time) = 3 THEN 'Miércoles'
        WHEN DATE_PART('dow', trans_date_trans_time) = 4 THEN 'Jueves'
        WHEN DATE_PART('dow', trans_date_trans_time) = 5 THEN 'Viernes'
        WHEN DATE_PART('dow', trans_date_trans_time) = 6 THEN 'Sábado'
    END AS dia_semana,
    count(1) AS "total"
  FROM transactions
  WHERE is_fraud = True
  GROUP BY DATE_PART('dow', trans_date_trans_time)
),
weekday_trans AS (
  SELECT
    CASE
        WHEN DATE_PART('dow', trans_date_trans_time) = 0 THEN 'Domingo'
        WHEN DATE_PART('dow', trans_date_trans_time) = 1 THEN 'Lunes'
        WHEN DATE_PART('dow', trans_date_trans_time) = 2 THEN 'Martes'
        WHEN DATE_PART('dow', trans_date_trans_time) = 3 THEN 'Miércoles'
        WHEN DATE_PART('dow', trans_date_trans_time) = 4 THEN 'Jueves'
        WHEN DATE_PART('dow', trans_date_trans_time) = 5 THEN 'Viernes'
        WHEN DATE_PART('dow', trans_date_trans_time) = 6 THEN 'Sábado'
    END AS dia_semana,
    COUNT(1) AS total_transacciones
  FROM transactions
  GROUP BY DATE_PART('dow', trans_date_trans_time)
)
select 
  f.dia_semana AS "dia de la semana",
  total,
  total_transacciones,
  ROUND((total::numeric(7,2)/total_transacciones)*1000,0) AS "fraudes c/1000"
FROM fraud_trans f JOIN weekday_trans w ON f.dia_semana=w.dia_semana
ORDER BY "fraudes c/1000" DESC; 
"""
FRAUD_1K_TIME = """with
fraud_trans AS (
  SELECT
    DATE_PART('hour', trans_date_trans_time) AS "hora",
    count(1) AS "total"
  FROM transactions
  WHERE is_fraud = True
  GROUP BY DATE_PART('hour', trans_date_trans_time)
),
time_trans AS (
  SELECT
    DATE_PART('hour', trans_date_trans_time) AS "hora",
    COUNT(1) AS total_transacciones
  FROM transactions
  GROUP BY DATE_PART('hour', trans_date_trans_time)
)
select 
  f.hora,
  total,
  total_transacciones,
  ROUND((total::numeric(7,2)/total_transacciones)*1000,0) AS "fraudes c/1000"
FROM fraud_trans f JOIN time_trans t ON f.hora=t.hora
ORDER BY f.hora ASC; 
"""
FRAUD_1K_CATEGORY = """WITH top_categories AS (
    SELECT
        category,
        COUNT(1) AS total_transacciones
    FROM transactions
    GROUP BY category
), trans_fraud AS (
  select 
    category,
    COUNT(1) AS fraud_trans
  FROM transactions
  WHERE is_fraud = true
  GROUP BY category
)
SELECT
    t.category AS categorias,
    t.total_transacciones,
    f.fraud_trans,
    ROUND((f.fraud_trans::numeric(7,2)/t.total_transacciones)*1000,0) AS "fraudes c/1000"
FROM top_categories t JOIN trans_fraud f ON t.category = f.category
ORDER BY "fraudes c/1000" DESC
LIMIT 5;
"""
FRAUD_1K_STATE = """WITH frauds AS (
  select 
    state_code,
    count(1) AS fraud_trans
  FROM transactions
  WHERE is_fraud = true
  GROUP BY state_code
),
state_pop AS (
  select
  state_code,
  SUM(city_population) AS state_population
FROM (
    SELECT
        city, state_code,
        city_population,
        ROW_NUMBER() OVER(PARTITION BY state_code, city ORDER BY city_population DESC) AS row_num
    FROM transactions) as subq
WHERE row_num = 1
GROUP BY state_code
)
select
  s.state_code AS "código estado",
  s.state_population,
  f.fraud_trans,
  ROUND((f.fraud_trans::numeric(10,2)/s.state_population)*1000,1) AS "fraudes c/1000"
FROM frauds f JOIN state_pop s ON f.state_code = s.state_code
ORDER BY "fraudes c/1000" DESC
LIMIT 5;
"""
CORR_POB_FRAUD = """
with
state_pop as (
  select
  state_code,
  SUM(city_population) AS state_population
FROM (
    SELECT
        city, state_code,
        city_population,
        ROW_NUMBER() OVER(PARTITION BY state_code, city ORDER BY city_population DESC) AS row_num
    FROM transactions) as subq
WHERE row_num = 1
GROUP BY state_code
),
state_fraud AS (
  select
    s.state_code,
    s.state_population,
    COUNT(t.id) AS "transacciones_fraudulentas"
  FROM state_pop s JOIN transactions t ON s.state_code = t.state_code
  WHERE t.is_fraud = true
  GROUP BY s.state_code,s.state_population
)
select
  corr(state_population,transacciones_fraudulentas)::numeric(4,2) AS "corr población fraude"
FROM state_fraud;
"""
CITY_MAX_FRAUD = """
SELECT
  city AS "ciudad",
  state_code AS "código estado",
  SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS "transacciones fraudulentas"
FROM transactions
GROUP BY ciudad,state_code
ORDER BY "transacciones fraudulentas" desc
LIMIT 1;
"""
CITY_MAX_TRANS = """
SELECT
  city AS "ciudad",
  state_code AS "código estado",
  sum(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS "transacciones no fraudulentas",
  count(1) AS "transacciones totales"
FROM transactions
GROUP BY ciudad,state_code
ORDER BY "transacciones totales" desc
LIMIT 1;
"""
FRAUD_GENDER = """
SELECT
    gender as "género",
    SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS "fraudes"
FROM
    transactions
GROUP BY
    gender
ORDER BY
    "fraudes";
"""
FRAUD_AGE = """
SELECT
  CASE 
    WHEN ('2020-12-31'::date-dob)/365 < 30 THEN '<30'
    WHEN ('2020-12-31'::date-dob)/365 between 30 AND 40 THEN '30-40'
    WHEN ('2020-12-31'::date-dob)/365 between 41 AND 50 THEN '40-50'
    WHEN ('2020-12-31'::date-dob)/365 between 51 AND 60 THEN '50-60'
    WHEN ('2020-12-31'::date-dob)/365 > 60 THEN '>60'
  END AS edad,
  COUNT(1) AS "fraudes"
FROM transactions
WHERE is_fraud = true
GROUP BY edad
ORDER BY "fraudes" DESC;
"""
FRAUD_JOB = """
SELECT
  job AS "trabajos",
  COUNT(1) AS "fraudes"
FROM transactions
WHERE is_fraud = true
GROUP BY job
ORDER BY "fraudes" DESC
LIMIT 5;
"""
