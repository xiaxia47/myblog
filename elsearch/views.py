from django.shortcuts import render
import json
from django.views.generic.base import View
from django.http import HttpResponse
from elasticsearch import Elasticsearch
from datetime import datetime
import redis
from .settings import *
from elasticsearch.exceptions import ConnectionTimeout
from elasticsearch_dsl import Search
client = Elasticsearch(hosts=[{"host":ELSERVER_HOST,"port":ELSERVER_PORT}],)
redis_cli = redis.StrictRedis(host=REDIS_SERVER, port=REDIS_PORT, password=REDIS_PASSWORD,decode_responses=True)


DEFAULT_DOCUMENT = 'jobbole'



class IndexView(View):
    def get(self, request):
        topn_search = redis_cli.zrevrangebyscore("search_keywords_set", "+inf", "-inf", start=0, num=5)
        topn_search = [content.split('-') for content in topn_search]
        return render(request, "elsearch/index.html", {"topn_search": topn_search})


class SearchSuggest(View):
    def get(self, request):
        key_words = request.GET.get('s','')
        key_type = request.GET.get('doc', DEFAULT_DOCUMENT)
        try:
            doc = Search(index=key_type)
        except KeyError:
            doc = Search(index=DEFAULT_DOCUMENT)
        re_datas = []
        try:
            if key_words:
                s = doc.suggest('my_suggest', key_words,
                               completion={
                                   "field":"suggest",
                                   "fuzzy":{
                                       "fuzziness":2
                                   },
                                   "size": 5})
                suggestions = s.execute()
                for match in suggestions.suggest.my_suggest[0].options:
                    source = match._source
                    re_datas.append(str(source['title']))
        except ConnectionTimeout as e:
            print(e)

        return HttpResponse(json.dumps(re_datas), content_type="application/json")


class SearchView(View):
    def get(self, request):
        key_word = request.GET.get("query","")
        index = request.GET.get("doc", DEFAULT_DOCUMENT)
        key_comb = '-'.join([key_word, index])
        redis_cli.zincrby("search_keywords_set",key_comb)
        topn_search = redis_cli.zrevrangebyscore("search_keywords_set","+inf","-inf",start=0,num=5)
        topn_search = [content.split('-') for content in topn_search]
        page = request.GET.get("p", "1")
        try:
            page = int(page)
        except:
            page = 1
        cnt = {}
        cnt["jobbole"] = redis_cli.get("jobbole_cnt")
        cnt["zhihu"] = redis_cli.get("zhihu_cnt")
        cnt["jobinfo"]= redis_cli.get("jobinfo_cnt")
        start_time = datetime.now()
        response = client.search(
            index=index,
            body={
                "query":{
                    "multi_match":{
                        "query":key_word,
                        "fields":["tages","title","content"]
                    }
                },
                "from":(page-1)*10,
                "size":10,
                "highlight":{
                    "pre_tags":['<span class="keyWord">'],
                    "post_tags":['</span>'],
                    "fields":{
                        "title":{},
                        "content":{},
                    }
                }
            }
        )
        end_time = datetime.now()
        last_seconds = (end_time - start_time).total_seconds()
        total_nums = response["hits"]["total"]
        if (page%10) >0:
            page_nums = int(total_nums/10) + 1
        else:
            page_nums = int(total_nums/10)
        hit_hist = []
        for hit in response["hits"]["hits"]:
            hit_dict = {}
            if "title" in hit["highlight"]:
                hit_dict["title"] = "".join(hit["highlight"]["title"])
            else:
                hit_dict["title"] = hit["_source"]["title"]
            if "content" in hit["highlight"]:
                hit_dict["content"] = "".join(hit["highlight"]["content"])[:500]
            else:
                hit_dict["content"] = hit["_source"]["content"][:500]

            hit_dict["create_date"] = hit["_source"]["create_date"]
            hit_dict["url"] = hit["_source"]["url"]
            hit_dict["source"] = hit["_source"]["source"]
            hit_dict["score"] = hit["_score"]
            hit_hist.append(hit_dict)
        return render(request, "elsearch/result.html", {"page":page,
                                               "doc":index,
                                               "all_hits":hit_hist,
                                               "key_words":key_word,
                                               "total_nums":total_nums,
                                               "page_nums":page_nums,
                                               "last_seconds":last_seconds,
                                               "cnt":cnt,
                                               "topn_search":topn_search})
