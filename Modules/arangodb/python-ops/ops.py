from __future__ import annotations

import json
import base64
import subprocess
import time
import urllib.parse
import urllib.request
import urllib.error


def arango_http_up(url: str = "http://127.0.0.1:8529/_api/version") -> bool:
    token = base64.b64encode(b"root:test123").decode("ascii")
    req = urllib.request.Request(url, headers={"Authorization": f"Basic {token}"}, method="GET")
    with urllib.request.urlopen(req, timeout=20) as rsp:
        payload = json.loads(rsp.read().decode("utf-8"))
    return payload.get("server") == "arango"


def arango_write_read_via_container(container: str = "arangodb-server") -> str:
    cmd = [
        "docker",
        "exec",
        container,
        "arangosh",
        "--server.endpoint",
        "tcp://127.0.0.1:8529",
        "--server.username",
        "root",
        "--server.password",
        "test123",
        "--javascript.execute-string",
        "if (!db._collection('qa_cli_test')) { db._create('qa_cli_test'); } var key = 'rw_' + Date.now(); db.qa_cli_test.insert({_key:key, k:'verify', v:'ok'}); var d = db.qa_cli_test.document(key); print(JSON.stringify(d));",
    ]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def arango_insert_graph_http(
    database: str = "_system",
    collection: str = "demo_nodes",
    edge_collection: str = "demo_edges",
    base_url: str = "http://127.0.0.1:8529",
) -> dict[str, object]:
    token = base64.b64encode(b"root:test123").decode("ascii")
    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json",
    }

    _ensure_collection(database, collection, base_url, headers, is_edge=False)
    _ensure_collection(database, edge_collection, base_url, headers, is_edge=True)

    now = int(time.time())
    node_a = f"n_{now}_a"
    node_b = f"n_{now}_b"
    edge_k = f"e_{node_a}_{node_b}"

    insert_node = "INSERT { _key: @k, label: @label, group: 'demo' } INTO @@nodes OPTIONS { overwriteMode: 'replace' } RETURN NEW._key"
    _aql_post(
        insert_node,
        {"@nodes": collection, "k": node_a, "label": "Source"},
        database,
        base_url,
        headers,
    )
    _aql_post(
        insert_node,
        {"@nodes": collection, "k": node_b, "label": "Target"},
        database,
        base_url,
        headers,
    )

    insert_edge = (
        "INSERT { _key: @e, _from: CONCAT(@nodes, '/', @a), _to: CONCAT(@nodes, '/', @b), type: 'links' } "
        "INTO @@edges OPTIONS { overwriteMode: 'replace' } RETURN NEW._key"
    )
    _aql_post(
        insert_edge,
        {"@edges": edge_collection, "nodes": collection, "a": node_a, "b": node_b, "e": edge_k},
        database,
        base_url,
        headers,
    )

    return {"a": node_a, "b": node_b, "e": edge_k}


def arango_fetch_graph_http(
    database: str = "_system",
    collection: str = "demo_nodes",
    edge_collection: str = "demo_edges",
    base_url: str = "http://127.0.0.1:8529",
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    token = base64.b64encode(b"root:test123").decode("ascii")
    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json",
    }

    nodes_query = "FOR n IN @@nodes SORT n._key RETURN {id:n._key,label:n.label,group:n.group}"
    edges_query = "FOR e IN @@edges SORT e._key RETURN {id:e._key,from:e._from,to:e._to,type:e.type}"

    nodes = _aql_post(nodes_query, {"@nodes": collection}, database, base_url, headers)
    edges = _aql_post(edges_query, {"@edges": edge_collection}, database, base_url, headers)
    return nodes, edges


def _aql_post(
    query: str,
    bind_vars: dict[str, object],
    database: str,
    base_url: str,
    headers: dict[str, str],
) -> list[dict[str, object]]:
    payload = json.dumps({"query": query, "bindVars": bind_vars}).encode("utf-8")
    endpoint = f"{base_url}/_db/{urllib.parse.quote(database)}/_api/cursor"
    req = urllib.request.Request(endpoint, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=20) as rsp:
        data = json.loads(rsp.read().decode("utf-8"))
    return data.get("result", [])


def _ensure_collection(
    database: str,
    collection: str,
    base_url: str,
    headers: dict[str, str],
    is_edge: bool,
) -> None:
    coll_name = urllib.parse.quote(collection)
    get_url = f"{base_url}/_db/{urllib.parse.quote(database)}/_api/collection/{coll_name}"
    get_req = urllib.request.Request(get_url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(get_req, timeout=20):
            return
    except urllib.error.HTTPError as err:
        if err.code != 404:
            raise

    create_url = f"{base_url}/_db/{urllib.parse.quote(database)}/_api/collection"
    payload = json.dumps({"name": collection, "type": 3 if is_edge else 2}).encode("utf-8")
    create_req = urllib.request.Request(create_url, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(create_req, timeout=20):
        return
