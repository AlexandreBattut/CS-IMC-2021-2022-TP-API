import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    birthyear=req.params.get('birthyear')
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
    if not birthyear:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('birthyear')

    server = os.environ["TPBDD_SERVER"]
    database = os.environ["TPBDD_DB"]
    username = os.environ["TPBDD_USERNAME"]
    password = os.environ["TPBDD_PASSWORD"]
    driver= '{ODBC Driver 17 for SQL Server}'

    neo4j_server = os.environ["TPBDD_NEO4J_SERVER"]
    neo4j_user = os.environ["TPBDD_NEO4J_USER"]
    neo4j_password = os.environ["TPBDD_NEO4J_PASSWORD"]

    if len(server)==0 or len(database)==0 or len(username)==0 or len(password)==0 or len(neo4j_server)==0 or len(neo4j_user)==0 or len(neo4j_password)==0:
        return func.HttpResponse("Au moins une des variables d'environnement n'a pas été initialisée.", status_code=500)
        
    errorMessage = ""
    dataString = "Number of actors per birth year !\n"
    try:
        logging.info("Test de connexion avec py2neo...")
        graph = Graph(neo4j_server, auth=(neo4j_user, neo4j_password))
#        producers = graph.run("MATCH (n:Name)-[:PRODUCED]->(t:Title) WHERE t.primaryTitle CONTAINS 'Spider-Man' RETURN DISTINCT n.nconst, n.primaryName LIMIT 3")
        if birthyear:
            nbactors=graph.run(f"MATCH (n:Person) WHERE n.birthYear = {birthyear} RETURN count(n)")
            dataString+=f"There were {nbactors} actors born in {birthyear} \n"
        else:
            nbactors=graph.run("MATCH (n:Person) WHERE n.birthYear = 1960 RETURN count(n)")
            dataString+=f"You did not gave a birthyear argument, so by default we show the number of actors born in 1960\n"
            dataString+=f"There were {nbactors} actors born in 1960"
#        for producer in producers:
#            dataString += f"CYPHER: nconst={producer['n.nconst']}, primaryName={producer['n.primaryName']}\n"

        # try:
        #     logging.info("Test de connexion avec pyodbc...")
        #     with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        #         cursor = conn.cursor()
        #         cursor.execute("SELECT TOP(3) tconst, primaryTitle, averageRating FROM [dbo].[tTitles] ORDER BY averageRating DESC")

        #         rows = cursor.fetchall()
        #         for row in rows:
        #             dataString += f"SQL: tconst={row[0]}, primaryTitle={row[1]}, averageRating={row[2]}\n"


        # except:
        #     errorMessage = "Erreur de connexion a la base SQL"
    except:
        errorMessage = "Erreur de connexion a la base Neo4j"
        
    
    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
    if errorMessage != "":
        return func.HttpResponse(dataString + nameMessage + errorMessage, status_code=500)

    else:
        return func.HttpResponse(dataString + nameMessage)