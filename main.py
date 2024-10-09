import snowflake.connector as sf

# Establishing connection
sf_conn_obj = sf.connect(
    user="test",
    password="test",
    account="test",
    database="test",
    host="snowflake.localhost.localstack.cloud",
)

print("1. Insert lot of rows from a list object to Snowflake table")

try:
    print("2. Creating a cursor object")
    sf_cur_obj = sf_conn_obj.cursor()

    try:
        print("Executing 'show tables' query")
        sf_cur_obj.execute("show tables")
    except Exception as e:
        pass

    print("3. Executing a query on cursor object")
    
    # Creating a new table
    sf_cur_obj.execute(
        "create or replace table "
        "ability(name string, skill string)"
    )

    # Inserting rows into the table
    rows_to_insert = [('John', 'SQL'), ('Alex', 'Java'), ('Pete', 'Snowflake')]
    
    sf_cur_obj.executemany(
        "insert into ability (name, skill) values (%s,%s)", rows_to_insert
    )

    # Executing a SELECT query
    sf_cur_obj.execute("select name, skill from ability")

    print("4. Fetching the results")
    result = sf_cur_obj.fetchall()
    print("Total # of rows:", len(result))
    if result:
        for idx, row in enumerate(result):
            print(f"Row-{idx + 1} => {row}")

except Exception as main_exception:
    print(f"An error occurred during execution: {main_exception}")

finally:
    print("Closing cursor and connection")
    # Closing cursor
    if sf_cur_obj:
        sf_cur_obj.close()
    # Closing connection
    if sf_conn_obj:
        sf_conn_obj.close()
