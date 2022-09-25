# %%
import pandas as pd
import psycopg2
import numpy as np
import os
from sklearn.cluster import KMeans
from flask import Flask, jsonify
from dotenv import dotenv_values

config = dotenv_values(".env")


viewName = 'vw_usuario_kpi'

queries = {
    'titulo': "SELECT a.attname " +
            "FROM pg_attribute a JOIN pg_class t on a.attrelid = t.oid JOIN pg_namespace s on t.relnamespace = s.oid " +
            "WHERE a.attnum > 0 AND NOT a.attisdropped AND t.relname = '" + viewName + "' AND s.nspname = 'public' " +
            "ORDER BY a.attnum;",
    'usuarioKPI': "select * from " + viewName + ";"
}

def one_hot(categorias, valor):
    categorias = list(set(categorias))

    indice = categorias.index(valor)

    vetor = np.zeros(len(categorias))
    vetor[indice] = 1

    return vetor

# %%
def connect():
    try:
        conn = psycopg2.connect(
            host=config['HOST'],
            database=config['DATABASE'],
            user=config['USER'],
            password=config['PASSWORD']
        )
        return conn
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)


def execute_query(cur, query, conn):
    cur = conn.cursor()
    try:
        cur.execute(query)
        print("Query executed successfully")
        result = cur.fetchall()
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating PostgreSQL table", error)


# %%
def generate_title(columnsResult):
    title = []
    for i in columnsResult:
        title.append(i[0])
    return title


# %%
def generate_df(usuarioKPI, title):
    df = pd.DataFrame(usuarioKPI)
    for n,col in enumerate(title):
        df = df.rename(columns={n:col})

    df = df[df.dt_referencia == max(df.dt_referencia)]

    df = df.drop(['dt_referencia', 'nm_usuario', 'dt_registro','id_plano','vl_plano','qt_jogo_criado','qt_avaliacao','vl_nota','qt_atividade','qt_atividade_login','qt_atividade_cadastro','qt_atividade_jogo','qt_atividade_busca','dt_updated'], axis=1)

    df.nm_plano = [  one_hot(df.nm_plano, _) for _ in df.nm_plano]

    df.set_index('id_usuario', inplace=True)

    return df


# %%
def generate_cluster(df):
    kmeans = KMeans(n_clusters=5, random_state=0).fit(df.values)
    kmeans.labels_
    return kmeans

# %%
def generate_result(df, kmeans):
    id = df.index
    cluster = kmeans.labels_

    result = pd.DataFrame()
    result['id'] = id
    result['group'] = cluster + 2
    result.head(5)
    return result


# %%
def generate_insert_strings(result):
    insertList = []
    for i in range(len(result)):
        line = result.iloc[i]
        insert = "insert into tb_usuario_grupo values(nextval('sq_usuario_grupo'), "+ str(line.id) +", "+ str(line.group) +", 'sim', null, current_timestamp);"
        insertList.append(insert)

    return insertList

# %%
def insert(insertList, conn):
    cur = conn.cursor()
    for i in range(len(insertList)):
        l = insertList[i]
        cur.execute(l)
    cur.execute("commit;")
    cur.close()


# %%
app = Flask(__name__)

# %%
@app.route('/')
def make_request():
    try:
        print('Connecting to database...')
        connection = connect()
        print('Connected to database')

        print('Executing queries...')
        columns_result = execute_query(connection, queries['titulo'], connection)
        usuario_kpi = execute_query(connection, queries['usuarioKPI'], connection)
        print('Queries executed')

        print('Generating title...')
        title = generate_title(columns_result)
        print('Title generated')

        print('Generating dataframe...')
        df = generate_df(usuario_kpi, title)
        print('Dataframe generated')

        print('Generating cluster...')
        kmeans = generate_cluster(df)
        print('Cluster generated')

        print('Generating result...')
        result = generate_result(df, kmeans)
        print('Result generated')

        print('Generating insert strings...')
        insertList = generate_insert_strings(result)
        print('Insert strings generated')

        print('Inserting...')
        insert(insertList, connection)
        print('Inserted')

        print('Calling recomendation engine...')
        connection.cursor().execute("call sp_recomendar_jogo()")
        print('Recomendation generated')

        print('Closing connection...')
        connection.close()
        print('Connection closed')
        
        return jsonify({'status': 'ok'})

    except Exception as e:
        print(e)
        print('Erro ao processar dados!')
        return jsonify({'status': 'error'})


# %%
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
