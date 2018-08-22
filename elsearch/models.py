from elasticsearch_dsl import DocType, Date, Completion, Keyword, Text, Integer
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
from elasticsearch_dsl.connections import connections
from .settings import ELSERVER_HOST, ELSERVER_PORT
connections.create_connection(hosts=[ELSERVER_HOST], port=ELSERVER_PORT)


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])


class ArticleType(DocType):
    #伯乐在线文章类型
    suggest = Completion(analyzer=ik_analyzer)
    title = Text(analyzer="ik_max_word")
    create_date = Date()
    url = Keyword()
    url_object_id = Keyword()
    front_image_url = Keyword()
    front_image_path = Keyword()
    praise_nums = Integer()
    comment_nums = Integer()
    fav_nums = Integer()
    tags = Text(analyzer="ik_max_word")
    content = Text(analyzer="ik_max_word")

    class Meta:
        name = 'jobbole'
        doc_type = "article"


class QuestionType(DocType):
    suggest = Completion(analyzer=ik_analyzer)
    title = Text(analyzer="ik_max_word")
    create_date = Date()
    url = Keyword()
    url_object_id = Keyword()
    tags = Text(analyzer="ik_max_word")
    content = Text(analyzer="ik_max_word")

    class Meta:
        index = "zhihu"
        doc_type = "question"


class JobType(DocType):
    suggest = Completion(analyzer=ik_analyzer)
    title = Text(analyzer="ik_max_word")
    create_date = Date()
    url = Keyword()
    url_object_id = Keyword()
    job_type = Text(analyzer="ik_max_word")
    job_city = Keyword()
    job_desc = Text(analyzer="ik_max_word")
    company_name = Text(analyzer="ik_max_word")
    tags = Text(analyzer="ik_max_word")
    job_advantage = Text(analyzer="ik_max_word")
    job_addr = Text(analyzer=ik_analyzer)

    class Meta:
        index = "jobinfo"
        doc_type = "job"


if __name__ == '__main__':
    ArticleType.init()
    QuestionType.init()
    JobType.init()
