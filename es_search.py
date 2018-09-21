from elasticsearch import Elasticsearch

if __name__ == "__main__":
    es = Elasticsearch(
        hosts=[{
            "host": "0.0.0.0",
            "port": 9200,
        }]
    )
    res = es.search(
        index="products_list_spider",
        doc_type="apple"
    )
    print(res)
