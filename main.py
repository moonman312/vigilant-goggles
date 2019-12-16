#####################################################################
# Author: Jacob Mooney and Ashley Stendel
# This program scrapes https://medicalsciences.stackexchange.com/
#####################################################################
import argparse
from api_parser import APIParser
from page_parser import PageParser
from question_summary import QuestionSummary
from tag import Tag
from database_connection import Database
from article import Article

MAX = 9999


def update_tag_table(db):
    """
    updates Tag database table
    :param db: database object
    """
    print("Updating DB...")
    tag_parser = PageParser("tag")
    tags = tag_parser.get_pages(Tag, MAX)
    db.insert_tags(tags)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_pages', type=int)
    parser.add_argument('--update_tag_db', '-u', help='Upsert scraped data to database',
                        required=False, action='store_true')
    args = parser.parse_args()

    results = {}

    db = Database()

    if db.is_empty('Tag'):
        print("Empty DB...")
        update_tag_table(db)

    if args.update_tag_db:
        update_tag_table(db)

    print("Getting Question Summaries...")
    summary_parser = PageParser("question_summary")
    summaries = summary_parser.get_pages(QuestionSummary, args.num_pages)

    #########GET ARTICLES#######################
    article_parser = APIParser()
    articles = article_parser.get_responses(Article, summaries)

    for question_summary, articles_list in zip(summaries, articles):
        question_summary.add_articles(articles_list)

    db.insert_question_summaries(summaries)

if __name__ == '__main__':
    main()
