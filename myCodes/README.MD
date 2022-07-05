**The process we need to follow:**
1. Have a ground truth for at least one year   

    We used FP-Inspector, a ML technique, to label a list of url into FP or no-fp.
    In total, for 2019, we have 92.193 non-fp urls and 1658 fp urls.
2. Gather javascript contents longitudinally

    We used CDX server, an API server by Wayback, to extract existing snapshots since 2010 to 2020.
    To do so:
    
         a.  call myCodes/CDX/wayback_CDX.py for both fp and non_fo urls; the output is a json file in this format:
          {
            "url_id": {
                        "snapshots": [...],
                        "origin" : "normal url",
                        "encoded_url": "encoded_url",
                        "digests" : [...]
                        },
                        ...
          }
3. Extract existing snapshots

    call myCodes/preprocessing/CDX/existing_snapshots.py
            This function go through each json file for each url returned back by CDX and extract unique digests and
             monthly snapshot dates. The output of this function is 2 files: existing_non_fp_snapshots and existing_fp_snapshots
4. Call "available" API from wayback
    for each encoded_url in existing_fp/non_fp_snapshots.json, call "available" API in existing snapshots
    call myCodes/wayback_crawl/CDX/wayback_availability
    Then save the content of existing files in this format:
    yes|hash|snapshot|url_id or no|snapshot|url_id

5. Extract API_keywords (features)
    call myCodes/AST/create_ast.py and then parse_ast.py to extract API_features
    
**Create co-occurrence graph**
6. unify API_features if you've them in different folders

    a. by calling api_feature_file_unify in graph_analysis/api_features_processor.py  
    b. then call extract_uniqueue_apis()
    c. then find_attendency_scripts()
    d.  add_hash_as_key()
    e. calc_fraction()
 7. Then call graph_maker to save graph, nodes, edges, weights, ...






         
   
    