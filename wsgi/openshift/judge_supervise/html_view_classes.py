from decimal     import Decimal, getcontext

class CountFeedbackRow(object):
    """ Collection of data
    """
    def __init__(self, feedback, total, prob_count_list):
        self.feedback = feedback
        self.total = total
        self.prob_count_list = prob_count_list

class ProblemAttempsCount(object):
    """ Collection of data
    """
    def _get_ratio(self):
        getcontext().prec = 2

        if self.successfull == 0:
            return 0
        if self.failed == 0:
            return self.successfull

        return (Decimal(self.successfull) / Decimal(self.failed))

    def __init__(self, problem, failed, successfull):
        self.problem = problem
        self.failed = failed
        self.successfull = successfull
        self.total = failed + successfull
        self.success_ratio = self._get_ratio()

class SubFeedbackView(object):
    """ Return some random feedback"""
    def __init__(self, submission, feedback=None):
        if not feedback:
            not_executed = "Not executed"
            self.feedback = not_executed
            self.retval = not_executed
            self.command = not_executed
            self.stderr = not_executed
            self.stdout = not_executed
        else:
            self.feedback = feedback
            self.retval = feedback.retval
            self.command = '\n' + feedback.command.replace('\n', '\\n')
            self.stderr = feedback.stderr
            self.stdout = feedback.stdout

        self.submissions = submission
        self.file_content = '\n' + submission.submission.read()
        self.problem= submission.problem
        self.date_uploaded = submission.date_uploaded

        self.subtext = submission.submission

class TeamSummaryRow(object):
    """ Collection of data
    """
    def __init__(self, team, fail_count, prev_solved,
                 site_location = ''):
        self.team = team
        self.fail_count = fail_count
        self.prev_solved = prev_solved
        self.site_location = site_location

# EOF
