""" QuestionSummary class contains the fields of a question summary
 """


class QuestionSummary:

    HTML_TAG = "div"
    KEYWORD = "question-summary"

    def __init__(self, parser=None):
        self.ref = None
        self.vote_count = None
        self.answer_count = None
        self.view_count = None
        self.question = None
        self.tags = None
        self.date = None
        self.parser = parser

    def pretty_print(self):

        info = (
                f'Question Text: {self.question}\n'
                f'Votes: {self.vote_count}\n'
                f'Answers: {self.answer_count}\n'
                f'Views: {self.view_count}\n'
                f'Tags: {self.tags}\n'
                f'Date Posted: {self.date}\n'
                f'URL: {self.ref}\n'
                )
        print(info)

    def scrape_info(self, match):
        """
        sets the fields of a QuestionSummary from the html snippet
        :param match: html segment containing question summary
        """
        self.ref = self.parser.get_match_other("a", "question-hyperlink", match, 'href')
        self.vote_count = self.parser.get_match_int("div", "votes", match)
        self.answer_count = self.parser.get_match_int("div", "status", match)
        self.view_count = self.parser.get_match_int("div", "views", match)
        self.question = self.parser.get_match_text("a", "question-hyperlink", match)
        self.tags = self.parser.get_match_tags("a", "post-tag", match)
        self.date = self.parser.get_match_other("span", "relativetime", match, 'title')

    def __str__(self):
        return str(self.__dict__)

    def get_attributes(self):
        return self.__dict__
